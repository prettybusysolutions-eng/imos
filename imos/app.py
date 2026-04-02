from fastapi import FastAPI
from imos.api.decisions import router as decisions_router
from imos.api.context import router as context_router

app = FastAPI(title="IMOS", version="0.1.0")
app.include_router(decisions_router, prefix="/decisions", tags=["decisions"])
app.include_router(context_router, prefix="/context", tags=["context"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "imos"}
