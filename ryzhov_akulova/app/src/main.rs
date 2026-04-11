#![allow(dead_code)]

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

#[derive(Serialize, Deserialize, Debug)]
struct Foo {
    message: String,
}

fn main() {
    println!("Hello, world!");

    let struct1 = Foo { message: String::from("hello from foo") }; 

    let serialized = serde_json::to_string(&struct1).unwrap();

    println!("{}", serialized);

    let deserialized: Foo = serde_json::from_str(&serialized).unwrap();

    println!("{:?}", deserialized);
}