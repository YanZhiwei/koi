from fastapi import status

from base.code import ErrorCode
from exception.base_exception import BaseException


class JobNotFountException(BaseException):
    def __init__(self, *args, **keys):
        keys["code"] = keys.get("code") or ErrorCode.NOT_FOUND_ERROR()["code"]
        keys["message"] = keys.get("message") or "User not found"
        keys["status_code"] = keys.get("status_code") or status.HTTP_404_NOT_FOUND
        super(JobNotFountException, self).__init__(*args, **keys)