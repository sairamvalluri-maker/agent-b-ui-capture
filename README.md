# README

# 🧭 Agent B — UI State Capture System  
A generalizable browser-automation agent that executes natural-language tasks inside real web applications, navigating live UIs and capturing **every UI state** (including non-URL states like modals, forms, and overlays).

This project implements **Agent B** from the take-home assignment. Agent B receives high-level tasks such as:

- “Create a project in Linear”  
- “Filter issues in Linear”  
- “Filter a database in Notion”  

It parses these tasks into structured “intents”, executes them using Playwright in a real browser, and captures a screenshot + metadata after each step.

---

# ✨ Features

### ✔ Natural-language → intents  
A pattern-based parser extracts:  
- **App** (Linear, Notion)  
- **Action** (create, filter, open)  
- **Object** (project, issue, database, page)  

This allows the agent to generalize to unseen phrasing.

---

### ✔ Real browser automation (Playwright)  
Agent B uses a **persistent browser profile**, allowing it to stay logged into apps such as Linear and Notion without re-logging every run.

---

### ✔ UI State Capture (including non-URL states)  
For **every intent**, Agent B captures:

- A screenshot (`state_###.png`)  
- Metadata including:
  - intent type / label
  - URL
  - page title
  - inferred **state_kind**:
    - `"page"`  
    - `"modal"`  
    - `"form"`  

This enables recognizing UI states that **do not change the URL**, such as:

- Create-project modal  
- Filter panel  
- Form fields  
- Template selector  

---

### ✔ Multi-app support  
Agent B currently supports:

- **Linear**
- **Notion**

…and the architecture allows adding more apps quickly.

---

# 📦 Project Structure

```
agent_b_submission/
│
├── agent_b.py               
├── intent_parser.py         
├── executor.py              
├── metadata.py              
├── DATASET.md               
│
├── login_linear.py          
│
└── data/
    ├── linear_create_project/
    ├── linear_create_issue/
    ├── linear_filter_issues/
    ├── notion_filter_database/
    └── notion_create_page/
```

---

# 🚀 How to Run

## 1. Create Python venv and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate

pip install playwright
playwright install
```

---

## 2. One-time login (Linear)

```bash
python login_linear.py
```

A browser window will open.

Log in fully → press ENTER in terminal → session saved.

---

## 3. Run any task

### Example: Create project in Linear

```bash
python agent_b.py --task "Create a project in Linear" --out data/linear_create_project
```

### Example: Create issue in Linear

```bash
python agent_b.py --task "Create an issue in Linear" --out data/linear_create_issue
```

### Example: Filter database in Notion

```bash
python agent_b.py --task "Filter a database in Notion" --out data/notion_filter_database
```

---

# 📂 Output Format

Each run creates:

```
data/<task_name>/
  state_001.png
  state_002.png
  ...
  metadata.json
```

---

# 📘 Dataset

This project includes **5 workflows** across **Linear** and **Notion**:
- Create a project in Linear  
- Create an issue in Linear  
- Filter issues in Linear  
- Filter a database in Notion  
- Create a page in Notion  

Full dataset documentation is available in:  
📄 **DATASET.md**

---

# 🧪 Architecture Overview

```
TASK ("Create a project in Linear")
        ↓
Intent Parser
        ↓
[ {type: "open_app"}, {type: "click"}, {type: "wait_modal"}, ... ]
        ↓
Executor (Playwright)
        ↓
UI Interactions on Live App
        ↓
After each intent:
    - Screenshot
    - Metadata (state_kind, element info, url)
```

---

# 🙌 Final Notes

This system shows how an autonomous agent can parse natural language, navigate real web UIs, and capture structured state transitions for downstream multi-agent workflows.

