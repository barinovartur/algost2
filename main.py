import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Узел бинарного дерева поиска
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, current, key):
        if key < current.key:
            if current.left is None:
                current.left = Node(key)
            else:
                self._insert(current.left, key)
        else:
            if current.right is None:
                current.right = Node(key)
            else:
                self._insert(current.right, key)

    def height(self):
        return self._height(self.root)

    def _height(self, current):
        if current is None:
            return 0
        return 1 + max(self._height(current.left), self._height(current.right))

# Узел AVL-дерева
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, current, key):
        if not current:
            return AVLNode(key)
        if key < current.key:
            current.left = self._insert(current.left, key)
        elif key > current.key:
            current.right = self._insert(current.right, key)
        else:
            return current

        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))
        balance = self._get_balance(current)

        if balance > 1 and key < current.left.key:
            return self._rotate_right(current)
        if balance < -1 and key > current.right.key:
            return self._rotate_left(current)
        if balance > 1 and key > current.left.key:
            current.left = self._rotate_left(current.left)
            return self._rotate_right(current)
        if balance < -1 and key < current.right.key:
            current.right = self._rotate_right(current.right)
            return self._rotate_left(current)

        return current

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, current):
        if not current:
            return 0
        return current.height

    def _get_balance(self, current):
        if not current:
            return 0
        return self._get_height(current.left) - self._get_height(current.right)

    def height(self):
        return self._get_height(self.root)

# Узел красно-черного дерева
class RBNode:
    def __init__(self, key, color="RED"):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = color

class RBTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color="BLACK")
        self.root = self.NIL

    def insert(self, key):
        new_node = RBNode(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        self._insert(new_node)

    def _insert(self, z):
        y = None
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        z.color = "RED"
        self._fix_insert(z)

    def _fix_insert(self, z):
        while z != self.root and z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._rotate_left(z.parent.parent)
        self.root.color = "BLACK"

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def height(self):
        def _height(node):
            if node == self.NIL:
                return 0
            left_height = _height(node.left)
            right_height = _height(node.right)
            return max(left_height, right_height) + 1

        return _height(self.root)

# Построение графиков
def build_and_plot():
    bst = BST()
    avl = AVLTree()
    rb = RBTree()

    keys = [random.randint(1, 100000) for _ in range(100000)]  # увеличиваем до 100000
    bst_heights = []
    avl_heights = []
    rb_heights = []
    x_vals = range(1000, 100001, 1000)

    for i, key in enumerate(keys):
        bst.insert(key)
        avl.insert(key)
        rb.insert(key)

        if (i + 1) % 1000 == 0:
            bst_heights.append(bst.height())
            avl_heights.append(avl.height())
            rb_heights.append(rb.height())

    # Функция для логарифмической регрессии
    def log_func(x, a, b):
        return a * np.log(x) + b

    # Регрессия для BST
    bst_params, _ = curve_fit(log_func, x_vals, bst_heights)
    bst_equation = f"h(n) = {bst_params[0]:.4f} * ln(x) + {bst_params[1]:.4f}"
    print(f"BST логарифмическая регрессия: {bst_equation}")

    # Регрессия для AVL
    avl_params, _ = curve_fit(log_func, x_vals, avl_heights)
    avl_equation = f"h(n) = {avl_params[0]:.4f} * ln(x) + {avl_params[1]:.4f}"
    print(f"AVL логарифмическая регрессия: {avl_equation}")

    # Регрессия для RB
    rb_params, _ = curve_fit(log_func, x_vals, rb_heights)
    rb_equation = f"h(n) = {rb_params[0]:.4f} * ln(x) + {rb_params[1]:.4f}"
    print(f"RB-Tree логарифмическая регрессия: {rb_equation}")

    # Построение графиков
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, bst_heights, label="BST", marker='o')
    plt.plot(x_vals, log_func(np.array(x_vals), *bst_params), linestyle='--', color='b', label=f"Регрессия BST: {bst_equation}")
    plt.xlabel('Количество элементов')
    plt.ylabel('Высота дерева')
    plt.title('Высота BST в зависимости от количества элементов')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 100000)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, avl_heights, label="AVL", marker='x')
    plt.plot(x_vals, log_func(np.array(x_vals), *avl_params), linestyle='--', color='r', label=f"Регрессия AVL: {avl_equation}")
    plt.xlabel('Количество элементов')
    plt.ylabel('Высота дерева')
    plt.title('Высота AVL в зависимости от количества элементов')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 100000)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, rb_heights, label="Красно-черное дерево", marker='^')
    plt.plot(x_vals, log_func(np.array(x_vals), *rb_params), linestyle='--', color='g', label=f"Регрессия RB: {rb_equation}")
    plt.xlabel('Количество элементов')
    plt.ylabel('Высота дерева')
    plt.title('Высота красно-черного дерева в зависимости от количества элементов')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 100000)
    plt.show()

    # Совместный график
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, bst_heights, label="BST", marker='o')
    plt.plot(x_vals, avl_heights, label="AVL", marker='x')
    plt.plot(x_vals, rb_heights, label="Красно-черное дерево", marker='^')
    plt.plot(x_vals, log_func(np.array(x_vals), *bst_params), linestyle='--', color='b', label=f"Регрессия BST: {bst_equation}")
    plt.plot(x_vals, log_func(np.array(x_vals), *avl_params), linestyle='--', color='r', label=f"Регрессия AVL: {avl_equation}")
    plt.plot(x_vals, log_func(np.array(x_vals), *rb_params), linestyle='--', color='g', label=f"Регрессия RB: {rb_equation}")
    plt.xlabel('Количество элементов')
    plt.ylabel('Высота дерева')
    plt.title('Сравнение высоты деревьев поиска (BST, AVL, RB) в зависимости от количества элементов')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 100000)
    plt.show()

build_and_plot()
