import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from app.models.schemas import CyberComplaint, MuleAccountNode, TransactionEdge
from app.core.mule_graph import mule_graph_engine
from app.core.spatial_forecaster import spatial_forecaster

FRAUD_TYPES = [
    "Digital Arrest / CBI Impersonation",
    "Telegram Part-Time Task Fraud",
    "Stock Trading / IPO Investment Scam",
    "Credit Card Reward Points Phishing",
    "Sextortion / Video Call Blackmail",
    "Electricity Bill Disconnection Fraud"
]

VICTIM_NAMES = [
    ("Sunil Sharma", "Noida", "Uttar Pradesh"),
    ("Priya Venkatesh", "Bengaluru", "Karnataka"),
    ("Rajesh Kulkarni", "Pune", "Maharashtra"),
    ("Ananya Mukherjee", "Kolkata", "West Bengal"),
    ("Dr. Mahendra Patel", "Ahmedabad", "Gujarat"),
    ("Harpreet Singh", "Chandigarh", "Punjab"),
    ("Kavita Nair", "Kochi", "Kerala"),
    ("Ramesh Babu", "Hyderabad", "Telangana")
]

MULE_NAMES = [
    "Aslam Khan", "Deepak Mandal", "Mubarak Ali", "Sukhdev Soren",
    "Raju Ansari", "Vikram Meena", "Imran Qureshi", "Santosh Das",
    "Mohd Farooq", "Chandan Kumar", "Akash Baisla", "Mintu Gorai"
]

BANKS = [
    ("State Bank of India", "SBIN000"),
    ("Punjab National Bank", "PUNB00"),
    ("Bank of Baroda", "BARB00"),
    ("Canara Bank", "CNRB00"),
    ("Airtel Payments Bank", "AIRP000"),
    ("Fino Payments Bank", "FINO000"),
    ("Union Bank of India", "UBIN000")
]

HOTSPOT_DISTRICTS = ["Nuh (Mewat)", "Jamtara", "Deoghar", "Alwar", "Bharatpur", "Delhi", "Bengaluru", "Mumbai"]

