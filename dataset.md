# DATASET — UI State Capture Dataset for Agent B

This dataset contains UI state transitions captured automatically by **Agent B**, a browser automation system that executes natural-language tasks (e.g., “Create a project in Linear”) and records screenshots + metadata after each step.

---

# 📁 Dataset Structure

```
data/
  linear_create_project/
  linear_create_issue/
  linear_filter_issues/
  notion_filter_database/
  notion_create_page/
```

Each folder includes:

- **state_###.png** — screenshot captured after each intent (step)
- **metadata.json** — metadata describing each state

---

# 📄 metadata.json Format

Each entry contains:

- **index** – Step number  
- **intent_type** – e.g., open_app, click, fill, wait_modal  
- **intent_label** – The label/description associated with the intent  
- **url** – Current URL in the browser  
- **title** – Page title  
- **screenshot** – Screenshot filename  
- **state_kind** – `"page"`, `"modal"`, `"form"`

Example:

```json
{
  "index": 3,
  "intent_type": "click",
  "intent_label": "New project",
  "url": "https://linear.app/...",
  "title": "Linear",
  "screenshot": "state_003.png",
  "state_kind": "modal"
}
```

---

# 📌 Included Tasks

This dataset captures 5 workflows across Linear and Notion.

## 1. Create a Project in Linear  
**Task Command:**
```
python agent_b.py --task "Create a project in Linear" --out data/linear_create_project
```

**Captured States Include:**
- Workspace load
- Sidebar navigation
- Attempted new-project modal
- Form state and non-URL UI transitions

---

## 2. Create an Issue in Linear  
**Command:**
```
python agent_b.py --task "Create an issue in Linear" --out data/linear_create_issue
```

**Captured States:**
- Workspace page
- Issue creation attempt
- Form attempt (title, description)
- Modal/form classifications

---

## 3. Filter Issues in Linear  
**Command:**
```
python agent_b.py --task "Filter issues in Linear" --out data/linear_filter_issues
```

**Captured States:**
- Issues view
- Attempted filter panel
- Overlay/modal-like UI

---

## 4. Filter a Database in Notion  
**Command:**
```
python agent_b.py --task "Filter a database in Notion" --out data/notion_filter_database
```

**Captured States:**
- Notion home
- Database view
- Attempted filter overlay (non-URL state)

---

## 5. Create a Page in Notion  
**Command:**
```
python agent_b.py --task "Create a page in Notion" --out data/notion_create_page
```

**Captured States:**
- Sidebar
- Template picker
- Page creation UI

---

# 🎯 Purpose of the Dataset

This dataset demonstrates how Agent B:

- Parses natural-language tasks  
- Executes browser actions live  
- Captures **non-URL UI state transitions** such as modals, forms, overlays  
- Produces a replayable sequence of visual steps with strict metadata  

It can be used for:

- Training UI navigation agents  
- Evaluating multi-step workflows  
- UI regression datasets  
- Agent-based reasoning research  

---

# 🙌 End of DATASET.md
