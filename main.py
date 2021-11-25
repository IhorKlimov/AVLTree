from dataclasses import dataclass
from typing import Any
import random


@dataclass
class Node:
    key: int
    value: str
    height: int = 1
    left: Any = None
    right: Any = None
    parent: Any = None


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, node: Node):

        # Step 1 - Perform normal BST
        parent = self.root

        while True:
            if parent is None:
                # first node
                self.root = node
                break
            elif node.key < parent.key:
                if parent.left is None:
                    # insert left
                    parent.left = node
                    node.parent = parent
                    break
                else:
                    parent = parent.left
            elif node.key > parent.key:
                if parent.right is None:
                    # insert right
                    parent.right = node
                    node.parent = parent
                    break
                else:
                    parent = parent.right
            else:
                # same, just assign a new value
                parent.value = node.value
                break

        if parent is None:
            return

        # Step 2 - Update the height of the
        # ancestor node
        parent.height = 1 + max(self.get_height(parent.left), self.get_height(parent.right))

        # Step 3 - Get the balance factor
        balance = self.get_balance(parent)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and node.key < parent.left.key:
            return self.right_rotate(parent)

        # Case 2 - Right Right
        if balance < -1 and node.key > parent.right.key:
            return self.left_rotate(parent)

        # Case 3 - Left Right
        if balance > 1 and node.key > parent.left.key:
            parent.left = self.left_rotate(parent.left)
            return self.right_rotate(parent)

        # Case 4 - Right Left
        if balance < -1 and node.key < parent.right.key:
            parent.right = self.right_rotate(parent.right)
            return self.left_rotate(parent)

        return parent

    def left_rotate(self, z):
        y = z.right
        t = y.left

        y.left = z
        z.right = t

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        t = y.right

        y.right = z
        z.left = t

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if root is None:
            return 0

        return root.height

    def delete(self, root, key):
        # Step 1 - Perform standard BST delete
        if not root:
            return root

        elif key < root.key:
            root.left = self.delete(root.left, key)

        elif key > root.key:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        # If the tree has only one node,
        # simply return it
        if root is None:
            return root

        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # Step 3 - Get the balance factor
        balance = self.get_balance(root)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def get_balance(self, root):
        if not root:
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

    def update(self, node: Node):
        parent = self.root

        while True:
            if parent is None:
                return
            elif node.key < parent.key:
                if parent.left is None:
                    return
                else:
                    parent = parent.left
            elif node.key > parent.key:
                if parent.right is None:
                    return
                else:
                    parent = parent.right
            else:
                # found it
                parent.value = node.value
                return

    def get(self, key: int):
        parent = self.root

        while True:
            if parent is None:
                return None
            elif key < parent.key:
                if parent.left is None:
                    return None
                else:
                    parent = parent.left
            elif key > parent.key:
                if parent.right is None:
                    return None
                else:
                    parent = parent.right
            else:
                # found it
                return parent


def main():
    tree = AVLTree()

    node_1 = Node(3, "Hey")
    node_2 = Node(5, "Hey there")
    node_3 = Node(1, "Hey dude")

    tree.insert(node_1)
    tree.insert(node_2)
    tree.insert(node_3)

    print(f"{tree.get(3)}")
    print(f"{tree.get(5)}")
    print(f"{tree.get(1)}")


if __name__ == '__main__':
    main()
