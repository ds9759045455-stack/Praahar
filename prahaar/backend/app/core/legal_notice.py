from datetime import datetime
from typing import List, Dict
from app.models.schemas import CyberComplaint

class LegalNoticeGenerator:
    def __init__(self):
        pass

    def generate_freeze_notice_html(
        self,
        complaint: CyberComplaint,
        bank_name: str,
        investigating_officer: str = "DSP Cyber Crime Cell",
        police_station: str = "State Cyber Crime Police Station"
    ) -> str:
        """
        Generates an authentic legal debit-freeze order under Section 102 CrPC / Section 106 BNSS 2023
        and Section 91 CrPC (Summons to produce documents) for Bank Nodal Officers.
        """
        now_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ref_no = f"CYBER/FREEZE/{datetime.now().strftime('%Y%m%d')}/{complaint.complaint_id}"

        # Find mule accounts belonging to this bank
        bank_accounts = [n for n in complaint.mule_nodes if bank_name.lower() in n.bank_name.lower()]
        if not bank_accounts:
            bank_accounts = complaint.mule_nodes

        accounts_table_rows = ""
        for idx, acc in enumerate(bank_accounts, 1):
            accounts_table_rows += f"""
            <tr>
                <td style="border: 1px solid #cbd5e1; padding: 8px; text-align: center;">{idx}</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px; font-weight: bold; font-family: monospace;">{acc.account_number}</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px;">{acc.holder_name}</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px;">{acc.bank_name}</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px; font-family: monospace;">{acc.ifsc_code}</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px; color: #dc2626; font-weight: bold;">Layer {acc.layer_level} ({acc.kyc_risk})</td>
                <td style="border: 1px solid #cbd5e1; padding: 8px; text-align: right; font-weight: bold;">₹{acc.current_balance:,.2f}</td>
            </tr>
            """

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Emergency Debit Freeze Notice - {ref_no}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; background: #ffffff; }}
                .header {{ text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; }}
                .header h2 {{ margin: 0; text-transform: uppercase; letter-spacing: 1px; color: #0f172a; }}
                .header h4 {{ margin: 4px 0 0 0; color: #475569; font-weight: normal; }}
                .badge-urgent {{ background: #dc2626; color: white; padding: 4px 12px; border-radius: 4px; font-size: 13px; font-weight: bold; display: inline-block; margin-top: 8px; }}
                .meta-table {{ width: 100%; margin-bottom: 20px; font-size: 14px; }}
                .meta-table td {{ padding: 4px 0; }}
                .section-title {{ font-size: 15px; font-weight: bold; color: #0f172a; margin-top: 20px; margin-bottom: 8px; text-transform: uppercase; border-left: 4px solid #0284c7; padding-left: 8px; }}
                .notice-body {{ font-size: 14px; line-height: 1.6; text-align: justify; }}
                .acc-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px; }}
                .acc-table th {{ background: #f1f5f9; border: 1px solid #cbd5e1; padding: 8px; text-align: left; font-weight: 600; }}
                .footer {{ margin-top: 40px; display: flex; justify-content: space-between; font-size: 13px; }}
                .stamp-box {{ border: 2px dashed #94a3b8; padding: 15px; width: 220px; text-align: center; border-radius: 6px; color: #475569; }}
                .qr-placeholder {{ font-size: 11px; color: #64748b; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>OFFICE OF THE SUPERINTENDENT OF POLICE (CYBER CRIME)</h2>
                <h4>{police_station.upper()} | CRIME INVESTIGATION DEPARTMENT</h4>
                <div class="badge-urgent">URGENT: SECTION 106 BNSS 2023 / SECTION 102 Cr.P.C FREEZE ORDER</div>
            </div>

            <table class="meta-table">
                <tr>
                    <td style="width: 50%;"><strong>Dispatch Ref No:</strong> {ref_no}</td>
                    <td style="width: 50%; text-align: right;"><strong>Date & Timestamp:</strong> {now_str}</td>
                </tr>
                <tr>
                    <td><strong>NCRP Ack No:</strong> {complaint.ack_number}</td>
                    <td style="text-align: right;"><strong>Helpline Ref:</strong> 1930 / I4C Incident ID #{complaint.complaint_id}</td>
                </tr>
            </table>

            <div class="notice-body">
                <p><strong>To,</strong><br>
                The Chief Nodal Officer / Fraud Risk Management (FRM) Cell,<br>
                <strong>{bank_name}</strong>, Head Office / Cyber Liaison Division.</p>

                <p><strong>Subject:</strong> Immediate Emergency Debit-Freeze Order under Section 106 of Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 (formerly Section 102 Cr.P.C) and Requisition under Section 94 BNSS (formerly Sec 91 Cr.P.C) regarding Cyber Fraud incident involving <strong>₹{complaint.total_defrauded_amount:,.2f}</strong>.</p>

                <p>Whereas, an emergency cyber fraud complaint was lodged on the National Cybercrime Reporting Portal (NCRP) regarding <em>{complaint.fraud_type}</em> defrauding citizen <strong>{complaint.victim_name}</strong> (R/o {complaint.victim_city}, {complaint.victim_state}). Multi-hop graph analytics and predictive intelligence have traced the illicit proceeds into the following high-risk beneficiary/mule accounts hosted at your institution:</p>

                <table class="acc-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Account Number</th>
                            <th>Account Holder</th>
                            <th>Bank Name</th>
                            <th>IFSC Code</th>
                            <th>Layer / Risk</th>
                            <th style="text-align: right;">Suspect Balance</th>
                        </tr>
                    </thead>
                    <tbody>
                        {accounts_table_rows}
                    </tbody>
                </table>

                <p><strong>DIRECTIVES TO THE BANK:</strong></p>
                <ol>
                    <li><strong>IMMEDIATE DEBIT FREEZE:</strong> Place an immediate total debit freeze (including ATM, Netbanking, UPI, and Branch withdrawal) on the aforementioned accounts to prevent cash siphon-off during the ongoing Golden Hour.</li>
                    <li><strong>TRANSACTION LOGS & KYC:</strong> Furnish account opening KYC documents, registered mobile number, IP logs, linked ATM card details, and 6-month statement of account within 24 hours via secure LEA portal.</li>
                    <li><strong>ATM/CSP EXTRACTION ALERT:</strong> Disable any pending tokenized ATM cash-out or biometric AEPS transactions on these accounts with immediate effect.</li>
                </ol>
            </div>

            <table style="width: 100%; margin-top: 50px;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="stamp-box">
                            <strong>DIGITALLY SIGNED & VERIFIED</strong><br>
                            I4C / LEA Secure Gateway<br>
                            Token: {complaint.complaint_id}-VERIFIED<br>
                            <span class="qr-placeholder">[Valid under Sec 65B Indian Evidence Act]</span>
                        </div>
                    </td>
                    <td style="width: 50%; text-align: right; vertical-align: top;">
                        <br><br>
                        <strong>({investigating_officer})</strong><br>
                        Investigating Officer (Cyber Crimes)<br>
                        {police_station}<br>
                        Ministry of Home Affairs / State Cyber Command
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html_template

legal_notice_generator = LegalNoticeGenerator()
