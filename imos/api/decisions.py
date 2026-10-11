import sqlite3
from fastapi import APIRouter,Depends,HTTPException,Request
from imos.auth import owner_for_request
from imos.models import DecisionRecord
router=APIRouter()

@router.get('/')
def list_decisions(request:Request,owner:str=Depends(owner_for_request)):
    return {'items':request.app.state.store.list(owner)}

@router.post('/',status_code=201)
def create_decision(record:DecisionRecord,request:Request,owner:str=Depends(owner_for_request)):
    try: decision=request.app.state.store.create(owner,record)
    except sqlite3.IntegrityError: raise HTTPException(409,'Decision already exists for this owner')
    return {'stored':True,'decision':decision}
