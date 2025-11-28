# Project Wise Hackathon Utilities

This repository contains a lightweight Python utility to jump-start hackathon work.
It includes a minimal Flask app to preview the travel UI mockups and a small Python
module with travel-mode helpers and a CLI demo.

## Requirements

- Python 3.10+
- [Flask](https://flask.palletsprojects.com/) (for the UI preview)

## Flask UI preview

The HTML, CSS, and image assets live in the `Frontend/` directory. The Flask app is
configured to serve templates and static files directly from that folder.

```bash
python APP.py
```

Then open http://127.0.0.1:5000/ in your browser to view the splash screen mock.

## CLI demo

The CLI walks through activating travel mode, fetching FX data, listing insights, and
printing spending summaries for a demo user. Run it from the project root:

```bash
python demo.py
```

Enter a country code (e.g., `HU` or `TR`) when prompted to see the demo output.
