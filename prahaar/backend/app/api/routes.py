from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional
from app.models.schemas import CyberComplaint, DispatchRequest, FreezeNoticeRequest
from app.models.database import db
from app.core.ncrp_simulator import ncrp_simulator
from app.core.mule_graph import mule_graph_engine
from app.core.legal_notice import legal_notice_generator

router = APIRouter(prefix="/api")

@router.get("/stats")
def get_command_stats():
    complaints = db.get_all_complaints()
    total_complaints = len(complaints)
    total_defrauded = sum(c.total_defrauded_amount for c in complaints)
    intercepted_count = sum(1 for c in complaints if c.status in ["DISPATCHED", "INTERCEPTED", "FROZEN"])
    frozen_amount = sum(c.total_defrauded_amount for c in complaints if c.status in ["DISPATCHED", "FROZEN"])

    return {
        "active_incidents": total_complaints,
        "total_at_risk_amount": total_defrauded,
        "interceptions_active": intercepted_count,
        "amount_saved_golden_hour": frozen_amount,
        "average_etw_minutes": 28,
        "hotspot_accuracy_pct": 94.2
    }

@router.get("/complaints", response_model=List[CyberComplaint])
def list_complaints():
    return db.get_all_complaints()

@router.get("/complaints/{complaint_id}")
def get_complaint_detail(complaint_id: str):
    c = db.get_complaint(complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return c

@router.post("/complaints/generate")
def generate_sample_complaint(district: Optional[str] = Query(None)):
    complaint = ncrp_simulator.generate_incident(custom_district=district)
    db.save_complaint(complaint)
    return complaint

@router.get("/complaints/{complaint_id}/graph")
def get_complaint_graph(complaint_id: str):
    c = db.get_complaint(complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    analysis = mule_graph_engine.analyze_mule_network(c.mule_nodes, c.transaction_edges)
    return analysis

@router.post("/dispatch")
def dispatch_pcr(request: DispatchRequest):
    c = db.get_complaint(request.complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    c.status = "DISPATCHED"
    c.assigned_pcr_unit = request.pcr_unit_id

    # Update PCR status
    for unit in db.pcr_units:
        if unit["unit_id"] == request.pcr_unit_id:
            unit["status"] = "DISPATCHED"
            break

    db.save_complaint(c)
    return {
        "status": "SUCCESS",
        "message": f"PCR unit {request.pcr_unit_id} dispatched to ATM {request.atm_id}",
        "complaint": c
    }

@router.post("/freeze-notice")
def create_freeze_notice(request: FreezeNoticeRequest):
    c = db.get_complaint(request.complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")

    c.freeze_notice_generated = True
    c.status = "FROZEN"
    db.save_complaint(c)

    html_doc = legal_notice_generator.generate_freeze_notice_html(
        complaint=c,
        bank_name=request.bank_name,
        investigating_officer=request.investigating_officer,
        police_station=request.police_station
    )
    return HTMLResponse(content=html_doc, status_code=200)

@router.get("/atms")
def get_all_atms():
    return db.get_all_atms()

@router.get("/pcr-units")
def get_all_pcr():
    return db.get_pcr_units()
