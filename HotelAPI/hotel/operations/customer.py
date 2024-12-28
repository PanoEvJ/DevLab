from pydantic import BaseModel

from hotel.db.engine import DBSession
from hotel.db.models import DBCustomer, to_dict


class CustomerCreateData(BaseModel):
    first_name: str
    last_name: str
    email_address: str


def read_all_customers():
    return [to_dict(customer) for customer in DBSession().query(DBCustomer).all()]


def read_customer(customer_id: int):
    return to_dict(DBSession().query(DBCustomer).get(customer_id))


def create_customer(data: CustomerCreateData):
    session = DBSession()
    customer = DBCustomer(**data.model_dump())
    session.add(customer)
    session.commit()
    return to_dict(customer)
