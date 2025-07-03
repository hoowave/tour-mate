from pydantic import BaseModel

class RequestDto(BaseModel):
    age: str            # 머신러닝용
    gender: str         # 머신러닝용
    theme: str          # 머신러닝용    
    message: str        # 자연어처리용
    days: str           # 자연어처리용