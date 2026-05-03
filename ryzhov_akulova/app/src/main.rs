#![allow(dead_code)]

use std::{sync::{Arc, Mutex}};

use axum::{
    routing::get,
    http::StatusCode,
    Json,
    Router,
    extract::{State, Query},
};

use serde::{Serialize, Deserialize};

use rand::{prelude::*};

#[derive(Serialize, Deserialize, Clone, Debug, Default)]
struct Recipe {
    title: String,
    ingredients: Vec<String>,
    steps: String,
}

#[derive(Clone)]
struct AppState {
    recipes: Arc<Mutex<Vec<Recipe>>>,
}

#[derive(Deserialize)]
struct QueryHas {
    has: Option<String>,
}

#[derive(Deserialize)]
struct QueryInclude {
    include: Option<String>,
}

#[derive(Serialize, Deserialize)]
struct ErrorResponse {
    message: String,
}

#[tokio::main]
async fn main() {
    let shared_state = AppState { recipes: Arc::new(Mutex::new(vec![])) };

    let app = Router::new()
        .route("/", get(root))
        .route("/recipes", get(get_recipes).post(post_recipe))
        .route("/recipes/random", get(random_recipe))
        .with_state(shared_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    println!("Server running on http://localhost:3000");

    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello from axum"
}

async fn get_recipes(
    State(state): State<AppState>,
    Query(query): Query<QueryHas>
) -> Json<Vec<Recipe>> {
    let recipes = state.recipes.lock().unwrap().clone();
    if let Some(has) = query.has {
        let has_ingredients: Vec<String> = has.split(',').map(|item| item.trim().to_lowercase()).collect();
        
        let filtered_recipes: Vec<Recipe> = 
            recipes
            .iter()
            .filter(|recipe| {
                has_ingredients.iter().all(|wanted| {
                    recipe.ingredients.contains(wanted)
                })
            }).cloned().collect();

        Json(filtered_recipes)
    } else {
        Json(recipes)
    }
}

async fn random_recipe(
    State(state): State<AppState>,
    Query(query): Query<QueryInclude>,
) -> Result<Json<Recipe>, (StatusCode, Json<ErrorResponse>)> {
    let recipes = state.recipes.lock().unwrap().clone();
    
    if recipes.is_empty() {
        return Err((
            StatusCode::NOT_FOUND, 
            Json(ErrorResponse { 
                message: String::from("An empty list"),
            }),
        ));
    }
    
    let candidate_recipes: Vec<Recipe> = match query.include {
        Some(include) => {
            let include_ingredients: Vec<String> = include.split(',').map(|item| item.trim().to_lowercase()).collect();
            let filtered_recipes: Vec<Recipe> = 
            recipes
                .iter()
                .filter(|recipe| {
                    include_ingredients.iter().all(|wanted| {
                        recipe.ingredients.contains(wanted)
                    }) 
                }).cloned().collect();
                
            filtered_recipes
        },
        None => {
            recipes
        }
    };

    if candidate_recipes.is_empty() {
        return Err((
            StatusCode::NOT_FOUND,
            Json(ErrorResponse { 
                message: "An empty list after filter".to_string() 
            })
        ))
    }
    
    let number_of_recipes = candidate_recipes.len();
    let mut rng = rand::rng();
    let index: u32 = rng.random::<u32>() % number_of_recipes as u32;
    
    if let Some(recipe ) = candidate_recipes.get(index as usize).cloned() {
        Ok(Json(recipe))
    } else { 
        return Err((
            StatusCode::NOT_FOUND, 
            Json(ErrorResponse { 
                message: "An empty list".to_string(),
            }),
        ));
    }
}


async fn post_recipe(
    State(state): State<AppState>,
    Json(recipe): Json<Recipe>
) -> StatusCode {
    let mut recipes = state.recipes.lock().unwrap();
    recipes.push(recipe);

    StatusCode::CREATED
}