from z3 import Int, And, Or, Sum, If, Solver
from SMT.src.global_constraints import lex_lesseq


def SMT_standard_model(instance):
    # --------------------------
    #         PARAMETERS
    # --------------------------

    # Define dimensions parameters
    x = 0
    y = 1

    # Define wrapping paper roll height and width
    paper_width = instance['paper_width']
    paper_height = instance['paper_height']

    # Define wrapping paper roll coordinates
    X_COORDINATES = range(paper_width)
    Y_COORDINATES = range(paper_height)

    # Define the number of presents to wrap
    n_presents = instance['n_presents']

    # Define presents as a set of integers from 0 to num. of presents-1
    PRESENTS = range(n_presents)

    # Define the dimensions of the presents paper to cut
    presents_dimensions = instance['presents_dimensions']

    # Lower and upper bounds for the dimensions
    lower_bounds = [0, 0]
    upper_bounds = [paper_width, paper_height]

    # --------------------------
    #         VARIABLES
    # --------------------------

    # DECISION VARIABLES

    # Define bottom-left corner of the pieces of paper to cut as 2-D (width-height) array of int decision variables
    presents_corners = [[Int("x_%s" % i), Int("y_%s" % i)] for i in PRESENTS]

    # --------------------------
    #        CONSTRAINTS
    # --------------------------

    # DOMAIN CONSTRAINTS: reduce the domain for the bottom-left corners of the pieces of paper

    # The cut can not be done outside the paper roll: the bottom-left corner coordinates of the pieces of paper to cut
    # must not exceed the paper roll coordinates limit
    domain_bound_constraints = [
        And(And(presents_corners[i][x] >= lower_bounds[x], presents_corners[i][x] < upper_bounds[x]),
            And(presents_corners[i][y] >= lower_bounds[y], presents_corners[i][y] < upper_bounds[y])) for i in PRESENTS]

    # Each cutted piece of paper pieces must fit the paper roll dimensions (considering the piece of paper dimensions):
    # bottom-left corner coordinates must be also calculated considering the piece of paper dimensions
    paper_fit_constraints = [And(presents_corners[i][x] + presents_dimensions[i][x] <= paper_width,
                                 presents_corners[i][y] + presents_dimensions[i][y] <= paper_height) for i in PRESENTS]

    # PAPER LIMIT CONSTRAINT: define the maximum number of usable paper

    # The maximum usable quantity of paper is defined by the paper roll dimensions
    cumulative_constraints = [Sum(
        [If(And(y_coord >= presents_corners[i][y], y_coord < presents_corners[i][y] + presents_dimensions[i][y]),
            presents_dimensions[i][x], 0) for i in PRESENTS]) <= paper_width for y_coord in Y_COORDINATES] + [Sum(
        [If(And(x_coord >= presents_corners[i][x], x_coord < presents_corners[i][x] + presents_dimensions[i][x]),
            presents_dimensions[i][y], 0) for i in PRESENTS]) <= paper_height for x_coord in X_COORDINATES]

    # NON-OVERLAPPING CONSTRAINT: define the non-overlapping property fo the pieces of paper

    # The cutted pieces of paper must not overlap: the bottom-left corner coordinates must not be equal to other
    # coordinates of the paper roll which are already occupied by other pieces of paper

    non_overlapping_constraints = [Or(presents_corners[i][x] + presents_dimensions[i][x] <= presents_corners[j][x],
                                      presents_corners[i][y] + presents_dimensions[i][y] <= presents_corners[j][y],
                                      presents_corners[j][x] + presents_dimensions[j][x] <= presents_corners[i][x],
                                      presents_corners[j][y] + presents_dimensions[j][y] <= presents_corners[i][y]) for
                                   i in PRESENTS
                                   for j in PRESENTS if i < j]

    # OPTIMIZATION CONSTRAINTS: constraint to speed up the search of solutions

    # Symmetry breaking constraint: constraint to break the vertical and horizontal symmetries
    symmetry_breaking_constraints = [And(lex_lesseq([presents_corners[i][x] for i in PRESENTS],
                                                    [paper_width - presents_corners[i][x] - presents_dimensions[i][x]
                                                     for i in PRESENTS]),
                                         lex_lesseq([presents_corners[i][y] for i in PRESENTS],
                                                    [paper_height - presents_corners[i][y] - presents_dimensions[i][y]
                                                     for i in PRESENTS]))]

    # --------------------------
    #          SOLUTION
    # --------------------------

    solver = Solver()
    solver.add(domain_bound_constraints + paper_fit_constraints + cumulative_constraints + non_overlapping_constraints +
               symmetry_breaking_constraints)

    return solver, PRESENTS, presents_corners
