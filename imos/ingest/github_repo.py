from pathlib import Path
import subprocess
from imos.services.graph_builder import GraphBuilder
from imos.models import EntityRecord, EdgeRecord
from imos.services.trust_engine import score_memory

class GitHubRepoIngestor:
    def ingest_repo(self, path: str):
        root = Path(path)
        builder = GraphBuilder()
        repo_name = root.name
        repo_id = f'repo:{repo_name}'
        builder.upsert_entity(EntityRecord(
            entity_id=repo_id,
            entity_type='repo',
            name=repo_name,
            metadata={'path': str(root)},
            trust_score=score_memory('github', verified=True, recency_weight=0.9),
        ))
        try:
            head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            commit_id = f'commit:{head[:12]}'
            builder.upsert_entity(EntityRecord(
                entity_id=commit_id,
                entity_type='commit',
                name=head[:12],
                metadata={'sha': head},
                trust_score=score_memory('github', verified=True, recency_weight=1.0),
            ))
            builder.upsert_edge(EdgeRecord(
                edge_id=f'edge:{repo_id}:{commit_id}',
                from_entity_id=repo_id,
                to_entity_id=commit_id,
                edge_type='HAS_HEAD',
                metadata={},
            ))
        except Exception:
            pass
        return {'repo': repo_name}

