from loguru import logger
from peewee import Model, SqliteDatabase

from home_guardian.function_collection import get_root_path

db_path = f"{get_root_path()}/home_guardian.db"
logger.info(f"SQLite database path: {db_path}")
db = SqliteDatabase(db_path)
logger.info(f"Initialized db file: {db}")


class BaseModel(Model):
    """
    Base model for persistence.

    @see Models and Fields https://docs.peewee-orm.com/en/latest/peewee/models.html#model-inheritance
    """

    class Meta:
        database = db
