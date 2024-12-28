from fastapi import APIRouter

from hotel.operations.customer import read_all_customers, read_customer

router = APIRouter()


@router.get("/customers")
def api_read_all_customers():
    return read_all_customers()


@router.get("/customer/{customer_id}")
def api_read_customer(customer_id: int):
    return read_customer(customer_id)
