from pydantic import BaseModel

class RequestDto(BaseModel):
    age_group: str
    gender: str
    theme: str
    days: str