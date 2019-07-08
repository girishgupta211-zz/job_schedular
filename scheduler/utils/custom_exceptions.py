"""
Custom exceptions module
"""


class BaseException(Exception):
    """
    Base exception class
    """
    err_code = None
    err_str = None
    http_status_code = 500

    def to_dict(self):
        """
        return json object
        """
        return {
            'err_code': self.err_code,
            'err_str': self.err_str,
            'err_msg': str(self),
            'http_status_code': self.http_status_code
        }


class PayloadParseError(BaseException):
    """
    Payload parsing exception
    """
    err_code = 1000
    err_str = 'E_PAYLOAD_PARSE'
    http_status_code = 400


class MissingKeysError(BaseException):
    """
    Missing required keys exception
    """
    err_code = 1001
    err_str = 'E_MISSING_KEYS'
    http_status_code = 400


class JobNotFoundError(BaseException):
    """
    Job not found exception
    """
    err_code = 1010
    err_str = 'E_INVALID_JOB_ID'
    http_status_code = 404


class InvalidCronExpressionError(BaseException):
    """
    Invalid function exception
    """
    err_code = 1011
    err_str = 'E_INVALID_CRON_TAB_EXPRESSION'
    http_status_code = 400


class InvalidFunctionError(BaseException):
    """
    Invalid function exception
    """
    err_code = 1012
    err_str = 'E_INVALID_FUNCTION_PATH'
    http_status_code = 400
