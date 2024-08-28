from pydantic import BaseModel


class Users(BaseModel):
    id: int
    login: str
    favorite_cities: list[str]


class RequestStatistic(BaseModel):
    id: int
    city: str
    requests: int
