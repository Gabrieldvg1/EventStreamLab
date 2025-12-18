using Microsoft.AspNetCore.Mvc;

namespace EventStreamLab.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EventsController : ControllerBase
    {
        private readonly IKafkaProducerService _kafka;
        private readonly string _topic;

        public EventsController(IKafkaProducerService kafka, IConfiguration configuration)
        {
            _kafka = kafka;
            _topic = configuration["Kafka:Topic"] ?? throw new Exception("Kafka:Topic is missing");
        }

        [HttpPost("publish")]
        public async Task<IActionResult> PublishEvent([FromBody] EventData eventData)
        {
            await _kafka.ProduceAsync(_topic, eventData);
            return Ok("Event sent to Kafka");
        }
    }
}
