# caminotutor.com — notes for Claude

- Static site on Vercel; `main` auto-deploys. Work in the `design-v2` worktree, then fast-forward `main` and push.
- Subject-guide pages (`/subjects/`) are maintained by the scripts in `_build/`. After any change to them, run `python3 _build/run.py`, then `python3 _build/run.py --check` must report `0 page(s) would change`. Read `_build/README.md` first.
- Never run `_build/subj/build_subjects.py` or `build_services.py` without understanding that they overwrite later HTML edits (they require `--force`).
- Curriculum facts come only from official sources (IB, Cambridge, College Board, universities). Official English rubric text is quoted verbatim with Japanese translation and credit.
