from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel

from hotel.operations.interface import DataInterface, DataObject


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


def read_all_bookings(booking_interface: DataInterface) -> list[DataObject]:
    return booking_interface.read_all()


def read_booking(booking_id: int, booking_interface: DataInterface) -> DataObject:
    return booking_interface.read_by_id(booking_id)


def create_booking(
    data: BookingCreateData,
    customer_interface: DataInterface,
    room_interface: DataInterface,
    booking_interface: DataInterface,
) -> DataObject:
    customer = customer_interface.read_by_id(data.customer_id)
    room = room_interface.read_by_id(data.room_id)

    if not customer or not room:
        raise HTTPException(status_code=404, detail="Customer or room not found")

    if data.to_date < data.from_date:
        raise HTTPException(status_code=400, detail="To date is before from date")

    days = (data.to_date - data.from_date).days
    if days < 1:
        raise InvalidBookingDateError("To date is before from date")

    booking_dict = data.model_dump()
    booking_dict["price"] = room["price"] * days
    # booking_dict["customer"] = customer
    # booking_dict["room"] = room

    return booking_interface.create(booking_dict)


def update_booking(
    booking_id: int,
    data: BookingUpdateData,
    booking_interface: DataInterface,
) -> DataObject:
    booking_dict = data.model_dump(exclude_none=True)
    return booking_interface.update(booking_id, booking_dict)


def delete_booking(booking_id: int, booking_interface: DataInterface) -> DataObject:
    return booking_interface.delete(booking_id)
