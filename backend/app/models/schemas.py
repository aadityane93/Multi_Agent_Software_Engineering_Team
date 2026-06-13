from pydantic import BaseModel, Field


class ProductIdeaRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10)


class ApprovalRequest(BaseModel):
    feedback: str | None = None


class RejectRequest(BaseModel):
    reason: str | None = None


class AgentArtifact(BaseModel):
    name: str
    content: str


class RunResponse(BaseModel):
    run_id: str
    status: str
    product_idea: str
    artifacts: list[AgentArtifact]