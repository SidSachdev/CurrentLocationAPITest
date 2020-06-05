import os


class ExtractRequestFields(object):
    class Input:
        SEARCHSTRING = "searchString"
        USER = "user"
        REQUEST_ID = "request_id"
        VISIT_ID = "visitor_id"
        USER_ID = "userId"
        MERCHANT = "merchant"
        MERCHANT_ID = "merchantId"
        MERCHANT_NAME = "merchantName"


class ExceptionMessage(object):
    BAD_REQUEST = "Input is malformed."


class Threshold(object):
    FUZZY_MATCH_THRESHOLD = int(os.environ.get("FUZZY_MATCH_THRESHOLD", 50))
