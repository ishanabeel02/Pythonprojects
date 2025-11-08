class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.grades = {}

    def view_profile(self):
        print(f"\n👩‍🎓 Student ID: {self.sid}")
        print(f"Name: {self.name}")
        print("Grades:", self.grades if self.grades else "No grades assigned yet.")

    def view_grades(self):
        if not self.grades:
            print("\n📌 No grades available.")
        else:
            print("\n📖 Grades:")
            for subject, grade in self.grades.items():
                print(f"{subject}: {grade}")


class Teacher:
    def __init__(self, tid, name):
        self.tid = tid
        self.name = name
        self.students = []

    def view_students(self):
        if not self.students:
            print("\n📌 No students assigned.")
        else:
            print(f"\n👨‍🏫 Students of {self.name}:")
            for s in self.students:
                print(f"{s.sid} - {s.name}")

    def assign_grade(self):
        if not self.students:
            print("\n⚠ No students to assign grades.")
            return

        sid = input("Enter Student ID to grade: ")
        for s in self.students:
            if s.sid == sid:
                subject = input("Enter Subject: ")
                grade = input("Enter Grade: ")
                s.grades[subject] = grade
                print(f"✅ Grade assigned to {s.name}.")
                return
        print("⚠ Student not found!")


class Admin:
    def __init__(self):
        self.students = []
        self.teachers = []

    def add_student(self):
        sid = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        student = Student(sid, name)
        self.students.append(student)
        print("✅ Student added successfully!")

    def remove_student(self):
        sid = input("Enter Student ID to remove: ")
        for s in self.students:
            if s.sid == sid:
                self.students.remove(s)
                print("🗑 Student removed successfully!")
                return
        print("⚠ Student not found!")

    def add_teacher(self):
        tid = input("Enter Teacher ID: ")
        name = input("Enter Teacher Name: ")
        teacher = Teacher(tid, name)
        self.teachers.append(teacher)
        print("✅ Teacher added successfully!")

    def remove_teacher(self):
        tid = input("Enter Teacher ID to remove: ")
        for t in self.teachers:
            if t.tid == tid:
                self.teachers.remove(t)
                print("🗑 Teacher removed successfully!")
                return
        print("⚠ Teacher not found!")

    def view_all(self):
        print("\n👩‍🎓 Students:")
        for s in self.students:
            print(f"{s.sid} - {s.name}")

        print("\n👨‍🏫 Teachers:")
        for t in self.teachers:
            print(f"{t.tid} - {t.name}")

    def assign_student_to_teacher(self):
        tid = input("Enter Teacher ID: ")
        sid = input("Enter Student ID: ")

        teacher = next((t for t in self.teachers if t.tid == tid), None)
        student = next((s for s in self.students if s.sid == sid), None)

        if teacher and student:
            teacher.students.append(student)
            print(f"✅ {student.name} assigned to {teacher.name}.")
        else:
            print("⚠ Teacher or Student not found!")


# ---------------- MAIN MENU ----------------
def main():
    admin = Admin()

    while True:
        print("\n===== LMS System =====")
        print("1. Admin")
        print("2. Teacher")
        print("3. Student")
        print("4. Exit")

        choice = input("Select Role: ")

        if choice == "1":  # Admin
            while True:
                print("\n--- Admin Menu ---")
                print("1. Add Student")
                print("2. Remove Student")
                print("3. Add Teacher")
                print("4. Remove Teacher")
                print("5. View All")
                print("6. Assign Student to Teacher")
                print("7. Back")
                ch = input("Enter choice: ")

                if ch == "1": admin.add_student()
                elif ch == "2": admin.remove_student()
                elif ch == "3": admin.add_teacher()
                elif ch == "4": admin.remove_teacher()
                elif ch == "5": admin.view_all()
                elif ch == "6": admin.assign_student_to_teacher()
                elif ch == "7": break
                else: print("⚠ Invalid choice.")

        elif choice == "2":  # Teacher
            tid = input("Enter Teacher ID: ")
            teacher = next((t for t in admin.teachers if t.tid == tid), None)
            if not teacher:
                print("⚠ Teacher not found!")
                continue

            while True:
                print(f"\n--- Teacher Menu ({teacher.name}) ---")
                print("1. View Students")
                print("2. Assign Grade")
                print("3. Back")
                ch = input("Enter choice: ")

                if ch == "1": teacher.view_students()
                elif ch == "2": teacher.assign_grade()
                elif ch == "3": break
                else: print("⚠ Invalid choice.")

        elif choice == "3":  # Student
            sid = input("Enter Student ID: ")
            student = next((s for s in admin.students if s.sid == sid), None)
            if not student:
                print("⚠ Student not found!")
                continue

            while True:
                print(f"\n--- Student Menu ({student.name}) ---")
                print("1. View Profile")
                print("2. View Grades")
                print("3. Back")
                ch = input("Enter choice: ")

                if ch == "1": student.view_profile()
                elif ch == "2": student.view_grades()
                elif ch == "3": break
                else: print("⚠ Invalid choice.")

        elif choice == "4":
            print("👋 Exiting LMS. Goodbye!")
            break

        else:
            print("⚠ Invalid option!")

# Run Program
if __name__ == "__main__":
    main()
