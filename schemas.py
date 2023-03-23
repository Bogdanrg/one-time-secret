from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema(cls, field_schema):
        field_schema.update(type="string")


class CreateSecretModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    secret: str = Field(le=100)
    phrase: str = Field(le=20)

