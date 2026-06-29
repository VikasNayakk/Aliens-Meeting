"""Generate Present, Late, Absent, CSV for 6/9/2026"""
import os

BASE = r"c:\Vikasnayak\Aliens-Meeting"
DATE = "6-9-2026"

# ─── MASTER DATA ──────────────────────────────────────────
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

# ─── TRIGGER BLOCK 2 DATA ─────────────────────────────────
all_join_raw = """Vikas Nayak
A'dii Sunlay
Anita Nayak
Dinesh Nayak - Graphic Dr.
Pooja Sudiya
Khushbu Rani
Dinesh kumar
Sumit Kumar
Sahiram Nayak
Tarachand Lohara
Rohit
Sandeep
Gagan Chouhan
Rajani Rani
Pawan Meghwal
Harman
HarpreetSingh
sapna
Poonam Kumari
RAJESH NAYAK
Harish Jaypal
Navraj Singh
Jaspal Byavat
sahil sudiya
SHIVAM BISHNOI
Aira
Ajay karwasra
Kavita
Pooja Nayak
Sidhant Aggrwal
Krishan lal
Prem Kumar
Abhinav Bishnoi
Ajay Nayak"""

time_par_raw = """Vikas Nayak (You)
A'dii Sunlay (Host)
Anita Nayak
Dinesh Nayak
Pooja Nayak
Khushbu Rani
Sumit Kumar
Prem Kumar
Abhinav Bishnoi
Ajay Nayak
Sandeep
Gagan Chouhan
Rajani Rani
Harpreet Singh
Aira
Navraj Singh
SHIVAM BISHNOI
Jaspal Byavat"""

# ─── CLEAN NAMES ──────────────────────────────────────────
def clean_name(name):
    name = name.strip()
    for suffix in [' (You)', ' (Host)', ' (Me)', ' - Graphic Dr.', ' ⭐']:
        name = name.replace(suffix, '')
    return name.strip()

def normalize(name):
    return name.lower().replace(' ', '').replace('-', '').replace('.', '')

all_join = [clean_name(n) for n in all_join_raw.strip().split('\n') if n.strip()]
time_par = [clean_name(n) for n in time_par_raw.strip().split('\n') if n.strip()]
members = [m.strip() for m in members_raw.strip().split('\n') if m.strip() and m.strip() != ',']
students = [s.strip() for s in students_raw.strip().split('\n') if s.strip() and s.strip() != ',']

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
print("=" * 50)
print(f"  ALIENS MEETING ATTENDANCE — {DATE}")
print("=" * 50)
print(f"\n📊 All-Join (Present): {len(all_join)}")
print(f"⏰ Time Par Join: {len(time_par)}")
print(f"⏰ Late: {len(late)}")
print(f"❌ Absent Members: {len(absent_members)}")
print(f"❌ Absent Students: {len(absent_students)}")
print(f"❌ Total Absent: {len(absent_members) + len(absent_students)}")

print("\n--- LATE ---")
for i, n in enumerate(late, 1):
    print(f"  {i}. {n}")

print("\n--- ABSENT MEMBERS ---")
for i, n in enumerate(absent_members, 1):
    print(f"  {i}. {n}")

print("\n--- ABSENT STUDENTS ---")
for i, n in enumerate(absent_students, 1):
    print(f"  {i}. {n}")

# ─── WRITE FILES ──────────────────────────────────────────
# 1. Present (All-Join)
present_path = os.path.join(BASE, "Derived", "Present", f"Present-{DATE}.txt")
with open(present_path, 'w', encoding='utf-8') as f:
    for n in all_join:
        f.write(n + '\n')
print(f"\n✅ Present: {present_path}")

# 2. Late
late_path = os.path.join(BASE, "Derived", "Late", f"5mlate-{DATE}.txt")
with open(late_path, 'w', encoding='utf-8') as f:
    if late:
        for n in late:
            f.write(n + '\n')
    else:
        f.write("# All on time - No late entries\n")
print(f"✅ Late: {late_path}")

# 3. Absent
absent_path = os.path.join(BASE, "Derived", "Absent", f"Absent-{DATE}.txt")
with open(absent_path, 'w', encoding='utf-8') as f:
    f.write("=== ABSENT MEMBERS ===\n")
    for m in absent_members:
        f.write(m + '\n')
    f.write("\n=== ABSENT STUDENTS ===\n")
    for s in absent_students:
        f.write(s + '\n')
print(f"✅ Absent: {absent_path}")

# 4. CSV Table
csv_path = os.path.join(BASE, "Derived", "Tables", f"Table-{DATE}.csv")
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("Name,Status,Type\n")
    for n in time_par:
        ptype = "Member" if normalize(n) in {normalize(m) for m in members} else "Student"
        f.write(f"{n},On Time,{ptype}\n")
    for n in late:
        ptype = "Member" if normalize(n) in {normalize(m) for m in members} else "Student"
        f.write(f"{n},Late,{ptype}\n")
    for m in absent_members:
        f.write(f"{m},Absent,Member\n")
    for s in absent_students:
        f.write(f"{s},Absent,Student\n")
print(f"✅ CSV: {csv_path}")

print(f"\n🎯 ALL FILES GENERATED for {DATE}!")
