from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CreateSecretModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    secret: str = Field(..., max_length=100)
    phrase: str = Field(..., max_length=20)
    timeToLive: Optional[int] = 3600

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "secret": "hello, 12",
                "phrase": "my secret phrase",
                "timeToLive": 3600
            }
        }

