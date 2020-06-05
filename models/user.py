from sqlalchemy import Column, Integer, String

from database import Base
from exceptions import UserDoesNotExist


class User(Base):
    __tablename__ = "userobj"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    user_obj_id = Column(String, nullable=False)

    @staticmethod
    def get_and_check_else_new(sess, user_obj_id):
        if len(sess.query(User).filter_by(user_obj_id=user_obj_id).all()) > 0:
            return sess.query(User).filter_by(user_obj_id=user_obj_id).first()
        new_user = User(user_obj_id=user_obj_id)
        sess.add(new_user)
        sess.commit()
        return new_user

    @staticmethod
    def get_by_pk(sess, request_id, user_obj_pk):
        user = sess.query(User).filter_by(pk=user_obj_pk).first()
        if not user:
            raise UserDoesNotExist(request_id=request_id)
        return user

    @staticmethod
    def get_by_id(sess, request_id, user_obj_id):
        user = sess.query(User).filter_by(user_obj_id=user_obj_id).first()
        if not user:
            raise UserDoesNotExist(request_id=request_id)
        return user
