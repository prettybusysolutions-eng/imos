from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from imos.storage import Base

class Decision(Base):
    __tablename__ = 'decisions'
    decision_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    verification_result = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Entity(Base):
    __tablename__ = 'entities'
    entity_id = Column(String, primary_key=True, index=True)
    entity_type = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    metadata_json = Column(Text, nullable=True)
    trust_score = Column(Float, default=0.5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Edge(Base):
    __tablename__ = 'edges'
    edge_id = Column(String, primary_key=True, index=True)
    from_entity_id = Column(String, ForeignKey('entities.entity_id'), nullable=False, index=True)
    to_entity_id = Column(String, ForeignKey('entities.entity_id'), nullable=False, index=True)
    edge_type = Column(String, nullable=False, index=True)
    metadata_json = Column(Text, nullable=True)

