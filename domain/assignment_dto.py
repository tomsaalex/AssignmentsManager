class AssignmentDTO:
    def __init__(self, studentID, lab_number, problem_number, grade = None):
        self.__studentID = studentID
        self.__lab_number = lab_number
        self.__problem_number = problem_number
        self.__grade = grade
        self.student = None
        self.problem = None

    def __str__(self):
        return f"{self.__studentID}, {self.__lab_number}, {self.__problem_number}"

    def __eq__(self, other):
        return self.__studentID == other.__studentID and self.__lab_number == other.__lab_number and self.__problem_number == other.__problem_number

    def get_studentID(self):
        return self.__studentID

    def get_lab_number(self):
        return self.__lab_number

    def get_problem_number(self):
        return self.__problem_number

    def get_grade(self):
        return self.__grade

    def set_grade(self, new_grade):
        self.__grade = new_grade

    def get_problem(self):
        return self.problem

    def get_student(self):
        return self.student

    def set_problem(self, problem):
        self.__problem = problem

    def set_student(self, student):
        self.__student = student