import random

from Exceptions.EmptyRepositoryError import EmptyRepositoryError
from Exceptions.RandomnessExceededError import RandomnessExceededError
from Exceptions.RepositoryError import RepositoryError
from domain.assignment_dto import AssignmentDTO


class ServiceAssignment:
    def __init__(self, validator, repo_assignments, repo_students, repo_problems):
        self.__validator = validator
        self.__repo_assignments = repo_assignments
        self.__repo_students = repo_students
        self.__repo_problems = repo_problems

    def add_assignment(self, studentID, lab_number, problem_number, grade = None):
        """
        A service function that adds an assignment to the list.
        :param studentID: The ID of the student to receive the assignment.
        :param lab_number: The number of the lab containing the problem to assign.
        :param problem_number: The number of the problem to assign.
        :param grade: An optional parameter specifying if an assignment should be graded.
        """

        assignment_to_add = AssignmentDTO(studentID, lab_number, problem_number)
        student_to_link = self.__repo_students.get_student_by_id(studentID)
        problem_to_link = self.__repo_problems.get_problem_by_num(lab_number, problem_number)
        self.__repo_assignments.add_assignment(assignment_to_add)

    def grade_assignment(self, studentID, lab_number, problem_number, grade):
        """
        A service function that grades an assignment.
        :param studentID: The ID of the student that has the assignment.
        :param lab_number: The number of the lab containing the problem in the assignment.
        :param problem_number: The number of the problem in the assignment.
        :param grade: The grade to issue to the assignment.
        """
        self.__repo_assignments.grade_assignment(studentID, lab_number, problem_number, grade)
        #TODO Update student average. Does this violate GRASP? service_assignment is not the information expert for students
        new_average = self.__repo_assignments.calculate_and_get_average_for_student(studentID)
        self.__repo_students.get_student_by_id(studentID).set_lab_average(new_average)

        new_problem_average = self.__repo_assignments.calculate_and_get_average_for_problem(lab_number, problem_number)
        self.__repo_problems.get_problem_by_num(lab_number, problem_number).set_lab_average(new_problem_average)
        self.__repo_problems.get_problem_by_num(lab_number, problem_number).set_num_of_students(self.__repo_assignments.calculate_and_get_number_of_students_per_problem(lab_number, problem_number))

    def get_all_assignments(self):
        """
        A service function that returns a list of all the assignments in the repo.
        :return:A list of all the assignments in the repo.
        """
        return self.__repo_assignments.get_all()

    def no_of_assignments(self):
        """
        Service function that returns the number of assignments stored.
        :return: The number of assignments stored.
        """
        return len(self.__repo_assignments)



    def add_random_assignment(self):
        counter = 0
        while True:
            counter += 1

            try:
                studentID = self.__repo_students.get_random_student().get_studentID()
            except EmptyRepositoryError as re:
                assert (str(re) == "Nu exista studenti din care sa fie ales unul")
                return


            try:
                problem = self.__repo_problems.get_random_problem()
                lab_number = problem.get_lab_number()
                problem_number = problem.get_problem_number()
            except EmptyRepositoryError as re:
                assert(str(re) == "Nu exista probleme din care sa fie aleasa una")
                return

            try:
                self.add_assignment(studentID, lab_number, problem_number, random.randrange(0, 10))
                break
            except RepositoryError as re:
                assert(str(re) == "Assignment duplicat")

            if counter > 100000:
                raise RandomnessExceededError("Nu mai sunt laboratoare care sa poata fi asignate")