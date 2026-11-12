# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-dqn/. The authors are listed in prov/WJ898F.jsonl.

import itertools
import random
from fractions import Fraction as F

from double_dqn import double_dqn, double_dqn_target, dqn_target


class Table:
    def __init__(self, rows):
        self.rows = rows

    def q(self, s):
        return self.rows[s]


GAMMA = F(9, 10)


def test_fixed_table():
    online = Table({4: [F(1), F(3), F(2)]})
    target = Table({4: [F(2), F(1), F(4)]})
    r = F(1, 2)
    assert dqn_target(r, 4, False, online, target, GAMMA) == r + GAMMA * 4
    assert double_dqn_target(r, 4, False, online, target, GAMMA) == r + GAMMA * 1
    assert double_dqn_target(r, 4, True, online, target, GAMMA) == r
    # the two targets agree when both networks pick the same action
    same = Table({4: [F(0), F(5), F(1)]})
    assert double_dqn_target(r, 4, False, same, target, GAMMA) == r + GAMMA * 1
    assert double_dqn_target(r, 4, False, target, target, GAMMA) == dqn_target(r, 4, False, target, target, GAMMA)


def test_exact_bias_with_plus_minus_one_noise():
    # True values are 0 for all m actions; each network adds independent noise of +-1.
    for m in (2, 3, 4):
        e_dqn = F(0)
        e_double = F(0)
        combos = list(itertools.product((-1, 1), repeat=2 * m))
        for noise in combos:
            online = Table({0: [F(x) for x in noise[:m]]})
            target = Table({0: [F(x) for x in noise[m:]]})
            e_dqn += dqn_target(F(0), 0, False, online, target, F(1))
            e_double += double_dqn_target(F(0), 0, False, online, target, F(1))
        e_dqn /= len(combos)
        e_double /= len(combos)
        assert e_dqn == 1 - F(2) ** (1 - m)
        assert e_double == 0


def test_gaussian_noise_bias_over_seeds():
    m, trials = 10, 4000
    rng = random.Random(31)
    s_dqn = s_double = 0.0
    for _ in range(trials):
        online = Table({0: [rng.gauss(0, 1) for _ in range(m)]})
        target = Table({0: [rng.gauss(0, 1) for _ in range(m)]})
        s_dqn += dqn_target(0.0, 0, False, online, target, 1.0)
        s_double += double_dqn_target(0.0, 0, False, online, target, 1.0)
    # E max of 10 standard normals is about 1.539; the double estimate has mean 0
    # and standard error 1 / sqrt(4000), about 0.016.
    assert abs(s_dqn / trials - 1.539) < 0.05
    assert abs(s_double / trials) < 0.06


def test_van_hasselt_lower_bound_tight_and_random():
    for m in (2, 3, 5):
        b = F(1, 3)
        e = [b] * (m - 1) + [-(m - 1) * b]
        assert sum(e) == 0
        c = sum(x * x for x in e) / m
        assert max(e) ** 2 == c / (m - 1)
    rng = random.Random(4)
    for _ in range(2000):
        m = rng.randint(2, 6)
        e = [F(rng.randint(-9, 9)) for _ in range(m)]
        mean = sum(e) / m
        e = [x - mean for x in e]
        c = sum(x * x for x in e) / m
        if c > 0:
            assert max(e) ** 2 >= c / (m - 1)


def chain(s, a):
    if a == 1:
        if s == 5:
            return 1.0, s, True
        return 0.0, s + 1, False
    return 0.0, max(s - 1, 0), False


def test_double_dqn_reaches_optimal_policy():
    for seed in (0, 1):
        net = double_dqn(chain, 6, 2, 0, 0.9, 3000, 1000, 16, 50, 0.05, 16, random.Random(seed))
        for s in range(6):
            q = net.q(s)
            assert q[1] > q[0]
            assert abs(q[1] - 0.9 ** (5 - s)) < 0.02
