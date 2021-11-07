from peewee import Model, SqliteDatabase

from home_guardian.function_collection import get_root_path

base_dir = get_root_path()
print(f"base_dir: {base_dir}")
db = SqliteDatabase(f"{base_dir}/home_guardian.db")
print(f"Initialized db file: {db}")


class BaseModel(Model):
    """
    Base model for persistence.

    @see Models and Fields https://docs.peewee-orm.com/en/latest/peewee/models.html#model-inheritance
    """

    class Meta:
        database = db
