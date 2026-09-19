from pathlib import Path
import json
from imos.services.graph_builder import GraphBuilder
from imos.models import EntityRecord, EdgeRecord
from imos.services.trust_engine import score_memory

class SessionLogIngestor:
    def ingest_directory(self, path: str):
        root = Path(path)
        builder = GraphBuilder()
        count = 0
        for file in root.glob('*.jsonl'):
            session_entity_id = f'session:{file.stem}'
            builder.upsert_entity(EntityRecord(
                entity_id=session_entity_id,
                entity_type='session',
                name=file.stem,
                metadata={'path': str(file)},
                trust_score=score_memory('memory', verified=False, recency_weight=0.7),
            ))
            for idx, line in enumerate(file.read_text(errors='ignore').splitlines()[:200]):
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                role = obj.get('message', {}).get('role')
                if not role:
                    continue
                msg_id = f'{session_entity_id}:msg:{idx}'
                builder.upsert_entity(EntityRecord(
                    entity_id=msg_id,
                    entity_type='message',
                    name=role,
                    metadata={'role': role},
                    trust_score=score_memory('memory', verified=False, recency_weight=0.6),
                ))
                builder.upsert_edge(EdgeRecord(
                    edge_id=f'edge:{session_entity_id}:{msg_id}',
                    from_entity_id=session_entity_id,
                    to_entity_id=msg_id,
                    edge_type='CONTAINS',
                    metadata={},
                ))
                count += 1
        return {'ingested_messages': count}

