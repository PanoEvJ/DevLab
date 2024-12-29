from typing import Any

from hotel.db.engine import DBSession
from hotel.db.models import Base, to_dict

DataObject = dict[str, Any]


class DBInterface:
    def __init__(self, db_class: Base):
        self.db_class = db_class

    def read_by_id(self, id: int) -> DataObject:
        session = DBSession()
        return to_dict(session.query(self.db_class).get(id))

    def read_all(self) -> list[DataObject]:
        session = DBSession()
        return [to_dict(item) for item in session.query(self.db_class).all()]

    def create(self, data: DataObject) -> DataObject:
        session = DBSession()
        item = self.db_class(**data)
        session.add(item)
        session.commit()
        return to_dict(item)

    def update(self, id: int, data: DataObject) -> DataObject:
        session = DBSession()
        item = session.query(self.db_class).get(id)
        for key, value in data.items():
            setattr(item, key, value)
        session.commit()
        return to_dict(item)

    def delete(self, id: int) -> DataObject:
        session = DBSession()
        item = session.query(self.db_class).get(id)
        session.delete(item)
        session.commit()
        return to_dict(item)
