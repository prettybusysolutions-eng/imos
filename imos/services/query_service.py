import json
from imos.storage import SessionLocal
from imos.db_models import Decision, Entity, Edge

class QueryService:
    def summary(self):
        db = SessionLocal()
        try:
            return {
                'decisions': db.query(Decision).count(),
                'entities': db.query(Entity).count(),
                'edges': db.query(Edge).count(),
                'blockers': db.query(Edge).filter(Edge.edge_type == 'BLOCKED_BY').count(),
                'repos': db.query(Entity).filter(Entity.entity_type == 'repo').count(),
                'sessions': db.query(Entity).filter(Entity.entity_type == 'session').count(),
            }
        finally:
            db.close()

    def blockers(self):
        db = SessionLocal()
        try:
            blockers = db.query(Edge).filter(Edge.edge_type == 'BLOCKED_BY').all()
            return [
                {
                    'edge_id': b.edge_id,
                    'from_entity_id': b.from_entity_id,
                    'to_entity_id': b.to_entity_id,
                    'metadata': json.loads(b.metadata_json or '{}')
                }
                for b in blockers
            ]
        finally:
            db.close()

    def decisions(self):
        db = SessionLocal()
        try:
            return [
                {
                    'decision_id': d.decision_id,
                    'title': d.title,
                    'reason': d.reason,
                    'verification_result': d.verification_result,
                }
                for d in db.query(Decision).order_by(Decision.created_at.desc()).all()
            ]
        finally:
            db.close()

    def entities_by_type(self, entity_type: str):
        db = SessionLocal()
        try:
            return [
                {
                    'entity_id': e.entity_id,
                    'name': e.name,
                    'trust_score': e.trust_score,
                }
                for e in db.query(Entity).filter(Entity.entity_type == entity_type).all()
            ]
        finally:
            db.close()

