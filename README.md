<h1 align="center">Juan Manuel Decoud</h1>

<p align="center">
  <b>Support &amp; Integrations Engineer at Darwin AI</b> · Computer Engineering @ Universidad Austral
</p>

<p align="center">
  <a href="https://decoudjuan.github.io"><img src="https://img.shields.io/badge/Portfolio-decoudjuan.github.io-10131a?style=flat-square" alt="Portfolio"></a>
  <a href="https://www.linkedin.com/in/decoudjuan/"><img src="https://img.shields.io/badge/LinkedIn-connect-0a66c2?style=flat-square" alt="LinkedIn"></a>
  <img src="https://img.shields.io/badge/Buenos_Aires-AR-6b7280?style=flat-square" alt="Buenos Aires, Argentina">
</p>

---

I build the unglamorous half of software: the integrations, the fallbacks and
the checks that decide whether a workflow still runs at 3 a.m. on a Tuesday.

Day to day that is n8n and Zapier pipelines against HubSpot, Salesforce and
Pipedrive at **Darwin AI**. On my own time it is shipped products — a Rust
security scanner, a precision-first playlist migrator, a desktop app that
replaced a legacy Access system in a real business — built to degrade
gracefully instead of failing loudly.

---

## Selected work

### 🎵 [Migratify](https://github.com/DecoudJuan/Migratify) · Python

Migrates playlists between Spotify and YouTube Music, in both directions, **without adding the wrong song.**

The same title exists as a cover, a karaoke track, a live take, a remix and as a completely different song by a completely different artist. Most migrators take the first search result and hand you a playlist that is quietly 15% wrong. Migratify scores candidates on artist, title, duration, album and result type, hard-vetoes wrong-artist and wrong-version matches, and when it still cannot tell two candidates apart it **asks instead of guessing**. Nothing is written until you run `apply`.

`weighted scoring` · `hard vetoes` · `review queue` · `SQLite cache` · `bidirectional`

### 🐝 [Wasp](https://github.com/DecoudJuan/Wasp) · Rust

An OWASP Top 10 auditor that walks a repository end to end.

A cheap, deterministic Rust harness sweeps the tree for vulnerable patterns, hardcoded secrets and vulnerable dependencies, then reports as SARIF so it drops straight into a CI annotation pipeline. Incremental mode rescans only the diff.

`rust` · `SAST` · `SARIF` · `secrets detection` · `incremental scanning`

### 🎼 [Agent-Orchestra](https://github.com/DecoudJuan/Agent-Orchestra) · Python

A coding agent built from scratch — a raw agentic loop, no frameworks.

An orchestrator coordinates specialised sub-agents (explorer, researcher, implementer, tester, reviewer) over an OpenAI-compatible API. Written to find out what an agent framework is actually doing under the abstraction, so everything between the LLM and its tools is visible and editable.

`agentic loop` · `multi-agent` · `tool calling` · `no frameworks`

### 🧾 [Vexa](https://github.com/DecoudJuan/Vexa) · Python

A desktop invoicing app that replaced a legacy Microsoft Access system, in production.

Clients, products and documents in PySide6 over SQLite. The Access migration is a one-time bootstrap step — at runtime the app depends on no ODBC driver and no Access install, which is the entire reason the replacement was worth doing.

`PySide6 / Qt` · `SQLite` · `legacy migration` · `PyInstaller`

### 🗺️ [Track Optimizer](https://github.com/DecoudJuan/TrackOptimizer) · JavaScript

Orders a list of stops into the shortest driving route. [**Live →**](https://googlemapsgigaoptimizer.vercel.app)

Google Maps routes stops in the order you type them; for a delivery round the *order* is the whole problem. Nearest-neighbour lands ~20–25% above optimal, so a 2-opt pass uncrosses the path and pulls it to within ~5%. Built on Leaflet, OpenStreetMap, Nominatim and OSRM, so it needs no billing account and runs the moment you clone it — one `index.html`, no build step.

### ⚔️ [Isometric God of War](https://github.com/DecoudJuan/isometric-god-of-war) · JavaScript

A Vampire Survivors-style roguelite in the God of War universe. [**Play →**](https://decoudjuan.github.io/isometric-god-of-war)

Isometric 2.5D, pixel art generated **100% in code**. No assets, no dependencies, no build — the entire game is one `index.html`.

`HTML5 Canvas` · `procedural pixel art` · `zero dependencies`

<sub>Also: <a href="https://github.com/DecoudJuan/ai-benchmarks-testing">ai-benchmarks-testing</a> — MMLU across 57 subjects plus agentic evaluation scored by an LLM judge · <a href="https://github.com/DecoudJuan/Mundialaustral">Mundialaustral</a> — match recommender for the Universidad Austral AI competition</sub>

---

## Stack

**Languages** — Python · TypeScript · Rust · Java · Kotlin · JavaScript · Embedded C

**AI &amp; Automation** — OpenAI API · prompt design · n8n · Zapier · webhooks

**Web** — React · NestJS · Flask · Express · Vite · PySide6 / Qt

**Data** — PostgreSQL · MySQL · SQLite · SQLAlchemy 2.0 · Prisma

**Cloud &amp; DevOps** — Azure · Docker · GitHub Actions · CI/CD · PyInstaller

**Integrations &amp; Auth** — HubSpot · Salesforce · Pipedrive · OAuth 2.0 · JWT · Auth0 · SOAP

---

<p align="center">
  <sub>Open to roles and freelance · <a href="https://decoudjuan.github.io">decoudjuan.github.io</a></sub>
</p>
