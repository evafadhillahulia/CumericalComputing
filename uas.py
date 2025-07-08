import math
import re
import sympy as sp
from tabulate import tabulate

table_data = [["x", "f(x)", "f(x + h)", "f(x + 2h)", "f'(x) numerik", "f'(x) analitik", "error"]]

# Input
expression = input("Input expression: ")
bottom_limit = float(input("Input bottom limit: "))
upper_limit = float(input("Input upper limit: "))

# Tukar jika salah urutan
if bottom_limit > upper_limit:
    bottom_limit, upper_limit = upper_limit, bottom_limit

print("1. Forward Differential\n2. Integral")
choice = int(input("> "))

# Input step or n
step = float(input(f"Input {'h' if choice == 1 else 'n'}: "))


def preprocess(pattern):
    expression = pattern.replace("^", "**").replace("e", str(math.e))
    return re.sub(r'(-?\d)([a-zA-Z])', r'\1*\2', expression)

def evaluate_expression(expression, x_value):
    x = sp.Symbol('x')
    processed_expr = preprocess(expression)
    parsed_expr = sp.sympify(processed_expr)
    return parsed_expr.subs(x, x_value).evalf()

def get_analytical_derivative(expression):
    x = sp.Symbol('x')
    processed_expr = preprocess(expression)
    parsed_expr = sp.sympify(processed_expr)
    return sp.diff(parsed_expr, x)

def evaluate_differential(fxh, fx, h):
    return (fxh - fx) / h

def do_differential():
    x = bottom_limit
    h = step
    diff_expr = get_analytical_derivative(expression)

    print(f"\nTurunan analitik f'(x) = {diff_expr}\n")

    while x <= upper_limit:
        fx = evaluate_expression(expression, x)
        fxh = evaluate_expression(expression, x + h)
        fx2h = evaluate_expression(expression, x + 2 * h)

        numerical_diff = evaluate_differential(fxh, fx, h)
        analytical_diff = sp.lambdify(sp.Symbol('x'), diff_expr)(x)
        error = analytical_diff - numerical_diff

        table_data.append([
            round(x, 4),
            round(fx, 6),
            round(fxh, 6),
            round(fx2h, 6),
            round(numerical_diff, 6),
            round(analytical_diff, 6),
            round(error, 6)
        ])
        x += h

    print("Hasil Turunan Numerik vs Analitik:")
    print(tabulate(table_data, headers="firstrow", tablefmt="rounded_grid"))

def evaluate_integral(h, fxs):
    return h / 2 * (fxs[0] + 2 * sum(fxs[1:-1]) + fxs[-1])

def do_integral():
    n = int(step)
    h = (upper_limit - bottom_limit) / n

    x_values = [bottom_limit + i * h for i in range(n + 1)]
    fxs = [evaluate_expression(expression, x) for x in x_values]

    numerical_result = evaluate_integral(h, fxs)

    x = sp.Symbol('x')
    processed_expr = preprocess(expression)
    parsed_expr = sp.sympify(processed_expr)
    analytical_result = sp.integrate(parsed_expr, (x, bottom_limit, upper_limit)).evalf()
    error = analytical_result - numerical_result

    print("\nHasil Integral Numerik vs Analitik:")
    print(f"Metode Trapesium ≈ {round(numerical_result, 6)}")
    print(f"Metode Analitik   = {round(analytical_result, 6)}")
    print(f"Error             = {round(error, 6)}")


print()
print(f"f(x) = {preprocess(expression)}")
print(f"x    = [{bottom_limit}, {upper_limit}]")
print(f"{'h' if choice == 1 else 'n'}    = {step}")

if choice == 1:
    do_differential()
elif choice == 2:
    do_integral()
else:
    print("Invalid input!")
