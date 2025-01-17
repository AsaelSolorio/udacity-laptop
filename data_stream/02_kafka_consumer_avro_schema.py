#CONSUMER 

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.serialization import StringDeserializer
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

# Initialize Schema Registry Client
schema_registry_conf = {'url': 'http://localhost:8082'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Define the Avro Deserializer for the 'click_event' schema
avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=value_schema_str
)

string_deserializer = StringDeserializer('utf_8')

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.deserializer': string_deserializer,
    'value.deserializer': avro_deserializer,
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(['udacity'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        print(f"Consumed record with key {msg.key()} and value {msg.value()}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
