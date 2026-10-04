import json
from pathlib import Path
from typing import List, Dict, Optional
from app.config import ATM_DATA_FILE
from app.models.schemas import CyberComplaint

class InMemoryDB:
    def __init__(self):
        self.complaints: Dict[str, CyberComplaint] = {}
        self.atms: List[Dict] = []
        self.pcr_units: List[Dict] = [
            {"unit_id": "PCR-NUH-01", "name": "Nuh Sector 1 Patrol", "driver": "SI Vikram Singh", "phone": "+91-98765-43210", "lat": 28.1090, "lng": 77.0150, "status": "AVAILABLE"},
            {"unit_id": "PCR-NUH-02", "name": "Tauru Highway QRT", "driver": "ASI Rakesh Meena", "phone": "+91-98765-43211", "lat": 28.1150, "lng": 77.0220, "status": "AVAILABLE"},
            {"unit_id": "PCR-JAM-01", "name": "Jamtara Town PCR", "driver": "SI Amit Kumar", "phone": "+91-98765-43212", "lat": 23.9650, "lng": 86.8050, "status": "AVAILABLE"},
            {"unit_id": "PCR-DEO-01", "name": "Deoghar Cyber Taskforce", "driver": "Inspector Rajesh Jha", "phone": "+91-98765-43213", "lat": 24.4800, "lng": 86.7020, "status": "AVAILABLE"},
            {"unit_id": "PCR-ALW-01", "name": "Alwar Border Squad", "driver": "SI Deepak Yadav", "phone": "+91-98765-43214", "lat": 27.8150, "lng": 76.7300, "status": "AVAILABLE"},
            {"unit_id": "PCR-DEL-01", "name": "Delhi Special Cell Mobile 4", "driver": "SI Manoj Sharma", "phone": "+91-98765-43215", "lat": 28.5510, "lng": 77.2500, "status": "AVAILABLE"}
        ]
        self.load_atms()

    def load_atms(self):
        if ATM_DATA_FILE.exists():
            try:
                with open(ATM_DATA_FILE, "r", encoding="utf-8") as f:
                    self.atms = json.load(f)
            except Exception:
                self.atms = []
        else:
            self.atms = []

    def get_complaint(self, complaint_id: str) -> Optional[CyberComplaint]:
        return self.complaints.get(complaint_id)

    def save_complaint(self, complaint: CyberComplaint):
        self.complaints[complaint.complaint_id] = complaint

    def get_all_complaints(self) -> List[CyberComplaint]:
        return sorted(self.complaints.values(), key=lambda c: c.reported_at, reverse=True)

    def get_all_atms(self) -> List[Dict]:
        return self.atms

    def get_pcr_units(self) -> List[Dict]:
        return self.pcr_units

db = InMemoryDB()
