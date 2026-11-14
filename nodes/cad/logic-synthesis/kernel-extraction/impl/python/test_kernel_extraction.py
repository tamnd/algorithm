# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-extraction/. The authors are listed in prov/6VFGF9.jsonl.

import itertools
import random

from kernel_extraction import (
    best_rectangle,
    divide_by_cube,
    evaluate,
    extract,
    is_cube_free,
    kernel_cube_matrix,
    kernels,
    network_literals,
    value,
)


def lit(name: str) -> int:
    neg = name.endswith("'")
    return 2 * (ord(name[0]) - ord("a")) + (1 if neg else 0)


def sop(text: str) -> frozenset:
    out = []
    for term in text.replace(" ", "").split("+"):
        lits = []
        i = 0
        while i < len(term):
            j = i + 2 if i + 1 < len(term) and term[i + 1] == "'" else i + 1
            lits.append(lit(term[i:j]))
            i = j
        out.append(frozenset(lits))
    return frozenset(out)


def all_cubes(variables):
    for choice in itertools.product((None, 0, 1), repeat=len(variables)):
        yield frozenset(2 * v + c for v, c in zip(variables, choice) if c is not None)


def brute_kernels(f):
    """Every cube divisor c of f whose quotient is cube-free."""
    variables = sorted({l >> 1 for c in f for l in c})
    return {(c, divide_by_cube(f, c)) for c in all_cubes(variables) if is_cube_free(divide_by_cube(f, c))}


def random_sop(rng, variables, lo, hi, maxlen):
    out = set()
    for _ in range(rng.randrange(lo, hi + 1)):
        k = rng.randrange(1, min(maxlen, len(variables)) + 1)
        out.add(frozenset(2 * v + rng.randrange(2) for v in rng.sample(variables, k)))
    return frozenset(out)


def brute_best_rectangle(rows) -> int:
    best = 0

    def grow(chosen, common, start):
        nonlocal best
        if chosen:
            cols = sorted(common, key=lambda c: sorted(c))
            for k in range(2, len(cols) + 1):
                for sub in itertools.combinations(cols, k):
                    best = max(best, value(rows, chosen, list(sub)))
        for s in range(start, len(rows)):
            nxt = rows[s][2] if not chosen else common & rows[s][2]
            if len(nxt) >= 2:
                grow(chosen + [s], nxt, s + 1)

    grow([], frozenset(), 0)
    return best


def same_network(old, new, inputs) -> bool:
    for bits in itertools.product((0, 1), repeat=len(inputs)):
        point = dict(zip(inputs, bits))
        a, b = evaluate(old, point), evaluate(new, point)
        if any(a[v] != b[v] for v in old):
            return False
    return True


def test_page_example() -> None:
    net = {10: sop("ac + ad + bc + bd + e"), 11: sop("cf + df + g")}
    rows, cols = kernel_cube_matrix(net)
    assert len(rows) == 7 and len(cols) == 12
    val, chosen, cubes = best_rectangle(rows)
    assert val == 4 and cubes == [frozenset([lit("c")]), frozenset([lit("d")])]
    assert sorted((rows[r][0], sorted(rows[r][1])) for r in chosen) == [(10, [0]), (10, [2]), (11, [10])]
    new, log = extract(net, 12)
    assert log == [4] and network_literals(net) == 14 and network_literals(new) == 10
    assert new[12] == sop("c + d")
    assert same_network(net, new, list(range(7)))


def test_kernels_of_products_of_binomials() -> None:
    for k in range(1, 5):
        f = frozenset([frozenset()])
        for i in range(k):
            f = frozenset(c | {l} for c in f for l in (4 * i, 4 * i + 2))
        pairs = kernels(f)
        assert len(pairs) == 3 ** k - 2 ** k
        assert len({ker for _, ker in pairs}) == 2 ** k - 1


