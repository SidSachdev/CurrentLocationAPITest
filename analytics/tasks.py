import time
import uuid
import logging

from analytics.util import get_matching_merchants
from constants import Threshold
from models.merchant import Merchant
from models.user import User
from models.visit import Visit

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("analytics.tasks.py")


def create_user_visit_helper(sess, request_id, user_obj_id, merchant_data):
    """
    A helper function that takes in the following params and creates a new visit
    object by communicating with the DB
    :param sess: Session object for access to the DB
    :param request_id: Request ID to track every request helps debugging
    :param user_obj_id: user_id to get the User object
    :param merchant_data: Merchant data from the given input
    :return: Visit object
    """
    merchant = Merchant.get_and_check_else_new(
        sess, merchant_data["merchantId"], merchant_data["merchantName"]
    )
    user = User.get_and_check_else_new(sess, user_obj_id)
    visit_id = uuid.uuid4()
    timestamp = int(time.time())
    Visit.new(sess, visit_id, timestamp, user.pk, merchant.pk)
    log.info("[{}] New visit created for user: {}".format(request_id, user.pk))
    return {
        "visitId": visit_id,
        "timestamp": timestamp,
        "merchant": {
            "merchantId": merchant.merchant_id,
            "merchantName": merchant.merchant_name,
        },
        "user": {"userId": user.user_obj_id},
    }


def get_merchant_visit_helper(sess, request_id, user_id, search_string):
    """
    A helper function that uses the analytics utils to get a list of matching
    merchants for the user based on the search string
    :param sess: Session object for access to the DB
    :param request_id: Request ID to track every request helps debugging
    :param user_id: User ID to get the User object
    :param search_string: search string to narrow down the list of merchants
    :return: list: list of objects that are the matching merchants and their data
    """
    user = User.get_by_id(sess, request_id, user_id)
    visits = sess.query(Visit).filter_by(user_obj_pk=user.pk).all()
    log.info(
        "[{}] Matching merchants requested by user: {}".format(request_id, user_id)
    )
    return get_matching_merchants(sess, request_id, user_id, visits, search_string,)


def get_visit_by_id_helper(sess, request_id, visit_id):
    visit = Visit.get_by_id(sess, request_id, visit_id)
    merchant = Merchant.get_by_pk(sess, request_id, visit.merchant_pk)
    user = User.get_by_pk(sess, request_id, visit.user_obj_pk)
    log.info("[{}] Found visit by user: {}".format(request_id, user.pk))
    return {
        "visitId": visit_id,
        "timestamp": visit.timestamp,
        "merchant": {
            "merchantId": merchant.merchant_id,
            "merchantName": merchant.merchant_name,
        },
        "user": {"userId": user.user_obj_id},
    }
