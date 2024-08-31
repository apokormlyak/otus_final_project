from pydantic import BaseModel


class Users(BaseModel):
    login: str
    favorite_cities: list[int]


class CityRequest(BaseModel):
    city: str
    requests: int
