from pydantic import BaseModel,Field
from typing import Optional,List
class DecisionRecord(BaseModel):
    decision_id:str=Field(min_length=1,max_length=256)
    title:str=Field(min_length=1,max_length=4096)
    reason:str=Field(min_length=1,max_length=65536)
    context:Optional[str]=Field(default=None,max_length=65536)
    verification_result:Optional[str]=Field(default=None,max_length=4096)
    downstream_artifacts:List[str]=Field(default_factory=list,max_length=100)
