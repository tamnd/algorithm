# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-codeword-inapproximability/. The authors are listed in prov/2PHH3V.jsonl.

import random
from itertools import product

from nearest_codeword_inapproximability import (
    decode,
    false_count,
    is_total_cover,
    label_cover_to_ncp,
    lin_to_ncp,
    min_total_cover,
    ncp_opt,
)


def test_equations_example() -> None:
    # Each variable occurs twice, so the left sides add to 0, but the right sides add to 1: one must fail.
    eqs = [((0, 1, 2), 0), ((0, 3, 4), 0), ((1, 3, 5), 0), ((2, 4, 5), 1)]
    k, rows, rhs = lin_to_ncp(6, eqs)
    assert ncp_opt(k, rows, rhs)[0] == 1


def test_ncp_is_min_unsat() -> None:
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(3, 7)
        eqs = [(tuple(rng.sample(range(n), 3)), rng.randint(0, 1)) for _ in range(rng.randint(1, 12))]
        k, rows, rhs = lin_to_ncp(n, eqs)
        best_sat = max(
            sum((sum(bits[v] for v in vs) & 1) == b for vs, b in eqs) for bits in product((0, 1), repeat=n)
        )
        assert ncp_opt(k, rows, rhs)[0] == len(eqs) - best_sat


def random_instance(rng, planted):
    nu, nw, nl, nr = 2, 2, 3, 2
    lab_u = [rng.randrange(nl) for _ in range(nu)]
    lab_w = [rng.randrange(nr) for _ in range(nw)]
    edges = []
    for u in range(nu):
        for w in range(nw):
            proj = [rng.randrange(nr) for _ in range(nl)]
            if planted:
                proj[lab_u[u]] = lab_w[w]
            edges.append((u, w, tuple(proj)))
    return nu, nw, nl, nr, edges


def test_sizes() -> None:
    nu, nw, nl, nr, edges = random_instance(random.Random(1), True)
    k, rows, rhs, m = label_cover_to_ncp(nu, nw, nl, nr, edges)
    assert k == nu * nl + nw * nr == 10 and m == 11
    assert len(rows) == k + m * (len(edges) * nr + nw) == 10 + 11 * 10


def test_completeness_and_soundness() -> None:
    rng = random.Random(9)
    for trial in range(24):
        nu, nw, nl, nr, edges = random_instance(rng, trial % 2 == 0)
        k, rows, rhs, m = label_cover_to_ncp(nu, nw, nl, nr, edges)
        opt, x = ncp_opt(k, rows, rhs)
        cover = min_total_cover(nu, nw, nl, nr, edges)
        assert false_count(rows, rhs, x) == opt
        assert opt >= cover
        if opt < m:
            # All heavy equations hold, and the ones in x are a total cover.
            lu, lw = decode(nu, nw, nl, nr, x)
            assert is_total_cover(edges, lu, lw)
            assert opt == sum(map(len, lu)) + sum(map(len, lw))
        else:
            assert cover <= k < m
        if trial % 2 == 0:
            assert opt == cover == nu + nw  # one label per vertex
