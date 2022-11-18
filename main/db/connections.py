from fastapi import FastAPI
from piccolo.engine import engine_finder


def handle_database_connections(app: FastAPI) -> None:
    """Process Postgres database connections."""

    @app.on_event("startup")
    async def open_database_connection_pool() -> None:
        engine = engine_finder()
        await engine.start_connection_pool()

    @app.on_event("shutdown")
    async def close_database_connection_pool() -> None:
        engine = engine_finder()
        await engine.close_connection_pool()
