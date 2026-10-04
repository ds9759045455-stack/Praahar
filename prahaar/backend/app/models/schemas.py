from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MuleAccountNode(BaseModel):
    account_number: str
    holder_name: str
    bank_name: str
    ifsc_code: str
    branch_city: str
    layer_level: int = Field(..., description="1 for Entry Mule, 2 for Layering Aggregator, 3 for Cashout Mule")
    risk_score: float = Field(..., ge=0.0, le=1.0)
    current_balance: float
    status: str = "ACTIVE" # ACTIVE, FROZEN, SUSPECT
    kyc_risk: str = "HIGH" # LOW, MEDIUM, HIGH, SYNTHETIC

class TransactionEdge(BaseModel):
    tx_id: str
    from_account: str
    to_account: str
    amount: float
    timestamp: str
    channel: str # UPI, IMPS, RTGS, NEFT
    layer: int

class PredictedHotspot(BaseModel):
    atm_id: str
    bank_name: str
    location_name: str
    district: str
    state: str
    lat: float
    lng: float
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    estimated_time_to_withdrawal_mins: int
    interception_window_mins: int
    is_csp: bool = False
    recommended_police_station: str
    distance_from_hub_km: float

class CyberComplaint(BaseModel):
    complaint_id: str
    ack_number: str
    reported_at: str
    victim_name: str
    victim_city: str
    victim_state: str
    victim_phone: str
    fraud_type: str # Task Fraud, Investment Scam, Digital Arrest, Sextortion, Part-Time Job Scam
    total_defrauded_amount: float
    initial_beneficiary_upi: str
    initial_beneficiary_account: str
    status: str = "PROCESSING" # PROCESSING, PREDICTED, DISPATCHED, INTERCEPTED, FROZEN
    mule_nodes: List[MuleAccountNode] = []
    transaction_edges: List[TransactionEdge] = []
    predicted_hotspots: List[PredictedHotspot] = []
    golden_hour_remaining_mins: int = 60
    assigned_pcr_unit: Optional[str] = None
    freeze_notice_generated: bool = False

class DispatchRequest(BaseModel):
    complaint_id: str
    atm_id: str
    pcr_unit_id: str
    officer_name: str
    officer_phone: str
    notes: Optional[str] = ""

class FreezeNoticeRequest(BaseModel):
    complaint_id: str
    bank_name: str
    account_numbers: List[str]
    police_station: str
    investigating_officer: str
    act_section: str = "Section 102 CrPC / Section 106 BNSS 2023"
