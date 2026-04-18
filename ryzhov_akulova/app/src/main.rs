#![allow(dead_code)]

use axum::{
    routing::{get, post},
    http::StatusCode,
    Json,
    Router,
};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
struct Recipe {
    title: String,
    ingredients: Vec<String>,
    steps: String,
}

#[derive(Clone)]
struct AppState {
    recipes: Vec<Recipe>,
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
struct Response {
    status: String,
    message: String,
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/recipes", get(get_recipes).post(post_recipe))
        .route("/recipes/random", get(random_recipe));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();
    println!("Server running on http://localhost:3000");

    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, from axum"
}

async fn get_recipes() -> &'static str {
    "Hello from get_recipes func"
}

async fn random_recipe() -> &'static str {
    "Hello from random_recipe func"
}

async fn post_recipe(Json(recipe): Json<Recipe>) -> (StatusCode, Json<Recipe>) {
    println!("{:?}", recipe);
    (StatusCode::CREATED, Json(Recipe { title: recipe.title, ingredients: recipe.ingredients, steps: recipe.steps }))
}