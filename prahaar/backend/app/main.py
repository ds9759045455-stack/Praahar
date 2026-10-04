import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.models.database import db
from app.core.ncrp_simulator import ncrp_simulator

# WebSocket Connection Manager for Live Radar & Alert Broadcasts
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Background Task to simulate realistic streaming incidents periodically
async def live_stream_simulation_task():
    while True:
        await asyncio.sleep(45) # Every 45s simulate a new 1930 NCRP incident
        try:
            new_complaint = ncrp_simulator.generate_incident()
            db.save_complaint(new_complaint)
            await manager.broadcast({
                "type": "NEW_INCIDENT",
                "complaint": new_complaint.model_dump()
            })
        except Exception as e:
            print(f"Simulation broadcast error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-seed initial 4 diverse incidents across key Indian hotspots if empty
    if len(db.complaints) == 0:
        districts = ["Nuh (Mewat)", "Jamtara", "Alwar", "Deoghar"]
        for dist in districts:
            comp = ncrp_simulator.generate_incident(custom_district=dist)
            db.save_complaint(comp)
    print(f"[PRAHAAR-AI] Initialized with {len(db.complaints)} live cybercrime incidents.")
    
    sim_task = asyncio.create_task(live_stream_simulation_task())
    yield
    sim_task.cancel()

app = FastAPI(
    title="PRAHAAR-AI | SIH26184",
    description="Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for local testing and cross-origin frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST Routes
app.include_router(router)

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "PONG", "message": "Connection active"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount Frontend static directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
