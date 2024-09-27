class Code(object):
    code_type = "API"
    code_business = "000"  # 标识系统统一编号
    code_error = "0000"  # 标识未知错误
    code_success = "9999"
    
class SuccessCode(Code):
    code_level = 'SUCCESS_'

    @classmethod
    def SUCCESS(cls):
        _code = cls.code_level + cls.code_type + "_200_" + cls.code_business + f"_{cls.code_success}"
        _zh = "成功"
        _en = "success"
        return {"code": _code, "zh": _zh, "en": _en}
    

class ErrorCode(Code):
    code_level = 'ERROR_'
    @classmethod
    def INTERNAL_ERROR(cls):
        _code = cls.code_level + cls.code_type + "_500_" + cls.code_business + "_0000"  # 未知错误
        _zh = "未知系统错误"
        _en = "internal error"
        return {"code": _code, "zh": _zh, "en": _en}

    @classmethod
    def REQUEST_VALIDATE_ERROR(cls):
        _code = cls.code_level + cls.code_type + "_422_" + cls.code_business + "_0001"  # request参数校验失败
        _zh = "request 请求参数校验失败，请检查参数格式"
        _en = "request validation error，please check your parameters"
        return {"code": _code, "zh": _zh, "en": _en}

    @classmethod
    def NOT_FOUND_ERROR(cls):
        _code = cls.code_level + cls.code_type + "_404_" + cls.code_business + "_0002"  # 资源不存在
        _zh = "请求的资源不存在"
        _en = "the request resource not exist"
        return {"code": _code, "zh": _zh, "en": _en}