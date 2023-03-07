import unittest

from controller.service_assignment import ServiceAssignment
from controller.service_statistics import ServiceStatistics
from presentation.user_interface import Console
from controller.service_problem import ServiceProblem
from controller.service_student import ServiceStudent
from infratructure.repo_problems import FileRepoProblems, RepoProblems
from infratructure.repo_students import FileRepoStudents, RepoStudents
from infratructure.repo_assignments import FileRepoAssignments, RepoAssignments
from validation.problem_validator import ProblemValidator
from validation.student_validator import StudentValidator
from tests.test_assignments import AssignmentsTests
from tests.test_problems import ProblemsTests
from tests.test_students import TestsStudents
from tests.test_sorting import SortingTests

repo_problems = FileRepoProblems("Problems.txt")
repo_students = FileRepoStudents("Students.txt")
repo_assignments = FileRepoAssignments("Assignments.txt")
#repo_problems = RepoProblems()
#repo_students = RepoStudents()
#repo_assignments = RepoAssignments()

validator_students = StudentValidator()
validator_problems = ProblemValidator()
validator_assignments = RepoAssignments()

srv_problem = ServiceProblem(validator_problems, repo_problems)
srv_student = ServiceStudent(validator_students, repo_students)
srv_assignments = ServiceAssignment(validator_assignments, repo_assignments, repo_students, repo_problems)
srv_statistics = ServiceStatistics(repo_students, repo_problems, repo_assignments)

ui = Console(srv_student, srv_problem, srv_assignments, srv_statistics)
unittest.main(exit=False)
ui.run()
