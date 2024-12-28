from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBCustomer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)


class DBRoom(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    size = Column(Integer)
    price = Column(Float)


class DBBooking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    total_price = Column(Float)
