from fastapi import APIRouter, Depends
from typing import Union

from interfaces.dto.request_dto import RequestDto
from service.service import Service

router = APIRouter()

def get_service():
    return Service()

@router.get("/")
def index():
    return "Welcome to the Tour Mate API!"

# 실제 요청받는 API
@router.post("/api/chat")
def reuqest(
    request_dto: RequestDto,
    service: Service = Depends(get_service)
):
    response = service.request(request_dto)
    return {"reply": response}