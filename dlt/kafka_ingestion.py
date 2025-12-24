import dlt
from pyspark.sql.functions import col

def _read_event_hubs_kafka_stream():
    """
    Reads from Azure Event Hubs via its Kafka-compatible endpoint, using
    configuration and secrets passed from the DLT pipeline.
    """
    bootstrap_server = spark.conf.get("BOOTSTRAP_SERVER")
    topic = spark.conf.get("EVENT_HUB_TOPIC")
    secret_scope = spark.conf.get("EVENT_HUB_SECRET_SCOPE")
    secret_key = spark.conf.get("EVENT_HUB_SECRET_KEY")

    if not bootstrap_server or not topic:
        raise ValueError("BOOTSTRAP_SERVER and EVENT_HUB_TOPIC must be set in the pipeline configuration.")

    if not secret_scope or not secret_key:
        raise ValueError("EVENT_HUB_SECRET_SCOPE and EVENT_HUB_SECRET_KEY must be set in the pipeline configuration.")

    # Get the Event Hubs connection string from Databricks secrets
    connection_string = dbutils.secrets.get(secret_scope, secret_key)

    # Kafka options for Azure Event Hubs (Kafka endpoint)
    kafka_options = {
        "kafka.bootstrap.servers": bootstrap_server,
        "subscribe": topic,
        "startingOffsets": "latest",
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.sasl.jaas.config": f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{connection_string}";',
    }

    return (
        spark.readStream
        .format("kafka")
        .options(**kafka_options)
        .load()
    )


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

    # Keep it simple: just cast the Kafka value to string and keep the event timestamp
    return df.select(
        col("value").cast("string").alias("value"),
        col("timestamp").alias("ingest_ts"),
    )
