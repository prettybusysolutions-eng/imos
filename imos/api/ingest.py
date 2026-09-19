from fastapi import APIRouter
from imos.ingest.memory_files import MemoryFileIngestor
from imos.ingest.session_logs import SessionLogIngestor
from imos.ingest.github_repo import GitHubRepoIngestor
from imos.ingest.github_events import GitHubEventIngestor

router = APIRouter()

@router.post('/memory-files')
def ingest_memory_files(path: str):
    return MemoryFileIngestor().ingest_directory(path)

@router.post('/session-logs')
def ingest_session_logs(path: str):
    return SessionLogIngestor().ingest_directory(path)

@router.post('/github-repo')
def ingest_github_repo(path: str):
    return GitHubRepoIngestor().ingest_repo(path)

@router.post('/github-event-file')
def ingest_github_event_file(path: str):
    return GitHubEventIngestor().ingest_file(path)

