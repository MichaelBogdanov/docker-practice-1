curl -X POST http://localhost:3000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"omelette","ingredients":["egg","milk"],"steps":"mix and fry"}'

curl "http://localhost:3000/recipes"

curl "http://localhost:3000/"