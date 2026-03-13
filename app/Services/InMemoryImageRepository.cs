using YourProject.Models;

namespace YourProject.Services;

public class InMemoryImageRepository : IImageRepository
{
    private readonly List<ImageMetadata> _images = new();
    private int _nextId = 1;

    public IEnumerable<ImageMetadata> GetAll(string? tag = null)
    {
        if (string.IsNullOrWhiteSpace(tag))
            return _images;

        return _images.Where(img => img.Tags.Contains(tag, StringComparer.OrdinalIgnoreCase));
    }

    public ImageMetadata? GetById(int id)
    {
        return _images.FirstOrDefault(img => img.Id == id);
    }

    public ImageMetadata Add(CreateImageRequest request)
    {
        var image = new ImageMetadata
        {
            Id = _nextId++,
            Url = request.Url,
            Width = request.Width,
            Height = request.Height,
            Tags = request.Tags
        };

        _images.Add(image);
        return image;
    }
}