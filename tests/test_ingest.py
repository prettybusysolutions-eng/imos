from pathlib import Path
from imos.ingest.memory_files import MemoryFileIngestor

def test_ingest_directory(tmp_path: Path):
    (tmp_path / 'a.md').write_text('# hi')
    out = MemoryFileIngestor().ingest_directory(str(tmp_path))
    assert out['ingested'] == 1

