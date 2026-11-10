import pytest
import requests

BASE_URL = "https://dummyjson.com"

def test_module_get_users_positive():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) > 0
    assert "total" in data
    assert "skip" in data
    assert "limit" in data

def test_module_get_users_filter_param():
    response = requests.get(f"{BASE_URL}/users/search", params={"q": "Emily"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) >= 1
    assert any("Emily" in u["firstName"] for u in data["users"])

def test_module_get_users_zero_limit_returns_all():
    response = requests.get(f"{BASE_URL}/users", params={"limit": 0})
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == data["total"]

def test_module_get_users_headers():
    headers = {"Accept": "application/json", "User-Agent": "Pytest-API-Client/1.0"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")

def test_crud_create_user():
    payload = {
        "firstName": "Алексей",
        "lastName": "Смирнов",
        "age": 28,
        "email": "alex.smirnov@example.com",
        "gender": "male"
    }
    response = requests.post(f"{BASE_URL}/users/add", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["firstName"] == "Алексей"
    assert data["lastName"] == "Смирнов"
    assert data["email"] == "alex.smirnov@example.com"
    assert "id" in data

def test_crud_read_user():
    user_id = 1
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "firstName" in data
    assert "email" in data

def test_crud_update_user():
    user_id = 1
    update_payload = {"email": "updated_emily@example.com"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "updated_emily@example.com"

def test_crud_delete_user():
    user_id = 1
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data.get("isDeleted") is True

def test_error_handling_empty_body():
    response = requests.post(f"{BASE_URL}/auth/login", json={})
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert len(data["message"]) > 0

def test_error_handling_non_existent_endpoint():
    response = requests.get(f"{BASE_URL}/api/v999/non_existent_resource")
    assert response.status_code == 404

def test_auth_protected_without_token():
    response = requests.get(f"{BASE_URL}/auth/me")
    assert response.status_code in [401, 403]
    data = response.json()
    assert "message" in data

def test_auth_protected_with_invalid_token():
    headers = {"Authorization": "Bearer invalid_fake_token_12345"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert response.status_code in [401, 403]

def test_auth_workflow_success():
    login_payload = {"username": "emilys", "password": "emilyspass"}
    login_res = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "accessToken" in login_data
    token = login_data["accessToken"]

    headers = {"Authorization": f"Bearer {token}"}
    auth_me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert auth_me_res.status_code == 200
    user_info = auth_me_res.json()
    assert user_info["username"] == "emilys"

def test_data_validation_non_existent_user_id():
    response = requests.get(f"{BASE_URL}/users/99999999")
    assert response.status_code == 404
    data = response.json()
    assert "message" in data
    assert "99999999" in data["message"]

def test_pagination_limit_and_skip():
    limit = 5
    skip = 10
    response = requests.get(f"{BASE_URL}/users", params={"limit": limit, "skip": skip})
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == limit
    assert data["skip"] == skip
    assert data["limit"] == limit

def test_pagination_out_of_range():
    response = requests.get(f"{BASE_URL}/users", params={"limit": 10, "skip": 999999})
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 0
