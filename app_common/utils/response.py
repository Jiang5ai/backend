from rest_framework.response import Response


class Error:
    """
    子定义错误码与错误信息
    """
    ParamsTypeError = {"30020": "参数类型错误"}
    JSON_TYPE_ERROR = {"30030": "JSON格式错误"}

    USER_OR_PAWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}

    PROJECT_ID_NULL = {"10020": "项目id不存在"}
    PROJECT_ID_ERROR = {"10021": "项目id错误"}
    MODULE_ID_NULL = {"10022": "模块id不存在"}
    CASE_ID_NULL = {"10023": "用例id不存在"}
    TASK_ID_NULL = {"10023": "测试任务id不存在"}

    PROJECT_OBJECT_NULL = {"10030": "通过id查询项目不存在"}
    MODULE_OBJECT_NULL = {"10031": "通过id查询模块不存在"}
    CASE_OBJECT_NULL = {"10032": "通过id查询用例不存在"}
    TASK_OBJECT_NULL = {"10032": "通过id查询测试任务不存在"}

    PROJECT_DELETE_ERROR = {"10040": "删除项目失败"}
    MODULE_DELETE_ERROR = {"10041": "删除模块失败"}
    CASE_DELETE_ERROR = {"10042": "删除用例失败"}
    TASK_DELETE_ERROR = {"10042": "删除测试任务失败"}


def response_fail(error=""):
    """
    返回失败, 主要用于参数验证失败
    """
    error_msg = {
        "30010": str(error)
    }
    return response(success=False, error=error_msg, data=[])


def response(success: bool = True, error={}, data: any = []) -> Response:
    """
    自定义接口返回格式
    """
    if error == {}:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    resp = {
        "success": success,
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "data": data
    }
    return Response(resp)
