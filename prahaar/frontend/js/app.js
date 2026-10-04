class CyberCommandApp {
  constructor() {
    this.complaints = [];
    this.selectedComplaint = null;
    this.tacticalMap = null;
    this.graphVis = null;
    this.activeTab = 'map';
    this.ws = null;
  }

  async init() {
    // Initialize Map and Graph
    this.tacticalMap = new TacticalMap('map');
    this.tacticalMap.init();

    this.graphVis = new MuleGraphVisualizer('mule-network-graph');

    this.setupEventListeners();
    this.connectWebSocket();
    await this.fetchStats();
    await this.fetchComplaints();
  }

  connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/stream`;
    
    try {
      this.ws = new WebSocket(wsUrl);
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "NEW_INCIDENT") {
          this.handleNewIncidentStream(data.complaint);
        }
      };
      this.ws.onclose = () => {
        setTimeout(() => this.connectWebSocket(), 5000);
      };
    } catch (e) {
      console.warn("WebSocket stream fallback active", e);
    }
  }

  setupEventListeners() {
    // Tab Switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = btn.dataset.tab;
        this.switchTab(tab);
      });
    });

    // Simulate New Complaint Button
    const simBtn = document.getElementById('btn-simulate-ncrp');
    if (simBtn) {
      simBtn.addEventListener('click', () => this.simulateNewIncident());
    }

    // Modal Close
    const closeBtn = document.getElementById('modal-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        document.getElementById('freeze-modal').classList.remove('active');
      });
    }
  }

  switchTab(tab) {
    this.activeTab = tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
    
    const mapEl = document.getElementById('map-view');
    const graphEl = document.getElementById('graph-view');

    if (tab === 'map') {
      mapEl.style.display = 'block';
      graphEl.style.display = 'none';
      if (this.tacticalMap && this.tacticalMap.map) {
        setTimeout(() => this.tacticalMap.map.invalidateSize(), 100);
      }
    } else {
      mapEl.style.display = 'none';
      graphEl.style.display = 'block';
      if (this.selectedComplaint) {
        this.loadGraphView(this.selectedComplaint.complaint_id);
      }
    }
  }

  async fetchStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      document.getElementById('stat-active-incidents').textContent = data.active_incidents;
      document.getElementById('stat-at-risk-amount').textContent = `₹${(data.total_at_risk_amount / 100000).toFixed(2)}L`;
      document.getElementById('stat-saved-amount').textContent = `₹${(data.amount_saved_golden_hour / 100000).toFixed(2)}L`;
      document.getElementById('stat-avg-etw').textContent = `${data.average_etw_minutes}m`;
      document.getElementById('stat-accuracy').textContent = `${data.hotspot_accuracy_pct}%`;
    } catch (e) {
      console.warn("Could not fetch stats", e);
    }
  }

  async fetchComplaints() {
    try {
      const res = await fetch('/api/complaints');
      this.complaints = await res.json();
      this.renderIncidentFeed();

      if (this.complaints.length > 0) {
        this.selectIncident(this.complaints[0].complaint_id);
      }
    } catch (e) {
      console.error("Could not fetch complaints", e);
    }
  }

  renderIncidentFeed() {
    const listEl = document.getElementById('incident-list');
    listEl.innerHTML = '';

    this.complaints.forEach(c => {
      const item = document.createElement('div');
      item.className = `incident-item ${this.selectedComplaint && this.selectedComplaint.complaint_id === c.complaint_id ? 'active' : ''}`;
      item.onclick = () => this.selectIncident(c.complaint_id);

      const riskClass = c.total_defrauded_amount > 500000 ? 'risk-critical' : 'risk-high';
      const riskText = c.total_defrauded_amount > 500000 ? 'CRITICAL RISK' : 'HIGH RISK';

      item.innerHTML = `
        <div class="incident-top">
          <span class="incident-id">🚨 ${c.ack_number}</span>
          <span class="risk-pill ${riskClass}">${riskText}</span>
        </div>
        <div class="incident-amount">₹${c.total_defrauded_amount.toLocaleString('en-IN')}</div>
        <div class="incident-victim">${c.fraud_type} • Victim: ${c.victim_name} (${c.victim_city})</div>
        <div class="incident-timer">
          ⏳ Golden Hour Window: <strong>${c.golden_hour_remaining_mins} mins left</strong>
        </div>
      `;

      listEl.appendChild(item);
    });
  }

  async selectIncident(complaintId) {
    const c = this.complaints.find(x => x.complaint_id === complaintId);
    if (!c) return;

    this.selectedComplaint = c;
    this.renderIncidentFeed();
    this.renderIncidentDeepDive(c);

    // Update Map
    if (this.tacticalMap) {
      this.tacticalMap.renderIncidentHotspots(c);
    }

    // If graph tab is active, render graph
    if (this.activeTab === 'graph') {
      this.loadGraphView(complaintId);
    }
  }

  async loadGraphView(complaintId) {
    try {
      const res = await fetch(`/api/complaints/${complaintId}/graph`);
      const graphData = await res.json();
      this.graphVis.render(graphData);
    } catch (e) {
      console.warn("Could not load graph data", e);
    }
  }

  renderIncidentDeepDive(c) {
    document.getElementById('detail-ack-no').textContent = c.ack_number;
    document.getElementById('detail-amount').textContent = `₹${c.total_defrauded_amount.toLocaleString('en-IN')}`;
    document.getElementById('detail-victim').textContent = `${c.victim_name} (${c.victim_city}, ${c.victim_state})`;
    document.getElementById('detail-type').textContent = c.fraud_type;
    document.getElementById('detail-reported-at').textContent = c.reported_at;
    document.getElementById('detail-status').textContent = c.status;

    // Render Predictions
    const predContainer = document.getElementById('prediction-list');
    predContainer.innerHTML = '';

    c.predicted_hotspots.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'prediction-card';
      card.innerHTML = `
        <div class="prediction-title">
          <span>🎯 TARGET #${idx + 1}: ${p.bank_name} ${p.is_csp ? '(CSP Kiosk)' : '(ATM)'}</span>
          <span style="font-weight: 800;">${p.confidence_score}% PROB</span>
        </div>
        <div style="font-size: 11px; color: #cbd5e1;">📍 ${p.location_name}, ${p.district}</div>
        <div class="confidence-bar-bg">
          <div class="confidence-bar-fill" style="width: ${p.confidence_score}%"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: var(--font-mono); margin-top: 4px;">
          <span>⏱️ Lead Time: <strong>${p.estimated_time_to_withdrawal_mins} min</strong></span>
          <span>⚡ Window: <strong>${p.interception_window_mins} min</strong></span>
        </div>
      `;
      predContainer.appendChild(card);
    });

    // Render Mule Nodes
    const muleBody = document.getElementById('mule-nodes-body');
    muleBody.innerHTML = '';

    c.mule_nodes.forEach(m => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="risk-pill ${m.layer_level === 3 ? 'risk-critical' : 'risk-high'}">L${m.layer_level}</span></td>
        <td><strong>${m.account_number}</strong><br><span style="color: #64748b;">${m.holder_name}</span></td>
        <td>${m.bank_name}</td>
        <td style="text-align: right; color: #f59e0b; font-weight: bold;">₹${m.current_balance.toLocaleString('en-IN')}</td>
      `;
      muleBody.appendChild(tr);
    });

    // Dispatch button and Freeze button status
    const freezeBtn = document.getElementById('btn-generate-freeze');
    freezeBtn.onclick = () => this.generateFreezeNotice(c.complaint_id);

    const dispatchBtn = document.getElementById('btn-dispatch-action');
    dispatchBtn.onclick = () => {
      if (c.predicted_hotspots.length > 0) {
        this.dispatchNearestPCR(c.complaint_id, c.predicted_hotspots[0].atm_id);
      }
    };
  }

  async simulateNewIncident() {
    try {
      const res = await fetch('/api/complaints/generate', { method: 'POST' });
      const newComplaint = await res.json();
      this.complaints.unshift(newComplaint);
      this.renderIncidentFeed();
      this.selectIncident(newComplaint.complaint_id);
      this.fetchStats();

      alert(`🚨 Live Incident Ingested!\nAck No: ${newComplaint.ack_number}\nAmount: ₹${newComplaint.total_defrauded_amount.toLocaleString('en-IN')}\nAI Hotspot Forecast Generated!`);
    } catch (e) {
      alert("Error simulating incident: " + e);
    }
  }

  async dispatchNearestPCR(complaintId, atmId) {
    try {
      const payload = {
        complaint_id: complaintId,
        atm_id: atmId,
        pcr_unit_id: "PCR-NUH-01",
        officer_name: "SI Vikram Singh",
        officer_phone: "+91-98765-43210",
        notes: "Immediate ATM cordon & intercept order issued."
      };

      const res = await fetch('/api/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      alert(`✅ PCR UNIT DISPATCHED!\nUnit: PCR-NUH-01 (SI Vikram Singh)\nTarget: ${atmId}\nPush alert sent to Field Officer Mobile App.`);
      this.fetchComplaints();
      this.fetchStats();
    } catch (e) {
      alert("Error dispatching unit: " + e);
    }
  }

  async generateFreezeNotice(complaintId) {
    const c = this.complaints.find(x => x.complaint_id === complaintId);
    if (!c) return;

    try {
      const payload = {
        complaint_id: complaintId,
        bank_name: c.mule_nodes[0]?.bank_name || "State Bank of India",
        account_numbers: c.mule_nodes.map(n => n.account_number),
        police_station: "Cyber Crime Police Station (MHA / State Cyber Command)",
        investigating_officer: "DSP Rajesh Varma (Cyber Crime Cell)"
      };

      const res = await fetch('/api/freeze-notice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const htmlContent = await res.text();

      // Show in modal
      document.getElementById('freeze-notice-content').innerHTML = htmlContent;
      document.getElementById('freeze-modal').classList.add('active');

      this.fetchComplaints();
      this.fetchStats();
    } catch (e) {
      alert("Error generating freeze notice: " + e);
    }
  }

  handleNewIncidentStream(complaint) {
    this.complaints.unshift(complaint);
    this.renderIncidentFeed();
    this.fetchStats();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new CyberCommandApp();
  window.app.init();
});
