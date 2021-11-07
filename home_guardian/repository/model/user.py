from peewee import CharField, DateTimeField

from home_guardian.repository.model.base.model import BaseModel, db


class User(BaseModel):
    """
    User model for testing peewee
    """

    username = CharField(unique=True)
    created_time = DateTimeField(null=False)


db.create_tables([User])
