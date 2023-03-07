import unittest
from datetime import date

from Exceptions.RepositoryError import RepositoryError
from Exceptions.ValidationError import ValidationError
from controller.service_assignment import ServiceAssignment
from controller.service_problem import ServiceProblem
from controller.service_statistics import ServiceStatistics
from controller.service_student import ServiceStudent
from domain.assignment_dto import AssignmentDTO
from domain.entity_problem import Problem
from domain.entity_student import Student
from infratructure.repo_assignments import RepoAssignments, FileRepoAssignments
from infratructure.repo_problems import RepoProblems, FileRepoProblems
from infratructure.repo_students import RepoStudents, FileRepoStudents
from validation.assignment_validator import AssignmentValidator
from validation.problem_validator import ProblemValidator
from validation.student_validator import StudentValidator


class AssignmentsTests(unittest.TestCase):
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

        self.studentID = 0
        self.student_name = "Alex"
        self.student_group = "2222"
        self.student = Student(self.studentID, self.student_name, self.student_group)

        self.studentID2 = 1
        self.student_name2 = "Alex2"
        self.student_group2 = "22223"
        self.student2 = Student(self.studentID2, self.student_name2, self.student_group2)

        self.studentID3 = 3
        self.student_name3 = "Alex3"
        self.student_group3 = "2224"
        self.student3 = Student(self.studentID3, self.student_name3, self.student_group3)

        self.assignment = AssignmentDTO(self.studentID, self.lab_number, self.problem_num)
        self.assignment2 = AssignmentDTO(self.studentID2, self.lab_number2, self.problem_num2)
        self.assignment3 = AssignmentDTO(self.studentID3, self.lab_number3, self.problem_num3)

        self.repo_problems = RepoProblems()
        self.repo_students = RepoStudents()
        self.repo_assignments = RepoAssignments()

        self.file_repo_problems = FileRepoProblems("tests/TestProblems.txt")
        self.file_repo_students = FileRepoStudents("tests/TestStudents.txt")
        self.file_repo_assignments = FileRepoAssignments("tests/TestAssignments.txt")

        self.problem_validator = ProblemValidator()
        self.student_validator = StudentValidator()
        self.assignment_validator = AssignmentValidator()

        self.srv_problems = ServiceProblem(self.problem_validator, self.repo_problems)
        self.srv_students = ServiceStudent(self.student_validator, self.repo_students)
        self.srv_assignments = ServiceAssignment(self.assignment_validator, self.repo_assignments, self.repo_students,
                                                 self.repo_problems)
        self.srv_statistics = ServiceStatistics(self.repo_students, self.repo_problems, self.repo_assignments)

    def test_create_assignment(self):
        """
        Function that tests the assignment creating function.
        :return:
        """

        self.assertEqual(self.assignment.get_lab_number(), self.lab_number)
        self.assertEqual(self.assignment.get_problem_number(), self.problem_num)
        self.assertEqual(self.assignment.get_studentID(), self.studentID)
        self.assertTrue(self.assignment.get_grade() is None)

        self.assertEqual(str(self.assignment), "0, 1, 2")
        self.assertEqual(self.assignment.__str__(), "0, 1, 2")

    def test_add_assignment_to_repo(self):
        """
        Test function that tests the assignment adding repo function.
        """

        self.assertEqual(len(self.repo_assignments), 0)
        self.repo_assignments.add_assignment(self.assignment)
        self.assertEqual(len(self.repo_assignments), 1)

        found_assignment = self.repo_assignments.get_assignment_by_ids(self.studentID, self.lab_number, self.problem_num)

        self.assertEqual(found_assignment.get_studentID(), self.studentID)
        self.assertEqual(found_assignment.get_problem_number(), self.problem_num)
        self.assertEqual(found_assignment.get_lab_number(), self.lab_number)
        self.assertTrue(found_assignment.get_grade() is None)

        self.assertRaises(RepositoryError, self.repo_assignments.add_assignment, self.assignment)

        invalid_studentID = -34
        invalid_lab_number = "30"
        invalid_problem_number = "27"

        self.assertRaises(RepositoryError, self.repo_assignments.get_assignment_by_ids, invalid_studentID, invalid_lab_number, invalid_problem_number)

    def test_add_assignment_service(self):
        """
        Test function that tests the assignment adding service function.
        """

        self.repo_students.add_student(self.student)
        self.repo_problems.add_problem(self.problem)


        self.assertEqual(self.srv_assignments.no_of_assignments(), 0)
        self.srv_assignments.add_assignment(self.studentID, self.lab_number, self.problem_num)
        self.assertEqual(self.srv_assignments.no_of_assignments(), 1)

        self.assertRaises(RepositoryError, self.srv_assignments.add_assignment, self.studentID, self.lab_number, self.problem_num)

    def test_assignments_get_all(self):
        """
        Test function that tests the get_all repo function for assignments.
        """

        self.repo_assignments.add_assignment(self.assignment)
        self.repo_assignments.add_assignment(self.assignment2)
        self.repo_assignments.add_assignment(self.assignment3)

        got_list = self.repo_assignments.get_all()
        self.assertEqual(got_list[0], self.assignment)
        self.assertEqual(got_list[1], self.assignment2)
        self.assertEqual(got_list[2], self.assignment3)

    def test_assignments_get_all_service(self):
        """
        Test function that tests the get_all service function for assignments.
        """

        self.repo_assignments.add_assignment(self.assignment)
        self.repo_assignments.add_assignment(self.assignment2)
        self.repo_assignments.add_assignment(self.assignment3)

        # TODO
        # Is this wrong? I added the assignments to the repo with the repo functions, not the service functions to save time.

        got_list = self.srv_assignments.get_all_assignments()
        self.assertEqual(got_list[0], self.assignment)
        self.assertEqual(got_list[1], self.assignment2)
        self.assertEqual(got_list[2], self.assignment3)


    def test_get_assignments_for_problem(self):
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)
        self.repo_students.add_student(student)

        studentID2 = 1
        student_name2 = "1had"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)
        self.repo_students.add_student(student2)

        studentID3 = 3
        student_name3 = "0Dan"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)
        self.repo_students.add_student(student3)

        studentID4 = 4
        student_name4 = "Michael"
        student_group4 = "220"
        student4 = Student(studentID4, student_name4, student_group4)
        self.repo_students.add_student(student4)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)
        self.repo_problems.add_problem(problem)

        assignment1 = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number, problem_num)
        assignment2.set_grade(10)
        assignment3 = AssignmentDTO(studentID3, lab_number, problem_num)
        assignment3.set_grade(7)

        self.repo_assignments.add_assignment(assignment1)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)

        assignments_that_fit = self.srv_statistics.get_assignments_for_problem(lab_number, problem_num)

        self.assertEqual(assignments_that_fit[0].get_studentID(), studentID2)
        self.assertEqual(assignments_that_fit[1].get_studentID(), studentID3)



    def test_grade_assignment_repo(self):
        """
        Test function that checks the assignment grading repo function.
        """

        # region Declaring the students and problems
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)

        studentID2 = 1
        student_name2 = "Alex2"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)

        studentID3 = 3
        student_name3 = "Alex3"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)

        lab_number2 = "8"
        problem_num2 = "13"
        problem_description2 = "Some problem, idk2"
        problem_deadline2 = date(2021, 11, 20)
        problem2 = Problem(lab_number2, problem_num2, problem_description2, problem_deadline2)

        lab_number3 = "9"
        problem_num3 = "14"
        problem_description3 = "Some problem, idk3"
        problem_deadline3 = date(2021, 11, 21)
        problem3 = Problem(lab_number3, problem_num3, problem_description3, problem_deadline3)
        # endregion

        assignment1 = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number2, problem_num2)
        assignment3 = AssignmentDTO(studentID3, lab_number3, problem_num3)

        self.repo_assignments.add_assignment(assignment1)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)

        self.repo_assignments.grade_assignment(studentID, lab_number, problem_num, 10)
        found_assignment = self.repo_assignments.get_assignment_by_ids(studentID, lab_number, problem_num)
        self.assertEqual(found_assignment.get_grade(), 10)

    def test_grade_assignment_service(self):
        """
        Test function that checks the assignment grading service function
        """
        # region definitions
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)
        self.repo_students.add_student(student)

        studentID2 = 1
        student_name2 = "Alex2"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)
        self.repo_students.add_student(student2)

        studentID3 = 3
        student_name3 = "Alex3"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)
        self.repo_students.add_student(student3)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)
        self.repo_problems.add_problem(problem)

        lab_number2 = "8"
        problem_num2 = "13"
        problem_description2 = "Some problem, idk2"
        problem_deadline2 = date(2021, 11, 20)
        problem2 = Problem(lab_number2, problem_num2, problem_description2, problem_deadline2)
        self.repo_problems.add_problem(problem2)

        lab_number3 = "9"
        problem_num3 = "14"
        problem_description3 = "Some problem, idk3"
        problem_deadline3 = date(2021, 11, 21)
        problem3 = Problem(lab_number3, problem_num3, problem_description3, problem_deadline3)
        self.repo_problems.add_problem(problem3)
        # endregion


        self.srv_assignments.add_assignment(studentID, lab_number, problem_num)
        self.srv_assignments.add_assignment(studentID2, lab_number2, problem_num2)
        self.srv_assignments.add_assignment(studentID3, lab_number3, problem_num3)

        self.srv_assignments.grade_assignment(studentID, lab_number, problem_num, 10)
        self.srv_assignments.grade_assignment(studentID2, lab_number2, problem_num2, 8)
        self.srv_assignments.grade_assignment(studentID3, lab_number3, problem_num3, 7)

        found_assignment = self.repo_assignments.get_assignment_by_ids(studentID, lab_number, problem_num)
        self.assertEqual(found_assignment.get_grade(), 10)

        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_student(studentID), 10)
        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_student(studentID2), 8)
        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_student(studentID3), 7)

        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number, problem_num), 10)
        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number2, problem_num2), 8)
        self.assertEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number3, problem_num3), 7)

    def test_calculate_and_get_number_of_students_per_problem(self):
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)
        self.repo_students.add_student(student)

        studentID2 = 1
        student_name2 = "Alex2"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)
        self.repo_students.add_student(student2)

        studentID3 = 3
        student_name3 = "Alex3"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)
        self.repo_students.add_student(student3)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)
        self.repo_problems.add_problem(problem)

        assignment = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number, problem_num)
        assignment3 = AssignmentDTO(studentID3, lab_number, problem_num)

        self.assertEqual(self.repo_assignments.calculate_and_get_number_of_students_per_problem(lab_number, problem_num), 0)

        self.repo_assignments.add_assignment(assignment)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)

        self.assertEqual(self.repo_assignments.calculate_and_get_number_of_students_per_problem(lab_number, problem_num), 3)

    def test_get_top_50per_most_assigned_problem(self):
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)
        self.repo_students.add_student(student)

        studentID2 = 1
        student_name2 = "Alex2"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)
        self.repo_students.add_student(student2)

        studentID3 = 3
        student_name3 = "Alex3"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)
        self.repo_students.add_student(student3)

        studentID4 = 4
        student_name4 = "Alex4"
        student_group4 = "2225"
        student4 = Student(studentID4, student_name4, student_group4)
        self.repo_students.add_student(student4)

        studentID5 = 5
        student_name5 = "Alex5"
        student_group5 = "2226"
        student5 = Student(studentID5, student_name5,student_group5)
        self.repo_students.add_student(student5)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)
        self.repo_problems.add_problem(problem)

        lab_number2 = "8"
        problem_num2 = "13"
        problem_description2 = "Some problem, idk2"
        problem_deadline2 = date(2022, 10, 20)
        problem2 = Problem(lab_number2, problem_num2, problem_description2, problem_deadline2)
        self.repo_problems.add_problem(problem2)

        lab_number3 = "9"
        problem_num3 = "14"
        problem_description3 = "Some problem, idk3"
        problem_deadline3 = date(2021, 11, 21)
        problem3 = Problem(lab_number3, problem_num3, problem_description3, problem_deadline3)
        self.repo_problems.add_problem(problem3)

        lab_number4 = "10"
        problem_num4 = "15"
        problem_description4 = "Some problem, idk4"
        problem_deadline4 = date(2021, 11, 22)
        problem4 = Problem(lab_number4, problem_num4, problem_description4, problem_deadline4)
        self.repo_problems.add_problem(problem4)

        lab_number5 = "11"
        problem_num5 = "16"
        problem_description5 = "Some problem, idk5"
        problem_deadline5 = date(2021, 11, 23)
        problem5 = Problem(lab_number5, problem_num5, problem_description5, problem_deadline5)
        self.repo_problems.add_problem(problem5)



        assignment = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number, problem_num)
        assignment3 = AssignmentDTO(studentID3, lab_number, problem_num)
        assignment4 = AssignmentDTO(studentID3, lab_number2, problem_num2)
        assignment5 = AssignmentDTO(studentID4, lab_number2, problem_num2)
        assignment6 = AssignmentDTO(studentID4, lab_number3, problem_num3)
        assignment7 = AssignmentDTO(studentID5, lab_number3, problem_num3)
        assignment8 = AssignmentDTO(studentID5, lab_number2, problem_num2)
        assignment9 = AssignmentDTO(studentID4, lab_number4, problem_num4)
        assignment10 = AssignmentDTO(studentID5, lab_number5, problem_num5)
        assignment11 = AssignmentDTO(studentID2, lab_number3, problem_num3)
        assignment12 = AssignmentDTO(studentID2, lab_number4, problem_num4)
        assignment13 = AssignmentDTO(studentID3, lab_number4, problem_num4)

        self.repo_assignments.add_assignment(assignment)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)
        self.repo_assignments.add_assignment(assignment4)
        self.repo_assignments.add_assignment(assignment5)
        self.repo_assignments.add_assignment(assignment6)
        self.repo_assignments.add_assignment(assignment7)
        self.repo_assignments.add_assignment(assignment8)
        self.repo_assignments.add_assignment(assignment9)
        self.repo_assignments.add_assignment(assignment10)
        self.repo_assignments.add_assignment(assignment11)
        self.repo_assignments.add_assignment(assignment12)
        self.repo_assignments.add_assignment(assignment13)

        self.repo_assignments.grade_assignment(studentID, lab_number, problem_num, 10)
        self.repo_assignments.grade_assignment(studentID2, lab_number, problem_num, 5)
        self.repo_assignments.grade_assignment(studentID3, lab_number, problem_num, 5)

        self.repo_assignments.grade_assignment(studentID3, lab_number2, problem_num2, 7)
        self.repo_assignments.grade_assignment(studentID4, lab_number2, problem_num2, 5)
        self.repo_assignments.grade_assignment(studentID5, lab_number2, problem_num2, 8)

        self.repo_assignments.grade_assignment(studentID4, lab_number3, problem_num3, 7)
        self.repo_assignments.grade_assignment(studentID5, lab_number3, problem_num3, 6)
        self.repo_assignments.grade_assignment(studentID2, lab_number3, problem_num3, 6)

        self.repo_assignments.grade_assignment(studentID4, lab_number4, problem_num4, 6)
        self.repo_assignments.grade_assignment(studentID2, lab_number4, problem_num4, 7)
        self.repo_assignments.grade_assignment(studentID3, lab_number4, problem_num4, 8)

        self.repo_assignments.grade_assignment(studentID5, lab_number5, problem_num5, 6)

        list_of_problems = self.srv_statistics.get_top_50per_most_assigned_problem()

        self.assertEqual(len(list_of_problems), 2)

        self.assertEqual(list_of_problems[0], problem)
        self.assertEqual(list_of_problems[1], problem2)

        self.repo_assignments.grade_assignment(studentID, lab_number, problem_num, 1)

        list_of_problems = self.srv_statistics.get_top_50per_most_assigned_problem()

        self.assertEqual(len(list_of_problems), 1)
        self.assertEqual(list_of_problems[0], problem2)

    def test_calculate_and_get_average_for_problem(self):
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)

        studentID2 = 1
        student_name2 = "Paul"
        student_group2 = "2235"
        student2 = Student(studentID2, student_name2, student_group2)

        studentID3 = 2
        student_name3 = "Darrow"
        student_group3 = "22"
        student3 = Student(studentID3, student_name3, student_group3)

        studentID4 = 3
        student_name4 = "Layton"
        student_group4 = "27"
        student4 = Student(studentID4, student_name4, student_group4)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)

        assignment = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number, problem_num)
        assignment3 = AssignmentDTO(studentID3, lab_number, problem_num)
        assignment4 = AssignmentDTO(studentID4, lab_number, problem_num)

        self.repo_students.add_student(student)
        self.repo_students.add_student(student2)
        self.repo_students.add_student(student3)
        self.repo_students.add_student(student4)

        self.repo_problems.add_problem(problem)

        self.repo_assignments.add_assignment(assignment)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)

        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number, problem_num), 0)

        self.repo_assignments.grade_assignment(studentID, lab_number, problem_num, 6)
        self.repo_assignments.grade_assignment(studentID2, lab_number, problem_num, 8)
        self.repo_assignments.grade_assignment(studentID3, lab_number, problem_num, 10)

        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number, problem_num), 8)

        self.repo_assignments.add_assignment(assignment4)
        self.repo_assignments.grade_assignment(studentID4, lab_number, problem_num, 9)
        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_problem(lab_number, problem_num), 8.25)

    def test_calculate_and_get_average_for_student(self):

        lab_number = "10"
        problem_num = "15"
        problem_description = "Some problem, idk1"
        problem_deadline = date(2021, 11, 22)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)

        lab_number2 = "10"
        problem_num2 = "16"
        problem_description2 = "Some problem, idk2"
        problem_deadline2 = date(2021, 11, 22)
        problem2 = Problem(lab_number2, problem_num2, problem_description2, problem_deadline2)

        lab_number3 = "10"
        problem_num3 = "17"
        problem_description3 = "Some problem, idk3"
        problem_deadline3 = date(2021, 11, 22)
        problem3 = Problem(lab_number3, problem_num3, problem_description3, problem_deadline3)

        lab_number4 = "10"
        problem_num4 = "18"
        problem_description4 = "Some problem, idk4"
        problem_deadline4 = date(2021, 11, 22)
        problem4 = Problem(lab_number4, problem_num4, problem_description4, problem_deadline4)

        assignment1 = AssignmentDTO(self.studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(self.studentID, lab_number2, problem_num2)
        assignment3 = AssignmentDTO(self.studentID, lab_number3, problem_num3)
        assignment4 = AssignmentDTO(self.studentID, lab_number4, problem_num4)

        self.repo_students.add_student(self.student)

        self.repo_problems.add_problem(problem)
        self.repo_problems.add_problem(problem2)
        self.repo_problems.add_problem(problem3)
        self.repo_problems.add_problem(problem4)

        self.repo_assignments.add_assignment(assignment1)
        self.repo_assignments.add_assignment(assignment2)
        self.repo_assignments.add_assignment(assignment3)

        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_student(self.studentID), 0)

        self.repo_assignments.grade_assignment(self.studentID, lab_number, problem_num, 6)
        self.repo_assignments.grade_assignment(self.studentID, lab_number2, problem_num2, 8)
        self.repo_assignments.grade_assignment(self.studentID, lab_number3, problem_num3, 10)

        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_student(self.studentID), 8)

        self.repo_assignments.add_assignment(assignment4)
        self.repo_assignments.grade_assignment(self.studentID, lab_number4, problem_num4, 9)

        self.assertAlmostEqual(self.repo_assignments.calculate_and_get_average_for_student(self.studentID), 8.25)

    def test_get_students_below_X_average(self):
        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)

        studentID2 = 1
        student_name2 = "Paul"
        student_group2 = "2223"
        student2 = Student(studentID2, student_name2, student_group2)

        lab_number = "7"
        problem_num = "12"
        problem_description = "Some problem, idk"
        problem_deadline = date(2021, 11, 19)
        problem = Problem(lab_number, problem_num, problem_description, problem_deadline)

        lab_number2 = "8"
        problem_num2 = "13"
        problem_description2 = "Some problem, idk2"
        problem_deadline2 = date(2021, 11, 20)
        problem2 = Problem(lab_number2, problem_num2, problem_description2, problem_deadline2)

        lab_number3 = "9"
        problem_num3 = "14"
        problem_description3 = "Some problem, idk3"
        problem_deadline3 = date(2021, 11, 21)
        problem3 = Problem(lab_number3, problem_num3, problem_description3, problem_deadline3)


        assignment = AssignmentDTO(studentID, lab_number, problem_num)
        assignment2 = AssignmentDTO(studentID2, lab_number2, problem_num2)

        self.repo_students.add_student(student)
        self.repo_students.add_student(student2)

        self.repo_problems.add_problem(problem)
        self.repo_problems.add_problem(problem2)

        self.repo_assignments.add_assignment(assignment)
        self.repo_assignments.add_assignment(assignment2)

        self.srv_assignments.grade_assignment(studentID, lab_number, problem_num, 6.9)
        self.srv_assignments.grade_assignment(studentID2, lab_number2, problem_num2, 8)


        list_of_students = self.srv_statistics.get_students_below_X_average(7)

        self.assertEqual(len(list_of_students), 1)

        self.assertTrue(self.repo_students.get_student_by_id(studentID, 0) in list_of_students)
        self.assertTrue(self.repo_students.get_student_by_id(studentID2, 0) not in list_of_students)

