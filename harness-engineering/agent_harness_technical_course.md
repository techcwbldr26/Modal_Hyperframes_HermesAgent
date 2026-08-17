# What is an Agent Harness? and How to Build One

**Video Reference:** [https://youtu.be/8vUCjYsWeSU](https://youtu.be/8vUCjYsWeSU) ("Prime-Agent: We've Been Building AI Agents Wrong?" / "What is an Agent Harness? and How to Build One" by Muhammad Farooq)  
**Reference Documents:**

- `Harness engineering: why agent performance now lives outside the model · Muhammad Farooq`  
- `What is an agent harness? The nine components of a great one · Muhammad Farooq`

---

## REFERENCE INVENTORY

1. **`Harness engineering_ why agent performance now lives outside the model · Muhammad Farooq.pdf`** — *PDF Research Essay* — Examines how orchestration logic, context management, memory, and safety (the harness) drive up to 6x performance variance over identical model weights. Cites 2026 findings from Tsinghua (NLAH) and Stanford (Meta-Harness). `[ref: Harness engineering: why agent performance now lives outside the model]`  
2. **`What is an agent harness_ The nine components of a great one · Muhammad Farooq.pdf`** — *PDF Architectural Essay* — Defines the 9 structural components of an agent harness (Loop, Context Management, Tools & Skills, Sub-Agents, Built-in Skills, Persistence, Prompt Assembly, Hooks, Permissions/Safety) and contrasts harnesses with assembly frameworks. `[ref: What is an agent harness? The nine components of a great one]`

---

# SECTION 1: Introduction to Agent Harness Engineering

### 1\. Content Analysis

To understand why modern AI agents succeed or fail in production, stop looking exclusively at model weights and start engineering the scaffolding around them `[00:00–00:45]`.

1. **Define the Core Agent Formula:** Recognize that a raw Large Language Model (LLM) is merely a stateless, one-shot text completion engine `[00:15–00:30]`. `[ref: What is an agent harness? The nine components of a great one]`  
     
   - Formulate your system around the identity equation: $$\\text{Agent} \= \\text{Model (Weights)} \+ \\text{Harness (Operating System)}$$  
   - Treat the **Model** as the raw cognitive engine and the **Harness** as the vehicle environment that enables persistent, multi-step execution.

   

2. **Map the Operating System Analogy:** Anchor your architecture in computer systems fundamentals `[00:45–01:25]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
     
   - **LLM $\\rightarrow$ CPU:** The language model acts as the Central Processing Unit, executing raw reasoning cycles.  
   - **Context Window $\\rightarrow$ RAM:** The context window is high-speed but limited volatile memory.  
   - **External Databases / Vector Stores $\\rightarrow$ Hard Disk:** Persistent storage for long-term knowledge and state.  
   - **Tools & Function Bindings $\\rightarrow$ Device Drivers:** Interfaces that connect reasoning to external execution environments (filesystems, web browsers, bash terminals).  
   - **The Harness $\\rightarrow$ Operating System:** The surrounding orchestration engine that schedules CPU cycles, manages RAM allocation, dispatches device driver calls, enforces security boundaries, and determines when a task is completed.

   

3. **Diagnose the Performance Gap:** Identify why two teams using identical model weights (e.g., GPT-5.4 or Claude 3.7 Sonnet) can experience up to a 6x difference in benchmark performance (such as SWE-bench Verified or Terminal-Bench 2\) `[01:25–02:00]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
     
   - Avoid swapping model versions as your primary optimization lever when performance plateaus.  
   - Audit the harness layer: system prompts, context compaction rules, tool registries, verification loops, and failure-handling taxonomies.

---

### 2\. Key Concepts

- **Agent vs. Model:** A language model takes text in and outputs text out. An agent combines a model with an active execution harness that loops through action, observation, and state persistence `[00:15]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **The OS Analogy:** Architectural mapping where LLM \= CPU, Context Window \= RAM, Database \= Disk, Tools \= Drivers, and Harness \= OS `[00:50]` `[ref: Harness engineering: why agent performance now lives outside the model]`.  
- **Harness Engineering Variance:** Empirical research demonstrates that orchestration code drives significantly more performance variation on real-world tasks than incremental weight updates `[01:40]` `[ref: Harness engineering: why agent performance now lives outside the model]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph AGENT \["AI AGENT SYSTEM"\]

        direction TB

        subgraph MODEL\_LAYER \["1. Cognition (Model Weights)"\]

            CPU\["LLM Engine / Central Processing Unit"\]

        end

        subgraph HARNESS\_LAYER \["2. Harness Layer (Operating System Scaffolding)"\]

            direction TB

            RAM\["Context Window (RAM Budget)"\]

            DISK\["External DB / State Files (Disk Storage)"\]

            DRIVERS\["Tool Registry (Device Drivers)"\]

            SCHEDULER\["Loop & Execution Controller (OS Kernel)"\]

            SAFETY\["Permissions & Hooks (Security Sandbox)"\]

        end

    end

    CPU \<--\>|"Inference Calls / Responses"| SCHEDULER

    SCHEDULER \<--\>|"Compaction & Truncation"| RAM

    SCHEDULER \<--\>|"Append JSONL / State Flush"| DISK

    SCHEDULER \<--\>|"Tool Dispatch & Result Capture"| DRIVERS

    SCHEDULER \<--\>|"Pre-Tool Interception"| SAFETY

    style AGENT fill:\#0f172a,stroke:\#3b82f6,stroke-width:2px,color:\#fff

    style MODEL\_LAYER fill:\#1e1b4b,stroke:\#6366f1,stroke-width:2px,color:\#fff

    style HARNESS\_LAYER fill:\#090d16,stroke:\#10b981,stroke-width:2px,color:\#fff

    style CPU fill:\#4338ca,stroke:\#818cf8,color:\#fff

    style SCHEDULER fill:\#047857,stroke:\#34d399,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_1\_os\_analogy.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_1_os_analogy.html)

---

# SECTION 2: Framework vs. Harness — Resolving the Confusion — \[02:00–04:30\]

### 1\. Content Analysis

One of the most pervasive confusions in AI software development is blurring the distinction between an **Agent Framework** and an **Agent Harness** `[02:00–02:20]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Distinguish Frameworks from Harnesses:**  
     
   - **Frameworks (e.g., LangChain, LangGraph, AutoGen, CrewAI):** Conceptualize a framework as a toolbox of modular building blocks (chains, DAG state graphs, memory adapters, retrievers) `[02:20–03:00]`. `[ref: What is an agent harness? The nine components of a great one]`  
     - *Human Role:* You, the developer, are responsible for wiring, assembling, and maintaining the control flow loop.  
     - *Target User:* A developer building a custom application.  
   - **Harnesses (e.g., Claude Code, Codex, Cursor, Windsurf):** Conceptualize a harness as a pre-wired, production-ready, autonomous agent system `[03:00–03:40]`. `[ref: What is an agent harness? The nine components of a great one]`  
     - *Human Role:* You supply only the high-level task goal (e.g., `"Fix issue #402 in the repository"`).  
     - *Target User:* The agent itself, which operates within the pre-packaged execution engine.

   

2. **Evaluate the Trade-offs:**  
     
   - Choose a **Framework** when building domain-specific, custom workflow DAGs where human developers must define explicit state transitions at compile time.  
   - Choose or build a **Harness** when you need a general-purpose, self-directed loop that dynamically navigates real-world environments (filesystems, shells, IDEs) using standardized tool registries and safety policies.

   

3. **Recognize the Industry Convergence:** Observe how tools like Claude Code, Cursor, and Windsurf have independently converged on nearly identical harness architectures (the 9 structural components) `[03:40–04:30]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **Framework:** Assembly parts for human developers. Provides primitive abstractions (chains, state nodes) requiring manual wiring `[02:30]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Harness:** A complete, pre-wired agent engine. Ships with loop, context manager, tool registry, session logger, and safety rules ready for task execution `[03:10]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Assembly Responsibility:** Frameworks require developer assembly; Harnesses ask only for a user goal `[03:45]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph FRAMEWORK\_PARADIGM \["FRAMEWORK PARADIGM (LangChain, AutoGen, CrewAI)"\]

        direction TB

        F\_PARTS\["Building Blocks: Chains, Retrievers, State Nodes"\]

        F\_DEV\["Developer Work: Manual Wiring & Loop Assembly Required"\]

        F\_OUTPUT\["Custom App Pipeline"\]

        F\_PARTS \--\> F\_DEV \--\> F\_OUTPUT

    end

    subgraph HARNESS\_PARADIGM \["HARNESS PARADIGM (Claude Code, Cursor, Windsurf)"\]

        direction TB

        H\_GOAL\["User Goal: 'Fix Issue \#402'"\]

        subgraph PREWIRED\_ENGINE \["Pre-Wired Agent Harness Engine"\]

            H\_LOOP\["Execution Loop (Read \-\> Act \-\> Observe)"\]

            H\_TOOLS\["Tool Registry & Built-ins"\]

            H\_PERM\["Permissions & Safety Layer"\]

            H\_STATE\["Session Persistence (JSONL)"\]

        end

        H\_WORK\["Agent Operates Directly on Workspace"\]

        H\_GOAL \--\> PREWIRED\_ENGINE \--\> H\_WORK

    end

    style FRAMEWORK\_PARADIGM fill:\#1e293b,stroke:\#64748b,stroke-width:2px,color:\#fff

    style HARNESS\_PARADIGM fill:\#0f172a,stroke:\#3b82f6,stroke-width:2px,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_2\_framework\_vs\_harness.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_2_framework_vs_harness.html)

---

# SECTION 3: Component 1 — The Execution Loop — \[04:30–06:45\]

### 1\. Content Analysis

At its absolute core, an agent harness is a `while` loop `[04:30–05:00]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Understand the Mechanics of the Core Loop:**  
     
   - Recognize that language models have no native concept of time, multi-step execution, or state iteration.  
   - Implement the fundamental agent loop cycle `[05:00–05:45]`: $$\\text{Read State} \\longrightarrow \\text{Model Decisions (Act)} \\longrightarrow \\text{Execute Tool} \\longrightarrow \\text{Feed Observation (Observe)} \\longrightarrow \\text{Repeat}$$

   

2. **Implement the Python Execution Loop Architecture:**  
     
   - Construct the loop with explicit safeguards, max iteration counters, and clean termination boundaries `[05:45–06:30]`. `[ref: What is an agent harness? The nine components of a great one]`

\# \[ref: What is an agent harness? The nine components of a great one\]

def run\_agent\_loop(system\_prompt: str, user\_goal: str, max\_iterations: int \= 30):

    messages \= \[

        {"role": "system", "content": system\_prompt},

        {"role": "user", "content": user\_goal}

    \]

    iteration \= 0

    while iteration \< max\_iterations:

        iteration \+= 1

        print(f"--- Turn {iteration} \---")

        \# 1\. READ & CALL MODEL

        response \= llm\_client.completion(messages=messages, tools=registered\_tools)

        messages.append(response.message)

        

        \# 2\. CHECK TERMINATION CONDITION

        if not response.has\_tool\_calls():

            print("Agent finished task with final answer.")

            return response.text       

        \# 3\. ACT: EXECUTE TOOL CALLS

        for tool\_call in response.tool\_calls:

            print(f"Executing tool: {tool\_call.name}")

            tool\_result \= dispatch\_tool(tool\_call.name, tool\_call.args)

    
            \# 4\. OBSERVE: FEED RESULT BACK INTO CONTEXT

            messages.append({

                "role": "tool",

                "tool\_call\_id": tool\_call.id,

                "content": str(tool\_result)

            })

    raise TimeoutError("Agent exceeded max iteration budget.")

3. **Identify the Inherent Loop Problem:**  
   - Note that while the `while` loop turns a model into an agent, **every turn makes the conversation transcript longer**. This immediately creates the problem that Component 2 (Context Management) must solve `[06:30–06:45]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **The Harness Loop:** The central `while` loop driving Read $\\rightarrow$ Act $\\rightarrow$ Observe $\\rightarrow$ Repeat `[04:45]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Termination Conditions:** The loop terminates when the model outputs text with zero tool calls or when `iteration == max_iterations` `[05:30]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Transcript Growth Problem:** Every turn appends assistant tool calls and user tool results, exhausting context RAM `[06:35]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

stateDiagram-v2

    \[\*\] \--\> InitializeSession: Load System Prompt & Goal

    InitializeSession \--\> ReadContext: Assemble Messages Array

    state "Harness Execution Loop (while iteration \< max\_iterations)" as LoopState {

        ReadContext \--\> CallLLM: Inference Request

        CallLLM \--\> EvaluateOutput: Inspect Completion

        

        EvaluateOutput \--\> FinalAnswer: No Tool Calls (Text Response)

        EvaluateOutput \--\> ExecuteTool: Tool Calls Present

        

        ExecuteTool \--\> AppendObservation: Capture Output/Errors

        AppendObservation \--\> IncrementTurn: Increment Iteration Counter

        IncrementTurn \--\> ReadContext

    }

    FinalAnswer \--\> \[\*\]: Task Complete

    IncrementTurn \--\> MaxLimitExceeded: Iteration \== Max

    MaxLimitExceeded \--\> \[\*\]: Exception Raised

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_3\_execution\_loop.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_3_execution_loop.html)

