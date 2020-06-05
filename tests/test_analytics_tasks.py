import uuid
from unittest import TestCase, mock
from unittest.mock import MagicMock

from analytics.tasks import create_user_visit_helper, get_visit_by_id_helper
from models.merchant import Merchant
from models.user import User
from models.visit import Visit


class TestAnalyticsTasks(TestCase):

    timestamp = 500

    @mock.patch("time.time", return_value=timestamp)
    @mock.patch("models.merchant.Merchant.get_and_check_else_new")
    @mock.patch("models.user.User.get_and_check_else_new")
    def test_create_user_visit_helper(
        self,
        mock_user_get_and_check_else_new,
        mock_merchant_get_and_check_else_new,
        mock_time,
    ):
        test_merchant = Merchant()
        test_user = User()

        test_merchant.pk = 50
        test_merchant.merchant_id = 50
        test_merchant.merchant_name = "test1"
        test_user.user_obj_id = 50
        test_request_id = "test1"
        mock_merchant_get_and_check_else_new.return_value = test_merchant
        mock_user_get_and_check_else_new.return_value = test_user
        sess_mock = MagicMock()
        test_merchant_data = {
            "merchantId": test_merchant.merchant_id,
            "merchantName": test_merchant.merchant_name,
        }
        test_output = {
            "merchant": test_merchant_data,
            "timestamp": 1591122440,
            "user": {"userId": test_user.user_obj_id},
            "visitId": "23642023-7307-45cc-9ce6-b7edf02dd5fe",
        }
        output = create_user_visit_helper(
            sess_mock, test_request_id, test_user.user_obj_id, test_merchant_data
        )
        mock_user_get_and_check_else_new.assert_called_once_with(
            sess_mock, test_user.user_obj_id
        )
        mock_merchant_get_and_check_else_new.assert_called_once_with(
            sess_mock,
            test_merchant_data["merchantId"],
            test_merchant_data["merchantName"],
        )
        self.assertEqual(
            test_output["merchant"]["merchantId"], output["merchant"]["merchantId"]
        )
        self.assertEqual(
            test_output["merchant"]["merchantName"], output["merchant"]["merchantName"]
        )
        self.assertEqual(test_output["user"]["userId"], output["user"]["userId"])
        self.assertEqual(type(uuid.uuid4()), type(output["visitId"]))
        self.assertEqual(500, output["timestamp"])

    @mock.patch("time.time", return_value=timestamp)
    @mock.patch("models.merchant.Merchant.get_by_pk")
    @mock.patch("models.user.User.get_by_pk")
    @mock.patch("models.visit.Visit.get_by_id")
    def test_get_visit_by_id_helper(
        self,
        mock_visit_get_by_id,
        mock_user_get_by_pk,
        mock_merchant_get_by_pk,
        mock_time,
    ):
        test_merchant = Merchant()
        test_user = User()
        test_visit = Visit()
        sess_mock = MagicMock()

        test_merchant.pk = 40
        test_merchant.merchant_id = 4
        test_merchant.merchant_name = "test2"

        test_visit.visit_id = uuid.uuid4()
        test_visit.timestamp = self.timestamp
        test_visit.merchant_pk = 40
        test_visit.user_obj_pk = 4

        test_request_id = "test2"

        test_user.user_obj_id = "20"
        test_user.pk = 4

        mock_merchant_get_by_pk.return_value = test_merchant
        mock_user_get_by_pk.return_value = test_user
        mock_visit_get_by_id.return_value = test_visit

        test_output = {
            "visitId": test_visit.visit_id,
            "timestamp": test_visit.timestamp,
            "merchant": {
                "merchantId": test_merchant.merchant_id,
                "merchantName": test_merchant.merchant_name,
            },
            "user": {"userId": test_user.user_obj_id},
        }
        output = get_visit_by_id_helper(sess_mock, test_request_id, test_visit.visit_id)

        mock_visit_get_by_id.assert_called_once_with(
            sess_mock, test_request_id, test_visit.visit_id
        )
        mock_merchant_get_by_pk.assert_called_once_with(
            sess_mock, test_request_id, test_visit.merchant_pk
        )
        mock_user_get_by_pk.assert_called_once_with(
            sess_mock, test_request_id, test_visit.user_obj_pk
        )
        mock_time.assert_called_once_with()

        self.assertEqual(
            test_output["merchant"]["merchantId"], output["merchant"]["merchantId"]
        )
        self.assertEqual(
            test_output["merchant"]["merchantName"], output["merchant"]["merchantName"]
        )
        self.assertEqual(test_output["user"]["userId"], output["user"]["userId"])
        self.assertEqual(type(uuid.uuid4()), type(output["visitId"]))
        self.assertEqual(500, output["timestamp"])
