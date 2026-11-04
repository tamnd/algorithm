# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zipper/. The authors are listed in prov/T3A6Y3.jsonl.

"""A Huet zipper over immutable binary trees.

A tree is None (empty) or a tuple (left, value, right). A zipper is a focus
subtree plus a path of crumbs back to the root. Each crumb records the
direction taken, the value of the parent, and the sibling subtree. The path
is a persistent stack of tuples (crumb, rest). Nothing is ever mutated, so
every zipper value stays valid after any later operation.
"""

from typing import Any, Iterator, List, Optional, Tuple

Tree = Optional[Tuple[Any, Any, Any]]  # (left, value, right) or None
_LEFT, _RIGHT = 0, 1


def node(left: Tree, value: Any, right: Tree) -> Tree:
    """Make a tree node. Cost: O(1)."""
    return (left, value, right)


def inorder(t: Tree) -> List[Any]:
    """Values of t in symmetric order, iteratively. Cost: Θ(size of t)."""
    out: List[Any] = []
    stack: List[Tuple[Any, Any, Any]] = []
    while stack or t is not None:
        while t is not None:
            stack.append(t)
            t = t[0]
        top = stack.pop()
        out.append(top[1])
        t = top[2]
    return out


class Zipper:
    """An immutable cursor into a binary tree."""

    __slots__ = ("_focus", "_path", "_depth")

    def __init__(self, tree: Tree, path: Any = None, depth: int = 0) -> None:
        """A zipper whose focus is the root of ``tree``. Cost: O(1)."""
        self._focus = tree
        self._path = path  # None or ((direction, value, sibling), rest)
        self._depth = depth

    @property
    def focus(self) -> Tree:
        """The subtree at the focus. Cost: O(1)."""
        return self._focus

    @property
    def depth(self) -> int:
        """Number of crumbs on the path. Cost: O(1)."""
        return self._depth

    def at_top(self) -> bool:
        """Whether the focus is the root. Cost: O(1)."""
        return self._path is None

    def value(self) -> Any:
        """The value at the focus. Cost: O(1)."""
        if self._focus is None:
            raise ValueError("the focus is empty")
        return self._focus[1]

    def left(self) -> "Zipper":
        """Move the focus to the left child. Cost: O(1)."""
        t, p = self._focus, self._path  # @line L1
        if t is None:  # @line L2
            raise ValueError("cannot go down from an empty focus")
        l, x, r = t  # @line L3
        return Zipper(l, ((_LEFT, x, r), p), self._depth + 1)  # @line L4

    def right(self) -> "Zipper":
        """Move the focus to the right child. Cost: O(1)."""
        t, p = self._focus, self._path
        if t is None:
            raise ValueError("cannot go down from an empty focus")
        l, x, r = t  # @line L5
        return Zipper(r, ((_RIGHT, x, l), p), self._depth + 1)  # @line L6

    def up(self) -> "Zipper":
        """Move the focus to the parent, rebuilding one node. Cost: O(1)."""
        t, p = self._focus, self._path
        if p is None:  # @line L7
            raise ValueError("already at the top")
        (d, x, s), rest = p  # @line L8
        if d == _LEFT:  # @line L9
            return Zipper((t, x, s), rest, self._depth - 1)
        return Zipper((s, x, t), rest, self._depth - 1)  # @line L10

    def replace(self, t: Tree) -> "Zipper":
        """Replace the focus subtree by t. Cost: O(1)."""
        return Zipper(t, self._path, self._depth)  # @line L11

    def set_value(self, x: Any) -> "Zipper":
        """Replace the value at the focus. Cost: O(1)."""
        if self._focus is None:
            raise ValueError("the focus is empty")
        l, _, r = self._focus
        return self.replace((l, x, r))

    def top(self) -> "Zipper":
        """Move the focus to the root. Cost: Θ(1 + depth)."""
        z = self
        while not z.at_top():  # @line L12
            z = z.up()
        return z  # @line L13

    def to_tree(self) -> Tree:
        """The whole tree that this zipper represents. Cost: Θ(1 + depth)."""
        return self.top().focus

    def path_values(self) -> Iterator[Any]:
        """Values of the ancestors of the focus, nearest first. Cost: Θ(depth)."""
        p = self._path
        while p is not None:
            yield p[0][1]
            p = p[1]

    def check_invariant(self) -> None:
        """Check that the path has ``depth`` well-formed crumbs and that the
        focus and the siblings are well-formed trees. Cost: Θ(depth)."""
        p, n = self._path, 0
        while p is not None:
            crumb, p = p
            assert crumb[0] in (_LEFT, _RIGHT) and len(crumb) == 3
            n += 1
        assert n == self._depth
        assert self._focus is None or len(self._focus) == 3
