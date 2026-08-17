"""Analyze harness-engineering diagrams using Qwen3.8-27B vision (reasoning_effort=xhigh)."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client.qwen_client import QwenClient

DIAGRAMS_DIR = Path(__file__).resolve().parent.parent / "harness-engineering" / "images" / "diagrams"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "harness-engineering-analysis"

SECTION_MAP = {
    "sec1-AI Agent System Architecture.png": 1,
    "sec2-Framework vs. Harness Paradigms in AI Development.png": 2,
    "sec-3-What is an agent harness The nine components of a great one.png": 3,
    "sec-3-Harness Execution Loop Process.png": 3,
    "sec-4-Agent Harness Compaction Process.png": 4,
    "sec-4-LLM History Compaction Process.png": 4,
    "sec-5=LLM Tool Execution Flow.png": 5,
    "sec-6-Parent-Harness-Subagent-Workflow.png": 6,
    "sec-7-Session Persistence and Prompt Pipeline Architecture.png": 7,
    "sec-8-tool-execution-workflow.png": 8,
    "sec-9-Tsinghua NLAH Module Ablation Analysis.png": 9,
    "sec-10 Minimal Python Agent.png": 10,
}

PROMPT = """Analyze this technical diagram for a video course on Agent Harness Engineering.

Provide a JSON object with these exact keys:
{
  "title": "Short title for this diagram (max 8 words)",
  "section_number": <int>,
  "components": ["List of key components/boxes shown in the diagram"],
  "relationships": ["Key connections/arrows/flows between components"],
  "visual_elements": ["3-5 key visual elements to reproduce in a video scene"],
  "key_points": ["3-5 teaching points this diagram conveys"],
  "suggested_clip_length": <int seconds, 30-42>
}

Return ONLY the JSON object, no markdown fences."""


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    client = QwenClient()
    results = []
    diagrams = sorted(DIAGRAMS_DIR.glob("*.png"))
    print(f"Analyzing {len(diagrams)} diagrams at reasoning_effort=xhigh...", flush=True)
    for i, diagram in enumerate(diagrams, 1):
        section = SECTION_MAP.get(diagram.name, 0)
        print(f"[{i}/{len(diagrams)}] Section {section}: {diagram.name}", end="", flush=True)
        t0 = time.time()
        try:
            response = client.ask_image(str(diagram), PROMPT, reasoning_effort="xhigh", max_tokens=2048)
            elapsed = time.time() - t0
            print(f" ({elapsed:.1f}s)")
            try:
                clean = response.strip()
                if clean.startswith("```"):
                    clean = clean.split("```")[1]
                    if clean.startswith("json"):
                        clean = clean[4:]
                    clean = clean.strip()
                parsed = json.loads(clean)
                parsed["source_file"] = diagram.name
                parsed["section_number"] = section
                results.append(parsed)
            except json.JSONDecodeError:
                results.append({"section_number": section, "source_file": diagram.name, "raw_response": response, "error": "JSON parse failed"})
        except Exception as e:
            elapsed = time.time() - t0
            print(f" ERROR ({elapsed:.1f}s): {e}")
            results.append({"section_number": section, "source_file": diagram.name, "error": str(e)})
    output_path = OUTPUT_DIR / "scene_descriptions.json"
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved {len(results)} analyses to {output_path}")
    print("\n=== Summary ===")
    for r in sorted(results, key=lambda x: x.get("section_number", 0)):
        sec = r.get("section_number", "?")
        title = r.get("title", r.get("error", "UNKNOWN"))
        print(f"  Section {sec}: {title}")


if __name__ == "__main__":
    main()