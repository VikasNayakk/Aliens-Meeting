"""
Aliens Meeting Attendance Generator — 6/24/2026
Trigger-driven execution from start.txt
"""
import os
import re

BASE = r"c:\Vikasnayak\Aliens-Meeting"
DATE = "6-24-2026"
DATE_DISPLAY = "6/24/2026"

# ============================================================
# 1. LOAD MASTER DATA
# ============================================================
def load_master(filepath):
    """Load names from master file, clean and return list"""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    names = []
    for line in raw.strip().split('\n'):
        name = line.strip()
        # Skip headers and empty/trash lines
        if not name or name.lower().startswith('all ') or name.startswith('--') or name == ',':
            continue
        names.append(name)
    return names

members_master = load_master(os.path.join(BASE, "Data", "Master", "members.txt"))
students_master = load_master(os.path.join(BASE, "Data", "Master", "students.txt"))
master_all = members_master + students_master

print(f"Master Members: {len(members_master)}")
print(f"Master Students: {len(students_master)}")
print(f"Master Total: {len(master_all)}")

# ============================================================
# 2. PARSE TRIGGER DATA — ALL-JOIN (PRESENT) & TIME-PAR-JOIN
# ============================================================
all_join_raw = """Vikas Nayak
A'dil Sunlay (Host)
Anita Nayak
Rajani Rani
Anita Nayak
Gurpreet
Mandeep Kour
Navraj Singh
Harish Jaypal
Arnav Bishnoi
Abhinav Bishnoi
Rajesh Nayak
RAJESH KUMAR
Sunil Kori
Pooja Nayak
Laxmi
Gagan Chouhan
Darsh Bishnoi
Dinesh Kumar
Jaspal Byavat
Khushbu Rani
Neharika
Sahiram Nayak
Sandeep Barupal
Harpreet Singh
Raju Singh
Sumit
Yogesh Khand
Anjali
SHIVAM-BISHNOI
Nemchand Nayak
Parveen Kumar
somveer bishnoi"""

time_par_raw = """Vikas Nayak
A'dil Sunlay (Host)
Anita Nayak
Rajani Rani
Anita Nayak
Gurpreet
Mandeep Kour
Navraj Singh
Harish Jaypal
Arnav Bishnoi
Abhinav Bishnoi
Rajesh Nayak
RAJESH KUMAR
Sunil Kori
Pooja Nayak
Laxmi
Gagan Chouhan
Darsh Bishnoi
Dinesh Kumar
Jaspal Byavat
Khushbu Rani
Neharika
Sahiram Nayak
Sandeep Barupal
Harpreet Singh
Raju Singh
Sumit
Yogesh Khand
Anjali
SHIVAM-BISHNOI
Nemchand Nayak
Parveen Kumar
somveer bishnoi"""

def clean_name(name):
    """Normalize a name: strip, remove suffixes like (Host), (Me)"""
    name = name.strip()
    for suffix in [' (Host)', ' (Me)', ' (host)', ' (me)']:
        name = name.replace(suffix, '')
    return name.strip()

def parse_names(raw_text):
    """Parse name list, deduplicate, normalize"""
    seen = set()
    result = []
    for line in raw_text.strip().split('\n'):
        name = clean_name(line)
        if not name:
            continue
        key = name.lower().strip()
        if key not in seen:
            seen.add(key)
            result.append(name)
    return result

present_list = parse_names(all_join_raw)
ontime_list = parse_names(time_par_raw)

print(f"\nPresent (All-Join) unique: {len(present_list)}")
print(f"On-Time (Time-Par) unique: {len(ontime_list)}")

# ============================================================
# 3. NORMALIZE MASTER NAMES FOR MATCHING
# ============================================================
def normalize_key(name):
    """Create a normalized key for fuzzy matching"""
    n = name.lower().strip()
    n = re.sub(r'\s+', ' ', n)
    n = n.replace('-', ' ').replace('_', ' ').replace("'", '')
    return n

# Known spelling variations / aliases — map to canonical master names
ALIAS_MAP = {
    "adil sunlay": "adii sunlay",
    "mandeep kour": "mandeep kaur",
    "namchand nayak": "namchand",
    "nemchand nayak": "namchand",
    "gurpreet": "gurpreet singh",
    "darsh bishnoi": "darsh",
    "shivam bishnoi": "shivam",
    "somveer bishnoi": "somveer",
}

def resolve_alias(name):
    """Map known name variations to canonical master name key"""
    key = normalize_key(name)
    return ALIAS_MAP.get(key, key)

def match_name(target, candidates):
    """
    Try to match target against a list of candidate names.
    Returns the matched candidate or None.
    """
    tkey = resolve_alias(target)
    
    # Exact match after alias resolution
    for c in candidates:
        if resolve_alias(c) == tkey:
            return c
    
    # Fuzzy: candidate is substring of target or vice versa
    for c in candidates:
        ckey = resolve_alias(c)
        if ckey in tkey or tkey in ckey:
            return c
    
    # Split name matching: check significant word overlap
    tparts = {p for p in tkey.split() if len(p) > 1}
    best_match = None
    best_score = 0
    for c in candidates:
        ckey = resolve_alias(c)
        cparts = {p for p in ckey.split() if len(p) > 1}
        common = tparts & cparts
        if len(common) > best_score:
            best_score = len(common)
            best_match = c
    
    if best_score >= 2:
        return best_match
    if best_score >= 1 and len(tparts) == 1 and best_match:
        return best_match
    
    return None

