import logging

from fuzzywuzzy import fuzz

from models.merchant import Merchant

from constants import Threshold

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("analytics.util.py")


def get_matching_merchants(sess, request_id, user_id, visits, search_string):
    """
    A util function that uses the threshold to return the list of merchants
    that match the fuzzy ratio set by the environment or default
    :param sess: Session object for the DB
    :param request_id: Request ID tracking for debugging
    :param user_id: User id to get the User Object
    :param visits: list of visits by the user without the matching
    :param search_string: given search string to narrow down search
    :return: list of objects with narrowed down list based on search string
    """
    result = []
    log.debug(
        "[{}] Fuzzy matching for search string {} user_id: {}".format(
            request_id, search_string, user_id
        )
    )
    for visit in visits:
        merchant = Merchant.get_by_pk(sess, request_id, visit.merchant_pk)
        if (
            fuzz.ratio(merchant.merchant_name, search_string)
            > Threshold.FUZZY_MATCH_THRESHOLD
        ):
            result.append(
                {
                    "visitId": visit.visit_id,
                    "timestamp": visit.timestamp,
                    "merchant": {
                        "merchantId": merchant.merchant_id,
                        "merchantName": merchant.merchant_name,
                    },
                    "user": {"userId": user_id},
                }
            )
    return result
