from fastapi import APIRouter
from imos.models import DecisionRecord
from imos.services.decision_ledger import DecisionLedger
from imos.services.query_service import QueryService

router = APIRouter()

@router.get('/')
def list_decisions():
    return {'items': QueryService().decisions()}

@router.post('/')
def create_decision(record: DecisionRecord):
    obj = DecisionLedger().create(record)
    return {
        'stored': True,
        'decision': {
            'decision_id': obj.decision_id,
            'title': obj.title,
            'reason': obj.reason,
            'verification_result': obj.verification_result,
        }
    }
