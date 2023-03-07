import string
import random

from domain.entity_student import Student


class ServiceStudent:
    def __init__(self, validator, repo_students):
        self.__validator = validator
        self.__repo_students = repo_students

    def no_of_students(self):
        """
        A function that returns the number of students in the service's repo.
        :return: The number of elements...
        """
        return len(self.__repo_students)

    def add_student(self, studentID, student_name, student_group):
        """
        A service function that adds a student to the students' repo.
        :param studentID: The student's id.
        :param student_name: The student's name.
        :param student_group: The student's group.
        """
        student_to_add = Student(studentID, student_name, student_group)
        self.__validator.validate_student(student_to_add)
        self.__repo_students.add_student(student_to_add)

    def remove_student(self, studentID):
        """
        A service function that removes a student from the students' repo.
        :param studentID: The id of the student to remove.
        """
        self.__repo_students.remove_student_by_id(studentID)

    def get_all_students(self):
        """
        A service function that returns all the elements in the students' repo.
        :return: All the elements in the students' repo.
        """
        return self.__repo_students.get_all()

    def get_student_by_id(self, student_id):
        """
        A service function that finds a student by his ID.
        :student_id: The id to search the student by.
        :return: The found student.
        """

        return self.__repo_students.get_student_by_id(student_id)

    def filter_students_by_name_prefix(self, prefix):
        """
        A service function that handles filtering the list of students by the prefixes of their name.
        :param prefix: The prefix the names of the required students must start with.
        :return:
        """
        return self.__repo_students.filter_by_name_prefix(prefix)

    def generate_student_random_string_field(self):
        length = random.randint(3, 12)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def generate_unique_id(self):
        return self.__repo_students.generate_unique_id()

    def add_random_student(self):
        studentID = self.generate_unique_id()
        student_name = self.generate_student_random_string_field()
        student_group = self.generate_student_random_string_field()

        self.add_student(studentID, student_name, student_group)

    """
    def generate_student_random_name(self):
        id = random.randint(0, 1000000)

        while True:
            try:
                student = self.get_student_by_id(id)
            except RepositoryError as re:
    """