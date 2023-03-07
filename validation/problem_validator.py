from Exceptions.ValidationError import ValidationError


class ProblemValidator:

    def validate_problem(self, problem):
        """
        A function that validates a problem.
        :param problem: The problem to validate.
        """
        lab_num = problem.get_lab_number()
        problem_num = problem.get_problem_number()
        description = problem.get_description()

        errors = ""

        if len(lab_num) == 0:
            errors += "Numar lab invalid\n"
        if len(problem_num) == 0:
            errors += "Numar problema invalid\n"
        if len(description) == 0:
            errors += "Descriere invalida\n"

        if len(errors) > 0:
            raise ValidationError(errors)
