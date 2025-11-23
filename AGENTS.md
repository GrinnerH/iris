# Repository Guidelines

## Project Structure & Module Organization
- `src/`: Core Python code for IRIS (analysis entrypoint `iris.py`, CodeQL helpers, prompts, and reusable modules/utilities).  
- `scripts/`: Operational scripts for fetching/building benchmarks and generating CodeQL databases (e.g., `fetch_and_build.py`, `build_codeql_dbs.py`).  
- `data/`: Benchmarks, build metadata, patches, and generated artifacts (CodeQL DBs, build info). Treat as large, mostly read-only inputs.  
- `docs/` and `visualizer/`: User-facing docs/assets and the SARIF visualizer (start from `visualizer/server.py`).  
- `environment.yml`, `dep_configs*.json`: Environment pinning and tool path configuration for Java/CodeQL.

## Build, Test, and Development Commands
- Set up environment: `conda env create -f environment.yml && conda activate iris`.  
- Fetch and build a target project: `python scripts/fetch_and_build.py --filter <project_id>`.  
- Build a single project: `python scripts/build_one.py --project <project_id>`.  
- Generate CodeQL DB: `python scripts/build_codeql_dbs.py --project <project_id>`.  
- Run analysis: `python src/iris.py --query <cwe_id> --run-id <tag> --llm <model> <project_id>`.  
- Visualizer: from `visualizer/`, `python server.py` then open `http://localhost:8000`.

## Coding Style & Naming Conventions
- Python 3.10; follow PEP 8 with 4-space indentation and descriptive, snake_case identifiers.  
- Favor small, composable helpers in `src/modules` and `src/utils`; keep query/prompt text in `src/prompts.py` or `src/queries/`.  
- Add docstrings for external-facing functions; prefer type hints for new code.  
- Keep logging consistent with `src/logger.py`; avoid printing in library code.

## Testing Guidelines
- No formal test suite; validate changes via the quickstart pipeline on a small project (e.g., `perwendel__spark_CVE-2018-9159_2.7.1`).  
- Check that `data/build-info/`, `data/codeql-dbs/`, and `output/` populate as expected and that SARIF can be viewed in the visualizer.  
- For query or prompt updates, compare findings before/after on a known project and note differences in the PR description.

## Commit & Pull Request Guidelines
- Recent commits use short, imperative titles with optional PR references (e.g., `Fix CWE queries for 295, 611, and 352 (#64)`).  
- Make commits focused; include brief body when behavior changes or new config is required.  
- PRs should describe scope, run commands used for validation, any dataset/config updates (e.g., `dep_configs*.json`), and screenshots for visualizer changes.  
- Link issues/PR numbers when applicable; flag breaking changes or large data additions explicitly.

## Security & Configuration Tips
- Keep `dep_configs*.json` aligned with your local JDK/Maven/Gradle/CodeQL installations; avoid committing machine-specific paths.  
- Do not commit proprietary CodeQL bundles; reference the required version and paths via environment variables.  
- Large artifacts under `data/` should be treated as generated/cache; confirm before adding new datasets to version control.
