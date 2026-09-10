from pathlib import Path
from tools.file_manager import Workspace

def test_workspace(tmp_path):
    ws = Workspace(tmp_path)
    result = ws.create_file("hello.txt", "hello")
    assert result["status"] == "success"
    assert ws.read_file("hello.txt")["content"] == "hello"
