import csv
import re
import os

INPUT_CSV = 'data/Jabalpur_Healthcare_Golden_Records.csv'
OUTPUT_CSV = 'data/Jabalpur_Healthcare_Golden_Records_V3.csv'
AUDIT_LOG = 'data/semantic_classifier_audit.log'

def log(msg):
    print(msg)
    with open(AUDIT_LOG, 'a') as f:
        f.write(msg + '\n')

def infer_taxonomy(name, specialty, current_type):
    text = (name + " " + specialty).lower()
    
    # Hospitals & Major Centers
    if any(k in text for k in ['multi specialty', 'multispeciality', 'multi-specialty']):
        return 'MULTISPECIALTY_HOSPITAL'
    if any(k in text for k in ['super specialty', 'superspeciality', 'super-specialty']):
        return 'SUPERSPECIALTY_HOSPITAL'
    if 'maternity' in text:
        return 'MATERNITY_HOSPITAL'
    if 'nursing home' in text:
        return 'NURSING_HOME'
    if 'hospital' in text:
        return 'HOSPITAL'
        
    # Diagnostics & Labs
    if any(k in text for k in ['pathology', 'blood test', 'lab']):
        return 'PATHOLOGY_LAB'
    if any(k in text for k in ['x-ray', 'xray', 'mri', 'ct scan', 'sonography', 'imaging', 'ultrasound']):
        return 'IMAGING_CENTER'
    if 'diagnostic' in text:
        return 'DIAGNOSTIC_CENTER'

    # Pharmacies
    if any(k in text for k in ['pharmacy', 'medical store', 'medicos']):
        return 'PHARMACY'

    # Alternative Medicine
    if any(k in text for k in ['ayurved', 'ayush']):
        return 'AYURVEDA_CLINIC'
    if any(k in text for k in ['homeopath', 'homoeo']):
        return 'HOMEOPATHY_CLINIC'
    if 'unani' in text:
        return 'UNANI_CLINIC'
    if any(k in text for k in ['physiotherapy', 'physio', 'acupressure', 'acupuncture']):
        return 'PHYSIOTHERAPY_CENTER'

    # Specialized Clinics
    if any(k in text for k in ['dental', 'dentist', 'tooth', 'teeth', 'smile', 'orthodont', 'bds', 'mds']):
        return 'DENTAL_CLINIC'
    if any(k in text for k in ['eye', 'vision', 'optical', 'ophthal', 'retina', 'lasik', 'glaucoma']):
        return 'EYE_CLINIC'
    if any(k in text for k in ['ortho', 'bone', 'joint', 'spine', 'fracture']):
        return 'ORTHOPEDIC_CLINIC'
    if any(k in text for k in ['pediatric', 'child', 'baby', 'kids', 'paediatric']):
        return 'PEDIATRIC_CLINIC'
    if any(k in text for k in ['gyne', 'gynae', 'women', 'pregnancy', 'ivf', 'female']):
        return 'GYNECOLOGY_CLINIC'
    if any(k in text for k in ['heart', 'cardiac', 'cardio']):
        return 'CARDIOLOGY_CLINIC'
    if any(k in text for k in ['neuro', 'brain', 'paralysis', 'epilepsy', 'migraine']):
        return 'NEUROLOGY_CLINIC'
    if any(k in text for k in ['gastro', 'stomach', 'liver', 'digest']):
        return 'GASTROENTEROLOGY_CLINIC'
    if any(k in text for k in ['skin', 'derma', 'hair', 'laser', 'cosmetic', 'beauty']):
        return 'DERMATOLOGY_CLINIC'
    if any(k in text for k in ['ent ', ' ear ', ' nose ', ' throat ']):
        return 'ENT_CLINIC'
    if any(k in text for k in ['cancer', 'onco']):
        return 'ONCOLOGY_CLINIC'
    if any(k in text for k in ['psychiat', 'psycholog', 'mental', 'stress']):
        return 'PSYCHIATRY_CLINIC'
    if any(k in text for k in ['kidney', 'nephro', 'urolog']):
        return 'NEPHROLOGY_CLINIC'
    if 'surgical' in text or 'surgeon' in text:
        return 'SURGICAL_CENTER'
    if 'polyclinic' in text:
        return 'POLYCLINIC'
        
    # If it was already a specific clinic type but got mangled, try to preserve it
    current = current_type.strip().upper()
    valid_types = [
        'DENTAL_CLINIC', 'ENT_CLINIC', 'HOSPITAL', 'PATHOLOGY_LAB', 'PHYSIOTHERAPY_CENTER', 'PHARMACY',
        'DIAGNOSTIC_CENTER', 'AYURVEDIC_CLINIC', 'HOMEOPATHIC_CLINIC', 'SKIN_CLINIC', 'EYE_CLINIC',
        'PEDIATRIC_CLINIC', 'ORTHOPEDIC_CLINIC', 'MULTI_SPECIALITY_HOSPITAL', 'NURSING_HOME', 'NEUROLOGY_CLINIC',
        'PSYCHIATRY_CLINIC', 'GYNECOLOGY_CLINIC', 'CARDIOLOGY_CLINIC', 'ONCOLOGY_CLINIC', 'SUPER_SPECIALITY_HOSPITAL',
        'NEPHROLOGY_CLINIC', 'GASTROENTEROLOGY_CLINIC', 'UROLOGY_CLINIC'
    ]
    if current in valid_types:
        # Standardize old names to our new taxonomy
        if current == 'AYURVEDIC_CLINIC': return 'AYURVEDA_CLINIC'
        if current == 'HOMEOPATHIC_CLINIC': return 'HOMEOPATHY_CLINIC'
        if current == 'SKIN_CLINIC': return 'DERMATOLOGY_CLINIC'
        if current == 'MULTI_SPECIALITY_HOSPITAL': return 'MULTISPECIALTY_HOSPITAL'
        if current == 'SUPER_SPECIALITY_HOSPITAL': return 'SUPERSPECIALTY_HOSPITAL'
        return current

    # Default fallback
    return 'GENERAL_CLINIC'

def process():
    if os.path.exists(AUDIT_LOG):
        os.remove(AUDIT_LOG)
        
    log("Starting Semantic Inference classification...")
    
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        rows = []
        changed = 0
        
        for row in reader:
            if not row or not row[0].strip():
                continue
            
            # The current row might be mangled. 
            # We strictly extract Name(1), Type(2), Specialty(3).
            name = row[1]
            old_type = row[2]
            specialty = row[3] if len(row) > 3 else ""
            
            new_type = infer_taxonomy(name, specialty, old_type)
            
            if new_type != old_type.strip().upper():
                changed += 1
                
            row[2] = new_type
            rows.append(row)
            
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        
    log(f"Processed {len(rows)} total records.")
    log(f"Re-classified {changed} generic or mangled records into strict Taxonomy.")
    log(f"Saved Golden Records V3 to {OUTPUT_CSV}")

if __name__ == '__main__':
    process()
