from fastapi import APIRouter, Depends
from typing import Union

from interfaces.dto.request_dto import RequestDto
from service.service import Service

router = APIRouter()

def get_service():
    return Service()

@router.get("/")
def index():
    return {"Hello": "World"}

# 실제 요청받는 API
@router.post("/request")
def reuqest(
    request: RequestDto,
    service: Service = Depends(get_service)
):
    service.kto_api_request()
    return {
        "age_group": request.age_group,
        "gender": request.gender,
        "theme": request.theme,
        "days": request.days
    }

# 테스트용
@router.get("/test")
def test(
    service: Service = Depends(get_service)
):
    response = service.request()
    return response

# 테스트용
@router.get("/test2")
def test(
    service: Service = Depends(get_service)
):
    response = service.ktoTest()
    return response