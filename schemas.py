from pydantic import BaseModel

class Restaurants(BaseModel):
    id:str
    rating:int
    name:str
    site:str
    email:str
    phone:str
    street:str
    city:str
    state:str
    lat:float
    lng:float