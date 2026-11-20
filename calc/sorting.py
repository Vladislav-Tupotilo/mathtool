"""Сортировки списка целых чисел: пузырёк, выбор, вставки, подсчёт.

Каждая сортировка изменяет переданный список и возвращает None.
Параметр descending=True задаёт порядок по убыванию.
Встроенные sort и sorted здесь не используются.
"""

from calc.arrays import MAX_VALUE, MIN_VALUE


def out_of_order(a, b, descending):
    """Возвращает True, если пара a, b (a стоит левее) стоит не по порядку."""
    if descending:
        return a < b
    return a > b


def bubble_sort(array, descending=False):
    """Сортировка пузырьком с досрочным выходом, если обменов не было."""
    n = len(array)
    for i in range(n - 1):
        swapped = False
        # После каждого прохода самый "тяжёлый" элемент встаёт на место,
        # поэтому внутренний цикл с каждым проходом короче.
        for j in range(n - 1 - i):
            if out_of_order(array[j], array[j + 1], descending):
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
                swapped = True
        if not swapped:
            break


def selection_sort(array, descending=False):
    """Сортировка выбором: на место i ставится лучший из оставшихся."""
    n = len(array)
    for i in range(n - 1):
        best = i
        # Ищем в хвосте списка элемент, который должен стоять первым.
        for j in range(i + 1, n):
            if out_of_order(array[best], array[j], descending):
                best = j
        temp = array[i]
        array[i] = array[best]
        array[best] = temp


def insertion_sort(array, descending=False):
    """Сортировка вставками: каждый элемент вставляется в готовую часть."""
    n = len(array)
    for i in range(1, n):
        current = array[i]
        j = i
        # Сдвигаем вправо элементы, которые должны стоять после current.
        while j > 0 and out_of_order(array[j - 1], current, descending):
            array[j] = array[j - 1]
            j = j - 1
        array[j] = current


def counting_sort(array, descending=False):
    """Сортировка подсчётом для значений от MIN_VALUE до MAX_VALUE.

    Считает, сколько раз встретилось каждое значение, затем
    записывает значения обратно в нужном порядке.
    """
    size = MAX_VALUE - MIN_VALUE + 1
    counters = []
    for _ in range(size):
        counters.append(0)

    # Подсчёт: значение смещается на MIN_VALUE, чтобы получить номер счётчика.
    for value in array:
        counters[value - MIN_VALUE] += 1

    # Обход счётчиков: слева направо, а при descending справа налево.
    k = 0
    for step in range(size):
        if descending:
            index = size - 1 - step
        else:
            index = step
        for _ in range(counters[index]):
            array[k] = index + MIN_VALUE
            k = k + 1


# Таблица сортировок: имя метода -> функция.
METHODS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "counting": counting_sort,
}