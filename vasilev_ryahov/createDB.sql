CREATE TABLE IF NOT EXISTS ingredient (
    ingredient_id SERIAL PRIMARY KEY, 
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS recipe (
    recipe_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    steps TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe_ingredient (
    recipe_id INT NOT NULL REFERENCES recipe(recipe_id) ON DELETE CASCADE,
    ingredient_id INT NOT NULL REFERENCES ingredient(ingredient_id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE INDEX IF NOT EXISTS idx_recipe_ingredient_ingredient_id ON recipe_ingredient (ingredient_id);
CREATE INDEX IF NOT EXISTS idx_recipe_ingredient_recipe_id ON recipe_ingredient (recipe_id);

INSERT INTO ingredient (name) VALUES 
    ('egg'), 
    ('milk'), 
    ('tomato'), 
    ('eggplant'), 
    ('zucchini'), 
    ('onion'),
    ('salt'),
    ('flour')
ON CONFLICT (name) DO NOTHING;

INSERT INTO recipe (title, steps) VALUES 
    ('Recipe 1', 'Step 1. Step 2. Step 3.'),
    ('Recipe 2', 'Step 1. Step 2. Step 3.');

INSERT INTO recipe_ingredient (recipe_id, ingredient_id)
SELECT r.recipe_id, i.ingredient_id FROM recipe r, ingredient i
WHERE r.title = 'Recipe 1' AND i.name IN ('egg', 'milk', 'salt')
ON CONFLICT DO NOTHING;

INSERT INTO recipe_ingredient (recipe_id, ingredient_id)
SELECT r.recipe_id, i.ingredient_id FROM recipe r, ingredient i
WHERE r.title = 'Recipe 2' AND i.name IN ('tomato', 'onion', 'salt')
ON CONFLICT DO NOTHING;