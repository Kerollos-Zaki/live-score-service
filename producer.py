print("1. Starting Worker...")
from kafka import KafkaConsumer
import json
import redis
from pymongo import MongoClient
import sys

# --- CONFIGURATION ---
print("2. Connecting to services...")

# Connect to Redis & Mongo
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
mongo_client = MongoClient("mongodb://localhost:27017")
matches_collection = mongo_client["live_score_db"]["matches"]

# Connect to Kafka
try:
    consumer = KafkaConsumer(
        'match_updates',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print("✅ Worker is READY and LISTENING for updates...")
except Exception as e:
    print(f"❌ Kafka Error: {e}")
    sys.exit(1)

# --- LISTENING LOOP ---
for message in consumer:
    try:
        data = message.value
        match_id = data['match_id']
        score = data['score']
        minute = data['minute']

        print(f"📥 Received Goal: {score} ({minute}') -> Updating Match {match_id}")

        # Update DB
        matches_collection.update_one(
            {"match_id": match_id},
            {"$set": {"score": score, "minute": minute}}
        )

        # Update Redis
        current_match = matches_collection.find_one({"match_id": match_id})
        if current_match:
            del current_match['_id']
            redis_client.set(f"match:{match_id}", json.dumps(current_match))
            
    except Exception as e:
        print(f"⚠ Error processing message: {e}")
