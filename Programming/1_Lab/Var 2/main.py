import unittest

def two_sum(lst: list[int], target: int) -> None | tuple[int, int]:
    """
    Функция ищет пару минимальных индексов из списка lst,
    значение под которыми в сумме даёт target

    :param list lst: список значений для поиска суммы
    :param int target: целевое значение суммы двух элементов
    :return: результирующий кортеж из двух индексов

    >>> two_sum([3, 3, 1, 3, 1], 4)
    (0, 2)
    """
    if len(lst) > 1:  # проверка возможности нахождения хотя бы 2-х любых различных индексов
        for i in range(0, len(lst) - 1):  # (1)
            for j in range(i + 1, len(lst)):  # (2), i+1 => без повторных обращений к элементам
                if lst[i] + lst[j] == target:  # основное условие задачи
                    return i, j  # кортеж с ответом - пара индексов списка
    return None  # возвращаем None, если не нашли индексы


def two_sum_hashed(lst: list[int], target: int) -> None | uple[int, int]:
    """
    Функция работает со словарём из списка lst, выполняет поиск 1 пары индексов,
    но уже с вычислительной сложностью немного (очень маловероятно) ниже O(n^2)

    :param list lst: список значений для поиска суммы
    :param int target: целевое значение суммы двух элементов
    :return: результирующий кортеж из двух индексов

    >>> two_sum_hashed([1, 2, 3, 4, 5, 6, 7, 8, 9], 8)
    (0, 6)
    """
    d = dict()  # Создадим и заполним словарь из lst
    for i in range(len(lst)):
        d[str(i)] = lst[i]  # index -> key

    # Создадим список, в который запишем нужные значения
    term = []
    for a in d.values():
        b = target - a  # находим парное слагаемое для текущего значения
        if b in d.values():  # ищем его в значениях (эта строка на O(n) вышла!!!)
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
    if len(res) > 1:
        return tuple(res)
    return None


def two_sum_hashed_2(lst:list[int], target:int) -> None | tuple[int, int]:
    """
        Наиболее эффективное решение задачи.
        Функция работает со словарём, выполняет поиск 1 пары индексов,
        но уже с вычислительной сложностью ниже O(n^2)

        :param list lst: список значений для поиска суммы
        :param int target: целевое значение суммы двух элементов
        :return: результирующий кортеж из двух индексов

        >>> two_sum_hashed_2([1, 2, 3, 4, 5, 6, 7, 8, 9], 8)
        (0, 6)
        """
    if len(lst) > 1:
        hash_map = {}  # создаём словарь, где ключи=значения списка, значения=индексы элементов списка
        for i in range(0, len(lst)):
            if lst[i] not in hash_map: # сохраняем лишь первое вхождение элемента
                hash_map[lst[i]] = i

        for i in range(len(lst)):
            comp = target - lst[i]  # вычисляем возможную пару текущего элемента
            if comp in hash_map and i != hash_map[comp]:  # проверяем на наличие в словаре и на повторы
                return  i, hash_map[comp]  # кортеж значений = искомых индексов

    return None


def two_sum_all(lst: list[int], target: int) -> None | list[tuple[int, int]]:
    """
    Функция записывает все пары индексов в список кортежей, начиная с минимальных.

    Используется словарь с ключами-значениями num и значениями-списком индексов i

    :param list lst: список значений для поиска суммы
    :param int target: целевое значение суммы двух элементов
    :return: список из кортежей со всеми парами индексов подходящих элементов

    >>> two_sum_all([3, 3, 1, 3, 1], 4)
    [(0, 2), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)]
    """
    # Простая версия с изменённой функцией two_sum
    # res = list()
    # if len(lst) > 1:
    #     for i in range(0, len(lst) - 1):  # см. two_sum()
    #         for j in range(i + 1, len(lst)):
    #             if lst[i] + lst[j] == target:
    #                 res.append((i, j))  # Добавляем элемент-кортеж из индексов
    #     if len(res) > 0: return res
    # return None

     if len(lst) <= 1:
        return None

    hashed = {} # Словарь со структурой: значение -> список индексов, где оно встречается
    for i, num in enumerate(lst):
        if num not in hashed:
            hashed[num] = []
        hashed[num].append(i)

    res = []
    for i in range(len(lst)):
        comp = target - lst[i]
        if comp in hashed:
            for j in hashed[comp]: # Это точно меньше O(n**2), т.к. кол-во j меньше len(lst)
                if j > i:  # чтобы не дублировать пары и не использовать один индекс дважды
                    res.append((i, j))

    if len(res) > 0:
        return res
    return None
