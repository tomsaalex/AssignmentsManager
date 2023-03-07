import random

from Exceptions.ValidationError import ValidationError


class Assignment:
    def __init__(self, studentID, lab_number, problem_num, grade = None):
        self.__studentID = studentID
        self.__lab_num = lab_number
        self.__problem_num = problem_num
        self.__grade = grade

    def get_studentID(self):
        """
        A getter for the student that has the assignment.
        """
        return self.__studentID

    def get_problem_num(self):
        """
        A getter for the problem_number of the problem.
        """
        return self.__problem_num

    def get_lab_num(self):
        """
        A getter for the lab_number of the problem.
        """
        return self.__lab_num

    def get_grade(self):
        """
        A getter for the grade of the assignment.
        """
        return self.__grade

    def set_grade(self, new_grade):
        """
        A setter for the grade of the assignment.
        :param new_grade: The new grade to assign to the assignment.
        """
        if 0 <= new_grade <= 10:
            self.__grade = new_grade
        else:
            raise ValidationError("Valoare invalida a notei")


    def __eq__(self, other):
        return (self.__studentID == other.__studentID) and (self.__problem_num == other.__problem_num) and (self.__lab_num == other.__lab_num)



    def __str__(self):
        string_assignment = ""
        string_assignment += str(self.__problem) + ' ---> ' + str(self.__student) + '    '
        if self.__grade is None:
            string_assignment += '(Ungraded)'
        else:
            string_assignment += '(' + str(self.__grade) + ')'
        return string_assignment
