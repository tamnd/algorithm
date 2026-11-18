# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chawathe-tree-diff/. The authors are listed in prov/Y3W16W.jsonl.
"""Change detection in ordered labeled trees, after Chawathe, Rajaraman, Garcia-Molina and Widom (SIGMOD 1996).

Trees have node identifiers, labels and values. fast_match finds a matching of the
nodes of two trees (Figure 11 of the paper), and edit_script turns a matching into an
edit script of inserts, deletes, updates and moves (Figures 8 and 9). Positions k
count from 1, as in the paper: MOV(x, y, k) makes x the k-th child of y.

Two details differ from the text of Figure 9. FIND-POS counts all the children of
the parent, not only the ones marked "in order", and the nodes that are inserted or
moved to their final place are marked "in order". Without these, a node can be
placed before an unmatched sibling or before a sibling inserted just before it.
"""

from collections import deque
from collections.abc import Callable, Hashable, Iterable, Sequence
from typing import Any, NamedTuple, Optional

from txdiff import lcs_matching


class Ins(NamedTuple):
    node: int
    label: Hashable
    value: Any
    parent: int
    k: int

    def __str__(self) -> str:
        return f"INS(({self.node},{self.label},{self.value}),{self.parent},{self.k})"


class Del(NamedTuple):
    node: int

    def __str__(self) -> str:
        return f"DEL({self.node})"


class Upd(NamedTuple):
    node: int
    value: Any

    def __str__(self) -> str:
        return f"UPD({self.node},{self.value})"


class Mov(NamedTuple):
    node: int
    parent: int
    k: int

    def __str__(self) -> str:
        return f"MOV({self.node},{self.parent},{self.k})"


class Tree:
    """An ordered tree with node identifiers; each node has a label, a value, a parent and a list of children."""

    def __init__(self) -> None:
        self.root: Optional[int] = None
        self.label: dict[int, Hashable] = {}
        self.value: dict[int, Any] = {}
        self.parent: dict[int, Optional[int]] = {}
        self.children: dict[int, list[int]] = {}

    @classmethod
    def from_nested(cls, spec: tuple, first_id: int = 1) -> "Tree":
        """Build a tree from (label, value, [children]) or (label, value); the ids go in breadth-first order."""
        tree = cls()
        queue = deque([(spec, None)])
        next_id = first_id
        while queue:
            node_spec, parent = queue.popleft()
            label, value = node_spec[0], node_spec[1]
            kids = node_spec[2] if len(node_spec) > 2 else []
            tree._add(next_id, label, value, parent, None)
            for kid in kids:
                queue.append((kid, next_id))
            next_id += 1
        return tree

    def _add(self, x: int, label: Hashable, value: Any, parent: Optional[int], k: Optional[int]) -> None:
        if x in self.label:
            raise ValueError(f"node {x} exists")
        self.label[x], self.value[x], self.parent[x], self.children[x] = label, value, parent, []
        if parent is None:
            if self.root is not None:
                raise ValueError("the tree has a root")
            self.root = x
        else:
            kids = self.children[parent]
            kids.insert(len(kids) if k is None else k - 1, x)

    def copy(self) -> "Tree":
        t = Tree()
        t.root, t.label, t.value, t.parent = self.root, dict(self.label), dict(self.value), dict(self.parent)
        t.children = {x: list(c) for x, c in self.children.items()}
        return t

    def bfs(self) -> list[int]:
        out, queue = [], deque([self.root] if self.root is not None else [])
        while queue:
            x = queue.popleft()
            out.append(x)
            queue.extend(self.children[x])
        return out

    def postorder(self) -> list[int]:
        out: list[int] = []
        stack = [(self.root, False)] if self.root is not None else []
        while stack:
            x, done = stack.pop()
            if done:
                out.append(x)
            else:
                stack.append((x, True))
                stack.extend((c, False) for c in reversed(self.children[x]))
        return out

    def preorder(self) -> list[int]:
        out: list[int] = []
        stack = [self.root] if self.root is not None else []
        while stack:
            x = stack.pop()
            out.append(x)
            stack.extend(reversed(self.children[x]))
        return out

    def leaves_below(self, x: int) -> list[int]:
        out, stack = [], [x]
        while stack:
            y = stack.pop()
            if self.children[y]:
                stack.extend(self.children[y])
            else:
                out.append(y)
        return out

    def nested(self, x: Optional[int] = None) -> tuple:
        """Return the tree without its ids, as (label, value, (children...))."""
        x = self.root if x is None else x
        return (self.label[x], self.value[x], tuple(self.nested(c) for c in self.children[x]))

    # The four edit operations of Section 3.2.
    def insert(self, x: int, label: Hashable, value: Any, y: int, k: int) -> None:
        if not 1 <= k <= len(self.children[y]) + 1:
            raise ValueError(f"bad position {k}")
        self._add(x, label, value, y, k)

    def delete(self, x: int) -> None:
        if self.children[x] or x == self.root:
            raise ValueError(f"node {x} is not a leaf")
        self.children[self.parent[x]].remove(x)
        for d in (self.label, self.value, self.parent, self.children):
            del d[x]

    def update(self, x: int, value: Any) -> None:
        self.value[x] = value

    def move(self, x: int, y: int, k: int) -> None:
        z = y
        while z is not None:
            if z == x:
                raise ValueError(f"node {y} is in the subtree of {x}")
            z = self.parent[z]
        self.children[self.parent[x]].remove(x)
        if not 1 <= k <= len(self.children[y]) + 1:
            raise ValueError(f"bad position {k}")
        self.children[y].insert(k - 1, x)
        self.parent[x] = y

    def apply(self, op: Any) -> None:
        if isinstance(op, Ins):
            self.insert(op.node, op.label, op.value, op.parent, op.k)
        elif isinstance(op, Del):
            self.delete(op.node)
        elif isinstance(op, Upd):
            self.update(op.node, op.value)
        elif isinstance(op, Mov):
            self.move(op.node, op.parent, op.k)
        else:
            raise ValueError(f"unknown operation {op!r}")


