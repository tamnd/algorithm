# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felsenstein-pruning/. The authors are listed in prov/9J75HR.jsonl.

import itertools
import math
import random
from fractions import Fraction

from felsenstein_pruning import (
    conditional_likelihoods,
    felsenstein_pruning,
    jc69_matrix,
    jc69_matrix_from_x,
    postorder,
    site_log_likelihood,
    tree_log_likelihood,
)


def random_tree(n, rng):
    """A random rooted tree on leaves 0 .. n-1; most joins are binary, some are ternary."""
    nodes = list(range(n))
    children = {}
    nxt = n
    while len(nodes) > 1:
        r = 3 if len(nodes) >= 3 and rng.random() < 0.2 else 2
        picked = rng.sample(nodes, r)
        for v in picked:
            nodes.remove(v)
        children[nxt] = picked
        nodes.append(nxt)
        nxt += 1
    return children, nodes[0]


def brute_force(children, root, P, pi, site):
    """Sum over all states of the internal nodes of pi(root) times the product over branches."""
    k = len(pi)
    internal = [v for v in postorder(children, root) if children.get(v)]
    total = 0
    for states in itertools.product(range(k), repeat=len(internal)):
        s = dict(site)
        s.update(zip(internal, states))
        prob = pi[s[root]]
        for v, kids in children.items():
            for c in kids:
                prob *= P[c][s[v]][s[c]]
        total += prob
    return total


def expm_series(Q, t):
    """exp(Qt) by a Taylor series with scaling and squaring (reference only)."""
    k = len(Q)
    j = 0
    while max(abs(Q[a][b]) * t for a in range(k) for b in range(k)) / 2 ** j > 0.1:
        j += 1
    A = [[Q[a][b] * t / 2 ** j for b in range(k)] for a in range(k)]
    E = [[1.0 if a == b else 0.0 for b in range(k)] for a in range(k)]
    term = [row[:] for row in E]
    for i in range(1, 30):
        term = [[sum(term[a][c] * A[c][b] for c in range(k)) / i for b in range(k)] for a in range(k)]
        E = [[E[a][b] + term[a][b] for b in range(k)] for a in range(k)]
    for _ in range(j):
        E = [[sum(E[a][c] * E[c][b] for c in range(k)) for b in range(k)] for a in range(k)]
    return E


def test_jc69_closed_form_is_the_matrix_exponential():
    Q = [[-1.0 if a == b else 1.0 / 3.0 for b in range(4)] for a in range(4)]
    for t in [0.0, 0.01, 0.1, 0.5, 1.0, 3.0]:
        E = expm_series(Q, t)
        J = jc69_matrix(t)
        for a in range(4):
            assert abs(sum(J[a]) - 1.0) < 1e-15
            for b in range(4):
                assert abs(E[a][b] - J[a][b]) < 1e-13


def test_worked_example():
    children = {"r": ["u", "w"], "u": ["1", "2"], "w": ["3", "4"]}
    t = {"u": 0.1, "w": 0.2, "1": 0.1, "2": 0.2, "3": 0.1, "4": 0.3}
    P = {v: jc69_matrix(x) for v, x in t.items()}
    site = {"1": 0, "2": 1, "3": 0, "4": 0}
    L = conditional_likelihoods(children, "r", P, site, 4)
    assert abs(L["u"][0] - 0.0530395) < 1e-7
    assert abs(L["u"][1] - 0.0257282) < 1e-7
    assert abs(L["w"][0] - 0.682269) < 1e-6
    assert abs(L["r"][0] - 0.0275791) < 1e-7
    value = felsenstein_pruning(children, "r", P, [0.25] * 4, site)
    assert abs(value - 0.00724868) < 1e-8
    assert abs(value - brute_force(children, "r", P, [0.25] * 4, site)) < 1e-15


def test_exact_jc69_against_brute_force():
    rng = random.Random(1)
    pi = [Fraction(1, 4)] * 4
    for _ in range(60):
        n = rng.randint(2, 5)
        children, root = random_tree(n, rng)
        P = {c: jc69_matrix_from_x(Fraction(rng.randint(1, 19), 20)) for kids in children.values() for c in kids}
        site = {v: rng.randrange(4) for v in range(n)}
        assert felsenstein_pruning(children, root, P, pi, site) == brute_force(children, root, P, pi, site)


