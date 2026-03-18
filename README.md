# AlgoPrep — Coding Interview Prep Platform

An interactive algorithm study platform targeting senior/staff engineer interviews at top tech companies. Browse 57 curated problems organized by pattern, read real Python solutions, and step through animated visualizations that show exactly how each algorithm executes.

---

## Features

- **57 problems** across 14 patterns, weighted toward Medium/Hard (only 3 Easy)
- **Interactive visualizations** — step through array, grid (DP/backtracking), tree, and graph algorithms frame by frame
- **11 animated algorithms** with full step-by-step execution traces
- **Company filter** — surface problems asked at Google, Meta, Amazon, Airbnb, Netflix, and more
- **CodeMirror editor** — Python syntax highlighting with toggleable solution reveal
- **Custom inputs** — supply your own test case and re-run the visualization
- **Pattern reference page** — descriptions and problem counts for every pattern

---

## Problem Coverage

### By Pattern

| Pattern | Problems | Difficulty |
|---|---|---|
| Two Pointers | 4 | 1 Easy, 3 Medium/Hard |
| Sliding Window | 4 | 2 Medium, 2 Hard |
| Binary Search | 5 | 4 Medium, 1 Hard |
| Dynamic Programming 1D | 6 | 4 Medium, 2 Hard |
| Dynamic Programming 2D | 4 | 2 Medium, 2 Hard |
| Trees | 6 | 2 Medium, 4 Hard |
| Graph Traversal | 6 | 3 Medium, 3 Hard |
| Heap / Priority Queue | 5 | 3 Medium, 2 Hard |
| Backtracking | 4 | 2 Medium, 2 Hard |
| Monotonic Stack | 3 | 1 Medium, 2 Hard |
| Intervals | 4 | 3 Medium, 1 Hard |
| Trie | 1 | Hard |
| Union Find | 3 | Medium |
| System Design Coding | 2 | 1 Medium, 1 Hard |

### Top Companies Covered

Google · Meta · Amazon · Microsoft · Airbnb · Apple · Netflix · Uber · LinkedIn

---

## Interactive Visualizations

11 problems have full step-by-step animated execution:

| Problem | Type | Steps (default input) |
|---|---|---|
| Container With Most Water | Array / two pointers | 18 |
| Trapping Rain Water | Array / two pointers | 13 |
| Minimum Window Substring | Array / sliding window | 25 |
| Search in Rotated Sorted Array | Array / binary search | 9 |
| Longest Increasing Subsequence | Array / DP | 30 |
| Coin Change | Grid / DP table | 19 |
| Edit Distance | Grid / 2D DP table | 17 |
| Largest Rectangle in Histogram | Array / monotonic stack | 14 |
| Merge Intervals | Array / intervals | 7 |
| N-Queens | Grid / backtracking | 80 |
| Unique Paths | Grid / DP table | 12 |

Visualization controls: **Prev · Play/Pause · Next · Reset** with adjustable playback speed (0.5×–3×) and a per-step description panel.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend language | Python 3.11+ |
| Backend framework | FastAPI |
| Package manager | Poetry |
| Data validation | Pydantic v2 |
| Frontend framework | React 18 + TypeScript |
| Frontend build | Vite 5 |
| Styling | Tailwind CSS |
| Code editor | CodeMirror 6 (`@uiw/react-codemirror`) |
| Routing | React Router v6 |
| HTTP client | Axios |

---

## Setup

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Node.js 18+ and npm

### 1. Clone / navigate to the project

```bash
cd algo_platform
```

### 2. Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs (Swagger UI): `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at `http://localhost:5173`.
Vite proxies all `/api` requests to the backend, so no CORS configuration is needed during development.

### One-command start (both servers)

```bash
./start.sh
```

This starts both processes and prints their URLs. Press `Ctrl+C` to stop both.

---

## Project Structure

```
algo_platform/
├── start.sh                        # Convenience script to start both servers
├── backend/
│   ├── pyproject.toml              # Poetry dependencies
│   └── app/
│       ├── main.py                 # FastAPI app, CORS config
│       ├── models.py               # Pydantic models (Problem, VizStep, etc.)
│       ├── problems_data.py        # All 57 problem definitions + solutions
│       ├── executor.py             # Visualization step generators
│       └── routers/
│           └── problems.py         # REST API routes
└── frontend/
    ├── vite.config.ts              # Vite config with /api proxy
    └── src/
        ├── App.tsx                 # Router setup
        ├── types.ts                # TypeScript interfaces
        ├── api.ts                  # Axios API client
        ├── pages/
        │   ├── HomePage.tsx        # Landing page with pattern grid
        │   ├── ProblemsPage.tsx    # Filterable problem list
        │   ├── ProblemPage.tsx     # 3-panel problem solver
        │   └── PatternsPage.tsx    # Pattern reference
        └── components/
            ├── Layout.tsx
            ├── Sidebar.tsx         # Pattern/difficulty/company filters
            ├── CodeEditor.tsx      # CodeMirror Python editor
            ├── DifficultyBadge.tsx
            ├── PatternBadge.tsx
            ├── ProblemCard.tsx
            └── Visualizer/
                ├── index.tsx           # Dispatcher (picks sub-visualizer by viz_type)
                ├── StepControls.tsx    # Play/Pause/Prev/Next + speed slider
                ├── ArrayVisualizer.tsx # SVG boxes/bars with pointer labels
                ├── GridVisualizer.tsx  # 2D DP tables + N-Queens board
                ├── TreeVisualizer.tsx  # SVG binary tree layout
                └── GraphVisualizer.tsx # Graph state display
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/problems` | List problems. Query params: `pattern`, `difficulty`, `company`, `search`, `skip`, `limit` |
| `GET` | `/api/problems/{id}` | Full problem detail including solution code |
| `GET` | `/api/problems/{id}/solution` | Solution code only |
| `POST` | `/api/problems/{id}/execute` | Run visualization. Body: `{ "input": { ... } }` |
| `GET` | `/api/patterns` | All patterns with problem counts and descriptions |
| `GET` | `/api/companies` | All companies with problem counts |

### Execute endpoint input formats

```jsonc
// Container With Most Water / Trapping Rain Water
{ "input": { "height": [1, 8, 6, 2, 5, 4, 8, 3, 7] } }

// Minimum Window Substring
{ "input": { "s": "ADOBECODEBANC", "t": "ABC" } }

// Search in Rotated Sorted Array
{ "input": { "nums": [4, 5, 6, 7, 0, 1, 2], "target": 0 } }

// Coin Change
{ "input": { "coins": [1, 2, 5], "amount": 11 } }

// Edit Distance
{ "input": { "word1": "horse", "word2": "ros" } }

// Largest Rectangle in Histogram
{ "input": { "heights": [2, 1, 5, 6, 2, 3] } }

// Merge Intervals
{ "input": { "intervals": [[1,3],[2,6],[8,10],[15,18]] } }

// N-Queens (capped at n=6 for visualization)
{ "input": { "n": 4 } }
```

---

## Adding a New Problem

1. **Define the problem** in `backend/app/problems_data.py` — add a `Problem(...)` entry to the `PROBLEMS` list with id, title, pattern, difficulty, companies, description, examples, constraints, solution code, and `viz_type`.

2. **(Optional) Add visualization** in `backend/app/executor.py` — write a step-generator function and add a branch in `execute_problem()` matching your problem's id.

3. The frontend picks up new problems automatically via the API — no frontend changes needed.
