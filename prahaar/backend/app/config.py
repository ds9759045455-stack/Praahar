import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ATM_DATA_FILE = DATA_DIR / "indian_atm_csp_hotspots.json"

# Key Cybercrime Hotspot Hubs in India
HOTSPOT_DISTRICTS = {
    "Mewat_Nuh": {"center_lat": 28.1065, "center_lng": 77.0125, "radius_km": 35, "state": "Haryana"},
    "Jamtara": {"center_lat": 23.9632, "center_lng": 86.8015, "radius_km": 30, "state": "Jharkhand"},
    "Deoghar": {"center_lat": 24.4826, "center_lng": 86.6997, "radius_km": 25, "state": "Jharkhand"},
    "Alwar_Bharatpur": {"center_lat": 27.7500, "center_lng": 76.9000, "radius_km": 40, "state": "Rajasthan"},
    "Delhi_NCR": {"center_lat": 28.6139, "center_lng": 77.2090, "radius_km": 45, "state": "Delhi"},
    "Bengaluru": {"center_lat": 12.9716, "center_lng": 77.5946, "radius_km": 30, "state": "Karnataka"},
    "Mumbai_Thane": {"center_lat": 19.0760, "center_lng": 72.8777, "radius_km": 35, "state": "Maharashtra"},
}

# Average Cash Withdrawal Time Velocity (minutes from complaint to ATM withdrawal)
DEFAULT_LEAD_TIME_MINUTES = 32
GOLDEN_HOUR_LIMIT_MINUTES = 90

# High Risk Banks commonly targeted for Mule Accounts
COMMON_MULE_BANKS = [
    "State Bank of India", "Punjab National Bank", "Bank of Baroda",
    "Canara Bank", "Union Bank of India", "Airtel Payments Bank",
    "Paytm Payments Bank", "Fino Payments Bank", "Yes Bank", "IndusInd Bank"
]
