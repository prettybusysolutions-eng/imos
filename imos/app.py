from fastapi import FastAPI
from imos.storage import Base, engine
from imos.api.decisions import router as decisions_router
from imos.api.context import router as context_router
from imos.api.graph import router as graph_router
from imos.api.ingest import router as ingest_router
from imos.api.blockers import router as blockers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='IMOS', version='0.3.0')
app.include_router(decisions_router, prefix='/decisions', tags=['decisions'])
app.include_router(context_router, prefix='/context', tags=['context'])
app.include_router(graph_router, prefix='/graph', tags=['graph'])
app.include_router(ingest_router, prefix='/ingest', tags=['ingest'])
app.include_router(blockers_router, prefix='/blockers', tags=['blockers'])

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'imos', 'version': '0.3.0'}
