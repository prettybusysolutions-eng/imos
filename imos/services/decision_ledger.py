from imos.storage import SessionLocal
from imos.db_models import Decision
from imos.models import DecisionRecord

class DecisionLedger:
    def create(self, record: DecisionRecord):
        db = SessionLocal()
        try:
            data = record.model_dump(exclude={'downstream_artifacts'})
            obj = db.get(Decision, data['decision_id'])
            if obj is None:
                obj = Decision(**data)
                db.add(obj)
            else:
                for k, v in data.items():
                    setattr(obj, k, v)
            db.commit()
            db.refresh(obj)
            return obj
        finally:
            db.close()

    def list(self):
        db = SessionLocal()
        try:
            return db.query(Decision).order_by(Decision.created_at.desc()).all()
        finally:
            db.close()

