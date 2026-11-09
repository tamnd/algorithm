# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probsat/. The authors are listed in prov/RPJ893.jsonl.

"""probSAT (Balint and Schöning 2012), the break-only version.

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
probSAT is incomplete: it returns a model or None, and None does not prove
that the formula is unsatisfiable.
"""

import random


def normalize(clauses: list[list[int]]) -> list[list[int]] | None:
    """Drop repeated literals and tautologies. None when an empty clause occurs."""
    out = []
    for cl in clauses:
        c = sorted(set(cl))
        if not c:
            return None
        if any(-l in c for l in c):
            continue
        out.append(c)
    return out


class State:
    """An assignment with the number of true literals of each clause and the list of false clauses."""

    def __init__(self, n: int, clauses: list[list[int]], x: list[bool]) -> None:
        self.clauses = clauses
        self.x = [False] + x
        self.occ: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
        for j, cl in enumerate(clauses):
            for lit in cl:
                self.occ[abs(lit)].append((j, lit))
        self.true_count = [sum(self.x[abs(l)] == (l > 0) for l in cl) for cl in clauses]
        self.false_list: list[int] = []
        self.where = [-1] * len(clauses)
        for j, c in enumerate(self.true_count):
            if c == 0:
                self.where[j] = len(self.false_list)
                self.false_list.append(j)

    def break_count(self, v: int) -> int:
        """The number of clauses whose only true literal is on v."""
        return sum(1 for j, lit in self.occ[v] if self.true_count[j] == 1 and self.x[v] == (lit > 0))

    def flip(self, v: int) -> None:
        self.x[v] = not self.x[v]
        for j, lit in self.occ[v]:
            if self.x[v] == (lit > 0):
                self.true_count[j] += 1
                if self.true_count[j] == 1:  # the clause was false
                    i = self.where[j]
                    last = self.false_list.pop()
                    if last != j:
                        self.false_list[i] = last
                        self.where[last] = i
                    self.where[j] = -1
            else:
                self.true_count[j] -= 1
                if self.true_count[j] == 0:  # the clause became false
                    self.where[j] = len(self.false_list)
                    self.false_list.append(j)


def weight(b: int, cb: float, eps: float, kind: str) -> float:
    """f(break): (eps + b) ** -cb for kind 'poly', cb ** -b for kind 'exp'."""
    if kind == "poly":
        return (eps + b) ** -cb
    if kind == "exp":
        return cb ** -b
    raise ValueError("kind must be 'poly' or 'exp'")


def probabilities(s: State, clause: list[int], cb: float, eps: float, kind: str) -> list[tuple[int, float]]:
    """The probability with which each variable of the false clause is flipped."""
    w = [(abs(l), weight(s.break_count(abs(l)), cb, eps, kind)) for l in clause]  # @line L6
    total = sum(x for _, x in w)
    return [(v, x / total) for v, x in w]


def probsat(n: int, clauses: list[list[int]], cb: float = 2.38, eps: float = 1.0, kind: str = "poly", max_tries: int = 10, max_flips: int | None = None, rng: random.Random | None = None) -> list[bool] | None:
    """Return a model as a list of n booleans (x[v - 1] is the value of v), or None.

    The defaults cb = 2.38, eps = 1 and kind 'poly' are the values reported for 3-SAT.
    max_flips defaults to 100 n.
    """
    rng = rng or random.Random()
    cls = normalize(clauses)
    if cls is None:
        return None
    if max_flips is None:
        max_flips = 100 * max(n, 1)
    for _ in range(max_tries):  # @line L1
        s = State(n, cls, [rng.random() < 0.5 for _ in range(n)])  # @line L2
        for f in range(max_flips + 1):  # @line L3
            if not s.false_list:  # @line L4
                return s.x[1:]
            if f == max_flips:
                break
            c = cls[s.false_list[rng.randrange(len(s.false_list))]]  # @line L5
            probs = probabilities(s, c, cb, eps, kind)
            v = rng.choices([v for v, _ in probs], weights=[q for _, q in probs])[0]  # @line L7
            s.flip(v)  # @line L8
    return None  # @line L9
