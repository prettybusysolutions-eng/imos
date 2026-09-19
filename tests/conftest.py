"""Keep recovered tests off an operator's database."""
import os
import tempfile
from pathlib import Path

_test_dir = tempfile.TemporaryDirectory(prefix='imos-tests-')
os.environ['IMOS_DATABASE_URL'] = f"sqlite:///{Path(_test_dir.name) / 'tests.db'}"
from imos.storage import Base, engine
from imos import db_models
Base.metadata.create_all(engine)
