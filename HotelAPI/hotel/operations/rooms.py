from hotel.db.engine import DBSession
from hotel.db.models import DBRoom


def read_all_rooms():
    return DBSession().query(DBRoom).all()