def test_exact_general_matrices_against_brute_force():
    rng = random.Random(2)
    for _ in range(60):
        k = rng.randint(2, 4)
        n = rng.randint(2, 5)
        children, root = random_tree(n, rng)
        w = [rng.randint(1, 9) for _ in range(k)]
        pi = [Fraction(x, sum(w)) for x in w]
        P = {}
        for kids in children.values():
            for c in kids:
                rows = []
                for _a in range(k):
                    r = [rng.randint(1, 9) for _ in range(k)]
                    rows.append([Fraction(x, sum(r)) for x in r])
                P[c] = rows
        site = {v: rng.randrange(k) for v in range(n)}
        assert felsenstein_pruning(children, root, P, pi, site) == brute_force(children, root, P, pi, site)


def test_float_jc69_against_brute_force():
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(2, 5)
        children, root = random_tree(n, rng)
        P = {c: jc69_matrix(rng.uniform(0.0, 2.0)) for kids in children.values() for c in kids}
        site = {v: rng.randrange(4) for v in range(n)}
        a = felsenstein_pruning(children, root, P, [0.25] * 4, site)
        b = brute_force(children, root, P, [0.25] * 4, site)
        assert abs(a - b) <= 1e-12 * b
        assert abs(site_log_likelihood(children, root, P, [0.25] * 4, site) - math.log(b)) < 1e-10


def test_pulley_principle_exact():
    # Root on the branch u-w, split as (x1, x2); moving the root keeps x1 * x2 = exp(-4 t / 3).
    pi = [Fraction(1, 4)] * 4
    leaf_x = {1: Fraction(9, 10), 2: Fraction(4, 5), 3: Fraction(7, 10), 4: Fraction(1, 2)}
    rng = random.Random(4)
    for _ in range(30):
        site = {v: rng.randrange(4) for v in leaf_x}
        values = set()
        for x1, x2 in [(Fraction(1), Fraction(3, 5)), (Fraction(3, 4), Fraction(4, 5)), (Fraction(3, 5), Fraction(1))]:
            children = {"r": ["u", "w"], "u": [1, 2], "w": [3, 4]}
            P = {v: jc69_matrix_from_x(x) for v, x in leaf_x.items()}
            P["u"], P["w"] = jc69_matrix_from_x(x1), jc69_matrix_from_x(x2)
            values.add(felsenstein_pruning(children, "r", P, pi, site))
        # the root at leaf 1's parent: u has children 1, 2 and w
        children = {"u": [1, 2, "w"], "w": [3, 4]}
        P = {v: jc69_matrix_from_x(x) for v, x in leaf_x.items()}
        P["w"] = jc69_matrix_from_x(Fraction(3, 5))
        values.add(felsenstein_pruning(children, "u", P, pi, site))
        assert len(values) == 1


def test_missing_data_sums_over_states():
    rng = random.Random(5)
    pi = [Fraction(1, 4)] * 4
    for _ in range(20):
        children, root = random_tree(4, rng)
        P = {c: jc69_matrix_from_x(Fraction(rng.randint(1, 9), 10)) for kids in children.values() for c in kids}
        site = {v: rng.randrange(4) for v in range(4)}
        site[0] = None
        total = 0
        for a in range(4):
            s = dict(site)
            s[0] = a
            total += felsenstein_pruning(children, root, P, pi, s)
        assert felsenstein_pruning(children, root, P, pi, site) == total


def test_patterns_and_scaling_on_a_deep_tree():
    rng = random.Random(6)
    n = 500
    children = {}
    prev = 0
    for i in range(1, n):
        children[n + i] = [prev, i]
        prev = n + i
    root = prev
    xs = {c: Fraction(rng.randint(5, 9), 10) for kids in children.values() for c in kids}
    P = {c: jc69_matrix_from_x(x) for c, x in xs.items()}
    Pf = {c: [[float(e) for e in row] for row in m] for c, m in P.items()}
    pi = [Fraction(1, 4)] * 4
    alignment = {v: [rng.randrange(4) for _ in range(3)] for v in range(n)}
    alignment = {v: s + s[:1] for v, s in alignment.items()}
    want = 0.0
    for j, weight in [(0, 2), (1, 1), (2, 1)]:
        site = {v: alignment[v][j] for v in range(n)}
        exact = felsenstein_pruning(children, root, P, pi, site)
        log_exact = math.log(exact.numerator) - math.log(exact.denominator)
        want += weight * log_exact
        assert log_exact < -745
        assert felsenstein_pruning(children, root, Pf, [0.25] * 4, site) == 0.0
    got = tree_log_likelihood(children, root, Pf, [0.25] * 4, alignment)
    assert abs(got - want) < 1e-9 * abs(want)
