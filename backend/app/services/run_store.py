from uuid import uuid4

from app.agents.state import EngineeringState

_RUNS: dict[str, EngineeringState] = {}


def create_run(state: EngineeringState) -> EngineeringState:
    run_id = str(uuid4())
    state["run_id"] = run_id
    _RUNS[run_id] = state
    return state


def get_run(run_id: str) -> EngineeringState | None:
    return _RUNS.get(run_id)


def update_run(run_id: str, state: EngineeringState) -> EngineeringState:
    state["run_id"] = run_id
    _RUNS[run_id] = state
    return state