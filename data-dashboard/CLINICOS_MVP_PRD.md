# ClinicOS MVP Product Requirements Document (PRD)

> [!IMPORTANT]
> **Communication Channel Priority (Fallback Logic)**
> For all patient notifications, reminders, confirmations, alerts, queue updates, appointment updates, and system-generated communications:
> 1. Check whether the patient has an active WhatsApp number.
> 2. **IF WhatsApp Available** → Send via WhatsApp API
> 3. **ELSE** → Send via SMS/Message API (Fallback)
> 
> *This mechanism applies consistently across all modules, workflows, and user journeys.*

## Generated via FRONTIER PRD OPERATING SYSTEM (PRD-OS v3)
### Classification: Founder-Grade | Engineering-Grade | Investor-Grade

---

# 1. EXECUTIVE SUMMARY

**ClinicOS** is a multi-tenant, AI-augmented clinical operations platform designed to upgrade India's outpatient clinic ecosystem from manual, paper-based workflows to a unified, role-based digital operating system. This MVP focuses specifically on providing robust solutions for Receptionists and Doctors, incorporating queue management, appointment scheduling, patient registration, consultations, and UPI/Cash payments. The core differentiator is the **Dual-Mode Automation Engine** (Review Mode / AI Mode), allowing clinics to control AI autonomy.

**Verdict:** Build. The current market is severely underserved, and the proposed feature set tightly addresses the immediate pain points of queue chaos and revenue leakage.

---

# 2. PRODUCT VISION

> To become the default operating system for India's 600,000+ outpatient clinics, replacing fragmented manual processes with an intelligent, ambient AI-assisted digital workflow that scales from a single rural clinic to a national network.

---

# 3. PROBLEM STATEMENT

### The Core Problem
Most outpatient clinics in India operate with zero or minimal software. They suffer from paper token queues, WhatsApp-based appointment chaos, handwritten prescriptions, cash reconciliation errors, and nonexistent patient history tracking.

### Pain Severity
- **Queue Chaos:** Daily. High impact on patient drop-off.
- **Payment Reconciliation:** Daily. High impact on revenue leakage.
- **Receptionist Overload:** Daily. High impact on burnout and operational errors.
- **Doctor Burnout:** Daily. Time wasted on non-clinical admin tasks.

### Consequence of Not Solving
Clinics lose 15-25% of potential revenue to operational inefficiencies and face compliance risks under upcoming Indian digital health mandates (ABDM).

---

# 4. PRODUCT DISCOVERY FINDINGS

Based on the existing prototype and UI/UX codebase analysis:
- **Patient Lifecycle:** Validated and modeled (`Arrived → Waiting → With Doctor → Completed`).
- **Dual-Mode AI:** Architecturally sound with immutable human-gated safety boundaries.
- **Role Isolation:** Strict separation between Receptionist, Doctor, and Admin workflows.
- **Current Gap:** The existing platform is a frontend prototype. A robust backend (Node.js/PostgreSQL) must be built to support the UI intent.

---

# 5. MARKET ANALYSIS

- **Total Addressable Market (India):** ~600,000 outpatient clinics.
- **Serviceable Addressable Market:** ~510,000 clinics currently lacking modern software.
- **Estimated TAM:** ₹12.2B/year (assuming ₹2,000/month SaaS fee).
- **Market Timing:** Highly favorable due to government ABDM mandates pushing digital health records.

---

# 6. COMPETITIVE ANALYSIS

| Competitor | Strength | Weakness | Why ClinicOS Wins |
|---|---|---|---|
| **Practo** | Consumer brand recognition | Complex, expensive, B2C focus | B2B Operations focus, Dual-Mode AI |
| **MocDoc** | Queue management features | Lacks AI automation layer | Deep AI integration, Luxury Minimal UI |
| **WhatsApp + Excel** | Free, ubiquitous | No data structure, no automation | AI removes manual overhead |

---

# 7. BUSINESS MODEL ANALYSIS

### Revenue Model
Subscription SaaS (Per-Clinic, Multi-tenant).

### Pricing Strategy (Proposed)
- **Starter:** ₹999/month (Queue + Payments + Basic Consultations)
- **Professional:** ₹2,499/month (Dual-Mode AI + WhatsApp Integration + Analytics)

