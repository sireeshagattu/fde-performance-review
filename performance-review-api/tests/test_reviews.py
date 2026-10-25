import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from db.database import get_connection
from main import app

client = TestClient(app)

URL = "/api/reviews"


@pytest.fixture(scope="module")
def seed():
    """Insert 2 employees, 2 periods and 3 reviews; delete them afterwards."""
    suffix = uuid.uuid4().hex[:8].upper()
    with get_connection() as conn:
        emp_a, emp_b = (
            conn.execute(
                "INSERT INTO employees (employee_id, name, department, email) "
                "VALUES (%s, %s, 'QA', %s) RETURNING id",
                (f"T{tag}{suffix}", f"Test {tag} {suffix}", f"{tag.lower()}{suffix}@example.test"),
            ).fetchone()["id"]
            for tag in ("A", "B")
        )
        period_1, period_2 = (
            conn.execute(
                "INSERT INTO review_periods (name, start_date, end_date) VALUES (%s, %s, %s) RETURNING id",
                (f"Test {name} {suffix}", start, end),
            ).fetchone()["id"]
            for name, start, end in (("P1", "2026-01-01", "2026-06-30"), ("P2", "2026-07-01", "2026-12-31"))
        )
        # (employee, period, quality, delivery, teamwork, created_at); average_rating is a generated column.
        review_rows = [
            (emp_a, period_1, 4, 5, 4, datetime(2026, 10, 25, 9, 30, 0)),
            (emp_b, period_1, 3, 3, 3, datetime(2026, 10, 24, 9, 30, 0)),
            (emp_a, period_2, 5, 5, 5, datetime(2026, 10, 23, 9, 30, 0)),
        ]
        review_ids = [
            conn.execute(
                "INSERT INTO performance_reviews "
                "(employee_id, period_id, quality_rating, delivery_rating, teamwork_rating, comments, created_at) "
                "VALUES (%s, %s, %s, %s, %s, 'Test review', %s) RETURNING id",
                row,
            ).fetchone()["id"]
            for row in review_rows
        ]

    data = {
        "employees": (emp_a, emp_b),
        "codes": (f"TA{suffix}", f"TB{suffix}"),
        "periods": (period_1, period_2),
        # Newest first: review_ids[0] (Oct 25), [1] (Oct 24), [2] (Oct 23).
        "reviews": review_ids,
    }
    yield data

    with get_connection() as conn:
        conn.execute("DELETE FROM performance_reviews WHERE id = ANY(%s)", (review_ids,))
        conn.execute("DELETE FROM employees WHERE id = ANY(%s)", ([emp_a, emp_b],))
        conn.execute("DELETE FROM review_periods WHERE id = ANY(%s)", ([period_1, period_2],))


def ids(response):
    return [item["id"] for item in response.json()]


def test_no_filters_returns_our_rows_newest_first(seed):
    response = client.get(URL)
    assert response.status_code == 200
    ours = [i for i in ids(response) if i in seed["reviews"]]
    assert ours == seed["reviews"]


def test_filter_by_employee(seed):
    emp_a, emp_b = seed["employees"]
    r1, r2, r3 = seed["reviews"]
    assert ids(client.get(URL, params={"employee_id": emp_a})) == [r1, r3]
    assert ids(client.get(URL, params={"employee_id": emp_b})) == [r2]


def test_filter_by_period(seed):
    period_1, period_2 = seed["periods"]
    r1, r2, r3 = seed["reviews"]
    assert ids(client.get(URL, params={"period_id": period_1})) == [r1, r2]
    assert ids(client.get(URL, params={"period_id": period_2})) == [r3]


def test_filter_by_employee_and_period(seed):
    emp_a, emp_b = seed["employees"]
    period_1, period_2 = seed["periods"]
    r1, _, r3 = seed["reviews"]
    assert ids(client.get(URL, params={"employee_id": emp_a, "period_id": period_2})) == [r3]
    assert ids(client.get(URL, params={"employee_id": emp_a, "period_id": period_1})) == [r1]
    assert ids(client.get(URL, params={"employee_id": emp_b, "period_id": period_2})) == []


def test_unknown_id_returns_empty_list(seed):
    for params in ({"employee_id": 999999999}, {"period_id": 999999999}):
        response = client.get(URL, params=params)
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.parametrize("name", ["employee_id", "period_id"])
def test_non_integer_returns_422(name):
    response = client.get(URL, params={name: "abc"})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", name]
    assert error["type"] == "int_parsing"
    assert error["msg"].startswith("Input should be a valid integer")


@pytest.mark.parametrize("name", ["employee_id", "period_id"])
@pytest.mark.parametrize("value", [0, -1])
def test_value_below_one_returns_422(name, value):
    response = client.get(URL, params={name: value})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", name]
    assert error["type"] == "greater_than_equal"


def test_response_values(seed):
    emp_a = seed["employees"][0]
    period_1 = seed["periods"][0]
    response = client.get(URL, params={"employee_id": emp_a, "period_id": period_1})
    assert response.status_code == 200
    [item] = response.json()
    assert item == {
        "id": seed["reviews"][0],
        "employee_id": emp_a,
        "employee_code": seed["codes"][0],
        "employee_name": item["employee_name"],
        "period_id": period_1,
        "period_name": item["period_name"],
        "quality_rating": 4,
        "delivery_rating": 5,
        "teamwork_rating": 4,
        "average_rating": 4.33,
        "comments": "Test review",
        "status": "Completed",
        "created_at": "2026-10-25T09:30:00Z",
    }
    assert isinstance(item["average_rating"], float)
    assert item["created_at"].endswith("Z")


def test_openapi_documents_endpoint():
    spec = client.get("/openapi.json").json()
    operation = spec["paths"]["/api/reviews"]["get"]
    assert operation["operationId"] == "listReviews"
    assert operation["tags"] == ["Mandatory - Reviews"]

    params = {p["name"]: p for p in operation["parameters"]}
    assert set(params) == {"employee_id", "period_id"}
    for param in params.values():
        assert param["in"] == "query"
        assert param["required"] is False
        assert param["description"]

    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert schema["type"] == "array"
    assert schema["items"]["$ref"] == "#/components/schemas/Review"

    review = spec["components"]["schemas"]["Review"]
    assert {
        "id", "employee_id", "employee_code", "employee_name", "period_id", "period_name",
        "quality_rating", "delivery_rating", "teamwork_rating", "average_rating",
        "comments", "status", "created_at",
    } <= set(review["properties"])
    assert "503" in operation["responses"]
