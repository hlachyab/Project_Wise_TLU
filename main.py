"""
Utility script to prepare this repository for hackathon work.

Provides handy commands for greeting teammates, printing quick-start tips,
and generating a starter checklist file.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

DEFAULT_CHECKLIST: List[str] = [
    "Create a virtual environment and install dependencies",
    "Document the problem statement and success criteria",
    "Set up version control branching strategy",
    "Define API contracts or data schemas",
    "Prepare demo script and rehearsal plan",
]


def build_greeting(name: str) -> str:
    """Return a friendly greeting with hackathon context."""
    return f"Hi, {name}! Let's build something awesome for the hackathon."


def format_tips() -> List[str]:
    """Return a list of quick tips to keep the team aligned."""
    return [
        "Keep commits small and descriptive",
        "Automate linting/tests early",
        "Share progress updates frequently",
        "Prototype quickly, then refine",
        "Leave time for polish and demos",
    ]


def write_checklist(destination: Path, project_name: str, items: Iterable[str]) -> Path:
    """Write a checklist file with timestamped header and return the path."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = [
        f"Hackathon checklist for {project_name}",
        f"Generated: {now}",
        "",
    ]

    lines = ["\n".join(header)]
    lines.extend(f"[ ] {item}" for item in items)

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def parse_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(
        description="Handy utilities to kickstart hackathon work in this repository.",
    )
    subparsers = parser.add_subparsers(dest="command")

    greet_parser = subparsers.add_parser("greet", help="Print a friendly greeting.")
    greet_parser.add_argument("name", help="Name to greet")

    subparsers.add_parser("tips", help="Show quick hackathon tips.")

    checklist_parser = subparsers.add_parser(
        "checklist",
        help="Generate a starter checklist file.",
    )
    checklist_parser.add_argument(
        "output",
        type=Path,
        help="Where to write the checklist (e.g. notes/checklist.md)",
    )
    checklist_parser.add_argument(
        "--project-name",
        default="Project",
        help="Name used in the checklist header.",
    )
    checklist_parser.add_argument(
        "--items",
        nargs="*",
        default=None,
        help="Custom checklist items. If omitted, defaults are used.",
    )

    return parser.parse_args(), parser


def main() -> None:
    args, parser = parse_args()

    if args.command == "greet":
        print(build_greeting(args.name))
    elif args.command == "tips":
        for tip in format_tips():
            print(f"- {tip}")
    elif args.command == "checklist":
        items = args.items if args.items else DEFAULT_CHECKLIST
        destination = write_checklist(args.output.expanduser(), args.project_name, items)
        print(f"Checklist written to {destination}")
    else:
        # If no command is provided, show the available options.
        parser.print_help()


if __name__ == "__main__":
    main()
