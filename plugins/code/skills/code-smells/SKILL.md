---
name: code-smells
description: Catalog of code-level smells with their fixes and, equally important, the false positives to suppress — correctness and robustness defects, bad practices and non-idiomatic constructs, duplication, dead weight, and complexity. Use when /code-sweep runs, when reviewing code for defects or bad practice, or when the user asks what to look for in a file. Covers implementations only — for interface, seam, and module-shape smells see codebase-design.
---

# Code Smells

Three lenses for finding what is wrong with code that already works. Each bucket lists **signals** (what to look for, and the fix) and **not a finding** (what to suppress).

**Scope: implementations.** Everything here lives inside a function body or a class's internals and is fixable without changing any caller's view of the module. The moment a fix would alter an **interface** — what callers must know — it belongs to `codebase-design` and `/refactor-interfaces`, not here.

The suppression lists matter as much as the signals. A sweep that reports 200 nitpicks gets ignored wholesale, and the false-positive rate is what decides whether the next sweep gets trusted.

A finding must be **real** (you read the code), **consequential** (you can name what goes wrong), **not already handled** (you checked the callers), and **not a lateral move** (the fix is clearly better, not differently-shaped).

---

## 1. Correctness & robustness

Code that already misbehaves, or will on plausible input. **Highest severity bucket** — findings here usually change behaviour.

### Signals

**Error handling**

- **Swallowed exception** — `except Exception: pass`, empty `catch {}`, an error logged at debug and then execution continues as if nothing happened. → Handle it, re-raise it, or let it propagate. If suppression is deliberate, narrow the exception type and comment *why*.
- **Over-broad catch** — a bare `except:` / `catch (e)` around a wide block, so a `KeyboardInterrupt`, typo-`AttributeError`, or unrelated failure is absorbed by handling written for one expected error. → Narrow the type; shrink the guarded block to the line that actually throws.
- **Wrong error semantics** — returning `None`, `-1`, `False`, or an empty collection to signal failure where the caller cannot distinguish it from a legitimate empty result. → Raise, or return an explicit result type.
- **Error message loses the cause** — re-raising without chaining (`raise ValueError("bad config")` discarding the original), or stringifying an exception into a log with no traceback. → Chain (`raise ... from e`), log with the exception attached.

**Absent-value and boundary handling**

- **Unchecked absence** — dereferencing something a documented path can leave `None`/`null`/absent; `dict[key]` where the key is optional; indexing a possibly-empty sequence. → Guard, or make absence unrepresentable at the type level.
- **Off-by-one / wrong bound** — `<` where `<=` is meant, `range(len(x) - 1)`, slice endpoints that silently drop the last element. → Fix, and name the input that exposes it.
- **Ignored partial failure** — a loop that continues after an item fails without recording which ones did, so callers see "success". → Collect and surface failures.

**Resources and state**

- **Unreleased resource** — file, socket, cursor, lock, or subprocess opened without `with` / `try…finally` / `defer`, so an exception leaks it. → Context manager or equivalent.
- **Mutable default argument** — `def f(items=[])` / `def f(cfg={})`. The default is created once and accumulates across calls. → `None` sentinel, build inside.
- **Mutable shared state** — module-level or class-level mutable containers mutated by instance methods or request handlers; a cached object handed to callers who mutate it. → Per-instance state, or hand out copies / immutable views.
- **Mutation during iteration** — adding to or deleting from a collection being iterated. → Iterate a copy, or build a new collection.
- **Time-of-check to time-of-use** — `if exists(p): open(p)`, `if not locked: lock()`. → Act and handle the failure, or use an atomic primitive.
- **Sync call in an async path** — blocking I/O or `time.sleep` inside a coroutine, stalling the event loop. → Async equivalent, or push to a thread/executor.

**Silent divergence**

- **Comment or docstring contradicts the code** — documented range, unit, return type, or raised exception that no longer matches. One of the two is a bug; find out which. → Correct whichever is wrong; never "fix" the comment without confirming intent.
- **Dead branch** — a condition that cannot be true (subsumed by an earlier check, comparing incompatible types, `if x is not None` after an unconditional assignment). → Delete, or fix the condition it was supposed to be.

### Not a finding

- A missing absence-check where **every call site** provably guarantees presence — check the callers before reporting.
- A broad `except` at a genuine top-level boundary (request handler, CLI entry point, worker loop) that **logs with traceback and reports failure** — that is the correct pattern.
- Defensive validation in a public API that looks redundant from inside the module.
- Anything requiring behaviour you cannot demonstrate from the code — if you must guess what a dependency does, say so or drop it.

---

## 2. Bad practices & idiom

Code that works but misleads readers, fights the language, or makes the next change harder. Behaviour-preserving.

### Signals

**Types and data shape**

- **Missing or lying annotations** — an un-annotated public function; `Any` used to silence a checker; an annotation that disagrees with what the body returns. A wrong annotation is worse than none. → Annotate honestly; if the real type is ugly, that is a design signal worth reporting.
- **Stringly-typed data** — statuses, kinds, keys, and modes as raw strings compared with `==` across many files; state packed into a delimited string and re-split downstream. → Enum, literal union, or a small type.
- **Primitive obsession** — a triple of `(x, y, unit)` or `(amount, currency)` threaded through many signatures; raw `dict` passed between layers as an implicit record. → A named type that keeps the fields together and validates once.
- **Boolean-flag parameter** — `f(data, True)` at the call site, or a flag selecting between two largely unrelated code paths inside the body. → Keyword-only at minimum; two functions when the paths barely overlap.
- **Illegal states representable** — several optional fields where only certain combinations are valid, enforced by scattered `if` checks. → Restructure so the invalid combination cannot be constructed.

