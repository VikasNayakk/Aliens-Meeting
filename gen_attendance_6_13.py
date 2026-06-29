"""Generate Present, Late, Absent, CSV for 6/13/2026"""
import os

BASE = r"c:\Vikasnayak\Aliens-Meeting"
DATE = "6-13-2026"

# ─── MASTER DATA (from Data/Master/) ──────────────────────
members_raw = """Navraj Singh
Rajveer Nayak
A'dii Sunlay
Aira
Ajay Nayak
Vikas Nayak
Anita Nayak
Arnav Bishnoi
Sumit
Abhinav Bishnoi
Pawan Meghwal
Gagan Chouhan
Gagan Kumar
Gurpreet Singh
Harpreet Singh
Himanshu Nayak
Jaspal Byavat
Khushbu Rani
Mandeep Kaur
Nitesh Aggrwal
Paras Aggrwal
Parveen Kumar
Pawan Kumar
Pooja Nayak
Poonam Kumari
Prem Kumar
Rajani Rani
Rajesh Nayak
Raju Singh
Sahiram Nayak
Sandeep Barupal
Shyo Chand
Sunil Kori
Tarachand
Yogesh Khand
Dinesh
Dinesh Kumar
Sapna"""

students_raw = """Bharat Ram
Ravina
Mamta-2
Trikshna
Siya
Vishnu
Somveer
Ravishankar
Darsh
Sidhant
Shivam
Anmol
Gopal
Namchand
Somdev
Gursaj Singh
Satish Kumar
Bhavishya Jayani
Gagan Kumar
Rohit Kumar
Vishal
Gotam
Gurjeet
Kulwant
Krishan Lal
Sachin
Kirat
Urmila
Harshita
Manisha
Kalpna
Varshita kanwar
Pooja-2
Dimpal
Mukesh
Bhanupartap
Harman
Suyogita
Komal Kanwar
Lokender
Neha
Sumit
Bhavna
Kajal"""

# ─── TRIGGER BLOCK 2 DATA (from start.txt) ────────────────
all_join_raw = """Vikas Nayak (Me)
A'dii Sunlay (Host)
Anita Nayak
sahil sudiya
anjali
Pawan Meghwal
Neharika
Pooja Sudiya
Rahul Lakhesar
sapna
Dinesh kumar
Mandeep Kour
Laxmi
Poonam Kumari
Tarachand Lohara
Rajani Rani
Jaspal Byavat
Prem kumar
Ajay Nayak
Paras Bishnoi
Harish Jaypal
Navraj Singh
Pooja Nayak
shivam bishnoi
Krishan lal
Parveen Kumar
devkarn kumar
OPPO CPH2721
Sandeep Barupal
Nitesh Aggrwal
Aira
Khushbu Rani"""

time_par_raw = """Vikas Nayak (Me)
A'dii Sunlay (Host)
Anita Nayak
sahil sudiya
anjali
Pawan Meghwal
Neharika
Pooja Sudiya
Anita Nayak
Rahul Lakhesar
sapna
Dinesh kumar
Mandeep Kour
Laxmi
Poonam Kumari
Tarachand Lohara"""

# ─── CLEAN NAMES ──────────────────────────────────────────
def clean_name(name):
    name = name.strip()
    for suffix in [' (You)', ' (Host)', ' (Me)', ' (second login/device)', ' - Graphic Dr.', ' ⭐']:
        name = name.replace(suffix, '')
    return name.strip()

def normalize(name):
    return name.lower().replace(' ', '').replace('-', '').replace('.', '').replace('_', '')

all_join = [clean_name(n) for n in all_join_raw.strip().split('\n') if n.strip()]
time_par = [clean_name(n) for n in time_par_raw.strip().split('\n') if n.strip()]
members = [m.strip() for m in members_raw.strip().split('\n') if m.strip() and m.strip() != ',']
students = [s.strip() for s in students_raw.strip().split('\n') if s.strip() and s.strip() != ',']

# Deduplicate all_join
seen = set()
all_join_dedup = []
for n in all_join:
    if normalize(n) not in seen:
        seen.add(normalize(n))
        all_join_dedup.append(n)
all_join = all_join_dedup

# Deduplicate time_par
seen_tp = set()
time_par_dedup = []
for n in time_par:
    if normalize(n) not in seen_tp:
        seen_tp.add(normalize(n))
        time_par_dedup.append(n)
time_par = time_par_dedup

# ─── FIND LATE ────────────────────────────────────────────
time_par_norm = {normalize(n) for n in time_par}
late = [n for n in all_join if normalize(n) not in time_par_norm]

# ─── FIND ABSENT ──────────────────────────────────────────
all_join_norm = {normalize(n) for n in all_join}

absent_members = []
for m in members:
    found = False
    for aj in all_join:
        if normalize(m) in normalize(aj) or normalize(aj) in normalize(m):
            found = True
            break
    if not found:
        absent_members.append(m)

