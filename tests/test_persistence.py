import json
import os
import subprocess
import sys
from fastapi.testclient import TestClient
from imos.app import app


def test_decision_survives_new_process_and_updates_without_duplication():
    client = TestClient(app)
    record = {'decision_id': 'persistence-proof', 'title': 'Restore persistence', 'reason': 'A stored claim must survive restart'}
    assert client.post('/decisions/', json=record).status_code == 200
    record['reason'] = 'Updated evidence'
    assert client.post('/decisions/', json=record).status_code == 200
    script = 'import json; from imos.services.query_service import QueryService; print(json.dumps(QueryService().decisions()))'
    result = subprocess.run([sys.executable, '-c', script], check=True, text=True, capture_output=True, env=os.environ.copy())
    stored = [r for r in json.loads(result.stdout) if r['decision_id'] == record['decision_id']]
    assert len(stored) == 1
    assert stored[0]['reason'] == 'Updated evidence'
