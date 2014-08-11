from rest_framework.exceptions import APIException

class TokenInvalid(APIException):
    status_code = 401
    default_detail = 'Token is invalid, please login again'


class IncorrectLogin(APIException):
    status_code = 401
    default_detail = 'Incorrect username or password'
