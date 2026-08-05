# CDIOS — Technical Documentation
## ClinicOS Decision Intelligence Operating System

**Version**: 3.0 | **Dataset**: V3 (3,694 records) | **City**: Jabalpur, MP, India

---

## 1. Project Architecture Overview

CDIOS is a **static, self-contained intelligence platform** delivered as a single HTML file. There is no backend, no API, no database at runtime. All intelligence is pre-computed offline by a Python pipeline and embedded as JavaScript objects loaded at page startup.

```
[ Raw Scrape Data ]
        │
        ▼
[ Golden Record Resolution ]  ←  dedup + normalize
        │
        ▼
[ Golden_Records_V3.csv ]     ←  3,694 rows, source of truth
        │
        ▼
[ compute_intelligence.py ]   ←  Python pipeline (run once)
        │
        ├──▶ gr_intelligence.js   (window.GR_INTELLIGENCE)
        └──▶ geo_intelligence.js  (window.GEO_INTELLIGENCE)
                │
                ▼
        [ index.html ]            ←  THE FINAL PRODUCT
         ├── CSS Design System
         ├── HTML Module Shells
         └── JS Bridge Engine (12 renderers)
```

**Design Rationale**: Zero-runtime-cost architecture means the dashboard loads instantly, works offline, requires no server, and can be shared as a single file. All intelligence computation happens once at build time.

---

## 2. Repository File Map

### Primary Artifact
| File | Role |
|------|------|
| `index.html` | Complete single-file intelligence dashboard — 3,675 lines, ~233KB |

### Data Layer & Asset Directory
| File | Role & Usage Description |
|------|--------------------------|
| `data-dashboard/Jabalpur_Healthcare_Golden_Records_V3.csv` | **Single Source of Truth (SSOT)**: 3,694 verified healthcare entities, geocoded and deduplicated from 3,927 raw crawl points. Processed by `compute_intelligence.py`. |
| `data-dashboard/gr_intelligence.js` | **Pre-Computed Runtime Object (`window.GR_INTELLIGENCE`)**: Global data payload containing pre-computed summary metrics, ICP breakdown tables, commercial waterfall funnel numbers, and technology adoption scores. |
| `data-dashboard/geo_intelligence.js` | **GIS Layer (`window.GEO_INTELLIGENCE`)**: Zone coordinates, locality rankings, and entity clusters used to render Leaflet.js interactive maps in Module 05. |
| `data-dashboard/geographic_analysis.geojson` | **Geospatial Vector Asset**: Boundary polygon GeoJSON for Jabalpur's 34 zones used for spatial clustering and identifying healthcare deserts. |
| `data-dashboard/Jabalpur_Locality_Intelligence.csv` | **Zone Aggregations**: 1,321 locality records summarizing healthcare entities, hospitals, clinics, labs, and pharmacies per ward. |
| `data-dashboard/Jabalpur_Healthcare_Doctors.csv` | **Doctor Registry Schema**: Structured practitioner-level data mapping physicians and specialists to clinics with fee and qualification schemas. |
| `data-dashboard/CLINICOS FRONTIER MARKET.md` | **Strategic Launch Dossier**: 990-line founder-grade document outlining the operational wedge (Queue Management), launch cluster sequencing, and 36-month ARR models. |
| `data-dashboard/CLINICOS STATISTICAL INTELLIGENCE.md` | **Bayesian Mathematical Engine**: Mathematical and probability modeling documenting the 67% overall success probability model, Bayesian conversion funnel, and price elasticity curve. |
| `data-dashboard/Jabalpur_Strategic_Intelligence_Report.md` | **Executive Briefing & Audit**: 25-section executive report validating the 94% Data Trust Score, audit methodology, and GTM field survey workflows. |
| `data-dashboard/Jabalpur_Healthcare_Dashboard.xlsx` | **Offline BI & Field Sales Workbook**: Multi-tab Excel spreadsheet with pivot tables and offline target lead sheets for ground surveyors. |
| `data-dashboard/Scraping_Quality_Report.xlsx` | **QA Audit Report**: Data quality evaluation tracking phone completeness, deduplication efficacy, and geocoding precision across crawl runs. |
| `Jabalpur_Master_Knowledge_Base.md` | **Master Engineering Knowledge Base**: Monolithic 2,194-line engineering reference containing all SQLite table schemas, entity distributions, and pipeline lineage. |

### Intelligence Pipeline
| File | Role |
|------|------|
| `compute_intelligence.py` | Python pipeline: CSV → JS intelligence objects (`gr_intelligence.js`) |
| `enterprise_geo_pipeline.py` | Geographic enrichment pipeline → `geo_intelligence.js` |
| `semantic_classifier.py` | Semantic keyword matcher for 29 canonical entity types |

---

## 3. Data Collection Methodology

### 3.1 Scraping Strategy
Healthcare entities were discovered via an automated Puppeteer-based crawling engine across multiple public directories including **Google Maps, Justdial, Practo, and state medical registries**. The strategy executed a dense multi-zone query matrix (e.g., "dentist in Wright Town Jabalpur", "pediatrician near Vijay Nagar Jabalpur") to ensure exhaustive street-level coverage without triggering rate limits.

Queries were structured as:
```
{entity_type} in {locality}, Jabalpur
```

Across 29 entity types × 34 zones × multiple keyword and directory variations = **10,000+ query combinations** executed over 70+ hours of continuous crawling.

