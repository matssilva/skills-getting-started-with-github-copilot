from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    email = "remove-me@example.com"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    activities = activities_response.json()[activity_name]
    assert email not in activities["participants"]