---

# SECTION 4: Component 2 — Context Management & Compaction — \[06:45–09:00\]

### 1\. Content Analysis

Context management is the first of two critical components in a harness that will **quietly wreck your agent if implemented improperly** `[06:45–07:15]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Understand Context Window Exhaustion:**  
   - Recognize that while LLM context windows have grown (from 200k tokens up to 1M+ tokens in Opus 4.6), the transcript grows monotonically on every single turn `[07:15–07:45]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Formulate a strict **Keep, Summarize, Discard** policy when usage hits a safety ceiling (typically 75%–80% of maximum context budget):

\# \[ref: What is an agent harness? The nine components of a great one\]

def compact\_context(messages: list, token\_threshold: int \= 160000\) \-\> list:

    current\_tokens \= count\_tokens(messages)

    if current\_tokens \< token\_threshold:

        return messages  \# Budget OK    

    print("⚠️ Token threshold reached. Triggering compaction...")

    \# 1\. KEEP: System prompt & initial user goal (Static prefix)

    system\_and\_goal \= messages\[:2\]

    \# 2\. KEEP: Most recent N turns (Verbatim working memory)

    recent\_messages \= messages\[-6:\]

    \# 3\. SUMMARIZE: Middle history (Boil down to key actions & state)

    middle\_history \= messages\[2:-6\]

    summary\_text \= llm\_summarizer.summarize\_middle(middle\_history)


    compacted\_summary \= {

        "role": "system", 

        "content": f"\[COMPACTION SUMMARY\]: {summary\_text}"

    }


    \# Reassemble non-contiguous history safely preserving prefix cache order

    return system\_and\_goal \+ \[compacted\_summary\] \+ recent\_messages

