using YourProject.Models;

namespace YourProject.Services;

public interface IImageRepository
{
    IEnumerable<ImageMetadata> GetAll(string? tag = null);
    ImageMetadata? GetById(int id);
    ImageMetadata Add(CreateImageRequest request);
}