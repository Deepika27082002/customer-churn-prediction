- [ ] Inspect repository files relevant to dependency setup (requirements.txt, any app entrypoint).
- [ ] Create and use an environment-local, compatible dependency set to fix `import pandas` crash.
- [x] Update `requirements.txt` to pinned versions known to be compatible.

- [ ] Remove/recreate the local venv and reinstall via `pip install -r requirements.txt`.
- [ ] Run a sanity import test: `python -c "import pandas as pd; print(pd.__version__)"`.
- [ ] (Optional) Re-run notebook/app import check.
