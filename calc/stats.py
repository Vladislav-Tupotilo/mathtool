"""Статистика числовой последовательности.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
Каждый показатель - отдельная функция: принимает непустой список чисел
и возвращает число либо None, если показатель не существует.
"""

import math

# Наибольшее допустимое количество чисел.
MAX_COUNT = 20
# Наибольшее допустимое значение числа по модулю.
MAX_ABS = 10000


def parse_numbers(text):
    """Превращает текст в список чисел и проверяет их.

    Числа в тексте разделяются пробелами или переводами строк.
    Возвращает список вещественных чисел.
    Если чисел нет, их больше MAX_COUNT, значение не число, не конечное
    или по модулю больше MAX_ABS, вызывает ValueError.
    """
    tokens = text.split()
    if len(tokens) == 0:
        raise ValueError("последовательность пуста")
    if len(tokens) > MAX_COUNT:
        raise ValueError(f"чисел больше {MAX_COUNT}")

    numbers = []
    for token in tokens:
        try:
            value = float(token)
        except ValueError:
            raise ValueError(f"{token} не является числом")
        if not math.isfinite(value):
            raise ValueError(f"{token} не является конечным числом")
        if abs(value) > MAX_ABS:
            raise ValueError(f"{token} по модулю больше {MAX_ABS}")
        numbers.append(value)
    return numbers


def count_numbers(numbers):
    """0. Количество чисел."""
    return len(numbers)


def total(numbers):
    """1. Сумма A1 + A2 + ... + AN."""
    result = 0
    for x in numbers:
        result += x
    return result


def mean(numbers):
    """2. Среднее арифметическое: сумма / N."""
    return total(numbers) / len(numbers)


def sum_squares(numbers):
    """3. Сумма квадратов A1^2 + A2^2 + ... + AN^2."""
    result = 0
    for x in numbers:
        result += x ** 2
    return result


def root_mean_square(numbers):
    """4. Среднее квадратическое: корень из (сумма квадратов / N)."""
    return math.sqrt(sum_squares(numbers) / len(numbers))


def squared_deviations_sum(numbers):
    """Вспомогательная: сумма (Ai - среднее)^2, считается в два прохода.

    Первый проход - среднее, второй - сумма квадратов отклонений.
    """
    m = mean(numbers)
    result = 0
    for x in numbers:
        result += (x - m) ** 2
    return result


def variance(numbers):
    """5. Дисперсия: сумма (Ai - среднее)^2 / N."""
    return squared_deviations_sum(numbers) / len(numbers)


def standard_deviation_pop(numbers):
    """6. СКО: корень из дисперсии."""
    return math.sqrt(variance(numbers))


def standard_deviation_sample(numbers):
    """7. Стандартное отклонение: корень из (сумма (Ai - среднее)^2 / (N - 1)).

    При N < 2 не существует: возвращает None.
    """
    if len(numbers) < 2:
        return None
    return math.sqrt(squared_deviations_sum(numbers) / (len(numbers) - 1))


def minimum(numbers):
    """8. Наименьшее число."""
    result = numbers[0]
    for x in numbers:
        if x < result:
            result = x
    return result


def maximum(numbers):
    """9. Наибольшее число."""
    result = numbers[0]
    for x in numbers:
        if x > result:
            result = x
    return result


def count_positive(numbers):
    """10. Количество положительных чисел (больше нуля)."""
    result = 0
    for x in numbers:
        if x > 0:
            result += 1
    return result


def count_negative(numbers):
    """11. Количество отрицательных чисел (меньше нуля)."""
    result = 0
    for x in numbers:
        if x < 0:
            result += 1
    return result


# Таблица вывода: (подпись, функция расчёта, формат значения).
# Порядок строк в таблице - это порядок вывода.
REPORT = [
    ("Количество", count_numbers, "d"),
    ("Сумма", total, ".3f"),
    ("Ср. арифм.", mean, ".3f"),
    ("Сумма кв.", sum_squares, ".3f"),
    ("Ср. кв.", root_mean_square, ".3f"),
    ("Дисперсия", variance, ".3f"),
    ("СКО", standard_deviation_pop, ".3f"),
    ("Станд. откл.", standard_deviation_sample, ".3f"),
    ("Наименьшее", minimum, ".3f"),
    ("Наибольшее", maximum, ".3f"),
    ("Положительных", count_positive, "d"),
    ("Отрицательных", count_negative, "d"),
]