import time
from calc.arrays import fill_array
from calc.sorting import METHODS

SIZES = [1000, 10000, 20000]

# Создаем базовый список с помощью твоей функции (сразу 20000 элементов)
# seed=1 гарантирует, что числа будут одинаковыми при каждом запуске
base_list = fill_array(20000, seed=1)

# Вывод заголовка таблицы
print(" " * 12, end="")
for size in SIZES:
    print(f"{size:<15}", end="")
print()

# Запуск тестов
for name, func in METHODS.items():
    print(f"{name + ':':<12}", end="")
    for size in SIZES:
        # Берем нужный кусок и делаем копию
        arr = base_list[:size].copy()
        
        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()
        
        print(f"{round(end - start, 6):<15}", end="")
    print()