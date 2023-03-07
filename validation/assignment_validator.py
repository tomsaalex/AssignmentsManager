from Exceptions.ValidationError import ValidationError


class AssignmentValidator:
    def validate_assignment(self, assignment):
        #TODO
        #Can you not validate the students and problems in here? To do that you have to reference their validators here,
        #which would add complexity, and they come from repos anyway, meaning they've already been validated.
        #Also, a new assignment will have no grade to check, and the later check is performed inside the setter, and ALSO ALSO
        #the test function or create_assignment already checks if the grade is none at first, so do we even need validation???
        """
        errors = ""

        grade = assignment.get_grade()
        if (grade < 0 or grade > 10) and (grade is not None):
            errors += "Valoare invalida a notei"

        raise ValidationError(errors)
        """
        pass