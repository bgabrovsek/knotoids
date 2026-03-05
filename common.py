from collections import defaultdict
import knotpy as kp
from sympy import expand, symbols, Symbol

def laurent_polynomial_to_tuples(expr, var):
    """
    Converts a SymPy Laurent polynomial expression into a list of tuples representation.

    Args:
        expr (core.expr.Expr): The SymPy Laurent polynomial expression to convert.
        var (core.symbol.Symbol): The variable in the Laurent polynomial.

    Returns:
        list of tuples: Each tuple represents a term in the polynomial as (coefficient, exponent).
    """

    if isinstance(var, str):
        var = symbols(var)

    if not isinstance(var, Symbol):
        raise ValueError("The variable must be a SymPy Symbol")

    # Expand the expression to ensure all terms are separated
    expr = expand(expr)

    # Get the terms of the polynomial
    terms = expr.as_ordered_terms()

    # Convert the terms into tuples
    poly_tuples = []
    for term in terms:
        coeff = term.as_coeff_exponent(var)[0]
        exponent = term.as_coeff_exponent(var)[1]
        poly_tuples.append((coeff, exponent))

    return sorted(poly_tuples, key=lambda t: (t[1],t[0]))

def is_mirror(poly):
    # return True if poly is the smaller of the two mirror polynomials
    def zlp(poly):
        # zip laurent poly
        return tuple(zip(*[(e, c) for c, e in kp.laurent_polynomial_to_tuples(poly, "A")]))
    return zlp(poly) < zlp(kp.reciprocal(poly, "A"))

def print_stats(d):
    print("Stats:")
    if isinstance(d, defaultdict):
        for key, value in d.items():
            print(key, ":", value)


from collections import Counter

def plot_bar_chart(set_list):
    # Count lengths, grouping 10 or more into one bin
    length_counts = Counter(min(len(s), 10) for s in set_list)

    print()

    # Prepare bins from 1 to 10
    for length in range(1, 11):
        count = length_counts.get(length, 0)
        label = f"{length}" if length < 10 else "10+"
        bar = '█' * count
        print(f"{label:>3}: {bar} ({count})")

    print()


# sets = [{1}, {1, 2}, {1, 2, 3}, {1, 2}, {1}, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, {1, 2}, set()]
# plot_bar_chart(sets)