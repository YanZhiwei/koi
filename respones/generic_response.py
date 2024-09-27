from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator

from base.code import SuccessCode

ResponseData = TypeVar("ResponseData")

class GenericResponse(BaseModel, Generic[ResponseData]):
    data: ResponseData = Field(default={})
    message: str = Field(default="",)
    code: str = Field(default=SuccessCode.SUCCESS()["code"])

    @field_validator("data")
    def format_data(cls, value):
        if value is None:
            value = {}
        return value

# 示例：
