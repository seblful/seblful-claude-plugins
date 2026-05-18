---
name: python-testing
description: Apply when writing or reviewing Python tests — TDD workflow, pytest fixtures, parametrization, mocking, async tests, and coverage. Trigger on "write tests", "add tests", "fix tests", test failures, or pytest questions.
---

# Python Testing

## Principles

- **Test behavior, not implementation.** A refactor that preserves behavior must not break tests.
- **One concern per test.** Name describes the behavior: `test_login_with_invalid_credentials_fails`.
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

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
testpaths = ["tests"]
markers = [
    "slow: long-running",
    "integration: hits external systems",
    "unit: pure unit tests",
]
```

## Assertions

Plain `assert` — pytest rewrites for rich diffs.

```python
assert result == expected
assert value is None
assert isinstance(obj, str)

with pytest.raises(ValueError, match="invalid input"):
    validate(bad)

with pytest.raises(CustomError) as exc_info:
    do_thing()
assert exc_info.value.code == 400
```

## Fixtures

```python
@pytest.fixture
def user() -> User:
    return User(id=1, name="Alice")

@pytest.fixture
def database():
    db = Database(":memory:")
    db.create_tables()
    try:
        yield db
    finally:
        db.close()
```

- Scopes: `function` (default) → `class` → `module` → `session`. Promote only when setup is genuinely expensive; broader scope invites cross-test pollution.
- `autouse=True` for unconditional setup (e.g. resetting a global).
- Share via `conftest.py` at the directory level that needs it.

### Built-ins worth knowing

| Fixture | Use for |
|---------|---------|
| `tmp_path` | Temp directory as `Path` — prefer over `tempfile` |
| `monkeypatch` | Patch attrs / env vars for the test only |
| `caplog` | Capture log records |
| `capsys` | Capture stdout / stderr |

```python
def test_uses_env(monkeypatch):
    monkeypatch.setenv("APP__DEBUG", "true")
    assert load_settings().debug is True
```

## Parametrization

```python
@pytest.mark.parametrize(
    "email,expected",
    [
        ("a@b.com", True),
        ("invalid", False),
        ("@no-domain.com", False),
    ],
    ids=["valid", "missing-at", "missing-domain"],
)
def test_email_validation(email: str, expected: bool):
    assert is_valid_email(email) is expected
```

Parametrize fixtures to run a suite across backends:

```python
@pytest.fixture(params=["sqlite", "postgres"])
def db(request):
    return Database(URLS[request.param])
```

## Mocking

- **Patch where it's looked up**, not where it's defined.
- `autospec=True` to catch API drift.
- **Don't mock what you don't own.** Wrap third-party calls in a thin adapter and mock the adapter.
- Never mock the system under test.

```python
@patch("mypkg.service.api_call", autospec=True)
def test_handles_error(api_call):
    api_call.side_effect = ConnectionError("net")
    with pytest.raises(ConnectionError):
        run()
    api_call.assert_called_once()
```

Over-specifying mocks (every arg, every call order) yields brittle tests. Assert the contract you care about, nothing more.

## Async

`pytest-asyncio` with `asyncio_mode = "auto"`.

```python
async def test_fetch():
    result = await fetch("https://api.example.com")
    assert result["status"] == "ok"

@patch("mypkg.async_call", autospec=True)
async def test_async_mock(async_call):
    async_call.return_value = {"ok": True}
    assert (await run())["ok"] is True
    async_call.assert_awaited_once()
```

## Structured-log assertions

```python
def test_logs_user_processed(caplog):
    with caplog.at_level("INFO"):
        process_user("u1")
    assert any(r.message == "user_processed" for r in caplog.records)
```

## Organization patterns

Group cohesive tests in a class when they share fixtures:

```python
class TestCalculator:
    @pytest.fixture
    def calc(self) -> Calculator:
        return Calculator()

    def test_add(self, calc):
        assert calc.add(2, 3) == 5

    def test_divide_by_zero(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
```

Database tests: roll back per test for isolation.

```python
@pytest.fixture
def session():
    s = Session(bind=engine)
    s.begin_nested()
    try:
        yield s
    finally:
        s.rollback()
        s.close()
```

## DO / DON'T

**DO** — write the test first; cover edges (empty, None, boundaries, unicode, errors); keep slow/integration tests behind markers so the unit suite stays fast.

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

**Tests are production code. Clean, fast, behavior-focused.**
