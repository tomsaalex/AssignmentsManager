import random

from Exceptions.RepositoryError import RepositoryError
from domain.assignment_dto import AssignmentDTO


class RepoAssignments:
    def __init__(self):
        self._assignments = []

    def __len__(self):
        return len(self._assignments)

    def add_assignment(self, assignment):
        """
        Repo function that adds an assignment to the repo.
        :param assignment: The assignment to add to the repo.
        """
        for _as in self._assignments:
            if _as == assignment:
                raise RepositoryError("Assignment duplicat")

        self._assignments.append(assignment)

    def get_assignment_by_ids(self, studentID, lab_number, problem_num):
        """
        A repo function that returns an assignment based on the identification numbers.
        :param studentID: The id of the student that has the assignment.
        :param lab_number: The number of the lab containing the problem in the assignment.
        :param problem_num: The number of the problem in tha assignment.
        :return: The assignment matching the criteria.
        """
        for _as in self._assignments:
            if (_as.get_studentID() == studentID and
                _as.get_lab_number() == lab_number and
                _as.get_problem_number() == problem_num):
                return _as

        raise RepositoryError("Assignment inexistent")

    def grade_assignment(self, studentID, lab_number, problem_number, grade):
        """
        A repo function that can grade an assignment matching the criteria given.
        :param studentID: The id of the student that has the assignment.
        :param lab_number: The number of the lab containing the problem in the assignment.
        :param problem_num: The number of the problem in tha assignment.
        :param grade: The grade to give this assignment.
        """
        for _as in self._assignments:
            if (_as.get_studentID() == studentID and
                _as.get_lab_number() == lab_number and
                _as.get_problem_number() == problem_number):
                    _as.set_grade(grade)
                    return

        raise RepositoryError("Assignment inexistent")

    def calculate_and_get_average_for_student(self, studentID):
        """
        A service function that calculates the average of the grades a student has on all his labs.
        :param studentID: The ID of the student.
        :return: The average of the lab grades.
        """

        sum_of_grades = 0
        number_of_grades = 0
        for _as in self._assignments:
            if _as.get_studentID() == studentID and _as.get_grade() is not None:
                sum_of_grades += float(_as.get_grade())
                number_of_grades += 1

        if number_of_grades == 0:
            return 0

        return float(sum_of_grades) / number_of_grades

    def calculate_and_get_average_for_problem(self, lab_number, problem_number):
        """
        A service function that calculates the average of the grades a problem has for all its students.
        :param lab_number: The number of the lab containing the problem.
        :param problem_number: The number of the problem.
        :return: The average of the lab grades.
        """

        sum_of_grades = 0
        number_of_grades = 0
        for _as in self._assignments:
            if _as.get_lab_number() == lab_number and _as.get_problem_number() == problem_number and _as.get_grade() is not None:
                sum_of_grades += float(_as.get_grade())
                number_of_grades += 1

        if number_of_grades == 0:
            return 0 #TODO THINK ABOUT THIS CAREFULLY

        return float(sum_of_grades) / number_of_grades


    def calculate_and_get_number_of_students_per_problem(self, lab_number, problem_number):
        """
        A repo function that returns the number of students have the given problem assigned
        :param lab_number: The number of the lab containing the problem.
        :param problem_number: The number of the problem.
        :return: The number of students that have the given problem assigned.
        """
        num_of_apparitions = 0
        for _as in self._assignments:
            if _as.get_lab_number() == lab_number and _as.get_problem_number() == problem_number:
                num_of_apparitions += 1

        return num_of_apparitions

    def get_all(self):
        """
        A repo function that returns everything in the repository.
        """
        return self._assignments[:]

