"""
metadata.py
-----------

This module defines classes and functions for recording metadata about
browser states captured by Agent B. Each state entry records the
screenshot file name, URL, title and the intent that led to the state.

We also store a lightweight classification of the UI state
(e.g. "page", "modal", "form") so that downstream consumers can
distinguish URL-based states from transient UI overlays.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json
import os


@dataclass
class StateEntry:
    index: int
    intent_type: str
    intent_label: str
    url: str
    title: str
    screenshot: str
    state_kind: str  # e.g. "page", "modal", "form"


class MetadataRecorder:
    """Record states and write them to a metadata JSON file."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self.entries: List[StateEntry] = []

    def add_state(
        self,
        index: int,
        intent: Dict[str, Any],
        page,
        state_kind: str = "page",
        title: str = "",
    ) -> None:
        """Add a state entry after completing an intent.

        ``page`` is a Playwright ``Page`` object. The screenshot file
        must already have been saved by the caller, using the same
        naming pattern as below.
        """
        screenshot_name = f"state_{index:03d}.png"
        entry = StateEntry(
            index=index,
            intent_type=intent.get("type", "unknown"),
            intent_label=intent.get("label", intent.get("description", "")),
            url=page.url,
            title=title,
            screenshot=screenshot_name,
            state_kind=state_kind,
        )
        self.entries.append(entry)

    def save(self) -> None:
        """Write the metadata entries to a file called ``metadata.json``."""
        data = [asdict(entry) for entry in self.entries]
        path = os.path.join(self.output_dir, "metadata.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


__all__ = ["MetadataRecorder", "StateEntry"]
