class Semester:
    def __init__(self, semester_no):
        self.semester_no = semester_no
        self.courses = []  # Each course: (course_name, grade, credits)

    def add_course(self):
        print(f"\n--- Add Course for Semester {self.semester_no} ---")
        course_name = input("Enter course name: ")
        grade = input("Enter grade (A/B/C/D/F or 4.0-0.0): ").upper()
        credits = input("Enter credits: ")
        try:
            credits = float(credits)
        except ValueError:
            print("Invalid credits value.")
            return
        grade_point = self.grade_to_points(grade)
        if grade_point is None:
            print("Invalid grade.")
            return
        self.courses.append((course_name, grade_point, credits))
        print(f"Course '{course_name}' added.")

    def grade_to_points(self, grade):
        # Accepts letter grades or numeric GPA
        letter_grades = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        if grade in letter_grades:
            return letter_grades[grade]
        try:
            point = float(grade)
            if 0.0 <= point <= 4.0:
                return point
        except ValueError:
            return None
        return None

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for _, grade_point, credits in self.courses:
            total_points += grade_point * credits
            total_credits += credits
        if total_credits == 0:
            return None
        return total_points / total_credits

    def list_courses(self):
        print(f"\nCourses for Semester {self.semester_no}:")
        for idx, (course_name, grade_point, credits) in enumerate(self.courses):
            print(f"{idx+1}. {course_name} - Grade Points: {grade_point}, Credits: {credits}")

class StudentRecord:
    def __init__(self):
        self.semesters = []  # List of Semester objects

    def add_semester(self):
        sem_no = len(self.semesters) + 1
        sem = Semester(sem_no)
        self.semesters.append(sem)
        print(f"\n--- Semester {sem_no} Added ---")

    def add_course_to_semester(self):
        if not self.semesters:
            print("No semesters added yet. Add a semester first.")
            return
        self.list_semesters()
        idx = input("Select semester number: ")
        try:
            idx = int(idx) - 1
            sem = self.semesters[idx]
        except:
            print("Invalid selection.")
            return
        sem.add_course()

    def calculate_gpa_for_semester(self):
        if not self.semesters:
            print("No semesters added yet.")
            return
        self.list_semesters()
        idx = input("Select semester number: ")
        try:
            idx = int(idx) - 1
            sem = self.semesters[idx]
        except:
            print("Invalid selection.")
            return
        gpa = sem.calculate_gpa()
        if gpa is not None:
            print(f"GPA for Semester {sem.semester_no}: {gpa:.2f}")
        else:
            print("No courses added yet.")

    def calculate_cgpa(self):
        total_points = 0
        total_credits = 0
        for sem in self.semesters:
            for _, grade_point, credits in sem.courses:
                total_points += grade_point * credits
                total_credits += credits
        if total_credits == 0:
            print("No courses added yet.")
            return
        cgpa = total_points / total_credits
        print(f"CGPA across all semesters: {cgpa:.2f}")

    def list_semesters(self):
        print("\nSemesters:")
        for idx, sem in enumerate(self.semesters):
            print(f"{idx+1}. Semester {sem.semester_no}")

    def list_all_courses(self):
        if not self.semesters:
            print("No semesters added yet.")
            return
        for sem in self.semesters:
            sem.list_courses()

    def menu(self):
        while True:
            print("\n=== GPA and CGPA Calculator ===")
            print("1. Add Semester")
            print("2. Add Course to Semester")
            print("3. List All Courses")
            print("4. Calculate GPA for a Semester")
            print("5. Calculate CGPA")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_semester()
            elif choice == "2":
                self.add_course_to_semester()
            elif choice == "3":
                self.list_all_courses()
            elif choice == "4":
                self.calculate_gpa_for_semester()
            elif choice == "5":
                self.calculate_cgpa()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    sr = StudentRecord()
    sr.menu()