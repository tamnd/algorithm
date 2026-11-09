# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-binary-decision-diagram/. The authors are listed in prov/DQZTGE.jsonl.

import random

from free_binary_decision_diagram import FALSE, FBDD, TRUE, hwb, probably_equal


def bits(n: int, a: int) -> list[int]:
    return [a >> i & 1 for i in range(n)]


def table(d: FBDD, root: int) -> list[int]:
    return [d.evaluate(root, bits(d.n, a)) for a in range(1 << d.n)]


def random_diagram(rng: random.Random, n: int, count: int, free: bool) -> tuple[FBDD, int]:
    """A random diagram. With free=True, a node never points to a node that tests its variable below."""
    d = FBDD(n)
    pool = [FALSE, TRUE]
    below = {FALSE: 0, TRUE: 0}
    for _ in range(count):
        v = rng.randrange(n)
        ok = [u for u in pool if not (free and below[u] >> v & 1)]
        u = d.mk(v, rng.choice(ok), rng.choice(ok))
        if u not in below:
            below[u] = below[d.nodes[u][1]] | below[d.nodes[u][2]] | 1 << v
            pool.append(u)
    return d, pool[-1]


def free_by_paths(d: FBDD, root: int) -> bool:
    stack = [(root, 0)]
    while stack:
        u, used = stack.pop()
        if u <= TRUE:
            continue
        v, lo, hi = d.nodes[u]
        if used >> v & 1:
            return False
        stack.append((lo, used | 1 << v))
        stack.append((hi, used | 1 << v))
    return True


def test_free_check_count_and_equivalence() -> None:
    rng = random.Random(1980)
    checked = 0
    for _ in range(600):
        n = rng.randrange(1, 9)
        free = rng.random() < 0.7
        d, f = random_diagram(rng, n, rng.randrange(1, 25), free)
        d.check_invariant()
        assert d.is_free(f) == free_by_paths(d, f)
        if free:
            assert d.is_free(f)
        t = table(d, f)
        if d.is_free(f):
            assert d.count(f) == sum(t)
            e, g = random_diagram(rng, n, rng.randrange(1, 25), True)
            assert probably_equal(d, f, e, g, rng) == (t == table(e, g))
            assert probably_equal(d, f, d, f, rng)
        checked += 1
    assert checked >= 500


def test_equal_functions_in_different_orders() -> None:
    rng = random.Random(77)
    for _ in range(100):
        n = rng.randrange(1, 7)
        t = [rng.randrange(2) for _ in range(1 << n)]
        roots = []
        diagrams = []
        for _ in range(2):  # a decision tree with a random variable at each node
            d = FBDD(n)
            stack: list[tuple[int, int, int, bool]] = [(0, 0, (1 << n) - 1, False)]
            done: dict[tuple[int, int], int] = {}
            pick: dict[tuple[int, int], int] = {}
            while stack:
                a, fixed, free_vars, ready = stack.pop()
                key = (a, fixed)
                if key in done:
                    continue
                if free_vars == 0:
                    done[key] = TRUE if t[a] else FALSE
                    continue
                if key not in pick:
                    pick[key] = rng.choice([i for i in range(n) if free_vars >> i & 1])
                v = pick[key]
                k0 = (a, fixed | 1 << v)
                k1 = (a | 1 << v, fixed | 1 << v)
                if ready:
                    done[key] = d.mk(v, done[k0], done[k1])
                    continue
                stack.append((a, fixed, free_vars, True))
                stack.append((a, fixed | 1 << v, free_vars & ~(1 << v), False))
                stack.append((a | 1 << v, fixed | 1 << v, free_vars & ~(1 << v), False))
            diagrams.append(d)
            roots.append(done[(0, 0)])
        assert all(d.is_free(r) for d, r in zip(diagrams, roots))
        assert table(diagrams[0], roots[0]) == t
        assert probably_equal(diagrams[0], roots[0], diagrams[1], roots[1], rng)


def test_hidden_weighted_bit() -> None:
    for n in range(1, 13):
        d, f = hwb(n)
        assert d.is_free(f)
        assert len(d.topo(f)) <= n * (n + 1)
        for a in range(1 << n):
            x = bits(n, a)
            s = sum(x)
            assert d.evaluate(f, x) == (0 if s == 0 else x[s - 1])
