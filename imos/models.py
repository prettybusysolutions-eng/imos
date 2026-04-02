from pydantic import BaseModel
from typing import Optional, List

class DecisionRecord(BaseModel):
    decision_id: str
    title: str
    reason: str
    context: Optional[str] = None
    verification_result: Optional[str] = None
    downstream_artifacts: List[str] = []
