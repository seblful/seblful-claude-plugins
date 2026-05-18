---
name: python-testing
description: Apply when writing or reviewing Python tests — TDD workflow, pytest fixtures, parametrization, mocking, async tests, and coverage. Trigger on "write tests", "add tests", "fix tests", test failures, or pytest questions.
---

# Python Testing

Tests are production code. Clean, fast, behavior-focused.

## Principles

- **Test behavior, not implementation.** A refactor that preserves behavior must not break tests.
- **One concern per test.** Name describes the behavior under verification.
- **Independent and order-free.** No shared mutable state. Any test runs in isolation.
- **TDD where it pays off**: red → green → refactor. Let the test shape the API.
- **Coverage is a floor, not a goal.** 80%+ overall, 100% on critical paths; chase missing branches, not the percentage.

## Layout

```
tests/
├── conftest.py        # shared fixtures
├── unit/              # fast, no I/O, no network
├── integration/       # real deps, marked
└── e2e/
```

Configure `addopts = "-ra --strict-markers"` and declare every marker (`slow`, `integration`, `unit`) in `pyproject.toml`. Unknown markers should fail loudly.

## Arrange–Act–Assert

Default layout for every test, with the three phases visually distinct. One logical assertion per test. The test name carries the contract.

A large Arrange block is a design smell — the code under test has too many dependencies. Extract setup into helpers, then fixtures; if that doesn't shrink it, the design itself wants changing.

## Assertions

Plain `assert` — pytest rewrites for rich diffs. Use `pytest.raises(..., match=...)` for expected exceptions and inspect `exc_info.value` when the exception itself carries state worth checking.

**Invariant assertions via context managers.** Classes that maintain invariants are easy to break silently. Wrap construction in a context manager that re-asserts the invariants on exit — every test using the wrapper guards the contract, even tests not written for it.

## Fixtures

Scopes: `function` (default) → `class` → `module` → `session`. Promote only when setup is genuinely expensive; broader scope invites cross-test pollution. `autouse=True` for unconditional setup. Share via `conftest.py` at the directory level that needs it. Yield-based fixtures for anything with teardown.

Built-ins worth defaulting to:

| Fixture | Use for |
|---------|---------|
| `tmp_path` | Temp directory as `Path` — prefer over `tempfile` |
| `monkeypatch` | Patch attrs / env vars for the test only |
| `caplog` | Capture log records |
| `capsys` | Capture stdout / stderr |

## Parametrization

Use `@pytest.mark.parametrize` with explicit `ids` so failure output names the case, not the values. Parametrize *fixtures* to run a whole suite across backends (sqlite vs postgres, sync vs async client) without duplicating tests.

## Mocking

- **Patch where it's looked up**, not where it's defined.
- `autospec=True` to catch API drift.
- **Don't mock what you don't own.** Wrap third-party calls in a thin adapter and mock the adapter.
- Never mock the system under test.

Over-specifying mocks (every arg, every call order) yields brittle tests. Assert the contract you care about, nothing more.

## Async

`pytest-asyncio` with `asyncio_mode = "auto"`. Use `assert_awaited_once()` rather than `assert_called_once()` for awaited mocks — the awaited-form catches the missing `await`.

## Property-based testing with Hypothesis

For pure functions, parsers, serializers, and anything with an interesting input space, describe the *property* and let Hypothesis generate hundreds of cases. It shrinks failures to a minimal counterexample. Reach for it whenever you write a pure transform or a serialize/deserialize pair — property tests catch nondeterminism and edge cases that example-based tests miss.

## Mutation testing — occasional sanity check

Once a project has a meaningful suite, run `mutmut` before a release or when coverage looks suspiciously high. It mutates the code and re-runs the tests; surviving mutants reveal tests that weren't actually checking what they looked like they were checking. Don't wire it into every commit — it's slow. Run it deliberately.

## Organization

Group cohesive tests in a class when they share fixtures. Database tests: roll back per test via a nested transaction for isolation.

## DO / DON'T

**DO** — write the test first; cover edges (empty, `None`, boundaries, unicode, errors); keep slow and integration tests behind markers so the unit suite stays fast; assert on structured log events by record, not by formatted string.

**DON'T** — test private internals; share mutable state across tests; over-specify mocks; use bare `try/except` instead of `pytest.raises`.

## Running

```bash
uv run pytest                          # all
uv run pytest -x --lf                  # stop on first fail, only last-failed
uv run pytest -k "user and not slow"   # filter by name
uv run pytest -m "not slow"            # filter by marker
uv run pytest --cov=src --cov-report=term-missing
uv run pytest --pdb                    # debugger on failure
```
