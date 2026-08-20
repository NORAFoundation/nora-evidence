# nora-evidence

Provenance-first evidence and record substrate with exact locators, source genealogy, transformations, custody, and reconstructable basis graphs.

**Status:** pre-alpha / migration build

## Hard problem

Preserve and transform heterogeneous records while keeping every consequential derived assertion reconstructable to exact source occurrences and transformation history.

## Why this exists

This repository isolates one reusable public-interest technology problem from the NORA Foundation platform so developers and researchers can improve it independently.

## Minimum vertical slice

synthetic source -> occurrence -> locator -> transformation -> basis edge -> reconstructability check

## Non-goals

- NORA One product UI
- private Matter storage
- generic SaaS dashboard work
- autonomous legal advice
- publication of private source corpora
- claims of production readiness without release evidence

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make doctor
make validate
make test
python examples/demo.py
```

## Source provenance

Legacy NORA repositories are component sources, not authorities. Migrated units are recorded in `SOURCE_PROVENANCE.yaml`.

## Contributing

See `CONTRIBUTING.md` and `ROADMAP.md`.

## Security

See `SECURITY.md`.

## License

New clean-room code is Apache-2.0. Migrated/third-party material remains subject to its recorded source license and notices.
