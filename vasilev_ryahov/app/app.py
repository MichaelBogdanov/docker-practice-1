from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
import asyncpg

from database import lifespan, get_db_connection
from recipes import (
    create_recipe, get_recipes, get_random_recipe, get_recipe_by_id
)

class RecipeCreate(BaseModel):
    title: str
    ingredients: list[str]
    steps: str

class RecipeResponse(BaseModel):
    recipe_id: int
    title: str
    ingredients: list[str]
    steps: str

app = FastAPI(title="Recipe API", lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "name": "Recipe API",
        "endpoints": {
            "POST /recipes": "Создать рецепт",
            "GET /recipes": "Получить все рецепты",
            "GET /recipes?has=milk,egg": "Рецепты с milk и egg",
            "GET /recipes?has=milk,egg&match=any": "Рецепты с milk или egg",
            "GET /recipes/random": "Случайный рецепт",
            "GET /recipes/random?include=milk": "Случайный с milk",
            "GET /health": "Статус сервиса",
        }
    }

@app.post("/recipes", response_model=RecipeResponse, status_code=201)
async def create_new_recipe(
    recipe: RecipeCreate,
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Создание нового рецепта"""
    try:
        recipe_id = await create_recipe(
            conn=conn,
            title=recipe.title,
            steps=recipe.steps,
            ingredients=recipe.ingredients
        )
        
        created = await get_recipe_by_id(conn, recipe_id)
        
        if not created:
            raise HTTPException(500, "Рецепт создан, но не найден")
        
        return RecipeResponse(**created)
    
    except Exception as e:
        raise HTTPException(400, f"Ошибка: {str(e)}")

@app.get("/recipes", response_model=list[RecipeResponse])
async def list_recipes(
    has: str | None = Query(None, description="Ингредиенты через запятую"),
    match: str = Query("all", description="all (все) | any (любой)"),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Получение рецептов с фильтрацией по ингредиентам"""
    ingredients = [i.strip() for i in has.split(",")] if has else None
    recipes = await get_recipes(conn, ingredients, match)
    return [RecipeResponse(**recipe) for recipe in recipes]

@app.get("/recipes/random", response_model=RecipeResponse) 
async def random_recipe(
    include: str | None = Query(None, description="Ингредиенты через запятую"),
    match: str = Query("all", description="all (все) | any (любой)"),
    conn: asyncpg.Connection = Depends(get_db_connection)        
):
    """Случайный рецепт с фильтрацией по ингредиентам"""
    ingredients = [i.strip() for i in include.split(",")] if include else None
    recipe = await get_random_recipe(conn, ingredients, match)
    
    if not recipe:
        raise HTTPException(404, "Рецепты не найдены")    
    
    return RecipeResponse(**recipe)

@app.get("/health")
async def health_check(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Проверка подключения к базе данных"""
    await conn.fetchval("SELECT 1")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)