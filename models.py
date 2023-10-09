from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import text
from sqlalchemy import TIMESTAMP

from db import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String, primary_key=True, nullable=False)
    rating = Column(Integer)
    name = Column(String)
    site = Column(String)
    email = Column(String)
    phone = Column(String)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    lat = Column(Float)
    lng = Column(Float)