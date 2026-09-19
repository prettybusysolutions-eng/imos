from pathlib import Path
from imos.ingest.session_logs import SessionLogIngestor

def test_session_ingest(tmp_path: Path):
    f = tmp_path / 's.jsonl'
    f.write_text('{"message":{"role":"user"}}\n{"message":{"role":"assistant"}}\n')
    out = SessionLogIngestor().ingest_directory(str(tmp_path))
    assert out['ingested_messages'] == 2

