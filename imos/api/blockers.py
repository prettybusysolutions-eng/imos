from fastapi import APIRouter
from imos.services.query_service import QueryService
from imos.services.blocker_extractor import BlockerExtractor

router = APIRouter()

@router.get('/')
def list_blockers():
    return {'items': QueryService().blockers()}

@router.post('/extract')
def extract_blockers(path: str):
    return BlockerExtractor().ingest_markdown(path)

