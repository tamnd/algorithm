# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reluplex/. The authors are listed in prov/J93TRS.jsonl.

"""Reluplex: the simplex method of Dutertre and de Moura, extended with ReLU pairs.

The query is a conjunction of linear equations (the tableau), bounds on the variables
and ReLU pairs f = max(0, b). The procedure keeps an assignment that meets every
equation. Simplex steps repair bounds, repair steps repair ReLU pairs, and a pair that
was repaired tau times is split into its two linear phases. All arithmetic is exact
(fractions.Fraction), so SAT and UNSAT answers are exact for the rational query.

The networks in the tests are synthetic networks with seeded rational weights.
"""

from fractions import Fraction
from typing import Optional, Sequence

Num = Fraction
Bound = Optional[Fraction]
Layer = tuple[Sequence[Sequence[Fraction]], Sequence[Fraction]]


class Query:
    """A tableau with bounds, an assignment and ReLU pairs.

    basic maps each basic variable to its row, a dict from non-basic variables to
    non-zero coefficients: x_i = sum of row[j] x_j. lo and hi hold the bounds (None for
    no bound) and val the assignment. pairs lists (b, f) with the constraint f = max(0, b).
    """

    def __init__(self, nvars: int) -> None:
        self.lo: list[Bound] = [None] * nvars
        self.hi: list[Bound] = [None] * nvars
        self.val: list[Num] = [Fraction(0)] * nvars
        self.basic: dict[int, dict[int, Num]] = {}
        self.pairs: list[tuple[int, int]] = []

    def copy(self) -> "Query":
        q = Query(0)
        q.lo, q.hi, q.val = list(self.lo), list(self.hi), list(self.val)
        q.basic = {i: dict(r) for i, r in self.basic.items()}
        q.pairs = list(self.pairs)
        return q

    def row_of(self, v: int) -> dict[int, Num]:
        """v as a combination of non-basic variables."""
        return dict(self.basic[v]) if v in self.basic else {v: Fraction(1)}

    def add_basic(self, row: dict[int, Num], lo: Bound, hi: Bound) -> int:
        """A new basic variable equal to the combination row of non-basic variables."""
        v = len(self.val)
        self.lo.append(lo)
        self.hi.append(hi)
        self.val.append(sum((c * self.val[j] for j, c in row.items()), Fraction(0)))
        self.basic[v] = {j: c for j, c in row.items() if c != 0}
        return v

    def below(self, v: int) -> bool:
        return self.lo[v] is not None and self.val[v] < self.lo[v]

    def above(self, v: int) -> bool:
        return self.hi[v] is not None and self.val[v] > self.hi[v]

    def update(self, j: int, v: Num) -> None:
        """Set the non-basic x_j to v and keep every equation true."""
        delta = v - self.val[j]
        for i, row in self.basic.items():
            if j in row:
                self.val[i] += row[j] * delta
        self.val[j] = v

    def pivot(self, i: int, j: int) -> None:
        """Make the basic x_i non-basic and the non-basic x_j basic. The assignment does not change."""
        row = self.basic.pop(i)
        a = row.pop(j)
        new = {k: -c / a for k, c in row.items()}
        new[i] = 1 / a
        for r in self.basic.values():
            if j in r:
                c = r.pop(j)
                for k, e in new.items():
                    s = r.get(k, Fraction(0)) + c * e
                    if s == 0:
                        r.pop(k, None)
                    else:
                        r[k] = s
        self.basic[j] = new

    def pivot_and_update(self, i: int, j: int, v: Num) -> None:
        """Move the basic x_i to v by a change of the non-basic x_j, then pivot them."""
        theta = (v - self.val[i]) / self.basic[i][j]
        self.val[i] = v
        self.val[j] += theta
        for k, row in self.basic.items():
            if k != i and j in row:
                self.val[k] += row[j] * theta
        self.pivot(i, j)


def relu_violated(q: Query, p: tuple[int, int]) -> bool:
    b, f = p
    return q.val[f] != max(Fraction(0), q.val[b])


def reluplex(q: Query, tau: int = 5) -> Optional[list[Num]]:
    """Decide the query. Returns a satisfying assignment, or None when there is none.

    Precondition: the assignment meets every equation of the tableau; tau >= 1.
    Simplex steps use Bland's rule (least index), so each simplex phase terminates,
    and each pair is repaired at most tau times before it is split, so the whole
    procedure terminates. Cost: exponential in the number of pairs in the worst case;
    each simplex phase can also take exponentially many pivots in the worst case.
    """
    repairs = {p: 0 for p in q.pairs}  # @line L1
    while True:  # @line L2
        nb = [j for j in range(len(q.val)) if j not in q.basic and (q.below(j) or q.above(j))]
        if nb:  # @line L3
            j = nb[0]
            q.update(j, q.lo[j] if q.below(j) else q.hi[j])  # @line L4
            continue
        bad = [i for i in sorted(q.basic) if q.below(i) or q.above(i)]
        if bad:  # @line L5
            i = bad[0]
            row = q.basic[i]
            if q.below(i):
                cand = [j for j in sorted(row) if (row[j] > 0 and (q.hi[j] is None or q.val[j] < q.hi[j]))
                        or (row[j] < 0 and (q.lo[j] is None or q.val[j] > q.lo[j]))]  # @line L6
                target = q.lo[i]
            else:
                cand = [j for j in sorted(row) if (row[j] < 0 and (q.hi[j] is None or q.val[j] < q.hi[j]))
                        or (row[j] > 0 and (q.lo[j] is None or q.val[j] > q.lo[j]))]  # @line L6
                target = q.hi[i]
            if not cand:  # @line L7
                return None  # @line L7
            q.pivot_and_update(i, cand[0], target)  # @line L8
            continue
        broken = [p for p in q.pairs if relu_violated(q, p)]
        if broken:  # @line L9
            p = broken[0]
            b, f = p
            free = [j for j in sorted(q.basic.get(f, {})) if j != b and q.lo[j] != q.hi[j]]
            if repairs[p] >= tau or (f in q.basic and b in q.basic and not free):  # @line L10
                return split(q, p, tau)  # @line L10
            repairs[p] += 1  # @line L11
            if f in q.basic and b in q.basic:  # @line L12
                q.pivot(f, free[0])  # @line L12: never with a fixed variable such as the constant
            if f not in q.basic:  # @line L13
                q.update(f, max(Fraction(0), q.val[b]))  # @line L13
            else:
                q.update(b, q.val[f])  # @line L13
            continue
        return list(q.val)  # @line L14


