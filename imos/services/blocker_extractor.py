import re
from pathlib import Path
from imos.services.graph_builder import GraphBuilder
from imos.models import EntityRecord, EdgeRecord
from imos.services.trust_engine import score_memory

BLOCK_PATTERNS = [
    re.compile(r'blocker[:\-]?\s*(.+)', re.IGNORECASE),
    re.compile(r'blocked by[:\-]?\s*(.+)', re.IGNORECASE),
    re.compile(r'pending[:\-]?\s*(.+)', re.IGNORECASE),
]

class BlockerExtractor:
    def ingest_markdown(self, path: str):
        p = Path(path)
        text = p.read_text(errors='ignore')
        builder = GraphBuilder()
        source_id = f'artifact:{p.name}'
        builder.upsert_entity(EntityRecord(
            entity_id=source_id,
            entity_type='artifact',
            name=p.name,
            metadata={'path': str(p)},
            trust_score=score_memory('memory', verified=False, recency_weight=0.8),
        ))
        found = []
        for idx, line in enumerate(text.splitlines()):
            for pat in BLOCK_PATTERNS:
                m = pat.search(line)
                if m:
                    label = m.group(1).strip()
                    blocker_id = f'blocker:{p.stem}:{idx}'
                    builder.upsert_entity(EntityRecord(
                        entity_id=blocker_id,
                        entity_type='blocker',
                        name=label[:120],
                        metadata={'source_line': idx + 1, 'source_path': str(p)},
                        trust_score=score_memory('memory', verified=False, recency_weight=0.7),
                    ))
                    builder.upsert_edge(EdgeRecord(
                        edge_id=f'edge:{source_id}:{blocker_id}',
                        from_entity_id=source_id,
                        to_entity_id=blocker_id,
                        edge_type='BLOCKED_BY',
                        metadata={'line': idx + 1},
                    ))
                    found.append(label)
        return {'blockers_found': len(found), 'items': found}

