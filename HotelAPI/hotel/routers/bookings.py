from fastapi import APIRouter

from hotel.operations.bookings import (
    BookingCreateData,
    BookingUpdateData,
    create_booking,
    delete_booking,
    read_all_bookings,
    read_booking,
    update_booking,
)

router = APIRouter()


@router.get("/bookings")
def api_read_all_bookings():
    return read_all_bookings()


@router.get("/booking/{booking_id}")
def api_read_booking(booking_id: int):
    return read_booking(booking_id)


@router.post("/booking")
def api_create_booking(data: BookingCreateData):
    return create_booking(data)


@router.put("/booking/{booking_id}")
def api_update_booking(booking_id: int, data: BookingUpdateData):
    return update_booking(booking_id, data)


@router.delete("/booking/{booking_id}")
def api_delete_booking(booking_id: int):
    return delete_booking(booking_id)


# curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 1, "room_id": 1, "from_date": "2024-01-01", "to_date": "2024-01-02"}' http://localhost:8000/booking
# curl -X POST http://localhost:8000/booking -H "Content-Type: application/json" -d '{"customer_id": 1, "room_id": 1, "from_date": "2024-01-01", "to_date": "2024-01-02"}'
# curl -X DELETE http://localhost:8000/booking/1
