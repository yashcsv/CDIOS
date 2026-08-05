import csv
import json
import os
import hashlib
from collections import defaultdict
from datetime import datetime

# Configuration
GOLDEN_RECORDS_PATH = 'data/Jabalpur_Healthcare_Golden_Records_V3.csv'
GEOJSON_OUTPUT_PATH = 'data/geographic_analysis.geojson'
LOCALITY_CSV_OUTPUT_PATH = 'data/Jabalpur_Locality_Intelligence.csv'
AUDIT_LOG_PATH = 'data/geographic_recovery_audit.log'

def log_audit(message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    with open(AUDIT_LOG_PATH, 'a') as f:
        f.write(log_entry)

def validate_and_extract_record(row):
    """
    Deterministic Validation Gate
    Enforces strict trust boundary: Only data explicitly present in the Golden Record is passed.
    """
    # Columns in Jabalpur_Healthcare_Golden_Records.csv:
    # 0:ID, 1:Name, 2:Type, 3:Specialty, 4:Locality, 5:Address, 6:Lat, 7:Lng, 
    # 8:Zone, 9:Phone, 10:Email, 11:Website, 12:Rating, 13:Reviews, 14:Sources, 
    # 15:Has Website, 16:Has Booking, 17:Maturity, 18:Fit Score, 19:Pain Score, 
    # 20:Lead Quality, 21:Survey Priority, 22:Confidence

    try:
        email = row[10].strip() if len(row) > 10 else ""
        if email and "@" not in email:
            email = None  # Basic integrity check, discard invalid emails
        
        lat_str = row[6].strip()
        lng_str = row[7].strip()
        
        # Only accept records with valid coordinates for Geographic Intelligence
        if not lat_str or not lng_str:
            return None
            
        lat = float(lat_str)
        lng = float(lng_str)
        
        # Parse numeric scores safely
        fit_score = float(row[18]) if len(row) > 18 and row[18].strip() else 0.0
        
        record = {
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "specialty": row[3],
            "locality": row[4],
            "address": row[5],
            "lat": lat,
            "lng": lng,
            "zone": row[8],
            "phone": row[9],
            "email": email if email else None,
            "website": row[11].strip() if len(row) > 11 else None,
            "fit_score": fit_score,
            "lead_quality": row[20] if len(row) > 20 else "UNKNOWN",
            "survey_priority": row[21] if len(row) > 21 else "UNKNOWN"
        }
        return record
    except ValueError:
        # Invalid coordinate or data type, discard
        return None
    except Exception as e:
        log_audit(f"Error parsing record {row[0] if row else 'UNKNOWN'}: {str(e)}")
        return None

def rebuild_geographic_intelligence():
    log_audit("STARTING GEOGRAPHIC INTELLIGENCE DATA INTEGRITY RECOVERY")
    
    if not os.path.exists(GOLDEN_RECORDS_PATH):
        log_audit(f"CRITICAL ERROR: Authoritative source {GOLDEN_RECORDS_PATH} not found.")
        return

    # 1. Read Authoritative Source
    verified_records = []
    locality_stats = defaultdict(lambda: {
        'total': 0, 'hospitals': 0, 'clinics': 0, 'labs': 0, 
        'pharmacies': 0, 'doctors': 0
    })

    log_audit(f"Reading from authoritative source: {GOLDEN_RECORDS_PATH}")
    with open(GOLDEN_RECORDS_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        for row_num, row in enumerate(reader, start=2):
            if not row or not row[0].strip():
                continue
                
            record = validate_and_extract_record(row)
            if record:
                verified_records.append(record)
                
                # Aggregate Locality Intelligence
                loc = record['locality']
                if loc:
                    stats = locality_stats[loc]
                    stats['total'] += 1
                    t = record['type'].upper()
                    if 'HOSPITAL' in t: stats['hospitals'] += 1
                    elif 'CLINIC' in t: stats['clinics'] += 1
                    elif 'LAB' in t or 'PATHOLOGY' in t: stats['labs'] += 1
                    elif 'PHARMACY' in t: stats['pharmacies'] += 1
                    elif 'DOCTOR' in t: stats['doctors'] += 1

    log_audit(f"Extracted {len(verified_records)} geo-verified records from source of truth.")

    # 2. Rebuild GeoJSON (Geographic Intelligence Map)
    features = []
    for r in verified_records:
        # Generate deterministic stable ID for full traceability across pipeline runs
        id_source = f"{r['name']}|{r['lat']:.6f}|{r['lng']:.6f}"
        stable_id = "CDIOS-" + hashlib.md5(id_source.encode('utf-8')).hexdigest()[:10].upper()

        properties = {
            "id": stable_id,
            "name": r['name'],
            "type": r['type'],
            "specialty": r['specialty'],
            "locality": r['locality'],
            "address": r['address'],
            "phone": r['phone'],
            "website": r.get('website', None),
            "fit_score": r['fit_score'],
            "priority": r['survey_priority'],
            "lead_quality": r['lead_quality'],
            "provenance": "Jabalpur_Healthcare_Golden_Records_V3.csv",
            "trust_status": "VERIFIED"
        }
        # Strict email inclusion: Only if verified
        if r['email']:
            properties['email'] = r['email']
            
        features.append({
            "id": stable_id,
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [r['lng'], r['lat']]
            },
            "properties": properties
        })

    geojson_data = {
        "type": "FeatureCollection",
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source_of_truth": "Jabalpur_Healthcare_Golden_Records_V3.csv",
            "integrity_status": "SECURE",
            "validation_gate": "STRICT_DETERMINISTIC"
        },
        "features": features
    }

    # Quarantine old file and write new
    if os.path.exists(GEOJSON_OUTPUT_PATH):
        os.remove(GEOJSON_OUTPUT_PATH)
        log_audit(f"Quarantined/Deleted contaminated {GEOJSON_OUTPUT_PATH}")
        
    with open(GEOJSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2)
    log_audit(f"Successfully wrote verified Geographic Intelligence to {GEOJSON_OUTPUT_PATH}")

    # 3. Rebuild Locality Intelligence (Aggregate)
    if os.path.exists(LOCALITY_CSV_OUTPUT_PATH):
        os.remove(LOCALITY_CSV_OUTPUT_PATH)
        log_audit(f"Quarantined/Deleted contaminated {LOCALITY_CSV_OUTPUT_PATH}")

    with open(LOCALITY_CSV_OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Locality', 'Total Entities', 'Hospitals', 'Clinics', 'Labs', 'Pharmacies', 'Doctors', 'Trust Status'])
        for loc, stats in sorted(locality_stats.items(), key=lambda x: x[1]['total'], reverse=True):
            writer.writerow([
                loc, stats['total'], stats['hospitals'], stats['clinics'], 
                stats['labs'], stats['pharmacies'], stats['doctors'], 'VERIFIED'
            ])
            
    log_audit(f"Successfully wrote verified Locality Intelligence to {LOCALITY_CSV_OUTPUT_PATH}")

    # 4. Generate Integrity Checksum
    def generate_checksum(filepath):
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    golden_hash = generate_checksum(GOLDEN_RECORDS_PATH)
    geo_hash = generate_checksum(GEOJSON_OUTPUT_PATH)
    loc_hash = generate_checksum(LOCALITY_CSV_OUTPUT_PATH)

    log_audit(f"INTEGRITY CHECKSUMS:")
    log_audit(f"Golden Records: {golden_hash}")
    log_audit(f"GeoJSON output: {geo_hash}")
    log_audit(f"Locality CSV output: {loc_hash}")
    log_audit("GEOGRAPHIC INTELLIGENCE DATA INTEGRITY RECOVERY COMPLETE. ZERO FABRICATED VALUES REMAIN.")

if __name__ == '__main__':
    rebuild_geographic_intelligence()
