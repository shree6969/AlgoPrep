from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import problems
from app.routers import security
import uvicorn

app = FastAPI(
    title="AlgoPrep API",
    description="Algorithm study platform for L7/L8 interviews",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems.router)
app.include_router(security.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
