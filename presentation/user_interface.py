from datetime import datetime

from Exceptions.RandomnessExceededError import RandomnessExceededError
from Exceptions.RepositoryError import RepositoryError
from Exceptions.StatisticalError import StatisticalError
from Exceptions.ValidationError import ValidationError
from colorama import Fore
from colorama import init

init(autoreset=True)


class Console:
    def __init__(self, srv_student, srv_problem, srv_assignments, srv_statistics):
        self.__srv_student = srv_student
        self.__srv_problem = srv_problem
        self.__srv_assignment = srv_assignments
        self.__srv_statistics = srv_statistics

    def ui_print_all_students(self):
        """
        A UI function that prints all of the students.
        """
        no_of_students = self.__srv_student.no_of_students()
        if no_of_students == 0:
            print(Fore.YELLOW + "Nu exista studenti in lista")
            return
        else:
            print(Fore.CYAN + "Toti studentii din lista sunt: ")
            for _st in self.__srv_student.get_all_students():
                print(Fore.CYAN + str(_st))

    def ui_print_all_problems(self):
        """
        A UI function that prints all of the problems.
        """
        no_of_problems = self.__srv_problem.no_of_problems()
        if no_of_problems == 0:
            print(Fore.YELLOW + "Nu exista probleme in lista")
            return
        else:
            print(Fore.CYAN + "Toate problemele din lista sunt: ")
            #TODO
            #The function below doesn't exist. Make it and test it.
            for _pb in self.__srv_problem.get_all_problems():
                print(Fore.CYAN + str(_pb))

    def ui_print_all_assignments(self):
        """
        A UI function that prints all of the assignments.
        """
        no_of_assignments = self.__srv_assignment.no_of_assignments()
        if no_of_assignments == 0:
            print(Fore.YELLOW + "Nu exista assignment-uri in lista")
            return
        else:
            print(Fore.CYAN + "Toate assignment-urile din lista sunt: ")
            # TODO
            # The function below doesn't exist. Make it and test it.
            for _as in self.__srv_assignment.get_all_assignments():
                print(Fore.CYAN + str(_as))

    def ui_find_student_by_id(self):
        print("Se incepe cautarea unui student.")

        try:
            studentID = int(input("Introduceti ID-ul studentului pe care vreti sa il gasiti: "))
        except ValueError:
            print(Fore.RED + "Valoare invalida pentru ID")
            return


        try:
            student = self.__srv_student.get_student_by_id(studentID)
            print(Fore.CYAN + "Studentul cerut este: " + str(student))
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
            return

    def ui_add_student(self):
        """
        A UI function that manages the addition of new students.
        """
        print("Se incepe adaugarea in lista a unui student.")

        try:
            studentID = int(input("Introdu id-ul studentului: "))
        except ValueError:
            print(Fore.RED + "ID invalid")
            return

        student_name = input("Introdu numele studentului: ")

        student_group = input("Introdu grupa studentului: ")

        try:
            self.__srv_student.add_student(studentID, student_name, student_group)
            print(Fore.CYAN + "Studentul a fost adaugat cu succes.")
        except ValidationError as ve:
            print(Fore.RED + "ValidationError: \n" + str(ve))
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
        except Exception as ex:
            print(Fore.RED + str(ex))

    def ui_rem_student(self):
        """
        A UI function that manages the removal of students.
        """
        print("Se incepe stergerea din lista a unui student.")
        try:
            studentID = int(input("Introdu id-ul studentului ce trebuie sters: "))
        except ValueError:
            print(Fore.RED + "ID invalid")
            return

        try:
            self.__srv_student.remove_student(studentID)
            print(Fore.CYAN + "Student sters cu succes.")
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
        except Exception as ex:
            print(Fore.RED + str(ex))

    def ui_statistics_for_one_problem(self):
        print("Se incepe generarea statisticilor pentru o problema la alegere.")

        lab_number = input("Introduceti numarul laboratorului in care se afla problema: ")
        problem_number = input("Introduceti numarul problemei: ")

        try:
            list_to_print = self.__srv_statistics.get_assignments_for_problem(lab_number, problem_number)

            for x in list_to_print:
                print(Fore.CYAN + str(x))
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
        except StatisticalError as se:
            print(Fore.RED + "StaticalError: \n" + str(se))
        #except Exception as ex:
        #    print(Fore.RED + str(ex))

    def ui_statistics_average_below_5(self):
        print("Se incepe generarea statisticilor pentru studenti si mediile lor.")
        try:
            list_of_students = self.__srv_statistics.get_students_below_X_average(5)
        except Exception as ex:
            print(str(ex))
            return

        if len(list_of_students) == 0:
            print(Fore.RED + "Nu exista studenti cu media notelor de laborator sub 5.")
        else:
            for _st in list_of_students:
                print(Fore.CYAN + _st.get_name() + " " + str(_st.get_lab_average()))

    def ui_filter_student_name_prefix(self):
        """
        UI function that allows the user to filter their list of students with a prefix for their names.
        """

        print("Se incepe filtrarea listei de studenti")
        try:
            prefix = input("Introduceti prefixul cu care doriti ca numele studentilor din lista sa inceapa: ")
            assert(len(prefix) != 0) #TODO Is this line of code good?
        except Exception as ex:
            print(Fore.RED + "Prefixul nu are voie sa aiba lungimea 0.")
            return

        list_of_students = self.__srv_student.filter_students_by_name_prefix(prefix)

        no_of_students = len(list_of_students)
        if no_of_students == 0:
            print(Fore.YELLOW + "Nu exista studenti in lista ai caror nume sa inceapa cu " + prefix + ".")
            return
        else:
            print(Fore.CYAN + "Toti studentii din lista ai caror nume incepe cu " + prefix + " sunt: ")
            for _st in list_of_students:
                print(Fore.CYAN + str(_st))

    def ui_find_problem_by_num(self):
        """
        UI function that allows the user to get a problem based on its identification number.
        """

        print("Se incepe cautarea unei probleme.")

        lab_number = input("Introduceti numarul laboratorului din care face parte problema: ")
        problem_number = input("Introduceti numarul problemei: ")

        try:
            problem = self.__srv_problem.get_problem_by_num(lab_number, problem_number)
            print(Fore.CYAN + "Problema ceruta este: " + str(problem))
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
            return

    def ui_add_problem(self):
        """
        A UI function that manages the addition of new problems.
        :return:
        """
        print("Se incepe adaugarea in lista a unei probleme")
        lab_num = input("Introduceti numarul laboratorului de care apartine problema: ")
        problem_num = input("Introduceti numarul problemei: ")
        problem_description = input("Introduceti descrierea problemei: ")

        deadline_string = input("Introduceti deadline-ul problemei (zz-ll-aaaa): ")
        # TODO
        # In situatia in care avem toate datele invalide, doar problema deadline-ului va fi semnalata.
        # Doar deadline-ul este validat in ui

        try:
            date_format = "%d-%m-%Y"
            problem_deadline = datetime.strptime(deadline_string, date_format)
        except ValueError:
            print(Fore.RED + "Valori numerice incorecte pentru deadline.")
            return
        except Exception as ex:
            print(Fore.RED + str(ex))
            return

        try:
            self.__srv_problem.add_problem(lab_num, problem_num, problem_description, problem_deadline)
            print(Fore.CYAN + "Problema adaugata cu succes")
        except ValidationError as ve:
            print(Fore.RED + "Validation Error: \n" + str(ve))
        except RepositoryError as re:
            print(Fore.RED + "Repository Error: \n" + str(re))

    def ui_rem_problem(self):
        """
        A UI function that manages the removal of problems.
        :return:
        """
        print("Se incepe stergerea din lista a unei probleme.")
        lab_num = input("Introduceti numarul laboratorului de care apartine problema: ")
        problem_num = input("Introduceti numarul problemei: ")

        try:
            self.__srv_problem.remove_problem(lab_num, problem_num)
            print(Fore.CYAN + "Problema stearss cu succes.")
        except ValidationError as ve:
            print(Fore.RED + "ValidationError: \n" + str(ve))
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))

    def ui_add_assignment(self):
        """
        UI function that lets the user add an assignment to the list.
        """
        print("Se incepe adaugarea in lista a unui assignment.")
        try:
            studentID = int(input("Introdu id-ul studentului: "))
        except ValueError:
            print(Fore.RED + "ID invalid")
            return

        lab_num = input("Introduceti numarul laboratorului de care apartine problema: ")
        problem_num = input("Introduceti numarul problemei: ")

        try:
            self.__srv_assignment.add_assignment(studentID, lab_num, problem_num)
            print(Fore.CYAN + "Laboratorul a fost asignat cu succes!")
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))
        except ValidationError as ve:
            print(Fore.RED + "ValidationError: \n" + str(ve))
        #except Exception as ex:
            #print(str(ex))

    def ui_grade_assignment(self):
        """
        UI function that allows the user to grade an assignment.
        """
        print("Se incepe notarea unui assignment")

        try:
            grade = float(input("Introduceti nota pe care vreti sa o dati acestui assignment: "))
            studentID = int(input("Introduceti ID-ul studentului care are assignment-ul: "))
        except ValueError:
            print(Fore.RED + "Valoare numerica invalida")
            return

        lab_number = input("Introduceti numarul laboratorului in care se afla problema din assignment: ")
        problem_number = input("Introduceti numarul problemei din assignment: ")


        try:
            self.__srv_assignment.grade_assignment(studentID, lab_number, problem_number, grade)
            print(Fore.CYAN + "Assignment notat cu succes")
        except RepositoryError as re:
            print(Fore.RED + "RepositoryError: \n" + str(re))

    def ui_add_X_random_students(self):
        """
        A UI function that allows a user to input random students.
        """
        print("Se incepe adaugarea unui numar de studenti generati aleator.")

        try:
            nr_studenti = int(input("Introduceti cati studenti ati vrea sa generati: "))
        except ValueError:
            print(Fore.RED + "Valoare intreaga invalida")
            return

        for i in range(0, nr_studenti):
            self.__srv_student.add_random_student()

    def ui_add_X_random_problems(self):
        """
        A UI function that allows a user to input random problems.
        """
        print("Se incepe adaugarea unui numar de probleme generate aleator.")

        try:
            nr_probleme = int(input("Introduceti cate probleme ati vrea sa generati: "))
        except ValueError:
            print(Fore.RED + "Valoare intreaga invalida")
            return

        for i in range(0, nr_probleme):
            self.__srv_problem.add_random_problem()

    def ui_assign_X_random_labs(self):
        """
        A UI function that allows a user to assign random labs.
        """
        print("Se incepe asignarea unui numar de laboratoare cu date alese aleator.")

        try:
            nr_laburi = int(input("Introduceti cate laboratoare ati vrea sa asignati: "))
        except ValueError:
            print(Fore.RED + "Valoare intreaga invalida")
            return

        for i in range(0, nr_laburi):
            try:
                self.__srv_assignment.add_random_assignment()
            except RepositoryError as re:
                print(Fore.RED + "RepositoryError: \n" + str(re))
                return
            except RandomnessExceededError as ree:
                print(Fore.RED + "RandomnessError: \n" + str(ree))

    def ui_magical_top50(self):
        print("Se genereaza raportul cerut.")
        try:
            magical_list = self.__srv_statistics.get_top_50per_most_assigned_problem()
        except Exception as ex:
            print(Fore.RED + str(ex))
            return

        if len(magical_list) == 0:
            print(Fore.YELLOW + "Nu sunt elemente care sa respecte cerinta")
            return

        for x in magical_list:
            print(Fore.CYAN + str(x))

    def ui_print_menu(self):
        """
        A UI function that prints the main menu.
        :return:
        """
        print("")
        print("-------------------------------------------------------")
        print("\"add_student\": Adauga un student nou in lista de studenti.")
        print("\"add_rnd_students\": Adauga X studenti noi cu date random in lista.")
        print("\"rem_student\": Elimina un student din lista de studenti.")
        print("\"src_student\": Cauta un student pe baza id-ului.")
        print("\"prt_students\": Afiseaza toti studentii din lista.")
        print("\"flt_students\": Afiseaza toti studentii din lista ai caror nume incepe cu un prefix dat de utilizator.")
        print("\"add_problem\": Adauga o problema noua in lista de probleme.")
        print("\"add_rnd_problems\": Adauga X probleme noi cu date random in lista.")
        print("\"rem_problem\": Elimina o problema din lista de probleme.")
        print("\"prt_problems\": Afiseaza toate problemele din lista.")
        print("\"src_problema\": Cauta o problema pe baza numarului de identificare.")
        print("\"assign_lab\": Asigneaza o tema de laborator unui student.")
        print("\"assign_rnd_labs\": Asigneaza X laboratoare cu date alese aleator dintre cele deja introduse.")
        print("\"grade_lab\": Noteaza o tema de laborator unui student.")
        print("\"prt_labs\": Afiseaza toate assignment-urile din lista.")
        print("\"stat_problems\": Afiseaza lista de studenți și notele lor la o problema de laborator dat, ordonat: alfabetic după nota, după nume.")
        print("\"stat_avg\": Afiseaza toți studenții cu media notelor de laborator mai mic decât 5. (nume student și notă).")
        print("\"top50\": Afiseaza un raport: Top 50% probleme cu cel mai mare nr. de studenti asignati si media notelor studentilor la problema respectiva peste 5, sortate dupa nr problemei.")
        print("\"help\": Afiseaza acest meniu.")
        print("\"exit\": Opreste executia programului.")
        print("-------------------------------------------------------")
        print("")



    def run(self):
        """
        Launches the program's main execution loop.
        """
        self.ui_print_menu()

        while True:
            cmd = input(">>>")
            if cmd == "":
                continue
            elif cmd == "exit":
                return
            elif cmd == "add_student":
                self.ui_add_student()
            elif cmd == "add_rnd_students":
                self.ui_add_X_random_students()
            elif cmd == "rem_student":
                self.ui_rem_student()
            elif cmd == "src_student":
                self.ui_find_student_by_id()
            elif cmd == "prt_students":
                self.ui_print_all_students()
            elif cmd == "flt_students":
                self.ui_filter_student_name_prefix()
            elif cmd == "add_problem":
                self.ui_add_problem()
            elif cmd == "add_rnd_problems":
                self.ui_add_X_random_problems()
            elif cmd == "rem_problem":
                self.ui_rem_problem()
            elif cmd == "src_problem":
                self.ui_find_problem_by_num()
            elif cmd == "prt_problems":
                self.ui_print_all_problems()
            elif cmd == "assign_lab":
                self.ui_add_assignment()
            elif cmd == "assign_rnd_labs":
                self.ui_assign_X_random_labs()
            elif cmd == "grade_lab":
                self.ui_grade_assignment()
            elif cmd == "prt_labs":
                self.ui_print_all_assignments()
            elif cmd == "stat_problems":
                self.ui_statistics_for_one_problem()
            elif cmd == "stat_avg":
                self.ui_statistics_average_below_5()
            elif cmd == "top50":
                self.ui_magical_top50()
            elif cmd == "help":
                self.ui_print_menu()
            else:
                print("Comanda invalida!")
