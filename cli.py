"""Разбор параметров командной строки для mathtool."""

import argparse

from calc.integration import FUNCTIONS
from calc.series import FORMULAS
from calc.arrays import MAX_VALUE, MIN_VALUE
from calc.sorting import METHODS


def build_parser():
    """Создаёт и возвращает разборщик командной строки (ArgumentParser).

    Разбор идёт в два этапа: сначала определяется имя команды,
    затем разбираются параметры именно этой команды.
    Сокращения имён параметров отключены (allow_abbrev=False).
    """
    parser = argparse.ArgumentParser(
        prog="mathtool",
        description="mathtool - решение уравнений и обработка числовых рядов",
        allow_abbrev=False,
    )
    # required=True не указываем: запуск без команды выводит справку.
    subparsers = parser.add_subparsers(dest="command")

    # --- команда solve ---
    solve_parser = subparsers.add_parser(
        "solve",
        help="решение уравнения A*x^2 + B*x + C = 0",
        allow_abbrev=False,
    )
    solve_parser.add_argument("-a", type=int, help="коэффициент A")
    solve_parser.add_argument("-b", type=int, help="коэффициент B")
    solve_parser.add_argument("-c", type=int, help="коэффициент C")

    # --- команда stats ---
    stats_parser = subparsers.add_parser(
        "stats",
        help="статистика последовательности чисел",
        allow_abbrev=False,
    )
    stats_parser.add_argument(
        "--input", help="имя файла с числами (без параметра - ввод с stdin)"
    )

    # --- команда series ---
    series_parser = subparsers.add_parser(
        "series",
        help="сумма знакочередующегося ряда",
        allow_abbrev=False,
    )
    series_parser.add_argument(
        "--func",
        required=True,
        choices=sorted(FORMULAS),
        help="имя ряда",
    )
    # Ровно один из двух способов остановки.
    stop_group = series_parser.add_mutually_exclusive_group(required=True)
    stop_group.add_argument(
        "--terms", type=int, help="остановка по количеству слагаемых"
    )
    stop_group.add_argument(
        "--eps", type=float, help="остановка по точности"
    )

    # --- команда integrate ---
    integrate_parser = subparsers.add_parser(
        "integrate",
        help="численное интегрирование (левые прямоугольники)",
        allow_abbrev=False,
    )
    integrate_parser.add_argument(
        "--func",
        required=True,
        choices=sorted(FUNCTIONS),
        help="имя подынтегральной функции",
    )
    # from - ключевое слово Python, поэтому атрибут называется lower.
    integrate_parser.add_argument(
        "--from", dest="lower", type=float, required=True,
        help="нижний предел интегрирования",
    )
    integrate_parser.add_argument(
        "--to", dest="upper", type=float, required=True,
        help="верхний предел интегрирования",
    )
    integrate_parser.add_argument(
        "--steps", type=int, required=True, help="число шагов"
    )

        # --- команда fill ---
    fill_parser = subparsers.add_parser(
        "fill", help="создание массива случайных чисел", allow_abbrev=False,
    )
    fill_parser.add_argument(
        "-c", "--count", type=int, required=True,
        help="количество элементов, от 1 до 1000000",
    )
    fill_parser.add_argument(
        "--min", type=int, default=MIN_VALUE,
        help="нижняя граница значений (по умолчанию %(default)s)",
    )
    fill_parser.add_argument(
        "--max", type=int, default=MAX_VALUE,
        help="верхняя граница значений (по умолчанию %(default)s)",
    )
    fill_parser.add_argument(
        "--seed", type=int, help="начальное значение генератора"
    )
    fill_parser.add_argument(
        "-o", "--output", help="файл для массива (без параметра - на экран)"
    )

    # --- команда sort ---
    sort_parser = subparsers.add_parser(
        "sort", help="сортировка массива", allow_abbrev=False,
    )
    sort_parser.add_argument(
        "-m", "--method", required=True, choices=sorted(METHODS),
        help="метод сортировки",
    )
    sort_parser.add_argument(
        "--order", choices=["asc", "desc"], default="asc",
        help="asc - по возрастанию, desc - по убыванию",
    )
    sort_parser.add_argument(
        "-i", "--input", help="файл с массивом (без параметра - с клавиатуры)"
    )
    sort_parser.add_argument(
        "-o", "--output", help="файл для результата (без параметра - на экран)"
    )

    # --- команда search ---
    search_parser = subparsers.add_parser(
        "search", help="двоичный поиск в массиве по возрастанию",
        allow_abbrev=False,
    )
    search_parser.add_argument(
        "-v", "--value", type=int, required=True, help="искомое число"
    )
    search_parser.add_argument(
        "-i", "--input", help="файл с массивом (без параметра - с клавиатуры)"
    )

    return parser