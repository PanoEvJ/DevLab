from hotel.db.engine import DBSession
from hotel.db.models import DBRoom


def read_all_rooms():
    return DBSession().query(DBRoom).all()


def read_room(room_id: int):
    # return DBSession().query(DBRoom).filter(DBRoom.id == room_id).first()
    return DBSession().query(DBRoom).get(room_id)
