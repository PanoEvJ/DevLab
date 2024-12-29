import datetime
import unittest

from hotel.operations.bookings import (
    BookingCreateData,
    InvalidBookingDateError,
    create_booking,
)
from hotel.operations.interface import DataObject


class DataInterfaceStub:
    def read_by_id(self, id: int) -> DataObject:
        raise NotImplementedError

    def read_all(self) -> list[DataObject]:
        raise NotImplementedError

    def create(self, data: DataObject) -> DataObject:
        raise NotImplementedError

    def update(self, id: int, data: DataObject) -> DataObject:
        raise NotImplementedError

    def delete(self, id: int) -> DataObject:
        raise NotImplementedError


class RoomInterfaceMock(DataInterfaceStub):
    def read_by_id(self, id: int) -> DataObject:
        return {"price": 100_00}


class CustomerInterfaceMock(DataInterfaceStub):
    def read_by_id(self, id: int) -> DataObject:
        return {"id": id}


class BookingInterfaceMock(DataInterfaceStub):
    def create(self, data: DataObject) -> DataObject:
        return {"id": 1, "price": 100_00}


class TestBooking(unittest.TestCase):
    def test_price_one_day(self):
        booking_data = BookingCreateData(
            from_date=datetime.date(2024, 1, 1),
            to_date=datetime.date(2024, 1, 2),
            customer_id=1,
            room_id=1,
        )
        booking = create_booking(
            booking_data,
            customer_interface=CustomerInterfaceMock(),
            room_interface=RoomInterfaceMock(),
            booking_interface=BookingInterfaceMock(),
        )
        self.assertEqual(booking["price"], 100_00)

    def test_date_error(self):
        booking_data = BookingCreateData(
            from_date=datetime.date(2024, 1, 2),
            to_date=datetime.date(2024, 1, 1),
            customer_id=1,
            room_id=1,
        )
        with self.assertRaises(InvalidBookingDateError):
            create_booking(
                booking_data,
                customer_interface=CustomerInterfaceMock(),
                room_interface=RoomInterfaceMock(),
                booking_interface=BookingInterfaceMock(),
            )
        )


if __name__ == "__main__":
    unittest.main()
