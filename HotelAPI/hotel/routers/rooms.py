from fastapi import APIRouter

from hotel.operations.rooms import read_all_rooms

router = APIRouter()


@router.get("/rooms")
def api_read_all_rooms():
    return read_all_rooms()
