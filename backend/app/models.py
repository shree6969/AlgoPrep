from pydantic import BaseModel
from typing import Any, Optional


class Example(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None


class TestCase(BaseModel):
    input_data: dict
    expected_output: Any


class VizStep(BaseModel):
    step_num: int
    description: str
    data: Any
    highlights: dict
    state: dict


class ExecutionResult(BaseModel):
    steps: list[VizStep]
    output: str
    passed: bool
    runtime_ms: float


class Problem(BaseModel):
    id: str
    title: str
    difficulty: str  # Easy / Medium / Hard
    pattern: str
    companies: list[str]
    description: str
    examples: list[Example]
    constraints: list[str]
    hints: list[str]
    solution_code: str
    time_complexity: str
    space_complexity: str
    viz_type: str  # array / tree / graph / grid / none


class ProblemListItem(BaseModel):
    id: str
    title: str
    difficulty: str
    pattern: str
    companies: list[str]
    viz_type: str
    solved: bool = False
