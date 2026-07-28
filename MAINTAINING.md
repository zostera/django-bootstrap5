# Maintaining django-bootstrap5

Notes for maintainers. For how to submit a contribution, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Version support policy

These are rules, not a snapshot of current versions — the current matrix lives in `tox.ini`
(`envlist`), `.github/workflows/ci.yml` (the `python_django_matrix` job), and `pyproject.toml`
(classifiers + `dependencies`). Those three files are the source of truth and must agree with
each other. Don't restate the matrix as a table in prose docs (AGENTS.md, README, etc.) — a
copy always drifts out of sync with the files that actually enforce it.

### Python and Django

- Support every Python and Django release cycle that is not end-of-life, per
  [endoflife.date/python](https://endoflife.date/python) and
  [endoflife.date/django](https://endoflife.date/django). Drop a cycle from the matrix as soon
  as it goes EOL — don't wait for a scheduled release to do it.
- Always track Django's `main` branch in the matrix. Add a new Django release series
  (e.g. 6.1) alongside `main` as soon as `main` has diverged from it — i.e. once upstream
  cuts a `stable/X.Y.x` branch and `main` itself moves on to the next alpha. Don't wait for
  the new series' final release.
- Add a new Python pre-release as a **non-blocking** CI job (`continue-on-error: true`) as
  soon as it's installable — `uv python install` can usually fetch a new CPython the same day
  it's cut, so the interpreter itself is rarely the blocker. Only make the job blocking once
  our C-extension test dependencies (currently Pillow) publish wheels for it; that's normally
  the actual bottleneck.

### Bootstrap

- Keep the default CDN URLs in `src/django_bootstrap5/core.py` pinned to the latest Bootstrap
  5.3.x patch release. Check [github.com/twbs/bootstrap/releases](https://github.com/twbs/bootstrap/releases)
  for newer ones.
- When bumping it, update the URL and the SRI `integrity` hash together, and verify the hash
  against the actual downloaded file — don't copy one from memory or from an unrelated source.
- Don't hardcode a Bootstrap version number in prose docs. Point at `core.py` and the upstream
  releases page instead.

## Release process

1. Update `CHANGELOG.md` and bump `version` in `pyproject.toml`
2. Commit and push to `main`
3. `just build` — builds wheel + tarball, runs packaging checks, and smoke-tests both against an isolated env
4. `just release-tag` — creates and pushes the version tag; GitHub Actions publishes to PyPI

`just release-tag` requires a clean working directory and the current branch to be `main`. It will fail otherwise.
