---
description: Refactor Python toward SOLID, clean-code, and production-ready patterns — small functions, narrow interfaces, dependency injection, pure cores, and testable seams
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Agent
---

# Python Refactoring — SOLID & Clean Code

Apply this catalogue to the code in scope: `$ARGUMENTS` if provided, otherwise the current file/selection or most recently edited Python module. Pair with the `python-patterns` and `python-testing` skills for style and verification.

## How to run this command

1. Identify the target from `$ARGUMENTS` or the most recently edited Python code.
2. Run the **Smell → Fix Map** as a triage pass; list smells found, ranked by impact.
3. Confirm tests exist and are green; if not, write characterization tests first.
4. Apply refactorings one at a time using the **Workflow** at the bottom. Show diffs; do not batch unrelated moves.
5. Cross-check against the **Production-Readiness Checklist** before declaring done.

## Operating Rules

1. **Refactor under green tests.** No behavior change without a test that fails first if you break it. If no tests exist, write characterization tests before touching code.
2. **One refactor per commit.** Rename, extract, inline, move — separate commits. Never mix refactor with feature/bugfix.
3. **Smallest reversible step.** Prefer many tiny diffs over one big rewrite. The IDE's rename/extract is safer than hand edits.
4. **Names are the API.** A bad name survives; rename early and aggressively.
5. **Delete first.** Dead code, unused params, speculative abstractions, "just in case" branches — remove them.

## Smell → Fix Map

| Smell                                                | Likely Fix                                                 |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| Function > ~20 lines, multiple `if`/`for` levels     | **Extract Function**                                       |
| Same code in 2+ places                               | **Extract Function** / **Pull Up Method**                  |
| Long parameter list (>3-4)                           | **Introduce Parameter Object** (dataclass/`BaseModel`)     |
| Boolean flag parameter switching behavior            | **Split Function** by flag value                           |
| Class touches many unrelated concerns                | **Extract Class** (SRP)                                    |
| Class with mostly data, no behavior                  | Use `@dataclass` / `BaseModel`                             |
| Class with one method                                | **Replace Class with Function**                            |
| `isinstance` ladder / type-switch                    | **Replace Conditional with Polymorphism** / `match`-`case` |
| Deep nesting                                         | **Guard Clauses** / early return                           |
| Mutable global / module-level state                  | **Inject as parameter** / settings object                  |
| Hard-coded I/O inside logic                          | **Separate I/O from computation** (pure core)              |
| `time.now()`, `random`, `requests` in business logic | **Inject clock/rng/http client** (DIP)                     |
| `None`-checking everywhere                           | **Null Object** / make non-optional / `Result` type        |
| Stringly-typed status/role                           | `Enum` / `Literal[...]`                                    |
| Comment explaining what code does                    | Rename / extract until the code says it                    |
| `# TODO` older than a sprint                         | Resolve, ticket, or delete                                 |

## SOLID in Python

### S — Single Responsibility

One reason to change. If a class both _parses_ and _persists_, split it.

```python
# Bad — parsing + persistence + notification
class OrderProcessor:
    def process(self, raw: str) -> None:
        data = json.loads(raw)
        self.db.save(data)
        self.smtp.send(data["email"], "ok")

# Good — three collaborators
class OrderParser:
    def parse(self, raw: str) -> Order: ...

class OrderRepository:
    def save(self, order: Order) -> None: ...

class OrderNotifier:
    def confirm(self, order: Order) -> None: ...

def process_order(raw: str, parser, repo, notifier) -> None:
    order = parser.parse(raw)
    repo.save(order)
    notifier.confirm(order)
```

### O — Open/Closed

Open to extension via new types/strategies; closed to modification of stable code.

```python
# Closed: registry pattern — add new exporters without editing the dispatcher
EXPORTERS: dict[str, Callable[[Report], bytes]] = {}

def register(fmt: str):
    def deco(fn): EXPORTERS[fmt] = fn; return fn
    return deco

@register("csv")
def to_csv(r: Report) -> bytes: ...

@register("json")
def to_json(r: Report) -> bytes: ...

def export(report: Report, fmt: str) -> bytes:
    return EXPORTERS[fmt](report)
```

### L — Liskov Substitution

Subtypes must honor the supertype's contract. In Python, this applies to **`Protocol`s and ABCs**: don't strengthen preconditions, weaken postconditions, or raise new exception types not in the base contract.

```python
class Repository(Protocol):
    def get(self, id: str) -> User: ...   # contract: raises NotFoundError if missing

# Bad — narrows acceptable input
class CachedRepo:
    def get(self, id: str) -> User:
        if not id.startswith("u_"): raise ValueError  # caller didn't sign up for this
        ...
```

### I — Interface Segregation

Many small `Protocol`s beat one fat one. Clients depend only on what they use.

