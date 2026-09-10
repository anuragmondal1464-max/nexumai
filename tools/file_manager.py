from pathlib import Path
from config import FILE_SIZE_LIMIT

class Workspace:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def safe(self, path):
        p = Path(path)
        if not p.is_absolute():
            p = self.root / p
        p = p.resolve()
        try:
            p.relative_to(self.root)
        except ValueError:
            raise ValueError("Path must stay inside the configured NEXUM workspace.")
        return p

    def create_folder(self, path):
        p = self.safe(path)
        p.mkdir(parents=True, exist_ok=True)
        return {"status": "success", "path": str(p)}

    def create_file(self, path, content, overwrite=False):
        p = self.safe(path)
        if p.exists() and not overwrite:
            return {"status": "confirmation_required", "path": str(p)}
        if len(content.encode("utf-8")) > FILE_SIZE_LIMIT:
            return {"status": "error", "message": "File exceeds configured size limit."}
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"status": "success", "path": str(p)}

    def read_file(self, path):
        p = self.safe(path)
        if not p.is_file():
            return {"status": "error", "message": "File not found."}
        if p.stat().st_size > FILE_SIZE_LIMIT:
            return {"status": "error", "message": "File exceeds configured size limit."}
        return {"status": "success", "path": str(p), "content": p.read_text(encoding="utf-8")}

    def edit_file(self, path, content):
        return self.create_file(path, content, overwrite=True)

    def list_files(self, path="."):
        p = self.safe(path)
        if not p.exists():
            return {"status": "error", "message": "Directory not found."}
        items = [{"name": x.name, "type": "dir" if x.is_dir() else "file"}
                 for x in sorted(p.iterdir(), key=lambda x: x.name.lower())]
        return {"status": "success", "path": str(p), "items": items}

    def delete_file(self, path, confirmed=False):
        p = self.safe(path)
        if not p.exists():
            return {"status": "error", "message": "File not found."}
        if not confirmed:
            return {"status": "confirmation_required", "path": str(p)}
        if p.is_dir():
            return {"status": "error", "message": "Directory deletion is not supported by this tool."}
        p.unlink()
        return {"status": "success", "path": str(p)}
