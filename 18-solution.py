import math
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Union, Tuple


class NodeIterator:
    def __init__(self, node: 'Node'):
        self._node: 'Node' = node
        self._iter_pos = 0
        self._iter_end = len(node)

    def __next__(self):
        if self._iter_pos == self._iter_end:
            raise StopIteration

        val = self._node[self._iter_pos]
        self._iter_pos += 1
        return val


@dataclass
class Node:
    left: Union['Node', int]
    right: Union['Node', int]
    depth: int
    min_index: int
    max_index: int
    remaining_depth: int

    def __getitem__(self, index) -> int:
        assert isinstance(index, int)
        return Node.get_index_value(self, index)

    def __setitem__(self, index, value):
        assert isinstance(index, int)
        assert isinstance(value, int) or isinstance(value, Node)
        Node.set_index_value(self, index, value)
        self.recalculate_indices(0)
        self.recalculate_remaining_depth()

    def __len__(self):
        return self.max_index + 1

    def __iter__(self):
        return NodeIterator(self)

    def increase_depth(self):
        self.depth += 1
        if isinstance(self.left, Node):
            self.left.increase_depth()

        if isinstance(self.right, Node):
            self.right.increase_depth()

    def increase_index(self, index):
        self.min_index += index
        self.max_index += index
        if isinstance(self.left, Node):
            self.left.increase_index(index)

        if isinstance(self.right, Node):
            self.right.increase_index(index)

    def is_reducible(self):
        return self.remaining_depth > 4 or any(map(lambda x: x > 9, self))

    def __add__(self, other: 'Node'):
        a = deepcopy(self)
        b = deepcopy(other)
        a.increase_depth()
        b.increase_depth()
        b.increase_index(a.max_index + 1)

        naive_sum = Node(
            left=a,
            right=b,
            depth=0,
            min_index=a.min_index,
            max_index=b.max_index,
            remaining_depth=max(a.remaining_depth, b.remaining_depth) + 1
        )

        smart_sum = naive_sum.reduce()

        return smart_sum

    @staticmethod
    def get_index_value(node: Union['Node', int], index: int) -> int:
        if isinstance(node, int):
            return node

        max_left_index = node.left.max_index if isinstance(node.left, Node) else node.min_index

        if index <= max_left_index:
            return Node.get_index_value(node.left, index)

        else:
            return Node.get_index_value(node.right, index)

    @staticmethod
    def set_index_value(node, index, value):
        if index == node.min_index and isinstance(node.left, int):
            node.left = value
            return

        if index == node.max_index and isinstance(node.right, int):
            node.right = value
            return

        max_left_index = node.left.max_index if isinstance(node.left, Node) else node.min_index
        if index <= max_left_index:
            return Node.set_index_value(node.left, index, value)
        else:
            return Node.set_index_value(node.right, index, value)

    def reduce(self):
        while self.is_reducible():
            while self.remaining_depth > 4:
                self.apply_first_explosion()
            if any(map(lambda x: x > 9, self)):
                self.apply_first_split()

        self.recalculate_depth(0)
        self.recalculate_remaining_depth()
        self.recalculate_indices(0)

        return self

    def apply_first_explosion(self):
        explode_index, explode_node = self.find_explosion_index(3)

        add_left = explode_node.left
        add_right = explode_node.right
        if explode_index > 0:
            self[explode_index - 1] += add_left
        if explode_index < len(self) - 2:
            self[explode_index + 2] += add_right
        self.replace_node(explode_node, 0)

    def find_explosion_index(self, remaining_depth) -> Tuple[int, 'Node']:
        assert self.remaining_depth > remaining_depth
        if remaining_depth == 0:
            if isinstance(self.left, Node):
                return self.left.min_index, self.left
            else:
                return self.right.min_index, self.right

        if isinstance(self.left, Node) and self.left.remaining_depth > remaining_depth:
            return self.left.find_explosion_index(remaining_depth-1)
        else:
            return self.right.find_explosion_index(remaining_depth-1)

    def replace_node(self, replace_node, new_val):
        if self.left is replace_node:
            self.left = new_val

        if self.right is replace_node:
            self.right = new_val

        if isinstance(self.left, Node):
            self.left.replace_node(replace_node, new_val)
        if isinstance(self.right, Node):
            self.right.replace_node(replace_node, new_val)

        if self.depth == 0:
            self.recalculate_indices(0)
            self.recalculate_remaining_depth()

    def count_children(self):
        left_children = 1 if isinstance(self.left, int) else self.left.count_children()
        right_children = 1 if isinstance(self.right, int) else self.right.count_children()

        return left_children + right_children

    def recalculate_indices(self, min_index: int):
        self.min_index = min_index
        self.max_index = self.min_index + self.count_children() - 1

        right_start_index = self.min_index + 1
        if isinstance(self.left, Node):
            self.left.recalculate_indices(self.min_index)
            right_start_index = self.left.max_index + 1

        if isinstance(self.right, Node):
            self.right.recalculate_indices(right_start_index)

    def recalculate_depth(self, current_depth: int):
        self.depth = current_depth

        if isinstance(self.left, Node):
            self.left.recalculate_depth(current_depth + 1)

        if isinstance(self.right, Node):
            self.right.recalculate_depth(current_depth + 1)

    def recalculate_remaining_depth(self):
        if isinstance(self.left, Node):
            self.left.recalculate_remaining_depth()

        if isinstance(self.right, Node):
            self.right.recalculate_remaining_depth()

        left_remaining_depth = self.left.remaining_depth if isinstance(self.left, Node) else 0
        right_remaining_depth = self.right.remaining_depth if isinstance(self.right, Node) else 0

        self.remaining_depth = max(left_remaining_depth, right_remaining_depth) + 1

    def apply_first_split(self):
        split_index = self.find_split_index()
        value = self[split_index]
        new_node = Node(
            left=math.floor(value/2),
            right=math.ceil(value/2),
            depth=0,
            min_index=0,
            max_index=0,
            remaining_depth=0
        )
        self[split_index] = new_node
        self.recalculate_depth(0)

    def find_split_index(self):
        if isinstance(self.left, Node):
            if (i := self.left.find_split_index()) != -1:
                return i
        elif self.left >= 10:
            return self.min_index

        if isinstance(self.right, Node):
            if (i := self.right.find_split_index()) != -1:
                return i
        elif self.right >= 10:
            return self.max_index

        return -1

    def magnitude(self):
        left_value = self.left if isinstance(self.left, int) else self.left.magnitude()
        right_value = self.right if isinstance(self.right, int) else self.right.magnitude()

        return 3 * left_value + 2 * right_value


    def __repr__(self):
        return f"[{str(self.left)}, {str(self.right)}]"


