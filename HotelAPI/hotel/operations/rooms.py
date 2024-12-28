from hotel.db.engine import DBSession
from hotel.db.models import DBRoom, to_dict


def read_all_rooms():
    return [to_dict(room) for room in DBSession().query(DBRoom).all()]


def read_room(room_id: int):
    return to_dict(DBSession().query(DBRoom).get(room_id))
