#!/usr/bin/env python3
"""
Simple script to generate sample security events for testing
"""

import json
import time
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

def create_sample_events(count=10):
    """Generate sample security events"""
    event_types = [
        "login_attempt", "malware_detected", "network_scan", 
        "data_exfiltration", "privilege_escalation", "suspicious_process"
    ]
    
    severities = ["low", "medium", "high", "critical"]
    sources = ["siem", "edr", "ndr", "email_security"]
    
    events = []
    
    for i in range(count):
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
            "event_type": random.choice(event_types),
            "source": random.choice(sources),
            "source_ip": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            "user": f"user_{random.randint(1000, 9999)}",
            "asset": f"asset_{random.randint(100, 999)}",
            "severity": random.choice(severities),
            "status": random.choice(["success", "failed", "blocked", "quarantined"]),
            "description": f"Sample {random.choice(event_types).replace('_', ' ')} event for testing"
        }
        events.append(event)
    
    return events

def save_sample_data():
    """Save sample events to JSON files"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data/sample-events")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate different sized datasets
        small_events = create_sample_events(10)
        medium_events = create_sample_events(100)
        large_events = create_sample_events(1000)
        
        # Save to files
        files_created = []
        
        with open(data_dir / "sample_events_small.json", 'w') as f:
            json.dump(small_events, f, indent=2)
            files_created.append("sample_events_small.json (10 events)")
        
        with open(data_dir / "sample_events_medium.json", 'w') as f:
            json.dump(medium_events, f, indent=2)
            files_created.append("sample_events_medium.json (100 events)")
        
        with open(data_dir / "sample_events_large.json", 'w') as f:
            json.dump(large_events, f, indent=2)
            files_created.append("sample_events_large.json (1000 events)")
        
        print("✅ Sample security events generated successfully!")
        print(f"📁 Location: {data_dir.absolute()}")
        print("\n📊 Files created:")
        for file_info in files_created:
            print(f"  - {file_info}")
        
        # Show sample event
        print(f"\n📋 Sample event:")
        print(json.dumps(small_events[0], indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        return False

def send_to_kafka_via_docker():
    """Send sample events to Kafka using Docker exec (no Python dependencies needed)"""
    try:
        import subprocess
        
        events = create_sample_events(5)
        
        print("📤 Sending sample events to Kafka...")
        
        for i, event in enumerate(events, 1):
            event_json = json.dumps(event)
            
            # Use docker exec to send message to Kafka
            cmd = [
                "docker", "exec", "-i", "agentic-soc-kafka",
                "kafka-console-producer", 
                "--bootstrap-server", "localhost:9092",
                "--topic", "security-events"
            ]
            
            result = subprocess.run(
                cmd, 
                input=event_json, 
                text=True, 
                capture_output=True
            )
            
            if result.returncode == 0:
                print(f"  ✅ Sent event {i}: {event['event_type']}")
            else:
                print(f"  ❌ Failed to send event {i}: {result.stderr}")
        
        print("\n🎉 Sample events sent to Kafka topic 'security-events'")
        print("🔍 View in Kafka UI: http://localhost:8081")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending to Kafka: {e}")
        print("💡 Make sure Docker containers are running: docker-compose ps")
        return False

if __name__ == "__main__":
    print("🚀 Generating sample security events...")
    print()
    
    # Always create JSON files
    save_success = save_sample_data()
    
    print()
    
    # Try to send to Kafka
    kafka_success = send_to_kafka_via_docker()
    
    if save_success:
        print(f"\n✨ Sample data is ready for development and testing!")
    else:
        print(f"\n⚠️  Some operations failed. Check the errors above.")