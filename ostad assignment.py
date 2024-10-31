import json


# Class Definitions
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        if subject in self.courses:
            self.grades[subject] = grade
            print(f"Grade {grade} added for {self.name} in {subject}.")
        else:
            print(f"Error: Student {self.name} is not enrolled in {subject}.")

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            return True  # Indicate successful enrollment
        return False  # Indicate the student was already enrolled

    def display_student_info(self):
        self.display_person_info()
        print(f"ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses)}")
        print(f"Grades: {self.grades}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            return True  # Indicate that the student was added
        return False  # Indicate the student was already enrolled

    def display_course_info(self):
        print(f"Course Name: {self.course_name}")
        print(f"Course Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        print("Enrolled Students:", ", ".join([student.name for student in self.students]))


# System Functionalities
class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        student = Student(name, age, address, student_id)
        self.students[student_id] = student

    def add_course(self):
        course_name = input("Enter Course Name: ")
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")
        course = Course(course_name, course_code, instructor)
        self.courses[course_code] = course
        print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

    def enroll_student_in_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")

        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]

            # Enroll student in the course
            student.enroll_course(course.course_name)
            course.add_student(student)

            # Output in the specified format
            print(
                f"Student {student.name} (ID: {student.student_id}) enrolled in {course.course_name} (Code: {course.course_code}).")
        else:
            print("Invalid Student ID or Course Code.")

    def add_grade_for_student(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if student and course:
            student.add_grade(course.course_name, grade)
        else:
            print("Error: Invalid student ID or course code.")

    def display_student_details(self):

        student_id = input("Enter Student ID: ")
        print("Student Information:")
        student = self.students.get(student_id)
        if student:
            student.display_student_info()
        else:
            print("Error: Student not found.")

    def display_course_details(self):
        course_code = input("Enter Course Code: ")
        print("Course Information:")
        course = self.courses.get(course_code)
        if course:
            course.display_course_info()
        else:
            print("Error: Course not found.")

    import json

    def save_data(self):
        # Prepare data to be JSON-serializable by converting custom objects to dictionaries
        data = {
            "students": {
                sid: {
                    "name": student.name,
                    "age": student.age,
                    "address": student.address,
                    "student_id": student.student_id,
                    "grades": student.grades,
                    "courses": student.courses
                } for sid, student in self.students.items()
            },
            "courses": {
                code: {
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "instructor": course.instructor,
                    "students": [student.student_id for student in course.students]  # List of student IDs
                } for code, course in self.courses.items()
            }
        }

        # Save data to JSON file
        try:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            print("All student and course data saved successfully.")
        except Exception as e:
            print("Error saving data:", e)

    def load_data(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
            # Load students
            self.students = {}
            for sid, info in data.get("students", {}).items():
                student = Student(
                    name=info["name"],
                    age=info["age"],
                    address=info["address"],
                    student_id=info["student_id"]
                )
                student.grades = info.get("grades", {})
                student.courses = info.get("courses", [])
                self.students[sid] = student
            # Load courses
            self.courses = {}
            for code, info in data.get("courses", {}).items():
                course = Course(
                    course_name=info["course_name"],
                    course_code=info["course_code"],
                    instructor=info["instructor"]
                )
                # Enroll students by ID
                course.students = [self.students[sid] for sid in info.get("students", []) if sid in self.students]
                self.courses[code] = course

            print("Data loaded successfully.")
        except Exception as e:
            print("Error loading data:", e)

    def menu(self):
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Save Data to File")
            print("8. Load Data from File")
            print("0. Exit")
            choice = input("Select Option: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_course()
            elif choice == "3":
                self.enroll_student_in_course()
            elif choice == "4":
                self.add_grade_for_student()
            elif choice == "5":
                self.display_student_details()
            elif choice == "6":
                self.display_course_details()
            elif choice == "7":
                self.save_data()
            elif choice == "8":
                self.load_data()
            elif choice == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


# Initialize the system and start the menu
sms = StudentManagementSystem()
sms.menu()