### Operational Costs (Estimate for 100 clinics)
- AWS/GCP Infra: ₹25,000
- OpenAI API: ₹20,000
- WhatsApp/SMS: ₹18,000
- Support/Monitoring: ₹45,000
- **Total:** ~₹1,08,000/month. Break-even at ~50 Professional tier clinics.

---

# 8. FOUNDER REALITY ASSESSMENT

- **Current State:** Comprehensive frontend prototype exists; zero backend infrastructure.
- **Execution Risk:** High if attempting to build the entire V2 scope immediately.
- **Recommendation:** Strictly limit MVP scope to the core workflows for the Receptionist and Doctor. Exclude complex AI Voice Agents, Medical Task Pipelines, and Staff Management for now.

---

# 9. GOALS & SUCCESS METRICS

| Goal | Metric | Target (3 Months Post-Launch) |
|---|---|---|
| **Operational Speed** | Patient check-in time | < 30 seconds |
| **Financial Accuracy** | Day-close discrepancy | < 1% error rate |
| **Adoption** | Active paying clinics | 10 pilot clinics |
| **AI Engagement** | AI suggestion acceptance | > 60% in Review Mode |

---

# 10. USER PERSONAS

1. **Reena (Receptionist):** 24, non-technical. Needs to manage 80+ patients/day. Requires a mobile-first, fast, foolproof UI with 100% Hindi localization.
2. **Dr. Sameer (Doctor/Owner):** 42, time-starved. Needs to see patients efficiently without software distraction. Requires a desktop-optimized, data-dense clinical command center.

---

# 11. USER JOURNEYS

- **Check-in to Queue:** Patient arrives → Reena uses Operations page to mark 'Arrived' → AI suggests moving to 'Waiting' → Reena approves → Patient appears on Doctor's queue.
- **Consultation:** Doctor selects patient → Reviews history → Records SOAP notes via dictation → Generates prescription → Ends consultation.
- **Payment:** Reena selects completed patient → Generates UPI QR → Patient scans → Payment verified → Invoice generated.

---

# 12. FUNCTIONAL REQUIREMENTS

Based on MVP scoping constraints from `Doctor_features.txt` and `Receptionist_features.txt`.

### Receptionist Features
- **Queue Management & Calendar:** Real-time patient status tracking, appointment booking, and waitlist management.
- **Patient Registration:** Integration with external/internal Google Form-style intake.
- **Patient Gateway:** WhatsApp integration for alerts, chat monitoring, and AI chatbot control/tracking.
- **Patient Directory:** Comprehensive list and search functionality.
- **Payment Processing:** Cash and UPI QR code generation, day-close reconciliation.

### Doctor Features
- **Consultation Workspace:** SOAP notes, vitals, and prescription builder.
- **Patient Data & Approvals:** Access to patient history and approval workflows for AI suggestions.
- **Analytics:** Doctor clinical analytics and Business/Revenue BI dashboards.
- **Queue Monitoring & Home Panel:** Real-time visibility into the clinic's waiting room.

### Global Modes
- Light/Dark Mode toggle.
- English/Hindi localization.
- Dual-Mode Automation: Review (Human-in-the-loop) vs. AI (Autonomous execution).

---

# 13. NON-FUNCTIONAL REQUIREMENTS

- **Performance:** App load < 2s on 4G networks; API P95 latency < 800ms.
- **Reliability:** 99.5% uptime during clinic hours (8am-10pm).
- **Scalability:** System architecture must support 500+ clinics (multi-tenant ready).

---

# 14. UX REQUIREMENTS

- **Design System:** "Luxury Minimal" — clean, empathetic warmth, organic shapes (no sharp corners).
- **Localization:** 100% Hindi support via `t()` function; UI must not break with text expansion.
- **Accessibility:** WCAG 2.1 AA compliant; massive tap targets (>44px) for mobile receptionist views.
- **Role Isolation:** Strict visual and routing boundaries between Receptionist and Doctor views.

---

# 15. FEATURE PRIORITIZATION MATRIX

