# MELT — Recommendations
> Generated 2026-07-02 by automated review (Fable 5). For human and AI-agent consumption.

## Current State
- Hexagonal skeleton is in place and matches the contract layout: `domain/core/` (IEmitter, IHarness, Harness), `domain/ports/` (EmitterNewRelic, EmitterSplunk), `domain/adaptors/` (MELTClient, MELTClientEnv, MELTClientConsul, MELTClientParamStore), `main.py` composition root, and a `tests/` tree mirroring layers.
- Everything below the skeleton is unimplemented: `EmitterNewRelic` raises `NotImplementedError` on both methods; `EmitterSplunk` posts a hardcoded test string; all four MELTClient adaptors are empty `pass` bodies; all 7 test files are **zero bytes**.
- README articulates a strong, coherent vision (vendor-agnostic emitter abstraction, runtime-tunable trace depth) but the Example and Visuals sections are empty.
- No packaging at all: no `pyproject.toml`, no `requirements.txt`, no `__init__.py` files, no CI. LICENSE exists.
- Last commit 2024-04-18 ("Fix some naming"); 3 commits total. Working tree clean.

## Recommended Changes
Prioritized path to a v0.1 PyPI release:

1. **Fix the interface bug (blocking, trivial).** `domain/core/IEmitter.py` and `domain/core/IHarness.py` declare `class IEmitter(ABCMeta)` / `class IHarness(ABCMeta)` — they subclass the *metaclass* instead of using it. Any real subclass will break. Change to `class IEmitter(abc.ABC)` with `@abstractmethod` (matches the owner's stated interface convention).
2. **Fix all imports.** Files import `from core.domain.X import X` and `main.py` imports `from MELT.core.adaptors...` / `from MELT.core.ports...`, but the tree is `domain/core|ports|adaptors`. Nothing in this repo is currently importable. Settle on a package name (`melt` is taken territory on PyPI — verify; consider `melt-harness` or `pymelt-obs`), create `src/<pkg>/` layout with `__init__.py`, and fix every import.
3. **Define the real emitter API.** `IEmitter` currently has only `configure()` and `trace_enable()` — it cannot express M, E, L, or T. Add the four verbs: `emit_metric(...)`, `emit_event(...)`, `emit_log(...)`, `start_span(...)/end_span(...)` (or a context-manager `trace()`), plus `configure()` and `shutdown()/flush()`.
4. **Define canonical dataclasses (contract requirement).** `MetricRecord`, `EventRecord`, `LogRecord`, `SpanRecord` in `domain/core/models.py`. These are the cartridge passed to every emitter; emitters translate canonical → vendor wire format, never the reverse.
5. **Write the tests first, then implement** (contract rule 1). Populate the 7 empty test files. Add `fixtures/raw/<emitter>/v1/` and `fixtures/expected/<emitter>/v1/` JSON — e.g. a canonical LogRecord fixture and the expected Splunk HEC envelope / OTLP payload it must serialize to. Mocks load fixtures, no inline JSON.
6. **Implement one real emitter end-to-end: OpenTelemetry.** Strategically the highest leverage — wrapping the OTEL SDK gives Datadog, New Relic, and most vendors for free via OTLP exporters, and makes the "vendor-agnostic" pitch credible. `domain/ports/EmitterOTEL.py`. Follow with `EmitterConsole` (stdlib-only, zero deps, great for tests/examples) and fix `EmitterSplunk`.
7. **Fix `EmitterSplunk.trace_enable`** while you're there: the headers dict `{"Authorization:" f"splunk {self.hec_token}"}` is an implicit string concatenation producing a single malformed key — should be `{"Authorization": f"Splunk {self.hec_token}"}`. Remove the hardcoded token/`main()` block from the port file.
8. **Packaging for v0.1:** `pyproject.toml` (hatchling or setuptools, `src/` layout), optional extras (`[otel]`, `[splunk]`), pinned minimum Python (3.10+), `README.md` as long description, version `0.1.0`, GitHub Actions workflow running tests + `twine check`, publish via trusted publishing.
9. **Example app** (README promises one, still "In progress"): `examples/fastapi_demo/` that wires `MELTClientEnv` + `EmitterConsole` in a composition root, showing the "swap emitters without touching app code" story.
10. **Add the Mermaid architecture diagram** to the README Visuals section (contract deliverable).

## Updates
- No dependency manifest exists; `EmitterSplunk` imports `requests` undeclared. Declare all deps in `pyproject.toml`.
- Hardcoded (dummy) HEC token string in `domain/ports/EmitterSplunk.py` — remove before publishing; even fake tokens trip secret scanners.
- Prefer `httpx` or keep `requests` pinned `>=2.32` (CVE-2024-35195 fixed there).
- Add ruff + mypy; the ABCMeta and import bugs above would have been caught immediately by mypy/CI.

## Premortem
1. **Published with broken imports/interfaces** — nothing is importable today; a rushed v0.1 upload would be dead on arrival and burn the package name.
2. **Reinventing OpenTelemetry instead of wrapping it** — hand-writing per-vendor emitters (Splunk raw HEC, New Relic REST) is a treadmill; OTEL already solved vendor transport. If MELT doesn't wrap OTEL it competes with it and loses.
3. **API churn after release** — `configure()/trace_enable()` doesn't cover metrics/events/logs; shipping v0.1 with that surface guarantees a breaking v0.2. Lock the four-verb canonical API before publishing.
4. **Zero tests rot** — with 7 empty test files, any contributor (human or agent) has no shared contract; blind multi-agent collaboration rules in AGENTS.md are impossible here.
5. **Two-year dormancy repeats** — no CI, no roadmap issues, no example app means nothing pulls the project forward; it stalls again after the next burst.

## Future Abilities
- **Runtime log/trace depth control** (already in the README vision) — the genuinely differentiating feature vs raw OTEL; pair `MELTClientConsul`/`MELTClientParamStore` with a watch loop so sampling/verbosity changes apply without restart.
- **Sibling integrations:** instrument `agent_supervisor`, `Agent-Tasks`/coordinator, and `slack_api` with MELT as first consumers — dogfooding produces the example apps and fixture payloads the contract requires.
- Emitter roadmap after OTEL/Console/Splunk: Datadog (via OTLP endpoint), CloudWatch EMF (fits `mission_lambda`/AWS estate), plain-file JSON emitter for air-gapped debugging.
- Decorator/context-manager sugar (`@melt.traced`, `with melt.span("...")`) built on the Harness.
- A2A/MCP documentation per the config hub's Required Documentation rule, so other agents can wire MELT unaided.

## Contract Alignment
- ✅ Folder layout matches hexagonal contract (core/ports/adaptors, composition in `main.py`, mirrored tests).
- ❌ Tests-first: all test files empty — the largest single contract violation in this repo.
- ❌ No `fixtures/raw/...` or `fixtures/expected/...` directories exist.
- ❌ No canonical dataclasses; emitters would receive ad hoc dicts (`data: dict`), violating the cartridge rule.
- ❌ Interfaces subclass `ABCMeta` instead of `abc.ABC` + `@abstractmethod`; naming (`IEmitter`, `IHarness`) is correct.
- ⚠️ Note: the contract's `adaptors` = inbound, `ports` = outbound convention **is** honored here (config-source clients inbound, emitters outbound) — keep it consistent as the repo grows.
- ❌ README lacks Mermaid diagrams; Example section unfinished (Required Documentation rule).
