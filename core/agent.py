import json
import os
from groq import Groq
import config
from config import SYSTEM_PROMPT, MAX_TOOL_ROUNDS, HISTORY_LIMIT
from core.model_manager import ModelManager
from tools.file_manager import Workspace
from tools.calculator import calculate
from tools.browser import web_search, fetch_webpage
from core.memory import MemoryStore
from core.tasks import TaskStore

class Agent:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.models = ModelManager(self.client)
        self.models.refresh()
        if not self.models.selected:
            raise RuntimeError("No suitable Groq chat model was available for this API key.")
        self.workspace = Workspace(config.WORKSPACE_ROOT)
        self.memory = MemoryStore(config.WORKSPACE_ROOT)
        self.tasks = TaskStore(config.WORKSPACE_ROOT)
        self.history = []

    def tool_specs(self):
        return [
            {"type":"function","function":{"name":"calculate","description":"Safely calculate arithmetic.","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}}},
            {"type":"function","function":{"name":"create_folder","description":"Create a folder inside the workspace.","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
            {"type":"function","function":{"name":"create_file","description":"Create a UTF-8 text file inside workspace. If it exists, confirmation is required.","parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
            {"type":"function","function":{"name":"read_file","description":"Read a text file inside workspace.","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
            {"type":"function","function":{"name":"edit_file","description":"Replace a text file's content inside workspace.","parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
            {"type":"function","function":{"name":"list_files","description":"List files/folders inside workspace.","parameters":{"type":"object","properties":{"path":{"type":"string"}}}}},
            {"type":"function","function":{"name":"delete_file","description":"Delete a file. Requires confirmed=true from an explicit user confirmation.","parameters":{"type":"object","properties":{"path":{"type":"string"},"confirmed":{"type":"boolean"}},"required":["path"]}}},
            {"type":"function","function":{"name":"web_search","description":"Search public web pages using a browser.","parameters":{"type":"object","properties":{"query":{"type":"string"},"limit":{"type":"integer"}},"required":["query"]}}},
            {"type":"function","function":{"name":"fetch_webpage","description":"Open a public URL and extract visible text.","parameters":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}}},
            {"type":"function","function":{"name":"save_memory","description":"Save a useful non-sensitive preference/fact.","parameters":{"type":"object","properties":{"key":{"type":"string"},"value":{"type":"string"}},"required":["key","value"]}}},
            {"type":"function","function":{"name":"list_memory","description":"List saved memory.","parameters":{"type":"object","properties":{}}}},
            {"type":"function","function":{"name":"delete_memory","description":"Delete saved memory by key.","parameters":{"type":"object","properties":{"key":{"type":"string"}},"required":["key"]}}},
            {"type":"function","function":{"name":"add_task","description":"Add a task.","parameters":{"type":"object","properties":{"title":{"type":"string"}},"required":["title"]}}},
            {"type":"function","function":{"name":"list_tasks","description":"List tasks.","parameters":{"type":"object","properties":{}}}},
            {"type":"function","function":{"name":"complete_task","description":"Complete a task by ID.","parameters":{"type":"object","properties":{"task_id":{"type":"integer"}},"required":["task_id"]}}},
        ]

    def call_tool(self, name, args):
        try:
            if name == "calculate": return calculate(args["expression"])
            if name == "create_folder": return self.workspace.create_folder(args["path"])
            if name == "create_file": return self.workspace.create_file(args["path"], args["content"])
            if name == "read_file": return self.workspace.read_file(args["path"])
            if name == "edit_file": return self.workspace.edit_file(args["path"], args["content"])
            if name == "list_files": return self.workspace.list_files(args.get("path", "."))
            if name == "delete_file": return self.workspace.delete_file(args["path"], args.get("confirmed", False))
            if name == "web_search": return web_search(args["query"], args.get("limit", 5))
            if name == "fetch_webpage": return fetch_webpage(args["url"])
            if name == "save_memory": return self.memory.save(args["key"], args["value"])
            if name == "list_memory": return self.memory.list()
            if name == "delete_memory": return self.memory.delete(args["key"])
            if name == "add_task": return self.tasks.add(args["title"])
            if name == "list_tasks": return self.tasks.list()
            if name == "complete_task": return self.tasks.complete(args["task_id"])
            return {"status":"error","message":"Unknown tool"}
        except Exception as e:
            return {"status":"error","message":str(e)}

    def ask(self, text):
        memories = self.memory.list()
        memory_context = ""
        if memories:
            memory_context = "\nRelevant persistent memory:\n" + json.dumps(memories, ensure_ascii=False)[:6000]
        messages = [{"role":"system","content":SYSTEM_PROMPT + memory_context}]
        messages += self.history[-HISTORY_LIMIT:]
        messages.append({"role":"user","content":text})

        for _ in range(MAX_TOOL_ROUNDS):
            resp = self.client.chat.completions.create(
                model=self.models.selected,
                messages=messages,
                tools=self.tool_specs(),
                tool_choice="auto",
            )
            msg = resp.choices[0].message
            tool_calls = getattr(msg, "tool_calls", None)
            if not tool_calls:
                answer = msg.content or ""
                self.history.extend([{"role":"user","content":text},{"role":"assistant","content":answer}])
                self.history = self.history[-HISTORY_LIMIT:]
                return answer

            assistant_message = {"role":"assistant","content":msg.content or "",
                                 "tool_calls":[{"id":tc.id,"type":"function",
                                                "function":{"name":tc.function.name,"arguments":tc.function.arguments}}
                                               for tc in tool_calls]}
            messages.append(assistant_message)
            for tc in tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                result = self.call_tool(tc.function.name, args)
                messages.append({"role":"tool","tool_call_id":tc.id,
                                 "content":json.dumps(result, ensure_ascii=False, default=str)})
        return "NEXUM stopped after reaching the tool-round limit."
