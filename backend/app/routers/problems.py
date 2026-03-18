from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models import Problem, ProblemListItem, ExecutionResult, VizStep
from app.problems_data import get_all_problems, get_problem_by_id, get_patterns, get_companies
from app.executor import execute_problem
import time

router = APIRouter(prefix="/api", tags=["problems"])


@router.get("/problems", response_model=list[ProblemListItem])
def list_problems(
    pattern: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    problems = get_all_problems()

    if pattern:
        problems = [p for p in problems if p.pattern.lower() == pattern.lower()]
    if difficulty:
        problems = [p for p in problems if p.difficulty.lower() == difficulty.lower()]
    if company:
        problems = [p for p in problems if company.lower() in [c.lower() for c in p.companies]]
    if search:
        q = search.lower()
        problems = [p for p in problems if q in p.title.lower() or q in p.pattern.lower()]

    items = [
        ProblemListItem(
            id=p.id,
            title=p.title,
            difficulty=p.difficulty,
            pattern=p.pattern,
            companies=p.companies,
            viz_type=p.viz_type,
            solved=False,
        )
        for p in problems
    ]
    return items[skip : skip + limit]


@router.get("/problems/{problem_id}", response_model=Problem)
def get_problem(problem_id: str):
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{problem_id}' not found")
    # Return problem without solution code
    return problem


@router.get("/problems/{problem_id}/solution")
def get_solution(problem_id: str):
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{problem_id}' not found")
    return {"id": problem_id, "solution_code": problem.solution_code}


@router.post("/problems/{problem_id}/execute", response_model=ExecutionResult)
def execute(problem_id: str, body: dict):
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{problem_id}' not found")

    input_data = body.get("input", {})
    t0 = time.time()
    steps, output, passed = execute_problem(problem_id, input_data)
    runtime_ms = (time.time() - t0) * 1000

    return ExecutionResult(
        steps=steps,
        output=output,
        passed=passed,
        runtime_ms=round(runtime_ms, 2),
    )


@router.get("/patterns")
def list_patterns():
    pattern_counts = get_patterns()
    pattern_descriptions = {
        "Two Pointers": "Use two indices to traverse an array from both ends or at different speeds.",
        "Sliding Window": "Maintain a window of elements and slide it through the array.",
        "Binary Search": "Divide and conquer on sorted data to find elements in O(log n).",
        "Dynamic Programming 1D": "Break problems into overlapping subproblems with 1D memoization.",
        "Dynamic Programming 2D": "Solve problems requiring 2D state tables for optimal substructure.",
        "Trees": "Traverse and manipulate binary trees using DFS/BFS.",
        "Graph Traversal": "BFS/DFS on graphs, topological sort, shortest paths.",
        "Heap / Priority Queue": "Efficiently maintain min/max elements with a heap.",
        "Backtracking": "Explore all possibilities and backtrack when constraints are violated.",
        "Monotonic Stack": "Use a stack that maintains monotonic order to solve span/range problems.",
        "Trie": "Prefix tree for efficient string storage and retrieval.",
        "Union Find": "Track connected components with efficient union and find operations.",
        "System Design Coding": "Implement data structures like LRU cache with specific complexity requirements.",
        "Intervals": "Merge, sort, and reason about ranges of values.",
    }
    return [
        {
            "name": pattern,
            "count": count,
            "description": pattern_descriptions.get(pattern, ""),
        }
        for pattern, count in sorted(pattern_counts.items())
    ]


@router.get("/companies")
def list_companies():
    company_counts = get_companies()
    return [
        {"name": company, "count": count}
        for company, count in sorted(company_counts.items(), key=lambda x: -x[1])
    ]
