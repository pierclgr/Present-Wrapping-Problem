import sys
from os import path, makedirs
import glob


def convert_to_dzn(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        n_presents = int(lines[1].rstrip())
        presents_dimensions = [[int(lines[i + 2].rstrip().split(" ")[0]), int(lines[i + 2].rstrip().split(" ")[1])] for
                               i in range(n_presents)]
        paper_width = int(lines[0].rstrip().split(" ")[0])
        paper_height = int(lines[0].rstrip().split(" ")[1])
    file.close()

    out_folder = path.dirname(file_path) + "/dzn/"
    file_name = path.basename(file_path).split(".")[0]

    with open(out_folder + file_name + ".dzn", "w") as out_file:
        out_file.write("paper_width = " + str(paper_width) + ";\n")
        out_file.write("paper_height = " + str(paper_height) + ";\n")
        out_file.write("n_presents = " + str(n_presents) + ";\n")
        out_file.write("presents_dimensions = [|")
        for elem in presents_dimensions:
            out_file.write("\n" + str(elem[0]) + ", " + str(elem[1]) + "|")
        out_file.write("];")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("\nCommand usage:")
        print("\tpython txt_to_dzn.py \"file path\" - convert specified .txt file to .dzn")
        print("\tpython txt_to_dzn.py \"folder path\" - convert all .txt files in specified folder to .dzn\n")
    else:
        specified_path = sys.argv[1]
        if path.isfile(specified_path):
            out_folder = path.dirname(specified_path) + "/dzn/"
            if not path.exists(out_folder):
                makedirs(out_folder)
            convert_to_dzn(specified_path)
            file_name = path.basename(specified_path).split(".")[0] + ".dzn"
            print("\nConversion finished successfully, file saved in \"" + out_folder + file_name + "\".\n")
        elif path.isdir(specified_path):
            files_in_folder = glob.glob(specified_path + "/*.txt")
            if not files_in_folder:
                print("\nSpecified folder is empty.\n")
            else:
                if specified_path[-1] == "/":
                    out_folder = specified_path + "dzn/"
                else:
                    out_folder = specified_path + "/dzn/"
                if not path.exists(out_folder):
                    makedirs(out_folder)
                for file_path in files_in_folder:
                    convert_to_dzn(file_path)
                print("\nConversion finished successfully, files saved in \"" + out_folder + "\".\n")
        else:
            print("\nSpecified path is not an existing file or folder.\n")
