%     ____ _       __   ____ 
%    / __ \ |     / /  / __ \
%   / /_/ / | /| / /  / /_/ /
%  / ____/| |/ |/ /_ / ____/ 
% /_/   (_)__/|__/(_)_/   (_)
                     
% -------------------------
% Present Wrapping Problem
% ------------------------- 

% Standard CP model (no rotation)

% Global constraints inclusions
include "cumulative.mzn";
include "diffn_k.mzn";
include "lex_lesseq.mzn";

% --------------------------
%         PARAMETERS
% --------------------------

% Define dimensions parameters
int: x = 1;
int: y = 2;
set of int: DIMENSIONS = x..y;

% Define wrapping paper roll height and width
int: paper_width;
int: paper_height;

% Define the number of presents to wrap
int: n_presents;

% Define presents as a set of integers from 1 to num. of presents
set of int: PRESENTS = 1..n_presents;

% Define the dimensions of the presents paper to cut
array[PRESENTS, DIMENSIONS] of int: presents_dimensions;

% Lower and upper bounds for the dimensions
array[DIMENSIONS] of int: lower_bounds = [0, 0];
array[DIMENSIONS] of int: upper_bounds = [paper_width, paper_height];

% --------------------------
%         VARIABLES
% --------------------------

% DECISION VARIABLES

% Define bottom-left corner of the pieces of paper to cut as 2-D (width-height) array of int decision variables
array[PRESENTS, DIMENSIONS] of var int: presents_corners;

% --------------------------
%        CONSTRAINTS
% --------------------------

% DOMAIN CONSTRAINTS: reduce the domain for the bottom-left corners of the pieces of paper

% The cut can not be done outside the paper roll: the bottom-left corner coordinates of the pieces of paper to cut
% must not exceed the paper roll coordinates limit
constraint forall(i in PRESENTS)((presents_corners[i, x] >= lower_bounds[x] /\ presents_corners[i, x] < upper_bounds[x]) /\
                                 (presents_corners[i, y] >= lower_bounds[y] /\ presents_corners[i, y] < upper_bounds[y]));

% Each cutted piece of paper pieces must fit the paper roll dimensions (considering the piece of paper dimensions): 
% bottom-left corner coordinates must be also calculated considering the piece of paper dimensions
constraint forall(i in PRESENTS)((presents_corners[i, x] + presents_dimensions[i, x] <= paper_width) /\ 
                                 (presents_corners[i, y] + presents_dimensions[i, y] <= paper_height));

% PIMPLIED CUMULATIVE CONSTRAINTS: define the maximum number of usable paper

% The maximum usable quantity of paper is defined by the paper roll dimensions
constraint cumulative(presents_corners[.., x], presents_dimensions[.., x], presents_dimensions[.., y], paper_height) /\
           cumulative(presents_corners[.., y], presents_dimensions[.., y], presents_dimensions[.., x], paper_width);

% NON-OVERLAPPING CONSTRAINTS: define the non-overlapping property fo the pieces of paper

% The cutted pieces of paper must not overlap: the bottom-left corner coordinates must not be equal to other coordinates
% of the paper roll which are already occupied by other pieces of paper
constraint diffn_k(presents_corners, presents_dimensions);

% OPTIMIZATION CONSTRAINTS: constraint to speed up the search of solutions

% Symmetry breaking constraint: constraint to break the vertical and horizontal symmetries
constraint lex_lesseq(presents_corners[.., x], [paper_width - presents_corners[i, x] - presents_dimensions[i, x] | i in PRESENTS]) /\
           lex_lesseq(presents_corners[.., y], [paper_height - presents_corners[i, y] - presents_dimensions[i, y] | i in PRESENTS]);


% --------------------------
%          SOLUTION
% --------------------------

% SEARCH ANNOTATION

% Use sarch  and restart annotations to investigate for best search strategy
ann: search_annotation;
% ann: restart_annotation;

search_annotation = int_search(presents_corners, first_fail, indomain_min); % BEST SOLUTION
% search_annotation = int_search(presents_corners, first_fail, indomain_split_random);
% search_annotation = int_search(presents_corners, dom_w_deg, indomain_min);
% search_annotation = int_search(presents_corners, dom_w_deg, indomain_split_random);
% search_annotation = int_search(presents_corners, most_constrained, indomain_min);
% search_annotation = int_search(presents_corners, most_constrained, indomain_split_random);

% restart_annotation = restart_luby(100);

% Search for solution as a constraint satisfaction problem
solve :: search_annotation 
      satisfy;

% Output the solution(s)
output ["Solution:\n"];
output [show(presents_dimensions[i, x]) ++ " " ++ show(presents_dimensions[i, y]) ++ "\t" ++ 
        show(presents_corners[i, x]) ++ " " ++ show(presents_corners[i, y]) ++
        "\n" | i in PRESENTS];