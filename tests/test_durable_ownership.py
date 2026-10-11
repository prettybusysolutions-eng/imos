import hashlib
import sqlite3
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from imos.app import create_app
from imos.storage import DecisionStore

def digest(key): return hashlib.sha256(key.encode()).hexdigest()
KEYS={'alice':digest('alice-secret'),'bob':digest('bob-secret')}
RECORD={'decision_id':'one','title':'Release','reason':'Tests passed'}

def test_owner_isolation_duplicate_and_restart():
    with tempfile.TemporaryDirectory() as root:
        path=str(Path(root)/'memory.sqlite')
        with TestClient(create_app(path,KEYS)) as client:
            assert client.get('/ready').status_code==200
            assert client.post('/decisions/',json=RECORD).status_code==401
            assert client.post('/decisions/',headers={'x-api-key':'alice-secret'},json=RECORD).status_code==201
            assert client.post('/decisions/',headers={'x-api-key':'alice-secret'},json=RECORD).status_code==409
            assert client.get('/decisions/',headers={'x-api-key':'bob-secret'}).json()['items']==[]
            assert client.post('/decisions/',headers={'x-api-key':'bob-secret'},json=RECORD).status_code==201
        with TestClient(create_app(path,KEYS)) as restarted:
            assert restarted.get('/decisions/',headers={'x-api-key':'alice-secret'}).json()['items']==[dict(RECORD,context=None,verification_result=None,downstream_artifacts=[])]

def test_unconfigured_auth_is_unavailable():
    with tempfile.TemporaryDirectory() as root:
        with TestClient(create_app(str(Path(root)/'db'),{})) as client:
            assert client.get('/ready').status_code==503
            assert client.get('/decisions/').status_code==503

def test_unknown_schema_does_not_get_silently_rewritten():
    with tempfile.TemporaryDirectory() as root:
        path=str(Path(root)/'db')
        with sqlite3.connect(path) as db: db.execute('PRAGMA user_version=99')
        with pytest.raises(RuntimeError): DecisionStore(path).migrate()

def test_reused_owner_credentials_are_rejected():
    with pytest.raises(ValueError): create_app(owner_keys={'alice':digest('same'),'bob':digest('same')})
