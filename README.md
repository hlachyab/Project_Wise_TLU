# Project Wise Hackathon Utilities

This repository contains a lightweight Python utility to jump-start hackathon work. It offers quick commands for greeting teammates, sharing tips, and generating a starter checklist.

## Requirements

- Python 3.10+

## Usage

Run commands from the project root:

- Print a greeting:

  ```bash
  python main.py greet "Your Name"
  ```

- Show quick tips:

  ```bash
  python main.py tips
  ```

- Generate a checklist (uses defaults unless custom items are provided):

  ```bash
  python main.py checklist notes/checklist.md --project-name "Demo App"
  ```

- Provide custom checklist items:

  ```bash
  python main.py checklist notes/custom.md --items "Set up CI" "Prepare slides"
  ```

The checklist command will create parent directories as needed and write a timestamped header.
