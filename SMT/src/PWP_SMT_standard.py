#     ____ _       __   ____
#    / __ \ |     / /  / __ \
#   / /_/ / | /| / /  / /_/ /
#  / ____/| |/ |/ /_ / ____/
# /_/   (_)__/|__/(_)_/   (_)

# -------------------------
# Present Wrapping Problem
# -------------------------

# Standard SMT model

# Library inclusions
from z3 import Int, And, Or, Sum, If, Solver


def SMT_standard_model(instance):
    # --------------------------
    #         PARAMETERS
    # --------------------------

    # Define dimensions parameters
    x = 0
    y = 1

    # Define wrapping paper roll height and width
    roll_width = instance['roll_width']
    roll_height = instance['roll_height']

    # Define wrapping paper roll coordinates
    X_COORDINATES = range(roll_width)
    Y_COORDINATES = range(roll_height)

    # Define the number of pieces to cut
    n_pieces = instance['n_pieces']

    # Define pieces as a set of integers from 0 to num. of presents-1
    PIECES = range(n_pieces)

    # Define the dimensions of the piecesq to cut
    pieces_dimensions = instance['pieces_dimensions']

    # Define lower and upper bounds for the dimensions
    lower_bounds = [0, 0]
    upper_bounds = [roll_width, roll_height]

    # --------------------------
    #         VARIABLES
    # --------------------------

    # DECISION VARIABLES

    # Define bottom-left corner of the pieces of paper to cut as 2-D (width-height) array of int decision variables
    pieces_corners = [[Int("x_%s" % i), Int("y_%s" % i)] for i in PIECES]

    # --------------------------
    #        CONSTRAINTS
    # --------------------------

    # DOMAIN CONSTRAINTS: reduce the domain for the bottom-left corners of the pieces of paper

    # The cut can not be done outside the paper roll: the bottom-left corner coordinates of the pieces of paper to cut
    # must not exceed the paper roll coordinates limit, considering also the dimension of the piece of paper
    domain_bound_constraints = [
        And(And(pieces_corners[i][x] >= lower_bounds[x],
                pieces_corners[i][x] <= upper_bounds[x] - pieces_dimensions[i][x]),
            And(pieces_corners[i][y] >= lower_bounds[y],
                pieces_corners[i][y] <= upper_bounds[y] - pieces_dimensions[i][y])) for i in PIECES]

    # IMPLIED CUMULATIVE CONSTRAINTS: define the maximum number of usable paper

    # The maximum usable quantity of paper is defined by the paper roll dimensions
    cumulative_constraints = [Sum(
        [If(And(y_coord >= pieces_corners[i][y], y_coord < pieces_corners[i][y] + pieces_dimensions[i][y]),
            pieces_dimensions[i][x], 0) for i in PIECES]) == roll_width for y_coord in Y_COORDINATES] + [Sum(
        [If(And(x_coord >= pieces_corners[i][x], x_coord < pieces_corners[i][x] + pieces_dimensions[i][x]),
            pieces_dimensions[i][y], 0) for i in PIECES]) == roll_height for x_coord in X_COORDINATES]

    # NON-OVERLAPPING CONSTRAINT: define the non-overlapping property fo the pieces of paper

    # The cutted pieces of paper must not overlap: the bottom-left corner coordinates must not be equal to other
    # coordinates of the paper roll which are already occupied by other pieces of paper

    non_overlapping_constraints = [Or(pieces_corners[i][x] + pieces_dimensions[i][x] <= pieces_corners[j][x],
                                      pieces_corners[i][y] + pieces_dimensions[i][y] <= pieces_corners[j][y],
                                      pieces_corners[j][x] + pieces_dimensions[j][x] <= pieces_corners[i][x],
                                      pieces_corners[j][y] + pieces_dimensions[j][y] <= pieces_corners[i][y])
                                   for i in PIECES for j in PIECES if i < j]

    # --------------------------
    #          SOLUTION
    # --------------------------

    solver = Solver()
    solver.add(domain_bound_constraints + cumulative_constraints + non_overlapping_constraints)

    return solver, PIECES, pieces_corners
