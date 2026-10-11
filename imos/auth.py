import hashlib
import hmac
from fastapi import Header,HTTPException,Request

def owner_for_request(request:Request,x_api_key:str=Header(default='')):
    keys=request.app.state.owner_keys
    if not keys: raise HTTPException(503,'Owner authentication is not configured')
    digest=hashlib.sha256(x_api_key.encode()).hexdigest()
    for owner,expected in keys.items():
        if hmac.compare_digest(digest,expected): return owner
    raise HTTPException(401,'Invalid owner credential')