class NCRPSimulator:
    def __init__(self):
        pass

    def generate_incident(self, custom_district: str = None) -> CyberComplaint:
        """
        Generates a realistic multi-hop cybercrime complaint mimicking
        National Cybercrime Reporting Portal (1930) schema.
        """
        comp_num = random.randint(100000, 999999)
        ack_no = f"NCRP-2026-{comp_num}"
        complaint_id = f"CMP-{comp_num}"

        victim = random.choice(VICTIM_NAMES)
        fraud_type = random.choice(FRAUD_TYPES)
        total_amount = round(random.choice([185000, 320000, 475000, 750000, 1200000, 2400000]), 2)
        district = custom_district if custom_district else random.choice(HOTSPOT_DISTRICTS)

        # Generate Initial Fraud Entry VPA
        entry_vpa = f"merchant.pay{random.randint(10, 99)}@okaxis"
        entry_acc = f"91{random.randint(1000000000, 9999999999)}"

        now = datetime.now()
        reported_at = now.strftime("%Y-%m-%d %H:%M:%S")

        # Construct Multi-Tier Mule Topology (Layer 1 -> Layer 2 -> Layer 3)
        nodes: List[MuleAccountNode] = []
        edges: List[TransactionEdge] = []

        # Layer 1 Node (Entry Mule / Immediate receiver)
        l1_bank = random.choice(BANKS)
        l1_acc = f"{random.randint(20000000000, 99999999999)}"
        l1_name = random.choice(MULE_NAMES)
        node_l1 = MuleAccountNode(
            account_number=l1_acc,
            holder_name=l1_name,
            bank_name=l1_bank[0],
            ifsc_code=f"{l1_bank[1]}{random.randint(1000, 9999)}",
            branch_city=district,
            layer_level=1,
            risk_score=0.92,
            current_balance=round(total_amount * 0.05, 2), # 5% commission retained
            status="ACTIVE",
            kyc_risk="SYNTHETIC"
        )
        nodes.append(node_l1)

        # Layer 2 Nodes (Aggregators / Smurfing distribution)
        num_l2 = random.randint(2, 3)
        l2_split_amount = round((total_amount * 0.95) / num_l2, 2)
        l2_nodes = []

        for i in range(num_l2):
            l2_bank = random.choice(BANKS)
            l2_acc = f"{random.randint(20000000000, 99999999999)}"
            l2_name = random.choice(MULE_NAMES)
            node_l2 = MuleAccountNode(
                account_number=l2_acc,
                holder_name=l2_name,
                bank_name=l2_bank[0],
                ifsc_code=f"{l2_bank[1]}{random.randint(1000, 9999)}",
                branch_city=district,
                layer_level=2,
                risk_score=0.88,
                current_balance=round(l2_split_amount * 0.08, 2),
                status="ACTIVE",
                kyc_risk="HIGH"
            )
            nodes.append(node_l2)
            l2_nodes.append(node_l2)

            # Edge from Layer 1 -> Layer 2
            edges.append(TransactionEdge(
                tx_id=f"TXN-L12-{uuid.uuid4().hex[:6].upper()}",
                from_account=l1_acc,
                to_account=l2_acc,
                amount=l2_split_amount,
                timestamp=(now - timedelta(minutes=random.randint(12, 25))).strftime("%H:%M:%S"),
                channel=random.choice(["IMPS", "NEFT", "UPI"]),
                layer=1
            ))

        # Layer 3 Nodes (Terminal Cashout / ATM withdrawal mules)
        num_l3 = random.randint(2, 4)
        l3_amount_each = round((total_amount * 0.85) / num_l3, 2)

        for j in range(num_l3):
            l3_bank = random.choice(BANKS)
            l3_acc = f"{random.randint(20000000000, 99999999999)}"
            l3_name = random.choice(MULE_NAMES)
            node_l3 = MuleAccountNode(
                account_number=l3_acc,
                holder_name=l3_name,
                bank_name=l3_bank[0],
                ifsc_code=f"{l3_bank[1]}{random.randint(1000, 9999)}",
                branch_city=district,
                layer_level=3,
                risk_score=0.96,
                current_balance=l3_amount_each, # Full active balance awaiting ATM drain
                status="ACTIVE",
                kyc_risk="HIGH"
            )
            nodes.append(node_l3)

            # Connect from random Layer 2 node
            parent_l2 = random.choice(l2_nodes)
            edges.append(TransactionEdge(
                tx_id=f"TXN-L23-{uuid.uuid4().hex[:6].upper()}",
                from_account=parent_l2.account_number,
                to_account=l3_acc,
                amount=l3_amount_each,
                timestamp=(now - timedelta(minutes=random.randint(3, 10))).strftime("%H:%M:%S"),
                channel="IMPS",
                layer=2
            ))

        # Run Spatio-temporal ATM hotspot prediction
        predicted_hotspots = spatial_forecaster.forecast_cashout_hotspots(
            mule_nodes=nodes,
            total_amount=total_amount,
            target_district=district
        )

        complaint = CyberComplaint(
            complaint_id=complaint_id,
            ack_number=ack_no,
            reported_at=reported_at,
            victim_name=victim[0],
            victim_city=victim[1],
            victim_state=victim[2],
            victim_phone=f"+91-98{random.randint(10000000, 99999999)}",
            fraud_type=fraud_type,
            total_defrauded_amount=total_amount,
            initial_beneficiary_upi=entry_vpa,
            initial_beneficiary_account=entry_acc,
            status="PREDICTED",
            mule_nodes=nodes,
            transaction_edges=edges,
            predicted_hotspots=predicted_hotspots,
            golden_hour_remaining_mins=random.randint(48, 75)
        )

        return complaint

ncrp_simulator = NCRPSimulator()
