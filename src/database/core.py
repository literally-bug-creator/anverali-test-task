from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, select
from database.config import settings
from database.models import metadata_object, tasks_table
from typing import Sequence


class Core:
    engine = create_async_engine(url=settings.asyncpg_connect_url)

    @staticmethod
    async def create_table() -> None:
        async with Core.engine.begin() as connection:
            await connection.run_sync(metadata_object.create_all)

    @staticmethod
    async def add_task(task_name: str, creator_id: str) -> None:
        async with Core.engine.connect() as connection:
            statement = insert(tasks_table).values({"name": task_name, "creator_id": creator_id})

            await connection.execute(statement)
            await connection.commit()

    @staticmethod
    async def get_tasks() -> Sequence:
        async with Core.engine.connect() as connection:
            query = select(tasks_table)
            query_result = await connection.execute(query)

            return list(query_result.all())