namespace YourProject.Models;

public class ImageMetadata
{
    public int Id { get; set; }
    public string Url { get; set; } = string.Empty;
    public int Width { get; set; }
    public int Height { get; set; }
    public List<string> Tags { get; set; } = new();
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public class CreateImageRequest
{
    public string Url { get; set; } = string.Empty;
    public int Width { get; set; }
    public int Height { get; set; }
    public List<string> Tags { get; set; } = new();
}