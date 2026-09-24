# Лабораторная работа № 2
## Рекурсия. Бинарное дерево

### Часть 1
Бинарное дерево рекурсивным способом
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
