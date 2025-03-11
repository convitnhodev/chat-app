from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoBaseModel(BaseModel):
    """
    Base class for all MongoDB models
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def collection_name(self) -> str:
        """
        Returns the collection name for the model (similar to __tablename__ in SQLAlchemy)
        """
        return self.__class__.__name__.lower()

    def dict(self, *args, **kwargs):
        """
        Override dict method to handle ObjectId serialization
        """
        dict_repr = super().dict(*args, **kwargs)
        # Convert ObjectId to string
        dict_repr["id"] = str(dict_repr.get("_id", ""))
        return dict_repr

class UpdateMixin(BaseModel):
    """
    Mixin class for update operations
    """
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def dict(self, *args, **kwargs):
        """
        Override dict method to exclude None values
        """
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)