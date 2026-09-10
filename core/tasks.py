import json
from pathlib import Path
from datetime import datetime, timezone

class TaskStore:
    def __init__(self, root):
        self.path = Path(root) / "data" / "tasks.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save(self, data):
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, title):
        tasks = self._load()
        task = {"id": (max([x.get("id", 0) for x in tasks], default=0) + 1),
                "title": title, "status": "open",
                "created_at": datetime.now(timezone.utc).isoformat()}
        tasks.append(task)
        self._save(tasks)
        return {"status": "success", "task": task}

    def list(self):
        return self._load()

    def complete(self, task_id):
        tasks = self._load()
        for task in tasks:
            if task.get("id") == int(task_id):
                task["status"] = "done"
                self._save(tasks)
                return {"status": "success", "task": task}
        return {"status": "error", "message": "Task not found."}
