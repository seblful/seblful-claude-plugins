---
name: python-patterns
description: Apply when writing or reviewing Python that will outlive a quick script — production code, packages, anything destined for a repo. Enforces robust-Python principles (intent-obvious code, illegal states unrepresentable, type-driven safety net) on top of the project stack (uv, ruff, ty, structlog, pydantic, typer). Triggers on new modules, classes, dataclasses, type annotations, refactors, code review, "make this production-ready / maintainable / robust" requests, configuration parsing, data validation, public API design, and bug fixes in existing code. Skip only for genuine throwaway scratch.
---

# Python Coding Practices

Code is asynchronous communication with the next maintainer. Three commitments:

1. **Make intent obvious.** One pass through the code should reveal what and why.
2. **Make illegal states unrepresentable.** Encode rules in types; let the checker enforce them.
3. **Build a safety net.** Types, lint, and tests catch what humans miss — shift errors left.

Apply these defaults silently. Don't lecture — write the code this way. Mention a principle only when the user asks "why?" or when deliberately deviating.

## Principles

- **Readable > clever.** Names carry meaning; structure carries intent.
- **Explicit > implicit.** No magic, no hidden side effects, no surprise globals.
- **EAFP > LBYL.** `try/except` over pre-checks when consuming fallible operations; for your own APIs, model expected absence as `T | None` rather than raising.
- **One obvious way.** PEP 8 + PEP 20. When unsure, write the boring version.
- **Boundaries validate, internals trust.** Parse external data once; trust your own types after.
- **Strictest type that fits.** Each narrowing closes off a class of bugs.
- **Optimize for the next reader**, not typing speed today.

## Tooling

