# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dagum-luby-theorem/. The authors are listed in prov/03QBR6.jsonl.

"""The reduction behind the Dagum-Luby theorem.

The network is Cooper's network for a 3-CNF formula: fair roots Q_0 .. Q_{n-1},
one OR node per clause, and a chain of AND nodes that ends in the output Y, so
P(Y = 1) = #models / 2^n. The evidence is the single node Y = 1.

find_assignment asks an oracle for P(Q_i = 1 | Y = 1) within an absolute error
eps < 1/2, fixes Q_i by setting its prior to 0 or 1, and goes on. P(Y = 1) stays
positive at each step, so after n calls the roots hold a satisfying assignment
when the formula has one. The final check makes the answer one-sided: an
unsatisfiable formula is never accepted, whatever the oracle says.
"""

from fractions import Fraction
from itertools import product
from math import ceil, log
from random import Random
from typing import Callable, Dict, List, NamedTuple, Optional, Sequence, Tuple

Clause = Sequence[Tuple[int, bool]]
Oracle = Callable[[Optional[Fraction]], Fraction]  # exact value, or None when undefined -> estimate
HALF = Fraction(1, 2)


class Node(NamedTuple):
    parents: Tuple[int, ...]
    cpt: Dict[Tuple[int, ...], Fraction]  # P(node = 1 | parent values)


def cooper_network(n: int, clauses: Sequence[Clause]) -> Tuple[List[Node], int]:
    """Cooper's network: roots, clause nodes, AND chain. Returns the nodes and the output index."""
    if not clauses:
        raise ValueError("the formula needs at least one clause")
    nodes = [Node((), {(): HALF}) for _ in range(n)]
    for cl in clauses:
        if not 1 <= len(cl) <= 3 or len({v for v, _ in cl}) != len(cl):
            raise ValueError("a clause has one to three literals on distinct variables")
        signs = [pos for _, pos in cl]
        cpt = {a: Fraction(int(any(bool(x) == s for x, s in zip(a, signs)))) for a in product((0, 1), repeat=len(cl))}
        nodes.append(Node(tuple(v for v, _ in cl), cpt))
    m = len(clauses)
    nodes.append(Node((n,), {(0,): Fraction(0), (1,): Fraction(1)}))
    for j in range(1, m):
        nodes.append(Node((n + m + j - 1, n + j), {(x, y): Fraction(x & y) for x in (0, 1) for y in (0, 1)}))
    return nodes, len(nodes) - 1


def probability_of(nodes: Sequence[Node], evidence: Dict[int, int]) -> Fraction:
    """P(evidence): the sum of P(x) over the full assignments x that agree with it, depth first
    in topological order; prefixes of probability 0 or against the evidence are cut."""
    total = Fraction(0)
    stack: List[Tuple[Tuple[int, ...], Fraction]] = [((), Fraction(1))]
    while stack:
        x, p = stack.pop()
        i = len(x)
        if i == len(nodes):
            total += p
            continue
        q = nodes[i].cpt[tuple(x[u] for u in nodes[i].parents)]
        for b, pb in ((1, q), (0, 1 - q)):
            if pb != 0 and evidence.get(i, b) == b:
                stack.append((x + (b,), p * pb))
    return total


def posterior(nodes: Sequence[Node], var: int, evidence: Dict[int, int]) -> Optional[Fraction]:
    """P(var = 1 | evidence), or None when P(evidence) = 0."""
    pe = probability_of(nodes, evidence)
    if pe == 0:
        return None
    return probability_of(nodes, {**evidence, var: 1}) / pe


def satisfies(q: Sequence[int], clauses: Sequence[Clause]) -> bool:
    return all(any(bool(q[v]) == pos for v, pos in cl) for cl in clauses)


def find_assignment(n: int, clauses: Sequence[Clause], oracle: Oracle) -> Optional[List[int]]:
    """The self-reduction. With an oracle whose answers are within eps < 1/2 of P(Q_i = 1 | Y = 1),
    it returns a satisfying assignment exactly when the formula is satisfiable, else None.
    Cost: n oracle calls on networks of n + 2m nodes, plus one check in O(n + m)."""
    nodes, y = cooper_network(n, clauses)
    q: List[int] = []
    for i in range(n):
        z = oracle(posterior(nodes, i, {y: 1}))
        b = 1 if z >= HALF else 0
        nodes[i] = Node((), {(): Fraction(b)})  # fix Q_i = b; the evidence stays the one node Y = 1
        q.append(b)
    return q if satisfies(q, clauses) else None


def absolute_oracle(eps: Fraction, rng: Random) -> Oracle:
    """An adversary that answers with an end point or the middle of [p - eps, p + eps] cut to [0, 1],
    and with anything when p is undefined."""
    def answer(p: Optional[Fraction]) -> Fraction:
        if p is None:
            return Fraction(rng.randint(0, 4), 4)
        lo, hi = max(Fraction(0), p - eps), min(Fraction(1), p + eps)
        return rng.choice((lo, hi, (lo + hi) / 2))
    return answer


def noisy_oracle(eps: Fraction, delta: float, rng: Random) -> Oracle:
    """Right (within eps) with probability 1/2 + delta; otherwise it gives the most misleading answer."""
    good = absolute_oracle(eps, rng)

    def answer(p: Optional[Fraction]) -> Fraction:
        if p is not None and rng.random() < 0.5 + delta:
            return good(p)
        return Fraction(1) if p is None or p < HALF else Fraction(0)
    return answer


def repetitions(n: int, delta: float) -> int:
    """An odd k with exp(-2 delta^2 k) <= 1/(4n): then the median of k answers is wrong with
    probability at most 1/(4n) (Hoeffding), and all n medians are right with probability >= 3/4."""
    return 2 * ceil(log(4 * n) / (4 * delta * delta)) + 1


def median_oracle(oracle: Oracle, k: int) -> Oracle:
    """Ask k times (k odd) and return the median: it lies in [p - eps, p + eps] when more than half do."""
    def answer(p: Optional[Fraction]) -> Fraction:
        return sorted(oracle(p) for _ in range(k))[k // 2]
    return answer


def decide_by_relative(n: int, clauses: Sequence[Clause], estimate: Callable[[Fraction], Fraction]) -> bool:
    """Any relative approximation Z of P(Y = 1), with P / (1 + eps) <= Z <= (1 + eps) P, is 0 exactly
    when P = 0, so the sign of one estimate decides satisfiability."""
    nodes, y = cooper_network(n, clauses)
    return estimate(probability_of(nodes, {y: 1})) > 0


def forward_sample(nodes: Sequence[Node], var: int, samples: int, rng: Random) -> Fraction:
    """The share of samples with var = 1, each node drawn given its parents in topological order.
    Without evidence it is within eps of P(var = 1) with probability >= 1 - delta for
    samples >= ln(2 / delta) / (2 eps^2), by Hoeffding."""
    hits = 0
    for _ in range(samples):
        x: List[int] = []
        for node in nodes:
            x.append(1 if rng.random() < node.cpt[tuple(x[u] for u in node.parents)] else 0)
        hits += x[var]
    return Fraction(hits, samples)


def samples_needed(eps: float, delta: float) -> int:
    return ceil(log(2 / delta) / (2 * eps * eps))
