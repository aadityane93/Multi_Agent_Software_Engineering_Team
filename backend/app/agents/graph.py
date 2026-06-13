from langgraph.graph import END, StateGraph

from app.agents.state import EngineeringState
from app.core.llm import generate_text


async def requirements_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Requirements Agent.

Convert this product idea into clear software requirements.

Product idea:
{state["product_idea"]}

Return:
1. Problem statement
2. Target users
3. Functional requirements
4. Non-functional requirements
5. Acceptance criteria
6. Open questions
"""
    output = await generate_text(prompt)
    return {"requirements": output, "status": "requirements_done"}


async def architecture_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Architecture Agent.

Design a practical architecture for this product.

Product idea:
{state["product_idea"]}

Requirements:
{state["requirements"]}

Use this stack:
- LangGraph
- MCP
- FastAPI
- React
- Docker
- GitHub API
- PydanticAI
- Ollama local Gemma model
- Gemini API as cloud option

Return:
1. System architecture
2. Backend modules
3. Frontend modules
4. Agent workflow
5. Data models
6. API endpoints
7. Docker services
8. Risks and tradeoffs
"""
    output = await generate_text(prompt)
    return {"architecture": output, "status": "awaiting_approval"}


async def backend_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Backend Agent.

Generate a backend implementation plan and starter code snippets.

Product idea:
{state["product_idea"]}

Requirements:
{state["requirements"]}

Architecture:
{state["architecture"]}

Human feedback:
{state.get("feedback", "")}

Return:
1. FastAPI routes
2. Service layer
3. Agent orchestration layer
4. GitHub integration plan
5. Important code snippets
"""
    output = await generate_text(prompt)
    return {"backend_code": output, "status": "backend_done"}


async def frontend_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Frontend Agent.

Generate a React frontend implementation plan and starter components.

Product idea:
{state["product_idea"]}

Requirements:
{state["requirements"]}

Architecture:
{state["architecture"]}

Backend plan:
{state["backend_code"]}

Return:
1. Page structure
2. Components
3. API client functions
4. State management approach
5. Important code snippets
"""
    output = await generate_text(prompt)
    return {"frontend_code": output, "status": "frontend_done"}


async def test_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Test Agent.

Create a testing strategy for the generated backend and frontend.

Backend:
{state["backend_code"]}

Frontend:
{state["frontend_code"]}

Return:
1. Backend test cases
2. Frontend test cases
3. Agent workflow tests
4. Human approval tests
5. Suggested test files
"""
    output = await generate_text(prompt)
    return {"tests": output, "status": "tests_done"}


async def docs_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Documentation Agent.

Create user-facing and developer-facing documentation.

Product idea:
{state["product_idea"]}

Requirements:
{state["requirements"]}

Architecture:
{state["architecture"]}

Return:
1. README sections
2. Setup instructions
3. Usage instructions
4. Environment variables
5. Developer notes
"""
    output = await generate_text(prompt)
    return {"documentation": output, "status": "docs_done"}


async def reviewer_agent(state: EngineeringState) -> EngineeringState:
    prompt = f"""
You are the Reviewer Agent.

Review the proposed software system.

Requirements:
{state["requirements"]}

Architecture:
{state["architecture"]}

Backend:
{state["backend_code"]}

Frontend:
{state["frontend_code"]}

Tests:
{state["tests"]}

Docs:
{state["documentation"]}

Return:
1. Strengths
2. Weaknesses
3. Missing pieces
4. Security concerns
5. Final recommendation
"""
    output = await generate_text(prompt)
    return {"review": output, "status": "completed"}


def build_planning_graph():
    graph = StateGraph(EngineeringState)

    graph.add_node("requirements_agent", requirements_agent)
    graph.add_node("architecture_agent", architecture_agent)

    graph.set_entry_point("requirements_agent")
    graph.add_edge("requirements_agent", "architecture_agent")
    graph.add_edge("architecture_agent", END)

    return graph.compile()


def build_implementation_graph():
    graph = StateGraph(EngineeringState)

    graph.add_node("backend_agent", backend_agent)
    graph.add_node("frontend_agent", frontend_agent)
    graph.add_node("test_agent", test_agent)
    graph.add_node("docs_agent", docs_agent)
    graph.add_node("reviewer_agent", reviewer_agent)

    graph.set_entry_point("backend_agent")
    graph.add_edge("backend_agent", "frontend_agent")
    graph.add_edge("frontend_agent", "test_agent")
    graph.add_edge("test_agent", "docs_agent")
    graph.add_edge("docs_agent", "reviewer_agent")
    graph.add_edge("reviewer_agent", END)

    return graph.compile()


planning_graph = build_planning_graph()
implementation_graph = build_implementation_graph()


async def run_planning(product_idea: str) -> EngineeringState:
    initial_state: EngineeringState = {
        "product_idea": product_idea,
        "status": "started",
    }

    result = await planning_graph.ainvoke(initial_state)
    return result


async def run_implementation(
    state: EngineeringState,
    feedback: str | None = None,
) -> EngineeringState:
    next_state: EngineeringState = {
        **state,
        "approved": True,
        "feedback": feedback or "",
        "status": "approved",
    }

    result = await implementation_graph.ainvoke(next_state)
    return result