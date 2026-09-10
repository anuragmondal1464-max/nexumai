import json
from pathlib import Path
from datetime import datetime, timezone

class MemoryStore:
    def __init__(self, root):
        self.path = Path(root) / "data" / "memory.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self, data):
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def save(self, key, value):
        data = self._load()
        data[key] = {"value": value, "updated_at": datetime.now(timezone.utc).isoformat()}
        self._save(data)
        return {"status": "success", "key": key}

    def list(self):
        return self._load()

    def delete(self, key):
        data = self._load()
        if key not in data:
            return {"status": "error", "message": "Memory key not found."}
        del data[key]
        self._save(data)
        return {"status": "success", "key": key}
