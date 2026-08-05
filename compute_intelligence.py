"""
CDIOS Enterprise Intelligence Engine — compute_intelligence.py
Reads Golden Records V3 CSV → outputs data/gr_intelligence.js
Run this ONCE after any GR V3 update. Zero runtime cost to dashboard.

Author: Antigravity AI / ECEOS Protocol
"""

import csv
import json
import math
import os
from collections import Counter, defaultdict
from datetime import datetime

GR_V3_PATH = 'data/Jabalpur_Healthcare_Golden_Records_V3.csv'
OUTPUT_JS   = 'data/gr_intelligence.js'

# ─────────────────────────────────────────────
# ICP DEFINITIONS (business-validated scores)
# ─────────────────────────────────────────────
ICP_SCORES = {
    'GENERAL_CLINIC':         {'score': 96, 'priority': 'P0', 'action': 'ATTACK NOW',   'segment': 'Single Doctor Clinic',   'conversionRate': '1 in 5 demos'},
    'ENT_CLINIC':             {'score': 94, 'priority': 'P0', 'action': 'ATTACK NOW',   'segment': 'ENT Clinic',             'conversionRate': '1 in 4 demos'},
    'DENTAL_CLINIC':          {'score': 93, 'priority': 'P0', 'action': 'ATTACK NOW',   'segment': 'Dental Clinic',          'conversionRate': '1 in 5 demos'},
    'PEDIATRIC_CLINIC':       {'score': 88, 'priority': 'P1', 'action': 'QUEUE UP',     'segment': 'Pediatric Clinic',       'conversionRate': '1 in 6 demos'},
    'ORTHOPEDIC_CLINIC':      {'score': 86, 'priority': 'P1', 'action': 'QUEUE UP',     'segment': 'Orthopedic Clinic',      'conversionRate': '1 in 7 demos'},
    'DERMATOLOGY_CLINIC':     {'score': 84, 'priority': 'P1', 'action': 'QUEUE UP',     'segment': 'Dermatology Clinic',     'conversionRate': '1 in 7 demos'},
    'GYNECOLOGY_CLINIC':      {'score': 82, 'priority': 'P1', 'action': 'QUEUE UP',     'segment': 'Gynecology Clinic',      'conversionRate': '1 in 8 demos'},
    'EYE_CLINIC':             {'score': 80, 'priority': 'P1', 'action': 'QUEUE UP',     'segment': 'Eye Clinic',             'conversionRate': '1 in 8 demos'},
    'PHYSIOTHERAPY_CENTER':   {'score': 78, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Physiotherapy Center',   'conversionRate': '1 in 8 demos'},
    'NEUROLOGY_CLINIC':       {'score': 76, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Neurology Clinic',       'conversionRate': '1 in 9 demos'},
    'PSYCHIATRY_CLINIC':      {'score': 75, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Psychiatry Clinic',      'conversionRate': '1 in 9 demos'},
    'CARDIOLOGY_CLINIC':      {'score': 74, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Cardiology Clinic',      'conversionRate': '1 in 10 demos'},
    'PATHOLOGY_LAB':          {'score': 72, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Pathology Lab',          'conversionRate': '1 in 10 demos'},
    'DIAGNOSTIC_CENTER':      {'score': 70, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Diagnostic Center',      'conversionRate': '1 in 10 demos'},
    'HOMEOPATHY_CLINIC':      {'score': 68, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Homeopathy Clinic',      'conversionRate': '1 in 10 demos'},
    'AYURVEDA_CLINIC':        {'score': 65, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Ayurveda Clinic',        'conversionRate': '1 in 12 demos'},
    'GASTROENTEROLOGY_CLINIC':{'score': 72, 'priority': 'P2', 'action': 'PLAN',         'segment': 'GI Clinic',              'conversionRate': '1 in 9 demos'},
    'NEPHROLOGY_CLINIC':      {'score': 70, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Nephrology Clinic',      'conversionRate': '1 in 10 demos'},
    'ONCOLOGY_CLINIC':        {'score': 68, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Oncology Clinic',        'conversionRate': '1 in 12 demos'},
    'IMAGING_CENTER':         {'score': 65, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Imaging Center',         'conversionRate': '1 in 12 demos'},
    'SURGICAL_CENTER':        {'score': 62, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Surgical Center',        'conversionRate': '1 in 12 demos'},
    'POLYCLINIC':             {'score': 60, 'priority': 'P2', 'action': 'PLAN',         'segment': 'Polyclinic',             'conversionRate': '1 in 12 demos'},
    'NURSING_HOME':           {'score': 58, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Nursing Home',           'conversionRate': '1 in 15 demos'},
    'MULTISPECIALTY_HOSPITAL':{'score': 55, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Multi-Specialty Hospital','conversionRate': '1 in 15 demos'},
    'HOSPITAL':               {'score': 52, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Hospital',               'conversionRate': '1 in 20+ demos'},
    'SUPERSPECIALTY_HOSPITAL':{'score': 48, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Super-Specialty Hospital','conversionRate': '1 in 25+ demos'},
    'MATERNITY_HOSPITAL':     {'score': 55, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Maternity Hospital',     'conversionRate': '1 in 15 demos'},
    'PHARMACY':               {'score': 40, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Pharmacy',               'conversionRate': '1 in 20+ demos'},
    'UNANI_CLINIC':           {'score': 35, 'priority': 'P3', 'action': 'DEFER',        'segment': 'Unani Clinic',           'conversionRate': '1 in 20+ demos'},
}

P0_TYPES = {t for t, v in ICP_SCORES.items() if v['priority'] == 'P0'}
P1_TYPES = {t for t, v in ICP_SCORES.items() if v['priority'] == 'P1'}
P0_P1_TYPES = P0_TYPES | P1_TYPES
PRICE_PER_ENTITY_MONTHLY = 1499  # INR

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
def load_rows():
    with open(GR_V3_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def is_valid(val):
    return bool(val and val.strip() and val.strip().lower() not in ['n/a', 'none', 'nan', ''])

# ─────────────────────────────────────────────
# DIGITAL MATURITY SCORE: 0–4 per entity
# ─────────────────────────────────────────────
def digital_maturity(row):
    score = 0
    if is_valid(row.get('Phone', '')): score += 1
    if is_valid(row.get('Website', '')): score += 2  # weighted double
    if is_valid(row.get('Email', '')): score += 1
    return score  # max = 4

# ─────────────────────────────────────────────
# COMPUTE AGGREGATES
# ─────────────────────────────────────────────
def compute(rows):
    total = len(rows)

    # ── Global stats
    with_phone   = sum(1 for r in rows if is_valid(r.get('Phone', '')))
    with_website = sum(1 for r in rows if is_valid(r.get('Website', '')))
    with_email   = sum(1 for r in rows if is_valid(r.get('Email', '')))

    # ── By Type
    by_type = defaultdict(list)
    for r in rows:
        by_type[r.get('Type', '').strip()].append(r)

    type_aggregates = {}
    for t, recs in sorted(by_type.items()):
        n = len(recs)
        wp = sum(1 for r in recs if is_valid(r.get('Phone', '')))
        ww = sum(1 for r in recs if is_valid(r.get('Website', '')))
        we = sum(1 for r in recs if is_valid(r.get('Email', '')))
        dm_scores = [digital_maturity(r) for r in recs]
        icp_meta  = ICP_SCORES.get(t, {'score': 30, 'priority': 'P3', 'action': 'DEFER', 'segment': t.replace('_', ' ').title(), 'conversionRate': 'N/A'})
        type_aggregates[t] = {
            'type':               t,
            'count':              n,
            'withPhone':          wp,
            'phonePercent':       round(100 * wp / n) if n else 0,
            'withWebsite':        ww,
            'websitePercent':     round(100 * ww / n) if n else 0,
            'withEmail':          we,
            'emailPercent':       round(100 * we / n) if n else 0,
            'digitalMaturityAvg': round(sum(dm_scores) / n, 2) if n else 0,
            'digitalMaturityPct': round(100 * sum(dm_scores) / (n * 4)) if n else 0,
            'icpScore':           icp_meta['score'],
            'priority':           icp_meta['priority'],
            'action':             icp_meta['action'],
            'segment':            icp_meta['segment'],
            'conversionRate':     icp_meta['conversionRate'],
            'reachableMRR':       n * PRICE_PER_ENTITY_MONTHLY,
        }

    # ── By Zone
    by_zone = defaultdict(list)
    for r in rows:
        by_zone[r.get('Zone', '').strip()].append(r)

    zone_aggregates = {}
    max_zone_count  = max(len(v) for v in by_zone.values()) if by_zone else 1

    for z, recs in sorted(by_zone.items()):
        n     = len(recs)
        wp    = sum(1 for r in recs if is_valid(r.get('Phone', '')))
        ww    = sum(1 for r in recs if is_valid(r.get('Website', '')))
        icp_n = sum(1 for r in recs if r.get('Type', '').strip() in P0_P1_TYPES)
        p0_n  = sum(1 for r in recs if r.get('Type', '').strip() in P0_TYPES)
        type_counts = dict(Counter(r.get('Type','').strip() for r in recs))
        dominant_type = max(type_counts, key=type_counts.get) if type_counts else 'N/A'

        # Normalized density (0–100)
        density_score = round(100 * n / max_zone_count)
        # Reachability (0–100)
        reach_score   = round(100 * wp / n) if n else 0
        # ICP concentration (0–100)
        icp_conc      = round(100 * icp_n / n) if n else 0
        # Digital maturity (0–100)
        dm_index      = round(100 * ww / n) if n else 0

        # Territory Attractiveness Score (composite)
        # Weights: ICP 40%, Reach 30%, Density 20%, Digital 10%
        attract_score = round(
            icp_conc * 0.40 +
            reach_score * 0.30 +
            density_score * 0.20 +
            dm_index * 0.10
        )

        zone_aggregates[z] = {
            'zone':              z,
            'total':             n,
            'withPhone':         wp,
            'phonePercent':      reach_score,
            'withWebsite':       ww,
            'websitePercent':    dm_index,
            'icpCount':          icp_n,
            'p0Count':           p0_n,
            'icpPercent':        icp_conc,
            'dominantType':      dominant_type,
            'densityScore':      density_score,
            'reachabilityScore': reach_score,
            'digitalIndex':      dm_index,
            'attractScore':      attract_score,
            'byType':            type_counts,
            'potentialMRR':      icp_n * PRICE_PER_ENTITY_MONTHLY,
        }

    # ── By Locality (top 100)
    by_locality = defaultdict(list)
    for r in rows:
        loc = r.get('Locality', '').strip()
        if loc and loc.lower() not in ['unknown', '']:
            by_locality[loc].append(r)

    locality_list = []
    for loc, recs in sorted(by_locality.items(), key=lambda x: -len(x[1]))[:100]:
        n     = len(recs)
        icp_n = sum(1 for r in recs if r.get('Type','').strip() in P0_P1_TYPES)
        zone  = Counter(r.get('Zone','').strip() for r in recs).most_common(1)[0][0]
        locality_list.append({
            'locality':  loc,
            'zone':      zone,
            'total':     n,
            'icpCount':  icp_n,
            'icpPercent': round(100 * icp_n / n) if n else 0,
        })

    # ── Market Fragmentation (Shannon Entropy of type distribution)
    type_counts = Counter(r.get('Type','').strip() for r in rows)
    probs = [c / total for c in type_counts.values()]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    max_entropy = math.log2(len(type_counts)) if type_counts else 1
    fragmentation_score = round(100 * entropy / max_entropy) if max_entropy else 0

    # ── TAM / SAM / SOM
    icp_p0_count    = sum(1 for r in rows if r.get('Type','').strip() in P0_TYPES)
    icp_p0p1_count  = sum(1 for r in rows if r.get('Type','').strip() in P0_P1_TYPES)
    tam_mrr         = total * PRICE_PER_ENTITY_MONTHLY
    sam_mrr         = icp_p0p1_count * PRICE_PER_ENTITY_MONTHLY
    som_y1_units    = 250
    som_mrr         = som_y1_units * PRICE_PER_ENTITY_MONTHLY

    # ── Zone ranking by attract score
    zone_ranking = sorted(zone_aggregates.values(), key=lambda z: -z['attractScore'])

    # ── Type ranking by (icpScore × count)
    type_ranking = sorted(type_aggregates.values(), key=lambda t: -(t['icpScore'] * t['count']))

    # ── Compile output
    intelligence = {
        '_meta': {
            'generatedAt':   datetime.now().isoformat(),
            'sourceFile':    GR_V3_PATH,
            'totalRecords':  total,
            'version':       'V3',
        },
        'summary': {
            'totalEntities':      total,
            'icpP0Count':         icp_p0_count,
            'icpP0P1Count':       icp_p0p1_count,
            'withPhone':          with_phone,
            'phonePercent':       round(100 * with_phone / total),
            'withWebsite':        with_website,
            'websitePercent':     round(100 * with_website / total),
            'withEmail':          with_email,
            'emailPercent':       round(100 * with_email / total),
            'totalZones':         len(zone_aggregates),
            'totalLocalities':    len(by_locality),
            'totalTypes':         len(type_aggregates),
            'fragmentationScore': fragmentation_score,
            'tam_mrr':            tam_mrr,
            'sam_mrr':            sam_mrr,
            'som_mrr_y1':         som_mrr,
            'tam_arr':            tam_mrr * 12,
            'sam_arr':            sam_mrr * 12,
            'som_arr_y1':         som_mrr * 12,
        },
        'byType':       type_aggregates,
        'byZone':       zone_aggregates,
        'byLocality':   locality_list,
        'zoneRanking':  zone_ranking,
        'typeRanking':  type_ranking,
    }

    return intelligence


def write_js(intelligence):
    js = f"""// ═══════════════════════════════════════════════════════════════════
// CDIOS ENTERPRISE INTELLIGENCE ENGINE — gr_intelligence.js
// Generated: {intelligence['_meta']['generatedAt']}
// Source: {intelligence['_meta']['sourceFile']}
// Total Records: {intelligence['_meta']['totalRecords']}
// DO NOT EDIT MANUALLY — regenerate via compute_intelligence.py
// ═══════════════════════════════════════════════════════════════════

window.GR_INTELLIGENCE = {json.dumps(intelligence, indent=2, ensure_ascii=False)};

// ─── Convenience Accessors ───────────────────────────────────────────
window.GRI = window.GR_INTELLIGENCE;

window.GRI.getZone = (name) => window.GRI.byZone[name] || null;
window.GRI.getType = (name) => window.GRI.byType[name] || null;
window.GRI.topZones = (n=10) => window.GRI.zoneRanking.slice(0, n);
window.GRI.topTypes = (n=10) => window.GRI.typeRanking.slice(0, n);
window.GRI.icpTypes = () => window.GRI.typeRanking.filter(t => ['P0','P1'].includes(t.priority));

console.log('[GR_INTELLIGENCE] Loaded. Total entities:', window.GRI.summary.totalEntities,
    '| Zones:', window.GRI.summary.totalZones,
    '| ICP P0:', window.GRI.summary.icpP0Count,
    '| ICP P0+P1:', window.GRI.summary.icpP0P1Count);
"""
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"[CDIOS Intelligence Engine] Written → {OUTPUT_JS}")
    print(f"  Total entities : {intelligence['summary']['totalEntities']}")
    print(f"  ICP P0         : {intelligence['summary']['icpP0Count']}")
    print(f"  ICP P0+P1      : {intelligence['summary']['icpP0P1Count']}")
    print(f"  Zones          : {intelligence['summary']['totalZones']}")
    print(f"  TAM MRR        : ₹{intelligence['summary']['tam_mrr']:,}")
    print(f"  SAM MRR        : ₹{intelligence['summary']['sam_mrr']:,}")
    print(f"  Fragmentation  : {intelligence['summary']['fragmentationScore']}/100")


if __name__ == '__main__':
    print("[CDIOS Intelligence Engine] Reading Golden Records V3...")
    rows = load_rows()
    print(f"  Loaded {len(rows)} records.")
    intelligence = compute(rows)
    write_js(intelligence)
    print("[CDIOS Intelligence Engine] COMPLETE. Dashboard intelligence layer ready.")
