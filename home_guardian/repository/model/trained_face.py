from datetime import datetime

from peewee import CharField, DateTimeField

from home_guardian.repository.model.base.model import BaseModel, database


class TrainedFace(BaseModel):
    """
    TrainedFace model
    """

    username = CharField(unique=True, max_length=50)
    created_time = DateTimeField(default=datetime.now)
    modified_time = DateTimeField(null=True, default=datetime.now)


database.create_tables([TrainedFace])
