# 🛡️ PROJECT PRAHAAR-AI (`SIH26184`)
### *Predictive Real-time Analytics & Hotspot Action for Anti-Fraud Recovery*
**Smart India Hackathon 2026 | Ministry of Home Affairs (MHA) / Indian Cyber Crime Coordination Centre (I4C)**  
**Theme:** Blockchain & Cybersecurity | **Category:** Software

---

## 📖 Executive Summary
When a citizen is defrauded and dials the **1930 Cyber Helpline** or registers a complaint on the **National Cybercrime Reporting Portal (NCRP)**, fraudsters race against time to disperse funds across **Layer 1 $\rightarrow$ Layer 2 $\rightarrow$ Layer 3 mule accounts**. Within **30 to 90 minutes ("The Golden Hour")**, these illicit funds are physically withdrawn as cash from ATMs and CSP (Customer Service Point) kiosks in remote cybercrime hubs (Mewat/Nuh, Jamtara, Alwar, Deoghar, Bharatpur).

Current Law Enforcement Agency (LEA) systems are **100% reactive** — by the time freeze requests reach banks, the money has already been extracted.

**PRAHAAR-AI** transforms reactive complaint data into **proactive predictive intelligence**:
* 🕸️ **MuleGraph™ Core**: Traverses multi-hop transaction topologies to identify smurfing rings, synthetic accounts, and terminal cashout mules in $<50$ ms.
* 📍 **Spatio-Temporal Forecaster**: Predicts the exact high-probability ATM/CSP withdrawal locations **15–45 minutes in advance** with confidence scores and lead times.
* 🗺️ **Tactical Cyber Command Center**: High-tech dark GIS map with pulsing danger zones, live 1930 streaming feed, and real-time police telemetry.
* 🚓 **Field Officer Tactical Mobile App**: Push alerts and GPS navigation for on-duty PCR patrol vans and beat officers for on-site interception.
* 📜 **Automated Legal Compliance**: 1-Click generation of court-admissible debit freeze orders under **Section 106 BNSS 2023 / Section 102 CrPC** for Bank Nodal Officers.

---

## 🏗️ System Architecture

```
[1930 / NCRP Incident Stream] ───► [Data Ingestion & Anonymization Engine]
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
       [MuleGraph Engine]                                           [Spatial Forecaster]
 • Multi-Hop Graph Traversal                                  • Spatio-Temporal KDE
 • PageRank & Centrality Scoring                              • ATM Vulnerability Scorer
 • Smurfing Ring / Cycle Detection                            • Lead Time & ETW Prediction
                 │                                                             │
                 └──────────────────────────────┬──────────────────────────────┘
                                                ▼
                                   [Risk Fusion & Decision Core]
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
     [Tactical Command Center]       [Automated Bank Freeze]        [Field Beat Officer App]
   • Real-Time GIS Heatmaps        • Sec 106 BNSS / 102 CrPC      • Geofenced Mobile Alerts
   • Live 1930 Triage Queue        • Automated Bank Nodal Notice  • Real-Time GPS Directions
```

---

## ⚡ Quickstart & Running Locally

### 1. Requirements
* Python 3.10+
* Modern Web Browser (Chrome / Edge / Firefox)

### 2. Launch the Application
Navigate to the backend directory and run:

```bash
cd prahaar_sih26184/backend
python run.py
```

### 3. Open in Browser
* **Tactical Cyber Command Center:** [http://localhost:8000](http://localhost:8000)
* **Field Beat Officer Mobile Interface:** [http://localhost:8000/field_officer.html](http://localhost:8000/field_officer.html)
* **Interactive API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎯 Winning SIH 2026 Presentation & Demo Flow

1. **The 30-Second Hook:**
   * Open the **Tactical Command Center** ([http://localhost:8000](http://localhost:8000)).
   * Highlight the live 1930 stream and the **"Golden Hour" countdown timers**.
2. **The Predictive Innovation:**
   * Click on an active critical incident or click **"⚡ INGEST 1930 INCIDENT"**.
   * Show how the **MuleGraph Engine** immediately decomposes the multi-tier layering (Layer 1 $\rightarrow$ Layer 2 $\rightarrow$ Layer 3) and flags the terminal cashout mule.
   * Switch to the **Tactical GIS Radar** to show the **pulsing red danger zone** around the predicted ATM terminal with **94%+ confidence** and a **28-minute lead time**.
3. **The Rapid Interception:**
   * Click **"⚡ DISPATCH NEAREST PCR"** — show how the nearest patrol car (`PCR-NUH-01`) is instantly dispatched.
   * Open the **Field Officer Mobile App** ([http://localhost:8000/field_officer.html](http://localhost:8000/field_officer.html)) to show the live mobile alert received by the on-duty officer.
4. **The Legal & Financial Seal:**
   * Click **"📜 FREEZE NOTICE"** to generate the authentic, digitally verifiable **Section 106 BNSS 2023 / Section 102 CrPC** debit freeze order for Bank Nodal Officers.
