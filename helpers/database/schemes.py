from pydantic import BaseModel


class Users(BaseModel):
    login: str
    favorite_cities: list[str]


class CityRequest(BaseModel):
    city: str
    requests: int
