"""Статистика числовой последовательности.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
Каждый показатель - отдельная функция: принимает список чисел и возвращает
число либо None, если показатель не существует.
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
        raise ValueError("нет данных: не указано ни одного числа")
    if len(tokens) > MAX_COUNT:
        raise ValueError(f"слишком много чисел (не более {MAX_COUNT})")

    numbers = []
    for token in tokens:
        try:
            value = float(token)
        except ValueError:
            raise ValueError(f"'{token}' не является числом")
        if not math.isfinite(value):
            raise ValueError(f"'{token}' не является конечным числом")
        if abs(value) > MAX_ABS:
            raise ValueError(f"значение вне допустимого диапазона: '{token}'")
        numbers.append(value)
    return numbers


def total(numbers):
    """1. Сумма A1 + A2 + ... + AN."""
    return sum(numbers)


def mean(numbers):
    """2. Среднее арифметическое: сумма / N. None, если чисел нет."""
    if len(numbers) == 0:
        return None
    return total(numbers) / len(numbers)


def sum_squares(numbers):
    """3. Сумма квадратов A1^2 + A2^2 + ... + AN^2."""
    result = 0.0
    for x in numbers:
        result += x * x
    return result


def root_mean_square(numbers):
    """4. Среднее квадратическое: корень из (сумма квадратов / N)."""
    if len(numbers) == 0:
        return None
    return math.sqrt(sum_squares(numbers) / len(numbers))


def squared_deviations_sum(numbers):
    """Вспомогательная: сумма (Ai - среднее)^2, считается в два прохода.

    Первый проход - среднее, второй - сумма квадратов отклонений.
    Для пустого списка возвращает None.
    """
    m = mean(numbers)
    if m is None:
        return None
    result = 0.0
    for x in numbers:
        result += (x - m) ** 2
    return result


def variance(numbers):
    """5. Дисперсия: сумма (Ai - среднее)^2 / N."""
    s = squared_deviations_sum(numbers)
    if s is None:
        return None
    return s / len(numbers)


def standard_deviation_pop(numbers):
    """6. СКО: корень из дисперсии."""
    v = variance(numbers)
    if v is None:
        return None
    return math.sqrt(v)


def standard_deviation_sample(numbers):
    """7. Стандартное отклонение: корень из (сумма (Ai - среднее)^2 / (N - 1)).

    При N < 2 не существует: возвращает None.
    """
    if len(numbers) < 2:
        return None
    s = squared_deviations_sum(numbers)
    return math.sqrt(s / (len(numbers) - 1))


def minimum(numbers):
    """8. Наименьшее число. None, если чисел нет."""
    if len(numbers) == 0:
        return None
    return min(numbers)


def maximum(numbers):
    """9. Наибольшее число. None, если чисел нет."""
    if len(numbers) == 0:
        return None
    return max(numbers)


def count_positive(numbers):
    """10. Количество положительных чисел (больше нуля)."""
    count = 0
    for x in numbers:
        if x > 0:
            count += 1
    return count


def count_negative(numbers):
    """11. Количество отрицательных чисел (меньше нуля)."""
    count = 0
    for x in numbers:
        if x < 0:
            count += 1
    return count


# Таблица показателей: подпись строки -> функция расчёта.
# Порядок строк в таблице - это порядок вывода.
REPORT = {
    "Сумма": total,
    "Ср. арифм.": mean,
    "Сумма кв.": sum_squares,
    "Ср. кв.": root_mean_square,
    "Дисперсия": variance,
    "СКО": standard_deviation_pop,
    "Станд. откл.": standard_deviation_sample,
    "Наименьшее": minimum,
    "Наибольшее": maximum,
    "Положительных": count_positive,
    "Отрицательных": count_negative,
}