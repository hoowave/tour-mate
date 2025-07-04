from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from interfaces.dto.request_dto import RequestDto
from service.service import Service

router = APIRouter()

service = Service()

def get_service():
    return service

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
@router.get("/api/graph")
def graph(
    service: Service = Depends(get_service)
):
    print("Graph API called")
    response = service.graph()
    return StreamingResponse(response, media_type="image/png")