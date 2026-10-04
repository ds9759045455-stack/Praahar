import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.ncrp_simulator import ncrp_simulator
from app.core.mule_graph import mule_graph_engine
from app.core.spatial_forecaster import spatial_forecaster
from app.core.legal_notice import legal_notice_generator

def test_ncrp_incident_generation():
    incident = ncrp_simulator.generate_incident("Nuh (Mewat)")
    assert incident.complaint_id.startswith("CMP-")
    assert incident.total_defrauded_amount > 0
    assert len(incident.mule_nodes) >= 3
    assert len(incident.transaction_edges) >= 2
    assert len(incident.predicted_hotspots) > 0

def test_mule_graph_analysis():
    incident = ncrp_simulator.generate_incident("Jamtara")
    analysis = mule_graph_engine.analyze_mule_network(incident.mule_nodes, incident.transaction_edges)
    assert analysis["node_count"] >= 3
    assert len(analysis["cashout_accounts"]) >= 1
    assert "vis_graph" in analysis

def test_spatial_forecasting():
    incident = ncrp_simulator.generate_incident("Nuh (Mewat)")
    hotspots = spatial_forecaster.forecast_cashout_hotspots(
        mule_nodes=incident.mule_nodes,
        total_amount=incident.total_defrauded_amount,
        target_district="Nuh (Mewat)"
    )
    assert len(hotspots) > 0
    assert hotspots[0].confidence_score >= 50.0
    assert hotspots[0].estimated_time_to_withdrawal_mins > 0

def test_legal_notice_generation():
    incident = ncrp_simulator.generate_incident("Deoghar")
    html_notice = legal_notice_generator.generate_freeze_notice_html(
        complaint=incident,
        bank_name="State Bank of India"
    )
    assert "SECTION 106 BNSS 2023" in html_notice
    assert incident.ack_number in html_notice
    assert "IMMEDIATE DEBIT FREEZE" in html_notice

def test_api_stats():
    with TestClient(app) as client:
        res = client.get("/api/stats")
        assert res.status_code == 200
        data = res.json()
        assert "active_incidents" in data
        assert "total_at_risk_amount" in data

def test_api_complaints_list():
    with TestClient(app) as client:
        res = client.get("/api/complaints")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_api_dispatch():
    with TestClient(app) as client:
        complaints = client.get("/api/complaints").json()
        target_c = complaints[0]
        atm_id = target_c["predicted_hotspots"][0]["atm_id"] if target_c["predicted_hotspots"] else "ATM-NUH-0101"
        
        payload = {
            "complaint_id": target_c["complaint_id"],
            "atm_id": atm_id,
            "pcr_unit_id": "PCR-NUH-01",
            "officer_name": "SI Vikram Singh",
            "officer_phone": "+91-98765-43210"
        }
        res = client.post("/api/dispatch", json=payload)
        assert res.status_code == 200
        assert res.json()["status"] == "SUCCESS"
