"""
intent_parser.py
-----------------

This module defines a simple parser that converts natural‑language task
descriptions into sequences of intent dictionaries.  Each intent
dictionary has a `type` key and may include additional parameters
depending on the intent.  The parser recognises a handful of example
phrases and falls back to a generic `perform_task` intent when it
cannot match a known pattern.

The intent types used here are illustrative and can be extended as
needed:

* ``open_app``: Navigate to a specific application URL.
* ``click``: Click a button or element identified by text.
* ``fill``: Enter text into an input field with an associated label.
* ``wait_modal``: Wait for a modal dialog to appear.
* ``perform_task``: A catch‑all for tasks that lack specific patterns.
"""

import re
from dataclasses import dataclass
from typing import List, Dict 

def extract_app(task: str) -> str:
    task = task.lower()
    if "linear" in task:
        return "linear"
    if "notion" in task:
        return "notion"
    return None


def extract_action(task: str) -> str:
    task = task.lower()

    # creation-type actions
    if re.search(r"\b(create|make|add|new)\b", task):
        return "create"

    # filtering
    if "filter" in task or "apply filter" in task:
        return "filter"

    # updating
    if "update" in task or "change" in task:
        return "update"

    # opening
    if "open" in task:
        return "open"

    return None


def extract_object(task: str) -> str:
    task = task.lower()

    # Linear objects
    if "project" in task:
        return "project"
    if "issue" in task:
        return "issue"

    # Notion objects
    if "database" in task:
        return "database"
    if "page" in task:
        return "page"

    return None

def parse_task(task: str) -> List[Dict[str, str]]:
    task_lower = task.lower()

    app = extract_app(task_lower)
    action = extract_action(task_lower)
    obj = extract_object(task_lower)

    if app == "linear" and action == "create" and obj == "project":
        return [
            {"type": "open_app", "url": "https://linear.app/test916/team/TES/active"},
            {"type": "click", "label": "Projects"},
            {"type": "click", "label": "New project"},
            {"type": "wait_modal", "text": "Create project"},
            {"type": "fill", "label": "Name", "text": "Sample Project"},
            {"type": "fill", "label": "Description", "text": "Created by Agent B"},
            {"type": "click", "label": "Create"},
        ]

    if app == "linear" and action == "create" and obj == "issue":
        return [
            {"type": "open_app", "url": "https://linear.app/test916/team/TES/active"},
            {"type": "click", "label": "New issue"},
            {"type": "wait_modal", "text": "Create issue"},
            {"type": "fill", "label": "Title", "text": "Example Issue"},
            {"type": "fill", "label": "Description", "text": "Created by Agent B"},
            {"type": "click", "label": "Create"},
        ]

    if app == "linear" and action == "filter" and obj == "issue":
        return [
            {"type": "open_app", "url": "https://linear.app/test916/team/TES/active"},
            {"type": "click", "label": "Issues"},
            {"type": "click", "label": "Filter"},
            {"type": "wait_modal", "text": "Filter"},
            {"type": "click", "label": "Assignee"},
            {"type": "click", "label": "Me"},
        ]

    if app == "notion" and action == "filter" and obj == "database":
        return [
            {"type": "open_app", "url": "https://www.notion.so"},
            {"type": "click", "label": "Filter"},
            {"type": "wait_modal", "text": "Filter"},
        ]

    if app == "notion" and action == "create" and obj == "page":
        return [
            {"type": "open_app", "url": "https://www.notion.so"},
            {"type": "click", "label": "New page"},
            {"type": "wait_modal", "text": "Templates"},
            {"type": "click", "label": "Meeting notes"},
        ]

    intents = []
    if app == "linear":
        intents.append(
            {"type": "open_app", "url": "https://linear.app/test916/team/TES/active"}
        )
    elif app == "notion":
        intents.append({"type": "open_app", "url": "https://www.notion.so"})
    else:
        intents.append({"type": "open_app", "url": "about:blank"})

    intents.append({"type": "perform_task", "description": task})
    return intents
