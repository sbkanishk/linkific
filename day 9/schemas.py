from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId
from typing import Optional, List

class PyObjectId(str):
    """
    Fixed helper class compatible with Pydantic V2 core schemas
    to translate between MongoDB ObjectIds and Python strings.
    """
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

class Course(BaseModel):
    course_name: str
    credits: int

class StudentBase(BaseModel):
    name: str
    email: str
    age: int
    courses: List[Course] = []
    mentor_id: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Kanishk",
                "email": "kanishksb2005@gmail.com",
                "age": 21,
                "courses": [
                    {"course_name": "Data Science", "credits": 4},
                    {"course_name": "Advanced Mathematics", "credits": 4}
                ],
                "mentor_id": "65f1a2b3c4d5e6f7a8b9c0d1"
            }
        }
    )