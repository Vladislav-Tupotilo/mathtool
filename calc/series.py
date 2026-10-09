"""Суммы знакочередующихся рядов.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
Формула ряда передаётся функциям суммирования параметром.
"""

import math

# Наибольшее допустимое количество слагаемых.
MAX_TERMS = 10000
# Наибольшая допустимая точность (остановка по eps).
MAX_EPS = 0.0001
# Предел числа повторений цикла, число шагов которого заранее неизвестно.
MAX_ITERATIONS = 100000

# Количество знаков после запятой в сумме, получается из MAX_EPS.
DIGITS = math.ceil(-math.log10(MAX_EPS))


def term_sqplus(n):
    """Модуль n-го слагаемого ряда sqplus: 1 / (n^2 + 1)."""
    return 1 / (n * n + 1)


def term_third(n):
    """Модуль n-го слагаемого ряда third: 1 / (3 * n)."""
    return 1 / (3 * n)


# Таблица рядов: имя -> (функция слагаемого, текст формулы для вывода).
FORMULAS = {
    "sqplus": (term_sqplus, "S = 1/(1^2+1) - 1/(2^2+1) + 1/(3^2+1) - ..."),
    "third": (term_third, "S = 1/3 - 1/6 + 1/9 - 1/12 + ..."),
}


def apply_sign(n, value):
    """Расставляет знак: нечётное слагаемое со знаком +, чётное со знаком -."""
    if n % 2 == 1:
        return value
    return -value


def sum_by_count(term, count):
    """Сумма первых count слагаемых ряда.

    term - функция, возвращающая модуль n-го слагаемого.
    Возвращает кортеж (сумма, количество слагаемых).
    Если count вне диапазона 1..MAX_TERMS, вызывает ValueError.
    """
    if count < 1 or count > MAX_TERMS:
        raise ValueError(
            f"количество слагаемых должно быть от 1 до {MAX_TERMS}"
        )
    result = 0.0
    for n in range(1, count + 1):
        result += apply_sign(n, term(n))
    return result, count


def sum_by_eps(term, eps):
    """Суммирует ряд, пока модуль слагаемого не станет меньше eps.

    Слагаемое, которое оказалось меньше eps, считается последним
    и входит в сумму.
    term - функция, возвращающая модуль n-го слагаемого.
    Возвращает кортеж (сумма, количество слагаемых).
    Если eps вне диапазона (0; MAX_EPS] или за MAX_ITERATIONS шагов
    точность не достигнута, вызывает ValueError.
    """
    if not (0 < eps <= MAX_EPS):
        raise ValueError(
            f"точность должна быть больше 0 и не больше {MAX_EPS}"
        )
    result = 0.0
    for n in range(1, MAX_ITERATIONS + 1):
        value = term(n)
        result += apply_sign(n, value)
        if abs(value) < eps:
            return result, n
    raise ValueError(
        f"точность не достигнута за {MAX_ITERATIONS} шагов"
    )