def test_kernels_edge_cases() -> None:
    assert kernels(frozenset()) == []
    assert kernels(sop("abc")) == []
    assert kernels(sop("a + b")) == [(frozenset(), sop("a + b"))]
    assert set(kernels(sop("ab + ac"))) == {(frozenset([lit("a")]), sop("b + c"))}


def test_kernels_against_all_cube_divisors() -> None:
    rng = random.Random(5)
    for _ in range(600):
        n = rng.randrange(2, 6)
        f = random_sop(rng, list(range(n)), 1, 6, 3)
        got = kernels(f)
        assert len(got) == len(set(got))
        assert set(got) == brute_kernels(f)


def planted_network(rng, nodes, nv, k):
    """Nodes that are sums of cokernel x kernel products from a shared pool, plus noise."""
    variables = list(range(nv))
    pool = [random_sop(rng, variables, 2, 3, 2) for _ in range(k)]
    net = {}
    for i in range(nodes):
        cubes = set()
        for _ in range(rng.randrange(1, 3)):
            ker = rng.choice(pool)
            kv = {l >> 1 for c in ker for l in c}
            free = [v for v in variables if v not in kv]
            if not free:
                continue
            size = rng.randrange(1, min(2, len(free)) + 1)
            cok = frozenset(2 * v + rng.randrange(2) for v in rng.sample(free, size))
            cubes |= {cok | c for c in ker}
        cubes |= set(random_sop(rng, variables, 1, 2, 3))
        net[100 + i] = frozenset(cubes)
    return net


def test_kernel_theorem() -> None:
    rng = random.Random(9)
    meets = 0
    for t in range(400):
        variables = list(range(4))
        if t % 2:
            f = random_sop(rng, variables, 2, 5, 3)
            g = random_sop(rng, variables, 2, 5, 3)
        else:
            f, g = planted_network(rng, 2, 4, 1).values()
        meet = any(len(kf & kg) >= 2 for _, kf in kernels(f) for _, kg in kernels(g))
        subs = set()
        for c in f | g:
            for k in range(len(c) + 1):
                subs.update(frozenset(s) for s in itertools.combinations(sorted(c), k))

        def divides(h, d):
            sd = {l >> 1 for c in d for l in c}
            first = next(iter(d))
            cands = {c - first for c in h if first <= c}
            return any(not {l >> 1 for l in q} & sd and all(q | di in h for di in d) for q in cands)

        share = any(divides(f, frozenset(p)) and divides(g, frozenset(p)) for p in itertools.combinations(sorted(subs, key=sorted), 2))
        assert meet == share
        meets += meet
    assert meets >= 100


def test_greedy_rectangle_against_brute_force() -> None:
    rng = random.Random(21)
    equal = 0
    for t in range(300):
        if t % 2:
            net = {10 + i: random_sop(rng, list(range(5)), 2, 4, 3) for i in range(2)}
        else:
            net = planted_network(rng, 3, 6, 2)
        rows, _ = kernel_cube_matrix(net)
        if len(rows) > 18:
            continue
        val, chosen, cubes = best_rectangle(rows)
        best = brute_best_rectangle(rows)
        assert 0 <= val <= best
        if chosen:
            assert len(cubes) >= 2 and val == value(rows, chosen, cubes)
            assert all(set(cubes) <= rows[r][2] for r in chosen)
        equal += val == best
    assert equal >= 200


def test_extraction_keeps_functions_and_counts_literals() -> None:
    rng = random.Random(33)
    changed = 0
    for t in range(500):
        if t % 2:
            variables = list(range(rng.randrange(3, 7)))
            net = {20 + i: random_sop(rng, variables, 2, 5, 3) for i in range(rng.randrange(1, 4))}
        else:
            variables = list(range(7))
            net = planted_network(rng, 3, 7, 2)
        new, log = extract(net, 300)
        changed += bool(log)
        assert all(v > 0 for v in log)
        assert network_literals(new) == network_literals(net) - sum(log)
        assert len(new) == len(net) + len(log)
        assert same_network(net, new, variables)
    assert changed >= 150
