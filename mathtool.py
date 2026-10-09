"""mathtool - решение уравнений и обработка числовых рядов.

Точка входа программы. Весь ввод-вывод и завершение программы
находятся здесь; расчёты вынесены в пакет calc.
"""

import sys

from calc.equation import check_coefficient, solve_equation
from calc.integration import FUNCTIONS, RESULT_DIGITS, check_limits, integrate
from calc.series import DIGITS, FORMULAS, sum_by_count, sum_by_eps
from calc.stats import REPORT, parse_numbers
from cli import build_parser

# Текст для показателя, который невозможно вычислить.
NOT_EXISTS = "НЕ СУЩЕСТВУЕТ"


def print_error(message):
    """Печатает сообщение об ошибке в stderr."""
    print(f"ОШИБКА: {message}", file=sys.stderr)


def read_coefficient(name):
    """Запрашивает коэффициент с клавиатуры.

    Возвращает целое число. Если ввод неверный, вызывает ValueError.
    """
    raw = input(f"Введите {name}: ")
    try:
        value = int(raw)
    except ValueError:
        raise ValueError("коэффициент не является целым числом")
    check_coefficient(value)
    return value


def read_text(filename):
    """Читает текст из файла, а если имя не задано (None), из stdin.

    Возвращает прочитанный текст. При ошибке чтения вызывает ValueError.
    """
    if filename is None:
        return sys.stdin.read()
    try:
        with open(filename, encoding="utf-8-sig") as f:
            return f.read()
    except OSError:
        raise ValueError(f"не удалось открыть файл '{filename}'")
    except UnicodeDecodeError:
        raise ValueError(f"файл '{filename}' не является текстом в UTF-8")


def format_value(value):
    """Превращает значение показателя в текст для вывода.

    None -> "НЕ СУЩЕСТВУЕТ", целое -> как есть, дробное -> 3 знака.
    """
    if value is None:
        return NOT_EXISTS
    if isinstance(value, int):
        return str(value)
    return f"{value:.3f}"


def handle_solve(args):
    """Команда solve. Возвращает код возврата: 0 - успех, 1 - ошибка."""
    try:
        if args.a is None and args.b is None and args.c is None:
            # Параметров нет: спрашиваем коэффициенты с клавиатуры.
            a = read_coefficient("A")
            b = read_coefficient("B")
            c = read_coefficient("C")
        elif args.a is None or args.b is None or args.c is None:
            # Указана только часть параметров.
            raise ValueError("неверный набор параметров")
        else:
            a, b, c = args.a, args.b, args.c
            for value in (a, b, c):
                check_coefficient(value)
        kind, d, roots = solve_equation(a, b, c)
    except ValueError as e:
        print_error(str(e))
        return 1

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
    """Команда stats. Возвращает код возврата: 0 - успех, 1 - ошибка."""
    try:
        text = read_text(args.input)
        numbers = parse_numbers(text)
    except ValueError as e:
        print_error(str(e))
        return 1

    print(f"Количество: {len(numbers)}")
    for label, function in REPORT.items():
        value = function(numbers)
        print(f"{label}: {format_value(value)}")
    return 0


def handle_series(args):
    """Команда series. Возвращает код возврата: 0 - успех, 1 - ошибка."""
    term, formula_text = FORMULAS[args.func]
    try:
        if args.terms is not None:
            result, count = sum_by_count(term, args.terms)
        else:
            result, count = sum_by_eps(term, args.eps)
    except ValueError as e:
        print_error(str(e))
        return 1

    # Вывод только после успешного расчёта: ошибка печатается раньше формулы.
    print(formula_text)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{DIGITS}f}")
    return 0


def handle_integrate(args):
    """Команда integrate. Возвращает код возврата: 0 - успех, 1 - ошибка."""
    function, formula_text, low, high, inclusive = FUNCTIONS[args.func]
    try:
        check_limits(args.lower, args.upper, low, high, inclusive)
        result = integrate(function, args.lower, args.upper, args.steps)
    except ValueError as e:
        print_error(str(e))
        return 1

    # Вывод только после успешного расчёта: ошибка печатается раньше формулы.
    print(formula_text)
    print(f"Значение интеграла: {result:.{RESULT_DIGITS}f}")
    return 0


# Таблица: имя команды -> функция-обработчик.
HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
}


def main():
    """Разбирает командную строку и запускает нужную команду.

    Возвращает код возврата программы.
    """
    parser = build_parser()
    if len(sys.argv) == 1:
        # Запуск без параметров: справка, как в ЛР1.
        parser.print_help()
        return 0
    args = parser.parse_args()
    handler = HANDLERS[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())