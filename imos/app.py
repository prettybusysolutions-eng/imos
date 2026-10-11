import json
import os
import re
from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException
from imos.storage import DecisionStore
from imos.api.decisions import router as decisions_router
from imos.api.context import router as context_router

def create_app(database_path=None,owner_keys=None):
    keys=owner_keys if owner_keys is not None else json.loads(os.getenv('IMOS_OWNER_KEY_HASHES','{}'))
    if not isinstance(keys,dict) or any(not isinstance(owner,str) or not owner.strip() or
        not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest) for owner,digest in keys.items()):
        raise ValueError('IMOS_OWNER_KEY_HASHES must map owner IDs to SHA256 credential hashes')
    if len(set(keys.values())) != len(keys): raise ValueError('Owners must use distinct credentials')
    store=DecisionStore(database_path or os.getenv('IMOS_DB_PATH','./state/imos.sqlite'))
    @asynccontextmanager
    async def lifespan(app):
        store.migrate()
        yield
    app=FastAPI(title='IMOS',version='0.2.0',lifespan=lifespan)
    app.state.store=store
    app.state.owner_keys=keys
    app.include_router(decisions_router,prefix='/decisions',tags=['decisions'])
    app.include_router(context_router,prefix='/context',tags=['context'])
    @app.get('/health')
    def health(): return {'status':'ok','service':'imos'}
    @app.get('/ready')
    def ready():
        try: storage_ready=store.ready()
        except Exception: storage_ready=False
        if not keys or not storage_ready: raise HTTPException(503,'Storage or owner authentication is not ready')
        return {'status':'ready','schema_version':1,'scope':'owner-scoped durable decisions'}
    return app
app=create_app()
