# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/term-dag/. The authors are listed in prov/9PFAX5.jsonl.

"""A term DAG: first-order terms stored with maximal sharing (hash consing).

A tree term is a variable (a Python str) or a tuple (symbol, arg1, ..., argk).
A constant is a tuple with one item, for example ("a",).
In the DAG each distinct subterm is one node, so two nodes are equal terms
if and only if they have the same id.
"""

from typing import Union

Term = Union[str, tuple]


class TermDAG:
    """Nodes are numbered 0, 1, 2, ... in order of creation."""

    def __init__(self) -> None:
        self._table: dict[tuple, int] = {}
        self._symbol: list[str] = []
        self._children: list[tuple[int, ...]] = []
        self._is_var: list[bool] = []

    def make_node(self, symbol: str, children: tuple[int, ...] = (), is_var: bool = False) -> int:
        """Return the node for symbol(children), making it only if it is new.

        Precondition: each child id exists. Cost: O(k) expected for k
        children, with one hash table lookup.
        """
        key = ("var", symbol) if is_var else ("app", symbol, children)  # @line L1
        node = self._table.get(key)
        if node is not None:
            return node  # @line L2
        node = len(self._symbol)  # @line L3
        self._symbol.append(symbol)
        self._children.append(() if is_var else tuple(children))
        self._is_var.append(is_var)
        self._table[key] = node  # @line L4
        return node  # @line L5

    def var(self, name: str) -> int:
        return self.make_node(name, (), True)

    def intern(self, term: Term) -> int:
        """Return the node of a tree term. Cost: O(size of the tree) expected."""
        out: list[int] = []
        stack: list[tuple[Term, bool]] = [(term, False)]
        while stack:
            u, done = stack.pop()
            if isinstance(u, str):
                out.append(self.var(u))  # @line L6
            elif not done:
                stack.append((u, True))
                for a in reversed(u[1:]):
                    stack.append((a, False))
            else:
                k = len(u) - 1
                kids = tuple(out[len(out) - k:]) if k else ()
                del out[len(out) - k:]
                out.append(self.make_node(u[0], kids))  # @line L7
        return out[0]

    def symbol(self, node: int) -> str:
        return self._symbol[node]

    def children(self, node: int) -> tuple[int, ...]:
        return self._children[node]

    def is_var(self, node: int) -> bool:
        return self._is_var[node]

    def dag_size(self) -> int:
        """The number of nodes, that is, of distinct subterms stored."""
        return len(self._symbol)

    def tree_size(self, node: int) -> int:
        """The number of nodes of the tree that node stands for.

        Children have smaller ids than their parents, so one pass in id
        order computes all sizes. Cost: O(number of nodes and edges).
        """
        sizes = [0] * (node + 1)
        for i in range(node + 1):
            sizes[i] = 1 + sum(sizes[c] for c in self._children[i])
        return sizes[node]

    def unfold(self, node: int) -> Term:
        """Return the tree term of node. Cost: O(size of the tree)."""
        memo: dict[int, Term] = {}
        stack = [(node, False)]
        while stack:
            d, done = stack.pop()
            if d in memo:
                continue
            if self._is_var[d]:
                memo[d] = self._symbol[d]
            elif done:
                memo[d] = (self._symbol[d], *[memo[c] for c in self._children[d]])
            else:
                stack.append((d, True))
                stack.extend((c, False) for c in self._children[d] if c not in memo)
        return memo[node]

    def check_invariant(self) -> None:
        """No two nodes have the same key, and each child is older than its parent."""
        keys = set()
        for i, sym in enumerate(self._symbol):
            key = ("var", sym) if self._is_var[i] else ("app", sym, self._children[i])
            assert key not in keys
            assert self._table[key] == i
            assert all(c < i for c in self._children[i])
            keys.add(key)
        assert len(keys) == len(self._table)
