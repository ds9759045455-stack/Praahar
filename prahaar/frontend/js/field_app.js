class FieldOfficerApp {
  constructor() {
    this.officerId = "PCR-NUH-01";
    this.activeIncident = null;
    this.complaints = [];
  }

  async init() {
    await this.fetchAndCheckAssigned();
    // Poll every 3 seconds for new live dispatches
    setInterval(() => this.fetchAndCheckAssigned(), 3000);
  }

  async fetchAndCheckAssigned() {
    try {
      const res = await fetch('/api/complaints');
      this.complaints = await res.json();
      
      // Look for a complaint assigned specifically to this unit or marked as DISPATCHED
      const assigned = this.complaints.find(c => c.assigned_pcr_unit === this.officerId || c.status === "DISPATCHED");

      if (assigned) {
        if (!this.activeIncident || this.activeIncident.complaint_id !== assigned.complaint_id) {
          this.activeIncident = assigned;
          this.renderIncidentAlert(assigned);
        }
      } else {
        if (!this.activeIncident) {
          this.renderIdleState();
        }
      }
    } catch (e) {
      console.warn("Field app poll error", e);
      if (!this.activeIncident) {
        this.renderIdleState();
      }
    }
  }

  renderIncidentAlert(c) {
    const alertBox = document.getElementById('field-alert-container');
    const topHotspot = (c.predicted_hotspots && c.predicted_hotspots.length > 0) ? c.predicted_hotspots[0] : {};
    const lastMule = (c.mule_nodes && c.mule_nodes.length > 0) ? c.mule_nodes[c.mule_nodes.length - 1] : {};

    alertBox.innerHTML = `
      <div class="field-card urgent-flash">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="background: #dc2626; color: white; padding: 5px 12px; border-radius: 4px; font-weight: 900; font-size: 13px; letter-spacing: 0.5px;">
            🚨 PRIORITY 1: ATM CASHOUT INTERCEPT
          </span>
          <span style="font-family: monospace; color: #facc15; font-weight: bold; font-size: 13px;">
            ETA: ${topHotspot.estimated_time_to_withdrawal_mins || 25} MINS
          </span>
        </div>

        <h2 style="margin: 14px 0 6px 0; font-size: 20px; color: #fff;">${topHotspot.bank_name || 'State Bank of India'} ${topHotspot.is_csp ? '(CSP Kiosk)' : '(ATM)'}</h2>
        <div style="color: #cbd5e1; font-size: 14px;">📍 ${topHotspot.location_name || 'Nuh Chowk'}, ${topHotspot.district || 'Nuh (Mewat)'}</div>

        <div style="background: rgba(0, 0, 0, 0.5); border: 1px solid #1e2e4f; border-radius: 8px; padding: 14px; margin: 14px 0; font-size: 13px;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #94a3b8;">NCRP Ack Number:</span>
            <span style="font-family: monospace; color: #38bdf8; font-weight: bold;">${c.ack_number}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #94a3b8;">Suspect Siphon Amount:</span>
            <span style="color: #4ade80; font-weight: 800; font-size: 16px;">₹${c.total_defrauded_amount.toLocaleString('en-IN')}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #94a3b8;">Target Mule Account:</span>
            <span style="font-family: monospace; color: #f87171; font-weight: bold;">${lastMule.account_number || '919876543210'}</span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Suspect Mule Name:</span>
            <span style="color: #fff; font-weight: bold;">${lastMule.holder_name || 'Aslam Khan'}</span>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
          <button onclick="window.fieldApp.openNavigation(${topHotspot.lat || 28.1065}, ${topHotspot.lng || 77.0125})" class="btn-field btn-nav">
            🗺️ START GPS NAVIGATION
          </button>
          <button onclick="window.fieldApp.confirmArrival('${c.complaint_id}')" class="btn-field btn-arrive">
            📍 ARRIVED AT ATM
          </button>
        </div>
        <button onclick="window.fieldApp.apprehendSuspect('${c.complaint_id}')" class="btn-field btn-success" style="margin-top: 10px; width: 100%;">
          🛡️ SUSPECT APPREHENDED & CASH SECURED
        </button>
      </div>
    `;
  }

  renderIdleState() {
    const alertBox = document.getElementById('field-alert-container');
    const firstComplaint = this.complaints[0] || null;

    alertBox.innerHTML = `
      <div class="field-card" style="text-align: center; padding: 30px 20px;">
        <div style="font-size: 48px; margin-bottom: 12px;">🚓</div>
        <h3 style="color: #38bdf8; font-size: 18px; margin-bottom: 6px;">PATROL STATUS: ACTIVE ON DUTY</h3>
        <p style="color: #94a3b8; font-size: 13px; line-height: 1.5; margin-bottom: 20px;">
          Unit <strong>PCR-NUH-01 (SI Vikram Singh)</strong> is scanning ATM clusters across Nuh (Mewat).
          Awaiting real-time cashout predictive dispatch from Cyber Command.
        </p>

        <div style="background: rgba(18, 28, 51, 0.7); border: 1px solid #1e2e4f; border-radius: 8px; padding: 14px; text-align: left; margin-bottom: 20px;">
          <div style="font-size: 12px; font-weight: 700; color: #facc15; margin-bottom: 8px;">
            📡 HIGH-PRIORITY ATM RADAR WATCHLIST (NUH DISTRICT)
          </div>
          <div style="font-size: 12px; color: #cbd5e1; line-height: 1.6;">
            • <strong>SBI ATM</strong> - Nuh Chowk Main Market (High Traffic)<br>
            • <strong>PNB CSP Kiosk</strong> - Tauru Road Junction (Zero CCTV)<br>
            • <strong>HDFC Bank ATM</strong> - Ferozepur Jhirka Bus Stand
          </div>
        </div>

        ${firstComplaint ? `
          <button onclick="window.fieldApp.simulateTestDispatch('${firstComplaint.complaint_id}')" class="btn-field btn-nav" style="width: 100%;">
            ⚡ TEST SIMULATE EMERGENCY DISPATCH TO THIS UNIT
          </button>
        ` : ''}
      </div>
    `;
  }

  openNavigation(lat, lng) {
    if (lat && lng) {
      window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`, '_blank');
    }
  }

  confirmArrival(complaintId) {
    alert("🚨 Status Transmitted to Cyber Command Center:\nUnit PCR-NUH-01 arrived at target ATM. Visual cordon & perimeter surveillance active.");
  }

  async apprehendSuspect(complaintId) {
    alert("🎉 SUCCESS TRANSMITTED TO I4C / MHA:\nSuspect money mule intercepted at ATM before cash extraction. ₹100% of citizen funds secured!");
    this.activeIncident = null;
    this.renderIdleState();
  }

  async simulateTestDispatch(complaintId) {
    try {
      const payload = {
        complaint_id: complaintId,
        atm_id: "ATM-NUH-0101",
        pcr_unit_id: "PCR-NUH-01",
        officer_name: "SI Vikram Singh",
        officer_phone: "+91-98765-43210",
        notes: "Emergency ATM cordon dispatch"
      };
      await fetch('/api/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      await this.fetchAndCheckAssigned();
    } catch (e) {
      console.error(e);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.fieldApp = new FieldOfficerApp();
  window.fieldApp.init();
});
