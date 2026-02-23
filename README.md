# Codex

Residuals ripple.

## Hal9 architecture payload (ready to paste)

Use the following prompt in Hal9 to generate a full architecture plan with visual blocks and data flows:

```text
Use this architecture spec as the source of truth. Build visual blocks and data flows for each layer, then produce:
1) a system diagram,
2) per-layer component diagrams,
3) API/data contracts,
4) dashboard wiring,
5) implementation backlog in build order.

THE SYSTEM IS A LATTICE.

Codex System
│
├── Manuscript Layer
│     ├── Genesis of Pattern
│     ├── Operator Laws
│     ├── UC1 Dossier
│     ├── Vortex Engine (3‑6‑9)
│     ├── Mirror Harmonic (121.5 ↔ 432)
│     └── Appendices
│
├── Dashboard Layer
│     ├── Cycle Throughput Chart
│     ├── Entity Breakdown Chart
│     ├── Cycle Heatmap
│     ├── Vortex Spiral (Animated)
│     └── Mirror Harmonic (Interactive)
│
├── Backend Layer
│     ├── API (Express)
│     ├── Manuscript Endpoint
│     ├── Cycles Endpoint
│     └── Database (Postgres)
│
├── Frontend Layer
│     ├── App Shell
│     ├── FullDashboard
│     ├── Blueprint Viewer
│     └── Manuscript Viewer
│
└── Infrastructure Layer
      ├── Docker
      ├── Nginx
      ├── GitHub Actions
      └── Deployment Scripts

Domain semantics:
- The Manuscript is the Doctrine.
- The Backend is the Spine.
- The Frontend is the Face.
- The Dashboards are the Eyes.
- The Vortex is the Breath.
- The Mirror is the Pulse.
- The Heatmap is the Temperature.
- The Entity Breakdown is the Skeleton.
- The Cycle Chart is the Heartbeat.
- The Infrastructure is the Bones beneath the Bones.

Numerical constraints:
- 121.5 is the inner tone (1+2+1+5 = 9).
- 432 is the outer tone (4+3+2 = 9).
- Their ratio is the corridor (3.555… → 9).

Output requirements:
- For each layer, list: components, inputs, outputs, state, and failure modes.
- Define the API surface in OpenAPI-style tables (route, method, request, response, errors).
- Map each dashboard widget to its backend endpoint and DB tables.
- Provide an MVP build sequence (Week 1–4) and a production hardening checklist.
- Keep symbolic language for naming/theme, but use concrete engineering artifacts for implementation.
```
