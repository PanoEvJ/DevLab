from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(obj: Base):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DBCustomer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email_address = Column(String(250), nullable=False)


class DBRoom(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(250), nullable=False)
    size = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


class DBBooking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("DBCustomer")
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship("DBRoom")
