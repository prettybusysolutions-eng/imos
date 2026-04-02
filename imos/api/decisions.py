from fastapi import APIRouter
from imos.models import DecisionRecord

router = APIRouter()

@router.get("/")
def list_decisions():
    return {"items": []}

@router.post("/")
def create_decision(record: DecisionRecord):
    return {"stored": True, "decision": record.model_dump()}
