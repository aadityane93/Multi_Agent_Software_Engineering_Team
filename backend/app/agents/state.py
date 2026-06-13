from typing import TypedDict


class EngineeringState(TypedDict, total=False):
    run_id: str
    product_idea: str
    status: str

    requirements: str
    architecture: str

    approved: bool
    feedback: str

    backend_code: str
    frontend_code: str
    tests: str
    documentation: str
    review: str