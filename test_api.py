# test_api.py
"""
Simple API testing script for MindMate chatbot.
Tests the /chat endpoint with various scenarios.

Run:
    python test_api.py
"""

import requests
import json
from typing import List, Dict
import time

API_URL = "http://localhost:8000"
SESSION_ID = f"test_session_{int(time.time())}"

def test_chat(message: str) -> Dict:
    """Send a message to the chatbot and return response."""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "session_id": SESSION_ID,
                "message": message
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def test_health() -> bool:
    """Check if API is healthy."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test_scenarios():
    """Run comprehensive test scenarios."""
    print("=" * 70)
    print("MINDMATE API TEST SUITE")
    print("=" * 70)
    
    # Check health
    print("\n1. Health Check...")
    if test_health():
        print("   ✓ API is healthy")
    else:
        print("   ✗ API is not responding. Make sure to start the server:")
        print("     uvicorn app:app --host 0.0.0.0 --port 8000")
        return
    
    # Test scenarios
    scenarios = [
        {
            "category": "Normal Conversation",
            "messages": [
                "Hello, how are you?",
                "I'm feeling a bit stressed about work",
                "Thank you for listening"
            ]
        },
        {
            "category": "Emotion Detection - Sadness",
            "messages": [
                "I'm feeling really sad today",
                "I feel lonely and isolated",
                "Everything feels overwhelming"
            ]
        },
        {
            "category": "Emotion Detection - Joy",
            "messages": [
                "I'm so happy! I got the promotion!",
                "Today was an amazing day",
                "I feel grateful for everything"
            ]
        },
        {
            "category": "Emotion Detection - Anger",
            "messages": [
                "I'm so frustrated with everything!",
                "This makes me really angry",
                "I can't believe they did that to me"
            ]
        },
        {
            "category": "Emotion Detection - Fear",
            "messages": [
                "I'm scared about the future",
                "I'm anxious about my health",
                "What if everything goes wrong?"
            ]
        },
        {
            "category": "Crisis Detection - CRITICAL",
            "messages": [
                "I want to end my life",
                "I'm planning to kill myself tonight"
            ]
        },
        {
            "category": "Crisis Detection - Concerning",
            "messages": [
                "I feel worthless and hopeless",
                "Nobody would care if I disappeared"
            ]
        },
        {
            "category": "Memory & Context",
            "messages": [
                "My name is Alex",
                "I've been having trouble sleeping",
                "Do you remember what I told you earlier?"
            ]
        }
    ]
    
    print("\n" + "=" * 70)
    print("RUNNING TEST SCENARIOS")
    print("=" * 70)
    
    for scenario in scenarios:
        print(f"\n{'=' * 70}")
        print(f"Category: {scenario['category']}")
        print(f"{'=' * 70}")
        
        for i, message in enumerate(scenario['messages'], 1):
            print(f"\n[{i}] User: {message}")
            
            response = test_chat(message)
            
            if response:
                print(f"    Emotion: {response.get('emotion', 'N/A')}")
                print(f"    Crisis: {response.get('crisis', False)}")
                print(f"    Bot: {response.get('response', 'N/A')[:200]}...")
                
                # Add delay to simulate natural conversation
                time.sleep(1)
            else:
                print("    ✗ Failed to get response")
                break
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
    print("\nNote: Check the responses for:")
    print("  1. Appropriate emotion detection")
    print("  2. Empathetic and contextual responses")
    print("  3. Proper crisis handling with helpline info")
    print("  4. Conversation memory and context awareness")

def interactive_mode():
    """Interactive testing mode."""
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("Type your messages to chat with MindMate.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    if not test_health():
        print("✗ API is not responding. Please start the server first.")
        return
    
    while True:
        try:
            message = input("You: ").strip()
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not message:
                continue
            
            response = test_chat(message)
            
            if response:
                print(f"\n[Emotion: {response.get('emotion')}]")
                if response.get('crisis'):
                    print("[⚠️  CRISIS DETECTED]")
                print(f"Bot: {response.get('response')}\n")
            else:
                print("Failed to get response. Please try again.\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        run_test_scenarios()
        
        print("\n" + "=" * 70)
        print("Want to try interactive mode?")
        print("Run: python test_api.py interactive")
        print("=" * 70)
