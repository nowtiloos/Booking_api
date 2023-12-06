from app.dao.base import BaseDAO


class ImporterDAO(BaseDAO):

    @classmethod
    async def add_from_csv(cls, table_name: str, data: dict):
        ...