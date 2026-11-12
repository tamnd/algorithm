# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/center-star-method/. The authors are listed in prov/3K9D30.jsonl.

import itertools
import random
from fractions import Fraction

from center_star_method import GAP, center_star_method, pairwise, sp_cost, unit_cost


def exact_sp(seqs: list[str], cost=unit_cost) -> int:
    """Oracle: minimum SP cost by dynamic programming over the k-dimensional lattice."""
    k = len(seqs)
    lens = [len(s) for s in seqs]
    best = {tuple([0] * k): 0}
    moves = [m for m in itertools.product((0, 1), repeat=k) if any(m)]
    for v in sorted(itertools.product(*[range(n + 1) for n in lens]), key=sum):
        if v not in best:
            continue
        for m in moves:
            w = tuple(a + b for a, b in zip(v, m))
            if any(w[i] > lens[i] for i in range(k)):
                continue
            col = [seqs[i][v[i]] if m[i] else GAP for i in range(k)]
            c = sum(cost(col[i], col[j]) for i in range(k) for j in range(i + 1, k))
            if best[v] + c < best.get(w, float("inf")):
                best[w] = best[v] + c
    return best[tuple(lens)]


def all_pair_alignments(s: str, t: str):
    """Oracle: every global alignment of s and t without gap-gap columns."""
    if not s and not t:
        yield "", ""
        return
    if s and t:
        for a, b in all_pair_alignments(s[1:], t[1:]):
            yield s[0] + a, t[0] + b
    if s:
        for a, b in all_pair_alignments(s[1:], t):
            yield s[0] + a, GAP + b
    if t:
        for a, b in all_pair_alignments(s, t[1:]):
            yield GAP + a, t[0] + b


def is_alignment_of(rows: list[str], seqs: list[str]) -> bool:
    if len(rows) != len(seqs):
        return False
    if rows and len({len(r) for r in rows}) != 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def induced_cost(r1: str, r2: str, cost=unit_cost) -> int:
    return sum(cost(x, y) for x, y in zip(r1, r2) if not (x == GAP and y == GAP))


def test_example() -> None:
    seqs = ["ACGTAC", "ACGGTAC", "AGTAC", "CGTTAC"]
    rows = center_star_method(seqs)
    assert rows == ["AC-G-TAC", "ACGG-TAC", "A--G-TAC", "-C-GTTAC"]
    assert sp_cost(rows) == 12
    assert exact_sp(seqs) == 11


def test_tight_for_three() -> None:
    seqs = ["A", "AC", "AA"]
    rows = center_star_method(seqs)
    assert rows == ["-A-", "-AC", "AA-"]
    assert sp_cost(rows) == 4 and exact_sp(seqs) == 3


def test_edges() -> None:
    assert center_star_method([]) == []
    assert center_star_method(["ACG"]) == ["ACG"]
    assert center_star_method(["", ""]) == ["", ""]
    assert center_star_method(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    rows = center_star_method(["", "A", "AA"])
    assert is_alignment_of(rows, ["", "A", "AA"])


def test_pairwise_against_enumeration() -> None:
    rng = random.Random(11)
    for _ in range(300):
        s = "".join(rng.choice("AC") for _ in range(rng.randint(0, 4)))
        t = "".join(rng.choice("AC") for _ in range(rng.randint(0, 4)))
        d, a, b = pairwise(s, t, unit_cost)
        best = min(induced_cost(x, y) for x, y in all_pair_alignments(s, t))
        assert d == best == induced_cost(a, b)
        assert a.replace(GAP, "") == s and b.replace(GAP, "") == t


def test_projection_and_bound_against_exact_sp() -> None:
    rng = random.Random(2024)
    worst = Fraction(0)
    for _ in range(500):
        k = rng.choice([3, 3, 3, 4])
        seqs = ["".join(rng.choice("ACG") for _ in range(rng.randint(0, 4 if k == 3 else 3))) for _ in range(k)]
        rows = center_star_method(seqs)
        assert is_alignment_of(rows, seqs)
        dist = [[pairwise(a, b, unit_cost)[0] for b in seqs] for a in seqs]
        c = min(range(k), key=lambda i: (sum(dist[i]), i))
        for i in range(k):
            assert induced_cost(rows[c], rows[i]) == dist[c][i]
        opt = exact_sp(seqs)
        got = sp_cost(rows)
        assert opt <= got
        assert got * k <= (2 * k - 2) * opt
        if opt:
            worst = max(worst, Fraction(got, opt))
    assert worst <= Fraction(3, 2)


def test_weighted_metric() -> None:
    def cost(x: str, y: str) -> int:
        if x == y:
            return 0
        if GAP in (x, y):
            return 2
        return 3

    rng = random.Random(7)
    for _ in range(200):
        seqs = ["".join(rng.choice("AT") for _ in range(rng.randint(1, 4))) for _ in range(3)]
        rows = center_star_method(seqs, cost)
        assert is_alignment_of(rows, seqs)
        assert 3 * sp_cost(rows, cost) <= 4 * exact_sp(seqs, cost)
