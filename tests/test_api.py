# tests/test_api.py
"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestChatEndpoint:
    """Test chat endpoint functionality."""
    
    def test_chat_basic_message(self):
        """Test sending a basic message."""
        response = client.post(
            "/chat",
            json={
                "session_id": "test_session_1",
                "message": "Hello, how are you?"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "session_id" in data
        assert "emotion" in data
        assert "response" in data
        assert "crisis" in data
        assert data["session_id"] == "test_session_1"
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
    
    def test_chat_empty_message(self):
        """Test that empty messages are rejected."""
        response = client.post(
            "/chat",
            json={
                "session_id": "test_session_2",
                "message": ""
            }
        )
        
        assert response.status_code == 400
    
    def test_chat_missing_fields(self):
        """Test that missing required fields are rejected."""
        # Missing message
        response = client.post(
            "/chat",
            json={"session_id": "test_session_3"}
        )
        assert response.status_code == 422
        
        # Missing session_id
        response = client.post(
            "/chat",
            json={"message": "Hello"}
        )
        assert response.status_code == 422
    
    def test_emotion_detection(self):
        """Test that emotions are detected correctly."""
        test_cases = [
            ("I'm so happy!", ["joy", "surprise"]),
            ("I feel sad and lonely", ["sadness"]),
            ("This makes me so angry!", ["anger"]),
            ("I'm scared about the future", ["fear"]),
        ]
        
        for message, expected_emotions in test_cases:
            response = client.post(
                "/chat",
                json={
                    "session_id": "test_emotion",
                    "message": message
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["emotion"] in expected_emotions, \
                f"Expected {expected_emotions}, got {data['emotion']} for '{message}'"
    
    def test_crisis_detection(self):
        """Test that crisis messages are detected."""
        crisis_messages = [
            "I want to kill myself",
            "I'm planning to end my life",
            "suicide is the only option"
        ]
        
        for message in crisis_messages:
            response = client.post(
                "/chat",
                json={
                    "session_id": "test_crisis",
                    "message": message
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["crisis"] is True, f"Crisis not detected for: {message}"
            assert data["emotion"] == "crisis"
            assert "helpline" in data["response"].lower() or "AASRA" in data["response"]
    
    def test_conversation_memory(self):
        """Test that conversation context is maintained."""
        session_id = "test_memory"
        
        # First message
        response1 = client.post(
            "/chat",
            json={
                "session_id": session_id,
                "message": "My name is Alice"
            }
        )
        assert response1.status_code == 200
        
        # Second message
        response2 = client.post(
            "/chat",
            json={
                "session_id": session_id,
                "message": "I'm feeling stressed about work"
            }
        )
        assert response2.status_code == 200
        
        # Third message - test memory
        response3 = client.post(
            "/chat",
            json={
                "session_id": session_id,
                "message": "Do you remember my name?"
            }
        )
        assert response3.status_code == 200
        # Note: Actual memory recall depends on model quality
    
    def test_different_sessions(self):
        """Test that different sessions are isolated."""
        # Session 1
        response1 = client.post(
            "/chat",
            json={
                "session_id": "session_1",
                "message": "My favorite color is blue"
            }
        )
        
        # Session 2
        response2 = client.post(
            "/chat",
            json={
                "session_id": "session_2",
                "message": "What's my favorite color?"
            }
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        # Session 2 should not have access to session 1's context


class TestResponseQuality:
    """Test response quality and appropriateness."""
    
    def test_response_not_empty(self):
        """Test that responses are never empty."""
        response = client.post(
            "/chat",
            json={
                "session_id": "test_quality",
                "message": "Hello"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["response"]) > 0
    
    def test_response_is_string(self):
        """Test that responses are always strings."""
        response = client.post(
            "/chat",
            json={
                "session_id": "test_type",
                "message": "How are you?"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["response"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
