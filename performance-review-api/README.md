# Employee Performance Review Management System API

FastAPI service backed by PostgreSQL (psycopg 3, plain SQL). The contract is
`employee-performance-review-openapi.json`. Implemented endpoints:

| Method | Path                | Description                                                        |
| ------ | ------------------- | ------------------------------------------------------------------ |
| GET    | `/api/reviews`      | List reviews, newest first. Optional `employee_id` and `period_id` filters. |
| GET    | `/api/reviews/{id}` | One review by ID; `404 REVIEW_NOT_FOUND` if it doesn't exist.      |

## Layout

```
db/database.py                           .env loading + get_connection()
models/PerformanceReview.py              ReviewStatus enum + Review response model
models/ErrorResponse.py                  {code, message} error body
repositories/PerformanceReviewRepository.py   SQL
services/services.py                     business logic
main.py                                  FastAPI app and route
tests/test_reviews.py                    API tests
```

## Setup

From the repository root (`fde-performance-review/`):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create `performance-review-api/.env` with the connection string read by `db/database.py`:

```
DATABASE_URL=postgresql://postgres:your-password@localhost:5432/performance_review
```

The app and the tests won't import without `DATABASE_URL`.

Create the tables once, if they don't exist yet:

```powershell
psql -f schema.sql
```

## Run

From `performance-review-api/`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- Example: http://localhost:8000/api/reviews?employee_id=1&period_id=1

Responses:

- `200` — JSON array of reviews (`[]` when nothing matches).
- `422` — `employee_id` / `period_id` is not an integer or is below 1.
- `503` — `{"code": "DATABASE_UNAVAILABLE", "message": "Database is unavailable. Try again later."}`.

## Test

From `performance-review-api/`:

```powershell
..\.venv\Scripts\python.exe -m pytest -v
```

The tests insert and then delete their own employees, review periods and reviews, so `PGUSER` needs
`SELECT`, `INSERT` and `DELETE` on `employees`, `review_periods` and `performance_reviews`, plus `USAGE`
on their id sequences.
