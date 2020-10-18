from z3 import And, Or


def lex_less(a, b):
    def lex_less_auxiliary(a, b, i, accumulator):
        if i == len(a) - 1:
            return lex_less_auxiliary(a, b, i - 1, a[i] < b[i])
        elif i == 0:
            return Or(a[i] < b[i], And(a[i] == b[i], accumulator))
        else:
            return lex_less_auxiliary(a, b, i - 1, Or(a[i] < b[i], And(a[i] == b[i], accumulator)))

    return lex_less_auxiliary(a, b, len(a) - 1, True)
