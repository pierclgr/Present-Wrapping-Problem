from SMT.src.PWP_SMT_standard import SMT_standard_model
from SMT.src.PWP_SMT_general import SMT_general_model
from z3 import sat
from datetime import timedelta


def SMT_model(input_instance, general, timeout=0):
    result = {}
    found = True
    not_found_timeout = False
    x, y = 0, 1

    if not general:
        solver, PRESENTS, pieces_corners = SMT_standard_model(input_instance)
        pieces_rotation = None
    else:
        solver, PRESENTS, pieces_corners, pieces_rotation = SMT_general_model(input_instance)

    if timeout != 0:
        solver.set(timeout=timeout * 1000)

    outcome = solver.check()

    if outcome == sat:
        model = solver.model()
        result['pieces_corners'] = [[int(model.evaluate(pieces_corners[i][x]).as_string()),
                                       int(model.evaluate(pieces_corners[i][y]).as_string())] for i in PRESENTS]
        if general:
            result['pieces_rotation'] = [bool(model.evaluate(pieces_rotation[i])) for i in PRESENTS]
    else:
        found = False
        if solver.reason_unknown() == "timeout":
            not_found_timeout = True

    return result, timedelta(
        milliseconds=solver.statistics().get_key_value('time') * 1000), not_found_timeout, solver.statistics(), found
