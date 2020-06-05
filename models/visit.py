from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base
from exceptions import VisitDoesNotExist


class Visit(Base):
    __tablename__ = "visit"

    pk = Column(Integer, autoincrement=True, primary_key=True)
    visit_id = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    user_obj_pk = Column(String, ForeignKey("userobj.pk"))
    merchant_pk = Column(String, ForeignKey("merchant.pk"))

    @staticmethod
    def new(sess, visit_id, timestamp, user_obj_pk, merchant_pk):
        new_visit = Visit(
            visit_id=visit_id,
            timestamp=timestamp,
            merchant_pk=merchant_pk,
            user_obj_pk=user_obj_pk,
        )
        sess.add(new_visit)
        sess.commit()
        return new_visit

    @staticmethod
    def get_by_id(sess, request_id, visit_id):
        visit = sess.query(Visit).filter_by(visit_id=visit_id).first()
        if not visit:
            raise VisitDoesNotExist(request_id=request_id)
        return visit
