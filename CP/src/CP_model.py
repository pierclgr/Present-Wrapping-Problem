from minizinc import Model, Solver, Instance
from datetime import timedelta


def CP_model(input_instance, general, timeout=0):
    not_found_timeout = False
    found = True

    if general:
        src_model = "CP/src/PWP_CP_general"
    else:
        src_model = "CP/src/PWP_CP_standard"
    model = Model(src_model + ".mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    instance["roll_width"] = input_instance['roll_width']
    instance["roll_height"] = input_instance['roll_height']
    instance["n_pieces"] = input_instance['n_pieces']
    instance["pieces_dimensions"] = input_instance['pieces_dimensions']

    if timeout != 0:
        timeout = timedelta(seconds=timeout)
        result = instance.solve(timeout=timeout)
        tolerance = timedelta(seconds=0.15)
        if result.statistics['time'] >= result.statistics['solveTime']:
            elapsed = result.statistics['time']
        else:
            elapsed = result.statistics['solveTime']
        if int(result.statistics['solutions']) == 0:
            found = False
            if elapsed >= timeout - tolerance:
                not_found_timeout = True
    else:
        result = instance.solve()
        elapsed = result.statistics['time']
        if int(result.statistics['solutions']) == 0:
            found = False

    return result, elapsed, not_found_timeout, result.statistics, found
