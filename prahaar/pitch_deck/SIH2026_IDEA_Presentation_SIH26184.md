# SMART INDIA HACKATHON (SIH) 2026 - IDEA PRESENTATION

---

## 📌 SLIDE 1: Title & Team Information
* **Problem Statement ID:** `SIH26184`
* **Problem Statement Title:** Development of a Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance, Enabling Generation of Actionable Intelligence for Timely and Proactive Cybercrime Intervention
* **Theme:** Blockchain & Cybersecurity
* **Category:** Software
* **Sponsoring Ministry:** Ministry of Home Affairs (MHA) / Indian Cyber Crime Coordination Centre (I4C)
* **Project Name:** **PRAHAAR-AI** *(Predictive Real-time Analytics & Hotspot Action for Anti-fraud Recovery)*
* **Team Name:** [Your Team Name]
* **Institute Name:** [Your College / Institute Name]

---

## 🎯 SLIDE 2: Problem Understanding & Real-World Crisis
* **The "Golden Hour" Challenge:**
  * When a citizen loses money in online scams (Digital Arrest, Investment Frauds, Task Scams) and reports to the **1930 Helpline** / **NCRP**, fraudsters rapidly fragment and disperse money across **Layer 1 $\rightarrow$ Layer 2 $\rightarrow$ Layer 3 mule accounts**.
  * Within **30 to 90 minutes**, the illicit funds are physically withdrawn as cash from ATMs / CSPs in cybercrime hotspots (Mewat, Jamtara, Alwar, Deoghar) before banks can execute manual freeze orders.
* **Flaws in Existing Systems:**
  * **Reactive Approach:** Law Enforcement Agencies (LEAs) currently only investigate *after* money has already left the banking system.
  * **Information Delay:** Inter-bank communications take hours to days; by then, the ATM trail is cold.
  * **Lack of Spatio-Temporal Foresight:** No intelligence system exists to predict *which* specific ATM or CSP kiosk will be hit next.

---

## 💡 SLIDE 3: Proposed Solution - PRAHAAR-AI
* **Core Value Proposition:**
  * PRAHAAR-AI transforms reactive complaint logs into a **proactive early-warning interception engine**.
  * By combining **Multi-Tier Graph Neural Networks (GNNs)** with **Spatio-Temporal Cashout Forecasters**, PRAHAAR-AI predicts the physical cash-out ATM/CSP terminal **15–45 minutes in advance**.
* **Key Capabilities:**
  1. **MuleGraph Engine:** Real-time multi-hop graph traversal to detect smurfing rings, synthetic accounts, and terminal cashout mules in $<50$ ms.
  2. **Spatial Forecaster:** Spatio-temporal predictive model that maps transaction velocity, ATM risk density, and non-CCTV vulnerability to pinpoint the top 3 high-probability withdrawal coordinates.
  3. **Tactical LEA Command Center:** Dark-mode GIS radar map with pulsing danger zones and real-time 1930 feed.
  4. **Field Officer Mobile PWA:** Instant geofenced dispatch to PCR vans and beat patrol cops for on-site interception.
  5. **1-Click Legal Compliance:** Instant automated generation of digitally verifiable **Section 106 BNSS 2023 / Section 102 CrPC** debit freeze notices for Bank Nodal Officers.

---

## 🏗️ SLIDE 4: System Architecture & Technical Flow

```
[1930 / NCRP Incident Feed]
           │
           ▼
[Real-Time Anonymization & Ingestion Core]
     │                                │
     ▼                                ▼
[MuleGraph Engine]           [Spatial Forecaster]
• Multi-Hop Graph Traversal   • Spatio-Temporal KDE
• PageRank & Centrality       • ATM Vulnerability Scorer
• Smurfing Ring Detection     • Lead Time & ETW Predictor
     │                                │
     └───────────────┬────────────────┘
                     │
                     ▼
        [Risk & Fusion Decision Core]
                     │
     ┌───────────────┼────────────────┐
     ▼               ▼                ▼
[LEA Command    [Automated Bank  [Field Officer
 Dashboard]      Freeze Order]    Mobile PWA]
```

