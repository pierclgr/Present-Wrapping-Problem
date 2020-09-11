from os import path, makedirs
import sys
import pyfiglet
import glob
import ntpath
import shutil
from CP.src.CP_model import CP_model
from SMT.src.SMT_model import SMT_model
from datetime import timedelta

from utils.plot import plot_solution


def command_line_interface():
    specified_path, specified_method, specified_mode, specified_plot, specified_timeout = None, None, None, None, None

    if len(sys.argv) <= 1:
        print(pyfiglet.figlet_format("P.W.P.", font="slant") + "-" * 25)
        print("Present Wrapping Problem")
        print("-" * 25, "\n")

        print("Mandatory commands that can be used:\n")
        print("--solve \"path\")")
        print("\tsolves the specified file/folder instance(s):")
        print("\t\tif \"path\" is a file, solves that file instance")
        print("\t\tif \"path\" is a folder, solves all the file instances in that folder\n")
        print("--method \"solver\"")
        print("\tsolves the specified file/folder instance(s) using one of these solver:")
        print("\t\t\"CP\" - Constraint Programming")
        print("\t\t\"SAT\" - Propositional Satisfiability")
        print("\t\t\"SMT\" - Satisfiability Modulo Theories\n")
        print("--mode \"solving_mode\"")
        print("\tsolves the specified file/folder instance(s) using one of these mode:")
        print("\t\t\"standard\" - standard mode")
        print("\t\t\"general\" - general mode (rotation and optimization of pieces with same size)\n")

        print("Optional commands:\n")
        print("--timeout \"seconds\"")
        print("\tspecifies a timeout (in seconds) for the search of each instance solution\n")
        print("--plot")
        print("\tif used, the solution is plotted visually (only works when specifying a single file)\n")
    else:
        commands = sys.argv
        if "--solve" not in commands:
            raise Exception("\nUnspecified file(s) to solve, use --solve \"path\" command.\n")
        elif "--method" not in commands:
            raise Exception("\nUnspecified solving method, use --method \"solver\" command.\n")
        elif "--mode" not in commands:
            raise Exception("\nUnspecified solving mode, use --mode \"solving_mode\" command.\n")

        solve_index = commands.index("--solve")
        try:
            specified_path = commands[solve_index + 1]
        except IndexError:
            raise Exception("\nNo arguments specified for --solve command, please insert a file/folder instance(s) "
                            "to solve.\n")

        method_index = commands.index("--method")
        try:
            specified_method = commands[method_index + 1]
        except IndexError:
            raise Exception("\nNo arguments specified for --method command, please insert a solving method.\n")

        mode_index = commands.index("--mode")
        try:
            specified_mode = commands[mode_index + 1]
        except IndexError:
            raise Exception("\nNo arguments specified for --mode command, please insert a solving mode.\n")

        if "--timeout" in commands:
            timeout_index = commands.index("--timeout")
            try:
                specified_timeout = commands[timeout_index + 1]
            except IndexError:
                raise Exception("\nNo arguments specified for --timeout command, please insert a timeout in "
                                "seconds.\n")

        if "--plot" in commands:
            specified_plot = True
        else:
            specified_plot = False

    return specified_path, specified_method, specified_mode, specified_timeout, specified_plot


# Define function to choose the timeout
def choose_timeout(chosen_timeout):
    if chosen_timeout is None:
        chosen_timeout = 0
    else:
        try:
            chosen_timeout = int(chosen_timeout)
        except ValueError:
            raise Exception(
                "\n\"" + chosen_timeout + "\" is not a valid timeout, please insert a timeout in seconds.\n")

        if chosen_timeout < 1:
            raise Exception("\n\"" + str(chosen_timeout) + "\" is not a valid timeout, please insert a non-negative "
                                                           "and not null timeout.\n")

    return chosen_timeout


# Define function to choose the solving mode (general or standard)
def choose_mode(chosen_mode):
    chosen_mode.lower()
    if chosen_mode == "general":
        general = True
    elif chosen_mode == "standard":
        general = False
    else:
        raise Exception("\n\"" + chosen_mode + "\" is not a valid solving mode, "
                                               "please insert one of these modes:\n"
                                               "\t\"standard\" - standard mode\n"
                                               "\t\"general\" - general mode (rotation "
                                               "and optimization of pieces with same size)\n")

    return general


