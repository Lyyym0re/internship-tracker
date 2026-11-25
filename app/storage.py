from typing import Any
from app.models import ApplicationStatus
import psycopg.rows
from psycopg_pool import AsyncConnectionPool

async def save_application(company: str, position: str, pool : AsyncConnectionPool) -> dict[str, Any]:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute("""
                INSERT INTO applications
                (company, position)
                VALUES
                (%s, %s)
                RETURNING id, company, position, status
            """, (company, position))
            new_application = await cursor.fetchone()
            if not isinstance(new_application, dict):
                raise RuntimeError("Could not retrieve the newly created application")
            return new_application


async def filtered_applications(status: ApplicationStatus | None, pool : AsyncConnectionPool) -> list[dict]:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            if status is None:

                await cursor.execute("""
                    SELECT id, company, position, status
                    FROM applications
                    ORDER BY id DESC
                """)
                return await cursor.fetchall()

            await cursor.execute("""
                SELECT id, company, position, status
                FROM applications
                WHERE status = %s
                ORDER BY id DESC
            """, (status, ))
            return await cursor.fetchall()

async def update_application_status(application_id: int, status: ApplicationStatus, pool: AsyncConnectionPool) -> dict | None:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute("""
                UPDATE applications
                SET status = %s
                WHERE id = %s
                RETURNING id, company, position, status
            """, (status, application_id))
            return await cursor.fetchone()

async def find_application_async(application_id : int, pool : AsyncConnectionPool) -> dict | None:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute("""
                SELECT id, company, position, status
                FROM applications
                WHERE id = %s
            """, (application_id, ))
            return await cursor.fetchone()

async def delete_application_async(application_id: int, pool: AsyncConnectionPool) -> dict | None:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute("""
                DELETE FROM applications
                WHERE id = %s
                RETURNING id, company, position, status;
            """, (application_id, ))
            return await cursor.fetchone()
