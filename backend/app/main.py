from fastapi import FastAPI

app = FastAPI(
    title="Multi-Agent Software Engineering Team",
    description="LangGraph-powered multi-agent software engineering backend",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}