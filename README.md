
# BantAI – Risk-Based Authentication with Zero-Trust Principles

**BantAI** (from *bantay* = guard/watch in Filipino + AI) is an AI-powered plugin for **adaptive, behavior-based authentication**. Designed with **Zero-Trust security principles**, it enables banks and financial institutions to detect anomalous login behaviors and enforce real-time access decisions.

By learning from user context (location, device, network, login patterns), BantAI dynamically adjusts the authentication process — strengthening trust without adding unnecessary friction for legitimate users.

---

## 🚀 Key Features

* **Risk-Based Authentication (RBA):**
  Calculates a real-time risk score for every login attempt based on multiple behavioral and contextual factors.

* **Zero-Trust Enforcement:**
  No implicit trust — every session is continuously evaluated to prevent identity threats.

* **Adaptive MFA Integration:**
  Users can toggle BantAI on/off. When enabled, additional MFA challenges are triggered only when risk levels exceed safe thresholds.

* **Anomaly Detection:**
  Detects suspicious logins such as unusual schedules, device changes, or location anomalies.

* **Dashboard & Logs:**
  Provides administrators with a clear, self-documenting **Recent Login Activity** dashboard and **Feature Reference (Data Dictionary)** for transparency.

---

## 📊 Example Use Case

* A rural bank customer logs in from an unusual device at midnight.
* BantAI flags the attempt as **high-risk** based on: new device, unusual schedule, and VPN IP.
* Instead of blocking access outright, BantAI **enforces MFA** (e.g., OTP or push notification).
* If the attempt passes MFA → access granted. Otherwise → login denied.

This ensures **security without unnecessary friction** for everyday logins.

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit (Python-based rapid prototyping)
* **Backend/Logic:** Python (risk scoring, anomaly detection, explainable AI)
* **Data:** Simulated login activity dataset (engineered features like `time_diff`, `distance`, `ip_type`, `asn`)
* **Version Control:** GitHub
* **Deployment:** Streamlit Cloud (for demo)

---

## 📖 Feature Reference (Data Dictionary)

| Feature      | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| `time_diff`  | Time difference between consecutive logins (hours)                 |
| `distance`   | Geographic distance between logins (km)                            |
| `latency`    | Round-trip network time (ms)                                       |
| `ip_type`    | Type of IP address (residential, datacenter, VPN, proxy, etc.)     |
| `asn`        | Autonomous System Number (ISP/organization associated with the IP) |
| `device_id`  | Unique identifier for login device                                 |
| `schedule`   | Typical login schedule profile for the user                        |
| `risk_score` | Computed risk score (0–100) based on weighted factors              |
| `action`     | Decision taken: Allow / Challenge MFA / Block                      |

---

## ⚡ Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/BantAI.git
   cd BantAI
   ```

2. Create a virtual environment & install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)

   pip install -r requirements.txt
   ```

3. Run the app locally:

   ```bash
   streamlit run streamlit_app.py
   ```

4. Access in browser at: `http://localhost:8501`

---

## 🔒 Why BantAI?

* **Banks’ Pain Point:** Traditional authentication = static, easily bypassed.
* **Our Solution:** AI-powered, adaptive, and behavior-aware.
* **Impact:** Enhances digital trust while reducing fraud risks, especially in underbanked rural financial institutions.

> BantAI — *Your AI Guard for Digital Trust.*

---

## 👥 Team

Developed by **Allaiza Era and Brando Allen Donato** for the **BPI DataWave 2025 Hackathon**, under the challenge track:
**Digital Trust – AI for Risk-Based Authentication with Zero-Trust Principles.**


