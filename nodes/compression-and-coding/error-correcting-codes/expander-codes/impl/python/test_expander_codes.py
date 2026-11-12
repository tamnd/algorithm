# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expander-codes/. The authors are listed in prov/D5Z0XF.jsonl.

import itertools
import random
from fractions import Fraction

from expander_codes import (
    array_graph,
    expansion_profile,
    flip_decode,
    guaranteed_radius,
    random_biregular,
    variable_lists,
)

P, C = 7, 6
N = P * P
CHECKS = array_graph(P, C)
VAR = variable_lists(CHECKS, N)


def null_space(checks, n):
    rows = [sum(1 << j for j in row) for row in checks]
    pivots = {}
    for r in rows:
        for col, pr in pivots.items():
            if r >> col & 1:
                r ^= pr
        if r:
            col = r.bit_length() - 1
            for k in list(pivots):
                if pivots[k] >> col & 1:
                    pivots[k] ^= r
            pivots[col] = r
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        v = 1 << f
        for col, pr in pivots.items():
            if pr >> f & 1:
                v |= 1 << col
        basis.append([v >> j & 1 for j in range(n)])
    return basis


def test_graph_shape() -> None:
    assert len(CHECKS) == C * P and all(len(r) == P for r in CHECKS)
    assert all(len(v) == C for v in VAR)
    assert all(len(set(VAR[a]) & set(VAR[b])) <= 1 for a in range(N) for b in range(a + 1, N))


def test_measured_expansion() -> None:
    prof = expansion_profile(VAR, 4)
    # Pairs share at most one check, and three variables on a triangle lose three.
    assert prof == [None, 6, 11, 15, 18]
    radius, a, delta = guaranteed_radius(prof, C)
    assert (radius, a, delta) == (2, 3, Fraction(5, 6))
    # With c = 5 the same construction only guarantees one error.
    prof5 = expansion_profile(variable_lists(array_graph(7, 5), N), 4)
    assert guaranteed_radius(prof5, 5)[0] == 1
    # Two equal columns: every graph is a (1, 1) expander, but delta = 1 gives no guarantee.
    twin = [[0, 1], [0, 1], [2, 3], [2, 3]]
    tprof = expansion_profile(variable_lists(twin, 4), 2)
    assert tprof == [None, 2, 2] and guaranteed_radius(tprof, 2)[0] == 0


def test_profile_against_combinations() -> None:
    rng = random.Random(9)
    for n, c, d in ((12, 3, 4), (15, 2, 5), (16, 4, 8)):
        checks = random_biregular(n, c, d, rng)
        var = variable_lists(checks, n)
        assert all(len(v) == c for v in var) and all(len(set(r)) == d for r in checks)
        prof = expansion_profile(var, 3)
        for s in (1, 2, 3):
            ref = min(len({i for j in S for i in var[j]}) for S in itertools.combinations(range(n), s))
            assert prof[s] == ref


def test_unique_neighbor_lemma() -> None:
    # Every error set S with |S| <= A = 3 has a variable with more than c / 2
    # unsatisfied checks, so the decoder never gets stuck inside the radius.
    for s in (1, 2, 3):
        for S in itertools.combinations(range(N), s):
            odd = {i for i in range(len(CHECKS)) if sum(1 for j in CHECKS[i] if j in S) % 2}
            assert any(2 * sum(1 for i in VAR[j] if i in odd) > C for j in S)


def test_flip_decoder_within_radius() -> None:
    basis = null_space(CHECKS, N)
    assert len(basis) == 12
    rng = random.Random(4)
    for w in (0, 1, 2):
        for S in itertools.combinations(range(N), w):
            mix = [rng.randrange(2) for _ in basis]
            code = [sum(m * v[j] for m, v in zip(mix, basis)) % 2 for j in range(N)]
            assert all(sum(code[j] for j in row) % 2 == 0 for row in CHECKS)
            recv = [b ^ (j in S) for j, b in enumerate(code)]
            out, flips = flip_decode(CHECKS, N, recv)
            assert out == code
            assert flips <= C * w


def test_beyond_the_radius() -> None:
    # The guarantee stops at 2. Every weight 3 pattern still decodes here,
    # and with this seed 132 of 300 random weight 4 patterns do.
    rng = random.Random(6)
    assert all(not any(flip_decode(CHECKS, N, [int(j in S) for j in range(N)])[0])
               for S in (set(rng.sample(range(N), 3)) for _ in range(300)))
    ok = 0
    for _ in range(300):
        S = set(rng.sample(range(N), 4))
        out, _ = flip_decode(CHECKS, N, [int(j in S) for j in range(N)])
        ok += not any(out)
    assert 0 < ok < 300
