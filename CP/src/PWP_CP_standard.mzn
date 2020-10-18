%     ____ _       __   ____ 
%    / __ \ |     / /  / __ \
%   / /_/ / | /| / /  / /_/ /
%  / ____/| |/ |/ /_ / ____/ 
% /_/   (_)__/|__/(_)_/   (_)
                     
% -------------------------
% Present Wrapping Problem
% ------------------------- 

% Standard CP model

% Global constraints inclusions
include "cumulative.mzn";
include "diffn_k.mzn";

% --------------------------
%         PARAMETERS
% --------------------------

% Define axes parameters
int: x = 1;
int: y = 2;
set of int: AXES = x..y;

% Define wrapping paper roll height and width
int: roll_width;
int: roll_height;

% Define the number of pieces to cut
int: n_pieces;

% Define pieces as a set of integers from 1 to num. of pieces
set of int: PIECES = 1..n_pieces;

% Define the dimensions of the pieces to cut
array[PIECES, AXES] of int: pieces_dimensions;

% Define lower and upper bounds for the dimensions
array[AXES] of int: lower_bounds = [0, 0];
array[AXES] of int: upper_bounds = [roll_width, roll_height];

% Define coordinates over the two axes
set of int: X_COORDINATES = lower_bounds[x]..upper_bounds[x]-1;
set of int: Y_COORDINATES = lower_bounds[y]..upper_bounds[y]-1;

% --------------------------
%         VARIABLES
% --------------------------

% DECISION VARIABLES

% Define bottom-left corner of the pieces of paper to cut as 2-D (width-height) array of int decision variables
array[PIECES, AXES] of var int: pieces_corners;

% --------------------------
%        CONSTRAINTS
% --------------------------

% DOMAIN CONSTRAINTS: reduce the domain for the bottom-left corners of the pieces of paper

% The cut can not be done outside the paper roll: the bottom-left corner coordinates of the pieces of paper to cut
% must not exceed the paper roll coordinates limit, considering also the dimension of the piece of paper
constraint forall(i in PIECES)((pieces_corners[i, x] >= lower_bounds[x] /\ pieces_corners[i, x] <= upper_bounds[x] - pieces_dimensions[i, x]) /\
                               (pieces_corners[i, y] >= lower_bounds[y] /\ pieces_corners[i, y] <= upper_bounds[y] - pieces_dimensions[i, y]));

% IMPLIED CUMULATIVE CONSTRAINTS: define the maximum number of usable paper

% The maximum usable quantity of paper is defined by the paper roll dimensions
constraint forall (x_coord in X_COORDINATES) (
                  sum(i in PIECES) 
                  (if x_coord >= pieces_corners[i, x] /\ x_coord < pieces_corners[i, x] + pieces_dimensions[i, x] then pieces_dimensions[i, y] else 0 endif) = roll_height) /\
           forall (y_coord in Y_COORDINATES) (
                  sum(i in PIECES) 
                  (if y_coord >= pieces_corners[i, y] /\ y_coord < pieces_corners[i, y] + pieces_dimensions[i, y] then pieces_dimensions[i, x] else 0 endif) = roll_width);

% NON-OVERLAPPING CONSTRAINTS: define the non-overlapping property fo the pieces of paper

% The cutted pieces of paper must not overlap: the bottom-left corner coordinates must not be equal to other coordinates
% of the paper roll which are already occupied by other pieces of paper
constraint diffn_k(pieces_corners, pieces_dimensions);

% --------------------------
%          SOLUTION
% --------------------------

% SEARCH ANNOTATION

% Use sarch  and restart annotations to investigate for best search strategy
ann: search_annotation;
ann: restart_annotation;

search_annotation = seq_search([int_search(pieces_corners[.., x], dom_w_deg, indomain_min), 
                                int_search(pieces_corners[.., y], dom_w_deg, indomain_min)]);

restart_annotation = restart_luby(1000);

% Search for solution as a constraint satisfaction problem
solve :: search_annotation
      :: restart_annotation
      satisfy;

% Output the solution(s)
output ["Solution:\n"];
output [show(roll_width) ++ " " ++ show(roll_height) ++ "\n" ++
        show(n_pieces) ++ "\n"];
          
output [show(pieces_dimensions[i, x]) ++ " " ++ show(pieces_dimensions[i, y]) ++ "\t" ++ 
        show(pieces_corners[i, x]) ++ " " ++ show(pieces_corners[i, y]) ++
        "\n" | i in PIECES];