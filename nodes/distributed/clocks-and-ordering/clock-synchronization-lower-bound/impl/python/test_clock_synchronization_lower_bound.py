# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-synchronization-lower-bound/. The authors are listed in prov/1YP4C2.jsonl.

import random

from clock_synchronization_lower_bound import averaging, chain_executions, follow, run, shift, skew, weighted

D, U = 10.0, 4.0


def test_two_process_shift() -> None:
    # alpha: p0 -> p1 takes d - u, p1 -> p0 takes d. Shift p0 by u.
    c = [3.0, -5.0]
    delay = [[0.0, D - U], [D, 0.0]]
    c2, delay2 = shift(c, delay, [U, 0.0])
    assert delay2 == [[0.0, D], [D - U, 0.0]]
    for alg in (averaging, follow(0, 0.5), follow(1, 0.0), weighted([0.3, 0.7], 0.25)):
        v1, a1 = run(alg, c, delay, D, U)
        v2, a2 = run(alg, c2, delay2, D, U)
        assert v1 == v2  # neither process can tell them apart
        assert abs((a2[0] - a2[1]) - (a1[0] - a1[1]) - U) < 1e-12  # the skews differ by u
        assert max(skew(a1), skew(a2)) >= U / 2 - 1e-12


def test_averaging_meets_upper_bound() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        n = rng.randrange(2, 8)
        c = [rng.uniform(-100, 100) for _ in range(n)]
        delay = [[rng.uniform(D - U, D) if i != j else 0.0 for j in range(n)] for i in range(n)]
        _, a = run(averaging, c, delay, D, U)
        assert skew(a) <= (1 - 1 / n) * U + 1e-9


def test_chain_forces_the_bound() -> None:
    rng = random.Random(1)
    for n in range(2, 7):
        c0 = [rng.uniform(-50, 50) for _ in range(n)]
        execs = chain_executions(n, D, U, c0)
        algs = [averaging, follow(0, 0.5), follow(n - 1, 0.3)]
        for _ in range(5):
            w = [rng.random() for _ in range(n)]
            algs.append(weighted([x / sum(w) for x in w], rng.random()))
        for alg in algs:
            results = [run(alg, ci, di, D, U) for ci, di in execs]
            for vs, _ in results[1:]:
                assert vs == results[0][0]
            worst = max(skew(a) for _, a in results)
            assert worst >= (1 - 1 / n) * U - 1e-9
        # The averaging algorithm reaches the bound exactly in alpha_0.
        _, a0 = run(averaging, *execs[0], D, U)
        assert abs(skew(a0) - (1 - 1 / n) * U) < 1e-9


def test_page_example() -> None:
    # n = 3, d = 10, u = 4: the bound is 8/3.
    c = [0.0, 2.0, -1.0]
    delay = [[0, 8, 9], [10, 0, 6], [7, 10, 0]]
    _, a = run(averaging, c, delay, D, U)
    assert [round(x, 6) for x in a] == [0.0, -0.333333, 0.666667]
    assert abs(skew(a) - 1.0) < 1e-9