**Language and stack idiom**

- **Reinvented stdlib / framework** — a hand-rolled grouping loop where the language has one call; manual retry/backoff, path joining, date parsing, or deep-merge the stack already provides. → Use the provided one.
- **Index-based iteration** over a collection whose items are all that is used; manual accumulator where a comprehension or fold reads better. → Idiomatic form, but only when genuinely clearer, not just shorter.
- **Print instead of logging** in library or application code; unstructured logging in a project that uses structured logging. → The project's logger, right level, context as fields.
- **String-built structured output** — SQL, JSON, HTML, shell commands, or paths assembled with `+` or f-strings. → Parameterized queries, serializers, `Path`, argument lists. *(If it is injection-prone it is also a security handoff — note both.)*
- **Bare magic value** — an unexplained numeric or string literal used in a decision, especially the same one in several places. → Named constant at the level that owns the meaning. A `0`, `1`, or `""` whose meaning is obvious needs no name.
- **Configuration read mid-logic** — `os.environ` reached deep inside a function, making the code untestable and its dependencies invisible. → Read at the edge, pass it in.

**Structure of the body**

- **Mixed levels of abstraction** — one function doing byte-fiddling and orchestration in the same twenty lines. → Extract the low level behind a name.
- **Output parameter / hidden mutation** — a function that mutates an argument and returns nothing, where its name suggests a computation. → Return the result, or rename so the mutation is expected.
- **Flag-then-act at a distance** — setting a variable in one branch and acting on it far below. → Act where the decision is made.

### Not a finding

- An established convention of **this** codebase, even if you would write it differently. Check `CONTEXT.md`, `CLAUDE.md`, ADRs, and neighbouring files first — consistency beats your preference.
- Idiom differences with no consequence: `%` vs `.format()` vs f-string in a log line, quote style, import ordering, anything the project's formatter or linter owns.
- Missing annotations in tests, scripts, or explicitly-throwaway code, unless the project types those too.
- Naming you merely dislike. Misleading is a finding; not-your-taste is not.
- A "magic number" in a well-named function whose whole purpose explains it.

---

## 3. Duplication, dead weight & complexity

Code that should not exist, or that costs too much to read. Behaviour-preserving, usually lower severity — **but the highest volume, so suppression discipline matters most here.**

### Signals

**Dead weight** — verify before deleting: grep the whole repo, and check for dynamic references (reflection, string-keyed dispatch, entry points, plugin registries, template lookups).

- **Unreachable or unused code** — a function, class, branch, or module with no callers; a parameter no caller passes and the body ignores; `if False`; code after an unconditional `return`.
- **Commented-out code** — delete it. Git has it.
- **Stale TODO/FIXME** — one referencing a shipped ticket, a resolved condition, or a person who has left. Resolve or delete; do not leave archaeology.
- **Unused imports, variables, assignments** — including a variable assigned then reassigned before any read. *(Skip if the linter already enforces this — no point reporting what CI reports.)*
- **Vestigial abstraction** — a config option nothing sets, a branch for a mode that no longer exists, a helper that forwards its arguments unchanged. When the fix is to delete a wrapper that callers go through, that changes an interface → hand to `/refactor-interfaces`.

**Duplication** — only report duplication that is genuinely the *same decision* expressed twice.

- **Copy-paste clone** — the same logic in two or more places, especially where the copies have already drifted (one was fixed, the others were not — that drift is the consequence to report). → Extract to one place.
- **Parallel maintenance burden** — adding a case requires editing several matching lists, switches, or mappings that must stay in sync. → Single source of truth.
- **Duplicated knowledge, not duplicated text** — the same regex, threshold, format string, or default repeated in code that otherwise looks different. → Shared constant.

**Complexity**

- **Long function** — one needing a scroll and a mental stack. Judge by number of distinct responsibilities, not line count. → Extract named steps.
- **Deep nesting** — three or more levels of conditional or loop, especially with the happy path innermost. → Guard clauses / early return to flatten.
- **Long parameter list** — many positional parameters, several of the same type, easy to transpose at a call site. → Group the ones that travel together. *(Changes the signature → check whether this is a `/refactor-interfaces` finding.)*
- **Feature envy** — a function reaching deep into another object's internals (`a.b.c.d`) to compute something that object should compute itself. → Move the behaviour to the data.
- **Misleading name** — a `get_*` that writes, a `validate_*` that mutates, a plural holding one item, a name whose stated unit or type is wrong. Rename **and update every call site**.
- **Temporal coupling** — two calls that must happen in a fixed order with nothing enforcing it. → One call that does both, or make the order impossible to get wrong.

### Not a finding

- **Coincidental similarity.** Two blocks that look alike but encode different decisions that will diverge. Merging these is the classic bad refactor — the wrong abstraction costs more than the duplication.
- **Duplication across a deliberate seam** — a test fixture mirroring production shape, a DTO mirroring a model, a vendored copy pinned on purpose.
- Two or three lines repeated twice, where extraction costs a name, an indirection, and a jump for the reader.
- A long function that is genuinely one linear sequence with no reusable middle — a parser, a state machine, a config assembler. Length alone is not a finding.
- Nesting inside a hot loop where flattening would change performance characteristics — measure first, or hand it off.
- Code that is verbose because it is **explicit**, and reads correctly at the point of use.
- A god object or grab-bag `utils.py`. Real, but splitting it moves seams → `/refactor-interfaces`.
