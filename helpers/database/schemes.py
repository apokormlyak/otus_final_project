from pydantic import BaseModel


class Users(BaseModel):
    login: str


class CityRequest(BaseModel):
    name: str
    requests_count: int


class UserData(BaseModel):
    user_login: str
    city_id: int