2. **Beware the Silent Compaction Trap:**  
     
   - Avoid aggressive or unstructured summarization that strips crucial details (e.g., file paths, secret tokens, exact line numbers, or test failure traces) `[07:45–08:30]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - When a summary drops a key variable or architectural assumption, the agent does not throw an exception; it proceeds **confidently working from a broken memory**, causing hallucinated tool parameters and cascade failures.

   

3. **Align with Cache Prefixes:** Keep static elements (System Prompt, AGENTS.md instructions) at the very top of the prompt to maximize KV-cache reuse, placing dynamic compaction summaries immediately before recent turns `[08:30–09:00]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **Compaction:** The automatic pruning and summarization of conversation history when token consumption crosses a defined threshold `[07:15]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Keep, Summarize, Discard:** The canonical triage strategy: Keep system/goal \+ recent turns, Summarize middle history, Discard raw verbose outputs `[07:35]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Broken Memory Cascade:** The failure mode where bad compaction causes silent, unrecoverable agent hallucinations `[08:15]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph RAW\_HISTORY \["RAW HISTORY (Growing past Token Limit)"\]

        SYS\["1. System Prompt & Goal (Keep Static)"\]

        MID1\["2. Early Tool Executions & File Reads"\]

        MID2\["3. Middle Discussion & Stack Traces"\]

        REC\["4. Recent 6 Turns (Keep Verbatim)"\]

        SYS \--- MID1 \--- MID2 \--- REC

    end

    subgraph COMPACTION\_TRIGGER \["Compaction Engine (Threshold: 80% Window)"\]

        TRIGGER{"Token Count \> Threshold?"}

        SUMMARIZER\["LLM Summarize Middle Blocks"\]

    end

    subgraph COMPACTED\_HISTORY \["COMPACTED HISTORY (Budget Restored)"\]

        C\_SYS\["1. System Prompt & Goal (Cached Prefix)"\]

        C\_SUMM\["2. \[SUMMARY BLOCK\]: Distilled State & Key Variables"\]

        C\_REC\["3. Recent 6 Turns (Verbatim Working Memory)"\] 

        C\_SYS \--- C\_SUMM \--- C\_REC

    end

    RAW\_HISTORY \--\> TRIGGER

    TRIGGER \-- Yes \--\> SUMMARIZER

    SUMMARIZER \--\> COMPACTED\_HISTORY

    TRIGGER \-- No \--\> RAW\_HISTORY

    style RAW\_HISTORY fill:\#1e293b,stroke:\#f59e0b,stroke-width:2px,color:\#fff

    style COMPACTED\_HISTORY fill:\#0f172a,stroke:\#10b981,stroke-width:2px,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_4\_context\_compaction.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_4_context_compaction.html)

---

# SECTION 5: Component 3 & 5 — Tools, Skills, and Built-in Primitives — \[09:00–11:30\]

### 1\. Content Analysis

For the execution loop to interact with the external world, it requires a structured **Tool & Skill Architecture** `[09:00–09:30]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Distinguish Primitives (Tools) from Encoded Knowledge (Skills):**  
     
   - **Tools (Primitives):** Universal, stateless operations implemented in execution code `[09:30–10:15]`. `[ref: What is an agent harness? The nine components of a great one]`  
     - Examples: `view_file`, `write_to_file`, `run_command` (bash), `grep_search`.  
     - *Design Constraint:* Implement built-in primitives using **Python standard libraries only** (`os`, `subprocess`, `pathlib`, `json`). Avoid third-party framework dependencies to preserve harness portability `[10:15–10:45]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - **Skills (Encoded Knowledge):** Higher-level procedural domain knowledge stored as instruction files (e.g., `SKILL.md` or team playbooks).  
     - Skills explain *how* to use primitive tools in combination to accomplish complex tasks (e.g., executing a multi-step Git rebase or running a test-suite audit).

   

2. **Implement the Central Tool Registry Pattern:**  
     
   - Bind all tools inside a central registry that handles schema generation, permission mapping, and dynamic execution dispatch:

\# \[ref: What is an agent harness? The nine components of a great one\]

class ToolRegistry:

    def \_\_init\_\_(self):

        self.\_registry \= {}

    def register(self, name: str, permission\_level: str, handler: callable, description: str):

        self.\_registry\[name\] \= {

            "name": name,

            "permission": permission\_level,  \# "read-only", "workspace", "full"

            "handler": handler,

            "description": description

        }

    def dispatch(self, tool\_name: str, kwargs: dict, current\_permission: str):

        tool \= self.\_registry.get(tool\_name)

        if not tool:

            raise KeyError(f"Unknown tool: {tool\_name}")

        \# Enforce static permission boundary

        if not self.\_check\_permission(tool\["permission"\], current\_permission):

            raise PermissionError(f"Tool {tool\_name} requires {tool\['permission'\]} access.")

        return tool\["handler"\](\*\*kwargs)

\# Baseline Built-in Primitive (Standard Library Only)

def view\_file(filepath: str) \-\> str:

    with open(filepath, 'r', encoding='utf-8') as f:

        return f.read()

3. **Incorporate Modern Built-in Workflows:** Equip the harness with out-of-the-box higher-level primitives: git commits, pull request creation, automated test execution, and code navigation `[10:45–11:30]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **Tools (Primitives):** Universal, atomic execution functions (read, write, bash) built using standard libraries `[09:35]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Skills (Knowledge):** Markdown-encoded team procedures explaining multi-step tool usage patterns `[10:05]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Tool Registry:** The central binding catalog managing schemas, permissions, and tool dispatch `[10:30]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph INVOCATION \["LLM Inference Output"\]

        TC\["Tool Call Request: { name: 'run\_command', args: { command: 'pytest' } }"\]

    end

    subgraph REGISTRY \["Harness Tool Registry"\]

        LOOKUP\["Lookup Tool Name & Metadata"\]

        PERM\_CHECK{"Check Permission Tiers"}

        LOOKUP \--\> PERM\_CHECK

    end

    subgraph EXECUTORS \["Standard Library Handlers"\]

        SYS\_IO\["Built-in File I/O (builtins.open)"\]

        SYS\_BASH\["Built-in Shell (subprocess.run)"\]

        SKILL\_DOC\["Skill Instruction Injector (SKILL.md)"\]

    end

    TC \--\> LOOKUP

    PERM\_CHECK \-- Allowed \--\> SYS\_BASH

    PERM\_CHECK \-- Denied \--\> ERR\["Permission Denied Exception"\]

    style REGISTRY fill:\#1e1b4b,stroke:\#6366f1,stroke-width:2px,color:\#fff

    style EXECUTORS fill:\#0f172a,stroke:\#10b981,stroke-width:2px,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_5\_tools\_and\_skills.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_5_tools_and_skills.html)

---

# SECTION 6: Component 4 — Sub-Agent Management & Delegation — \[11:30–13:45\]

### 1\. Content Analysis

Some engineering tasks are too broad, exploratory, or computationally expensive to process inside a single linear conversation thread `[11:30–12:00]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Recognize the Sub-Agent Motivation:**  
   - Attempting to perform large-scale repository searches, multi-file code exploration, or parallel test verification in the primary context window rapidly triggers context compaction and degrades model reasoning `[12:00–12:30]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Delegate sub-tasks using the canonical sub-agent lifecycle: $$\\text{Spawn Sub-Agent} \\longrightarrow \\text{Restrict Tools & Scope} \\longrightarrow \\text{Collect Condensed Output}$$

\# \[ref: What is an agent harness? The nine components of a great one\]

class SubAgentManager:

    def \_\_init\_\_(self, parent\_harness):

        self.parent \= parent\_harness

    def spawn\_subagent(self, role: str, sub\_prompt: str, restricted\_tools: list) \-\> str:

        print(f"🚀 \[SPAWN\]: Launching child sub-agent for role: {role}")

        \# 1\. ISOLATED SESSION: Fresh context window

        child\_context \= \[

            {"role": "system", "content": f"You are a specialized sub-agent ({role}). {sub\_prompt}"}

        \]    

        \# 2\. RESTRICT: Filter tool registry to allowed subset (e.g. read-only)

        scoped\_registry \= self.parent.tool\_registry.filter\_by\_list(restricted\_tools)

        \# 3\. RUN CHILD LOOP

        child\_result \= run\_isolated\_loop(child\_context, scoped\_registry, max\_iterations=10)
    

        \# 4\. COLLECT: Return condensed summary to parent context

        print(f"✅ \[COLLECT\]: Sub-agent {role} finished.")

        return f"\[SUB-AGENT RESULT \- {role}\]: {child\_result.summary}"

2. **Understand Compute Allocation Dynamics:**  
     
   - Note the empirical finding from harness engineering research: **\~90% of total compute tokens in production agents flow through delegated child agents**, rather than the parent coordinator `[12:30–13:15]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
   - Treat the parent agent primarily as an **orchestration, decomposition, and verification layer** rather than a heavy execution engine.

   

