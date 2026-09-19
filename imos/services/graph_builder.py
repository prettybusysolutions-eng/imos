import json
from imos.storage import SessionLocal
from imos.db_models import Entity, Edge
from imos.models import EntityRecord, EdgeRecord

class GraphBuilder:
    def upsert_entity(self, record: EntityRecord):
        db = SessionLocal()
        try:
            obj = Entity(
                entity_id=record.entity_id,
                entity_type=record.entity_type,
                name=record.name,
                metadata_json=json.dumps(record.metadata),
                trust_score=record.trust_score,
            )
            db.merge(obj)
            db.commit()
            return obj
        finally:
            db.close()

    def upsert_edge(self, record: EdgeRecord):
        db = SessionLocal()
        try:
            obj = Edge(
                edge_id=record.edge_id,
                from_entity_id=record.from_entity_id,
                to_entity_id=record.to_entity_id,
                edge_type=record.edge_type,
                metadata_json=json.dumps(record.metadata),
            )
            db.merge(obj)
            db.commit()
            return obj
        finally:
            db.close()

