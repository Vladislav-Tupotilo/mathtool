"""Работа с массивами целых чисел: константы, генерация, проверки, поиск.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
"""

import random

# Границы значений элементов массива.
MIN_VALUE = -100
MAX_VALUE = 100
# Наибольшее допустимое количество элементов.
MAX_COUNT = 1_000_000
# Наибольший допустимый модуль искомого значения.
MAX_SEARCH = 1000


def check_count(count):
    """Проверяет количество элементов: от 1 до MAX_COUNT.

    При нарушении вызывает ValueError.
    """
    if not 1 <= count <= MAX_COUNT:
        raise ValueError(f"количество элементов вне диапазона 1..{MAX_COUNT}")


def check_bounds(low, high):
    """Проверяет границы значений для генерации.

    Обе границы должны лежать в диапазоне MIN_VALUE..MAX_VALUE,
    нижняя граница не больше верхней. При нарушении вызывает ValueError.
    """
    if not MIN_VALUE <= low <= MAX_VALUE or not MIN_VALUE <= high <= MAX_VALUE:
        raise ValueError(
            f"границы значений вне диапазона {MIN_VALUE}..{MAX_VALUE}"
        )
    if low > high:
        raise ValueError("нижняя граница больше верхней")


def fill_array(count, low=MIN_VALUE, high=MAX_VALUE, seed=None):
    """Создаёт список из count случайных целых чисел от low до high.

    Границы low и high входят в диапазон. При одинаковых параметрах и
    заданном seed результат повторяется; если seed равен None,
    последовательность каждый раз новая.
    """
    random.seed(seed)
    result = []
    for _ in range(count):
        result.append(random.randint(low, high))
    return result


def parse_array(text):
    """Превращает текст в список целых чисел и проверяет его.

    Числа разделяются пробельными символами и запятыми.
    Если чисел нет или их больше MAX_COUNT, значение не целое число
    либо выходит за MIN_VALUE..MAX_VALUE, вызывает ValueError.
    """
    # Запятые заменяем пробелами, затем режем текст на слова.
    tokens = text.replace(",", " ").split()
    check_count(len(tokens))

    result = []
    for token in tokens:
        try:
            value = int(token)
        except ValueError:
            raise ValueError(f"{token} не является целым числом")
        if not MIN_VALUE <= value <= MAX_VALUE:
            raise ValueError(
                f"значение {value} вне диапазона {MIN_VALUE}..{MAX_VALUE}"
            )
        result.append(value)
    return result


def check_search_value(value):
    """Проверяет искомое значение: модуль не больше MAX_SEARCH.

    При нарушении вызывает ValueError.
    """
    if abs(value) > MAX_SEARCH:
        raise ValueError(
            f"искомое значение вне диапазона {-MAX_SEARCH}..{MAX_SEARCH}"
        )


def check_ascending(array):
    """Проверяет, что каждый элемент не больше следующего.

    Если порядок по возрастанию нарушен, вызывает ValueError.
    """
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            raise ValueError("массив не упорядочен по возрастанию")


def binary_search(array, value):
    """Ищет value в массиве, упорядоченном по возрастанию.

    Возвращает индекс найденного элемента (с нуля) или None, если
    значения в массиве нет. При повторах возвращает любое вхождение.
    """
    left = 0
    right = len(array) - 1
    while left <= right:
        middle = (left + right) // 2
        if array[middle] == value:
            return middle
        if array[middle] < value:
            left = middle + 1
        else:
            right = middle - 1
    return None