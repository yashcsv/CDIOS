<div align="center">

# CDIOS — ClinicOS Decision Intelligence Operating System

### *A Palantir-grade market intelligence command center built to enable surgical GTM execution for a healthcare SaaS startup in Tier-2 India.*

[![HTML](https://img.shields.io/badge/Built%20With-HTML%2FJS%2FCSS-orange?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web)
[![Chart.js](https://img.shields.io/badge/Charts-Chart.js-ff6384?style=flat-square)](https://www.chartjs.org/)
[![Leaflet](https://img.shields.io/badge/Maps-Leaflet.js-green?style=flat-square)](https://leafletjs.com/)
[![Python](https://img.shields.io/badge/Pipeline-Python%203-blue?style=flat-square)](https://www.python.org/)
[![Data](https://img.shields.io/badge/Dataset-3%2C694%20Records-yellow?style=flat-square)](./data-dashboard/gr_intelligence.js)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey?style=flat-square)](./LICENSE)

</div>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Intelligence Modules](#intelligence-modules)
- [Data Sources & Collection](#data-sources--collection)
- [Data Pipeline Architecture](#data-pipeline-architecture)
- [Dashboard Architecture](#dashboard-architecture)
- [Repository Structure](#repository-structure)
- [Technologies Used](#technologies-used)
- [Quick Start](#quick-start)
- [Reproducing the Data Pipeline](#reproducing-the-data-pipeline)
- [Limitations & Assumptions](#limitations--assumptions)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

**CDIOS** (ClinicOS Decision Intelligence Operating System) is a self-contained, single-file intelligence dashboard that transforms raw healthcare market data into actionable, founder-grade business intelligence.

It was built to answer one fundamental question:

> *"Where exactly should ClinicOS — a healthcare SaaS startup — focus its first 90 days of GTM execution in Jabalpur, India?"*

This is not a generic analytics dashboard. It is a **decision platform** — purpose-engineered to support specific strategic, commercial, geographic, and product decisions for a founder, CEO, or GTM lead.

The final deliverable is a single `index.html` file (~230KB) that runs completely in the browser with zero backend dependencies, embedding:
- 3,694 golden records of healthcare entities
- 34 geographic zone analyses
- 29 segment-type breakdowns
- 12 intelligence modules
- Live interactive maps, charts, and priority queues

---

## Problem Statement

Most B2B SaaS companies enter markets using generic playbooks:
- Target everyone indiscriminately
- Spray-and-pray outreach
- Focus on largest entities first
- Generic feature pitches

This approach fails catastrophically in Tier-2 Indian healthcare because:

1. **The market is radically fragmented** — 1,435 single-doctor general clinics, each independently operated, each with different pain levels and digital maturity
2. **Geography matters at the street level** — a 2km difference can mean a 10x difference in conversion probability
3. **Segment heterogeneity is extreme** — a dental clinic and a hospital have completely different workflows, willingness-to-pay, and adoption barriers
4. **There is no CRM data, no conversion history, no industry benchmark** — founders are flying blind

CDIOS solves this by converting scraped public data into a structured intelligence system that prioritizes where to go, who to talk to, and what to sell.

---

## Key Features

| Feature | Description |
|---|---|
| 🎯 **Decision-First Architecture** | Every module answers a specific strategic question, not just displays data |
| 🗺️ **Live Interactive Map** | Leaflet.js map with 34 zones, P0–P3 color tiers, ICP concentration overlay, and per-zone drilldowns |
| 📊 **12 Intelligence Modules** | Exec Center → Founder Center → Market → Commercial → Geo → Competitive → Operational → Product → GTM → Expansion → AI Intel → Risk Center |
| 🔢 **3,694 Golden Records** | Deduplicated, classified, and enriched healthcare entity dataset |
| ⚡ **Zero Backend** | Entire system runs in a single HTML file — no server, no database, no API key |
| 📐 **Black-Ops Design System** | Dark command-center aesthetic inspired by Palantir Foundry and Bloomberg Terminal |
| 🧠 **CDIOS Intelligence Engine** | Python pipeline computes ICP scores, TAM/SAM/SOM, digital maturity, zone rankings, and more |
| 🔄 **Regenerable** | Run `compute_intelligence.py` after any data update to refresh all metrics |

---

## Intelligence Modules

| # | Module | Key Question Answered | Key Visual Component |
|---|---|---|---|
| 01 | **Exec Command Center** | What is the full market picture in 60 seconds? | Executive KPI bar, MRR Scenarios, P0-P3 Priority Queue |
| 02 | **Founder Command Center** | Where do I go and who do I call tomorrow? | Revenue-This-Week target list & first 10 customers sprint |
| 03 | **Market Intelligence** | Is this market worth entering? How fragmented is it? | Market Health composite scores & entity distribution breakdown |
| 04 | **Commercial Intelligence** | Where is the money? What is TAM/SAM/SOM? | Commercial waterfall funnel & segment yield matrix |
| 05 | **Geo Intelligence** | Which locality should I attack first? | Leaflet.js interactive 34-zone map with ICP concentration layer |
| 06 | **Competitive Intelligence** | What am I truly competing against? | Displacement matrix for Paper, WhatsApp, local EHRs, and Enterprise HMS |
| 07 | **Operational Intelligence** | What is the biggest workflow pain in clinics? | Legacy vs CDIOS friction chart across 4 clinic bottlenecks |
| 08 | **Product Intelligence** | What should be built first? What is the wedge? | Feature × Phase Priority Matrix (11 features across Now/Next/Later) |
| 09 | **GTM War Room** | Which zones get sales sprints? | Zone-level campaign planner & daily route queue |
| 10 | **Expansion Center** | Where does ClinicOS expand after Jabalpur? | Tier-2 market expansion index (Indore, Bhopal, Gwalior) |
| 11 | **AI Intelligence Center** | Where does AI automation generate the highest clinical ROI? | Segment PMF signal bar chart & clinical AI readiness score |
| 12 | **Risk Center** | What can go wrong? What are critical failure modes? | Probability × Impact risk registry & mitigation playbook |

---

## Data Sources & Collection

### Primary Dataset
- **Name**: Jabalpur Healthcare Golden Records V3
- **Records**: 3,694 healthcare entities
- **Source**: Scraped from Google Maps and public directories using Puppeteer-based crawlers
- **Coverage**: 34 zones across Jabalpur, Madhya Pradesh, India

### Data Fields Captured
| Field | Description |
|---|---|
| `Name` | Business/clinic name |
| `Type` | Entity classification (29 categories) |
| `Zone` | Geographic zone in Jabalpur |
| `Locality` | Sub-zone locality |
| `Phone` | Contact number (if available) |
| `Website` | Website URL (if available) |
| `Email` | Email address (if available) |
| `Rating` | Google Maps rating |
| `Reviews` | Review count |

---

## Data Pipeline Architecture

```
Raw Scrape Data (3,927 signals)
     │
     ▼
Golden Record Resolution (Deduplication + Normalization)
     │
     ▼
Jabalpur_Healthcare_Golden_Records_V3.csv (3,694 Verified Entities)
     │
     ├──▶ compute_intelligence.py ──▶ gr_intelligence.js (window.GR_INTELLIGENCE)
     ├──▶ enterprise_geo_pipeline.py ──▶ geo_intelligence.js (window.GEO_INTELLIGENCE)
     └──▶ geographic_analysis.geojson (34 Locality Boundary Polygons)
     │
     ▼
index.html (Single-File CDIOS Dashboard)
```

---

## Data Assets & File Lineage Guide

Here is the exact role, schema, and usage of every data asset in the CDIOS ecosystem:

| # | Data File | Role in System | How It Is Used |
|---|---|---|---|
| 1 | `Jabalpur_Healthcare_Golden_Records_V3.csv` | **Primary Single Source of Truth (SSOT)** | Master CSV containing 3,694 deduplicated healthcare entities with lat/lng, phone, entity classification, and digital readiness flags. Processed by `compute_intelligence.py`. |
| 2 | `gr_intelligence.js` | **Pre-Computed Runtime Intelligence Payload** | Generated by `compute_intelligence.py`. Embedded in `index.html` as `window.GR_INTELLIGENCE` to drive Executive KPIs, TAM/SAM/SOM funnels, ICP conversion matrices, and technology displacement stats with zero runtime latency. |
| 3 | `geo_intelligence.js` | **Pre-Computed GIS & Locality Layer** | Generated by `enterprise_geo_pipeline.py`. Embedded in `index.html` as `window.GEO_INTELLIGENCE` to feed coordinate pins, density ratings, and cluster boundaries into Leaflet.js in Module 05. |
| 4 | `geographic_analysis.geojson` | **Geospatial Vector Boundary Asset** | GeoJSON polygon collection for Jabalpur's 34 zones. Used for thematic choropleth mapping and spatial clustering of high-density medical hubs vs underserved healthcare deserts. |
| 5 | `Jabalpur_Locality_Intelligence.csv` | **Zone-Level Aggregated Metrics** | Ward-level aggregated counts of clinics, hospitals, pharmacies, and labs. Used for regional sales routing and geographic density ranking across 34 micro-markets. |
| 6 | `Jabalpur_Healthcare_Doctors.csv` | **Doctor & Practitioner Registry** | Schema for mapping individual specialists and doctors to clinic entities, tracking consultation fees and specialty concentrations. |
| 7 | `CLINICOS FRONTIER MARKET.md` | **Founder-Grade Strategic Launch Dossier** | Strategic market playbook defining the operational thesis (why Queue Management is the wedge over AI), priority launch zones (Wright Town, Napier Town), and 12/24/36-month ARR models. |
| 8 | `CLINICOS STATISTICAL INTELLIGENCE.md` | **Bayesian Probability & Math Engine** | Quantitative probability modeling (67% market success probability model, Bayesian conversion funnel, and price elasticity curves at ₹999/₹1,499/₹2,499). |
| 9 | `Jabalpur_Strategic_Intelligence_Report.md` | **Executive Briefing & Data Trust Audit** | 25-section executive report validating the 94% Data Trust Score, audit methodology, and operational risk mitigation for leadership. |
| 10 | `Jabalpur_Master_Knowledge_Base.md` | **Master Knowledge Base & SQL Schemas** | Monolithic 2,194-line offline engineering dossier consolidating all table schemas, 29 entity breakdowns, 1,300+ localities, and data pipelines. |
| 11 | `Jabalpur_Healthcare_Dashboard.xlsx` | **Offline Business Intelligence Workbook** | Multi-sheet Excel workbook with pivot tables, revenue projections, and offline lead lists for non-technical stakeholders and field sales reps. |
| 12 | `Scraping_Quality_Report.xlsx` | **Scraping QA & Data Quality Audit** | QA audit tracking entity resolution precision, deduplication rates, null contact frequencies, and geocoding coverage across crawl batches. |

---

## Repository Structure

```
CDIOS/
├── index.html                           # 🎯 Primary deliverable (complete standalone dashboard)
├── README.md                            # Professional GitHub README
├── TECHNICAL_DOCUMENTATION.md           # Complete technical documentation & architecture spec
├── .gitignore                           # Exclude dev artifacts, prompts, raw data, temp files
├── LICENSE                              # License (Apache-2.0)
│
├── compute_intelligence.py              # 🔄 Core intelligence compute engine
├── enterprise_geo_pipeline.py           # Geo pipeline
├── semantic_classifier.py               # Entity classification engine
│
└── data-dashboard/                      # Production data & intelligence layer
    ├── gr_intelligence.js               # Auto-generated SSOT intelligence object
    ├── geo_intelligence.js              # Geographic intelligence object
    ├── Jabalpur_Healthcare_Golden_Records_V3.csv
    ├── Jabalpur_Locality_Intelligence.csv
    ├── geographic_analysis.geojson
    ├── CLINICOS FRONTIER MARKET.md
    └── CLINICOS STATISTICAL INTELLIGENCE.md
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **HTML5** | Dashboard structure and semantic layout |
| **CSS3 (Vanilla)** | Complete design system — no external CSS framework |
| **JavaScript (ES6+)** | All rendering logic, bridge functions, interactivity |
| **Chart.js** | Bar charts (Operational Intelligence, AI module) |
| **Leaflet.js** | Interactive geographic map with zone overlays |
| **Python 3** | Data processing pipeline (`compute_intelligence.py`) |
| **Inter + Space Grotesk** | Typography (Google Fonts) |

---

## Quick Start

Since the dashboard is a single self-contained HTML file, running it is straightforward:

### Option 1: Local Development Server (Recommended)
```bash
# Clone the repository
git clone https://github.com/yashcsv/CDIOS.git
cd CDIOS

# Run with Python built-in server
python3 -m http.server 5500
# Open in browser: http://localhost:5500
```

### Option 2: Using Node.js
```bash
npx serve .
# Open in browser: http://localhost:3000
```

---

## Reproducing the Data Pipeline

To regenerate the intelligence files after updating the source dataset:

```bash
# 1. Verify source data
ls data-dashboard/Jabalpur_Healthcare_Golden_Records_V3.csv

# 2. Run the intelligence pipeline
python3 compute_intelligence.py

# 3. Output files are refreshed automatically
# data-dashboard/gr_intelligence.js
# data-dashboard/geo_intelligence.js

# 4. Reload index.html in browser
```

The compute pipeline uses **only Python standard library** modules (`csv`, `json`, `math`, `os`, `collections`, `datetime`) — zero external dependencies.

---

## Limitations & Assumptions

| Limitation | Details |
|---|---|
| **Static Dataset** | 3,694 records reflect a point-in-time scrape |
| **Pricing Assumption** | ARPU of ₹1,499/mo is a product hypothesis |
| **ICP Scores** | Scores are business-validated estimates calibrated by domain logic |
| **Zero Runtime Compute** | All intelligence is pre-computed at build time |

---

## Future Improvements

- [ ] Automate scheduled data refresh pipeline with live scraping
- [ ] Add CSV export for filtered P0 leads directly from the dashboard
- [ ] Multi-city expansion modeling (Indore, Bhopal, Raipur)
- [ ] CRM integration layer to track outreach status per lead
- [ ] Mobile-optimized field sales view

---

## License

This project is licensed under the **Apache-2.0 License**. See [LICENSE](./LICENSE) for details.
