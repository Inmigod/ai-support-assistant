# AI Support Assistant

A Python-based IT support assistant project. **Current version: rule-based prototype (not generative AI yet).**

## Features
- Classifies basic DNS, network and computer startup problems
- Suggests non-destructive diagnostic steps
- Includes unit tests and handles empty input
- Uses only the Python standard library

## Run
```bash
python main.py
```

## Tests
```bash
python -m unittest discover -s tests -v
```

## Roadmap
1. Improve classifications and add structured support cases.
2. Build a REST API with input validation.
3. Integrate an LLM API with secrets stored in environment variables.
4. Add safe fallback behavior, logging, tests and documentation.

**Privacy:** This project uses no proprietary company code or data.
