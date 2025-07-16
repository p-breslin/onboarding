## Setup

1. Install [uv](https://github.com/astral-sh/uv)
2. Clone the repo and sync the environment:

   ```bash
   uv sync
   uv pip install -e .
   uv run python -m core.cli --help
   ```