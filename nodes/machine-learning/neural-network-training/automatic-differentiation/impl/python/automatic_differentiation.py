# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automatic-differentiation/. The authors are listed in prov/9QSEWQ.jsonl.
"""Forward mode with dual numbers and reverse mode with a tape (a Wengert list).

A program is a Python function that uses +, -, *, / and the functions exp, log,
sin, cos and tanh of this module. The same function runs on floats, on Dual
numbers (forward mode, one Jacobian vector product per run) and on Var objects
(reverse mode, one vector Jacobian product per backward sweep of the tape).

Cost: if the program performs T elementary operations, one forward mode run
costs O(T) and gives J v for one direction v; the tape holds T entries, and one
backward sweep costs at most two multiply-adds per entry, so it gives u^T J for
one weight vector u in O(T) time and O(T) memory.
"""

import math
from typing import Callable, Sequence


class Dual:
    """A number a + b e with e^2 = 0: val is f(x), dot is the derivative along v."""

    __slots__ = ("val", "dot")

    def __init__(self, val: float, dot: float = 0.0) -> None:
        self.val = val
        self.dot = dot

    def __add__(self, o):
        o = _lift_dual(o)
        return Dual(self.val + o.val, self.dot + o.dot)

    __radd__ = __add__

    def __sub__(self, o):
        o = _lift_dual(o)
        return Dual(self.val - o.val, self.dot - o.dot)

    def __rsub__(self, o):
        return _lift_dual(o) - self

    def __mul__(self, o):
        o = _lift_dual(o)
        return Dual(self.val * o.val, self.dot * o.val + self.val * o.dot)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _lift_dual(o)
        q = self.val / o.val
        return Dual(q, (self.dot - q * o.dot) / o.val)

    def __rtruediv__(self, o):
        return _lift_dual(o) / self

    def __neg__(self):
        return Dual(-self.val, -self.dot)


def _lift_dual(o) -> Dual:
    return o if isinstance(o, Dual) else Dual(float(o), 0.0)


class Tape:
    """The trace of one evaluation: entry i is (parents, local partials)."""

    def __init__(self) -> None:
        self.parents: list[tuple[int, ...]] = []
        self.partials: list[tuple[float, ...]] = []

    def push(self, parents: tuple[int, ...], partials: tuple[float, ...]) -> int:
        self.parents.append(parents)
        self.partials.append(partials)
        return len(self.parents) - 1

    def __len__(self) -> int:
        return len(self.parents)


class Var:
    """A value recorded on a tape. idx is its entry; inputs have no parents."""

    __slots__ = ("val", "tape", "idx")

    def __init__(self, tape: Tape, val: float, parents=(), partials=()) -> None:
        self.val = val
        self.tape = tape
        self.idx = tape.push(tuple(parents), tuple(partials))

    def _lift(self, o) -> "Var":
        return o if isinstance(o, Var) else Var(self.tape, float(o))

    def __add__(self, o):
        o = self._lift(o)
        return Var(self.tape, self.val + o.val, (self.idx, o.idx), (1.0, 1.0))

    __radd__ = __add__

    def __sub__(self, o):
        o = self._lift(o)
        return Var(self.tape, self.val - o.val, (self.idx, o.idx), (1.0, -1.0))

    def __rsub__(self, o):
        return self._lift(o) - self

    def __mul__(self, o):
        o = self._lift(o)
        return Var(self.tape, self.val * o.val, (self.idx, o.idx), (o.val, self.val))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._lift(o)
        q = self.val / o.val
        return Var(self.tape, q, (self.idx, o.idx), (1.0 / o.val, -q / o.val))

    def __rtruediv__(self, o):
        return self._lift(o) / self

    def __neg__(self):
        return Var(self.tape, -self.val, (self.idx,), (-1.0,))


def _unary(x, f: Callable[[float], float], df: Callable[[float, float], float]):
    """Apply f with derivative df(x, f(x)) to a float, a Dual or a Var."""
    if isinstance(x, Dual):
        y = f(x.val)
        return Dual(y, df(x.val, y) * x.dot)
    if isinstance(x, Var):
        y = f(x.val)
        return Var(x.tape, y, (x.idx,), (df(x.val, y),))
    return f(x)


def exp(x):
    return _unary(x, math.exp, lambda a, y: y)


def log(x):
    return _unary(x, math.log, lambda a, y: 1.0 / a)


def sin(x):
    return _unary(x, math.sin, lambda a, y: math.cos(a))


def cos(x):
    return _unary(x, math.cos, lambda a, y: -math.sin(a))


def tanh(x):
    return _unary(x, math.tanh, lambda a, y: 1.0 - y * y)


def jvp(f: Callable, x: Sequence[float], v: Sequence[float]) -> tuple[list[float], list[float]]:
    """Forward mode: return f(x) and J(x) v with one run on dual numbers."""
    out = f([Dual(a, b) for a, b in zip(x, v)])
    out = out if isinstance(out, (list, tuple)) else [out]
    outs = [_lift_dual(o) for o in out]
    return [o.val for o in outs], [o.dot for o in outs]


def reverse_sweep(tape: Tape, seeds: dict[int, float]) -> list[float]:
    """Accumulate adjoints from the last tape entry to the first."""
    adj = [0.0] * len(tape)  # @line L2
    for i, s in seeds.items():
        adj[i] += s  # @line L3
    for i in range(len(tape) - 1, -1, -1):  # @line L4
        a = adj[i]
        if a == 0.0:
            continue
        for j, c in zip(tape.parents[i], tape.partials[i]):  # @line L5
            adj[j] += a * c  # @line L6
    return adj


def vjp(f: Callable, x: Sequence[float], u: Sequence[float]) -> tuple[list[float], list[float], int]:
    """Reverse mode: return f(x), u^T J(x) and the tape length, with one sweep."""
    tape = Tape()
    xs = [Var(tape, float(a)) for a in x]  # @line L1
    out = f(xs)  # @line L1
    out = out if isinstance(out, (list, tuple)) else [out]
    outs = [o if isinstance(o, Var) else Var(tape, float(o)) for o in out]
    seeds: dict[int, float] = {}
    for o, w in zip(outs, u):
        seeds[o.idx] = seeds.get(o.idx, 0.0) + w
    adj = reverse_sweep(tape, seeds)
    return [o.val for o in outs], [adj[v.idx] for v in xs], len(tape)  # @line L7


def grad(f: Callable, x: Sequence[float]) -> list[float]:
    """The gradient of a scalar program by one reverse sweep."""
    return vjp(f, x, [1.0])[1]


def grad_forward(f: Callable, x: Sequence[float]) -> list[float]:
    """The gradient of a scalar program by n forward mode runs, one per input."""
    n = len(x)
    g = []
    for i in range(n):
        e = [0.0] * n
        e[i] = 1.0
        g.append(jvp(f, x, e)[1][0])
    return g


def jacobian_forward(f: Callable, x: Sequence[float]) -> list[list[float]]:
    """The m x n Jacobian by n forward runs (one column each)."""
    n = len(x)
    cols = []
    for i in range(n):
        e = [0.0] * n
        e[i] = 1.0
        cols.append(jvp(f, x, e)[1])
    m = len(cols[0])
    return [[cols[j][i] for j in range(n)] for i in range(m)]


def jacobian_reverse(f: Callable, x: Sequence[float], m: int) -> list[list[float]]:
    """The m x n Jacobian by m reverse sweeps (one row each)."""
    rows = []
    for i in range(m):
        u = [0.0] * m
        u[i] = 1.0
        rows.append(vjp(f, x, u)[1])
    return rows
