# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-satisfy-count/. The authors are listed in prov/SH4TH9.jsonl.

import random

from bdd_satisfy_count import AND, BDD, FALSE, OR, TRUE, XOR


def rtable(rng: random.Random, n: int, density: float = 0.5) -> list[int]:
    return [1 if rng.random() < density else 0 for _ in range(1 << n)]


def check_reduced(b: BDD) -> None:
    seen = set()
    for u in range(2, len(b.nodes)):
        v, lo, hi = b.nodes[u]
        assert lo != hi and (v, lo, hi) not in seen
        assert v < b.var(lo) and v < b.var(hi)
        seen.add((v, lo, hi))


def bryant_1986_original(b: BDD, f: int) -> int:
    # The formula as printed in 1986, without the -1 in the exponents.
    # Indices are 1-based there: index(v) = var(v) + 1, and a terminal has n + 1.
    memo: dict[int, int] = {}

    def alpha(u: int) -> int:
        if u <= TRUE:
            return u
        if u not in memo:
            i, lo, hi = b.nodes[u]
            memo[u] = alpha(lo) * 2 ** (b.var(lo) - i) + alpha(hi) * 2 ** (b.var(hi) - i)
        return memo[u]

    return alpha(f) * 2 ** b.var(f)


def test_small_example() -> None:
    # (x0 AND x1) OR x2 over three variables has 5 models.
    b = BDD(3)
    x = [b.ithvar(i) for i in range(3)]
    f = b.apply(OR, b.apply(AND, x[0], x[1]), x[2])
    assert b.satcount(f) == 5
    assert b.satcount_bottom_up(f) == 5


def test_skipped_levels() -> None:
    b = BDD(10)
    x = [b.ithvar(i) for i in range(10)]
    assert b.satcount(x[9]) == 512
    assert b.satcount(b.apply(AND, x[0], x[9])) == 256
    assert b.satcount(b.apply(OR, x[3], x[6])) == 768
    assert b.satcount(FALSE) == 0
    assert b.satcount(TRUE) == 1024


def test_against_brute_force() -> None:
    rng = random.Random(1986)
    for n in range(0, 11):
        b = BDD(n)
        for density in (0.05, 0.5, 0.95):
            for _ in range(5):
                t = rtable(rng, n, density)
                f = b.build(t)
                assert b.satcount(f) == sum(t)
                assert b.satcount_bottom_up(f) == sum(t)
        check_reduced(b)


def test_sparse_functions_skip_levels() -> None:
    # Functions of a few variables leave long gaps between levels.
    rng = random.Random(2001)
    n = 10
    b = BDD(n)
    x = [b.ithvar(i) for i in range(n)]
    ops = (AND, OR, XOR)
    for _ in range(200):
        f = x[rng.randrange(n)]
        for _ in range(rng.randrange(1, 4)):
            f = b.apply(rng.choice(ops), f, x[rng.randrange(n)])
        want = sum(b_eval(b, f, a) for a in range(1 << n))
        assert b.satcount(f) == want
    check_reduced(b)


def b_eval(b: BDD, u: int, a: int) -> int:
    while u > TRUE:
        i, lo, hi = b.nodes[u]
        u = hi if (a >> i) & 1 else lo
    return u


def test_original_formula_is_wrong() -> None:
    # Without the -1, each path is weighted by an extra factor 2 for each
    # inner node on it, so every nonconstant function is overcounted.
    b = BDD(4)
    x = [b.ithvar(i) for i in range(4)]
    assert b.satcount(x[3]) == 8
    assert bryant_1986_original(b, x[3]) == 16
    rng = random.Random(10)
    for _ in range(50):
        f = b.build(rtable(rng, 4))
        if f <= TRUE:
            assert bryant_1986_original(b, f) == b.satcount(f)
        else:
            assert bryant_1986_original(b, f) > b.satcount(f)


def test_big_integers() -> None:
    n = 300
    b = BDD(n)
    x = [b.ithvar(i) for i in range(n)]
    assert b.satcount(b.apply(AND, x[0], x[n - 1])) == 2 ** (n - 2)
    p = FALSE
    for i in reversed(range(n)):
        p = b.apply(XOR, x[i], p)
    assert b.size(p) == 2 * n + 1
    assert b.satcount(p) == 2 ** (n - 1)
    assert b.satcount_bottom_up(p) == 2 ** (n - 1)


def test_probability_matches_count() -> None:
    rng = random.Random(7)
    for n in range(1, 9):
        b = BDD(n)
        t = rtable(rng, n)
        f = b.build(t)
        assert b.probability(f, [0.5] * n) == b.satcount(f) / 2 ** n
        p = [rng.random() for _ in range(n)]
        want = 0.0
        for a in range(1 << n):
            if t[a]:
                w = 1.0
                for i in range(n):
                    w *= p[i] if (a >> i) & 1 else 1 - p[i]
                want += w
        assert abs(b.probability(f, p) - want) < 1e-9
