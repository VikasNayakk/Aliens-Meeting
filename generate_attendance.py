"""Generate Present, Late, Absent, CSV for Aliens Meeting"""
import os

BASE = r"c:\Vikasnayak\Aliens-Meeting"
DATE = "6-9-2026"

# Master data
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

present_raw = """A'dii Sunlay (Host)
Mukesh (Me)
Arnav Bishnoi
Abhinav Bishnoi
Harish Jaypal
Krishan Lal
Sumit Kumar
Rohit
Ajay Nayak
Dinesh Nayak
Tarachand Lohara
Sunil Kori
Harpreet Singh
Prem Kumar
Sapna
Raju Singh
Mandeep Kour
Sahil Sudiya
Poonam Kumari
Rajani Rani
Gagan Chouhan
Sandeep
Rahul Lakhesar
Dinesh Kumar
RAJESH NAYAK
Jaspal Byavat
Sahiram Nayak
Harman
Anjali
Navraj Singh
Laxmi
Pooja Sudiya
Vikas Nayak
Gursaj
SHIVAM-BISHNOI
Rajesh Nayak
Anita Nayak
Neharika
Himanshu Nayak
Khushbu Rani"""

# Clean present names
present_clean = []
for name in present_raw.strip().split('\n'):
    name = name.strip()
    for suffix in [' (Host)', ' (Me)', ' \u2b50']:
        name = name.replace(suffix, '')
    present_clean.append(name.lower().strip())

members = [m.strip().lower() for m in members_raw.strip().split('\n') if m.strip() and m.strip() != ',']
students = [s.strip().lower() for s in students_raw.strip().split('\n') if s.strip() and s.strip() != ',']

# Find absent
absent_members = []
absent_students = []

for m in members:
    found = False
    for p in present_clean:
        if m in p or p in m:
            found = True
            break
    if not found:
        absent_members.append(m)

for s in students:
    found = False
    for p in present_clean:
        if s in p or p in s:
            found = True
            break
    if not found:
        absent_students.append(s)

print("=== ABSENT MEMBERS ===")
for m in absent_members:
    print(m.title())
print(f"\nTotal absent members: {len(absent_members)}")

print("\n=== ABSENT STUDENTS ===")
for s in absent_students:
    print(s.title())
print(f"\nTotal absent students: {len(absent_students)}")
print(f"\nTotal absent: {len(absent_members) + len(absent_students)}")
print(f"Total present: {len(present_clean)}")

# Write absent file
absent_path = os.path.join(BASE, "Derived", "Absent", "Absent-6-4-2026.txt")
with open(absent_path, 'w', encoding='utf-8') as f:
    f.write("=== ABSENT MEMBERS ===\n")
    for m in absent_members:
        f.write(m.title() + '\n')
    f.write("\n=== ABSENT STUDENTS ===\n")
    for s in absent_students:
        f.write(s.title() + '\n')
print(f"\nAbsent file written: {absent_path}")

# Write late file (empty - all on time)
late_path = os.path.join(BASE, "Derived", "Late", "5mlate-6-4-2026.txt")
with open(late_path, 'w', encoding='utf-8') as f:
    f.write("# All members joined on time - No late entries\n")
print(f"Late file written: {late_path}")

# Write CSV table
csv_path = os.path.join(BASE, "Derived", "Tables", "Table-6-4-2026.csv")
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("Name,Status,Type\n")
    for p in present_clean:
        ptype = "Member" if p in members else "Student"
        f.write(f"{p.title()},Present,{ptype}\n")
    for m in absent_members:
        f.write(f"{m.title()},Absent,Member\n")
    for s in absent_students:
        f.write(f"{s.title()},Absent,Student\n")
print(f"CSV table written: {csv_path}")

print("\n✅ ALL FILES GENERATED for 6/4/2026!")