| Feature | Priority | Phase |
|---|---|---|
| Auth, DB, Backend API | **P0** | MVP |
| Queue Management | **P0** | MVP |
| Consultation Workspace | **P0** | MVP |
| Payments (UPI/Cash) | **P0** | MVP |
| Dual-Mode Automation | **P1** | MVP/V1 |
| WhatsApp Gateway | **P1** | MVP |
| Analytics/BI Dashboards | **P1** | MVP |
| Live AI Moderation | **P2** | V1 |
| Communication Hub | **Excluded** | V2 |
| Staff Management | **Excluded** | V2 |

---

# 16. MVP SCOPE

**Focus:** Core clinic loop with explicit exclusions.
- Patient Registration, Directory, Queue Management, Calendar.
- Consultation Workspace (Doctor Home Panel, Patient Data, Approvals).
- Payment Processing (UPI/Cash).
- WhatsApp Patient Gateway (Alerts, Chats, Tracking).
- Doctor & Business Analytics Dashboards.
- Global Modes: Light/Dark, EN/HI, Review/AI modes.

**Explicitly Excluded:** Tasks, Communication Center, Staff Management, Online Consultation, AI Voice Agent, Advanced Payment Management.

---

# 17. V1 SCOPE

- Full deployment of AI Moderation and abuse detection.
- Deepened Dual-Mode capabilities with complex workflows.
- Expanded WhatsApp chatbot autonomous routing.

---

# 18. V2 SCOPE

- Enterprise Command Center (Multi-tenant Admin UI).
- Staff Management & Medical Task Pipeline.
- ABDM Compliance and Pharmacy Integrations.

---

# 19. SYSTEM ARCHITECTURE

- **Frontend:** React SPA (Vite + TypeScript), Tailwind CSS v4, Context API (migrating to modular contexts + React Query).
- **Backend:** Node.js (Express/Fastify) for API layer.
- **Database:** PostgreSQL (Core Data) + Redis (Real-time WebSockets/Queue).
- **Real-time:** WebSocket layer for live queue and AI automation event synchronization.

---

# 20. ARCHITECTURE DECISION RECORDS (ADR)

- **ADR-01: Monolith vs Microservices:** Chosen modular monolith (Node.js). Faster iteration for MVP; microservices add unnecessary operational overhead for a small team.
- **ADR-02: PostgreSQL:** Chosen for strict ACID compliance required by financial and medical data.

---

# 21. DATABASE DESIGN

Core Tables:
- `tenants`
- `users` (Roles: Receptionist, Doctor, Admin)
- `patients`
- `appointments`
- `queue_entries`
- `consultation_notes`
- `transactions`
- `automation_events`

---

# 22. API DESIGN

RESTful Architecture:
- `POST /auth/login`
- `GET/POST /patients`
- `GET/PATCH /queue`
- `GET/POST /appointments`
- `POST /payments/upi-generate`
- `POST /consultations`
- `GET /analytics/doctor`
- `GET /analytics/business`

---

# 23. AI SYSTEM DESIGN

- **LLM:** OpenAI GPT-4o mini for chat gateway and suggestion engine.
- **Architecture:** System prompt injection with clinic context. Moderation layer runs parallel to scan for abuse scoring.

---

# 24. AUTOMATION DESIGN

- **Review Mode:** AI generates `AISuggestion` records -> Pushed to client -> Human approves -> Logs `AutomationEvent`.
- **AI Mode:** AI executes immediately -> Pushed to live feed -> 30-second undo window -> Logs `AutomationEvent`.
- **Hard-gated overrides:** Clinical approvals, refunds, and emergency queue jumps *always* require human review.

---

# 25. SAAS DESIGN

Multi-tenant architecture utilizing Row-Level Security (RLS) in PostgreSQL with `tenant_id` foreign keys injected via JWT.

---

# 26. INTEGRATION REQUIREMENTS

- **Razorpay:** UPI QR code generation and verification.
- **Meta/Interakt:** WhatsApp Business API for the Patient Gateway.
- **OpenAI:** For the Dual-Mode AI engine.
- **Browser Web Speech API:** For Doctor voice dictation.

---

# 27. SECURITY REQUIREMENTS

