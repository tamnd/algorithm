# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-packet-marking/. The authors are listed in prov/EZNZ9R.jsonl.

import random
from fractions import Fraction
from itertools import product

from probabilistic_packet_marking import (
    expected_packets,
    harmonic_bound,
    mark,
    paths,
    reconstruct,
    savage_estimate,
    send,
)

EMPTY = (None, None, 0)


def path_edges(path: list[str], v: str) -> set[tuple[str, str, int]]:
    d = len(path)
    nxt = path[1:] + [v]
    return {(path[i], nxt[i], d - 1 - i) for i in range(d)}


def test_example() -> None:
    path = ["R1", "R2", "R3", "R4"]
    # R2 marks; R3 and R4 do not.
    w = send(path, EMPTY, 0.25, [0.9, 0.1, 0.9, 0.9])
    assert w == ("R2", "R3", 2)
    # R4, next to the victim, marks.
    assert send(path, EMPTY, 0.25, [0.9, 0.9, 0.9, 0.1]) == ("R4", None, 0)
    # Nobody marks: the attacker's mark arrives, 4 hops further away.
    assert send(path, ("X", "Y", 3), 0.25, [0.9] * 4) == ("X", "Y", 7)
    marks = [("R4", None, 0), ("R3", "R4", 1), ("R2", "R3", 2), ("R1", "R2", 3), ("X", "Y", 7), ("X", "R9", 2)]
    kept = reconstruct(marks, "V")
    assert kept == path_edges(path, "V")
    assert paths(kept, "V") == {("R1", "R2", "R3", "R4", "V")}
    assert abs(float(expected_packets(10, Fraction(1, 25))) - 89.572) < 0.001
    assert abs(savage_estimate(10, 0.04) - 83.122) < 0.001
    assert abs(harmonic_bound(10, 0.04) - 105.734) < 0.001


def test_edges() -> None:
    assert reconstruct([], "V") == set()
    assert paths(set(), "V") == set()
    assert reconstruct([EMPTY], "V") == set()
    assert expected_packets(1, Fraction(1, 2)) == 2
    # d = 2, p = 1/2: q = 1/2 and 1/4, E = 2 + 4 - 4/3.
    assert expected_packets(2, Fraction(1, 2)) == Fraction(14, 3)
    # The distance saturates at 31.
    assert mark(("X", "Y", 31), "R", 0.5, 0.9) == ("X", "Y", 31)
    # A forged mark with distance 0 is completed by the first router.
    assert send(["R1", "R2"], ("X", None, 0), 0.5, [0.9, 0.9]) == ("X", "R1", 2)


def test_mark_distribution_exact() -> None:
    """Enumerate every marking decision and compare with q_j = p (1 - p)^j."""
    rng = random.Random(2000)
    for _ in range(500):
        d = rng.randrange(1, 7)
        p = Fraction(rng.randrange(1, 10), 10)
        path = [f"R{i}" for i in range(1, d + 1)]
        w0 = ("X", "Y", rng.randrange(0, 4))
        dist: dict[tuple, Fraction] = {}
        for bits in product((0, 1), repeat=d):
            us = [0.0 if b else 0.999999 for b in bits]
            w = send(path, w0, float(p), us)
            pr = Fraction(1)
            for b in bits:
                pr *= p if b else 1 - p
            dist[w] = dist.get(w, Fraction(0)) + pr
        want = {e: p * (1 - p) ** e[2] for e in ((path[i], (path[i + 1] if i + 1 < d else None), d - 1 - i) for i in range(d))}
        forged = (w0[0], w0[1] if w0[2] > 0 else path[0], w0[2] + d)
        want[forged] = (1 - p) ** d
        assert dist == want


def random_tree(rng: random.Random, n: int) -> dict[str, str]:
    """Parent links of a random tree of routers R1..Rn rooted at the victim V."""
    parent = {}
    names = [f"R{i}" for i in range(1, n + 1)]
    for i, r in enumerate(names):
        parent[r] = "V" if i == 0 or rng.random() < 0.2 else names[rng.randrange(0, i)]
    return parent


def test_reconstruct_random_trees() -> None:
    """Collect marks from several attackers until every edge has arrived; compare with the true graph."""
    rng = random.Random(295)
    for _ in range(500):
        parent = random_tree(rng, rng.randrange(1, 9))
        leaves = [r for r in parent if r not in parent.values()]
        attackers = rng.sample(leaves, rng.randrange(1, len(leaves) + 1))
        true_edges: set = set()
        routes = []
        for a in attackers:
            route = [a]
            while parent[route[-1]] != "V":
                route.append(parent[route[-1]])
            routes.append(route)
            true_edges |= path_edges(route, "V")
        p = rng.choice((0.2, 0.3, 0.5))
        marks = []
        seen: set = set()
        while not true_edges <= seen:
            route = routes[rng.randrange(len(routes))]
            w0 = (f"F{rng.randrange(3)}", "Y", rng.randrange(0, 3))
            w = send(route, w0, p, (rng.random() for _ in route))
            marks.append(w)
            if w[0] is not None:
                seen.add((w[0], "V" if w[2] == 0 else w[1], w[2]))
        kept = reconstruct(marks, "V")
        assert true_edges <= kept
        for x, y, k in kept - true_edges:
            assert x.startswith("F")  # only attacker marks add edges
            route = next(r for r in routes if y in r)
            assert k >= len(route) - route.index(y)  # and they sit beyond the valid suffix
        for chain in paths(kept, "V"):
            assert any(list(chain[len(chain) - 1 - len(r):-1]) == r for r in routes)


def test_convergence_monte_carlo() -> None:
    """The mean number of packets matches the exact expectation within 4 standard errors."""
    rng = random.Random(306)
    d, p = 5, Fraction(1, 5)
    path = [f"R{i}" for i in range(1, d + 1)]
    want = path_edges(path, "V")
    counts = []
    for _ in range(2000):
        seen: set = set()
        n = 0
        while len(seen) < d:
            w = send(path, EMPTY, float(p), (rng.random() for _ in path))
            n += 1
            if w[0] is not None:
                seen.add((w[0], "V" if w[2] == 0 else w[1], w[2]))
        assert seen == want
        counts.append(n)
    mean = sum(counts) / len(counts)
    var = sum((c - mean) ** 2 for c in counts) / (len(counts) - 1)
    exact = float(expected_packets(d, p))
    assert abs(mean - exact) < 4 * (var / len(counts)) ** 0.5
    assert exact <= harmonic_bound(d, float(p))


def test_bounds() -> None:
    rng = random.Random(25)
    for _ in range(40):
        d = rng.randrange(1, 9)
        p = Fraction(rng.randrange(1, 20), 20)
        assert float(expected_packets(d, p)) <= harmonic_bound(d, float(p)) + 1e-9
    # The printed estimate is not an upper bound for small d.
    assert float(expected_packets(2, Fraction(1, 25))) > savage_estimate(2, 0.04)
