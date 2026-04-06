namespace JokesPracticeDocker
{
    public class Joke
    {
        public int Id { get; set; }
        public string Text { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public Votes Votes { get; set; } = new Votes();
    }
}
