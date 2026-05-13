import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivities:
    def test_get_activities(self):
        """Test retrieving all activities"""
        # Arrange: No specific setup needed for this test
        
        # Act: Make a GET request to retrieve activities
        response = client.get("/activities")
        
        # Assert: Check that the response is successful and contains expected activities
        assert response.status_code == 200
        activities = response.json()
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities


class TestSignup:
    def test_signup_new_participant(self):
        """Test signing up a new participant"""
        # Arrange: Define test data
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act: Attempt to sign up the participant
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert: Verify successful signup
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_participant(self):
        """Test that duplicate signups are prevented"""
        # Arrange: Sign up a participant first
        activity_name = "Chess Club"
        email = "test@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act: Attempt to sign up the same participant again
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert: Verify that duplicate signup is rejected
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self):
        """Test signing up for a nonexistent activity"""
        # Arrange: Define test data for a nonexistent activity
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act: Attempt to sign up for the nonexistent activity
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert: Verify that the request fails with 404
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUnregister:
    def test_unregister_participant(self):
        """Test unregistering a participant"""
        # Arrange: Define test data (assuming the participant exists)
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act: Attempt to unregister the participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert: Verify successful unregistration
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_nonexistent_participant(self):
        """Test unregistering a participant that doesn't exist"""
        # Arrange: Define test data for a nonexistent participant
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        
        # Act: Attempt to unregister the nonexistent participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert: Verify that the request fails with 404
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]