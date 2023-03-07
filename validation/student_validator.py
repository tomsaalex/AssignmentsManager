from Exceptions.ValidationError import ValidationError


class StudentValidator:
    def validate_student(self, student):
        """
        A function that validates a given student.
        :param student: The student to validate.
        :return:
        """
        errors = ""
        studentID = student.get_studentID()
        student_name = student.get_name()
        student_group = student.get_group()

        if studentID < 0:
            errors += "studentID invalid\n"
        if len(student_name) == 0:
            errors += "student_name invalid\n"
        if len(student_group) == 0:
            errors += "student_group invalid\n"

        if len(errors) > 0:
            raise ValidationError(errors)