3. **Enforce Archetype Isolation:** Define distinct sub-agent archetypes (e.g., *Exploration Sub-Agent*, *Code Generation Sub-Agent*, *Verification Sub-Agent*), each restricted to the exact tools needed for its role `[13:15–13:45]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **Spawn, Restrict, Collect:** The canonical 3-stage lifecycle for managing isolated sub-agent sessions `[12:15]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **90% Compute Rule:** \~90% of all token compute flows through child sub-agents, leaving the parent harness clean for orchestration `[12:45]` `[ref: Harness engineering: why agent performance now lives outside the model]`.  
- **Context Protection:** Sub-agents shield the main context window from exploratory bloat and compaction crashes `[13:30]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

sequenceDiagram

    autonumber

    actor Parent as Parent Harness (Coordinator)

    participant SubManager as Sub-Agent Manager

    participant Child1 as Exploration Sub-Agent (Read-Only)

    participant Child2 as Verification Sub-Agent (Test Runner)

    Parent-\>\>SubManager: 1\. Spawn Sub-Agent (Role: Code Explorer)

    SubManager-\>\>Child1: 2\. Create Isolated Session & Restrict Tools (view\_file, grep)

    activate Child1

    Child1-\>\>Child1: Run 8 Search Turns in Fresh Context

    Child1--\>\>SubManager: 3\. Return Condensed Findings Summary

    deactivate Child1

    SubManager--\>\>Parent: 4\. Inject Summary into Parent Context (Save \~80k tokens)

    Parent-\>\>SubManager: 5\. Spawn Sub-Agent (Role: Test Verifier)

    SubManager-\>\>Child2: 6\. Create Isolated Session & Restrict Tools (pytest)

    activate Child2

    Child2-\>\>Child2: Run Test Suite Execution

    Child2--\>\>SubManager: 7\. Return Pass/Fail Report

    deactivate Child2

    SubManager--\>\>Parent: 8\. Inject Verification Result into Parent Context

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_6\_subagent\_delegation.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_6_subagent_delegation.html)

---

# SECTION 7: Component 6 & 7 — Session Persistence & Prompt Assembly — \[13:45–16:00\]

### 1\. Content Analysis

Long agent execution sessions are highly stateful environments `[13:45–14:15]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Implement Crash-Safe Session Persistence (Component 6):**  
   - Eliminate in-memory state fragility. If an agent process crashes after 45 minutes of execution, losing session history is unacceptable `[14:15–14:45]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Write state using an **append-only JSONL stream**: flush a single JSON object to disk immediately upon every turn event (user prompt, model tool call, tool observation, compaction event).

\# \[ref: What is an agent harness? The nine components of a great one\]

import json

import time

class SessionLogger:

    def \_\_init\_\_(self, log\_path: str):

        self.log\_file \= open(log\_path, 'a', encoding='utf-8')

        

    def log\_event(self, event\_type: str, payload: dict):

        event \= {

            "timestamp": time.time(),

            "type": event\_type,  \# "USER\_INPUT", "MODEL\_CALL", "TOOL\_RESULT", "COMPACTION"

            "payload": payload

        }

        \# Immediately write and flush to disk for crash safety

        self.log\_file.write(json.dumps(event) \+ "\\n")

        self.log\_file.flush()

        

    def replay\_session(self) \-\> list:

        \# Reconstitute exact working memory from disk after crash

        messages \= \[\]

        with open(self.log\_file.name, 'r', encoding='utf-8') as f:

            for line in f:

                event \= json.loads(line)

                messages.append(event\["payload"\])

        return messages

2. **Assemble System Prompts & Enforce Prefix Caching (Component 7):**  
   - Recognize that system prompts are not hardcoded static strings `[14:45–15:30]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Implement dynamic prompt discovery: walk workspace ancestor directories to locate instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`) `[15:30–16:00]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - **Enforce the Prefix Caching Golden Rule:** Place all **static content first** (base system instructions, tool definitions) and **dynamic content second** (injected project instructions, user prompt, turn history). Reversing this order breaks KV-cache prefixes, multiplying token billing on every request\!

