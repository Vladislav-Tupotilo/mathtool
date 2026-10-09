"""Численное интегрирование методом левых прямоугольников.

В модуле только расчёты: ввода, вывода и завершения программы здесь нет.
Подынтегральная функция передаётся функции интегрирования параметром.
"""

import math

# Наибольшее допустимое число шагов интегрирования.
MAX_STEPS = 100000
# Количество знаков после запятой в значении интеграла.
RESULT_DIGITS = 4


def f_ratio(x):
    """Подынтегральная функция ratio: x / (x + 1)."""
    return x / (x + 1)


def f_root(x):
    """Подынтегральная функция root: sqrt(x^2 + 1)."""
    return math.sqrt(x * x + 1)


# Таблица функций: имя -> (функция, текст формулы для вывода,
# нижняя граница промежутка, верхняя граница промежутка,
# True - границы промежутка допустимы, False - недопустимы).
FUNCTIONS = {
    "ratio": (f_ratio, "F(x) = x / (x + 1)", 0, 20, True),
    "root": (f_root, "F(x) = sqrt(x^2 + 1)", -5, 5, False),
}


def in_interval(x, low, high, inclusive):
    """Проверяет, лежит ли x в промежутке между low и high.

    Если inclusive равно True, границы входят в промежуток, иначе нет.
    """
    if inclusive:
        return low <= x <= high
    return low < x < high


def check_limits(a, b, low, high, inclusive):
    """Проверяет пределы интегрирования a и b.

    Оба предела должны быть конечными, b должно быть больше a,
    и оба предела должны лежать в промежутке функции.
    При нарушении вызывает ValueError.
    """
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError("пределы интегрирования должны быть конечными числами")
    if not a < b:
        raise ValueError("верхний предел должен быть больше нижнего")
    if not (in_interval(a, low, high, inclusive)
            and in_interval(b, low, high, inclusive)):
        if inclusive:
            left, right = "[", "]"
        else:
            left, right = "(", ")"
        raise ValueError(
            f"пределы интегрирования вне промежутка {left}{low}; {high}{right}"
        )


def integrate(func, a, b, steps):
    """Интеграл func от a до b методом левых прямоугольников.

    func - подынтегральная функция одного аргумента.
    steps - число шагов, от 1 до MAX_STEPS; иначе вызывает ValueError.
    Пределы предполагаются уже проверенными (check_limits).
    """
    if steps < 1 or steps > MAX_STEPS:
        raise ValueError(f"количество шагов должно быть от 1 до {MAX_STEPS}")
    dx = (b - a) / steps
    result = 0.0
    for i in range(steps):
        x = a + i * dx
        result += func(x) * dx
    return result