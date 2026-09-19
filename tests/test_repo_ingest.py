from pathlib import Path
from imos.ingest.github_repo import GitHubRepoIngestor

def test_repo_ingest_handles_non_repo(tmp_path: Path):
    out = GitHubRepoIngestor().ingest_repo(str(tmp_path))
    assert out['repo'] == tmp_path.name

