from fastapi import HTTPException, status

from base.code import ErrorCode


class BaseException(HTTPException):


    def __init__(self, code=ErrorCode.INTERNAL_ERROR()["code"], message="", data=None,
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, **keys):
        self.code = code
        self.message = message
        self.data = data
        self.status_code = status_code
        super(BaseException, self).__init__(self.status_code, self.message, **keys)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, status_code={self.status_code!r}, message={self.message!r})"

    def __str__(self):
        return self.message + '\n' + super().__str__()