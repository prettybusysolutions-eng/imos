import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from imos.ingest.memory_files import MemoryFileIngestor
from imos.ingest.session_logs import SessionLogIngestor
from imos.ingest.github_repo import GitHubRepoIngestor
from imos.services.blocker_extractor import BlockerExtractor
from imos.services.entity_linker import EntityLinker

WORKSPACE = Path('/Users/marcuscoarchitect/.openclaw/workspace-aurex')
REPO = Path('/Users/marcuscoarchitect/.openclaw/agents/aurex/workspace/projects/imos')
SESSIONS = Path('/Users/marcuscoarchitect/.openclaw/agents/aurex/sessions')


def seed_all():
    out = {}
    if WORKSPACE.joinpath('memory').exists():
        out['memory'] = MemoryFileIngestor().ingest_directory(str(WORKSPACE / 'memory'))
    if SESSIONS.exists():
        out['sessions'] = SessionLogIngestor().ingest_directory(str(SESSIONS))
    out['repo'] = GitHubRepoIngestor().ingest_repo(str(REPO))
    hb = WORKSPACE / 'HEARTBEAT.md'
    if hb.exists():
        out['blockers'] = BlockerExtractor().ingest_markdown(str(hb))
    out['links'] = EntityLinker().link_same_name()
    return out

if __name__ == '__main__':
    print(seed_all())
