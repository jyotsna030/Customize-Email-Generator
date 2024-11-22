from pydantic import BaseModel

class EmailStatus(BaseModel):
    email: str
    status: str
