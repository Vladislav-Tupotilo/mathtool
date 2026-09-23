import sys
import math

MAX_VALUE = 10000


def read_coefficient(name):
    """Запрашивает коэффициент с клавиатуры, преобразует в int и проверяет диапазон."""
    raw = input(f"Введите {name}: ")
    try:
        value = int(raw)
    except ValueError:
        print("ОШИБКА: коэффициент не является целым числом", file=sys.stderr)
        sys.exit(1)
    if abs(value) > MAX_VALUE:
        print("ОШИБКА: значение вне допустимого диапазона", file=sys.stderr)
        sys.exit(1)
    return value


# --- 1. Разбор параметров командной строки ---
args = sys.argv[1:]

if len(args) == 0 or args[0] == "--help":
    print("mathtool – решение уравнений вида A*x^2 + B*x + C = 0")
    print()
    print("Использование:")
    print("  python mathtool.py                        вывод справки")
    print("  python mathtool.py --help                 вывод справки")
    print("  python mathtool.py solve                  ввод коэффициентов с клавиатуры")
    print("  python mathtool.py solve -a 1 -b -3 -c 2  решение с заданными коэффициентами")
    sys.exit(0)

if args[0] != "solve":
    print("ОШИБКА: неизвестная команда", file=sys.stderr)
    sys.exit(1)

# --- 2. Получение исходных данных ---
if len(args) == 1:
    a = read_coefficient("A")
    b = read_coefficient("B")
    c = read_coefficient("C")
elif len(args) == 7:
    if args[1] != "-a" or args[3] != "-b" or args[5] != "-c":
        print("ОШИБКА: неизвестный параметр", file=sys.stderr)
        sys.exit(1)
    raw_a = args[2]
    raw_b = args[4]
    raw_c = args[6]

    try:
        a = int(raw_a)
        b = int(raw_b)
        c = int(raw_c)
    except ValueError:
        print("ОШИБКА: коэффициент не является целым числом", file=sys.stderr)
        sys.exit(1)
    if max(abs(a), abs(b), abs(c)) > MAX_VALUE:
        print("ОШИБКА: значение вне допустимого диапазона", file=sys.stderr)
        sys.exit(1)
else:
    print("ОШИБКА: неверный набор параметров", file=sys.stderr)
    sys.exit(1)

# --- 3. Определение вида уравнения и решение ---
if a == 0:
    if b != 0:
        print("Уравнение линейное")
        x = -c / b
        print(f"x = {x:.3f}")
    else:
        print("ОШИБКА: это не уравнение, неизвестное отсутствует", file=sys.stderr)
        sys.exit(1)
else:
    print("Уравнение квадратное")
    d = b * b - 4 * a * c
    print(f"D = {d}")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")

sys.exit(0)