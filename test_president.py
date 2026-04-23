from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # your FastAPI file

client = TestClient(app)

def test_get_president_success():
    mock_response = MagicMock()
    mock_response.data = [{"id": 1, "name": "George Washington"}]

    with patch("main.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        response = client.get("/presidents/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "George Washington"}

def test_get_president_invalid_id():
    response = client.get("/presidents/abc")

    assert response.status_code == 422
  
def test_get_president_not_found():
    mock_response = MagicMock()
    mock_response.data = []

    with patch("main.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        response = client.get("/presidents/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "President not found"

def test_get_president_db_error():
    with patch("main.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("DB failure")

        response = client.get("/presidents/1")

        assert response.status_code == 500
      