def add_root(tree: Tree, x: int, label: Hashable = "(root)") -> Tree:
    """Return a copy of the tree under a new root x, with the old root as its only child."""
    t = tree.copy()
    old = t.root
    t.label[x], t.value[x], t.parent[x], t.children[x] = label, None, None, [old]
    t.parent[old] = x
    t.root = x
    return t


def apply_script(tree: Tree, script: Iterable[Any]) -> Tree:
    """Apply the operations to a copy of the tree and return it; raise ValueError if one does not fit."""
    t = tree.copy()
    for op in script:
        t.apply(op)
    return t


class EditResult(NamedTuple):
    script: list  # the operations, in order
    matching: dict[int, int]  # the total matching of the final T1 with T2, as T1 node -> T2 node
    root1: Optional[int]  # the dummy root added to T1, or None
    root2: Optional[int]  # the dummy root added to T2, or None


def edit_script(t1: Tree, t2: Tree, matching: Iterable[tuple[int, int]]) -> EditResult:
    """Return an edit script that turns t1 into t2 and keeps the pairs (x of t1, y of t2) of the matching."""
    partner: dict[int, int] = {}
    back: dict[int, int] = {}
    for x, y in matching:
        if x not in t1.label or y not in t2.label or x in partner or y in back or t1.label[x] != t2.label[y]:
            raise ValueError(f"({x}, {y}) does not fit a matching of nodes with equal labels")
        partner[x], back[y] = y, x
    fresh = max(list(t1.label) + list(t2.label)) + 1
    t, target, root1, root2 = t1.copy(), t2, None, None
    if partner.get(t.root) != target.root:  # @line L1
        root1, root2, fresh = fresh, fresh + 1, fresh + 2
        t, target = add_root(t, root1), add_root(t2, root2)
        partner[root1], back[root2] = root2, root1
    script: list = []
    # The nodes of T2 marked "in order": their partners already have their final place
    # among the siblings. The paper marks the partners in T1 too, but FIND-POS reads only these.
    in_order: set[int] = set()

    def do(op: Any) -> None:
        script.append(op)
        t.apply(op)

    def find_pos(x: int) -> int:
        kids = target.children[target.parent[x]]
        left = [v for v in kids[:kids.index(x)] if v in in_order]
        if not left:  # @line L14
            return 1
        u = back[left[-1]]  # @line L15
        siblings = [s for s in t.children[t.parent[u]] if s != back.get(x)]
        return siblings.index(u) + 2

    def align_children(w: int, x: int) -> None:
        in_order.difference_update(target.children[x])  # @line L10
        kids1, kids2 = set(t.children[w]), set(target.children[x])
        s1 = [a for a in t.children[w] if partner.get(a) in kids2]  # @line L11
        s2 = [b for b in target.children[x] if back.get(b) in kids1]
        keep = lcs_matching(s1, s2, lambda a, b: partner[a] == b)  # @line L12
        kept = {s1[i] for i, _ in keep}
        in_order.update(s2[j] for _, j in keep)
        for a in s1:  # @line L13
            if a not in kept:
                do(Mov(a, w, find_pos(partner[a])))
                in_order.add(partner[a])

    for x in target.bfs():  # @line L2
        y = target.parent[x]
        if x not in back:  # @line L3
            k = find_pos(x)
            w = fresh
            fresh += 1
            do(Ins(w, target.label[x], target.value[x], back[y], k))
            partner[w], back[x] = x, w
            in_order.add(x)
        else:
            w = back[x]  # @line L4
            if t.value[w] != target.value[x]:  # @line L5
                do(Upd(w, target.value[x]))
            if y is not None and t.parent[w] != back[y]:  # @line L6
                do(Mov(w, back[y], find_pos(x)))
                in_order.add(x)
        align_children(back[x], x)  # @line L7
    for w in t.postorder():  # @line L8
        if w not in partner:
            do(Del(w))
    return EditResult(script, partner, root1, root2)  # @line L9


