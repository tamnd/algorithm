# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrofitting-word-vectors/. The authors are listed in prov/TKNXEG.jsonl.

import math
import random

from retrofitting_word_vectors import (
    objective,
    retrofit,
    solve_direct,
    solve_linear,
    update,
)

TOL = 1e-9


def max_diff(p, q):
    return max(abs(x - y) for w in p for x, y in zip(p[w], q[w]))


def random_case(rng, n=12, d=4, p=0.3):
    words = [f"w{i:02d}" for i in range(n)]
    vectors = {w: [rng.uniform(-1, 1) for _ in range(d)] for w in words}
    lexicon = {w: [] for w in words}
    for a in range(n):
        for b in range(a + 1, n):
            if rng.random() < p:
                lexicon[words[a]].append(words[b])
                lexicon[words[b]].append(words[a])
    lexicon["w00"].append("not-in-vocabulary")
    return vectors, lexicon


def test_chain_hand_values():
    vectors = {"a": [0.0], "b": [0.0], "c": [4.0]}
    lexicon = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
    exact = solve_direct(vectors, lexicon)
    assert abs(exact["a"][0] - 1 / 3) < TOL
    assert abs(exact["b"][0] - 2 / 3) < TOL
    assert abs(exact["c"][0] - 7 / 3) < TOL
    one = retrofit(vectors, lexicon, iterations=1, jacobi=True)
    assert [one[w][0] for w in "abc"] == [0.0, 1.0, 2.0]
    two = retrofit(vectors, lexicon, iterations=2, jacobi=True)
    assert [two[w][0] for w in "abc"] == [0.5, 0.5, 2.5]
    gs = retrofit(vectors, lexicon, iterations=1)
    assert [gs[w][0] for w in "abc"] == [0.0, 1.0, 2.5]


def test_iteration_converges_to_direct_solve():
    rng = random.Random(1)
    for _ in range(5):
        vectors, lexicon = random_case(rng)
        exact = solve_direct(vectors, lexicon)
        for jacobi in (False, True):
            got = retrofit(vectors, lexicon, iterations=60, jacobi=jacobi)
            assert max_diff(got, exact) < 1e-12


def test_jacobi_contracts_by_half():
    rng = random.Random(2)
    vectors, lexicon = random_case(rng)
    exact = solve_direct(vectors, lexicon)
    prev = max_diff(vectors, exact)
    q = {w: list(v) for w, v in vectors.items()}
    nbs = {w: sorted({u for u in lexicon[w] if u in vectors}) for w in vectors}
    for _ in range(8):
        q = {w: (update(w, q, vectors, nbs[w]) if nbs[w] else vectors[w]) for w in vectors}
        err = max_diff(q, exact)
        assert err <= 0.5 * prev + 1e-15
        prev = err


def test_gauss_seidel_not_slower_than_bound():
    rng = random.Random(3)
    vectors, lexicon = random_case(rng)
    exact = solve_direct(vectors, lexicon)
    e0 = max_diff(vectors, exact)
    for t in range(1, 8):
        got = retrofit(vectors, lexicon, iterations=t)
        assert max_diff(got, exact) <= 0.5 ** t * e0 + 1e-15


def test_words_outside_lexicon_unchanged():
    vectors = {"x": [1.0, 2.0], "y": [3.0, -1.0], "lonely": [5.0, 5.0], "z": [0.5, 0.5]}
    lexicon = {"x": ["y", "ghost"], "y": ["x"], "z": ["ghost"]}
    got = retrofit(vectors, lexicon)
    assert got["lonely"] == [5.0, 5.0]
    assert got["z"] == [0.5, 0.5]
    assert got["x"] != [1.0, 2.0]


def test_update_matches_released_code_formula():
    # retrofit.py: newVec = (numNeighbours * q_hat + sum of neighbours) / (2 * numNeighbours)
    rng = random.Random(4)
    vectors, lexicon = random_case(rng)
    q = {w: [rng.uniform(-1, 1) for _ in range(4)] for w in vectors}
    for w in vectors:
        nb = sorted({u for u in lexicon[w] if u in vectors})
        if not nb:
            continue
        ref = [(len(nb) * vectors[w][t] + sum(q[u][t] for u in nb)) / (2 * len(nb)) for t in range(4)]
        got = update(w, q, vectors, nb)
        assert max(abs(x - y) for x, y in zip(got, ref)) < 1e-12


def test_symmetric_weights_minimize_objective():
    rng = random.Random(5)
    vectors, lexicon = random_case(rng, n=10, d=3)
    del lexicon["w00"][-1]
    ones = lambda i, j, deg: 1.0  # noqa: E731
    best = solve_direct(vectors, lexicon, beta=ones)
    psi = objective(best, vectors, lexicon)
    h = 1e-6
    for w in vectors:
        for t in range(3):
            plus = {u: list(v) for u, v in best.items()}
            minus = {u: list(v) for u, v in best.items()}
            plus[w][t] += h
            minus[w][t] -= h
            grad = (objective(plus, vectors, lexicon) - objective(minus, vectors, lexicon)) / (2 * h)
            assert abs(grad) < 1e-5
    for _ in range(20):
        other = {u: [x + rng.gauss(0, 0.1) for x in v] for u, v in best.items()}
        assert objective(other, vectors, lexicon) > psi
    got = retrofit(vectors, lexicon, iterations=80, beta=ones)
    assert max_diff(got, best) < 1e-9


def test_lexicon_clusters_move_together():
    rng = random.Random(6)
    a = [f"a{i}" for i in range(6)]
    b = [f"b{i}" for i in range(6)]
    vectors = {w: [rng.gauss(0, 1) for _ in range(8)] for w in a + b}
    lexicon = {w: [u for u in grp if u != w] for grp in (a, b) for w in grp}

    def spread(q, grp):
        pairs = [(u, v) for k, u in enumerate(grp) for v in grp[k + 1:]]
        return sum(math.dist(q[u], q[v]) for u, v in pairs) / len(pairs)

    got = retrofit(vectors, lexicon)
    for grp in (a, b):
        assert spread(got, grp) < 0.6 * spread(vectors, grp)


def test_solve_linear_against_known_system():
    x = solve_linear([[2.0, 1.0], [1.0, 3.0]], [[3.0], [5.0]])
    assert abs(x[0][0] - 0.8) < TOL and abs(x[1][0] - 1.4) < TOL
