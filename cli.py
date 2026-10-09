"""Разбор параметров командной строки для mathtool."""

import argparse

from calc.integration import FUNCTIONS
from calc.series import FORMULAS


def build_parser():
    """Создаёт и возвращает разборщик командной строки (ArgumentParser).

    Разбор идёт в два этапа: сначала определяется имя команды,
    затем разбираются параметры именно этой команды.
    """
    parser = argparse.ArgumentParser(
        prog="mathtool",
        description="mathtool - решение уравнений и обработка числовых рядов",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- команда solve ---
    solve_parser = subparsers.add_parser(
        "solve", help="решение уравнения A*x^2 + B*x + C = 0"
    )
    solve_parser.add_argument("-a", type=int, help="коэффициент A")
    solve_parser.add_argument("-b", type=int, help="коэффициент B")
    solve_parser.add_argument("-c", type=int, help="коэффициент C")

    # --- команда stats ---
    stats_parser = subparsers.add_parser(
        "stats", help="статистика последовательности чисел"
    )
    stats_parser.add_argument(
        "--input", help="имя файла с числами (без параметра - ввод с stdin)"
    )

    # --- команда series ---
    series_parser = subparsers.add_parser(
        "series", help="сумма знакочередующегося ряда"
    )
    series_parser.add_argument(
        "--func",
        required=True,
        choices=list(FORMULAS),
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
        "integrate", help="численное интегрирование (левые прямоугольники)"
    )
    integrate_parser.add_argument(
        "--func",
        required=True,
        choices=list(FUNCTIONS),
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

    return parser