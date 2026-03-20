GigShield – AI-Powered Parametric Income Insurance for Delivery Workers

## 👥 Team & Responsibilities
- Harshith (Backend Developer)
- Vignesh (API Integeration)
- Sathwik (AI/Risk Model)
- Shresta (Frontend Developer)
- Vijay (Dashboard+Demo+PPT)

 Problem Statement

Delivery workers (Swiggy, Zomato, Amazon, etc.) often lose income due to external disruptions such as heavy rain, extreme heat, pollution, or curfews.

These disruptions reduce working hours, leading to significant income loss.

Current challenges:

- No income protection system exists
- Workers bear financial loss alone
- Insurance models are not designed for gig economy workers

GigShield solves this by providing AI-powered parametric income insurance with automatic payouts.

---

👤 Persona-Based Scenario

Persona: Delivery Worker (Ravi)

- Works for a delivery platform
- Depends on daily income
- Faces frequent disruptions (rain, heat, pollution)

Problem:
During heavy rain or extreme conditions, Ravi cannot work → loses income

Solution:
GigShield automatically detects disruptions and provides compensation for lost income.

---

🔄 Application Workflow

1. User registers using face-based identity
2. Weekly insurance policy is activated
3. AI calculates user risk profile
4. System monitors external events (weather, pollution, etc.)
5. Parametric trigger detected (e.g., heavy rain)
6. Income loss is calculated
7. Automatic claim is initiated
8. Instant payout is processed

💡 Example (Income Loss Calculation)

If:

- Heavy rain stops deliveries for 4 hours
- Average earning = ₹80/hour

👉 Income loss = 4 × 80 = ₹320
👉 Instant payout = ₹320

---

 Weekly Premium Model

Premium is calculated based on:

- Location risk (flood-prone / pollution-prone areas)
- Historical weather disruptions
- AI-generated risk score

Example:

Risk Level| Premium
Low Risk| ₹50/week
Medium Risk| ₹100/week
High Risk| ₹200/week

---

 Parametric Triggers (Core Feature)

GigShield uses real-world data to trigger automatic claims:

- Rainfall above threshold → payout triggered
- Temperature above threshold → payout triggered
- AQI (Pollution level) above threshold → payout triggered
- Government curfew / zone closure → payout triggered

 This is a zero-touch claim system — no manual claim submission required.

---

 Integration Capabilities

- Weather API (rainfall, temperature data)
- Pollution API (AQI levels)
- Mock delivery platform data (working hours estimation)
- Payment gateway simulation (UPI/Razorpay for payouts)

---

 AI/ML Integration

- AI-based risk prediction model
- Dynamic premium calculation
- Fraud detection (duplicate identity, anomaly detection)
- Behavioral pattern analysis

---

 Fraud Detection

- Face-based identity verification
- Duplicate account detection
- Suspicious activity monitoring
- Claim validation mechanisms

---

 Tech Stack

- Backend: Flask (Python)
- Database: SQLite
- AI: Face Recognition + Risk Scoring
- APIs: Weather API (planned / simulated)
- Version Control: GitHub

---

 Development Plan

Phase 1

- Idea design
- Backend setup
- Risk model planning

Phase 2

- Policy creation
- Dynamic pricing
- Parametric trigger logic

Phase 3

- Claim automation
- Fraud detection system

Phase 4

- Dashboard
- Payout simulation
- Deployment

---

 Future Scope

- Mobile application
- Real-time GPS validation
- Live weather API integration
- Payment gateway integration (UPI / Razorpay)
- Advanced AI fraud detection

---

📉 Market Crash Handling

GigShield is designed to handle large-scale disruptions affecting multiple users simultaneously.

In case of a market-wide disruption (e.g., heavy rainfall across a city):

- AI models predict expected claim volume
- Dynamic payout limits are applied to maintain system sustainability
- Risk-adjusted premium updates are triggered for upcoming weeks
- Claims are prioritized based on verified activity and location data

This ensures that the platform remains financially stable while still protecting workers during large-scale events.

---

🛡️ Adversarial Defense & Anti-Spoofing Strategy

GigShield is designed to detect and prevent large-scale coordinated fraud attacks such as GPS spoofing and fake claims.

🔍 Multi-Layer Fraud Detection:

1. Face Identity Verification
- Each user is uniquely identified using face encoding
- Prevents duplicate accounts and identity spoofing

2. Behavioral Pattern Analysis
- Detects unusual patterns such as:
  - Multiple claims in short time
  - Abnormal working hours
  - Unrealistic activity spikes

3. Location Validation (Anti-GPS Spoofing)
- Cross-verification using:
  - Historical movement patterns
  - Expected delivery zones
  - Time-based travel feasibility
- Flags impossible or suspicious location jumps

4. Anomaly Detection using AI
- AI model identifies:
  - Sudden surge in claims from same region
  - Similar behavior across multiple users (fraud rings)
- High-risk clusters are flagged instantly

5. Risk-Based Claim Control
- High-risk users:
  - Claims are delayed or reduced
  - Additional verification triggered
- Genuine users are not impacted

6. Market Crash Handling
- During mass disruptions:
  - System limits maximum payouts dynamically
  - Prioritizes verified and active users
  - Adjusts future premiums based on risk surge

Outcome:
GigShield ensures protection against fraud rings while maintaining fairness for genuine workers.
