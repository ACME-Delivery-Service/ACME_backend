from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if 'msg' not in response.data:
            response.data['msg'] = response.data.pop('detail', None)

        if response.data['msg'] and response.data['msg'].code != APIException.default_code:
            msg_code = response.data['msg'].code
            if str(msg_code).isnumeric() and response.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
                response.status_code = int(msg_code)
            elif 'error_code' not in response.data:
                response.data['error_code'] = msg_code

        response.data['status_code'] = response.status_code

    return response
