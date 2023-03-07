import random
import string
from datetime import date

from domain.entity_problem import Problem


class ServiceProblem:
    def __init__(self, validator, repo_problems):
        self.__validator = validator
        self.__repo_problems = repo_problems

    def add_problem(self, lab_number, problem_number, problem_description, problem_deadline):
        """
        A service function that calls all necessary functions to add a problem to the problem repo.
        :param lab_number: The number of the lab the problem belongs to.
        :param problem_number: The number of the problem.
        :param problem_description: The description of the problem.
        :param problem_deadline: The deadline of the problem.
        """

        problem_to_add = Problem(lab_number, problem_number, problem_description, problem_deadline)
        self.__validator.validate_problem(problem_to_add)
        self.__repo_problems.add_problem(problem_to_add)

    def no_of_problems(self):
        """
        A function that calculates and returns the number of elements in the repo of a service.
        :return: The number of elements in the service's repo.
        """
        return len(self.__repo_problems)

    def remove_problem(self, lab_number, problem_number):
        """
        A service function that calls all necessary functions to remove a problem from the problem repo.
        :param lab_number: The number of the lab the problem is in.
        :param problem_number: The number of the problem.
        :return:
        """
        #TODO
        #Is it ok to just call a method from the repo here, no other checks?
        return self.__repo_problems.remove_problem_by_num(lab_number, problem_number)

    def get_problem_by_num(self, lab_number, problem_number):
        """
        A service function that finds a problem by its num.
        :lab_number: The number of the lab containing the problem.
        :problem_number: The number of the problem itself.
        :return: The found problem.
        """

        return self.__repo_problems.get_problem_by_num(lab_number, problem_number)

    def get_all_problems(self):
        """
        A service function that returns a list of all the problems in the repo.
        :return: A list of all the problems in the repo.
        """
        return self.__repo_problems.get_all()

    def generate_student_random_string_field(self):
        length = random.randint(3, 7)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def generate_unique_problem_number(self, lab_num):
        return self.__repo_problems.generate_unique_problem_number(lab_num)

    def add_random_problem(self):
        lab_number = self.generate_student_random_string_field()
        problem_number = self.generate_unique_problem_number(lab_number)
        problem_description = self.generate_student_random_string_field()
        problem_deadline = date(random.randint(2000, 2900), random.randint(1, 12), random.randint(1, 28))

        self.add_problem(lab_number, problem_number, problem_description, problem_deadline)