using Microsoft.AspNetCore.Mvc;

namespace EventStreamLab.Controllers;

[Route("api/[controller]")]
[ApiController]
public class HealthController : ControllerBase
{
    [HttpPost("check")]
    public IActionResult Check([FromBody] EventData eventData)
    {
        return Ok("All working");
    }
}

