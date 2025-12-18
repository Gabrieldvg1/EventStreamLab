namespace EventStreamLab;
public interface IKafkaProducerService
{
    Task ProduceAsync(string topic, EventData eventData);
}

