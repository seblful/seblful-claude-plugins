---
name: python-patterns
description: Apply when writing or reviewing Python that will outlive a quick script — production code, packages, anything destined for a repo. Enforces robust-Python principles (intent-obvious code, illegal states unrepresentable, type-driven safety net) on top of the project stack (uv, ruff, ty, structlog, pydantic, typer). Triggers on new modules, classes, dataclasses, type annotations, refactors, code review, "make this production-ready / maintainable / robust" requests, configuration parsing, data validation, public API design, and bug fixes in existing code. Skip only for genuine throwaway scratch.
---

# Python Coding Practices

Code is asynchronous communication with the next maintainer. Three commitments:

1. **Make intent obvious.** One pass through the code should reveal what and why.
2. **Make illegal states unrepresentable.** Encode rules in types; let the checker enforce them.
3. **Build a safety net.** Types, lint, and tests catch what humans miss — shift errors left.

## Principles

- **Readable > clever.** Names carry meaning; structure carries intent.
- **Explicit > implicit.** No magic, no hidden side effects, no surprise globals.
- **EAFP > LBYL.** `try/except` over pre-checks.
- **One obvious way.** PEP 8 + PEP 20. When unsure, write the boring version.
- **Boundaries validate, internals trust.** Parse external data once; trust your own types after.
- **Strictest type that fits.** `Literal["chef", "server"]` beats `str`. `PositiveInt` beats `int`. `list[Recipe]` beats `list`.
- **Optimize for the next reader**, not typing speed today.

Apply these defaults silently. Don't lecture — just write the code this way. Mention a principle only when the user asks "why?" or when you're deliberately deviating.

## Tooling

