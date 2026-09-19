from pathlib import Path
from imos.services.blocker_extractor import BlockerExtractor

def test_blocker_extract(tmp_path: Path):
    f = tmp_path / 'notes.md'
    f.write_text('Blocker: webhook ingress still unstable\n')
    out = BlockerExtractor().ingest_markdown(str(f))
    assert out['blockers_found'] == 1