# Define function to choose the input instance
def choose_input_instance(chosen_input_instance):
    if path.isfile(chosen_input_instance):
        files_in_folder = [chosen_input_instance]
    elif path.isdir(chosen_input_instance):
        files_in_folder = glob.glob(chosen_input_instance + "/*.txt")
        if not files_in_folder:
            raise Exception("\nSpecified folder is empty, please insert a folder containing file instances.\n")
    else:
        raise Exception("\n\"" + chosen_input_instance + "\" file/folder does not exist, please insert a valid "
                                                         "file/folder path.\n")

    files_in_folder.sort()
    files_in_folder.sort(key=lambda s: len(s))

    instances = []
    for file in files_in_folder:
        name = ntpath.basename(file).split(".")[0]
        with open(file) as input_instance_file:
            lines = input_instance_file.readlines()
            n_presents = int(lines[1].rstrip())
            presents_dimensions = [[int(lines[i + 2].rstrip().split(" ")[0]), int(lines[i + 2].rstrip().split(" ")[1])]
                                   for
                                   i in range(n_presents)]
            instance = {'paper_width': int(lines[0].rstrip().split(" ")[0]),
                        'paper_height': int(lines[0].rstrip().split(" ")[1]),
                        'n_presents': n_presents,
                        'presents_dimensions': presents_dimensions,
                        'name': name}
            instances.append(instance)

    input_instance_file.close()
    return instances


# Define function to choose the solving method
def choose_method(chosen_method):
    if chosen_method.upper() != "CP" and chosen_method.upper() != "SAT" and chosen_method.upper() != "SMT":
        raise Exception("\n\"" + chosen_method + "\" is not a valid solving method, "
                                                 "please insert one of these methods:\n"
                                                 "\t\"CP\" - Constraint Programming\n"
                                                 "\t\"SAT\" - Propositional Satisfiability\n"
                                                 "\t\"SMT\" - Satisfiability Modulo Theories\n")

    chosen_solving_method = chosen_method.upper()

    return chosen_solving_method


# Define function to save the solution to file
def save_solution(solving_method, chosen_input_instance, general, corners, rotation):
    file_name = chosen_input_instance

    if general:
        out_path = solving_method + "/out/general/"
    else:
        out_path = solving_method + "/out/standard/"

    if not path.exists(out_path):
        makedirs(out_path)

    out_path = out_path + file_name + "-out.txt"
    shutil.copy2("in/" + chosen_input_instance + ".txt", out_path)

    with open(out_path, "r+") as output_file:
        lines = output_file.readlines()
        if int(lines[1].rstrip()) == len(corners):
            output_file.seek(0)
            output_file.write(lines[0])
            output_file.write(lines[1])
            for i in range(len(corners)):
                if rotation[i]:
                    output_file.write(
                        lines[i + 2].rstrip() + "\t" + str(corners[i][0]) + " " + str(corners[i][1]) + "\trotated\n")
                else:
                    output_file.write(
                        lines[i + 2].rstrip() + "\t" + str(corners[i][0]) + " " + str(corners[i][1]) + "\n")
            output_file.truncate()
        else:
            raise Exception(
                "\nError in saving the solution: the number of pieces is not the same number of presents.\n")
    output_file.close()

    return path.abspath(out_path)


def solve(input_instance, solving_method, general, timeout):
    found = True
    corners = None
    rotation = None

    if solving_method == "CP":
        result, elapsed, not_found_timeout = CP_model(input_instance, general, timeout)
    elif solving_method == "SMT":
        result, elapsed, not_found_timeout = SMT_model(input_instance, general, timeout)
    else:
        raise Exception("Error in choosing solving method.\n")

    try:
        corners = result['presents_corners']
        if general:
            rotation = result['presents_rotation']
    except KeyError:
        found = False

    return found, corners, rotation, elapsed, not_found_timeout


if __name__ == "__main__":
    #try:
    specified_path, specified_method, specified_mode, specified_timeout, specified_plot = command_line_interface()

    # Choose the model (standard or complete)
    general = choose_mode(specified_mode)

    # Choose the input instance
    input_instances = choose_input_instance(specified_path)

    # Choose the solving method
    solving_method = choose_method(specified_method)

    timeout = choose_timeout(specified_timeout)

    out_path = ""

    if len(input_instances) is 0:
        raise Exception("\nSpecified folder is empty, please insert a folder containing file instances.\n")

    for input_instance in input_instances:

        print("Solving " + input_instance['name'] + " instance...")

        found, corners, rotation, elapsed, not_found_timeout = solve(input_instance, solving_method, general,
                                                                     timeout)
        if timeout is 0:
            not_found_timeout = False

        if found:
            print("Solution found in " + str(elapsed) + ".")
            if not general:
                rotation = [False for _ in range(input_instance['n_presents'])]
            out_path = save_solution(solving_method, input_instance['name'], general, corners, rotation)
            print("Solution saved in \"" + path.abspath(out_path) + "\".\n")
            if specified_plot and len(input_instances) is 1:
                plot_solution(input_instance, corners, rotation)
        else:
            if not not_found_timeout:
                print("No solution existing for " + input_instance['name'] + " instance.\n")
            else:
                print("Timeout! Solution not found for " + input_instance['name'] + " instance in " + str(
                    timedelta(seconds=timeout))+".\n")
    """except Exception as e:
        print(e)"""
