import dlt
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

def _read_event_hubs_kafka_stream():
    """
    Reads from Azure Event Hubs via its Kafka-compatible endpoint using
    configuration and secrets passed from the DLT pipeline.
    """
    # Hardcoded values can be replaced by spark.conf if you want them configurable
    bootstrap_server = "eventstreamlab-ns.servicebus.windows.net:9093"
    topic = "demo-events"

    # Fetch Event Hubs connection string securely from Databricks secrets
    connection_string = dlt.secrets.get(scope="event-hubs", key="connection-string")

    # Kafka options for Event Hubs (Kafka endpoint)
    kafka_options = {
        "kafka.bootstrap.servers": bootstrap_server,
        "subscribe": topic,
        "startingOffsets": "latest",
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.sasl.jaas.config": f'org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{connection_string}";',
    }

    return spark.readStream.format("kafka").options(**kafka_options).load()


@dlt.table(
    name="events_raw",
    comment="Raw events consumed from Azure Event Hubs (Kafka endpoint) from EventStreamLab API.",
    table_properties={"quality": "bronze"},
)
def events_raw():
    """
    Bronze DLT table with raw Kafka messages.
    """
    df = _read_event_hubs_kafka_stream()

    # Keep it simple: cast Kafka value to string and keep the timestamp
    return df.select(
        col("value").cast("string").alias("value"),
        col("timestamp").alias("ingest_ts"),
    )
