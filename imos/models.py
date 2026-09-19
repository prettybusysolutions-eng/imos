from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DecisionRecord(BaseModel):
    decision_id: str
    title: str
    reason: str
    context: Optional[str] = None
    verification_result: Optional[str] = None
    downstream_artifacts: List[str] = Field(default_factory=list)

class EntityRecord(BaseModel):
    entity_id: str
    entity_type: str
    name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    trust_score: float = 0.5

class EdgeRecord(BaseModel):
    edge_id: str
    from_entity_id: str
    to_entity_id: str
    edge_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
