from fastapi import APIRouter
from imos.services.context_service import ContextService

router = APIRouter()

@router.get('/summary')
def summary():
    return ContextService().executive_summary()
