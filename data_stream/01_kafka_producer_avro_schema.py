##PRODUCER

import asyncio
import random
from faker import Faker
from dataclasses import asdict, dataclass, field
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

# Define the Avro schema for the ClickEvent
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

# Define the Avro schema for the Id (key)
key_schema_str = """
{
    "namespace": "example.avro",
    "type": "record",
    "name": "Id",
    "fields": [
        {"name": "id", "type": "int"}
    ]
}
"""

# Configuration for Kafka Producer
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

# Configuration for Schema Registry
schema_registry_conf = {
    'url': 'http://localhost:8082',
}

# Initialize the Schema Registry Client
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Initialize the AvroSerializer for Kafka value
avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=value_schema_str
)

# Initialize the StringSerializer for Kafka key
string_serializer = StringSerializer("utf_8")

# Create the Kafka producer
producer = Producer(producer_conf)

# Initialize Faker for generating fake data
faker = Faker()

@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)
    number: int = field(default_factory=lambda: random.randint(0, 999))

    def serialize(self):
        """Serializes the ClickEvent for sending to Kafka"""
        return asdict(self)

async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    while True:
        try:
            event = ClickEvent()
            key = f"{event.email}-{event.timestamp}"
            serialized_event = avro_serializer(event.serialize(), SerializationContext(topic_name, MessageField.VALUE))
            serialized_key = string_serializer(key, SerializationContext(topic_name, MessageField.KEY))
            producer.produce(topic=topic_name, key=serialized_key, value=serialized_event)
            producer.flush()
            await asyncio.sleep(1.0)
        except Exception as e:
            print(f"Exception in produce: {e}")
            break

def main():
    """Starts the asyncio event loop for producing Kafka messages"""
    try:
        asyncio.run(produce("udacity"))
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()

