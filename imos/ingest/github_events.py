from pathlib import Path
import json
from imos.services.graph_builder import GraphBuilder
from imos.models import EntityRecord, EdgeRecord
from imos.services.trust_engine import score_memory

class GitHubEventIngestor:
    def ingest_file(self, path: str):
        p = Path(path)
        data = json.loads(p.read_text())
        builder = GraphBuilder()
        event_type = data.get('event') or data.get('action') or 'github_event'
        event_id = f'github-event:{p.stem}'
        builder.upsert_entity(EntityRecord(
            entity_id=event_id,
            entity_type='github_event',
            name=event_type,
            metadata={'path': str(p)},
            trust_score=score_memory('github', verified=True, recency_weight=0.95),
        ))
        repo = data.get('repository') or {}
        repo_name = repo.get('full_name') or repo.get('name')
        if repo_name:
            repo_id = f'repo:{repo_name}'
            builder.upsert_entity(EntityRecord(
                entity_id=repo_id,
                entity_type='repo',
                name=repo_name,
                metadata={'source': 'github_event'},
                trust_score=score_memory('github', verified=True, recency_weight=0.9),
            ))
            builder.upsert_edge(EdgeRecord(
                edge_id=f'edge:{event_id}:{repo_id}',
                from_entity_id=event_id,
                to_entity_id=repo_id,
                edge_type='IMPACTS',
                metadata={},
            ))
        return {'event_id': event_id, 'repo': repo_name}

