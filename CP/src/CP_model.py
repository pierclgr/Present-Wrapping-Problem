from minizinc import Model, Solver, Instance
from datetime import timedelta


def CP_model(input_instance, general, timeout=0):
    not_found_timeout = False
    # Declare path for the src of the model
    if general:
        src_model = "CP/src/PWP_CP_general"
    else:
        src_model = "CP/src/PWP_CP_standard"
    model = Model(src_model + ".mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    instance["paper_width"] = input_instance['paper_width']
    instance["paper_height"] = input_instance['paper_height']
    instance["n_presents"] = input_instance['n_presents']
    instance["presents_dimensions"] = input_instance['presents_dimensions']

    if timeout is not 0:
        timeout = timedelta(seconds=timeout)
        result = instance.solve(timeout=timeout)
        if result.statistics['time'] >= timeout:
            not_found_timeout = True
    else:
        result = instance.solve()

    return result, result.statistics['solveTime'], not_found_timeout
