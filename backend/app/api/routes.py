from fastapi import APIRouter, HTTPException

from app.agents.graph import run_implementation, run_planning
from app.agents.state import EngineeringState
from app.models.schemas import (
    AgentArtifact,
    ApprovalRequest,
    ProductIdeaRequest,
    RejectRequest,
    RunResponse,
)
from app.services.run_store import create_run, get_run, update_run

router = APIRouter()


def state_to_response(state: EngineeringState) -> RunResponse:
    artifact_fields = [
        ("Requirements", "requirements"),
        ("Architecture", "architecture"),
        ("Backend Code", "backend_code"),
        ("Frontend Code", "frontend_code"),
        ("Tests", "tests"),
        ("Documentation", "documentation"),
        ("Review Report", "review"),
    ]

    artifacts = [
        AgentArtifact(name=name, content=str(state[key]))
        for name, key in artifact_fields
        if key in state and state[key]
    ]

    return RunResponse(
        run_id=state["run_id"],
        status=state.get("status", "unknown"),
        product_idea=state["product_idea"],
        artifacts=artifacts,
    )


@router.post("/runs", response_model=RunResponse)
async def start_run(payload: ProductIdeaRequest):
    product_idea = f"{payload.title}\n\n{payload.description}"

    planned_state = await run_planning(product_idea)
    saved_state = create_run(planned_state)

    return state_to_response(saved_state)


@router.get("/runs/{run_id}", response_model=RunResponse)
async def read_run(run_id: str):
    state = get_run(run_id)

    if not state:
        raise HTTPException(status_code=404, detail="Run not found")

    return state_to_response(state)


@router.post("/runs/{run_id}/approve", response_model=RunResponse)
async def approve_run(run_id: str, payload: ApprovalRequest):
    state = get_run(run_id)

    if not state:
        raise HTTPException(status_code=404, detail="Run not found")

    if state.get("status") != "awaiting_approval":
        raise HTTPException(
            status_code=400,
            detail=f"Run is not awaiting approval. Current status: {state.get('status')}",
        )

    completed_state = await run_implementation(state, feedback=payload.feedback)
    saved_state = update_run(run_id, completed_state)

    return state_to_response(saved_state)


@router.post("/runs/{run_id}/reject", response_model=RunResponse)
async def reject_run(run_id: str, payload: RejectRequest):
    state = get_run(run_id)

    if not state:
        raise HTTPException(status_code=404, detail="Run not found")

    state["status"] = "rejected"
    state["approved"] = False
    state["feedback"] = payload.reason or ""

    saved_state = update_run(run_id, state)

    return state_to_response(saved_state)