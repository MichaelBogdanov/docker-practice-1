struct Recipe {
    title: String,
    ingredients: Vec<String>,
    steps: String,
}

struct AppState {
    recipes: Vec<Recipe>,
}

struct QueryHas {
    has: Option<String>,
}

struct QueryInclude {
    include: String,
}

struct Response {
    status: String,
    message: String,
}

fn main() {
    println!("Hello, world!");
}