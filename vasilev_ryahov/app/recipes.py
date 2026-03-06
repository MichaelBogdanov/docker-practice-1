import random

import asyncpg

async def create_recipe(
    conn: asyncpg.Connection, 
    title: str,
    steps: str,
    ingredients: list[str]
) -> int:
    """Создание рецепта (и добавление ингредиентов, которых не существует в таблице)"""
    async with conn.transaction():
        recipe_id = await conn.fetchval(
            "INSERT INTO recipe (title, steps) VALUES ($1, $2) RETURNING recipe_id",
            title, steps
        )
        
        unique_ingredients = list(set(ingredients))
        
        ingredient_ids = [
            row["ingredient_id"] 
            for row in await conn.fetch("""
                WITH new_ingredients AS (
                    INSERT INTO ingredient (name)
                    SELECT * FROM UNNEST($1::TEXT[])
                    ON CONFLICT (name) DO NOTHING
                    RETURNING ingredient_id
                )
                SELECT ingredient_id FROM new_ingredients
                UNION
                SELECT ingredient_id FROM ingredient 
                WHERE name = ANY($1)
            """, unique_ingredients)
        ]
        
        await conn.executemany("""
            INSERT INTO recipe_ingredient (recipe_id, ingredient_id)
            VALUES ($1, $2)
        """, [(recipe_id, ing_id) for ing_id in ingredient_ids])
        
        return recipe_id

async def get_recipes(
    conn: asyncpg.Connection,
    ingredients: list[str] | None = None,
    match: str = "all"
) -> list[dict]:
    """ 
    Получение рецептов с фильтрацией по ингредиентам.

    match:
    - any: хотя бы один из списка
    - all: все из списка (можно больше)
    """
    
    if not ingredients:
        rows = await conn.fetch("""
            SELECT
                r.recipe_id,
                r.title,
                ARRAY_AGG(DISTINCT i.name) as ingredients,
                r.steps
            FROM recipe r
            LEFT JOIN recipe_ingredient ri USING (recipe_id)
            LEFT JOIN ingredient i USING (ingredient_id)
            GROUP BY r.recipe_id, r.title, r.steps
            ORDER BY r.recipe_id
        """)
    elif ingredients and match == "any":
        rows = await conn.fetch("""
            SELECT
                r.recipe_id,
                r.title,
                ARRAY_AGG(DISTINCT i.name ORDER BY i.name) as ingredients,
                r.steps
            FROM recipe r
            JOIN recipe_ingredient ri USING (recipe_id)
            JOIN ingredient i USING (ingredient_id)
            WHERE i.name = ANY($1::text[])
            GROUP BY r.recipe_id, r.title, r.steps
            ORDER BY r.recipe_id
        """, ingredients)
    else:
        rows = await conn.fetch("""
        SELECT
            r.recipe_id,
            r.title,
            ARRAY_AGG(DISTINCT i.name ORDER BY i.name) as ingredients,
            r.steps
        FROM recipe r
        JOIN recipe_ingredient ri USING (recipe_id)
        JOIN ingredient i USING (ingredient_id)
        WHERE EXISTS (
            SELECT 1
            FROM recipe_ingredient ri2
            JOIN ingredient i2 USING (ingredient_id)
            WHERE ri2.recipe_id = r.recipe_id
            AND i2.name = ANY($1::text[])
            GROUP BY ri2.recipe_id
            HAVING COUNT(DISTINCT i2.name) = $2
        )
        GROUP BY r.recipe_id, r.title, r.steps
        ORDER BY r.recipe_id
        """, ingredients, len(ingredients))

    return [
        {
            "recipe_id": row["recipe_id"],
            "title": row["title"],
            "ingredients": list(row["ingredients"]) if row["ingredients"] else [],
            "steps": row["steps"],
        }
        for row in rows
    ]

async def get_random_recipe(
    conn: asyncpg.Connection,
    ingredients: list[str] | None = None,
    match: str = "all"
) -> dict:
    """Случайный рецепт"""
    recipes = await get_recipes(conn, ingredients, match)
    return random.choice(recipes) if recipes else None

async def get_recipe_by_id(conn: asyncpg.Connection, recipe_id: int) -> dict | None:
    """Рецепт по ID"""
    row = await conn.fetchrow("""
        SELECT
            r.recipe_id,
            r.title,
            ARRAY_AGG(DISTINCT i.name ORDER BY i.name) as ingredients,
            r.steps
        FROM recipe r
        LEFT JOIN recipe_ingredient ri ON r.recipe_id = ri.recipe_id
        LEFT JOIN ingredient i ON ri.ingredient_id = i.ingredient_id
        WHERE r.recipe_id = $1
        GROUP BY r.recipe_id, r.title, r.steps
    """, recipe_id)

    if row:
        return {
            "recipe_id": row["recipe_id"],
            "title": row["title"],
            "ingredients": list(row["ingredients"]) if row["ingredients"] else [],
            "steps": row["steps"],
        }
    return None