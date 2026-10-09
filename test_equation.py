from calc import equation

# Проверка solve
print(equation.solve(1, -3, 2))   # ('квадратное', 1, [2.0, 1.0])
print(equation.solve(1, -2, 1))   # ('квадратное', 0, [1.0])
print(equation.solve(1, 0, 5))    # ('квадратное', -20, [])
print(equation.solve(0, 2, -5))   # ('линейное', None, [2.5])
print(equation.solve(0, 0, 7))    # ('нет', None, [])

# Проверка validate
equation.validate_coefficients({"A": 1, "B": -3, "C": 2})
print("Проверка 1: ок")

try:
    equation.validate_coefficients({"A": 50000, "B": 1, "C": 1})
except ValueError as e:
    print(f"Проверка 2: {e}")