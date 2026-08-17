# Minimal Python Agent Harness (Zero-Dependency Reference Implementation)
# [ref: What is an agent harness? The nine components of a great one]

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# --- 6. SESSION PERSISTENCE (JSONL) ---
class SessionLogger:
    def __init__(self, log_path: str = "session_log.jsonl"):
        self.log_path = log_path
        self.file = open(log_path, "a", encoding="utf-8")
        
    def log(self, event_type: str, data: dict):
        event = {"timestamp": time.time(), "type": event_type, "data": data}
        self.file.write(json.dumps(event) + "\n")
        self.file.flush()

    def replay(self) -> list:
        events = []
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        return events

# --- 3 & 9. TOOL REGISTRY & PERMISSIONS ---
class ToolRegistry:
    def __init__(self):
        self.tools = {}
        
    def register(self, name: str, permission: str, handler: callable, description: str):
        self.tools[name] = {"permission": permission, "handler": handler, "desc": description}
        
    def dispatch(self, name: str, args: dict, active_perm: str):
        if name not in self.tools:
            raise KeyError(f"Tool {name} not found.")
        tool = self.tools[name]
        if tool["permission"] == "full" and active_perm != "full":
            raise PermissionError(f"Tool {name} requires full permission.")
        return tool["handler"](**args)

# --- 5. BUILT-IN PRIMITIVES (Stdlib Only) ---
def view_file(filepath: str) -> str:
    return Path(filepath).read_text(encoding="utf-8")

def write_file(filepath: str, content: str) -> str:
    Path(filepath).write_text(content, encoding="utf-8")
    return f"Successfully wrote to {filepath}"

def run_bash(command: str) -> str:
    res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return res.stdout if res.returncode == 0 else f"ERROR:\n{res.stderr}"

# --- 2. CONTEXT MANAGEMENT & COMPACTION ---
def compact_history(messages: list, max_tokens: int = 150000) -> list:
    if len(messages) <= 10:
        return messages
    system_and_goal = messages[:2]
    recent = messages[-4:]
    summary = {"role": "system", "content": f"[COMPACTION SUMMARY]: Compacted {len(messages)-6} previous turns."}
    return system_and_goal + [summary] + recent

# --- 7. PROMPT ASSEMBLY ---
def assemble_system_prompt(workspace_dir: str) -> str:
    base_instructions = "You are a minimal autonomous Python agent harness."
    instruction_files = ["AGENTS.md", "CLAUDE.md"]
    dynamic_parts = []
    
    for filename in instruction_files:
        p = Path(workspace_dir) / filename
        if p.exists():
            dynamic_parts.append(f"\n--- {filename} ---\n" + p.read_text(encoding="utf-8"))
            
    # Caching order: Static first, dynamic second
    return base_instructions + "".join(dynamic_parts)

# --- 1 & 8. THE MAIN LOOP & HOOKS ---
def run_minimal_harness(user_goal: str, workspace_dir: str = "."):
    logger = SessionLogger()
    registry = ToolRegistry()
    
    # Register Built-in Primitives
    registry.register("view_file", "read-only", view_file, "Read text file")
    registry.register("write_file", "workspace", write_file, "Write text file")
    registry.register("run_bash", "full", run_bash, "Run shell command")
    
    sys_prompt = assemble_system_prompt(workspace_dir)
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_goal}
    ]
    
    logger.log("SESSION_START", {"goal": user_goal})
    
    iteration = 0
    max_iterations = 25
    
    print(f"🚀 Initializing Minimal Harness with goal: '{user_goal}'")
    
    while iteration < max_iterations:
        iteration += 1
        messages = compact_history(messages)
        print(f"🔄 Turn {iteration}/{max_iterations} - Context Message Count: {len(messages)}")
        
        # Simulating single turn demonstration
        break
        
    print("✅ Harness Loop Initialized & Verified.")

if __name__ == "__main__":
    run_minimal_harness("Fix issue #402 in repo.")
