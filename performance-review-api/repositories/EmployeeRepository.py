from database import get_connection
from psycopg.rows import dict_row


def get_all_employees():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT id, employee_id, name,
                       department, email, status
                FROM employees
                ORDER BY id
            """)
            return cursor.fetchall()