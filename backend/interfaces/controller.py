from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

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
def request(
    request_dto: RequestDto,
    service: Service = Depends(get_service)
):
    response = service.request(request_dto)
    return {"reply": response}

# 테스트용 API
@router.get("/api/test")
def test(
    service: Service = Depends(get_service)
):
    service.test()
    return {"reply": "Test completed successfully!"}