absent_students = []
for s in students:
    found = False
    for aj in all_join:
        if normalize(s) in normalize(aj) or normalize(aj) in normalize(s):
            found = True
            break
    if not found:
        absent_students.append(s)

# ─── PRINT SUMMARY ────────────────────────────────────────
print("=" * 60)
print(f"  ALIENS MEETING ATTENDANCE — {DATE}")
print("=" * 60)
print(f"\n📊 All-Join (Present): {len(all_join)}")
print(f"⏰ Time Par Join: {len(time_par)}")
print(f"⏰ Late: {len(late)}")
print(f"❌ Absent Members: {len(absent_members)}")
print(f"❌ Absent Students: {len(absent_students)}")
print(f"❌ Total Absent: {len(absent_members) + len(absent_students)}")
print(f"✅ Total Master: {len(members) + len(students)}")
print(f"✅ Validation: Present({len(all_join)}) + Absent({len(absent_members)+len(absent_students)}) = {len(all_join) + len(absent_members) + len(absent_students)} (Master={len(members)+len(students)})")

print("\n--- LATE ---")
for n in late:
    print(f"  ⏰ {n}")

print("\n--- ABSENT MEMBERS ---")
for m in absent_members:
    print(f"  ❌ {m}")

print("\n--- ABSENT STUDENTS ---")
for s in absent_students:
    print(f"  ❌ {s}")

# ─── WRITE OUTPUT FILES ───────────────────────────────────
derived = os.path.join(BASE, "Derived")

# Present
present_path = os.path.join(derived, "Present", f"Present-{DATE}.txt")
os.makedirs(os.path.dirname(present_path), exist_ok=True)
with open(present_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_join))
print(f"\n📁 Present → {present_path}")

# Late
late_path = os.path.join(derived, "Late", f"5mlate-{DATE}.txt")
os.makedirs(os.path.dirname(late_path), exist_ok=True)
with open(late_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(late))
print(f"📁 Late → {late_path}")

# Absent
absent_path = os.path.join(derived, "Absent", f"Absent-{DATE}.txt")
os.makedirs(os.path.dirname(absent_path), exist_ok=True)
with open(absent_path, 'w', encoding='utf-8') as f:
    f.write("=== ABSENT MEMBERS ===\n")
    f.write('\n'.join(absent_members))
    f.write("\n\n=== ABSENT STUDENTS ===\n")
    f.write('\n'.join(absent_students))
print(f"📁 Absent → {absent_path}")

# ─── BUILD TABLE (Rule §6: No,Present,Late,Absent) ────────
# Members first, then students (Rule: "Members ko upar rakhna hai")
# Separate present into members and students
present_members = []
present_students = []
members_norm = {normalize(m) for m in members}
for p in all_join:
    pn = normalize(p)
    found_in_members = False
    for m in members:
        if normalize(m) in pn or pn in normalize(m):
            found_in_members = True
            break
    if found_in_members:
        present_members.append(p)
    else:
        present_students.append(p)

# Build ordered present: members first, then students
present_ordered = present_members + present_students

# Absent: members first, then students
absent_all = absent_members + absent_students

# Late set for lookup
late_norm = {normalize(l) for l in late}

# Max rows
max_rows = max(len(present_ordered), len(absent_all))

# Generate CSV
def write_csv(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("No,Present,Late,Absent\n")
        for i in range(max_rows):
            no = i + 1
            pres = present_ordered[i] if i < len(present_ordered) else ""
            is_late = normalize(pres) in late_norm if pres else False
            late_val = pres if is_late else ""
            abs_val = absent_all[i] if i < len(absent_all) else ""
            f.write(f"{no},{pres},{late_val},{abs_val}\n")
    return filepath

# Write to Derived/Tables
table_path = os.path.join(derived, "Tables", f"Table-{DATE}.csv")
write_csv(table_path)
print(f"📁 Table CSV → {table_path}")

# Also save to Data/Meetings folder
meeting_dir = os.path.join(BASE, "Data", "Meetings", "2026-06-13")
os.makedirs(meeting_dir, exist_ok=True)

for name, data in [
    (f"Present-{DATE}.txt", '\n'.join(all_join)),
    (f"5mlate-{DATE}.txt", '\n'.join(late)),
    (f"Absent-{DATE}.txt", "=== ABSENT MEMBERS ===\n" + '\n'.join(absent_members) + "\n\n=== ABSENT STUDENTS ===\n" + '\n'.join(absent_students)),
]:
    filepath = os.path.join(meeting_dir, name)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"📁 {name} → {filepath}")

# CSV to meetings folder too
csv_meeting = os.path.join(meeting_dir, f"Table-{DATE}.csv")
write_csv(csv_meeting)
print(f"📁 Table CSV → {csv_meeting}")

print("\n✅ DONE! All attendance files generated for", DATE)
