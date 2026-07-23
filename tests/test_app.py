from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_for_activity():
    # Arrange
    email = "new-student@example.com"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_duplicate_signup_is_rejected():
    # Arrange
    email = "duplicate-student@example.com"
    activity_name = "Chess Club"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_missing_activity_returns_not_found():
    # Arrange
    email = "student@example.com"
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_from_activity():
    # Arrange
    email = "remove-me@example.com"
    activity_name = "Chess Club"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    activities = activities_response.json()[activity_name]
    assert email not in activities["participants"]
