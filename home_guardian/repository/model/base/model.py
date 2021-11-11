from loguru import logger
from peewee import Model, SqliteDatabase

from home_guardian.function_collection import get_data_dir

_db_path: str = f"{get_data_dir()}/home_guardian.db"
logger.info(f"SQLite database path: {_db_path}")
database: SqliteDatabase = SqliteDatabase(_db_path)
logger.warning(f"Initialized db file: {database}")


class BaseModel(Model):
    """
    Base model for persistence.
    Models and Fields https://docs.peewee-orm.com/en/latest/peewee/models.html#model-inheritance
    """

    class Meta:
        database = database
        legacy_table_names = False
