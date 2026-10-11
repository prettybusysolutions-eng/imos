from fastapi import APIRouter,Depends,Request
from imos.auth import owner_for_request
router=APIRouter()
@router.get('/summary')
def summary(request:Request,owner:str=Depends(owner_for_request)):
    return {'status':'durable pilot','decision_count':len(request.app.state.store.list(owner))}
