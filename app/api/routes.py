from fastapi import APIRouter
from app.models.schema import TitleRequest
from app.services.title_service import TitleService

router = APIRouter()

service = TitleService()

@router.post("/analyze")
def analyze_title(request: TitleRequest):
    return service.analyze(request.title)