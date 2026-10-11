"""Versioned SQLite pilot storage. Owner is assigned by authentication, not input."""
import json
import sqlite3
from pathlib import Path

class DecisionStore:
    def __init__(self, path):
        self.path = str(path)
    def connect(self):
        return sqlite3.connect(self.path, timeout=30)
    def migrate(self):
        Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            version=db.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0,1):
                raise RuntimeError('Unsupported IMOS storage version; explicit migration required')
            db.execute('CREATE TABLE IF NOT EXISTS decisions(owner TEXT NOT NULL,decision_id TEXT NOT NULL,payload TEXT NOT NULL,PRIMARY KEY(owner,decision_id))')
            db.execute('PRAGMA user_version=1')
    def ready(self):
        with self.connect() as db:
            if db.execute('PRAGMA user_version').fetchone()[0]!=1: return False
            db.execute('SELECT owner,decision_id,payload FROM decisions LIMIT 1')
            return True
    def create(self, owner, record):
        payload=record.model_dump()
        with self.connect() as db:
            db.execute('INSERT INTO decisions(owner,decision_id,payload) VALUES(?,?,?)',
                       (owner,record.decision_id,json.dumps(payload)))
        return payload
    def list(self, owner):
        with self.connect() as db:
            return [json.loads(row[0]) for row in db.execute('SELECT payload FROM decisions WHERE owner=? ORDER BY decision_id',(owner,))]
