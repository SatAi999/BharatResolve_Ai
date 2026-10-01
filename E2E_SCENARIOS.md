# BHARATRESOLVE AI - GOLDEN E2E SCENARIOS REPORT

---

## 1. SCENARIO 1: NSP SCHOLARSHIP DISBURSEMENT FAILURE
- **Input:** *"My NSP scholarship of Rs 12000 was approved 2 months ago but payment not received in bank account"*
- **Agent Behavior:**
  1. Intake Agent classifies Domain: `Education`, Intent: `Scholarship Support`.
  2. Investigator searches live `.gov.in` sources for CPGRAMS and NSP nodal officer contact guidelines.
  3. Risk Gate classifies `prepare_grievance` action as `MEDIUM` risk, entering `PENDING_APPROVAL` state interrupt.
  4. Upon citizen approval, action executes CPGRAMS Nodal Appeal Representation generation.
  5. Verification Agent confirms evidence completeness and assigns Case Resolution Score.

---

## 2. SCENARIO 2: ELECTRICITY BILL SUDDEN ANOMALY
- **Input:** *"My electricity bill for June jumped from Rs 1200 to Rs 18400. Meter number meter-889977 in Jaipur Rajasthan"*
- **Agent Behavior:**
  1. Intake Agent classifies Domain: `Utilities`, Intent: `Bill Anomaly`.
  2. Investigator invokes `Open-Meteo` weather API to inspect Jaipur temperature history for extreme heatwave surges.
  3. OpenStreetMap geocodes DISCOM office location.
  4. Grievance Builder generates formal Executive Engineer Dispute Application.

---

## 3. SCENARIO 3: UNSEASONAL CROP DAMAGE RELIEF
- **Input:** *"Heavy unseasonal rain damaged my wheat crop in Varanasi Uttar Pradesh. How to claim PM Fasal Bima Yojana relief?"*
- **Agent Behavior:**
  1. Intake Agent classifies Domain: `Agriculture`, Intent: `Crop Damage Relief`.
  2. Investigator queries `Open-Meteo` live precipitation forecast (`0.0mm` rain, temp verified).
  3. Live Search retrieves PMFBY 72-hour crop loss notification procedure.
  4. Generates insurance representation application.

---

## 4. SCENARIO 4: HUMAN APPROVAL PAUSE & REJECTION
- **Input:** *"File a formal complaint against municipal water supply department"*
- **Agent Behavior:**
  1. Case reaches `risk_gate_stage`.
  2. Action `prepare_grievance` identified as `MEDIUM` risk.
  3. Agent enters `PENDING_APPROVAL` status (`is_paused_for_approval = True`) and emits SSE event.
  4. When citizen selects `REJECT`, backend sets case status to `REJECTED` and halts execution safely without unauthorized dispatches.
