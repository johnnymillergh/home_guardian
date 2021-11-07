import logging

from peewee import Model, SqliteDatabase
from home_guardian.function_collection import get_root_path

log = logging.getLogger("rotatingFileLogger")

db_path = f"{get_root_path()}/home_guardian.db"
log.info(f"SQLite database path: {db_path}")
db = SqliteDatabase(db_path)
log.info(f"Initialized db file: {db}")


class BaseModel(Model):
    """
    Base model for persistence.

    @see Models and Fields https://docs.peewee-orm.com/en/latest/peewee/models.html#model-inheritance
    """

    class Meta:
        database = db
