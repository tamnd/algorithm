# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeny-based-cryptography/. The authors are listed in prov/BZ6XVD.jsonl.

import random
from collections import Counter

import pytest

from isogeny_based_cryptography import Curve, Fp2, cgl_hash, phi2, two_isogeny_graph, velu

P = 431


@pytest.fixture(scope="module")
def graph():
    return two_isogeny_graph(P, seed=1)


def test_modular_polynomial_over_the_integers():
    # j = 1728 is 2-isogenous to j = 287496 (= 66^3), and j = 8000 and j = -3375
    # have 2-isogenous endomorphisms (CM by sqrt(-2) and (1 + sqrt(-7)) / 2).
    assert phi2(1728, 287496) == 0
    assert phi2(8000, 8000) == 0
    assert phi2(-3375, -3375) == 0


def test_vertex_count(graph):
    adj, _ = graph
    # p = 11 mod 12, so there are floor(p / 12) + 2 supersingular j-invariants.
    assert len(adj) == P // 12 + 2 == 37
    assert sum(1 for j in adj if j.b == 0) == 21


def test_three_regular_and_edges_on_phi2(graph):
    adj, _ = graph
    for j, nb in adj.items():
        assert len(nb) == 3
        for j2 in nb:
            assert phi2(j, j2).is_zero()
            assert j in adj[j2]


def test_small_vertices(graph):
    adj, _ = graph
    j1728 = Fp2(1728, 0, P)
    assert j1728 == Fp2(4, 0, P)
    assert Counter(z.key() for z in adj[j1728]) == Counter({19: 2, 4: 1})
    assert Counter(z.key() for z in adj[Fp2(0, 0, P)]) == Counter({125: 3})


def test_velu_map_is_a_homomorphism():
    rng = random.Random(5)
    E = Curve(Fp2(1, 0, P), Fp2(0, 0, P))
    T = (Fp2(0, 0, P), Fp2(0, 0, P))  # (0, 0) has order 2
    E2, phi = velu(E, T, 2)
    for _ in range(5):
        A, B = E.random_point(rng), E.random_point(rng)
        lhs, rhs = phi(E.add(A, B)), E2.add(phi(A), phi(B))
        assert lhs == rhs
        X, Y = phi(A)
        assert Y * Y == E2.rhs(X)
    assert phi(T) is None


def test_cgl_hash(graph):
    adj, _ = graph
    start = Fp2(4, 0, P)
    previous = sorted(adj[start], key=lambda z: z.key())[0]
    rng = random.Random(9)
    outputs = Counter()
    for _ in range(2000):
        bits = [rng.randrange(2) for _ in range(16)]
        h = cgl_hash(bits, adj, start, previous)
        assert h in adj
        assert h == cgl_hash(bits, adj, start, previous)
        outputs[h.key()] += 1
    # Walks of 16 steps reach every vertex: the graph mixes fast.
    assert len(outputs) == 37
    # With 37 outputs, collisions are certain: the parameters are toy.
    assert max(outputs.values()) > 1


def test_worked_example(graph):
    adj, _ = graph
    start, previous = Fp2(19, 0, P), Fp2(4, 0, P)
    assert cgl_hash([1, 0, 1, 1, 0, 0, 1], adj, start, previous) == Fp2(141, 389, P)
    assert cgl_hash([1, 0, 1, 1, 0, 0, 0], adj, start, previous) == Fp2(422, 0, P)
    assert cgl_hash([0, 0, 1, 1, 0, 0, 1], adj, start, previous) == Fp2(422, 0, P)