---

### 2\. Key Concepts

- **Append-Only JSONL Stream:** Crash-safe, disk-persisted event log enabling instant session replay after process termination `[14:25]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **System Prompt Assembly:** Dynamic directory traversal discovering `AGENTS.md` and `CLAUDE.md` `[15:00]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Prefix Caching Order:** Static system rules first, dynamic project instructions second to preserve KV-cache hits `[15:45]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph EVENT\_STREAM \["Session Persistence (JSONL Log File)"\]

        E1\["Event 1: USER\_INPUT ('Fix bug \#402')"\] \--\> E2\["Event 2: MODEL\_CALL ('view\_file')"\]

        E2 \--\> E3\["Event 3: TOOL\_RESULT ('def foo():...')"\]

        E3 \--\> E4\["Event 4: COMPACTION\_EVENT (Summary)"\]


        E4 \-.-\>|Flush to Disk| DISK\[("session\_transcript.jsonl")\]

    end

    subgraph PROMPT\_PIPELINE \["System Prompt Assembly (KV-Cache Preserving)"\]

        direction TB

        P\_STATIC\["1. Base Harness Instructions & Tool Schemas (STATIC FIRST)"\]

        P\_DYNAMIC\["2. Injected AGENTS.md / CLAUDE.md (DYNAMIC SECOND)"\]

        P\_HISTORY\["3. Replayed / Compacted History (WORKING MEMORY)"\]

        P\_STATIC \--\> P\_DYNAMIC \--\> P\_HISTORY

    end

    style DISK fill:\#0f172a,stroke:\#10b981,stroke-width:2px,color:\#fff

    style PROMPT\_PIPELINE fill:\#1e1b4b,stroke:\#6366f1,stroke-width:2px,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_7\_persistence\_and\_prompts.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_7_persistence_and_prompts.html)

---

# SECTION 8: Component 8 & 9 — Lifecycle Hooks, Permissions, and Safety — \[16:00–18:15\]

### 1\. Content Analysis

Because execution loops run real bash commands and file mutations on local Developer workstations or production sandboxes, security and governance cannot be an afterthought `[16:00–16:30]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Implement Lifecycle Hooks (Component 8):**  
   - Provide pre-tool and post-tool interception points around tool dispatch `[16:30–17:15]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - **Pre-Tool Hook:** Intercepts proposed calls before execution. Returns `ALLOW`, `DENY` (with error message), or `MODIFY` (sanitizing flags or paths).  
   - **Post-Tool Hook:** Receives execution outputs after completion for audit logging, telemetry, or compliance verification.

\# \[ref: What is an agent harness? The nine components of a great one\]

class SecurityHarness:

    def \_\_init\_\_(self, permission\_mode: str \= "workspace"):

        self.mode \= permission\_mode  \# "read-only", "workspace", "full"

        self.pre\_hooks \= \[\]

        self.post\_hooks \= \[\]

    def register\_pre\_hook(self, hook\_fn: callable):

        self.pre\_hooks.append(hook\_fn)

    def dispatch\_with\_safety(self, tool\_name: str, tool\_args: dict):

        \# 1\. RUN PRE-TOOL HOOKS

        for hook in self.pre\_hooks:

            decision, modified\_args \= hook(tool\_name, tool\_args)

            if decision \== "DENY":

                raise PermissionError(f"Pre-tool hook DENIED execution of {tool\_name}")

            if decision \== "MODIFY":

                tool\_args \= modified\_args

                

        \# 2\. DYNAMIC BASH PARSING (Component 9\)

        if tool\_name \== "run\_bash":

            command \= tool\_args.get("command", "")

            required\_tier \= self.\_classify\_bash\_command(command)

            

            if not self.\_check\_tier\_allowed(required\_tier):

                user\_approved \= self.\_interactive\_prompt(command, required\_tier)

                if not user\_approved:

                    return "User denied execution of command."

                    

        \# 3\. EXECUTE & RUN POST-TOOL HOOKS

        result \= execute\_native\_tool(tool\_name, tool\_args)

        for post\_hook in self.post\_hooks:

            post\_hook(tool\_name, tool\_args, result)

            

        return result

    def \_classify\_bash\_command(self, cmd: str) \-\> str:

        read\_only\_cmds \= \["ls", "cat", "grep", "head", "find", "git status"\]

        if any(cmd.strip().startswith(c) for c in read\_only\_cmds) and "\>" not in cmd and "rm" not in cmd:

            return "read-only"

        return "full"

2. **Enforce Dynamic Permission Tiers (Component 9):**  
     
   - Establish three canonical permission tiers: **Read-Only** $\\rightarrow$ **Workspace-Only** $\\rightarrow$ **Full Access** `[17:15–17:45]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Perform **Dynamic Command Classification:** Do not rely on static tool names. Parse shell command strings dynamically at runtime.

   

