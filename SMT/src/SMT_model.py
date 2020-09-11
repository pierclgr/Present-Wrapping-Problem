from SMT.src.PWP_SMT_standard import SMT_standard_model
from SMT.src.PWP_SMT_general import SMT_general_model
from z3 import sat
from datetime import datetime


def SMT_model(input_instance, general, timeout=0):
    result = {}
    not_found_timeout = False
    x, y = 0, 1

    if not general:
        solver, PRESENTS, presents_corners = SMT_standard_model(input_instance)
    else:
        solver, PRESENTS, presents_corners, presents_rotation = SMT_general_model(input_instance)

    if timeout is not 0:
        solver.set(timeout=timeout * 1000)

    start = datetime.now()
    outcome = solver.check()
    end = datetime.now()
    elapsed = end - start

    if outcome == sat:
        model = solver.model()
        result['presents_corners'] = [[int(model.evaluate(presents_corners[i][x]).as_string()),
                                       int(model.evaluate(presents_corners[i][y]).as_string())] for i in PRESENTS]
        if general:
            result['presents_rotation'] = None

    elif solver.reason_unknown() == "timeout":
        not_found_timeout = True

    return result, elapsed, not_found_timeout
