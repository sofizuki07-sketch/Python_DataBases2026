# Лабораторная работа № 2/3
## Рекурсия. Бинарное дерево. map() и zip(). Генераторы списков

### Часть 1
Бинарное дерево рекурсивным способом

**тесты в [test_recursion](test_recursion.py)**
```python
import unittest
from pprint import pprint

# v 5: Root = 5; height = 6, left_leaf = root^2, right_leaf = root-2

def gen_bin_tree(root: int = 5, height: int = 6, left_branch_f: Callable[[int], int] =lambda x: x * x, right_branch_f: Callable[[int], int] =lambda y: y - 2) -> dict:
    """ Рекурсивная функция вычисления бинарного дерева

    :param root: корень дерева
    :param height: количество узлов под корнем (высота дерева)
    :param left_branch_f: функция для корней левой ветви
    :param right_branch_f: функция для корней правой ветви
    :return: бинарное дерево
    """


    # терминальный случай (дошли до листьев)
    if height == 0:
        return {str(root): []}
    else:
        # вычисления корней поддеревьев
        l = left_branch_f(root)
        r = right_branch_f(root)
        # возвращаем словарь: текущий корень -> [левая ветвь, правая ветвь]
        return {str(root): [gen_bin_tree(l, height - 1), gen_bin_tree(r, height - 1)]}


tree = gen_bin_tree(5, 5)
pprint()print(tree, width=10, sort_dicts=False)  # красивый вывод дерева
# print(tree)

"""
Пример ответа с корнем 5
tree = {"5": []} # height = 0
tree = {"5": [{"25": []}, {"3":[]}]} # height = 1

tree = {"5": [{"25": [{"625": []},
                     {"23": []}]},
              {"3":[{"9":[]},
                     {"0": []}]}]} # height = 2

tree = {"5": [{"25": [{"625": [
                          {"390625":[]},
                          {"623":[]}
]},
                     {"23": [
                         {"529":[]},
                         {"20": []}
                     ]}]},
              {"3":[{"9":[
                        {"81": []},
                        {"6":[]}

              ]},
                     {"1": [
                         {"1":[]},
                         {"-1":[]}
                     ]}]}]} # height = 3
"""

```



### Часть 2
Бинарное дерево с помощью вложенных списков

**тесты в [test_List-Dict](test_List-Dict.py)**
```python
from pprint import pprint
from typing import Callable, List


def gen_bin_tree(root: int = 5, height: int = 6, left_branch_f: Callable[[int], int] = lambda x: x * x, right_branch_f: Callable[[int], int] = lambda x: x - 2) -> dict:
    """Итеративно строит бинарное дерево и возвращает его вложенным словарём.


    :param root: значение корня
    :param height: ыысота дерева вместе с корнем
    :param left_branch_f: функция вычисления левого потомка
    :param right_branch_f: функция вычисления правого потомка
    :return: вложенное дерево вида {'5': [{'25': [...]}, {'3': [...]}]}


    >>> gen_bin_tree(5, 3)
    {'5': [{'25': [{'625': []}, {'23': []}]}, {'3': [{'9': []}, {'1': []}]}]}
    """


    # 1) Строим уровни значений дерева
    roots = [[root]]

    for leaf in range(height - 1):
        if len(roots) == 1:
            r = roots[0]
        else:
            r = []
            for s in roots[-1]:
                for item in s:
                    r.append(item)

        leaves = list(map(lambda root_value: [left_branch_f(root_value), right_branch_f(root_value)], r))
        roots.append(leaves)

    # print(f"Корни:  {roots}")

    # 2) Словарно-списковое представление уровней
    tree = []
    for i, leaf in enumerate(roots):
        if i == 0:
            leaves_dict = [ {str(item): []} for item in leaf ]
        else:
            leaves_dict = [ [{str(s[0]): []}, {str(s[1]): []}] for s in leaf ]
        tree.append(leaves_dict)

    # 3) Значения уровней в виде перечисления всех значений в нём (слева направо)
    values = [[str(v) for v in roots[0]]]
    for level in roots[1:]:
        values.append([ str(v) for pair in level for v in pair  ])

    # 4) Снизу вверх собираем вложенное дерево через zip и map
    subtrees = list(map(lambda v: {v: []}, values[-1]))
    for i in range(len(values) - 2, -1, -1):
        children_pairs = list(zip(subtrees[::2], subtrees[1::2])) # обирает в пары левого и правого потомка
        subtrees = list(map(lambda v, pair: {v: [pair[0], pair[1]]}, values[i], children_pairs)) # собирает потомков под узел v в словарь

    # 5) Возвращаем корень со всеми вложенными уровнями-потомками
    return subtrees[0]




```

```
