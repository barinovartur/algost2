import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from collections import deque

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

    # Симметричный обход (In-order)
    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.key)
            self._in_order(node.right, result)

    # Прямой обход (Pre-order)
    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node, result):
        if node:
            result.append(node.key)
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)

    # Обратный обход (Post-order)
    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node, result):
        if node:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append(node.key)

    # Обход в ширину (BFS)
    def bfs(self):
        result = []
        if not self.root:
            return result
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

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

    # Симметричный обход (In-order)
    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.key)
            self._in_order(node.right, result)

    # Прямой обход (Pre-order)
    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node, result):
        if node:
            result.append(node.key)
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)

    # Обратный обход (Post-order)
    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node, result):
        if node:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append(node.key)

    # Обход в ширину (BFS)
    def bfs(self):
        result = []
        if not self.root:
            return result
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

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

    # Симметричный обход (In-order)
    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node != self.NIL:
            self._in_order(node.left, result)
            result.append(node.key)
            self._in_order(node.right, result)

    # Прямой обход (Pre-order)
    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node, result):
        if node != self.NIL:
            result.append(node.key)
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)

    # Обратный обход (Post-order)
    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node, result):
        if node != self.NIL:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append(node.key)

    # Обход в ширину (BFS)
    def bfs(self):
        result = []
        if self.root == self.NIL:
            return result
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left != self.NIL:
                queue.append(node.left)
            if node.right != self.NIL:
                queue.append(node.right)
        return result

# Построение графиков
def build_and_plot():
    bst = BST()
    avl = AVLTree()
    rb = RBTree()

    for _ in range(10):  # 10 случайных чисел
        key = random.randint(1, 1000)
        bst.insert(key)
        avl.insert(key)
        rb.insert(key)

    bst_in_order = bst.in_order()
    avl_in_order = avl.in_order()
    rb_in_order = rb.in_order()

    bst_pre_order = bst.pre_order()
    avl_pre_order = avl.pre_order()
    rb_pre_order = rb.pre_order()

    bst_post_order = bst.post_order()
    avl_post_order = avl.post_order()
    rb_post_order = rb.post_order()

    bst_bfs = bst.bfs()
    avl_bfs = avl.bfs()
    rb_bfs = rb.bfs()

    print(f"In-order BST: {bst_in_order}")
    print(f"In-order AVL: {avl_in_order}")
    print(f"In-order RB: {rb_in_order}")

    print(f"-----------")

    print(f"Pre-order BST: {bst_pre_order}")
    print(f"Pre-order AVL: {avl_pre_order}")
    print(f"Pre-order RB: {rb_pre_order}")

    print(f"-----------")

    print(f"Post-order BST: {bst_post_order}")
    print(f"Post-order AVL: {avl_post_order}")
    print(f"Post-order RB: {rb_post_order}")

    print(f"-----------")

    print(f"BFS BST: {bst_bfs}")
    print(f"BFS AVL: {avl_bfs}")
    print(f"BFS RB: {rb_bfs}")

# Вызов функции для построения и вывода результатов
build_and_plot()
