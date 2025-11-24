"""
agent_b.py
----------

This script provides a command‑line interface for running the Agent B
automation workflow.  It accepts a natural‑language task and an output
directory, uses ``intent_parser`` to convert the task into intent
steps, and then launches an ``Executor`` to perform those steps using
Playwright.  The resulting dataset of screenshots and metadata is
written to the specified directory.

Example usage:

```sh
python agent_b.py --task "Create a project in Linear" --out data/linear
```

The code is designed to be educational and may require additional
context (e.g. login credentials) to operate fully on real web
applications.  See the README.md for more details.
"""

import argparse
import asyncio
import os
from typing import List, Dict

from intent_parser import parse_task
from executor import Executor


def main(args: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Agent B browser automation agent.")
    parser.add_argument("--task", required=True, help="Natural‑language description of the task to perform.")
    parser.add_argument("--out", required=True, help="Output directory to store screenshots and metadata.")
    ns = parser.parse_args(args)
    task_str = ns.task
    output_dir = ns.out

    intents: List[Dict[str, str]] = parse_task(task_str)
    print(f"Parsed intents: {intents}")
    executor = Executor(intents, output_dir)
    asyncio.run(executor.run())


if __name__ == "__main__":
    main()