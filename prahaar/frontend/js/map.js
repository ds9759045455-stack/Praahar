class TacticalMap {
  constructor(mapElementId) {
    this.mapId = mapElementId;
    this.map = null;
    this.atmLayer = null;
    this.pcrLayer = null;
    this.incidentLayer = null;
    this.pulseCircle = null;
  }

  init() {
    // Center initially on North India cybercrime corridor (Nuh/Mewat, Delhi, Alwar, Jamtara)
    this.map = L.map(this.mapId, {
      zoomControl: true,
      attributionControl: false
    }).setView([28.1065, 77.0125], 8);

    // OpenStreetMap standard tile layer (100% free, zero API key required)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      subdomains: ['a', 'b', 'c']
    }).addTo(this.map);

    this.atmLayer = L.layerGroup().addTo(this.map);
    this.pcrLayer = L.layerGroup().addTo(this.map);
    this.incidentLayer = L.layerGroup().addTo(this.map);

    this.loadStaticLayers();
  }

  async loadStaticLayers() {
    try {
      // 1. Load and plot all known ATM & CSP Hotspots
      const atmRes = await fetch('/api/atms');
      const atms = await atmRes.json();

      this.atmLayer.clearLayers();
      atms.forEach(atm => {
        const isCsp = atm.is_csp;
        const iconHtml = `<div style="background: ${isCsp ? '#a855f7' : '#0284c7'}; border: 2px solid #fff; border-radius: 4px; padding: 2px 5px; font-size: 10px; font-weight: bold; color: white; box-shadow: 0 0 6px rgba(0,0,0,0.5);">${isCsp ? '🏪 CSP' : '🏧 ATM'}</div>`;

        const atmIcon = L.divIcon({
          className: 'atm-static-marker',
          html: iconHtml,
          iconSize: [60, 20]
        });

        const marker = L.marker([atm.lat, atm.lng], { icon: atmIcon });
        marker.bindPopup(`
          <div style="color: #0f172a; font-family: sans-serif; font-size: 12px;">
            <strong>${atm.bank_name}</strong> (${atm.type})<br>
            <span>📍 ${atm.location_name}, ${atm.district}</span><br>
            <span>📹 CCTV: <strong>${atm.cctv_active ? 'Active' : 'Missing/Inactive'}</strong></span><br>
            <span>💵 Limit: <strong>₹${atm.daily_cash_limit.toLocaleString('en-IN')}</strong></span>
          </div>
        `);
        this.atmLayer.addLayer(marker);
      });

      // 2. Load and plot PCR Units
      const pcrRes = await fetch('/api/pcr-units');
      const pcrUnits = await pcrRes.json();

      this.pcrLayer.clearLayers();
      pcrUnits.forEach(unit => {
        const pcrIcon = L.divIcon({
          className: 'police-unit-marker',
          html: `<div style="background: #10b981; border: 2px solid #fff; border-radius: 4px; padding: 2px 6px; font-size: 10px; font-weight: bold; color: white; box-shadow: 0 0 8px rgba(16,185,129,0.7);">🚓 ${unit.unit_id}</div>`,
          iconSize: [85, 22]
        });

        const marker = L.marker([unit.lat, unit.lng], { icon: pcrIcon });
        marker.bindPopup(`
          <div style="color: #0f172a; font-family: sans-serif; font-size: 12px;">
            <strong>🚓 ${unit.name}</strong><br>
            Officer: ${unit.driver}<br>
            Phone: ${unit.phone}<br>
            Status: <span style="color: ${unit.status === 'AVAILABLE' ? 'green' : 'red'}; font-weight: bold;">${unit.status}</span>
          </div>
        `);
        this.pcrLayer.addLayer(marker);
      });
    } catch (e) {
      console.warn("Could not load static map layers", e);
    }
  }

  renderIncidentHotspots(complaint) {
    this.incidentLayer.clearLayers();
    if (this.pulseCircle) {
      this.map.removeLayer(this.pulseCircle);
    }

    if (!complaint || !complaint.predicted_hotspots || complaint.predicted_hotspots.length === 0) {
      return;
    }

    const topHotspot = complaint.predicted_hotspots[0];

    // Smoothly pan to top predicted hotspot
    this.map.flyTo([topHotspot.lat, topHotspot.lng], 13, { duration: 1.2 });

    // Draw pulsating danger circle for the top predicted cashout ATM
    this.pulseCircle = L.circle([topHotspot.lat, topHotspot.lng], {
      radius: 800,
      color: '#ef4444',
      fillColor: '#ef4444',
      fillOpacity: 0.28,
      weight: 3
    }).addTo(this.map);

    // Plot all predicted hotspots
    complaint.predicted_hotspots.forEach((h, index) => {
      const isTop = index === 0;
      const markerHtml = `
        <div class="${isTop ? 'pulse-marker-danger' : ''}" style="${!isTop ? 'width: 16px; height: 16px; background: #f59e0b; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 8px #f59e0b;' : ''}"></div>
      `;

      const customIcon = L.divIcon({
        className: 'custom-atm-marker',
        html: markerHtml,
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      });

      const marker = L.marker([h.lat, h.lng], { icon: customIcon });

      const popupContent = `
        <div style="color: #0f172a; font-family: 'Segoe UI', sans-serif; min-width: 240px; font-size: 12px;">
          <div style="background: #ef4444; color: #fff; padding: 6px 10px; border-radius: 4px 4px 0 0; font-weight: bold; font-size: 13px;">
            🚨 PREDICTED CASHOUT TARGET #${index + 1}
          </div>
          <div style="padding: 10px; border: 1px solid #cbd5e1; border-top: none; background: #fff;">
            <strong style="font-size: 13px;">${h.bank_name} ${h.is_csp ? '(CSP Kiosk)' : '(ATM)'}</strong><br>
            <span style="color: #64748b;">${h.location_name}, ${h.district}</span>
            <hr style="margin: 8px 0; border: none; border-top: 1px solid #e2e8f0;">
            <div><strong>Probability Score:</strong> <span style="color: #dc2626; font-weight: 800; font-size: 13px;">${h.confidence_score}%</span></div>
            <div><strong>Estimated Time to Cashout:</strong> <span style="color: #d97706; font-weight: bold;">${h.estimated_time_to_withdrawal_mins} mins</span></div>
            <div><strong>Interception Window:</strong> ${h.interception_window_mins} mins</div>
            <button onclick="window.app.dispatchNearestPCR('${complaint.complaint_id}', '${h.atm_id}')" 
              style="margin-top: 10px; width: 100%; background: #0284c7; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold; cursor: pointer;">
              ⚡ DISPATCH NEAREST PCR PATROL
            </button>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);
      this.incidentLayer.addLayer(marker);

      if (isTop) {
        marker.openPopup();
      }
    });
  }
}

window.TacticalMap = TacticalMap;
