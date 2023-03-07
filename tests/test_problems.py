import unittest
from datetime import date

from Exceptions.RepositoryError import RepositoryError
from Exceptions.ValidationError import ValidationError
from controller.service_problem import ServiceProblem
from domain.entity_problem import Problem
from infratructure.repo_problems import RepoProblems, FileRepoProblems
from validation.problem_validator import ProblemValidator


class ProblemsTests(unittest.TestCase):
    def setUp(self):
        self.lab_number = "1"
        self.problem_num = "2"
        self.problem_description = "Some problem, idk"
        self.problem_deadline = date(2021, 11, 19)
        self.problem = Problem(self.lab_number, self.problem_num, self.problem_description, self.problem_deadline)

        self.lab_number2 = "1"
        self.problem_num2 = "3"
        self.problem_description2 = "Some problem, idk2"
        self.problem_deadline2 = date(2022, 10, 20)
        self.problem2 = Problem(self.lab_number2, self.problem_num2, self.problem_description2, self.problem_deadline2)

        self.lab_number3 = "1"
        self.problem_num3 = "4"
        self.problem_description3 = "Some problem, idk3"
        self.problem_deadline3 = date(2021, 11, 21)
        self.problem3 = Problem(self.lab_number3, self.problem_num3, self.problem_description3, self.problem_deadline3)

        self.lab_number4 = "1"
        self.problem_num4 = "5"
        self.problem_description4 = "Some problem, idk4"
        self.problem_deadline4 = date(2021, 11, 22)
        self.problem4 = Problem(self.lab_number4, self.problem_num4, self.problem_description4, self.problem_deadline4)

        self.lab_number5 = "1"
        self.problem_num5 = "6"
        self.problem_description5 = "Some problem, idk5"
        self.problem_deadline5 = date(2021, 11, 23)
        self.problem5 = Problem(self.lab_number5, self.problem_num5, self.problem_description5, self.problem_deadline5)

        self.repo_problems = RepoProblems()
        self.file_repo_problems = FileRepoProblems("tests/TestProblems.txt")
        self.problem_validator = ProblemValidator()

        self.srv_problems = ServiceProblem(self.problem_validator, self.repo_problems)

    def test_create_problem(self):
        """
        Test function for create_problem.
        """

        self.assertTrue(self.problem.get_lab_number() == self.lab_number)
        self.assertTrue(self.problem.get_problem_number() == self.problem_num)
        self.assertTrue(self.problem.get_description() == self.problem_description)
        self.assertTrue(self.problem.get_deadline() == self.problem_deadline)

        other_lab_number = "1"
        other_problem_num = "2"
        other_problem_description = "Some problem, idk2"
        other_problem_deadline = date(2022, 10, 20)
        other_problem = Problem(other_lab_number, other_problem_num, other_problem_description, other_problem_deadline)

        self.assertEqual(self.problem, other_problem)
        self.assertTrue(self.problem.__eq__(other_problem))

        self.assertEqual(str(self.problem), "[1_2]Some problem, idk[19-11-2021]")
        self.assertEqual(self.problem.__str__(), "[1_2]Some problem, idk[19-11-2021]")

    def test_validate_problem(self):
        """
        Test function for validate_problem.
        """

        self.problem_validator.validate_problem(self.problem)

        inv_lab_number = ""
        inv_problem_num = ""
        inv_problem_description = ""
        inv_problem = Problem(inv_lab_number, inv_problem_num, inv_problem_description, self.problem_deadline)

        self.assertRaises(ValidationError, self.problem_validator.validate_problem, inv_problem)

    def test_add_problem_to_repo(self):
        """
        Test function for add_problem_to_repo.
        """
        self.assertEqual(len(self.repo_problems), 0)
        self.assertEqual(self.repo_problems.__len__(), 0)

        self.repo_problems.add_problem(self.problem)

        self.assertTrue(len(self.repo_problems), 1)
        self.assertTrue(self.repo_problems.__len__(), 1)

        found_problem = self.repo_problems.get_problem_by_num(self.lab_number, self.problem_num)
        self.assertTrue(found_problem, self.problem)
        self.assertTrue(found_problem.get_description(), self.problem_description)
        self.assertTrue(found_problem.get_deadline(), self.problem_deadline)

        inexist_lab_number = "4"
        inexist_problem_number = "12"

        self.assertRaises(RepositoryError, self.repo_problems.get_problem_by_num, inexist_lab_number, inexist_problem_number)

        other_description = "3"
        other_deadline = "14"
        other_problem = Problem(self.lab_number, self.problem_num, other_description, other_deadline)

        self.assertRaises(RepositoryError, self.repo_problems.add_problem, other_problem)

    def test_add_problem_service(self):
        """
        Test function for add_problem_service.
        """
        self.assertEqual(self.srv_problems.no_of_problems(), 0)
        self.srv_problems.add_problem(self.lab_number, self.problem_num, self.problem_description, self.problem_deadline)
        self.assertEqual(self.srv_problems.no_of_problems(), 1)

        self.assertRaises(RepositoryError, self.srv_problems.add_problem, self.lab_number, self.problem_num, self.problem_description, self.problem_deadline)

        inv_lab_number = ""
        inv_problem_num = ""
        inv_problem_description = ""

        self.assertRaises(ValidationError, self.srv_problems.add_problem, inv_lab_number, inv_problem_num, inv_problem_description, self.problem_deadline)

    def test_remove_problem_by_num(self):
        """
        Test function for remove_problem_by_num.
        """
        self.assertEqual(len(self.repo_problems), 0)
        self.repo_problems.add_problem(self.problem)
        self.assertEqual(len(self.repo_problems), 1)

        self.repo_problems.remove_problem_by_num(self.lab_number, self.problem_num)

        self.assertEqual(len(self.repo_problems), 0)

        invalid_lab_number = "10"
        invalid_problem_number = "20"

        self.assertRaises(RepositoryError, self.repo_problems.remove_problem_by_num, invalid_lab_number, invalid_problem_number)

    def test_remove_problem_by_num_service(self):
        """
        Test function for remove_problem_by_num_service.
        """

        self.assertEqual(self.srv_problems.no_of_problems(), 0)
        self.srv_problems.add_problem(self.lab_number, self.problem_num, self.problem_description, self.problem_deadline)
        self.assertEqual(self.srv_problems.no_of_problems(), 1)

        self.srv_problems.remove_problem(self.lab_number, self.problem_num)

        self.assertEqual(self.srv_problems.no_of_problems(), 0)

        invalid_lab_number = "10"
        invalid_problem_number = "20"

        self.assertRaises(RepositoryError, self.srv_problems.remove_problem, invalid_lab_number, invalid_problem_number)

    def test_get_problem_by_num_service(self):
        """
        Function that tests the get_problem_by_num service function.
        """

        self.assertEqual(self.srv_problems.no_of_problems(), 0)
        self.srv_problems.add_problem(self.lab_number, self.problem_num, self.problem_description, self.problem_deadline)
        self.assertEqual (self.srv_problems.no_of_problems(), 1)

        found_problem = self.srv_problems.get_problem_by_num(self.lab_number, self.problem_num)
        self.assertEqual(found_problem.get_lab_number(), self.lab_number)
        self.assertEqual(found_problem.get_problem_number(), self.problem_num)
        self.assertEqual(found_problem.get_description(), self.problem_description)
        self.assertEqual(found_problem.get_deadline(), self.problem_deadline)

        inexist_lab_num = "10"
        inexist_problem_num = "9"

        self.assertRaises(RepositoryError, self.srv_problems.get_problem_by_num, inexist_lab_num, inexist_problem_num)

    def test_problems_get_all(self):
        """
        Test function that tests the get_all repo function for problems.
        """
        self.repo_problems.add_problem(self.problem)
        self.repo_problems.add_problem(self.problem2)
        self.repo_problems.add_problem(self.problem3)

        got_list = self.repo_problems.get_all()
        self.assertEqual(got_list[0], self.problem)
        self.assertEqual(got_list[1], self.problem2)
        self.assertEqual(got_list[2], self.problem3)

    def test_problems_get_all_service(self):
        """
        Test function that tests the get_all service function for problems.
        """
        self.repo_problems.add_problem(self.problem)
        self.repo_problems.add_problem(self.problem2)
        self.repo_problems.add_problem(self.problem3)

        got_list = self.srv_problems.get_all_problems()

        self.assertEqual(got_list[0], self.problem)
        self.assertEqual(got_list[1], self.problem2)
        self.assertEqual(got_list[2], self.problem3)


