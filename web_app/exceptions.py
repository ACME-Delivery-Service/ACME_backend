from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class AcmeAPIException(APIException):
    default_code = HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        if code is None:
            code = self.default_code

        super(AcmeAPIException, self).__init__(detail, code)