def word_compare(u: Any, v: Any) -> float:
    """Return a distance in [0, 2] of two values: 0 if equal, 2 if they share no word, by a longest common subsequence."""
    if u == v:
        return 0.0
    a, b = str(u).split(), str(v).split()
    if not a or not b:
        return 2.0
    return 2.0 - 4.0 * len(lcs_matching(a, b)) / (len(a) + len(b))


def fast_match(t1: Tree, t2: Tree, compare: Callable[[Any, Any], float] = word_compare,
               f: float = 0.5, t: float = 0.6) -> list[tuple[int, int]]:
    """Return a matching of the nodes of t1 and t2 by Algorithm FastMatch.

    Leaves x and y may match if they have the same label and compare(v(x), v(y)) <= f
    (Matching Criterion 1). Internal nodes may match if they have the same label and
    more than a fraction t of the leaves below the larger one are matched to leaves
    below the other (Matching Criterion 2).
    """
    if not (0 <= f <= 1 and 0.5 <= t <= 1):
        raise ValueError("need 0 <= f <= 1 and 1/2 <= t <= 1")
    match: dict[int, int] = {}
    back: dict[int, int] = {}
    leaves1 = {x: t1.leaves_below(x) for x in t1.label}
    leaves2 = {y: set(t2.leaves_below(y)) for y in t2.label}

    def equal(x: int, y: int) -> bool:
        if t1.label[x] != t2.label[y]:
            return False
        if not t1.children[x] and not t2.children[y]:
            return compare(t1.value[x], t2.value[y]) <= f
        if not t1.children[x] or not t2.children[y]:
            return False
        common = sum(1 for w in leaves1[x] if match.get(w) in leaves2[y])
        return common / max(len(leaves1[x]), len(leaves2[y])) > t

    def labels(tree: Tree, leaf: bool) -> dict[Hashable, list[int]]:
        chains: dict[Hashable, list[int]] = {}
        for x in tree.preorder():
            if (not tree.children[x]) == leaf:
                chains.setdefault(tree.label[x], []).append(x)
        return chains

    # Leaves first, so that the test of Criterion 2 can count matched leaves. The paper
    # chains the nodes in in-order; for the leaves, preorder gives the same order.
    for leaf in (True, False):
        chains1, chains2 = labels(t1, leaf), labels(t2, leaf)
        for lab, s1 in chains1.items():
            s2 = chains2.get(lab, [])
            for i, j in lcs_matching(s1, s2, equal):
                match[s1[i]], back[s2[j]] = s2[j], s1[i]
            for x in s1:
                if x in match:
                    continue
                y = next((y for y in s2 if y not in back and equal(x, y)), None)
                if y is not None:
                    match[x], back[y] = y, x
    return sorted(match.items())


def isomorphic(t1: Tree, t2: Tree) -> bool:
    """Return True if the trees are equal except for their node ids."""
    return t1.nested() == t2.nested()


def lower_bound(t1: Tree, t2: Tree, matching: Sequence[tuple[int, int]]) -> int:
    """Return the least number of operations of a script that keeps exactly the pairs of the matching.

    The count is: unmatched nodes of t1 (deletes), unmatched nodes of t2 (inserts),
    pairs with different values (updates), pairs whose parents are not a pair (moves to
    another parent), and for each pair of parents, the number of child pairs between
    them minus a longest common subsequence of them (moves among siblings).
    """
    # The parent None stands for the dummy roots, which are always a pair.
    partner = dict(matching)
    pairs = set(matching) | {(None, None)}
    cost = (len(t1.label) - len(partner)) + (len(t2.label) - len(partner))
    for x, y in matching:
        cost += t1.value[x] != t2.value[y]
        cost += (t1.parent[x], t2.parent[y]) not in pairs
    for u, v in pairs:
        kids1 = t1.children[u] if u is not None else [t1.root]
        kids2 = t2.children[v] if v is not None else [t2.root]
        s1 = [a for a in kids1 if partner.get(a) in kids2]
        s2 = [b for b in kids2 if b in {partner[a] for a in s1}]
        cost += len(s1) - len(lcs_matching(s1, s2, lambda a, b: partner[a] == b))
    return cost
