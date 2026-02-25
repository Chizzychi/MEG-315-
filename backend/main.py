# backend/main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import steam_state_points

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/process/{process_type}")
def get_process(
    process_type: str,
    T0: float = Query(300.0),
    V0: float = Query(1.0),
    n_points: int = Query(20)
):
    return steam_state_points(T0, V0, process_type, n_points)