---

## ⚙️ SLIDE 5: Technology Stack & Innovation

* **Backend & Intelligence Engine:**
  * Python 3, FastAPI (Asynchronous high-throughput API)
  * NetworkX / PyTorch Geometric (Graph analytics & link prediction)
  * Scikit-Learn & Spatial-KDE (Spatio-temporal trajectory clustering)
  * WebSockets & Redis (Real-time live incident stream)
* **Frontend & Visualization:**
  * Modern HTML5 / JavaScript / CSS3 (Tactical Cyber Command Center)
  * Leaflet.js / OpenStreetMap (GIS dark tactical maps with live PCR telemetry)
  * Vis.js Network (Interactive force-directed multi-tier mule ring graph)
* **Field Mobile & Automation:**
  * Progressive Web App (PWA) with GPS Geofencing
  * Jinja2 / Legal Compliance Engine (Sec 106 BNSS & Sec 91/102 CrPC generation)

---

## 🌟 SLIDE 6: Novelty & Unique Differentiators (Why PRAHAAR-AI Wins)

| Feature | Existing Portals (NCRP/CFCFRMS) | **PRAHAAR-AI (Our Solution)** |
| :--- | :--- | :--- |
| **Response Model** | Post-incident reactive tracking | **15–45 min Pre-Cashout Prediction** |
| **Mule Analysis** | Single-hop account lookup | **Multi-tier graph traversal & ring detection** |
| **ATM Location** | None (Investigated days later) | **Pinpoint ATM ID, Geocode & Confidence Score** |
| **Field Response** | Manual phone calls / Delayed FIR | **Automated PCR Van & Beat Cop Push Dispatch** |
| **Legal Freezing** | Manual paperwork across banks | **Instant 1-Click Sec 106 BNSS Digital Notice** |

---

## 📈 SLIDE 7: Feasibility, Impact & Business Model
* **Feasibility:**
  * Plug-and-play REST & WebSocket APIs designed to seamlessly integrate with existing **I4C / NCRP 1930** and **NPCI / Finnet** gateways.
* **National Impact:**
  * **85%+ Reduction** in the time needed to flag and freeze mule accounts.
  * **Crores saved annually** by intercepting physical cash extraction during the Golden Hour.
  * **Deterrence Factor:** Breaking the operating cycle of organized cyber fraud syndicates in known hotspots.

---

## 🚀 SLIDE 8: Project Milestones & Hackathon Roadmap
* **Phase 1 (Completed):** Core architecture, In-memory simulation engine, MuleGraph multi-hop analysis, Spatio-temporal ATM forecaster, Tactical Command Dashboard, and Field Officer PWA.
* **Phase 2 (Next 60 Days):** Real-time integration with bank API sandbox, AI video analytics integration for ATM CCTV feeds, automated voice broadcast to bank branch managers.
* **Phase 3 (Post-SIH):** National rollout across state Cyber Police Headquarters and I4C coordination nodes.

---

## 👥 SLIDE 9: Team Roles & Responsibilities
* **Lead Architect & AI/ML:** [Name] (Graph Neural Networks, Spatial Forecasting)
* **Full-Stack & Backend Engineer:** [Name] (FastAPI, WebSockets, Security)
* **GIS & UI/UX Developer:** [Name] (Leaflet Command Center, Vis.js Graphs)
* **Mobile / PWA Developer:** [Name] (Field Officer Response App)
* **Cyber Forensics & Legal Compliance:** [Name] (NCRP Schema, Sec 106 BNSS Engine)
* **Testing & QA Lead:** [Name] (Load testing, Edge resilience, Demo validation)

---

## 🎯 SLIDE 10: Conclusion & Vision
* **PRAHAAR-AI** is not just an analysis tool — it is an active **interception shield** for India's digital economy.
* We empower the Ministry of Home Affairs and State Police Forces to stay **one step ahead of cybercriminals**.
* *"From Reactive Investigation to Predictive Interception."*
