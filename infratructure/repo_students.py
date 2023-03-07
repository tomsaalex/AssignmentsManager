import random

from Exceptions.EmptyRepositoryError import EmptyRepositoryError
from Exceptions.RepositoryError import RepositoryError
from domain.entity_student import Student


class RepoStudents:
    def __init__(self):
        self._students = []

    def __len__(self):
        """
        Returns the number of elements in the repo.
        :return: The number of elements in the repo.
        """
        return len(self._students)

    def update_student_average(self, studentID, new_average):
        """
        Repo function that can update the average of all the grades a student got on their lab.
        :param studentID: The ID of the student to update.
        :param new_average: The new average of the student.
        """
        for i, _st in enumerate(self._students):
            if _st.get_studentID() == studentID:
                self._students[i].set_lab_average(new_average)
                return

        raise RepositoryError("Id invalid")

    def add_student(self, student):
        """
        A repo function that adds a student to the repo.
        :param student: The student to add.
        """
        for _st in self._students:
            if _st == student:
                raise RepositoryError("Id deja existent")
        self._students.append(student)

    """
    def remove_student_by_id(self, id):
        
        A repo function that removes a student from the repo.
        :param id: The id of the student to remove.
        
        for i, _st in enumerate(self._students):
            if _st.get_studentID() == id:
                del self._students[i]
                return

        raise RepositoryError("Id invalid")
    """

    # TODO This is recursive function #2
    def remove_student_by_id(self, id, current_index=0):
        """
        A repo function that removes a student from the repo. But this time, IT'S RECURSIVE.
        :param id: The id of the student to remove.
        """
        if current_index >= len(self._students):
            raise RepositoryError("Id invalid")

        if self._students[current_index].get_studentID() == id:
            for i in range(len(self._students)):
                print(self._students[i])
            del self._students[current_index]
            for i in range(len(self._students)):
                print(self._students[i])
            return

        RepoStudents.remove_student_by_id(self, id, current_index + 1)

    """
    def get_student_by_id(self, studentID):
        
        A function that searches for a student based on its id.
        :param studentID: The student that corresponds to that id.
        :return: The required student, should it exist.
        
        for _st in self._students:
            if _st.get_studentID() == studentID:
                return _st

        raise RepositoryError("Id inexistent")
    """

    # TODO This is recursive function #1
    def get_student_by_id(self, studentID, current_index=0):
        """
        A function that searches for a student based on its id, BUT THIS TIME IT'S RECURSIVE!
        :param studentID: The student that corresponds to that id.
        :param current_index: The index used for recursion. It needs not be assigned by the user.
        :return: The required student, should it exist.
        """
        if current_index >= len(self._students):
            raise RepositoryError("Id inexistent")

        if self._students[current_index].get_studentID() == studentID:
            return self._students[current_index]

        return RepoStudents.get_student_by_id(self, studentID, current_index+1)

    def get_all(self):
        """
        A repo function that returns everything there is in the repo.
        :return: The elements in the repo, as a list.
        """
        return self._students[:]

    def get_random_student(self):
        if len(self._students) == 0:
            raise EmptyRepositoryError("Nu exista studenti din care sa fie ales unul")

        return random.choice(self._students)

    def filter_by_name_prefix(self, prefix):
        """
        A repo function that returns a list of all the students whose names begin with the given prefix.
        :param prefix: A prefix that the required students must have in their name
        :return: A list of all the students whose names begin with the given prefix
        """
        list_of_students = []
        for _st in self._students:
            if _st.get_name().startswith(prefix):
                list_of_students.append(_st)
        return list_of_students

    def generate_unique_id(self):
        while True:
            id = random.randint(0, 10000000)

            try:
                student = self.get_student_by_id(id)
            except RepositoryError as re:
                assert (str(re) == "Id inexistent")
                break

        return id


class FileRepoStudents(RepoStudents):
    def __init__(self, file_path):
        RepoStudents.__init__(self)
        self.__file_path = file_path

    def __len__(self):
        self.__read_all_from_file()
        return RepoStudents.__len__(self)

    def get_all(self):
        self.__read_all_from_file()
        return RepoStudents.get_all(self)

    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._students = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    parts = line.split(',')
                    studentID = int(parts[0])
                    student_name = parts[1]
                    student_group = parts[2]
                    student_lab_average = float(parts[3])
                    student = Student(studentID, student_name, student_group, student_lab_average)
                    self._students.append(student)

    def __append_to_file(self, student):
        with open(self.__file_path, "a") as f:
            f.write(
                f"{student.get_studentID()},{student.get_name()},{student.get_group()},{student.get_lab_average()}\n")

    def __rewrite_file(self):
        with open(self.__file_path, "w") as f:
            for _st in self._students:
                f.write(f"{_st.get_studentID()},{_st.get_name()},{_st.get_group()},{_st.get_lab_average()}\n")

    """
    def __read_all_from_file(self):
        with open(self.__file_path, "r") as f:
            self._students = []
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
                student_name = good_lines[1]
                student_group = good_lines[2]
                student_lab_average = float(good_lines[3])
                student = Student(studentID, student_name, student_group, student_lab_average)
                self._students.append(student)

                i += 4
    def __append_to_file(self, student):
        with open(self.__file_path, "a") as f:
            f.write(
                f"{student.get_studentID()}\n{student.get_name()}\n{student.get_group()}\n{student.get_lab_average()}\n")
                
        def __rewrite_file(self):
        with open(self.__file_path, "w") as f:
            for _st in self._students:
                f.write(f"{_st.get_studentID()}\n{_st.get_name()}\n{_st.get_group()}\n{_st.get_lab_average()}\n")
    """

    def update_student_average(self, studentID, new_average):
        """
        Repo function that can update the average of all the grades a student got on their lab.
        :param studentID: The ID of the student to update.
        :param new_average: The new average of the student.
        """
        self.__read_all_from_file()
        RepoStudents.update_student_average(self, studentID, new_average)
        self.__rewrite_file()

    def add_student(self, student):
        """
        A repo function that adds a student to the repo.
        :param student: The student to add.
        """
        self.__read_all_from_file()
        RepoStudents.add_student(self, student)
        self.__append_to_file(student)

    def remove_student_by_id(self, id, current_index=0):
        """
        A repo function that removes a student from the repo.
        :param id: The id of the student to remove.
        """
        self.__read_all_from_file()
        RepoStudents.remove_student_by_id(self, id)
        self.__rewrite_file()

    def get_student_by_id(self, studentID, current_index=0):
        """
        A function that searches for a student based on its id.
        :param studentID: The student that corresponds to that id.
        :return: The required student, should it exist.
        """
        self.__read_all_from_file()
        return RepoStudents.get_student_by_id(self, studentID, 0)

    def get_random_student(self):
        self.__read_all_from_file()
        return RepoStudents.get_random_student(self)

    def filter_by_name_prefix(self, prefix):
        """
        A repo function that returns a list of all the students whose names begin with the given prefix.
        :param prefix: A prefix that the required students must have in their name
        :return: A list of all the students whose names begin with the given prefix
        """
        self.__read_all_from_file()
        return RepoStudents.filter_by_name_prefix(self, prefix)

    def generate_unique_id(self):
        self.__read_all_from_file()
        return RepoStudents.generate_unique_id(self)
