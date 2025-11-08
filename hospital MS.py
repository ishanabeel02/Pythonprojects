import json
from datetime import datetime

class HospitalSystem:
    def __init__(self):
        self.patients = self.load_data('patients.json')
        self.doctors = self.load_data('doctors.json')
        self.appointments = self.load_data('appointments.json')
        self.records = self.load_data('records.json')

    def load_data(self, filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def main_menu(self):
        while True:
            print("\n=== HOSPITAL MANAGEMENT ===")
            print("1. Patient Management")
            print("2. Doctor Management")
            print("3. Appointments")
            print("4. Medical Records")
            print("5. Exit")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                self.record_menu()
            elif choice == '5':
                self.save_all()
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice!")

    def save_all(self):
        self.save_data(self.patients, 'patients.json')
        self.save_data(self.doctors, 'doctors.json')
        self.save_data(self.appointments, 'appointments.json')
        self.save_data(self.records, 'records.json')

    def patient_menu(self):
        while True:
            print("\n=== PATIENT MANAGEMENT ===")
            print("1. Add Patient")
            print("2. View Patients")
            print("3. Search Patient")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.search_patient()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def add_patient(self):
        pid = input("Enter patient ID: ")
        if pid in self.patients:
            print("ID already exists!")
            return

        self.patients[pid] = {
            'name': input("Name: "),
            'age': input("Age: "),
            'gender': input("Gender (M/F/O): ").upper(),
            'phone': input("Phone: "),
            'reg_date': datetime.now().strftime("%Y-%m-%d")
        }
        print("Patient added!")

    def view_patients(self):
        if not self.patients:
            print("No patients!")
            return

        for pid, p in self.patients.items():
            print(f"\nID: {pid}")
            print(f"Name: {p['name']}")
            print(f"Age: {p['age']}")
            print(f"Gender: {p['gender']}")
            print(f"Phone: {p['phone']}")
            print(f"Registered: {p['reg_date']}")

    def search_patient(self):
        term = input("Enter ID or name: ").lower()
        found = False

        for pid, p in self.patients.items():
            if term in pid.lower() or term in p['name'].lower():
                print(f"\nID: {pid}, Name: {p['name']}, Phone: {p['phone']}")
                found = True

        if not found: print("No matches found!")

    def doctor_menu(self):
        while True:
            print("\n=== DOCTOR MANAGEMENT ===")
            print("1. Add Doctor")
            print("2. View Doctors")
            print("3. Search Doctor")
            print("4. Back")

            choice = input("Enter choice (1-4): ")

            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_doctors()
            elif choice == '3':
                self.search_doctor()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

    def add_doctor(self):
        did = input("Enter doctor ID: ")
        if did in self.doctors:
            print("ID already exists!")
            return

        self.doctors[did] = {
            'name': input("Name: "),
            'specialization': input("Specialization: "),
            'phone': input("Phone: "),
            'fee': input("Consultation Fee: ")
        }
        print("Doctor added!")

    def view_doctors(self):
        if not self.doctors:
            print("No doctors!")
            return

        for did, d in self.doctors.items():
            print(f"\nID: {did}")
            print(f"Name: Dr. {d['name']}")
            print(f"Specialization: {d['specialization']}")
            print(f"Phone: {d['phone']}")
            print(f"Fee: ${d['fee']}")

    def search_doctor(self):
        term = input("Enter ID or name: ").lower()
        found = False

        for did, d in self.doctors.items():
            if term in did.lower() or term in d['name'].lower():
                print(f"\nID: {did}, Name: Dr. {d['name']}, Spec: {d['specialization']}")
                found = True

        if not found: print("No matches found!")

    def appointment_menu(self):
        while True:
            print("\n=== APPOINTMENTS ===")
            print("1. Schedule")
            print("2. View All")
            print("3. View by Patient")
            print("4. View by Doctor")
            print("5. Cancel")
            print("6. Back")

            choice = input("Enter choice (1-6): ")

            if choice == '1':
                self.schedule_appointment()
            elif choice == '2':
                self.view_appointments()
            elif choice == '3':
                self.view_patient_appointments()
            elif choice == '4':
                self.view_doctor_appointments()
            elif choice == '5':
                self.cancel_appointment()
            elif choice == '6':
                break
            else:
                print("Invalid choice!")

    def schedule_appointment(self):
        if not self.patients or not self.doctors:
            print("Need patients and doctors first!")
            return

        aid = str(len(self.appointments) + 1).zfill(3)
        pid = input("Enter patient ID: ")
        if pid not in self.patients:
            print("Invalid patient ID!")
            return

        did = input("Enter doctor ID: ")
        if did not in self.doctors:
            print("Invalid doctor ID!")
            return

        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM): ")

        self.appointments[aid] = {
            'patient': pid,
            'doctor': did,
            'date': date,
            'time': time,
            'status': 'Scheduled'
        }
        print(f"Appointment {aid} scheduled!")

    def view_appointments(self):
        if not self.appointments:
            print("No appointments!")
            return

        for aid, a in self.appointments.items():
            p = self.patients[a['patient']]
            d = self.doctors[a['doctor']]
            print(f"\nID: {aid}")
            print(f"Patient: {p['name']}")
            print(f"Doctor: Dr. {d['name']}")
            print(f"Date: {a['date']} at {a['time']}")
            print(f"Status: {a['status']}")

    def view_patient_appointments(self):
        pid = input("Enter patient ID: ")
        if pid not in self.patients:
            print("Invalid ID!")
            return

        found = False
        for aid, a in self.appointments.items():
            if a['patient'] == pid:
                d = self.doctors[a['doctor']]
                print(f"\nAppt {aid} with Dr. {d['name']} on {a['date']} ({a['status']})")
                found = True

        if not found: print("No appointments found!")

    def view_doctor_appointments(self):
        did = input("Enter doctor ID: ")
        if did not in self.doctors:
            print("Invalid ID!")
            return

        found = False
        for aid, a in self.appointments.items():
            if a['doctor'] == did:
                p = self.patients[a['patient']]
                print(f"\nAppt {aid} with {p['name']} on {a['date']} ({a['status']})")
                found = True

        if not found: print("No appointments found!")

    def cancel_appointment(self):
        aid = input("Enter appointment ID: ")
        if aid not in self.appointments:
            print("Invalid ID!")
            return

        self.appointments[aid]['status'] = 'Cancelled'
        print("Appointment cancelled!")

    def record_menu(self):
        while True:
            print("\n=== MEDICAL RECORDS ===")
            print("1. Add Record")
            print("2. View Records")
            print("3. Back")

            choice = input("Enter choice (1-3): ")

            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.view_records()
            elif choice == '3':
                break
            else:
                print("Invalid choice!")

    def add_record(self):
        if not self.patients or not self.doctors:
            print("Need patients and doctors first!")
            return

        rid = str(len(self.records) + 1).zfill(3)
        pid = input("Patient ID: ")
        if pid not in self.patients:
            print("Invalid ID!")
            return

        did = input("Doctor ID: ")
        if did not in self.doctors:
            print("Invalid ID!")
            return

        self.records[rid] = {
            'patient': pid,
            'doctor': did,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'diagnosis': input("Diagnosis: "),
            'treatment': input("Treatment: "),
            'notes': input("Notes: ")
        }
        print("Record added!")

    def view_records(self):
        pid = input("Enter patient ID: ")
        if pid not in self.patients:
            print("Invalid ID!")
            return

        found = False
        for rid, r in self.records.items():
            if r['patient'] == pid:
                d = self.doctors[r['doctor']]
                print(f"\nRecord {rid} by Dr. {d['name']} on {r['date']}")
                print(f"Diagnosis: {r['diagnosis']}")
                print(f"Treatment: {r['treatment']}")
                print(f"Notes: {r['notes']}")
                found = True

        if not found: print("No records found!")


# Run the system
if __name__ == "__main__":
    hospital = HospitalSystem()
    hospital.main_menu()