3. **Interactive Confirmation Gating:** Pause execution and prompt human operators before running any action classified as destructive or outside active workspace bounds `[17:45–18:15]`. `[ref: What is an agent harness? The nine components of a great one]`

---

### 2\. Key Concepts

- **Lifecycle Hooks:** Pre-tool (allow/deny/modify) and post-tool (audit) extension points wrapping tool execution `[16:40]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Dynamic Bash Classification:** Parsing command line strings dynamically at runtime to assign permission tiers `[17:25]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Interactive Approval Gating:** Halting the execution loop to request human confirmation for high-risk actions `[17:55]` `[ref: What is an agent harness? The nine components of a great one]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

flowchart TD

    START\["Tool Call Proposed: run\_bash('rm \-rf ./dist')"\] \--\> PRE\_HOOK{"Run Pre-Tool Hooks"}

    PRE\_HOOK \-- Deny \--\> ABORT\["Abort Execution & Return Exception"\]

    PRE\_HOOK \-- Allow / Modify \--\> PARSER\["Dynamic Command Parser"\]

    PARSER \--\> CLASSIFY{"Command Tier?"}

    CLASSIFY \-- "Read-Only (e.g. ls)" \--\> EXECUTE\["Execute Subprocess"\]

    CLASSIFY \-- "Full/Destructive (e.g. rm \-rf)" \--\> TIER\_CHECK{"Active Permission Tier?"}

    TIER\_CHECK \-- Full Access Granted \--\> EXECUTE

    TIER\_CHECK \-- Workspace Mode \--\> PROMPT{"Interactive User Approval Prompt"}

    PROMPT \-- User Approves \--\> EXECUTE

    PROMPT \-- User Denies \--\> REJECT\["Return 'Execution Denied by User' to Model"\]

    EXECUTE \--\> POST\_HOOK\["Run Post-Tool Audit Hooks"\]

    POST\_HOOK \--\> END\["Return Result to Context"\]

    style PRE\_HOOK fill:\#312e81,stroke:\#6366f1,color:\#fff

    style PARSER fill:\#064e3b,stroke:\#34d399,color:\#fff

    style PROMPT fill:\#831843,stroke:\#f472b6,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_8\_hooks\_and\_permissions.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_8_hooks_and_permissions.html)

---

# SECTION 9: Modern Research & Harness Ablation Insights — \[18:15–20:00\]

### 1\. Content Analysis

In March 2026, empirical research transformed agent harness design from an ad-hoc craft into an exact science `[18:15–18:30]`. `[ref: Harness engineering: why agent performance now lives outside the model]`

1. **Analyze Tsinghua University's NLAH Paper:**  
     
   - Review the Natural-Language Agent Harness (NLAH) experiment: researchers converted the OS-Symphony native code harness into a structured natural-language harness representation `[18:30–19:00]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
   - **Performance Results:** Benchmark resolve rate jumped from **30.4% to 47.2% (+16.8 points)** with identical LLM weights. Runtime collapsed from 361 minutes down to 141 minutes, and LLM calls dropped from 1,200 to 34 calls.

   

