from dataclasses import dataclass
from typing import Any
import random


@dataclass
class Node:
    key: int
    value: str
    height: int = -1
    left: Any = None
    right: Any = None
    parent: Any = None

    def delete(self):
        print(f"Deleting {self}")
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.next_larger()
            print(f"next larger {s}")
            self.key, s.key = s.key, self.key
            return s.delete()

    def find_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current

    def next_larger(self):
        if self.right is not None:
            return self.right.find_min()
        current = self
        while current.parent is not None and current is current.parent.right:
            current = current.parent
        return current.parent


def height(node):
    if node is None:
        return -1
    else:
        return node.height


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


class AVLTree:
    def __init__(self):
        self.root = None

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            print(f"Checking node {node.key}. Left: {height(node.left)}, right: {height(node.right)}")

            if height(node.left) >= 2 + height(node.right):
                print(f"Node {node.key} is left-heavy")
                if height(node.left.left) >= height(node.left.right):
                    print("Doing right rotation")
                    self.right_rotate(node)
                else:
                    print("Doing right left rotation and right rotation")
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                print(f"Node {node.key} is right-heavy")
                if height(node.right.right) >= height(node.right.left):
                    print("Doing left rotation")
                    self.left_rotate(node)
                else:
                    print("Doing right right rotation and left rotation")
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    def insert(self, node: Node):
        print(f"Inserting {node}")
        parent = self.root

        while True:
            if parent is None:
                # first node
                print("First node in a tree. Setting as a root")
                self.root = node
                break
            elif node.key < parent.key:
                if parent.left is None:
                    # insert left
                    parent.left = node
                    node.parent = parent
                    print(f"Inserting as a left child of {parent}")
                    break
                else:
                    parent = parent.left
            elif node.key > parent.key:
                if parent.right is None:
                    # insert right
                    parent.right = node
                    node.parent = parent
                    print(f"Inserting as a right child of {parent}")
                    break
                else:
                    parent = parent.right
            else:
                # same key, just assign a new value
                print(f"Node with this key already existed. Replacing node {parent}")
                parent.value = node.value
                break

        self.rebalance(node)

    def left_rotate(self, node):
        right = node.right
        right.parent = node.parent
        if right.parent is None:
            self.root = right
        else:
            if right.parent.left is node:
                right.parent.left = right
            elif right.parent.right is node:
                right.parent.right = right
        node.right = right.left
        if node.right is not None:
            node.right.parent = node
        right.left = node
        node.parent = right
        update_height(node)
        update_height(right)

    def right_rotate(self, node):
        left = node.left
        left.parent = node.parent
        if left.parent is None:
            self.root = left
        else:
            if left.parent.left is node:
                left.parent.left = left
            elif left.parent.right is node:
                left.parent.right = left
        node.left = left.right
        if node.left is not None:
            node.left.parent = node
        left.right = node
        node.parent = left
        update_height(node)
        update_height(left)

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
        print(f"Finding a node with key: {key}")
        parent = self.root
        num_of_loops = 0

        while True:
            if parent is None:
                print(f"Num of loops to find a node: {num_of_loops}")
                print("Node doesn't exist")
                return None
            elif key < parent.key:
                if parent.left is None:
                    print(f"Num of loops to find a node: {num_of_loops}")
                    print("Node doesn't exist")
                    return None
                else:
                    print("Going left in the tree")
                    parent = parent.left
            elif key > parent.key:
                if parent.right is None:
                    print(f"Num of loops to find a node: {num_of_loops}")
                    print("Node doesn't exist")
                    return None
                else:
                    print("Going right in the tree")
                    parent = parent.right
            else:
                # found it
                print(f"Num of loops to find a node: {num_of_loops}")
                print("Found a node")
                return parent

            num_of_loops += 1

    def delete(self, node):
        deleted = None

        node = self.get(node)
        if node is None:
            return
        if node is self.root:
            pseudoroot = Node(-1, "")
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()

        self.rebalance(deleted.parent)


def main():
    tree = AVLTree()

    # for n in range(10000):
    #     node = Node(random.randint(0, 100_000), f"Test value {n}")
    #     tree.insert(node)
    #
    # for n in range(15):
    #     number = random.randint(0, 100_000)
    #     print(f"Contains node {number}: {tree.get(number) is not None}")

    tree.insert(Node(5, "New York"))
    tree.insert(Node(4, "Boston"))
    tree.insert(Node(8, "Los Angeles"))
    tree.insert(Node(7, "Houston"))
    tree.insert(Node(9, "Fort Lauderdale"))

    tree.get(9)



if __name__ == '__main__':
    main()
