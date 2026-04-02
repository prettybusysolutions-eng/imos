from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def summary():
    return {
        "thesis": "Institutional memory as executable organizational cognition",
        "status": "bootstrap"
    }
