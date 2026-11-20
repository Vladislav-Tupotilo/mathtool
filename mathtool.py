"""mathtool - решение уравнений и обработка числовых рядов.

Точка входа программы. Весь ввод-вывод и завершение программы
находятся здесь; расчёты вынесены в пакет calc.
"""

import sys
import time

from calc.arrays import (
    binary_search,
    check_ascending,
    check_bounds,
    check_count,
    check_search_value,
    fill_array,
    parse_array,
)
from calc.equation import check_coefficients, solve_equation
from calc.integration import FUNCTIONS, RESULT_DIGITS, check_limits, integrate, check_steps
from calc.series import DIGITS, FORMULAS, sum_by_count, sum_by_eps, check_eps, check_terms
from calc.sorting import METHODS
from calc.stats import REPORT, parse_numbers
from cli import build_parser

# Текст для показателя, который невозможно вычислить.
NOT_EXISTS = "НЕ СУЩЕСТВУЕТ"


def print_error(message):
    """Печатает сообщение об ошибке в поток ошибок (stderr)."""
    print(f"ОШИБКА: {message}", file=sys.stderr)


def read_coefficient(name):
    """Запрашивает коэффициент с клавиатуры и проверяет его.

    Возвращает целое число. Если ввод неверный, вызывает ValueError.
    """
    raw = input(f"Введите {name}: ")
    try:
        value = int(raw)
    except ValueError:
        raise ValueError("коэффициент не является целым числом")
    check_coefficients({name: value})
    return value

def read_lines_with_input():
    """Читает строки функцией input(), пока не встретится пустая строка.

    Пустой считается и строка из одних пробелов. Конец ввода (например,
    при передаче данных через конвейер) тоже завершает чтение.
    Возвращает все прочитанные строки одним текстом.
    """
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def read_file(filename):
    """Читает весь текстовый файл. При ошибке чтения вызывает ValueError."""
    try:
        with open(filename, encoding="utf-8-sig") as handle:
            return handle.read()
    except OSError:
        raise ValueError("файл не открывается")
    except UnicodeDecodeError:
        raise ValueError("файл не является текстом в UTF-8")


def read_text(filename):
    """Читает текст из файла, а если имя не задано (None), с клавиатуры.

    Если filename равен None - читает строки через input() до пустой строки.
    Возвращает прочитанный текст. При ошибке чтения вызывает ValueError.
    """
    if filename is None:
        return read_lines_with_input()
    return read_file(filename)  


def handle_solve(args):
    """Команда solve. Возвращает код возврата 0."""
    if args.a is None and args.b is None and args.c is None:
        # Параметров нет: спрашиваем коэффициенты с клавиатуры.
        a = read_coefficient("A")
        b = read_coefficient("B")
        c = read_coefficient("C")
    elif args.a is None or args.b is None or args.c is None:
        # Указана только часть коэффициентов.
        raise ValueError("укажите все три коэффициента либо ни одного")
    else:
        a, b, c = args.a, args.b, args.c
        check_coefficients({"A": a, "B": b, "C": c})

    kind, d, roots = solve_equation(a, b, c)

    if kind == "linear":
        print("Уравнение линейное")
        print(f"x = {roots[0]:.3f}")
    else:
        print("Уравнение квадратное")
        print(f"D = {d}")
        if len(roots) == 2:
            print(f"x1 = {roots[0]:.3f}")
            print(f"x2 = {roots[1]:.3f}")
        elif len(roots) == 1:
            print(f"x = {roots[0]:.3f}")
        else:
            print("Действительных корней нет")
    return 0


def handle_stats(args):
    """Команда stats. Возвращает код возврата 0."""
    numbers = parse_numbers(read_text(args.input))

    for label, function, form in REPORT:
        value = function(numbers)
        if value is None:
            print(f"{label}: {NOT_EXISTS}")
        else:
            print(f"{label}: {value:{form}}")
    return 0


def handle_series(args):
    """Команда series. Возвращает код возврата 0."""
    term, formula_text = FORMULAS[args.func]

    if args.terms is not None:
        check_terms(args.terms)
        result, count = sum_by_count(term, args.terms)
    else:
        check_eps(args.eps)
        result, count = sum_by_eps(term, args.eps)

    print(formula_text)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{DIGITS}f}")
    return 0


def handle_integrate(args):
    """Команда integrate. Возвращает код возврата 0."""
    function, formula_text, low, high, inclusive = FUNCTIONS[args.func]

    check_limits(args.lower, args.upper, low, high, inclusive)
    check_steps(args.steps)
    result = integrate(function, args.lower, args.upper, args.steps)

    print(formula_text)
    print(f"Значение интеграла: {result:.{RESULT_DIGITS}f}")
    return 0


def read_array(filename):
    """Читает массив целых чисел из файла или с клавиатуры.

    Возвращает список целых. При ошибке данных или чтения
    вызывает ValueError.
    """
    if filename is None:
        print("Введите числа (пустая строка завершает ввод):", file=sys.stderr)
        text = read_lines_with_input()
    else:
        text = read_file(filename)
    return parse_array(text)

def format_array(array):
    """Превращает список чисел в строку: числа через пробел."""
    words = []
    for x in array:
        words.append(str(x))
    return " ".join(words)


def write_array(array, filename):
    """Выводит массив на экран, а если задан filename, записывает в файл.

    При записи в файл печатает число записанных элементов и имя файла.
    """
    line = format_array(array)
    if filename is None:
        print(line)
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        raise ValueError("не удалось записать файл")
    print(f"Записано элементов: {len(array)} в файл {filename}")


def measure(name, operation, parameters):
    """Выполняет operation(*parameters) и печатает время в stderr.

    Возвращает результат операции.
    """
    start = time.perf_counter()
    result = operation(*parameters)
    elapsed = time.perf_counter() - start
    print(f"Время операции {name}: {elapsed:.6f} с", file=sys.stderr)
    return result

def handle_fill(args):
    """Команда fill. Возвращает код возврата 0; ошибки - исключения."""
    check_count(args.count)
    check_bounds(args.min, args.max)
    array = fill_array(args.count, args.min, args.max, args.seed)
    write_array(array, args.output)
    return 0


def handle_sort(args):
    """Команда sort. Возвращает код возврата 0; ошибки - исключения."""
    array = read_array(args.input)
    method = METHODS[args.method]
    descending = args.order == "desc"
    # Время измеряется только вокруг расчёта.
    measure(f"sort ({args.method})", method, [array, descending])
    write_array(array, args.output)
    print("Массив отсортирован.")
    return 0


def handle_search(args):
    """Команда search. Возвращает код возврата: 0 - найдено, 1 - нет."""
    check_search_value(args.value)
    array = read_array(args.input)
    check_ascending(array)
    index = binary_search(array, args.value)
    if index is None:
        print(f"Значение {args.value} не найдено.")
        return 1
    print(f"Значение {args.value} имеет элемент с индексом {index + 1}.")
    return 0



# Таблица: имя команды -> функция-обработчик.
HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
    "fill": handle_fill,
    "sort": handle_sort,
    "search": handle_search,
}


def main(argv):
    """Разбирает параметры argv и запускает нужную команду.

    argv - список параметров без имени программы (sys.argv[1:]).
    Возвращает код возврата программы.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        return HANDLERS[args.command](args)
    except (ValueError, OSError) as error:
        print_error(str(error))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))