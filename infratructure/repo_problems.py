import random
import string
from datetime import datetime

from Exceptions.EmptyRepositoryError import EmptyRepositoryError
from Exceptions.RepositoryError import RepositoryError
from domain.entity_problem import Problem


class RepoProblems:

    def __init__(self):
        self._problems = []

    def __len__(self):
        """
        Returns the number of elements in the repo.
        :return: The number of elements in the repo.
        """
        return len(self._problems)

    def add_problem(self, problem):
        """
        A repo function that adds a problem to the repo.
        :param problem: The problem to add.
        """
        for _pb in self._problems:
            if _pb == problem:
                raise RepositoryError("Numarul problemei e deja existent")
        self._problems.append(problem)

    def remove_problem_by_num(self, lab_number, problem_number):
        """
        A repo function that removes a problem from the repo.
        :param lab_number: The lab_number of the problem to remove.
        :param problem_number: The problem_number of the problem to remove.
        """
        for i, _pb in enumerate(self._problems):
            if (_pb.get_lab_number() == lab_number) and (_pb.get_problem_number() == problem_number):
                del self._problems[i]
                return

        raise RepositoryError("Num invalid")

    def get_problem_by_num(self, lab_number, problem_number):
        """
        A function that searches for a problem based on its num.
        :param lab_number: The lab_number of the problem to search for.
        :param problem_number: The problem_number of the problem to search for.
        :return: The requested problem.
        """
        for _pb in self._problems:
            if _pb.get_lab_number() == lab_number and _pb.get_problem_number() == problem_number:
                return _pb

        raise RepositoryError("Numarul problemei este inexistent")

    def get_all(self):
        """
        A repo function that returns everything there is in the repo.
        :return: The elements in the repo, as a list.
        """
        return self._problems[:]

    def get_random_problem(self):
        if len(self._problems) == 0:
            raise EmptyRepositoryError("Nu exista probleme din care sa fie aleasa una")

        return random.choice(self._problems)

    def generate_unique_problem_number(self, lab_num):
        length = random.randint(3, 7)

        while True:
            problem_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            try:
                self.get_problem_by_num(lab_num, problem_num)
            except RepositoryError as re:
                assert (str(re) == "Numarul problemei este inexistent")
                break

        return problem_num


class FileRepoProblems(RepoProblems):
    def __init__(self, file_path):
        RepoProblems.__init__(self)
        self.__file_path = file_path

    def __len__(self):
        self.__read_all_from_file()
        return RepoProblems.__len__(self)

    def get_all(self):
        self.__read_all_from_file()
        return RepoProblems.get_all(self)

    """
    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._problems = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    parts = line.split(',')
                    lab_number = parts[0]
                    problem_number = parts[1]
                    problem_description = parts[2]
                    date_format = "%d-%m-%Y"
                    problem_deadline_string = parts[3]
                    problem_deadline = datetime.strptime(problem_deadline_string, date_format)
                    problem_average = parts[4]
                    problem_num_of_students = parts[5]

                    problem = Problem(lab_number, problem_number, problem_description, problem_deadline, problem_average, problem_num_of_students)
                    self._problems.append(problem)
    
    def __append_to_file(self, problem):
        with open(self.__file_path, "a") as f:
            f.write(f'{problem.get_lab_number()},{problem.get_problem_number()},{problem.get_description()},{problem.get_deadline():%d-%m-%Y},{problem.get_lab_average()},{problem.get_num_of_students()}\n')

    """


    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._problems = []
            lines = f.readlines()

            i = 0
            while i < len(lines):
                good_lines = []
                j = i
                while len(good_lines) < 6:
                    while len(lines[j]) == 1:
                        j = j + 1
                        i = i + 1
                    good_lines.append(lines[j].strip())
                    j = j + 1

                lab_number = good_lines[0]
                problem_number = good_lines[1]
                problem_description = good_lines[2]

                date_format = "%d-%m-%Y"
                problem_deadline_string = good_lines[3]

                problem_deadline = datetime.strptime(problem_deadline_string, date_format)
                problem_average = good_lines[4]
                problem_num_of_students = good_lines[5]

                problem = Problem(lab_number, problem_number, problem_description, problem_deadline, problem_average, problem_num_of_students)
                self._problems.append(problem)
                i += 6



    def __append_to_file(self, problem):
        with open(self.__file_path, "a") as f:
            f.write(f'{problem.get_lab_number()}\n{problem.get_problem_number()}\n{problem.get_description()}\n{problem.get_deadline():%d-%m-%Y}\n{problem.get_lab_average()}\n{problem.get_num_of_students()}\n')

    def add_problem(self, problem):
        """
        A repo function that adds a problem to the repo.
        :param problem: The problem to add.
        """
        self.__read_all_from_file()
        RepoProblems.add_problem(self, problem)
        self.__append_to_file(problem)

    def remove_problem_by_num(self, lab_number, problem_number):
        """
        A repo function that removes a problem from the repo.
        :param lab_number: The lab_number of the problem to remove.
        :param problem_number: The problem_number of the problem to remove.
        """
        self.__read_all_from_file()
        RepoProblems.remove_problem_by_num(self, lab_number, problem_number)

    def get_problem_by_num(self, lab_number, problem_number):
        """
        A function that searches for a problem based on its num.
        :param lab_number: The lab_number of the problem to search for.
        :param problem_number: The problem_number of the problem to remove.
        :return:
        """
        self.__read_all_from_file()
        return RepoProblems.get_problem_by_num(self, lab_number, problem_number)

    def get_random_problem(self):
        self.__read_all_from_file()
        return RepoProblems.get_random_problem(self)

    def generate_unique_problem_number(self, lab_num):
        self.__read_all_from_file()
        return RepoProblems.generate_unique_problem_number(self, lab_num)
