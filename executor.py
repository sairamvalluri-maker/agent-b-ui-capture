"""
executor.py
-----------

This module defines the ``Executor`` class, responsible for
interacting with web applications using Playwright. It executes
intents produced by the parser, captures screenshots after each
intent, and delegates metadata recording to a ``MetadataRecorder``.

The executor employs simple heuristics for locating UI elements:

* ``click`` intents search for a button, link or element containing the
  specified text. It uses generic text and CSS selectors.
* ``wait_modal`` intents wait for a modal or dialog containing the
  specified text.

This is a simplified example and will need app-specific tuning for
real-world use.
"""

import asyncio
import os
from typing import Dict, Any, List

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from metadata import MetadataRecorder

USER_DATA_DIR = ".playwright-linear-profile"


class Executor:
    def __init__(self, intents: List[Dict[str, Any]], output_dir: str) -> None:
        self.intents = intents
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.recorder = MetadataRecorder(self.output_dir)

    async def run(self) -> None:
        """Execute all intents sequentially using a persistent Playwright context."""
        async with async_playwright() as p:
            # Use persistent context so we stay logged into Linear/Notion
            context = await p.chromium.launch_persistent_context(
                USER_DATA_DIR,
                headless=False,
            )
            page = await context.new_page()

            try:
                for idx, intent in enumerate(self.intents, start=1):
                    intent_type = intent.get("type")
                    try:
                        if intent_type == "open_app":
                            url = intent.get("url")
                            await page.goto(url, wait_until="domcontentloaded")
                        elif intent_type == "click":
                            label = intent.get("label")
                            await self._click_by_text(page, label)
                        elif intent_type == "fill":
                            label = intent.get("label")
                            text = intent.get("text", "")
                            await self._fill_field(page, label, text)
                        elif intent_type == "wait_modal":
                            text = intent.get("text")
                            await self._wait_for_modal(page, text)
                        elif intent_type == "perform_task":
                            # Generic fallback: no specific action; just note current state
                            pass

                        # Capture state after each intent
                        await self._capture_state(idx, intent, page)

                    except PlaywrightTimeoutError:
                        print(f"[Warning] Timeout while executing intent {intent_type}")
                        await self._capture_state(idx, intent, page)

                # Save metadata when finished
                self.recorder.save()
            finally:
                await context.close()

    async def _click_by_text(self, page, label: str) -> bool:
        """Click an element by multiple possible selector strategies."""
        if not label:
            return False

        selectors = [
            f"text={label}",
            f"button:has-text('{label}')",
            f"[aria-label='{label}']",
            f"a:has-text('{label}')",
            f"div:has-text('{label}')",
            f"span:has-text('{label}')",
        ]

        for selector in selectors:
            try:
                el = page.locator(selector).first
                if await el.is_visible():
                    await el.click()
                    return True
            except Exception:
                pass

        print(f"[Warning] Could not find element with text '{label}'")
        return False

    async def _fill_field(self, page, label: str, text: str) -> None:
        """Fill an input field located by its label text."""
        try:
            locator = page.get_by_label(label)
            await locator.first.fill(text, timeout=5000)
        except PlaywrightTimeoutError:
            print(f"[Warning] Could not fill field '{label}'")

    async def _wait_for_modal(self, page, text: str) -> None:
        """Wait for a modal containing the specified text to appear."""
        try:
            await page.get_by_text(text).first.wait_for(timeout=8000)
        except PlaywrightTimeoutError:
            # If no modal appears, just wait a bit to let the page settle
            await asyncio.sleep(2)

    async def _infer_state_kind(self, page, intent: Dict[str, Any]) -> str:
        """Heuristically classify the current UI state.

        Returns a simple label like "page", "modal" or "form" so that
        downstream consumers can reason about non-URL states.
        """
        intent_type = intent.get("type", "")

        # If there is any visible dialog / modal, treat as modal
        try:
            modal_locator = page.locator(
                "dialog, [role=dialog], .modal, .ReactModal__Content"
            )
            first_modal = modal_locator.first
            if await first_modal.is_visible():
                return "modal"
        except Exception:
            # If anything goes wrong, fall back to other heuristics
            pass

        # If we're filling fields, it's likely a form state
        if intent_type == "fill":
            return "form"

        # Default classification
        return "page"

    async def _capture_state(self, idx: int, intent: Dict[str, Any], page) -> None:
        """Capture a screenshot and record metadata for the current page."""
        # Infer the kind of UI state we are currently in
        state_kind = await self._infer_state_kind(page, intent)

        # Save screenshot
        screenshot_name = f"state_{idx:03d}.png"
        path = os.path.join(self.output_dir, screenshot_name)
        await page.screenshot(path=path, full_page=True)

        # Get current page title (async)
        title = await page.title()

        # Record metadata using the recorder, including state_kind and title
        self.recorder.add_state(
            index=idx,
            intent=intent,
            page=page,
            state_kind=state_kind,
            title=title,
        )


__all__ = ["Executor"]
