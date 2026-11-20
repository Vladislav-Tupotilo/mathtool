"""Суммы знакочередующихся рядов.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
Формула ряда передаётся функциям суммирования параметром.
"""

import math

# Наибольшее допустимое количество слагаемых (--terms).
MAX_TERMS = 10000
# Наибольшее допустимое eps, то есть самая грубая точность (--eps).
MAX_EPS = 0.0001
# Предел числа повторений цикла суммирования по точности.
MAX_ITERATIONS = 100000

# Количество знаков после запятой в сумме, получается из MAX_EPS.
DIGITS = math.ceil(-math.log10(MAX_EPS))


def sign(n):
    """Знак n-го слагаемого: нечётное +1, чётное -1."""
    if n % 2 == 0:
        return -1
    return 1


def term_sqplus(n):
    """n-е слагаемое ряда sqplus со знаком: (-1)^(n+1) / (n^2 + 1)."""
    return sign(n) / (n * n + 1)


def term_third(n):
    """n-е слагаемое ряда third со знаком: (-1)^(n+1) / (3 * n)."""
    return sign(n) / (3 * n)

def D(n):
    return sign(n)/(n**3 - 12)


# Таблица рядов: имя -> (функция слагаемого, текст формулы для вывода).
FORMULAS = {
    "sqplus": (term_sqplus, "S = 1/(1^2+1) - 1/(2^2+1) + 1/(3^2+1) - ..."),
    "third": (term_third, "S = 1/3 - 1/6 + 1/9 - 1/12 + ..."),
    "D": (D,""),
}


def check_terms(terms):
    """Проверяет количество слагаемых: от 1 до MAX_TERMS.

    При нарушении вызывает ValueError.
    """
    if not 1 <= terms <= MAX_TERMS:
        raise ValueError(
            f"количество слагаемых вне диапазона: от 1 до {MAX_TERMS}"
        )


def check_eps(eps):
    """Проверяет точность: конечное число, больше 0 и не больше MAX_EPS.

    При нарушении вызывает ValueError.
    """
    if not (math.isfinite(eps) and 0 < eps <= MAX_EPS):
        raise ValueError(
            f"точность вне диапазона: больше 0 и не больше {MAX_EPS}"
        )


def sum_by_count(term, count):
    """Сумма первых count слагаемых ряда.

    term - функция слагаемого: получает номер, возвращает значение со знаком.
    Возвращает кортеж (сумма, количество слагаемых).
    """
    result = 0
    for n in range(1, count + 1):
        result += term(n)
    return result, count


def sum_by_eps(term, eps):
    """Суммирует ряд, пока модуль слагаемого не станет меньше eps.

    Слагаемое, которое оказалось меньше eps, входит в сумму последним.
    term - функция слагаемого: получает номер, возвращает значение со знаком.
    Возвращает кортеж (сумма, количество слагаемых).
    Если за MAX_ITERATIONS повторений точность не достигнута,
    вызывает ValueError.
    """
    result = 0
    n = 0
    while True:
        n += 1
        value = term(n)
        result += value
        if abs(value) < eps:
            return result, n
        if n >= MAX_ITERATIONS:
            raise ValueError(
                f"точность не достигнута за {MAX_ITERATIONS} повторений"
            )