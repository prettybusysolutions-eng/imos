from imos.storage import SessionLocal
from imos.db_models import Entity, Edge
from imos.models import EdgeRecord
from imos.services.graph_builder import GraphBuilder

class EntityLinker:
    def link_same_name(self):
        db = SessionLocal()
        builder = GraphBuilder()
        created = 0
        try:
            entities = db.query(Entity).all()
            by_name = {}
            for e in entities:
                by_name.setdefault((e.entity_type, e.name.lower()), []).append(e)
            for (_, _), group in by_name.items():
                if len(group) > 1:
                    root = group[0]
                    for other in group[1:]:
                        edge_id = f'edge:related:{root.entity_id}:{other.entity_id}'
                        builder.upsert_edge(EdgeRecord(
                            edge_id=edge_id,
                            from_entity_id=root.entity_id,
                            to_entity_id=other.entity_id,
                            edge_type='RELATED_TO',
                            metadata={'reason': 'same_name_same_type'},
                        ))
                        created += 1
            return {'links_created': created}
        finally:
            db.close()