```python
class Reader(Protocol):
    def read(self, key: str) -> bytes: ...

class Writer(Protocol):
    def write(self, key: str, data: bytes) -> None: ...

# A read-only consumer takes Reader, not a Storage god-interface.
def render_page(key: str, store: Reader) -> str: ...
```

### D — Dependency Inversion

High-level policy depends on abstractions; low-level details implement them. Inject collaborators; don't `import` them inside functions.

```python
# Bad — concrete coupling, untestable without network
def fetch_price(symbol: str) -> Decimal:
    r = httpx.get(f"https://api.x/{symbol}")
    return Decimal(r.json()["price"])

# Good — inject the HTTP boundary
class PriceClient(Protocol):
    def get(self, symbol: str) -> dict: ...

def fetch_price(symbol: str, client: PriceClient) -> Decimal:
    return Decimal(client.get(symbol)["price"])
```

## Clean Code Principles (Python flavor)

- **Functions do one thing.** If you can extract a method and name it meaningfully, do.
- **Levels of abstraction.** Don't mix high-level orchestration with bit-twiddling in the same function.
- **Command-Query Separation.** A function either _returns a value_ or _changes state_ — not both, where avoidable.
- **Tell, don't ask.** Push behavior to the data owner instead of pulling fields out and computing externally.
- **Law of Demeter.** `a.b.c.d()` is a refactoring smell — add a method on `a`.
- **No flag arguments.** `send(urgent=True)` → `send_urgent()` and `send_normal()`, or strategy.
- **Output arguments are bad.** Return new values; don't mutate caller's objects implicitly.
- **DRY, but not premature.** Three uses before extracting; two similar things may diverge.
- **Boy-scout rule.** Leave the file cleaner than you found it — but in a _separate commit_.

## Core Refactorings (with Python-specific notes)

### Extract Function

```python
# Before
def post_order(order):
    if order.total < 0: raise ValueError
    if not order.items: raise ValueError
    if order.user.banned: raise PermissionError
    db.save(order)
    smtp.send(order.user.email, render(order))

# After
def post_order(order: Order) -> None:
    _validate(order)
    _persist(order)
    _notify(order)
```

### Introduce Parameter Object

```python
# Before
def search(q: str, page: int, size: int, sort: str, asc: bool, filters: dict): ...

# After
@dataclass(frozen=True)
class SearchQuery:
    q: str
    page: int = 1
    size: int = 20
    sort: str = "relevance"
    asc: bool = True
    filters: Mapping[str, str] = field(default_factory=dict)

def search(query: SearchQuery) -> SearchResult: ...
```

### Replace Conditional with Polymorphism

```python
# Before
def fee(account):
    if account.kind == "basic":   return 0
    if account.kind == "pro":     return 5
    if account.kind == "enterprise": return 50

# After — strategy via Protocol
class Plan(Protocol):
    def fee(self) -> int: ...

class Basic:      def fee(self): return 0
class Pro:        def fee(self): return 5
class Enterprise: def fee(self): return 50
```

Or, when shapes are closed and small, `match`-`case` over `Enum`:

```python
class Kind(StrEnum): BASIC = "basic"; PRO = "pro"; ENTERPRISE = "enterprise"

def fee(kind: Kind) -> int:
    match kind:
        case Kind.BASIC: return 0
        case Kind.PRO: return 5
        case Kind.ENTERPRISE: return 50
```

### Replace Nested Conditional with Guard Clauses

```python
# Before
def discount(user):
    if user is not None:
        if user.active:
            if user.years >= 5:
                return 0.2
            else: return 0.1
        else: return 0
    return 0

# After
def discount(user: User | None) -> float:
    if user is None or not user.active: return 0.0
    if user.years >= 5: return 0.2
    return 0.1
```

### Move Function to its Data (Tell, Don't Ask)

```python
# Before
if order.total - order.discount > 100: ...

# After
class Order:
    def net_total(self) -> Decimal:
        return self.total - self.discount

if order.net_total() > 100: ...
```

### Extract Class

When a class has two clusters of fields/methods that change for different reasons, split it. Keep the original as a thin facade if callers depend on it; deprecate gradually.

### Replace Inheritance with Composition

Default to composition. Inherit only when the subclass _is-a_ substitutable variant of the base. Mixins are fine for orthogonal capabilities; don't use inheritance for code reuse alone.

### Replace Magic with Named Constants / Enums

```python
# Before
if status == 2: ...

# After
class Status(IntEnum): PENDING = 1; ACTIVE = 2; CLOSED = 3
if status is Status.ACTIVE: ...
```

### Replace Exception with Result (where exceptions are control flow)

For _expected_ failure modes (validation, parse), return a typed result; reserve exceptions for _exceptional_ paths.

