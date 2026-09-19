from pathlib import Path
import json
from imos.ingest.github_events import GitHubEventIngestor

def test_github_event_ingest(tmp_path: Path):
    p = tmp_path / 'e.json'
    p.write_text(json.dumps({'event':'push','repository':{'full_name':'prettybusysolutions-eng/imos'}}))
    out = GitHubEventIngestor().ingest_file(str(p))
    assert out['repo'] == 'prettybusysolutions-eng/imos'

