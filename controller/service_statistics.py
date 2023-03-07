from Exceptions.StatisticalError import StatisticalError
from Sorting.sorting_methods import SortingMethods

class ServiceStatistics:
    def __init__(self, repo_students, repo_problems, repo_assignments):
        self.__repo_students = repo_students
        self.__repo_problems = repo_problems
        self.__repo_assignments = repo_assignments

    def Compare_Name_Grade(self, a, b, reversed):
        if reversed == False:
            if(a.get_grade() < b.get_grade()):
                return True
            if a.get_grade() == b.get_grade() and (self.__repo_students.get_student_by_id(a.get_studentID()).get_name() < self.__repo_students.get_student_by_id(b.get_studentID()).get_name()):
                return True
            return False
        if reversed == True:
            if (a.get_grade() > b.get_grade()):
                return True
            if a.get_grade() == b.get_grade() and (self.__repo_students.get_student_by_id(
                    a.get_studentID()).get_name() > self.__repo_students.get_student_by_id(
                    b.get_studentID()).get_name()):
                return True
            return False

    def get_assignments_for_problem(self, lab_number, problem_number):
        full_list_of_assignments = self.__repo_assignments.get_all()
        new_list_of_assignments = []

        lambda_function = None

        """
        if type_of_sort == 'a':
            lambda_function = lambda a: self.__repo_students.get_student_by_id(a.get_studentID()).get_name()
        elif type_of_sort == 'n':
            lambda_function = lambda a: a.get_grade()
        """
        for x in full_list_of_assignments:
            if x.get_lab_number() == lab_number and x.get_problem_number() == problem_number and x.get_grade() is not None:
                new_list_of_assignments.append(x)

        if len(new_list_of_assignments) == 0:
            raise StatisticalError("Nu exista studenti care sa fi rezolvat problema ceruta.")

        for i, x in enumerate(new_list_of_assignments):
            new_list_of_assignments[i].set_student(self.__repo_students.get_student_by_id(x.get_studentID()))
            new_list_of_assignments[i].set_problem(self.__repo_problems.get_problem_by_num(x.get_lab_number(), x.get_problem_number()))


        #new_list_of_assignments.sort(key=lambda_function)
        new_list_of_assignments = SortingMethods.InsertionSort(new_list_of_assignments, cmp=self.Compare_Name_Grade, reversed=True)
        return new_list_of_assignments

    def get_students_below_X_average(self, grade_to_compare_against):

        for i, x in enumerate(self.__repo_students.get_all()):
            new_average = self.__repo_assignments.calculate_and_get_average_for_student(x.get_studentID())
            self.__repo_students.update_student_average(x.get_studentID(), new_average)

        list_of_students = self.__repo_students.get_all()

        students_below_X_average = []


        for x in list_of_students:
            if x.get_lab_average() < grade_to_compare_against:
                students_below_X_average.append(x)

        return students_below_X_average

    def get_top_50per_most_assigned_problem(self):
        list_of_problems = self.__repo_problems.get_all()
        curated_list_of_problems = []

        for i, _pb in enumerate(list_of_problems):
            lab_num = _pb.get_lab_number()
            problem_num = _pb.get_problem_number()
            if self.__repo_assignments.calculate_and_get_average_for_problem(lab_num, problem_num) > 5:
                list_of_problems[i].set_num_of_students(self.__repo_assignments.calculate_and_get_number_of_students_per_problem(lab_num, problem_num))
                list_of_problems[i].set_lab_average(self.__repo_assignments.calculate_and_get_average_for_problem(lab_num, problem_num))

                curated_list_of_problems.append(_pb)



        #curated_list_of_problems.sort(reverse=True, key=lambda x: x.get_num_of_students())
        #TODO Here is the insertion sort.
        SortingMethods.InsertionSort(curated_list_of_problems, reversed=True, key=lambda x: x.get_num_of_students())
        max_num_students = 0

        if len(curated_list_of_problems) > 0:
            max_num_students = curated_list_of_problems[0].get_num_of_students()

        curated_list_of_problems2 = []

        for _pb in curated_list_of_problems:
            if _pb.get_num_of_students() == max_num_students:
                curated_list_of_problems2.append(_pb)


        middle_index = int(len(curated_list_of_problems2) / 2)
        top50 = curated_list_of_problems2[:middle_index]


        #top50.sort(key=lambda x: str(x.get_lab_number()) + '_' + str(x.get_problem_number))
        #TODO Here is the CombSort.
        SortingMethods.CombSort(top50, key=lambda x: str(x.get_lab_number()) + '_' + str(x.get_problem_number))

        return top50
