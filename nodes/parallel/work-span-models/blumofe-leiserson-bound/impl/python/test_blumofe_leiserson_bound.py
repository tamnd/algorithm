# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blumofe-leiserson-bound/. The authors are listed in prov/4P69AP.jsonl.

import math
import random
from fractions import Fraction

from blumofe_leiserson_bound import balls_in_weighted_bins, build_dag, potential, run, span


def fib_program(n):
    return {("f", k): ([("work", 1)] if k <= 1 else
                       [("spawn", ("f", k - 1)), ("call", ("f", k - 2)), ("sync",), ("work", 1)])
            for k in range(n + 1)}


def random_program(rng, depth):
    prog, counter = {}, [0]

    def make(d):
        counter[0] += 1
        name = counter[0]
        body = []
        for _ in range(rng.randint(1, 4)):
            x = rng.random()
            if d > 0 and x < 0.5:
                body.append(("spawn", make(d - 1)))
            elif d > 0 and x < 0.6:
                body.append(("call", make(d - 1)))
            elif x < 0.7:
                body.append(("sync",))
            else:
                body.append(("work", rng.randint(1, 4)))
        prog[name] = body
        return name

    return prog, make(depth)


def dags():
    yield build_dag(fib_program(9), ("f", 9))
    rng = random.Random(77)
    for _ in range(30):
        yield build_dag(*random_program(rng, 5))


def test_potential_proof_invariants():
    for succ, child in dags():
        tinf = span(succ)
        for p in (1, 2, 3, 8):
            for seed in range(3):
                phis = [3 ** (2 * tinf - 1)]  # the root is assigned with weight T_inf

                def check(assigned, deques, depth):
                    total, per = potential(assigned, deques, depth, tinf)
                    assert total <= phis[-1]  # the potential never increases
                    phis.append(total)
                    for q in range(p):
                        dq = list(deques[q])  # top first
                        if not dq:
                            continue
                        assert assigned[q] is not None  # an owner with work is busy
                        w = [tinf - depth[v] for v in reversed(dq)]  # bottom to top
                        assert all(x >= 1 for x in w)
                        # structural lemma: w(v0) <= w(v1) < w(v2) < ... < w(vk)
                        assert tinf - depth[assigned[q]] <= w[0]
                        assert all(w[i] < w[i + 1] for i in range(len(w) - 1))
                        # top-heavy deques: the top node holds 3/4 of the potential of q
                        assert 4 * 3 ** (2 * w[-1]) >= 3 * per[q]

                r = run(succ, child, p, random.Random(seed), check)
                assert phis[-1] == 0
                assert p * r["time"] == len(succ) + r["attempts"]


def test_mean_steal_attempts():
    for succ, child in dags():
        tinf = span(succ)
        for p in (2, 4, 16):
            runs = [run(succ, child, p, random.Random(s)) for s in range(20)]
            mean_a = sum(r["attempts"] for r in runs) / len(runs)
            mean_t = sum(r["time"] for r in runs) / len(runs)
            assert mean_a <= 2 * p * tinf
            assert mean_t <= len(succ) / p + 2 * tinf


def test_balls_into_weighted_bins():
    rng = random.Random(5)
    beta = Fraction(1, 2)
    bound = 1 - 1 / ((1 - float(beta)) * math.e)  # 1 - 2/e, about 0.264
    for p in range(1, 6):
        for _ in range(8):
            weights = [Fraction(rng.randint(0, 20)) for _ in range(p)]
            if sum(weights) == 0:
                continue
            pr = balls_in_weighted_bins(weights, beta)
            assert float(pr) > bound
            assert pr > Fraction(1, 4)
    # one heavy bin: X >= W/2 exactly when that bin is hit
    assert balls_in_weighted_bins([Fraction(1), Fraction(0), Fraction(0)], beta) == 1 - Fraction(8, 27)
