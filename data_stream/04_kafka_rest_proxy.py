import json
import requests

REST_PROXY_URL = "http://localhost:8082"

def get_topics():
    """Gets topics from REST Proxy"""
    resp = requests.get(f"{REST_PROXY_URL}/topics")

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get topics: {e}", file=sys.stderr)
        print(json.dumps(resp.json(), indent=2), file=sys.stderr)
        return []

    return resp.json()

def get_topic(topic_name):
    """Get specific details on a topic"""
    resp = requests.get(f"{REST_PROXY_URL}/topics/{topic_name}")

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get topic {topic_name}: {e}", file=sys.stderr)
        print(json.dumps(resp.json(), indent=2), file=sys.stderr)
        return

    return resp.json()

def get_brokers():
    """Gets broker information"""
    resp = requests.get(f"{REST_PROXY_URL}/brokers")

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get brokers: {e}", file=sys.stderr)
        print(json.dumps(resp.json(), indent=2), file=sys.stderr)
        return

    return resp.json()

def get_partitions(topic_name):
    """Prints partition information for a topic"""
    resp = requests.get(f"{REST_PROXY_URL}/topics/{topic_name}/partitions")

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get partitions for topic {topic_name}: {e}", file=sys.stderr)
        print(json.dumps(resp.json(), indent=2), file=sys.stderr)
        return

    return resp.json()

if __name__ == "__main__":
    import sys
    
    topics = get_topics()
    if topics:
        print(json.dumps({"topics": topics}, indent=2))
        
        topic_info = get_topic(topics[0])
        if topic_info:
            print(json.dumps({"topic_info": topic_info}, indent=2))

        brokers = get_brokers()
        if brokers:
            print(json.dumps({"brokers": brokers}, indent=2))

        partitions = get_partitions(topics[-1])
        if partitions:
            print(json.dumps({"partitions": partitions}, indent=2))
