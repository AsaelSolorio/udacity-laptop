import faust
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# Define the Avro schema for deserialization
value_schema_str = """
{
    "type": "record",
    "name": "click_event",
    "namespace": "udacity",
    "fields": [
        {"name": "email", "type": "string"},
        {"name": "timestamp", "type": "string"},
        {"name": "uri", "type": "string"},
        {"name": "number", "type": "int"}
    ]
}
"""

# Initialize Schema Registry Client (not directly used in Faust)
schema_registry_conf = {'url': 'http://localhost:8082'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Create an AvroDeserializer instance
avro_deserializer = AvroDeserializer(schema_str=value_schema_str, schema_registry_client=schema_registry_client)

# Create a Faust application
app = faust.App(
    'avro-consumer',
    broker='kafka://localhost:9092',
    value_serializer='raw'  # Use raw serializer for binary data
)

# Define a topic and Avro deserializer function
topic = app.topic('udacity', value_type=bytes)  # Define your topic here

# Define a Faust agent to consume Avro messages
@app.agent(topic)
async def consume_avro(avro_messages):
    async for message in avro_messages:
        # Deserialize Avro message using avro_deserializer
        deserialized_message = avro_deserializer(message, ctx=None)  # Pass ctx=None to satisfy the argument requirement
        # Process your deserialized Avro message here
        print(deserialized_message)

if __name__ == '__main__':
    app.main()
