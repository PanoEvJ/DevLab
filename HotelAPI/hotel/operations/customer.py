from hotel.db.engine import DBSession
from hotel.db.models import DBCustomer


def read_all_customers():
    return DBSession().query(DBCustomer).all()


def read_customer(customer_id: int):
    return DBSession().query(DBCustomer).get(customer_id)