2. **Deconstruct Module Ablation Results (The Lesson of Subtraction):**  
     
   - Examine the counter-intuitive module ablations measured across SWE-bench Verified and OSWorld `[19:00–19:30]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
     - **Self-Evolution (+4.8 SWE-bench / \+2.7 OSWorld):** The **only** module that consistently improved performance. It operates by maintaining an acceptance-gated attempt loop that keeps context narrow until explicit failure signals justify broadening.  
     - **Verifiers (-0.8 SWE-bench / \-8.4 OSWorld):** Contrary to instinct, added verification gates degraded overall success by creating brittle validation traps.  
     - **Multi-Candidate Search (-2.4 SWE-bench / \-5.6 OSWorld):** Multi-branch tree search bloated context RAM without buying accuracy.  
   - *Core Takeaway:* Most added structure hurts. **Narrowing the agent's attempt loop beats broadening search.**

   

3. **Examine Stanford's Meta-Harness:**  
     
   - Analyze Meta-Harness (Lee, Khattab et al.), which treats the harness as an automated optimization target using raw execution traces `[19:30–20:00]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
   - **Key Finding:** On Terminal-Bench 2, Meta-Harness achieved **76.4% (Rank \#1)** using a smaller model (Claude Haiku) outranking larger hand-engineered models. Harness optimizations transferred successfully across 5 distinct model families.

---

### 2\. Key Concepts

- **Natural-Language Agent Harness (NLAH):** Representing control logic in structured natural language to enable controlled ablations (+16.8 point benchmark jump) `[18:40]` `[ref: Harness engineering: why agent performance now lives outside the model]`.  
- **The Subtraction Dynamic:** Most added harness components degrade performance; removing expired assumptions yields immediate gains `[19:15]` `[ref: Harness engineering: why agent performance now lives outside the model]`.  
- **Meta-Harness Optimization:** Automated harness optimization using raw execution traces allows smaller models to outrank larger models `[19:45]` `[ref: Harness engineering: why agent performance now lives outside the model]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph ABLATION\_STUDY \["Tsinghua NLAH Module Ablation Results"\]

        direction TB

        SELF\_EVO\["Self-Evolution Attempt Loop\\n(+4.8 SWE-bench / \+2.7 OSWorld)\\n✅ CONSISTENTLY HELPS"\]

        VERIFIERS\["Evaluation Verifiers\\n(-0.8 SWE-bench / \-8.4 OSWorld)\\n❌ HURTS PERFORMANCE"\]

        SEARCH\["Multi-Candidate Search\\n(-2.4 SWE-bench / \-5.6 OSWorld)\\n❌ HURTS PERFORMANCE"\]

    end

    subgraph CORE\_RULE \["Harness Design Principle"\]

        RULE\["Narrowing Attempt Loop \> Broadening Search Space"\]

    end

    SELF\_EVO \--\> CORE\_RULE

    VERIFIERS \--\> CORE\_RULE

    SEARCH \--\> CORE\_RULE

    style ABLATION\_STUDY fill:\#0f172a,stroke:\#3b82f6,stroke-width:2px,color:\#fff

    style SELF\_EVO fill:\#064e3b,stroke:\#34d399,color:\#fff

    style VERIFIERS fill:\#7f1d1d,stroke:\#f87171,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_9\_ablation\_research.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_9_ablation_research.html)

---

# SECTION 10: Building a Minimal Python Harness & Synthesis — \[20:00–21:00\]

### 1\. Content Analysis

To truly master agent harness engineering, **build a minimal harness yourself** `[20:00–20:20]`. `[ref: What is an agent harness? The nine components of a great one]`

1. **Assemble the 9-Component Minimal Python Architecture:**  
     
   - Combine all nine structural components into a single, zero-dependency Python module using only the standard library (`os`, `sys`, `json`, `subprocess`, `time`, `pathlib`) `[20:20–20:45]`. `[ref: What is an agent harness? The nine components of a great one]`  
   - Reference Implementation saved to repository root: [minimal\_harness.py](file:///Users/gregorykennedy/Desktop/harness-engineering/minimal_harness.py).

   

2. **Final Synthesizing Directives:**  
     
   - Recognize that the harness is the primary site of architectural differentiation in modern AI software `[20:45–21:00]`. `[ref: Harness engineering: why agent performance now lives outside the model]`  
   - Rather than waiting for model upgrades, invest directly in your harness scaffolding: optimize your context compaction rules, strictly isolate child sub-agents, enforce append-only persistence, and prune unnecessary verifier complexity on schedule.

---

### 2\. Key Concepts

- **Zero-Dependency Architecture:** Building core harness primitives using standard libraries only to guarantee total framework independence `[20:15]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **The Complete 9-Component Engine:** Integrating Loop, Context Manager, Tool Registry, Sub-Agents, Built-ins, Persistence, Prompt Assembly, Hooks, and Safety into a single coherent system `[20:35]` `[ref: What is an agent harness? The nine components of a great one]`.  
- **Harness Engineering Discipline:** Moving performance optimization from weight prompt tweaks to systematic operating system engineering `[20:50]` `[ref: Harness engineering: why agent performance now lives outside the model]`.

---

### 3\. Visual Documentation Assets

#### Asset A: Logic Diagram (Mermaid)

graph TD

    subgraph MINIMAL\_HARNESS \["MINIMAL PYTHON AGENT HARNESS (9 COMPONENTS)"\]

        direction TB

        C7\["1. System Prompt Assembly (Static First \+ AGENTS.md)"\] \--\> C1\["2. The Execution Loop (while iteration \< max)"\]

        C1 \--\> C2\["3. Context Management (Compacting \> 150k Tokens)"\]

        C1 \--\> C8\["4. Pre-Tool Hooks (Allow / Deny / Modify)"\]

        C8 \--\> C9\["5. Permissions & Safety (Read-Only / Workspace / Full)"\]

        C9 \--\> C3\["6. Tool Registry Dispatch"\]

        C3 \--\> C5\["7. Built-in Primitives (view\_file, write\_file, run\_bash)"\]

        C3 \--\> C4\["8. Sub-Agent Management (Spawn, Restrict, Collect)"\]

        C1 \--\> C6\["9. Session Persistence (Append-only JSONL Stream)"\]

    end

    style MINIMAL\_HARNESS fill:\#0f172a,stroke:\#10b981,stroke-width:2px,color:\#fff

    style C1 fill:\#047857,stroke:\#34d399,color:\#fff

    style C3 fill:\#1e1b4b,stroke:\#818cf8,color:\#fff

    style C6 fill:\#831843,stroke:\#f472b6,color:\#fff

#### Asset B: Animated HTML Slide Reference

- Saved to: [slides/section\_10\_minimal\_harness\_synthesis.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_10_minimal_harness_synthesis.html)

---

## COURSE SUMMARY & REPOSITORY ASSETS

All assets generated for this course have been saved directly to this repository:

1. **Course Documentation:** `agent_harness_technical_course.md`  
2. **Minimal Python Reference Implementation:** `minimal_harness.py`  
3. **Interactive Animated HTML Slides (10 Files):**  
   - [slides/section\_1\_os\_analogy.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_1_os_analogy.html)  
   - [slides/section\_2\_framework\_vs\_harness.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_2_framework_vs_harness.html)  
   - [slides/section\_3\_execution\_loop.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_3_execution_loop.html)  
   - [slides/section\_4\_context\_compaction.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_4_context_compaction.html)  
   - [slides/section\_5\_tools\_and\_skills.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_5_tools_and_skills.html)  
   - [slides/section\_6\_subagent\_delegation.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_6_subagent_delegation.html)  
   - [slides/section\_7\_persistence\_and\_prompts.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_7_persistence_and_prompts.html)  
   - [slides/section\_8\_hooks\_and\_permissions.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_8_hooks_and_permissions.html)  
   - [slides/section\_9\_ablation\_research.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_9_ablation_research.html)  
   - [slides/section\_10\_minimal\_harness\_synthesis.html](file:///Users/gregorykennedy/Desktop/harness-engineering/slides/section_10_minimal_harness_synthesis.html)