```python
@dataclass(frozen=True)
class Ok[T]:    value: T
@dataclass(frozen=True)
class Err:      message: str
Result = Ok[T] | Err

def parse_age(raw: str) -> Result[int]:
    if not raw.isdigit(): return Err("not a number")
    n = int(raw)
    if not 0 <= n <= 150: return Err("out of range")
    return Ok(n)
```

## Production-Readiness Checklist

A "production-ready" Python module exhibits:

- [ ] **Pure core, imperative shell.** Business logic is functions/classes free of I/O; I/O lives at the edges (CLI, HTTP handler, repo).
- [ ] **Dependencies injected**, not imported inside functions. The constructor or function signature reveals every collaborator.
- [ ] **Configuration via `BaseSettings`**, not module globals. No hard-coded URLs/paths/keys.
- [ ] **Structured logging** (`structlog`) at boundaries; no `print`. Log events, not prose.
- [ ] **Error hierarchy rooted in an `AppError`**; specific catches; `raise ... from e` to preserve causes.
- [ ] **Idempotency** for retryable operations (HTTP handlers, queue consumers): same input → same effect.
- [ ] **Timeouts on every outbound call** (`httpx.Timeout`, DB statement timeout). No unbounded waits.
- [ ] **Resource lifecycle** via `with` / async `async with` / lifespan handlers — never leaked sockets, files, sessions.
- [ ] **Concurrency boundaries explicit.** No mutable globals shared across tasks; use `contextvars` for request-scoped state.
- [ ] **Observability hooks**: request IDs, correlation IDs threaded through (`structlog.contextvars.bind_contextvars`).
- [ ] **Metrics & health endpoints** for long-running services (`/healthz`, `/readyz`).
- [ ] **Graceful shutdown**: signal handling, drain in-flight work, close pools.
- [ ] **Schema validation at every untrusted boundary** (`BaseModel`).
- [ ] **Tests**: unit (pure core), integration (real adapters with testcontainers), contract (against `Protocol`s).
- [ ] **Type-checked** with `ty`; CI fails on type errors.
- [ ] **Lint clean** with `ruff`; format enforced.
- [ ] **Versioned**, with `__version__` and a changelog. Public API listed in `__all__`.
- [ ] **No silent fallbacks** that mask failures (e.g., `except Exception: pass`).

## Anti-Patterns to Refactor Away

```python
# God object
class Manager:               # vague name = vague responsibility
    def do_everything(self): ...

# Hidden I/O
def total(order):
    user = db.query(User).get(order.uid)   # logic does DB
    return order.amount * user.discount

# Stringly-typed
def transition(state: str, event: str) -> str: ...
# → Enum + match

# Boolean flag explosion
def export(data, csv=False, json=False, pretty=False, gzip=False): ...
# → strategy / parameter object

# Wide except
try: do()
except Exception: pass
# → catch what you handle; let the rest crash fast

# Mutable default
def append(x, items=[]): items.append(x); return items
# → items: list | None = None; items = items or []

# Module globals as state
_cache = {}
def get(k): return _cache.get(k)
# → inject cache or use a class
```

## A Refactoring Session — Workflow

1. **Read the change request.** Decide: is this a refactor or a behavior change? If both, split.
2. **Pin behavior with tests.** Run them green. If absent, write characterization tests on observed I/O.
3. **Identify the dominant smell** (use the Smell Map). Pick the smallest fix.
4. **Apply one refactoring.** Prefer IDE rename/extract. Run tests. Commit.
5. **Repeat** until smells are gone or you hit diminishing returns. Stop before over-engineering.
6. **Review the diff for new smells you introduced** (helper sprawl, premature interfaces). Inline back if so.
7. **Update docs** only when behavior, public API, or invariants changed — not for internal moves.

## When NOT to Refactor

- Code is about to be deleted.
- The smell is in a third-party-controlled boundary you can't own.
- You'd be introducing an abstraction with **one** caller. Wait for the third.
- Tests don't exist and writing them is out of scope — flag it, don't refactor blind.
- The "improvement" is taste, not a measurable maintainability gain.

## Quick Reference

| Goal                                     | First Move                               |
| ---------------------------------------- | ---------------------------------------- |
| Shrink a function                        | Extract Function under guard clauses     |
| Reduce parameters                        | Parameter Object                         |
| Kill `if isinstance` chains              | Polymorphism / `match` over `Enum`       |
| Test a function that calls the network   | Inject the client (Protocol)             |
| Test a function that uses `datetime.now` | Inject a `clock: Callable[[], datetime]` |
| Tame a god class                         | Extract Class along field clusters       |
| Remove a flag argument                   | Split Function by flag value             |
| Replace `None` sentinels                 | Null Object or non-optional + `Result`   |
| Decouple from globals                    | Pass settings/clients as arguments       |

**Refactor in small, reversible steps under green tests. Names first, structure second, abstractions last.**
