"""Решение уравнения A*x^2 + B*x + C = 0.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
"""

import math

# Наибольшее допустимое значение коэффициента по модулю.
MAX_VALUE = 10000


def check_coefficients(value):
    """Проверяет коэффициенты уравнения.

    Параметр coefficients — словарь {"A": a, "B": b, "C": c}.
    Возбуждает ValueError, если какой-либо коэффициент по модулю больше
    MAX_VALUE или если A == 0 и B == 0 (неизвестного в уравнении нет).
    """
    for name, value in value.items():
        if abs(value) > MAX_VALUE:
            raise ValueError(f"коэффициент {name} вне допустимого диапазона")


def solve_equation(a, b, c):
    """Решает уравнение a*x^2 + b*x + c = 0.

    Возвращает кортеж из трёх значений (вид, дискриминант, корни):
      вид          - строка "linear" (линейное) или "quadratic" (квадратное);
      дискриминант - число для квадратного, None для линейного;
      корни        - список из нуля, одного или двух чисел.

    Если a == 0 и b == 0, это не уравнение: вызывает ValueError.
    """
    if a == 0:
        if b == 0:
            raise ValueError("это не уравнение, неизвестное отсутствует")
        return "linear", None, [-c / b]

    d = b * b - 4 * a * c
    if d > 0:
        root = math.sqrt(d)
        roots = [(-b + root) / (2 * a), (-b - root) / (2 * a)]
    elif d == 0:
        roots = [-b / (2 * a)]
    else:
        roots = []
    return "quadratic", d, roots