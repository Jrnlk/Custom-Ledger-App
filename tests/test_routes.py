import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from app.main import app

client = TestClient(app)

TEST_ACCOUNT_ID = "aeda3011-d9fa-4f50-a66a-3c1478a3aa8c"

NONEXISTENT_ACCOUNT_ID = "11111111-2222-3333-4444-555555555555"

# test for getting correct balance
def test_get_balance_success():
    response = client.get(f"/balance/{TEST_ACCOUNT_ID}")
    assert response.status_code == 200

    data = response.json()

    assert "account_id" in data 
    assert "balance" in data 
    assert UUID(data["account_id"])
    assert data["balance"] == 10000

# test for invalid UUID
def test_get_balance_invalid_uuid():
    response = client.get("/balance/this-is-not-uuid")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid uuid"

# test for nonexistent account 
def test_get_balance_nonexistent_account():
    response = client.get(f"/balance/{NONEXISTENT_ACCOUNT_ID}")
    # This depends on your implementation — if you raise 404, test that
    assert response.status_code == 404
    assert response.json()["detail"] in [
        "Balance not found", "Account not found", "Not Found"
    ]
