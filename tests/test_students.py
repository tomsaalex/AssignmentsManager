import unittest

from Exceptions.RepositoryError import RepositoryError
from Exceptions.ValidationError import ValidationError
from controller.service_student import ServiceStudent
from domain.entity_student import Student
from infratructure.repo_students import RepoStudents, FileRepoStudents
from validation.student_validator import StudentValidator


class TestsStudents(unittest.TestCase):

    def setUp(self):
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


        self.repo_students = RepoStudents()

        self.file_repo_students = FileRepoStudents("tests/TestStudents.txt")

        self.student_validator = StudentValidator()

        self.srv_students = ServiceStudent(self.student_validator, self.repo_students)

    def test_create_student(self):
        """
        Test function for create_student.
        """

        self.assertEqual(self.student.get_studentID(), self.studentID)
        self.assertEqual(self.student.get_name(), self.student_name)
        self.assertEqual(self.student.get_group(), self.student_group)

        other_name = "Paul"
        other_group = "218"
        other_student_same_id = Student(self.studentID, other_name, other_group)

        self.assertEqual(self.student, other_student_same_id)
        self.assertTrue(self.student.__eq__(other_student_same_id))

        self.assertEqual(str(self.student), "[0]Alex[2222]")
        self.assertEqual(self.student.__str__(), "[0]Alex[2222]")

    def test_validate_student(self):
        """
        Test function for validate_student.
        """

        self.student_validator.validate_student(self.student)

        inv_studentID = -42
        inv_student_name = ""
        inv_student_group = ""
        inv_student = Student(inv_studentID, inv_student_name, inv_student_group)

        self.assertRaises(ValidationError, self.student_validator.validate_student, inv_student)

    def test_add_student_to_repo(self):
        """
        Test function for add_student_to_repo.
        """
        self.assertEqual(len(self.repo_students), 0)
        self.assertEqual(self.repo_students.__len__(), 0)

        self.repo_students.add_student(self.student)

        self.assertEqual(len(self.repo_students), 1)
        self.assertEqual(self.repo_students.__len__(), 1)

        found_student = self.repo_students.get_student_by_id(self.studentID)
        self.assertEqual(found_student, self.student)
        self.assertEqual(found_student.get_name(), self.student.get_name())
        self.assertEqual(found_student.get_group(), self.student.get_group())

        inexist_id = 10

        self.assertRaises(RepositoryError, self.repo_students.get_student_by_id, inexist_id, 0)


        other_name = "Paul"
        other_group = "300"
        other_student_same_id = Student(self.studentID, other_name, other_group)

        self.assertRaises(RepositoryError, self.repo_students.add_student, other_student_same_id)

    def test_add_student_service(self):
        """
        Test function for add_student_service.
        """

        self.assertEqual(self.srv_students.no_of_students(), 0)
        self.srv_students.add_student(self.studentID, self.student_name, self.student_group)
        self.assertEqual(self.srv_students.no_of_students(), 1)

        self.assertRaises(RepositoryError, self.srv_students.add_student, self.studentID, self.student_name, self.student_group)

        inv_studentID = -42
        inv_student_name = ""
        inv_student_group = ""
        inv_student = Student(inv_studentID, inv_student_name, inv_student_group)

        self.assertRaises(ValidationError, self.srv_students.add_student, inv_studentID, inv_student_name, inv_student_group)

    def test_remove_student_by_id(self):
        """
        Test function for remove_student_by_id.
        """

        self.assertEqual(len(self.repo_students), 0)
        self.repo_students.add_student(self.student)
        self.assertEqual(len(self.repo_students), 1)

        self.repo_students.remove_student_by_id(0)
        self.assertEqual(len(self.repo_students), 0)

        self.assertRaises(RepositoryError, self.repo_students.remove_student_by_id, 24)

    def test_remove_student_by_id_service(self):
        """
        Test function for remove_student_by_id_service.
        """

        self.assertEqual(self.srv_students.no_of_students(), 0)

        self.srv_students.add_student(self.studentID, self.student_name, self.student_group)
        self.assertEqual(self.srv_students.no_of_students(), 1)

        self.srv_students.add_student(self.studentID2, self.student_name2, self.student_group2)
        self.assertEqual(self.srv_students.no_of_students(), 2)

        self.srv_students.remove_student(self.studentID2)
        self.assertEqual(self.srv_students.no_of_students(), 1)

        self.srv_students.remove_student(self.studentID)
        self.assertEqual(self.srv_students.no_of_students(), 0)

        self.assertRaises(RepositoryError, self.srv_students.remove_student, 40)

    def test_get_student_by_id_service(self):
        """
        Test function that checks the get_student_by_id service function.
        :return:
        """

        self.assertEqual(self.srv_students.no_of_students(), 0)
        self.srv_students.add_student(self.studentID, self.student_name, self.student_group)
        self.assertEqual(self.srv_students.no_of_students(), 1)
        self.srv_students.add_student(self.studentID2, self.student_name2, self.student_group2)
        self.assertEqual(self.srv_students.no_of_students(), 2)

        found_student = self.srv_students.get_student_by_id(self.studentID2)
        self.assertEqual(found_student.get_name(), self.student_name2)
        self.assertEqual(found_student.get_group(), self.student_group2)
        self.assertEqual(found_student.get_studentID(), self.studentID2)

        inexist_id = 10

        self.assertRaises(RepositoryError, self.srv_students.get_student_by_id, inexist_id)

    def test_students_get_all(self):
        """
        Test function that tests the get_all repo function for students.
        """
        self.repo_students.add_student(self.student)
        self.repo_students.add_student(self.student2)
        self.repo_students.add_student(self.student3)

        got_list = self.repo_students.get_all()
        self.assertEqual(got_list[0], self.student)
        self.assertEqual(got_list[1], self.student2)
        self.assertEqual(got_list[2], self.student3)

    def test_students_get_all_service(self):
        """
        Test function that tests the get_all service function for students.
        :return:
        """
        self.repo_students.add_student(self.student)
        self.repo_students.add_student(self.student2)
        self.repo_students.add_student(self.student3)

        got_list = self.srv_students.get_all_students()

        self.assertEqual(got_list[0], self.student)
        self.assertEqual(got_list[1], self.student2)
        self.assertEqual(got_list[2], self.student3)

    def test_update_student_average(self):
        self.repo_students.add_student(self.student)

        self.assertAlmostEqual(self.repo_students.get_student_by_id(0).get_lab_average(), 0)
        self.repo_students.update_student_average(0, 6)
        self.assertAlmostEqual(self.repo_students.get_student_by_id(0).get_lab_average(), 6)

    def test_students_filter_by_name_prefix(self):

        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        student = Student(studentID, student_name, student_group)
        self.repo_students.add_student(student)

        studentID2 = 1
        student_name2 = "Allan"
        student_group2 = "22223"
        student2 = Student(studentID2, student_name2, student_group2)
        self.repo_students.add_student(student2)

        studentID3 = 3
        student_name3 = "Aiden"
        student_group3 = "2224"
        student3 = Student(studentID3, student_name3, student_group3)
        self.repo_students.add_student(student3)

        studentID4 = 4
        student_name4 = "Michael"
        student_group4 = "220"
        student4 = Student(studentID4, student_name4, student_group4)
        self.repo_students.add_student(student4)

        students_list = self.repo_students.filter_by_name_prefix("Al")
        self.assertTrue(student in students_list)
        self.assertTrue(student2 in students_list)
        self.assertTrue(student3 not in students_list)
        self.assertTrue(student4 not in students_list)


    def test_students_filter_by_name_prefix_service(self):

        studentID = 0
        student_name = "Alex"
        student_group = "2222"
        self.srv_students.add_student(studentID, student_name, student_group)
        student = Student(studentID, student_name, student_group)

        studentID2 = 1
        student_name2 = "Allan"
        student_group2 = "22223"
        self.srv_students.add_student(studentID2, student_name2, student_group2)
        student2 = Student(studentID2, student_name2, student_group2)

        studentID3 = 3
        student_name3 = "Aiden"
        student_group3 = "2224"
        self.srv_students.add_student(studentID3, student_name3, student_group3)
        student3 = Student(studentID3, student_name3, student_group3)

        studentID4 = 4
        student_name4 = "Michael"
        student_group4 = "220"
        student4 = Student(studentID4, student_name4, student_group4)
        self.srv_students.add_student(studentID4, student_name4, student_group4)

        students_list = self.srv_students.filter_students_by_name_prefix("Al")
        self.assertTrue(student in students_list)
        self.assertTrue(student2 in students_list)

        self.assertTrue(student3 not in students_list)
        self.assertTrue(student4 not in students_list)
