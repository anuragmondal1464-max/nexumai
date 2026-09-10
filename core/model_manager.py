from groq import Groq
from config import MODEL_OVERRIDE

PREFERRED = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

class ModelManager:
    def __init__(self, client):
        self.client = client
        self.models = []
        self.selected = None

    def refresh(self):
        result = self.client.models.list()
        ids = []
        for m in getattr(result, "data", []):
            mid = getattr(m, "id", None)
            if mid:
                ids.append(mid)
        self.models = ids
        self.selected = self.choose()
        return ids

    def choose(self):
        if MODEL_OVERRIDE and MODEL_OVERRIDE in self.models:
            return MODEL_OVERRIDE
        for name in PREFERRED:
            if name in self.models:
                return name
        # Prefer likely chat-capable models, avoiding obvious embedding/whisper/guard models.
        bad = ("embed", "whisper", "guard", "safeguard", "compound")
        candidates = [m for m in self.models if not any(x in m.lower() for x in bad)]
        return candidates[0] if candidates else None
