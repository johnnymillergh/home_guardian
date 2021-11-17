from datetime import datetime

from peewee import CharField, DateTimeField

from home_guardian.repository.model.base.model import BaseModel, database


class DetectedFace(BaseModel):
    """
    DetectedFace model
    """

    picture_path = CharField(max_length=500)
    detected_username = CharField(max_length=50, null=True)
    created_time = DateTimeField(default=datetime.now)


database.create_tables([DetectedFace])
