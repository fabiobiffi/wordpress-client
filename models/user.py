from pydantic import BaseModel

class WPUser(BaseModel):
    username: str
    email: str
    password: str