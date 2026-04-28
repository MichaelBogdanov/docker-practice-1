#!/usr/bin/env bash


curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"omelette","ingredients":["egg","milk"],"steps":"mix and fry"}'

echo

curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"pancakes","ingredients":["egg","milk","flour"],"steps":"mix and cook"}'

echo

curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"salad","ingredients":["tomato","cucumber","oil"],"steps":"cut and mix"}'

echo

curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"fried egg","ingredients":["egg","oil"],"steps":"fry the egg"}'

echo

curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"milkshake","ingredients":["milk","banana"],"steps":"blend everything"}'

echo

curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"pizza toast","ingredients":["bread","tomato","cheese"],"steps":"assemble and bake"}'

echo
echo "----- all recipes -----"
curl "http://localhost:3000/recipes" | jq

echo
echo "----- has=egg -----"
curl "http://localhost:3000/recipes?has=egg" | jq