| Tool | Role |
|:-----|:-----|
| [uv](https://docs.astral.sh/uv/) | Packages and envs — never `pip`, `venv`, `poetry` |
| [Ruff](https://docs.astral.sh/ruff/) | Lint and format — single source of style truth |
| [ty](https://github.com/astral-sh/ty) | Type checker — hard gate in CI, not a suggestion |
| [pytest](https://pytest.org/) | Tests — see [[python-testing]] |

Strict type-check config, complexity limit (≤10), and `bandit` security scans belong in `pyproject.toml` from day one. Wire to pre-commit and CI.

## Style

`snake_case` for vars/functions/modules, `CamelCase` for classes, `UPPER_SNAKE` for constants. f-strings for formatting (exception: structured log events — see logging below). Google-style docstrings on public API only — document non-obvious invariants and exceptions that escape. Absolute imports, ordered stdlib → third-party → local. Functions stay short enough that one sentence describes what they do.

## Types — mandatory on every public signature

Python 3.10+ syntax: built-in generics, `|` unions. No `Optional`, `Union`, or `List[...]`.

Reach for the constraining type:

| Need | Reach for |
|:-----|:----------|
| Value may be absent | `T \| None` — forces the caller to handle it |
| One of several types | `A \| B` — adding a variant fails every unhandled caller |
| Restricted string/int | `Literal[...]` (one-off) or `Enum` (shared) |
| Distinct subtype, no runtime cost | `NewType` |
| Module-level constant | `Final` |
| Fixed-schema dict from JSON | `TypedDict` at boundary, dataclass downstream |

Never return `None` from a function whose return type is `T` — fix the signature or narrow the value. Don't use exceptions for expected absence; return `T | None`.

`typing.Protocol` for structural typing — prefer it for new abstractions over `abc.ABC`. Use `ABC` only when enforced inheritance is the point.

## Data modeling

| Use case | Choice |
|:---------|:-------|
| Fixed set of values | `Enum` (default), `Flag` only if bitwise-combined. Avoid `IntEnum` unless interop demands it. |
| Grouped independent fields | `@dataclass(frozen=True)` |
| Grouped fields with invariants | regular `class`, private fields, validated `__init__` |
| Accept duck-typed callers | `Protocol` |
| External / untrusted data | `pydantic.BaseModel` |
| Env-var config | `pydantic_settings.BaseSettings` |
| Internal mutable record | `@dataclass` |

**Sum types over product types.** Whenever you're documenting "this field only matters when…", that's a sum type screaming to escape — split into a `Union` of dataclasses so illegal combinations stop being constructible.

**Class over dataclass when fields constrain each other.** Validate in `__init__`, keep fields private, expose only invariant-preserving methods. Document invariants in the docstring; the typechecker can't infer them. `frozen=True` blocks rebinding, not mutation of inner mutables — use `tuple` / `frozenset` for deep immutability.

**Validate at the boundary with pydantic.** Anything from files, network, env vars, CLI, or users becomes a typed model before it flows into business logic. After parsing, data is trustworthy — don't re-validate downstream. Hand-written `if`/`raise` validation chains are sprawling and easy to get wrong.

## Inheritance and composition

Inherit only for **is-a** relationships, and respect Liskov substitutability — subclasses must accept everything the base accepts and return everything the base would. Overriding to raise `NotImplementedError` means the base API is wrong.

**Use composition for code reuse**, not inheritance. Composition couples to public methods only; inheritance couples to invariants and protected members. Mixins are the legitimate exception: small, no state.

Design APIs around natural Python idioms (`__add__`, `__enter__`/`__exit__`, `__iter__`) when callers would reach for them. Don't invent custom method names where the language has the right one.

## Standard library defaults

| Concern | Use | Never |
|:--------|:----|:------|
| Paths | `pathlib.Path` | `os.path.join`, string concat |
| Datetime | `datetime.now(timezone.utc)` | `datetime.utcnow()`, naive datetimes |
| Logging | `structlog` | `logging` direct, `print` for diagnostics |
| HTTP (async) | `httpx.AsyncClient` | `aiohttp`, `urllib`, `requests` in async code |
| CLI | `typer` | `argparse`, hand-rolled `sys.argv` |
| Settings | `pydantic_settings.BaseSettings` | scattered `os.getenv` calls |

Log events: lowercase snake_case past-tense (`user_processed`), context as kwargs, never f-string the message.

## Errors

Catch specific exceptions. Never bare `except`. Don't swallow with `except Exception: pass`. Chain with `raise NewError(...) from e`. Build a project-rooted hierarchy so callers can catch broadly or narrowly. Never use `assert` for production validation — asserts disappear under `python -O`; raise an explicit exception.

## Resources — always `with`

Built-ins for files, locks, connections. `@contextmanager` for your own — anything that owns acquire/release semantics belongs in one, so callers can't forget cleanup.

## Async

I/O-bound only. CPU work belongs in a process pool. `asyncio.gather` for concurrency; never block the loop with sync I/O. `asyncio.run` only at entry points.

## Functional idioms

Comprehensions for simple transforms; a named function once logic spans multiple clauses. Generators for streaming or large data. Decorators always `@functools.wraps(func)`.

## Performance — measure first

Reach for tricks only after `cProfile` / `timeit` justifies it: `"".join(...)` over `+=` in hot loops, generators over materialized lists for large pipelines, `__slots__` on small classes with many instances.

## Package layout

```
src/{package}/
├── __init__.py        # __version__, public exports, __all__
├── cli.py             # Typer entry point
├── logging.py         # structlog setup
├── settings.py        # Pydantic settings
├── py.typed           # PEP 561 marker
└── ...
tests/
├── conftest.py
└── test_*.py
```

## Anti-patterns to flag and rewrite

Fix silently when reviewing or modifying existing code:

- Mutable default arguments (`def f(items=[])`) — shared across calls.
- `type(x) == list` — use `isinstance`.
- `x == None` — use `is None`.
- Wildcard imports.
- Bare `except` or silent `except Exception: pass`.
- `datetime.utcnow()` — naive; use timezone-aware.
- `os.path.join` — use `Path`.
- f-string log messages — log events take kwargs.
- `assert` for production validation.

Structural smells:

- Function declared `-> T` but a branch returns `None` → change to `T | None` or narrow first.
- Dataclass field that "only matters when another field is X" → split into a `Union` of dataclasses.
- `IntEnum` used for non-interop purposes → plain `Enum`.
- Bare `dict` or `list` in an annotation → annotate element types.
- `tuple` of 3+ unrelated values returned from a function → dataclass.
- Hand-written cascading `if`/`raise` validation of external input → pydantic model.
- Override that raises `NotImplementedError` → the is-a relationship is wrong.
- Public attribute the class must keep valid → make it private, expose a method.

**Write the obvious version. Optimize only when measurement demands it.**
