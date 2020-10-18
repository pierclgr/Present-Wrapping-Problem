from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import sys
from os import path


# Define function to plot the solution
def plot_solution(input_instance, corners, rotation):
    n_presents = input_instance['n_pieces']
    cmap = plt.cm.get_cmap('hsv', n_presents + 1)
    fig1 = plt.figure("Solution", figsize=(15, 9))
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_title("Solution to " + str(input_instance['roll_width']) + "x" + str(input_instance['roll_height']))
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    rectangles = []
    for i in range(n_presents):
        if rotation[i]:
            rectangle = Rectangle((corners[i][0], corners[i][1]), input_instance['pieces_dimensions'][i][1],
                                  input_instance['pieces_dimensions'][i][0], color=cmap(i), ec='black', lw=1.5,
                                  clip_on=False, label=str(input_instance['pieces_dimensions'][i][0]) + "x" +
                                                       str(input_instance['pieces_dimensions'][i][1]) + " (rotated)")
        else:
            rectangle = Rectangle((corners[i][0], corners[i][1]), input_instance['pieces_dimensions'][i][0],
                                  input_instance['pieces_dimensions'][i][1], color=cmap(i), ec='black', lw=1.5,
                                  clip_on=False, label=str(input_instance['pieces_dimensions'][i][0]) + "x" +
                                                       str(input_instance['pieces_dimensions'][i][1]))
        rectangles.append(rectangle)
        point = plt.Circle((corners[i][0], corners[i][1]), 0.2, color='black', clip_on=False)
        ax1.add_patch(rectangle)
        ax1.add_artist(point)
    ax1.add_artist(
        Rectangle((0, 0), input_instance['roll_width'], input_instance['roll_height'], fill=False, ec='black', lw=1.5,
                  clip_on=False))
    plt.ylim((0, input_instance['roll_height']))
    ax1.set_yticks(np.arange(0, input_instance['roll_height'] + 1, 1))
    plt.xlim((0, input_instance['roll_width']))
    ax1.set_xticks(np.arange(0, input_instance['roll_width'] + 1, 1))
    plt.grid(color='black', linestyle='--')
    plt.legend(handles=rectangles, title="$\\bf{Presents}$", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("\nCommand usage:")
        print("\tpython plot.py \"file path\" - plot specified .txt solution\n")
    else:
        specified_path = sys.argv[1]
        if path.isfile(specified_path):
            with open(specified_path) as input_instance_file:
                lines = input_instance_file.readlines()
                n_pieces = int(lines[1].rstrip())
                pieces_dimensions = [
                    [int(lines[i + 2].rstrip().split("\t")[0].split(" ")[0]),
                     int(lines[i + 2].rstrip().split("\t")[0].split(" ")[1])]
                    for
                    i in range(n_pieces)]
                instance = {'roll_width': int(lines[0].rstrip().split(" ")[0]),
                            'roll_height': int(lines[0].rstrip().split(" ")[1]),
                            'n_pieces': n_pieces,
                            'pieces_dimensions': pieces_dimensions}
                corners = [
                    [int(lines[i + 2].rstrip().split("\t")[1].split(" ")[0]),
                     int(lines[i + 2].rstrip().split("\t")[1].split(" ")[1])]
                    for i in range(n_pieces)]
                rotation = [
                    True if lines[i + 2].rstrip().split("\t")[-1] == "rotated" else False
                    for i in range(n_pieces)]
            input_instance_file.close()
            plot_solution(instance, corners, rotation)
        else:
            print("\nSpecified file does not exist, please insert an existing solution file.\n")
