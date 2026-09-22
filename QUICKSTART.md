# Quickstart

## Run the verified path

```bash
git clone https://github.com/prettybusysolutions-eng/imos.git
cd imos
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt httpx pytest
.venv/bin/python -m pytest -q
.venv/bin/uvicorn imos.app:app --host 127.0.0.1 --port 8010
```

In another terminal:

```bash
curl --fail http://127.0.0.1:8010/health
```

Expected response:

```json
{"status":"ok","service":"imos"}
```

This proves the public API surface is runnable. It does not prove durable
storage, authentication, or production readiness; those remain outside the
current alpha boundary.
