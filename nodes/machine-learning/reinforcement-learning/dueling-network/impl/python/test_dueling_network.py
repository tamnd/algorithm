# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dueling-network/. The authors are listed in prov/P4J42D.jsonl.

import random
from fractions import Fraction as F

from dueling_network import DuelingQNet, aggregate, decompose, dueling_ddqn


def test_mean_aggregation_is_identifiable():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(2, 5)
        q = [F(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(m)]
        v, a = decompose(q, "mean")
        assert v == sum(q) / m
        assert aggregate(v, a, "mean") == q
        # shifting A by a constant does not change Q, shifting V does
        c = F(rng.randint(1, 9), 7)
        assert aggregate(v, [x + c for x in a], "mean") == q
        assert aggregate(v + c, a, "mean") != q
        # any (V', A') with the same Q has V' = mean Q and A' = centred A plus a constant
        a2 = [F(rng.randint(-9, 9)) for _ in range(m)]
        v2 = sum(q) / m
        q2 = aggregate(v2, a2, "mean")
        assert decompose(q2, "mean")[0] == v2


def test_max_aggregation_gives_v_equal_max_q():
    rng = random.Random(2)
    for _ in range(300):
        m = rng.randint(2, 5)
        v = F(rng.randint(-9, 9), 3)
        adv = [F(rng.randint(-9, 9), 2) for _ in range(m)]
        q = aggregate(v, adv, "max")
        assert max(q) == v  # the greedy action has Q = V
        assert decompose(q, "max")[0] == v
        assert aggregate(*decompose(q, "max"), "max") == q


def test_naive_sum_is_not_identifiable():
    v, adv = F(3), [F(1), F(-2), F(5)]
    q = aggregate(v, adv, "sum")
    for c in (F(1), F(-7, 2), F(10)):
        assert aggregate(v + c, [x - c for x in adv], "sum") == q


def loss(net, batch):
    return sum(0.5 * (y - net.q(s)[a]) ** 2 for s, a, y in batch) / len(batch)


def test_gradients_match_finite_differences():
    for kind in ("mean", "max"):
        rng = random.Random(5)
        net = DuelingQNet(4, 3, 5, rng, kind, rescale=1.0)
        batch = [(rng.randrange(4), rng.randrange(3), rng.uniform(-2, 2)) for _ in range(6)]
        g = net.grads(batch, loss="square")
        h = 1e-6

        def check(get, put, analytic):
            old = get()
            put(old + h)
            up = loss(net, batch)
            put(old - h)
            down = loss(net, batch)
            put(old)
            assert abs((up - down) / (2 * h) - analytic) < 1e-5

        check(lambda: net.bv, lambda x: setattr(net, "bv", x), g["bv"])
        for i in range(net.hidden):
            check(lambda: net.wv[i], lambda x: net.wv.__setitem__(i, x), g["wv"][i])
            check(lambda: net.b1[i], lambda x: net.b1.__setitem__(i, x), g["b1"][i])
        for b in range(3):
            check(lambda: net.ba[b], lambda x: net.ba.__setitem__(b, x), g["ba"][b])
            for i in range(net.hidden):
                check(lambda: net.wa[b][i], lambda x: net.wa[b].__setitem__(i, x), g["wa"][b][i])
        for s in range(4):
            for i in range(net.hidden):
                an = g["w1"].get(s, [0.0] * net.hidden)[i]
                check(lambda: net.w1[i][s], lambda x: net.w1[i].__setitem__(s, x), an)


def chain(s, a):
    if a == 1:
        if s == 5:
            return 1.0, s, True
        return 0.0, s + 1, False
    return 0.0, max(s - 1, 0), False


def test_dueling_ddqn_reaches_optimal_policy():
    for kind, seed in (("mean", 0), ("mean", 1), ("max", 0)):
        net = dueling_ddqn(chain, 6, 2, 0, 0.9, 3000, 1000, 16, 50, 0.05, 16,
                           random.Random(seed), kind)
        for s in range(6):
            q = net.q(s)
            assert q[1] > q[0]
            assert abs(q[1] - 0.9 ** (5 - s)) < 0.03
