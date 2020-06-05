from sqlalchemy import Column, Integer, String

from database import Base
from exceptions import MerchantDoesNotExist


class Merchant(Base):
    __tablename__ = "merchant"

    pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    merchant_id = Column(Integer, nullable=False)
    merchant_name = Column(String, nullable=True)

    @staticmethod
    def get_and_check_else_new(sess, merchant_id, merchant_name):
        if len(sess.query(Merchant).filter_by(merchant_id=merchant_id).all()) > 0:
            return sess.query(Merchant).filter_by(merchant_id=merchant_id).first()
        new_merchant = Merchant(merchant_id=merchant_id, merchant_name=merchant_name)
        sess.add(new_merchant)
        sess.commit()
        return new_merchant

    @staticmethod
    def get_by_pk(sess, request_id, merchant_pk):
        merchant = sess.query(Merchant).filter_by(pk=merchant_pk).first()
        if not merchant:
            raise MerchantDoesNotExist(request_id=request_id)
        return merchant
