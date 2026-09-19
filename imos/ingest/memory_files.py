from pathlib import Path
from imos.services.graph_builder import GraphBuilder
from imos.models import EntityRecord
from imos.services.trust_engine import score_memory

class MemoryFileIngestor:
    def ingest_directory(self, path: str):
        root = Path(path)
        builder = GraphBuilder()
        count = 0
        for file in root.glob('*.md'):
            entity = EntityRecord(
                entity_id=f'memory:{file.name}',
                entity_type='memory_file',
                name=file.name,
                metadata={'path': str(file), 'size': file.stat().st_size},
                trust_score=score_memory('memory', verified=False, recency_weight=0.8),
            )
            builder.upsert_entity(entity)
            count += 1
        return {'ingested': count}

