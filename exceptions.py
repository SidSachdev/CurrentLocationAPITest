class APIError(Exception):
    error_code = 1000
    log_message = "API Error"
    send_to_sentry = False
    request_id = None

    def __init__(self, request_id=None, message=None):
        if message is not None:
            self.log_message = message
        self.request_id = request_id

    def __str__(self):
        return "[{}] - ({}: {})".format(
            self.request_id, self.error_code, self.log_message
        )


class InputMalformed(APIError):
    error_code = 2001
    log_message = "Input Malformed."


class UserDoesNotExist(APIError):
    error_code = 2002
    log_message = "User does not exist"


class MerchantDoesNotExist(APIError):
    error_code = 2003
    log_message = "Merchant does not exist"


class VisitDoesNotExist(APIError):
    error_code = 2004
    log_message = "Visit does not exist"