def make_tree(snail_num: Union[list, int], min_index, depth) -> Union[Node, int]:
    if isinstance(snail_num, list):
        assert len(snail_num) == 2
        left = make_tree(snail_num[0], min_index, depth + 1)
        right_index = min_index + 1 if isinstance(left, int) else left.max_index + 1
        right = make_tree(snail_num[1], right_index, depth + 1)
        max_index = right_index if isinstance(right, int) else right.max_index

        left_remaining_depth = left.remaining_depth if isinstance(left, Node) else 0
        right_remaining_depth = right.remaining_depth if isinstance(right, Node) else 0

        return Node(
            left=left,
            right=right,
            depth=depth,
            min_index=min_index,
            max_index=max_index,
            remaining_depth=max(left_remaining_depth, right_remaining_depth) + 1
        )
    else:
        # assert snail_num <= 9
        return snail_num


def tests():
    def easy_tree(snail_num) -> Node:
        return make_tree(snail_num, 0, 0)
    # Test 1
    snail_num_1 = Node(left=5, right=4, depth=0, min_index=0, max_index=1, remaining_depth=1)
    snail_num_2 = Node(left=1, right=2, depth=0, min_index=0, max_index=1, remaining_depth=1)
    assert snail_num_1 + snail_num_2 == Node(
        left=Node(left=5, right=4, depth=1, min_index=0, max_index=1, remaining_depth=1),
        right=Node(left=1, right=2, depth=1, min_index=2, max_index=3, remaining_depth=1),
        depth=0,
        min_index=0,
        max_index=3,
        remaining_depth=2,
    )

    # Test 2
    node = make_tree([1, 1], 0, 0) + make_tree([2, 2], 0, 0) + make_tree([3, 3], 0, 0) + make_tree([5, 5], 0, 0)
    assert node.remaining_depth == 4
    assert node.right == Node(
        left=5,
        right=5,
        depth=1,
        min_index=6,
        max_index=7,
        remaining_depth=1,
    )

    assert node.left.left.right == Node(
        left=2,
        right=2,
        depth=3,
        min_index=2,
        max_index=3,
        remaining_depth=1,
    )

    assert not Node(left=9, right=0, depth=0, min_index=0, max_index=1, remaining_depth=1).is_reducible()
    assert not Node(left=0, right=0, depth=0, min_index=0, max_index=1, remaining_depth=4).is_reducible()
    assert Node(left=10, right=0, depth=0, min_index=0, max_index=1, remaining_depth=1).is_reducible()
    assert Node(left=0, right=10, depth=0, min_index=0, max_index=1, remaining_depth=1).is_reducible()
    assert Node(left=0, right=0, depth=0, min_index=0, max_index=1, remaining_depth=5).is_reducible()

    # Test 3
    node = easy_tree(snail_num=[[[[[1, 1], [2, 2]], [3, 3]], [4, 4]], [5, 5]])
    assert node.find_explosion_index(3)[0] == 0

    node = easy_tree([1, [1, [1, [1, [1, 1]]]]])
    assert node.find_explosion_index(3)[0] == 4

    # Test 4 - index access for setting
    node[4] = 5
    assert node[3] == 1
    assert node[4] == 5
    assert node[5] == 1

    node[2] += 3
    assert node[2] == 4

    # Test 5 - replacing nodes
    right_node = Node(left=1, right=2, depth=1, min_index=2, max_index=3, remaining_depth=1)
    node = Node(
        left=Node(left=5, right=4, depth=1, min_index=0, max_index=1, remaining_depth=1),
        right=right_node,
        depth=0,
        min_index=0,
        max_index=3,
        remaining_depth=2,
    )
    assert node.count_children() == 4
    node.replace_node(right_node, 2)
    assert node.count_children() == 3
    assert node[0] == 5
    assert node[1] == 4
    assert node[2] == 2

    # Test 6 - basic explosion
    reduced_tree = easy_tree([[6, [5, [4, [3, 2]]]], 1]).reduce()
    assert reduced_tree.max_index == 4
    assert reduced_tree.min_index == 0
    assert reduced_tree.left.max_index == 3
    assert reduced_tree.left.right.max_index == 3
    assert reduced_tree == easy_tree([[6, [5, [7, 0]]], 3])

    # Test 7 - Explosion edge cases
    assert easy_tree([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]).reduce() == \
           easy_tree([[3, [2, [8, 0]]], [9, [5, [7, 0]]]])

    node = easy_tree([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    node.apply_first_explosion()
    assert node == easy_tree([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])

    assert easy_tree([7, [6, [5, [4, [3, 2]]]]]).reduce() == easy_tree([7, [6, [5, [7, 0]]]])
    assert easy_tree([[[[[9, 8], 1], 2], 3], 4]).reduce() == easy_tree([[[[0, 9], 2], 3], 4])

    # Test 8 - Find split index
    assert easy_tree([10, 10]).find_split_index() == 0
    assert easy_tree([8, 10]).find_split_index() == 1
    assert easy_tree([7, [8, 10]]).find_split_index() == 2
    assert easy_tree([7, [[8, 10], 5]]).find_split_index() == 2

    assert easy_tree([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]).find_split_index() == 3

    # Test 9: Replace int with node
    new_node = Node(left=1, right=2, depth=1, min_index=0, max_index=1, remaining_depth=1)
    node = Node(
        left=Node(left=5, right=4, depth=1, min_index=0, max_index=1, remaining_depth=1),
        right=Node(left=7, right=8, depth=1, min_index=2, max_index=3, remaining_depth=1),
        depth=0,
        min_index=0,
        max_index=3,
        remaining_depth=2,
    )

    node[2] = new_node
    assert node.max_index == 4
    assert node.remaining_depth == 3
    assert node.right.remaining_depth == 2

    node = easy_tree([10, 10])
    node.apply_first_split()
    assert node == easy_tree([[5, 5], 10])

    first_arg = easy_tree([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    second_arg = easy_tree([1,  1])
    actual = first_arg + second_arg
    expected = easy_tree([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
    assert actual == expected

    magnitude = easy_tree([[[[7, 7], [7, 7]], [[7, 0], [7, 7]]], [[[8, 9], [7, 8]], [[8, 3], 8]]]).magnitude()
    assert magnitude == 3997


snail_numbers = []
with open("18-input.txt", "r") as f:
    for line in f.readlines():
        as_list = eval(line.strip())
        snail_numbers.append(make_tree(as_list, 0, 0))

print("Result part 1:")
print(sum(snail_numbers[1:], snail_numbers[0]).magnitude())


print("Solution part 2:")
print(max([(a+b).magnitude() for a in snail_numbers for b in snail_numbers]))