# Sort master lists by name length descending — longer names match first
members_master.sort(key=lambda x: -len(x))
students_master.sort(key=lambda x: -len(x))

# ============================================================
# 4. FIND ABSENT (Master - Present)
# ============================================================
absent_members = []
absent_students = []
matched_present_keys = set()  # Track which present names were matched

def find_matched_master(master_name, present_list, already_matched_present):
    """Return the present name that matches master_name, or None"""
    matched = match_name(master_name, present_list)
    if matched and matched.lower().strip() not in already_matched_present:
        return matched
    return None

for m in members_master:
    matched = find_matched_master(m, present_list, matched_present_keys)
    if matched:
        matched_present_keys.add(matched.lower().strip())
    else:
        absent_members.append(m)

for s in students_master:
    matched = find_matched_master(s, present_list, matched_present_keys)
    if matched:
        matched_present_keys.add(matched.lower().strip())
    else:
        absent_students.append(s)

# Find present names that didn't match any master (guests/extras)
unmatched_present = [p for p in present_list if p.lower().strip() not in matched_present_keys]

print(f"\nAbsent Members: {len(absent_members)}")
for m in absent_members:
    print(f"  - {m}")
print(f"\nAbsent Students: {len(absent_students)}")
for s in absent_students:
    print(f"  - {s}")
if unmatched_present:
    print(f"\n⚠ Unmatched Present (not in master): {len(unmatched_present)}")
    for u in unmatched_present:
        print(f"  - {u}")

# ============================================================
# 5. FIND LATE (Present - OnTime)
# ============================================================
late_list = []
for p in present_list:
    pk = normalize_key(p)
    found = False
    for o in ontime_list:
        if normalize_key(o) == pk:
            found = True
            break
    if not found:
        # Also try fuzzy
        matched = match_name(p, ontime_list)
        if matched:
            found = True
    if not found:
        late_list.append(p)

print(f"\nLate: {len(late_list)}")
for l in late_list:
    print(f"  - {l}")

# ============================================================
# 6. GENERATE OUTPUT FILES
# ============================================================

# --- Present File ---
present_path = os.path.join(BASE, "Derived", "Present", f"Present-{DATE}.txt")
with open(present_path, 'w', encoding='utf-8') as f:
    for p in present_list:
        f.write(p + '\n')
print(f"\n✅ Present file: {present_path}")

# --- Late File ---
late_path = os.path.join(BASE, "Derived", "Late", f"5mlate-{DATE}.txt")
with open(late_path, 'w', encoding='utf-8') as f:
    if late_list:
        for l in late_list:
            f.write(l + '\n')
    else:
        f.write("# All members joined on time - No late entries\n")
print(f"✅ Late file: {late_path}")

# --- Absent File ---
absent_path = os.path.join(BASE, "Derived", "Absent", f"Absent-{DATE}.txt")
with open(absent_path, 'w', encoding='utf-8') as f:
    f.write("=== ABSENT MEMBERS ===\n")
    for m in absent_members:
        f.write(m + '\n')
    f.write("\n=== ABSENT STUDENTS ===\n")
    for s in absent_students:
        f.write(s + '\n')
    if unmatched_present:
        f.write("\n=== UNMATCHED PRESENT (NOT IN MASTER) ===\n")
        for u in unmatched_present:
            f.write(u + '\n')
print(f"✅ Absent file: {absent_path}")

# --- CSV Table (Main.txt Rule Format) ---
# Format: No,Present,Late,Absent
# Teen columns side-by-side: Present | Late | Absent
# Present = on-time pehle, late baad me
# Late = sirf late walo ke rows me (on-time me blank)
# Absent = Members pehle, Students baad me

csv_path = os.path.join(BASE, "Derived", "Tables", f"Table-{DATE}.csv")

# Separate present into on-time and late
present_ontime = [p for p in present_list if p.lower().strip() not in {l.lower().strip() for l in late_list}]
present_late_only = [p for p in present_list if p.lower().strip() in {l.lower().strip() for l in late_list}]

# Present column order: on-time first, then late
present_col = present_ontime + present_late_only

# Late column: blank for on-time rows, filled for late rows
late_col = ([''] * len(present_ontime)) + present_late_only

# Absent column: Members first, then Students
absent_col = absent_members + absent_students

# Total rows = max of all columns
total_rows = max(len(present_col), len(late_col), len(absent_col))

# Pad shorter columns with empty strings
present_col += [''] * (total_rows - len(present_col))
late_col += [''] * (total_rows - len(late_col))
absent_col += [''] * (total_rows - len(absent_col))

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    f.write("No,Present,Late,Absent\n")
    for i in range(total_rows):
        f.write(f"{i+1},{present_col[i]},{late_col[i]},{absent_col[i]}\n")

print(f"✅ CSV Table: {csv_path}")

# ============================================================
# 7. VALIDATION
# ============================================================
print("\n" + "="*50)
print("VALIDATION")
print("="*50)
print(f"Master Total:  {len(master_all)}")
print(f"Present:       {len(present_list)}")
print(f"Absent:        {len(absent_members) + len(absent_students)}")
print(f"Present+Absent: {len(present_list) + len(absent_members) + len(absent_students)}")
print(f"Late:          {len(late_list)}")
print(f"On-Time:       {len(present_list) - len(late_list)}")
print(f"\n✅ ALL FILES GENERATED for {DATE_DISPLAY}!")
