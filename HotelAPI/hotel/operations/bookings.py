from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel

from hotel.db.engine import DBSession
from hotel.db.models import DBBooking, DBCustomer, DBRoom, to_dict


class InvalidBookingDateError(Exception):
    pass


class BookingCreateData(BaseModel):
    customer_id: int
    room_id: int
    from_date: date
    to_date: date


class BookingUpdateData(BaseModel):
    from_date: date | None = None
    to_date: date | None = None
    customer_id: int | None = None
    room_id: int | None = None


def read_all_bookings():
    return [to_dict(booking) for booking in DBSession().query(DBBooking).all()]


def read_booking(booking_id: int):
    return to_dict(DBSession().query(DBBooking).get(booking_id))


def create_booking(data: BookingCreateData):
    print("START")
    print("SESSION")
    session = DBSession()
    print("CUSTOMER")
    customer = session.query(DBCustomer).get(data.customer_id)
    print("ROOM")
    room = session.query(DBRoom).get(data.room_id)

    if not customer or not room:
        raise HTTPException(status_code=404, detail="Customer or room not found")

    if data.to_date < data.from_date:
        raise HTTPException(status_code=400, detail="To date is before from date")

    days = (data.to_date - data.from_date).days
    if days < 1:
        raise InvalidBookingDateError("To date is before from date")

    price = room.price * days

    booking = DBBooking(
        **data.model_dump(),
        price=price,
        customer=customer,
        room=room,
    )
    session.add(booking)
    session.commit()
    return to_dict(booking)


def update_booking(booking_id: int, data: BookingUpdateData):
    session = DBSession()
    booking = session.query(DBBooking).get(booking_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(booking, key, value)
    session.commit()
    return to_dict(booking)


def delete_booking(booking_id: int):
    session = DBSession()
    booking = session.query(DBBooking).get(booking_id)
    session.delete(booking)
    session.commit()
    return to_dict(booking)
