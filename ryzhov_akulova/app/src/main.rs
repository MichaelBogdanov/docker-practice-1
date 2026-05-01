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
    include: String,
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

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();
    println!("Server running on http://localhost:3000");

    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, from axum"
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
) -> Result<Json<Recipe>, (StatusCode, Json<ErrorResponse>)> {
    let recipes = state.recipes.lock().unwrap().clone();
    let mut rng = rand::rng();
    
    if recipes.is_empty() {
        return Err((
            StatusCode::BAD_REQUEST, 
            Json(ErrorResponse { 
                message: String::from("An empty list"),
            }),
        ));
    }

    let number_of_recipes = recipes.len();
    let index: u32 = rng.random::<u32>() % number_of_recipes as u32;
    
    if let Some(recipe ) = recipes.get(index as usize).cloned() {
        Ok(Json(recipe))
    } else { 
        return Err((
            StatusCode::NOT_FOUND, 
            Json(ErrorResponse { 
                message: String::from("An empty list"),
            }),
        ));
    }
    
}

async fn post_recipe(
    State(state): State<AppState>,
    Json(recipe): Json<Recipe>
) -> Result<StatusCode, (StatusCode, Json<ErrorResponse>)> {
    println!("{:?}", recipe);
    let mut recipes = state.recipes.lock().unwrap();
    recipes.push(recipe);

    Ok(StatusCode::CREATED)
}