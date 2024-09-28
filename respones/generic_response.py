from typing import Generic, TypeVar

from pydantic import Field, validator
from pydantic.generics import GenericModel

from base.code import SuccessCode

ResponseData = TypeVar("ResponseData")

class GenericResponse(GenericModel, Generic[ResponseData]):
    data: ResponseData = Field(default={})
    message: str = Field(default="",)
    code: str = Field(default=SuccessCode.SUCCESS()["code"])

    @validator("data")
    def format_data(cls, value):
        if value is None:
            value = {}
        return value


