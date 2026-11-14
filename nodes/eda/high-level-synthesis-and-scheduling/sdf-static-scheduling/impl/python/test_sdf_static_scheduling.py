# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdf-static-scheduling/. The authors are listed in prov/XS6G6S.jsonl.

import random
from fractions import Fraction
from math import gcd, lcm

from sdf_static_scheduling import buffer_sizes, repetition_vector, schedule, topology_matrix

# A -(2, 3)-> B -(1, 2)-> C -(3, 1)-> A, with d tokens on the edge C -> A.
def ring(d):
    return [(0, 1, 2, 3, 0), (1, 2, 1, 2, 0), (2, 0, 3, 1, d)]


def null_space(rows, n):
    """Basis of {x : rows x = 0} over the rationals, by Gauss-Jordan elimination."""
    m = [[Fraction(v) for v in r] for r in rows]
    pivots = []
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = 1 / m[r][col]
        m[r] = [v * inv for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][col] != 0:
                f = m[i][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        pivots.append(col)
        r += 1
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for fcol in free:
        x = [Fraction(0)] * n
        x[fcol] = Fraction(1)
        for i, pc in enumerate(pivots):
            x[pc] = -m[i][fcol]
        basis.append(x)
    return basis


def least_positive(x):
    if all(v < 0 for v in x):
        x = [-v for v in x]
    if not all(v > 0 for v in x):
        return None
    k = lcm(*(v.denominator for v in x))
    ints = [int(v * k) for v in x]
    g = 0
    for v in ints:
        g = gcd(g, v)
    return [v // g for v in ints]


def run(edges, seq):
    """Token counts after each firing; fail if one goes negative."""
    tokens = [e[4] for e in edges]
    for a in seq:
        for i, (s, d, p, c, _) in enumerate(edges):
            if d == a:
                tokens[i] -= c
                assert tokens[i] >= 0
        for i, (s, d, p, c, _) in enumerate(edges):
            if s == a:
                tokens[i] += p
    return tokens


def some_period_exists(n, edges, q):
    """Brute force: search all orders of firings with counts at most q."""
    start = (tuple(e[4] for e in edges), tuple([0] * n))
    seen = {start}
    stack = [start]
    while stack:
        tokens, count = stack.pop()
        if list(count) == q:
            return True
        for a in range(n):
            if count[a] == q[a]:
                continue
            if any(d == a and tokens[i] < c for i, (s, d, p, c, _) in enumerate(edges)):
                continue
            t = list(tokens)
            for i, (s, d, p, c, _) in enumerate(edges):
                if d == a:
                    t[i] -= c
                if s == a:
                    t[i] += p
            cnt = list(count)
            cnt[a] += 1
            state = (tuple(t), tuple(cnt))
            if state not in seen:
                seen.add(state)
                stack.append(state)
    return False


def random_graph(rng: random.Random):
    n = rng.randint(1, 4)
    edges = []
    for b in range(1, n):
        a = rng.randrange(b)
        if rng.random() < 0.5:
            a, b = b, a
        edges.append((a, b, rng.randint(1, 3), rng.randint(1, 3), rng.randint(0, 4)))
    for _ in range(rng.randint(0, 3)):
        edges.append((rng.randrange(n), rng.randrange(n), rng.randint(1, 3), rng.randint(1, 3), rng.randint(0, 5)))
    return n, edges


def simple_cycles(n, edges):
    out = []

    def walk(s, v, path, seen):
        for i, e in enumerate(edges):
            if e[0] != v:
                continue
            if e[1] == s:
                out.append(path + [i])
            elif e[1] not in seen and e[1] > s:
                walk(s, e[1], path + [i], seen | {e[1]})

    for s in range(n):
        walk(s, s, [], {s})
    return out


def cycle_completes(edges, cyc, q):
    """Can the cycle alone, with its own initial tokens, fire each actor q times?"""
    sub = [edges[i] for i in cyc]
    actors = [e[0] for e in sub]
    tokens = [e[4] for e in sub]
    count = {a: 0 for a in actors}
    moved = True
    while moved:
        moved = False
        for j, a in enumerate(actors):
            k = (j - 1) % len(sub)  # the edge of the cycle that enters a
            if count[a] < q[a] and tokens[k] >= sub[k][3]:
                tokens[k] -= sub[k][3]
                tokens[j] += sub[j][2]
                count[a] += 1
                moved = True
    return all(count[a] == q[a] for a in actors)


def test_deadlock_exactly_when_a_cycle_is_short_of_tokens():
    rng = random.Random(1971)
    checked = 0
    for _ in range(1500):
        n, edges = random_graph(rng)
        q, seq = schedule(n, edges)
        if q is None or max(q) > 12:
            continue
        checked += 1
        short = any(not cycle_completes(edges, c, q) for c in simple_cycles(n, edges))
        assert (seq is None) == short
    assert checked > 400


def test_ring_example():
    assert topology_matrix(3, ring(0)) == [[2, -3, 0], [0, 1, -2], [-1, 0, 3]]
    assert repetition_vector(3, ring(0)) == [3, 2, 1]
    for d in range(3):
        assert schedule(3, ring(d)) == ([3, 2, 1], None)
    q, seq = schedule(3, ring(3))
    assert q == [3, 2, 1]
    assert seq == [0, 0, 0, 1, 1, 2]
    assert run(ring(3), seq) == [0, 0, 3]
    assert buffer_sizes(ring(3), seq) == [6, 2, 3]
    # Another valid order needs a smaller buffer on the first edge.
    assert run(ring(3), [0, 0, 1, 0, 1, 2]) == [0, 0, 3]
    assert buffer_sizes(ring(3), [0, 0, 1, 0, 1, 2]) == [4, 2, 3]


def test_inconsistent():
    edges = [(0, 1, 2, 3, 0), (1, 2, 1, 2, 0), (2, 0, 2, 1, 5)]
    assert repetition_vector(3, edges) is None
    assert schedule(3, edges) == (None, None)
    assert null_space(topology_matrix(3, edges), 3) == []


def test_chain_grows_exponentially():
    n = 12
    edges = [(i, i + 1, 2, 1, 0) for i in range(n - 1)]
    assert repetition_vector(n, edges) == [2 ** i for i in range(n)]


def test_random_against_null_space_and_search():
    rng = random.Random(1987)
    consistent = deadlocked = 0
    for _ in range(1500):
        n, edges = random_graph(rng)
        basis = null_space(topology_matrix(n, edges), n)
        q = repetition_vector(n, edges)
        if q is None:
            assert len(basis) == 0 or least_positive(basis[0]) is None
            assert schedule(n, edges) == (None, None)
            continue
        assert len(basis) == 1 and least_positive(basis[0]) == q
        consistent += 1
        if sum(q) > 40:
            continue
        q2, seq = schedule(n, edges)
        assert q2 == q
        exists = some_period_exists(n, edges, q)
        assert (seq is not None) == exists
        if seq is None:
            deadlocked += 1
            continue
        assert sorted(seq) == sorted(a for a in range(n) for _ in range(q[a]))
        assert run(edges, seq) == [e[4] for e in edges]
    assert consistent > 400 and deadlocked > 30
