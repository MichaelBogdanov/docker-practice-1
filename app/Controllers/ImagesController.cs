using Microsoft.AspNetCore.Mvc;
using YourProject.Models;
using YourProject.Services;

namespace YourProject.Controllers;

[ApiController]
[Route("images")]
public class ImagesController : ControllerBase
{
    private readonly IImageRepository _repository;

    public ImagesController(IImageRepository repository)
    {
        _repository = repository;
    }

    [HttpGet]
    public IActionResult GetImages([FromQuery] string? tag)
    {
        var images = _repository.GetAll(tag);
        return Ok(images);
    }

    [HttpGet("{id}")]
    public IActionResult GetImage(int id)
    {
        var image = _repository.GetById(id);

        if (image == null)
            return NotFound(new { message = $"Image with id {id} not found" });

        return Ok(image);
    }

    [HttpPost]
    public IActionResult CreateImage([FromBody] CreateImageRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Url))
            return BadRequest(new { message = "URL is required" });

        if (request.Width <= 0 || request.Height <= 0)
            return BadRequest(new { message = "Width and height must be positive numbers" });

        var image = _repository.Add(request);

        // Return 201 Created with location header
        return CreatedAtAction(nameof(GetImage), new { id = image.Id }, image);
    }
}