- OTP-based Auth with JWT session management.
- PHI (Protected Health Information) encryption at rest (AES-256) and in transit (TLS 1.3).
- Strict role-based access control (RBAC) preventing Receptionists from viewing Analytics, and Doctors from managing Tenant config.

---

# 28. COMPLIANCE REQUIREMENTS

- **DPDP Act (India):** Data minimization and consent management.
- **IT Act 2000:** Data residency strictly within India (e.g., AWS ap-south-1).

---

# 29. COST ENGINEERING REPORT

- **Target MVP Infra Cost:** < ₹30,000/month for initial 10-20 clinics.
- **Optimization:** Utilize GPT-4o mini over GPT-4o to reduce AI inference costs by 10x.

---

# 30. FAILURE ENGINEERING REPORT

- **Network Drops:** Offline queue mode (PWA caching) allows Receptionists to keep operating; syncs upon reconnection.
- **AI Hallucination:** Mitigated by the immutable hard-gating of clinical decisions. AI can *draft* notes but cannot *save* a prescription.

---

# 31. MONITORING & OBSERVABILITY

- **Frontend:** Sentry for React crash reporting.
- **Backend:** Datadog/Prometheus for API latency and database load monitoring.
- **Business:** Tracking the ratio of Review Mode vs. AI Mode execution.

---

# 32. ANALYTICS REQUIREMENTS

- **Doctor BI:** Consultations per day, average time per patient.
- **Business BI:** Total revenue collected, pending dues, UPI vs. Cash split.

---

# 33. TESTING STRATEGY

- **Unit:** Jest for AI automation state logic.
- **E2E:** Playwright for critical paths: Login -> Register Patient -> Arrive Queue -> Consultation -> Payment.

---

# 34. DEPLOYMENT STRATEGY

- **Frontend:** Vercel or AWS Amplify.
- **Backend:** AWS ECS (Fargate) or Render for zero-downtime rolling deployments.

---

# 35. ROLLOUT STRATEGY

- **Phase 1 (Weeks 1-4):** Internal testing with mock data.
- **Phase 2 (Weeks 5-8):** Closed beta with 3 hand-picked clinics (Review mode only).
- **Phase 3 (Weeks 9-12):** Expand to 10 clinics, unlock AI mode and WhatsApp gateway.

---

# 36. RISKS & MITIGATIONS

- **Risk:** High dependency on WhatsApp API stability.
- **Mitigation:** Fallback to standard SMS/In-app alerts if WhatsApp delivery fails.
- **Risk:** Doctor resistance to digital consultation tools.
- **Mitigation:** Voice dictation is heavily emphasized to make digital input faster than handwriting.

---

# 37. ASSUMPTIONS

- Clinics have sufficient internet connectivity for a cloud-first SPA.
- Patients are comfortable scanning dynamic UPI QR codes.

---

# 38. OPEN QUESTIONS

- Does the WhatsApp chatbot need to handle complex medical queries, or strictly operational (scheduling/alerts) queries for MVP? *(Recommendation: Operational only for MVP).*
- Will the Google Form integration for patient registration be an embedded iframe or an API-driven webhook?

---

# 39. ROADMAP

- **Month 1:** Backend infrastructure, Auth, Database schema, Core APIs.
- **Month 2:** Frontend integration, Queue Management, Consultation Workspace, Payments.
- **Month 3:** Dual-Mode AI engine integration, WhatsApp Gateway, Analytics Dashboards.

---

# 40. RECOMMENDED BUILD ORDER

1. PostgreSQL Database & Node.js API foundation.
2. Auth & Role-based Routing.
3. Queue Management & Patient Directory.
4. Consultation Workspace.
5. Payment Processing.
6. Dashboards (Doctor & Business Analytics).
7. WhatsApp Integration & Patient Gateway.
8. Dual-Mode Automation Polish.

---

# 41. FINAL RECOMMENDATION

Execute immediately. The scope has been effectively narrowed to remove high-effort/low-impact features (Communication Center, Tasks, AI Voice Agent) while retaining the core value prop (Queue + Payments + Clinical Workflow + Dual-Mode AI). Proceed with building the backend infrastructure.
