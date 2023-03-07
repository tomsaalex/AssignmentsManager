class Problem:
    def __init__(self, lab_number, problem_number, description, deadline, average = None, num_of_students = None):
        self.__lab_number = lab_number
        self.__problem_number = problem_number
        self.__description = description
        self.__deadline = deadline
        self.__average = average
        self.__num_of_students = num_of_students

    def get_lab_number(self):
        """
        A getter for the lab_number
        :return:
        """
        return self.__lab_number

    def set_lab_number(self, lab_number):
        """
        A setter for the lab_number
        :return:
        """
        self.__lab_number = lab_number

    def get_problem_number(self):
        """
        A getter for the problem_number
        :return:
        """
        return self.__problem_number

    def set_problem_number(self, problem_number):
        """
        A setter for the problem_number
        :return:
        """
        self.__problem_number = problem_number

    def get_description(self):
        """
        A getter for the description
        :return:
        """
        return self.__description

    def set_description(self, description):
        """
        A setter for the description
        :return:
        """
        self.__description = description

    def get_deadline(self):
        """
        A getter for the deadline
        :return:
        """
        return self.__deadline

    def set_deadline(self, deadline):
        """
        A setter for the deadline
        :return:
        """
        self.__deadline = deadline

    def get_lab_average(self):
        """
        A getter for the lab grades average.
        """
        return self.__average

    def set_lab_average(self, new_average):
        """
        A setter for the lab grades average.
        """
        self.__average = new_average


    def get_num_of_students(self):
        """
        Getter for the number of students a problem is assigned to.
        """
        return self.__num_of_students

    def set_num_of_students(self, new_num):
        """
        Setter for the number of students a problem is assigned to.
        """
        self.__num_of_students = new_num

    def __eq__(self, other):
        return (self.__lab_number == other.__lab_number) and (self.__problem_number == other.__problem_number)

    def __str__(self):
        return '[' + self.__lab_number + '_' + self.__problem_number + ']' + self.__description + '[' + self.__deadline.strftime("%d-%m-%Y") + ']'