| Tool | Role | Notes |
|:-----|:-----|:------|
| [uv](https://docs.astral.sh/uv/) | Packages + envs | Never `pip`, `venv`, `poetry` |
| [Ruff](https://docs.astral.sh/ruff/) | Lint + format | Single source of style truth |
| [ty](https://github.com/astral-sh/ty) | Type checker | Hard gate, not a suggestion — run in CI |
| [pytest](https://pytest.org/) | Tests | See [[python-testing]] |

```bash
uv add <pkg>              # prod
uv add --dev <pkg>        # dev
uv run ruff format .
uv run ruff check . --fix
uv run ty check src/ tests/
uv run pytest
```

Strict type-check config, complexity limit (≤10), and `bandit` for security scans belong in `pyproject.toml` from day one. Wire to pre-commit + CI.

## Style

- `snake_case` vars/functions/modules · `CamelCase` classes · `UPPER_SNAKE` constants.
- f-strings for formatting. Google-style docstrings on public API only; document non-obvious invariants and exceptions that escape.
- Absolute imports. Order: stdlib → third-party → local (ruff-enforced).
- Functions stay short — one sentence describes what each does.

## Types — mandatory on every public signature

Python 3.10+ syntax: built-in generics, `|` unions. No `Optional`, `Union`, or `List[...]`.

```python
def first(items: list[T]) -> T | None: ...

JSON = dict[str, Any] | list[Any] | str | int | float | bool | None
```

Reach for the constraining types — each one closes off a class of bugs:

| Need | Reach for |
|:-----|:----------|
| Value may be absent | `T \| None` — forces the caller to handle it |
| One of several types | `A \| B` — adding a variant fails every unhandled caller |
| Restricted string/int | `Literal["a", "b"]` (one-off) or `Enum` (shared) |
| Distinct subtype, no runtime cost | `NewType` — e.g. `SanitizedString` vs `str` |
| Module-level constant | `Final` |
| Fixed-schema dict from JSON | `TypedDict` at boundary, convert to dataclass downstream |

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

### Sum types over product types

Whenever you're documenting "this field only matters when…", that's a sum type screaming to escape:

```python
# Bad — illegal combinations are constructible
@dataclass
class Snack:
    name: str
    condiments: set[str]
    error_code: int       # 0 means "success"
    disposed_of: bool     # only meaningful if error_code != 0

# Good — illegal states unrepresentable
@dataclass
class Snack:
    name: Literal["Hotdog", "Pretzel", "Veggie Burger"]
    condiments: set[Literal["Mustard", "Ketchup"]]

@dataclass
class SnackError:
    error_code: Literal[1, 2, 3, 4, 5]
    disposed_of: bool

Result = Snack | SnackError
```

### Dataclass vs. class with invariants

Use a regular class (not a dataclass) when fields constrain each other, operations are state-dependent, or the constructor must validate inputs. Pattern: validate in `__init__`, mark fields private, expose only invariant-preserving methods. Document invariants in the docstring — the typechecker can't infer them.

`frozen=True` blocks rebinding, not mutation of inner mutable members. Use `tuple` / `frozenset` for fields when deep immutability matters.

### Validate at the boundary with pydantic

Anything from files, network, env vars, CLI, or users becomes a typed model before it flows into business logic. Hand-written `if`/`raise` chains for validation are sprawling and easy to get wrong.

```python
from pydantic import BaseModel, Field, field_validator, PositiveInt
from typing import Literal

class Dish(BaseModel):
    name: str = Field(min_length=1, max_length=16)
    price_in_cents: PositiveInt
    description: str = Field(min_length=1, max_length=80)

class Restaurant(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9 ]*$", min_length=1, max_length=32)
    employees: list[Employee] = Field(min_length=2)

    @field_validator("employees")
    @classmethod
    def must_have_chef_and_server(cls, employees: list[Employee]) -> list[Employee]:
        roles = {e.position for e in employees}
        if "Chef" not in roles or "Server" not in roles:
            raise ValueError("Must have at least one chef and one server")
        return employees
```

After parsing, the data is trustworthy — don't re-validate downstream.

## Inheritance and composition

- Inherit only for **is-a** relationships, and respect Liskov substitutability — subclasses must accept everything the base accepts and return everything the base would. Overriding to raise `NotImplementedError` is a code smell: the base API is wrong.
- **Use composition for code reuse**, not inheritance. A `Restaurant` *has-a* `Menu`. Composition couples to public methods only; inheritance couples to invariants and protected members.
- Mixins are the legitimate exception: small, no state.

Design APIs around natural Python idioms — `__add__`, `__enter__`/`__exit__`, `__iter__` — when callers would reach for them. Don't invent custom method names where the language has the right one.

## Standard library defaults

| Concern | Use | Never |
|:--------|:----|:------|
| Paths | `pathlib.Path` | `os.path.join`, string concat |
| Datetime | `datetime.now(timezone.utc)` | `datetime.utcnow()`, naive datetimes |
| Logging | `structlog` | `logging` direct, `print` for diagnostics |
| HTTP (async) | `httpx.AsyncClient` | `aiohttp`, `urllib`, `requests` in async code |
| CLI | `typer` | `argparse`, hand-rolled `sys.argv` |
| Settings | `pydantic_settings.BaseSettings` | scattered `os.getenv` calls |

```python
cfg = Path("config") / "settings.toml"
out = Path("output/result.json")
out.parent.mkdir(parents=True, exist_ok=True)

logger = structlog.get_logger()
logger.info("user_processed", user_id=uid, duration_ms=42)
```

Log events: lowercase snake_case past-tense (`user_processed`), context as kwargs, never f-string the message.

## Errors

- Catch specific exceptions. Never bare `except`. Don't swallow with `except Exception: pass`.
- Chain with `raise NewError(...) from e`.
- Project-rooted hierarchy so callers can catch broadly or narrowly.
- Never use `assert` for production validation — asserts disappear under `python -O`. Raise an explicit exception.

```python
class AppError(Exception): ...
class ConfigError(AppError): ...

try:
    return Config.from_json(path.read_text())
except FileNotFoundError as e:
    raise ConfigError(f"missing: {path}") from e
```

## Resources — always `with`

Built-ins for files/locks/connections; `@contextmanager` for your own.

```python
@contextmanager
def timer(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        logger.info("timed", name=name, elapsed=time.perf_counter() - start)
```

## Async

I/O-bound only. CPU work belongs in a process pool.

- `asyncio.gather` for concurrency; never block the loop with sync I/O.
- `asyncio.run` only at entry points.

```python
async def fetch(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()

results = await asyncio.gather(*(fetch(u) for u in urls))
```

## Functional idioms

- Comprehensions for simple transforms; a named function once logic spans multiple clauses.
- Generators for streaming or large data.
- Decorators always `@functools.wraps(func)`.

## Performance — measure first

Reach for tricks only after `cProfile` / `timeit` justifies it:

- `"".join(...)` over `+=` in hot loops.
- Generators over materialized lists for large pipelines.
- `__slots__` on small classes with many instances.

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

When reviewing or modifying existing code, fix these silently — mention only if non-obvious:

```python
def f(items=[]): ...                # mutable default — shared across calls
if type(x) == list: ...             # use isinstance
if x == None: ...                   # use `is None`
from os.path import *               # no wildcard imports
try: ...
except: pass                        # no bare except, no silent swallow
datetime.utcnow()                   # naive — use datetime.now(timezone.utc)
os.path.join(a, b)                  # Path(a) / b
logger.info(f"processed {uid}")     # log events take kwargs, not f-strings
assert user.is_admin                # use raise for production checks
```

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
