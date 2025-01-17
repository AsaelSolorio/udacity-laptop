import json
import os
from confluent_kafka import Producer, KafkaError

# Configuration for the Kafka producer
kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Update this with your Kafka broker address
}

# Create a Kafka producer instance
producer = Producer(**kafka_config)


# Read the JSON file and produce each record to Kafka
def produce_json_to_kafka(file_path, topic):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                try:
                    # Parse the JSON line
                    record = json.loads(line)
                    
                    # Convert the record to a string
                    record_str = json.dumps(record)
                    
                    # Produce the record to Kafka
                    producer.produce(topic, value=record_str)
                    
                    # Poll to trigger delivery reports
                    producer.poll(1)
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error on line: '{line}'\nError: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"IO error: {e}")
    print("messages delivered")

    # Wait for any outstanding messages to be delivered
    producer.flush()

if __name__ == "__main__":
    # Get the current working directory
    cwd = os.getcwd()
    # Path to the JSON file in the current working directory
    json_file_path = os.path.join(cwd, 'bank-deposits.json')  # Ensure your JSON file is named 'atm_withdrawals.json'
    kafka_topic = 'bank-deposits'  # Update with your Kafka topic
    
    # Produce the JSON records to Kafka
    produce_json_to_kafka(json_file_path, kafka_topic)