### 3.2 Entity Classification
Raw scraped names were semantically classified into 29 canonical types using `semantic_classifier.py`. Classification used keyword matching with fallback rules:
- "dental" → `DENTAL_CLINIC`
- "hospital" → `HOSPITAL` (with sub-classification rules)
- "physio*" → `PHYSIOTHERAPY_CENTER`

### 3.3 Golden Record Resolution
Duplicate detection was performed on name + locality pairs, collapsing near-duplicates (string similarity > 0.85) into single golden records. The output was `Jabalpur_Healthcare_Golden_Records_V3.csv` — 3,694 unique entities.

---

## 4. Intelligence Pipeline: compute_intelligence.py

This is the core data transformation engine. It reads the CSV and outputs all intelligence as JS objects embeddable in the HTML dashboard.

### 4.1 ICP Score Definitions

Business-validated scores (0–100) for each entity type, manually calibrated by domain logic:

```python
ICP_SCORES = {
    'GENERAL_CLINIC':   {'score': 96, 'priority': 'P0', 'action': 'ATTACK NOW'},
    'ENT_CLINIC':       {'score': 94, 'priority': 'P0', 'action': 'ATTACK NOW'},
    'DENTAL_CLINIC':    {'score': 93, 'priority': 'P0', 'action': 'ATTACK NOW'},
    'PEDIATRIC_CLINIC': {'score': 88, 'priority': 'P1', 'action': 'QUEUE UP'},
    ...
    'HOSPITAL':         {'score': 52, 'priority': 'P3', 'action': 'DEFER'},
    'PHARMACY':         {'score': 40, 'priority': 'P3', 'action': 'DEFER'},
}
```

**Scoring Rationale**: ICP score correlates with expected conversion difficulty, workflow complexity alignment, digital readiness, and price sensitivity. General clinics score 96 because they have high pain (paper-based OPD), low switching cost from paper, and a receptive single decision-maker.

### 4.2 Digital Maturity Score (per entity)

```python
def digital_maturity(row):
    score = 0
    if phone:   score += 1   # basic reachability
    if website: score += 2   # weighted double (active digital presence)
    if email:   score += 1   # email = higher maturity
    return score  # max = 4 → converted to % = score/4 × 100
```

### 4.3 TAM / SAM / SOM Calculation

```python
PRICE_PER_ENTITY_MONTHLY = 1499  # INR

TAM_MRR = total_entities × 1499
SAM_MRR = (P0 + P1 entities) × 1499
SOM_MRR_Y1 = SAM_MRR × 0.112   # ~11.2% Y1 penetration assumption

TAM_ARR = TAM_MRR × 12
SAM_ARR = SAM_MRR × 12
SOM_ARR_Y1 = SOM_MRR_Y1 × 12
```

### 4.4 Zone Aggregation

For every zone, the pipeline computes:
- `total` — count of all entities in zone
- `withPhone`, `withWebsite`, `withEmail` — contact coverage
- `icpCount` — count of P0+P1 entities
- `p0Count` — count of P0 entities only
- `dominantType` — most frequent entity type
- `densityScore` — `(total / max_zone_total) × 100`
- `reachabilityScore` — `(withPhone / total) × 100`
- `digitalIndex` — `(withWebsite / total) × 100`
- `attractScore` — composite: `0.4×density + 0.3×reachability + 0.3×digitalIndex`
- `potentialMRR` — `icpCount × 1499`

---

## 5. Dashboard Architecture (index.html)

### 5.1 CSS Design System

All CSS is inline in `<style>` tags. Key design tokens:

```css
:root {
  --bg-deep:           #050505;  /* Ultra-deep black — page background */
  --bg-surface:        #111111;  /* Card/panel surface */
  --border-color:      #222222;  /* Subtle borders */
  --accent-tactical:   #FFD100;  /* Primary action color — tactical yellow */
  --text-primary:      #ffffff;
  --text-secondary:    #888888;
  --font-ui:           'Inter', sans-serif;
  --font-heading:      'Space Grotesk', sans-serif;
  --font-data:         'Space Grotesk', monospace;
}
```

### 5.2 HTML Module Structure

The main content area is a vertical stack of `<div class="module">` containers:

```html
<main id="main-content">
  <div id="mod-exec"        class="module"> ... </div>
  <div id="mod-founder"     class="module"> ... </div>
  <div id="mod-market"      class="module"> ... </div>
  <div id="mod-commercial"  class="module"> ... </div>
  <div id="mod-geo"         class="module"> ... </div>
  <div id="mod-compete"     class="module"> ... </div>
  <div id="mod-ops"         class="module"> ... </div>
  <div id="mod-product"     class="module"> ... </div>
  <div id="mod-gtm"         class="module"> ... </div>
  <div id="mod-expand"      class="module"> ... </div>
  <div id="mod-ai"          class="module"> ... </div>
  <div id="mod-risk"        class="module"> ... </div>
</main>
```

### 5.3 JS Bridge Architecture

The JS bridge is a `DOMContentLoaded` handler that reads `window.GR_INTELLIGENCE` and `window.GEO_INTELLIGENCE` and renders dynamic HTML into the containers.

```javascript
document.addEventListener('DOMContentLoaded', () => {
  if (window.GR_INTELLIGENCE) {
    const gr  = window.GR_INTELLIGENCE;
    const grs = gr.summary;

    // Bridge logic for each module
  }
});
```

---

## 6. Reproduction Instructions

To regenerate the intelligence dataset from scratch:

```bash
# Run intelligence compute pipeline
python3 compute_intelligence.py

# Run geographic intelligence pipeline
python3 enterprise_geo_pipeline.py

# Launch dashboard locally
python3 -m http.server 5500
```
