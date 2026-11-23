from app.models import ApplicationStatus
import psycopg.rows
from app.db import get_connection

def save_application(company: str, position: str):
    with get_connection() as conn:
        conn.row_factory=psycopg.rows.dict_row
        result = conn.execute("""
            INSERT INTO applications
            (company, position)
            VALUES
            (%s, %s)
            RETURNING id, company, position, status
        """, (company, position), ).fetchone()
        return result

def find_application(application_id: int) -> None | dict:
    with get_connection() as conn:
        conn.row_factory = psycopg.rows.dict_row
        return conn.execute("""
            SELECT id, company, position, status
            FROM applications
            WHERE id = %s
        """, (application_id, )).fetchone()

def filtered_applications(status: ApplicationStatus | None = None) -> list[dict]:
    with get_connection() as conn:
        conn.row_factory = psycopg.rows.dict_row
        if status is None:
            return conn.execute("""
                SELECT id, company, position, status
                FROM applications
                ORDER BY id DESC
            """).fetchall()

        return conn.execute("""
            SELECT id, company, position, status
            FROM applications
            WHERE status = %s
            ORDER BY id DESC
        """, (status, )).fetchall()

def update_application_status(application_id: int, status: ApplicationStatus) -> dict | None:
    with get_connection() as conn:
        conn.row_factory = psycopg.rows.dict_row
        return conn.execute("""
            UPDATE applications
            SET status = %s
            WHERE id = %s
            RETURNING id, company, position, status
        """, (status, application_id)).fetchone()