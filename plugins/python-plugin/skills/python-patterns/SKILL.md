---
name: python-patterns
description: Apply when writing or reviewing Python code — enforces PEP 8, type hints, modern idioms, and the project stack (uv, ruff, ty, structlog, pydantic, typer). Trigger on new Python files, code style questions, tooling setup, or module structure.
---

# Python Coding Practices

## Principles

- **Readable > clever.** Names carry meaning; structure carries intent.
- **Explicit > implicit.** No magic, no hidden side effects, no surprise globals.
- **EAFP > LBYL.** `try/except` over pre-checks.
- **One obvious way.** PEP 8 + PEP 20. When unsure, write the boring version.
- **Boundaries validate, internals trust.** Parse external data once; trust your own types after.

## Tooling

| Tool | Role | Notes |
|:-----|:-----|:------|
| [uv](https://docs.astral.sh/uv/) | Packages + envs | Never `pip`, `venv`, `poetry` |
| [Ruff](https://docs.astral.sh/ruff/) | Lint + format | Single source of style truth |
| [ty](https://github.com/astral-sh/ty) | Type checker | Run in CI |
| [pytest](https://pytest.org/) | Tests | See [[python-testing]] |

```bash
uv add <pkg>              # prod
uv add --dev <pkg>        # dev
uv run ruff format .
uv run ruff check . --fix
uv run ty check src/ tests/
uv run pytest
```

## Style

- `snake_case` vars/functions/modules · `CamelCase` classes · `UPPER_SNAKE` constants.
- f-strings for formatting. Google-style docstrings on public API only.
- Absolute imports. Order: stdlib → third-party → local (ruff-enforced).

## Types — mandatory on every signature

Python 3.10+ syntax: built-in generics, `|` unions. No `Optional`, `Union`, or `List[...]`.

```python
def first(items: list[T]) -> T | None: ...

JSON = dict[str, Any] | list[Any] | str | int | float | bool | None
```

- `typing.Protocol` for structural typing — prefer it for new abstractions.
- `abc.ABC` only when you need enforced inheritance.

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

## Data modeling

| Use case | Choice |
|:---------|:-------|
| Env-var config | `BaseSettings` |
| External / untrusted data | `BaseModel` |
| Internal records | `@dataclass` (or `pydantic.dataclass`) |
| Immutable DTOs / value objects | `@dataclass(frozen=True)` |

Validate at the boundary; pass typed objects within.

## Errors

- Catch specific exceptions. Never bare `except`.
- Chain with `raise NewError(...) from e`.
- Define a project-rooted hierarchy so callers can catch broadly or narrowly.

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
- Decorators always `@functools.wraps(func)` to preserve metadata.

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

## Anti-patterns

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
```

**Write the obvious version. Optimize only when measurement demands it.**