def split(q: Query, p: tuple[int, int], tau: int) -> Optional[list[Num]]:
    """Case split on the pair p = (b, f): first b <= 0 and f = 0, then b >= 0 and f = b.

    Every solution of the query meets one of the two phases, and in each phase the pair
    is a linear constraint, so it is removed from the list of pairs.
    """
    b, f = p
    rest = [r for r in q.pairs if r != p]
    off = q.copy()  # @line L15
    off.pairs = rest  # @line L15
    off.hi[b] = Fraction(0) if off.hi[b] is None else min(off.hi[b], Fraction(0))  # @line L15
    off.hi[f] = Fraction(0) if off.hi[f] is None else min(off.hi[f], Fraction(0))  # @line L15
    off.lo[f] = Fraction(0) if off.lo[f] is None else max(off.lo[f], Fraction(0))  # @line L15: so f = 0
    result = reluplex(off, tau)  # @line L15
    if result is not None:  # @line L16
        return result[: len(q.val)]  # @line L16
    on = q.copy()  # @line L17
    on.pairs = rest  # @line L17
    on.lo[b] = Fraction(0) if on.lo[b] is None else max(on.lo[b], Fraction(0))  # @line L17
    row = on.row_of(f)
    for j, c in on.row_of(b).items():
        row[j] = row.get(j, Fraction(0)) - c
    on.add_basic(row, Fraction(0), Fraction(0))  # @line L17: the new variable e = f - b is fixed to 0
    result = reluplex(on, tau)  # @line L17
    return None if result is None else result[: len(q.val)]  # @line L17


def encode(layers: Sequence[Layer], lower: Sequence[Fraction], upper: Sequence[Fraction],
           row: Sequence[Fraction], threshold: Fraction) -> tuple[Query, list[int]]:
    """The query: some x in [lower, upper] has row . z(x) >= threshold.

    Variable 0 is the constant 1, variables 1 .. d are the inputs, then each hidden
    unit has a pair (b, f), and the last variable is the output row . z(x).
    Returns the query and the indices of the input variables. Cost O(N) for N weights.
    """
    d = len(lower)
    nh = sum(len(w) for w, _ in layers[:-1])
    q = Query(1 + d + nh)
    q.lo[0] = q.hi[0] = Fraction(1)
    q.val[0] = Fraction(1)
    inputs = list(range(1, d + 1))
    for t, j in enumerate(inputs):
        q.lo[j], q.hi[j] = lower[t], upper[t]
        q.val[j] = lower[t]
    prev = inputs
    nxt = d + 1
    for w, bias in layers[:-1]:
        fs = []
        for wr, bi in zip(w, bias, strict=True):
            f = nxt
            nxt += 1
            q.lo[f] = Fraction(0)
            r = {0: bi}
            for c, v in zip(wr, prev, strict=True):
                r[v] = r.get(v, Fraction(0)) + c
            b = q.add_basic(r, None, None)
            q.pairs.append((b, f))
            fs.append(f)
        prev = fs
    w, bias = layers[-1]
    out = {0: sum((c * bi for c, bi in zip(row, bias, strict=True)), Fraction(0))}
    for t, v in enumerate(prev):
        out[v] = sum((c * wr[t] for c, wr in zip(row, w, strict=True)), Fraction(0))
    q.add_basic(out, threshold, None)
    return q, inputs


def exists_output_at_least(layers: Sequence[Layer], lower: Sequence[Fraction], upper: Sequence[Fraction],
                           row: Sequence[Fraction], threshold: Fraction, tau: int = 5) -> Optional[list[Fraction]]:
    """An input x in the box with row . z(x) >= threshold, or None if there is none."""
    q, inputs = encode(layers, lower, upper, row, threshold)
    sol = reluplex(q, tau)
    return None if sol is None else [sol[j] for j in inputs]


def verify_robust(layers: Sequence[Layer], x: Sequence[Fraction], y: int, epsilon: Fraction,
                  tau: int = 5) -> Optional[list[Fraction]]:
    """None if y is the only argmax on B_infinity(x, epsilon) in [0, 1]^d, else a counterexample.

    For each label j != y it asks whether some input of the box has z_j - z_y >= 0.
    """
    lower = [max(a - epsilon, Fraction(0)) for a in x]
    upper = [min(a + epsilon, Fraction(1)) for a in x]
    k = len(layers[-1][0])
    for j in range(k):
        if j == y:
            continue
        row = [Fraction(1) if t == j else Fraction(-1) if t == y else Fraction(0) for t in range(k)]
        cex = exists_output_at_least(layers, lower, upper, row, Fraction(0), tau)
        if cex is not None:
            return cex
    return None
