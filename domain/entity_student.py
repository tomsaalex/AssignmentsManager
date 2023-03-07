class Student:
    def __init__(self, studentID, name, group, lab_average = 0):
        self.__studentID = studentID
        self.__name = name
        self.__group = group
        self.__lab_average = lab_average

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_studentID(self):
        return self.__studentID

    def get_group(self):
        return self.__group

    def set_group(self, group):
        self.__group = group

    def get_lab_average(self):
        return self.__lab_average

    def set_lab_average(self, average):
        self.__lab_average = average

    def __eq__(self, other):
        return self.__studentID == other.__studentID

    def __str__(self):
        return "[" + str(self.__studentID) + "]" + self.__name + "[" + self.__group + "]"