class FileRepoAssignments(RepoAssignments):
    def __init__(self, file_path):
        RepoAssignments.__init__(self)
        self.__file_path = file_path

    def __len__(self):
        self.__read_all_from_file()
        return len(self._assignments)


    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._assignments = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    parts = line.split(',')
                    studentID = int(parts[0])

                    lab_number = parts[1]

                    problem_number = parts[2]
                    grade = parts[3]
                    if grade != "None":
                        grade = float(grade)
                    else:
                        grade = None
                    assignment = AssignmentDTO(studentID, lab_number, problem_number, grade)
                    self._assignments.append(assignment)

    def __append_to_file(self, assignment):
        with open(self.__file_path, "a") as f:
            f.write(f"{assignment.get_studentID()},{assignment.get_lab_number()},{assignment.get_problem_number()},{assignment.get_grade()}\n")

    """
    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._assignments = []
            lines = f.readlines()

            i = 0
            while i < len(lines):
                good_lines = []
                j = i
                while len(good_lines) < 4:
                    while len(lines[j]) == 1:
                        j = j + 1
                        i = i + 1
                    good_lines.append(lines[j].strip())
                    j = j + 1

                studentID = int(good_lines[0])

                lab_number = good_lines[1]

                problem_number = good_lines[2]
                grade = good_lines[3]
                if grade != "None":
                    grade = float(grade)
                else:
                    grade = None
                assignment = AssignmentDTO(studentID, lab_number, problem_number, grade)
                self._assignments.append(assignment)

                i += 4

    def __append_to_file(self, assignment):
        with open(self.__file_path, "a") as f:
            f.write(
                f"{assignment.get_studentID()}\n{assignment.get_lab_number()}\n{assignment.get_problem_number()}\n{assignment.get_grade()}\n")
    """
    def get_all(self):
        self.__read_all_from_file()
        return RepoAssignments.get_all(self)

    def calculate_and_get_average_for_student(self, studentID):
        """
        A service function that calculates the average of the grades a student has on all his labs.
        :param studentID: The ID of the student.
        :return: The average of the lab grades.
        """
        self.__read_all_from_file()
        return RepoAssignments.calculate_and_get_average_for_student(self, studentID)

    def calculate_and_get_number_of_students_per_problem(self, lab_number, problem_number):
        """
        A repo function that returns the number of students have the given problem assigned
        :param lab_number: The number of the lab containing the problem.
        :param problem_number: The number of the problem.
        :return: The number of students that have the given problem assigned.
        """
        self.__read_all_from_file()
        return RepoAssignments.calculate_and_get_number_of_students_per_problem(self, lab_number, problem_number)

    def calculate_and_get_average_for_problem(self, lab_number, problem_number):
        """
        A service function that calculates the average of the grades a problem has for all its students.
        :param lab_number: The number of the lab containing the problem.
        :param problem_number: The number of the problem.
        :return: The average of the lab grades.
        """
        self.__read_all_from_file()
        return RepoAssignments.calculate_and_get_average_for_problem(self, lab_number, problem_number)



    def add_assignment(self, assignment):
        """
        Repo function that adds an assignment to the repo.
        :param assignment: The assignment to add to the repo.
        """
        self.__read_all_from_file()
        RepoAssignments.add_assignment(self, assignment)
        self.__append_to_file(assignment)

    def get_assignment_by_ids(self, studentID, lab_number, problem_num):
        """
        A repo function that returns an assignment based on the identification numbers.
        :param studentID: The id of the student that has the assignment.
        :param lab_number: The number of the lab containing the problem in the assignment.
        :param problem_num: The number of the problem in tha assignment.
        :return: The assignment matching the criteria.
        """
        self.__read_all_from_file()
        return RepoAssignments.get_assignment_by_ids(self, studentID, lab_number, problem_num)

    def grade_assignment(self, studentID, lab_number, problem_number, grade):
        """
        A repo function that can grade an assignment matching the criteria given.
        :param studentID: The id of the student that has the assignment.
        :param lab_number: The number of the lab containing the problem in the assignment.
        :param problem_num: The number of the problem in tha assignment.
        :param grade: The grade to give this assignment.
        """
        self.__read_all_from_file()
        RepoAssignments.grade_assignment(self, studentID, lab_number, problem_number, grade)

        assignment_line_identifier = f"{studentID},{lab_number},{problem_number}"
        new_line = assignment_line_identifier + f",{grade}\n"
        lines = []

        with open(self.__file_path, "r") as f:
            lines = f.readlines()

        for i, _line in enumerate(lines):
            if assignment_line_identifier in _line:
                lines[i] = new_line

        with open(self.__file_path, "w") as f:
            for _line in lines:
                f.write(_line)
