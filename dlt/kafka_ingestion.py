import json
import dlt
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# ---- Read configuration from databricks.yml ----
config = {
    "flows": json.loads(spark.conf.get("FLOWS")),
    "bootstrap_server": spark.conf.get("BOOTSTRAP_SERVER"),
    "secret_scope": spark.conf.get("EVENT_HUB_SECRET_SCOPE"),
    "secret_key": spark.conf.get("EVENT_HUB_SECRET_KEY"),
}

# ---- Load Event Hubs connection string ----
connection_string = dbutils.secrets.get(
    config["secret_scope"],
    config["secret_key"],
)

def _read_kafka(topic: str) -> DataFrame:
    kafka_options = {
        "kafka.bootstrap.servers": config["bootstrap_server"],
        "subscribe": topic,
        "startingOffsets": "latest",
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.sasl.jaas.config": (
            'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule '
            f'required username="$ConnectionString" password="{connection_string}";'
        ),
    }

    return (
        spark.readStream
        .format("kafka")
        .options(**kafka_options)
        .load()
    )

def _create_raw_table(topic_name: str, table_name: str) -> None:
    @dlt.table(
        name=table_name,
        comment=f"Raw events from Kafka topic {topic_name}",
        table_properties={"quality": "bronze"},
    )
    def _table() -> DataFrame:
        df = _read_kafka(topic_name)
        return df.select(
            col("value").cast("string").alias("value"),
            col("timestamp").alias("ingest_ts"),
        )

    # Register dynamically so DLT can discover it
    globals()[table_name] = _table

# ---- Create one raw table per flow ----
for flow in config["flows"]:
    _create_raw_table(
        topic_name=flow["topic_name"],
        table_name=flow["table_name"],
    )
