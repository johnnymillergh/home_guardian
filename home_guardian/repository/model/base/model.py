from loguru import logger
from peewee import Model, SqliteDatabase

from home_guardian.function_collection import get_data_dir

db_path = f"{get_data_dir()}/home_guardian.db"
logger.info(f"SQLite database path: {db_path}")
db = SqliteDatabase(db_path)
logger.warning(f"Initialized db file: {db}")


class BaseModel(Model):
    """
    Base model for persistence.

    @see Models and Fields https://docs.peewee-orm.com/en/latest/peewee/models.html#model-inheritance
    """

    class Meta:
        database = db
        legacy_table_names = False
