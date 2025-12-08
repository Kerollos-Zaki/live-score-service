from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

MATCHES = [
    # MATCH 1: Bayern vs Dortmund (Starts at 30 minutes)
    {
        "match_id": 1005, 
        "timeline": [
            {"score": "1-0", "minute": 30}, # <--- STARTS AT 30'
            {"score": "1-1", "minute": 45},
            {"score": "2-1", "minute": 60},
            {"score": "2-2", "minute": 75},
            {"score": "3-2", "minute": 90}
        ]
    },
    # MATCH 2: Ahly vs Zamalek (Cairo Derby - Kickoff)
    {
        "match_id": 1008, 
        "timeline": [
            {"score": "0-0", "minute": 1},
            {"score": "1-0", "minute": 15}, # Ahly Goal
            {"score": "1-1", "minute": 35}, # Zamalek Equalizer
            {"score": "2-1", "minute": 70}, # Ahly Goal
            {"score": "2-1", "minute": 90}  # FT
        ]
    },
    # MATCH 3: Milan vs Inter (Kickoff)
    {
        "match_id": 1006, 
        "timeline": [
            {"score": "0-0", "minute": 1},
            {"score": "0-1", "minute": 20},
            {"score": "1-1", "minute": 50},
            {"score": "1-2", "minute": 88},
            {"score": "1-2", "minute": 90}
        ]
    }
]

print(f"⚽ Starting Derby Night Simulation...")
print(f"   - Bayern: Starts at 30'")
print(f"   - Ahly vs Zamalek: Kickoff")

# Find the longest game
max_steps = max(len(m["timeline"]) for m in MATCHES)

for step in range(max_steps):
    for game in MATCHES:
        if step < len(game["timeline"]):
            update = game["timeline"][step]
            
            message = {
                "match_id": game["match_id"],
                "score": update["score"],
                "minute": update["minute"]
            }
            
            producer.send('match_updates', message)
            print(f"📢 Match {game['match_id']}: {update['score']} ({update['minute']}')")
    
    time.sleep(4) 

print("🏁 All Matches Finished!")
