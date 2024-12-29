from fastapi import APIRouter

from hotel.operations.customers import (
    CustomerCreateData,
    CustomerUpdateData,
    create_customer,
    read_all_customers,
    read_customer,
    update_customer,
)

router = APIRouter()


@router.get("/customers")
def api_read_all_customers():
    return read_all_customers()


@router.get("/customer/{customer_id}")
def api_read_customer(customer_id: int):
    return read_customer(customer_id)


@router.post("/customer")
def api_create_customer(data: CustomerCreateData):
    return create_customer(data)


@router.put("/customer/{customer_id}")
def api_update_customer(customer_id: int, data: CustomerUpdateData):
    return update_customer(customer_id, data)
