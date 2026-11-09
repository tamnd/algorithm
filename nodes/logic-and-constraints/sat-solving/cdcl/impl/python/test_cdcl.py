# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cdcl/. The authors are listed in prov/H3D7MV.jsonl.

import random

from cdcl import Solver, cdcl, luby


def truth_table(n: int, clauses: list[list[int]]) -> tuple[int, list[int]]:
    """Bit a of the result is 1 when assignment a (bit v-1 of a is x_v)
    satisfies every clause. Brute force over all 2^n assignments."""
    size = 1 << n
    full = (1 << size) - 1
    xs = []
    for v in range(n):
        period = 1 << (v + 1)
        block = ((1 << (1 << v)) - 1) << (1 << v)
        unit = sum(1 << (i * period) for i in range(size // period))
        xs.append(block * unit)
    f = full
    for c in clauses:
        f &= clause_bits(c, xs, full)
    return f, xs


def clause_bits(c: list[int], xs: list[int], full: int) -> int:
    b = 0
    for lit in c:
        b |= xs[lit - 1] if lit > 0 else full ^ xs[-lit - 1]
    return b


def implied(n: int, clauses: list[list[int]], c: list[int]) -> bool:
    f, xs = truth_table(n, clauses)
    full = (1 << (1 << n)) - 1
    return f & (full ^ clause_bits(c, xs, full)) == 0


def satisfies(model: list[int], clauses: list[list[int]]) -> bool:
    s = set(model)
    return all(any(lit in s for lit in c) for c in clauses)


def random_ksat(rng: random.Random, n: int, m: int, k: int = 3) -> list[list[int]]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), min(k, n))
        out.append([v if rng.random() < 0.5 else -v for v in vs])
    return out


def pigeonhole(p: int, h: int) -> tuple[int, list[list[int]]]:
    """p pigeons, h holes; x(i, j) = i*h + j + 1 says pigeon i sits in hole j."""
    x = lambda i, j: i * h + j + 1  # noqa: E731
    cl = [[x(i, j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a + 1, p):
                cl.append([-x(a, j), -x(b, j)])
    return p * h, cl


OPTIONS = [
    {},
    {"restart": None, "minimize": False},
    {"restart": "luby", "restart_unit": 1, "reduce_first": 4, "reduce_inc": 1},
    {"restart": "glucose", "reduce_first": 6, "reduce_inc": 2},
]


def check_run(n: int, clauses: list[list[int]], opts: dict, expect_sat: bool | None) -> None:
    s = Solver(n, clauses, check=True, **opts)
    model = s.solve()
    if expect_sat is not None:
        assert (model is not None) == expect_sat
    if model is not None:
        assert len(model) == n and satisfies(model, clauses)
    if n <= 12:
        for c in s.learned_log:
            assert implied(n, clauses, c), c


def test_luby() -> None:
    assert [luby(i) for i in range(1, 16)] == [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8]


def test_page_example() -> None:
    f = [[1, 2], [1, 3, 7], [-2, -3, 4], [-4, 5, 8], [-4, 6, 9], [-5, -6]]
    s = Solver(9, f, restart=None, check=True)
    s.decide(-7)
    s.decide(-8)
    s.decide(-9)
    assert s.propagate() is None
    s.decide(-1)
    confl = s.propagate()
    assert confl is not None
    assert s.trail == [-7, -8, -9, -1, 2, 3, 4, 5, 6]
    learnt, b, lbd = s.analyze(confl)
    assert sorted(learnt) == [-4, 8, 9] and learnt[0] == -4
    assert (b, lbd) == (3, 3)
    model = cdcl(9, f)
    assert model is not None and satisfies(model, f)


def test_hand_cases() -> None:
    assert cdcl(0, []) == []
    assert cdcl(0, [[]]) is None
    assert cdcl(1, [[1], [-1]]) is None
    assert cdcl(2, [[1, 2], [-1, 2], [1, -2], [-1, -2]]) is None
    assert cdcl(3, [[1, -1], [2]]) in ([-1, 2, -3], [1, 2, -3], [-1, 2, 3], [1, 2, 3])
    assert cdcl(2, [[1, 1, 2], [-2]]) == [1, -2]
    for opts in OPTIONS:
        check_run(3, [[1, 2, 3], [-1, -2], [-2, -3], [-1, -3], [-1, 2], [-2, 3]], opts, True)


def test_random_3sat_against_brute_force() -> None:
    rng = random.Random(4026)
    for t in range(240):
        n = rng.randint(3, 12)
        m = round(4.26 * n)
        f = random_ksat(rng, n, m)
        sat = truth_table(n, f)[0] != 0
        check_run(n, f, OPTIONS[t % len(OPTIONS)], sat)


def test_random_mixed_widths() -> None:
    rng = random.Random(77)
    for t in range(200):
        n = rng.randint(1, 9)
        f = [random_ksat(rng, n, 1, rng.randint(1, 4))[0] for _ in range(rng.randint(0, 5 * n))]
        sat = truth_table(n, f)[0] != 0
        check_run(n, f, OPTIONS[t % len(OPTIONS)], sat)


def test_pigeonhole() -> None:
    for h in range(1, 6):
        n, f = pigeonhole(h + 1, h)
        for opts in OPTIONS:
            check_run(n, f, opts, False)
        n, f = pigeonhole(h, h)
        check_run(n, f, {}, True)


def naive_closure(clauses: list[list[int]], lits: list[int]) -> tuple[set[int], bool]:
    """Unit propagation by repeated scans: the closure and whether a clause
    became false."""
    a = set(lits)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            if any(lit in a for lit in c):
                continue
            free = [lit for lit in c if -lit not in a]
            if not free:
                return a, True
            if len(free) == 1:
                a.add(free[0])
                changed = True
    return a, False


def test_watched_literals_against_naive_propagation() -> None:
    rng = random.Random(911)
    checks = 0
    for _ in range(300):
        n = rng.randint(2, 10)
        f = []
        for _ in range(rng.randint(1, 4 * n)):
            vs = rng.sample(range(1, n + 1), rng.randint(1, min(5, n)))
            f.append([v if rng.random() < 0.5 else -v for v in vs])
        s = Solver(n, f)
        decisions: list[int] = []

        def compare(confl: int | None) -> None:
            closure, bad = naive_closure(f, decisions)
            assert s.check_watches()
            if confl is None:
                assert not bad and set(s.trail) == closure
            else:
                assert bad
                c = s.clauses[confl]
                assert c is not None and all(s.val(q) == -1 for q in c)

        if not s.ok:
            assert naive_closure(f, [])[1]
            continue
        confl = s.propagate()
        compare(confl)
        if confl is not None:
            continue
        for _ in range(30):
            free = [v for v in range(1, n + 1) if s.value[v] == 0]
            if not free:
                break
            if decisions and rng.random() < 0.25:
                b = rng.randint(0, len(decisions) - 1)
                s.cancel_until(b)
                del decisions[b:]
                compare(None)
                continue
            v = rng.choice(free)
            lit = v if rng.random() < 0.5 else -v
            s.decide(lit)
            decisions.append(lit)
            confl = s.propagate()
            compare(confl)
            checks += 1
            if confl is not None:
                b = rng.randint(0, len(decisions) - 1)
                s.cancel_until(b)
                del decisions[b:]
                compare(None)
    assert checks > 1000
