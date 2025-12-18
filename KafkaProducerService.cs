using System.Text.Json;
using Confluent.Kafka;

namespace EventStreamLab;
public class KafkaProducerService : IKafkaProducerService
{
    private readonly IProducer<Null, string> _producer;

    public KafkaProducerService(IConfiguration configuration)
    {
        var bootstrapServers  = configuration["Kafka:BootstrapServers"] 
                                ?? throw new Exception("Kafka:BootstrapServers is missing");

        // For Azure Event Hubs' Kafka endpoint we authenticate using SASL/SSL,
        // with the Event Hubs connection string as the password.
        var connectionString = configuration["Kafka:ConnectionString"]
                               ?? configuration["EventHubConnectionString"]
                               ?? throw new Exception("Kafka:ConnectionString or EventHubConnectionString is missing");

        var config = new ProducerConfig
        {
            BootstrapServers = bootstrapServers,
            SecurityProtocol = SecurityProtocol.SaslSsl,
            SaslMechanism    = SaslMechanism.Plain,
            SaslUsername     = "$ConnectionString",
            SaslPassword     = connectionString
        };

        _producer = new ProducerBuilder<Null, string>(config).Build();
    }

    public async Task ProduceAsync(string topic, EventData eventData)
    {
        if (string.IsNullOrWhiteSpace(topic)) throw new ArgumentException("Topic cannot be empty");

        var message = new Message<Null, string>
        {
            Value = JsonSerializer.Serialize(eventData)
        };

        await _producer.ProduceAsync(topic, message);
    }
}

