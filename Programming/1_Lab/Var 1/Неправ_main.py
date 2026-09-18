"""
Решение "в лоб" с помощью вложенных циклов:

Функция ищет пару минимальных индексов из списка lst,
значение под которыми в сумме даёт target
"""
def two_sum(l: list, t: int) -> tuple:
    if len(l) > 1:  # проверка возможности нахождения хотя бы 2-х любых различных индексов
        for i in range(0, len(l) - 1):  # (1)
            for j in range(i + 1, len(l)):  # (2), i+1 => без повторных обращений к элементам
                if l[i] + l[j] == t:  # основное условие задачи
                    return i, j  # кортеж с ответом - пара индексов списка
    return tuple()  # пустой кортеж, если не нашли индексы

lst = [3, 3, 1, 3, 1]
target = 4
print(two_sum(lst, target))  # (0, 2)


"""
Усложнение 1: Оптимизация вычислительной сложности.

Функция работает со словарём из списка lst, выполняет поиск 1 пары индексов,
но уже с вычислительной сложностью ниже O(n^2)
"""
def two_sum_hashed(l: list, t: int) -> tuple:
    d = dict()  # Создадим и заполним словарь из lst
    for i in range(len(l)):
        d[str(i)] = l[i]  # index -> key

    # Создадим список, в который запишем нужные значения
    term = []
    for a in d.values():
        b = t - a  # находим парное слагаемое для текущего значения
        if b in d.values():  # ищем его в значениях
            term = [a, b]
            break  # нашли первую пару => выход

    #Подбираем пару ключей по списку найденных значений
    res = list()
    if len(term) > 0:  # только если нашли подходящую пару
        for key in d.keys():  # сопоставим 1-е значение ключу
            if d[key] == term[0]:
                res.append(int(key))
                break
        for key in d.keys():  # сопоставим 2-е значение ключу
            if d[key] == term[1] and int(key) not in res:
                res.append(int(key))
                break
    return tuple(res)

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 8
print(two_sum_hashed(lst, target))  # (0, 6)


"""
Усложнение 2: нахождение всех пар индексов.

Функция записывает все пары в список кортежей, начиная с минимальных
"""
def two_sum_all(l: list, t: int) -> tuple:  # см: Решение "в лоб"
    res = list()
    if len(l) > 1:
        for i in range(0, len(l) - 1):
            for j in range(i + 1, len(l)):
                if l[i] + l[j] == t:
                    res.append((i, j))  # Добавляем элемент-кортеж из индексов
    return res

lst = [3, 3, 1, 3, 1]
target = 4
print(two_sum_all(lst, target))  # [(0, 2), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)]
