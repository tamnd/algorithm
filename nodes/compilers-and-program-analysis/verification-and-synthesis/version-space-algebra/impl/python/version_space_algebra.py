# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/version-space-algebra/. The authors are listed in prov/4T1SEM.jsonl.
"""A version space algebra over a small arithmetic language.

Programs of the language:
    "x", "y", "1", "2"        terminals; the input is a pair (x, y) of ints
    (op, p, q)                 op is "+", "-" or "*"; p and q are programs
The size of a program is the number of nodes of its tree, so sizes are odd.

A version space is a DAG of three kinds of nodes:
    Leaf(progs)       a finite set of terminal programs
    Union(kids)       the union of the sets of the kids
    Join(op, a, b)    all programs (op, p, q) with p in a and q in b
EMPTY is the union with no kids. The constructors make_leaf, make_union and
make_join never build any other node with an empty set.

build(inp, out, max_size) returns the version space of all programs of size
at most max_size whose output on inp is out. intersect(a, b) returns a
version space for the intersection of the two sets. count(n) gives the
number of programs without listing them. The unions that build and
intersect make have kids with disjoint sets, so count(n) is exact.
"""

TERMINALS = ("x", "y", "1", "2")
OPS = ("+", "-", "*")


def apply_op(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    raise ValueError(f"unknown operator {op!r}")


def evaluate(p, inp):
    """The output of program p on the input pair inp = (x, y)."""
    if p == "x":
        return inp[0]
    if p == "y":
        return inp[1]
    if p == "1":
        return 1
    if p == "2":
        return 2
    return apply_op(p[0], evaluate(p[1], inp), evaluate(p[2], inp))


def size(p):
    if isinstance(p, str):
        return 1
    return 1 + size(p[1]) + size(p[2])


def show(p):
    if isinstance(p, str):
        return p
    return f"({show(p[1])} {p[0]} {show(p[2])})"


class Leaf:
    __slots__ = ("progs",)

    def __init__(self, progs):
        self.progs = progs


class Union:
    __slots__ = ("kids",)

    def __init__(self, kids):
        self.kids = kids


class Join:
    __slots__ = ("op", "left", "right")

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


EMPTY = Union(())


def make_leaf(progs):
    progs = frozenset(progs)
    return Leaf(progs) if progs else EMPTY


def make_union(kids):
    kids = tuple(k for k in kids if k is not EMPTY)
    if not kids:
        return EMPTY
    if len(kids) == 1:
        return kids[0]
    return Union(kids)


def make_join(op, left, right):
    if left is EMPTY or right is EMPTY:
        return EMPTY
    return Join(op, left, right)


def build(inp, out, max_size):
    """The version space of the programs of size <= max_size with output out on inp."""
    by_value = {}
    for t in TERMINALS:  # @line L1
        by_value.setdefault(evaluate(t, inp), []).append(t)
    vals = {1: set(by_value)}  # @line L2
    how = {}
    for s in range(3, max_size + 1, 2):  # @line L3
        table = {}
        for s1 in range(1, s - 1, 2):  # @line L4
            s2 = s - 1 - s1
            for a in vals[s1]:
                for b in vals[s2]:
                    for op in OPS:
                        table.setdefault(apply_op(op, a, b), []).append((op, s1, a, b))  # @line L5
        how[s] = table
        vals[s] = set(table)  # @line L6

    memo = {}

    def node(s, v):
        key = (s, v)
        if key not in memo:
            if s == 1:
                memo[key] = make_leaf(by_value.get(v, ()))  # @line L8
            else:
                memo[key] = make_union(  # @line L9
                    make_join(op, node(s1, a), node(s - 1 - s1, b))
                    for (op, s1, a, b) in how[s].get(v, ())
                )
        return memo[key]

    return make_union(node(s, out) for s in range(1, max_size + 1, 2) if out in vals[s])  # @line L7


def intersect(a, b, memo=None):
    """A version space whose set is the intersection of the sets of a and b."""
    if memo is None:
        memo = {}
    key = (id(a), id(b))
    if key in memo:
        return memo[key]
    if a is EMPTY or b is EMPTY:  # @line L10
        r = EMPTY
    elif isinstance(a, Union):  # @line L11
        r = make_union(intersect(k, b, memo) for k in a.kids)
    elif isinstance(b, Union):  # @line L12
        r = make_union(intersect(a, k, memo) for k in b.kids)
    elif isinstance(a, Leaf) and isinstance(b, Leaf):  # @line L13
        r = make_leaf(a.progs & b.progs)
    elif isinstance(a, Join) and isinstance(b, Join) and a.op == b.op:  # @line L14
        left = intersect(a.left, b.left, memo)
        r = EMPTY if left is EMPTY else make_join(a.op, left, intersect(a.right, b.right, memo))
    else:
        r = EMPTY  # @line L15
    memo[key] = r
    return r


def synthesize(examples, max_size):
    """The version space of the programs of size <= max_size consistent with all examples."""
    root = None
    for inp, out in examples:
        v = build(inp, out, max_size)
        root = v if root is None else intersect(root, v)
        if root is EMPTY:
            break
    return root


def _nodes(n):
    """All nodes reachable from n, each once."""
    seen = {}
    stack = [n]
    while stack:
        m = stack.pop()
        if id(m) in seen:
            continue
        seen[id(m)] = m
        if isinstance(m, Union):
            stack.extend(m.kids)
        elif isinstance(m, Join):
            stack.append(m.left)
            stack.append(m.right)
    return list(seen.values())


def dag_size(n):
    """(number of nodes, number of edges) of the DAG; a leaf counts its programs as edges."""
    nodes = _nodes(n)
    edges = 0
    for m in nodes:
        if isinstance(m, Union):
            edges += len(m.kids)
        elif isinstance(m, Join):
            edges += 2
        else:
            edges += len(m.progs)
    return len(nodes), edges


def count(n, memo=None):
    """The number of programs in the set of n, without listing them."""
    if memo is None:
        memo = {}
    if id(n) in memo:
        return memo[id(n)]
    if isinstance(n, Leaf):
        c = len(n.progs)  # @line L16
    elif isinstance(n, Union):
        c = sum(count(k, memo) for k in n.kids)  # @line L17
    else:
        c = count(n.left, memo) * count(n.right, memo)  # @line L18
    memo[id(n)] = c
    return c


def programs(n):
    """Yield every program of the set of n."""
    if isinstance(n, Leaf):
        yield from sorted(n.progs)
    elif isinstance(n, Union):
        for k in n.kids:
            yield from programs(k)
    else:
        rights = list(programs(n.right))
        for p in programs(n.left):
            for q in rights:
                yield (n.op, p, q)


def smallest(n, memo=None):
    """A program of least size in the set of n, or None if the set is empty."""
    if memo is None:
        memo = {}
    if id(n) in memo:
        return memo[id(n)]
    if isinstance(n, Leaf):
        best = min(n.progs)
    elif isinstance(n, Union):
        cands = [smallest(k, memo) for k in n.kids]
        cands = [c for c in cands if c is not None]
        best = min(cands, key=size) if cands else None
    else:
        best = (n.op, smallest(n.left, memo), smallest(n.right, memo))
    memo[id(n)] = best
    return best
