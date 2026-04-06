using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Concurrent;

namespace JokesPracticeDocker.Controllers
{
    [ApiController]
    [Route("")]
    public class JokesController : ControllerBase
    {
        private static readonly ConcurrentDictionary<int, Joke> _jokes = new();
        private static int _nextId = 1;

        static JokesController()
        {
            AddInitialJoke("Why do programmers prefer dark mode? Because light attracts bugs!", "programming");
            AddInitialJoke("Why is 6 afraid of 7? Because 7 ate 9!", "math");
            AddInitialJoke("What do you call a fake noodle? An impasta!", "food");
        }

        private static void AddInitialJoke(string text, string category)
        {
            var joke = new Joke
            {
                Id = _nextId++,
                Text = text,
                Category = category,
                Votes = new Votes()
            };
            _jokes.TryAdd(joke.Id, joke);
        }

        [HttpGet("jokes")]
        public IActionResult GetJokes([FromQuery] string? category)
        {
            var jokes = _jokes.Values.AsEnumerable();

            if (!string.IsNullOrEmpty(category))
            {
                jokes = jokes.Where(j => j.Category == category);
            }

            return Ok(jokes.Select(j => new
            {
                j.Id,
                j.Text,
                j.Category,
                j.Votes
            }));
        }

        [HttpGet("jokes/random")]
        public IActionResult GetRandomJoke([FromQuery] string? category)
        {
            var jokes = _jokes.Values.AsEnumerable();

            if (!string.IsNullOrEmpty(category))
            {
                jokes = jokes.Where(j => j.Category == category);
            }

            var jokesList = jokes.ToList();
            if (jokesList.Count == 0)
            {
                return NotFound(new { error = "No jokes found" });
            }

            var random = new Random();
            var joke = jokesList[random.Next(jokesList.Count)];

            return Ok(new
            {
                joke.Id,
                joke.Text,
                joke.Category,
                joke.Votes
            });
        }

        [HttpPost("jokes")]
        public IActionResult AddJoke([FromBody] AddJokeRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Text) || string.IsNullOrWhiteSpace(request.Category))
            {
                return BadRequest(new { error = "Missing required fields: text, category" });
            }

            var joke = new Joke
            {
                Id = _nextId++,
                Text = request.Text,
                Category = request.Category,
                Votes = new Votes()
            };

            _jokes.TryAdd(joke.Id, joke);

            return CreatedAtAction(nameof(GetJokes), new { id = joke.Id }, new
            {
                joke.Id,
                joke.Text,
                joke.Category,
                joke.Votes
            });
        }

        [HttpPost("jokes/{id}/vote")]
        public IActionResult VoteJoke(int id, [FromBody] VoteRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Vote) || (request.Vote != "up" && request.Vote != "down"))
            {
                return BadRequest(new { error = "Vote must be 'up' or 'down'" });
            }

            if (!_jokes.TryGetValue(id, out var joke))
            {
                return NotFound(new { error = "Joke not found" });
            }

            if (request.Vote == "up")
            {
                joke.Votes.Up++;
            }
            else
            {
                joke.Votes.Down++;
            }

            return Ok(new
            {
                message = $"Voted {request.Vote} on joke {id}",
                votes = joke.Votes
            });
        }
    }
}
