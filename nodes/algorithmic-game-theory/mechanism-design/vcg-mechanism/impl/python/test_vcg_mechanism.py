# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vcg-mechanism/. The authors are listed in prov/SH7M6B.jsonl.

import random
from fractions import Fraction
from itertools import combinations, product

from vcg_mechanism import (
    auction_valuations,
    best_outcome,
    bundle,
    groves,
    single_item,
    utility,
    vcg,
    welfare,
    xor_value,
)

F = Fraction


def random_valuations(rng, outcomes, n, lo, hi):
    return [{o: F(rng.randint(lo, hi)) for o in outcomes} for _ in range(n)]


def opt_by_dp(xor_bids, m, skip=None):
    """Best welfare of a combinatorial auction by a dynamic program over sets of items."""
    agents = [b for i, b in enumerate(xor_bids) if i != skip]
    items = frozenset(range(m))
    memo = {}

    def best(k, rest):
        if k == len(agents):
            return F(0)
        key = (k, rest)
        if key not in memo:
            r = sorted(rest)
            val = F(-1)
            for size in range(len(r) + 1):
                for t in combinations(r, size):
                    t = frozenset(t)
                    val = max(val, xor_value(agents[k], t) + best(k + 1, rest - t))
            memo[key] = val
        return memo[key]

    return best(0, items)


def random_xor_bids(rng, m, k, hi):
    bids = {}
    for _ in range(k):
        s = frozenset(j for j in range(m) if rng.random() < 0.6)
        if s:
            bids[s] = F(rng.randint(0, hi))
    return bids


def check_dsic(outcomes, type_sets, mech):
    """Every agent, every true type, every report of the others, every misreport: truth is best."""
    n = len(type_sets)
    for prof in product(*[range(len(t)) for t in type_sets]):
        truth = [type_sets[i][prof[i]] for i in range(n)]
        x, p = mech(outcomes, truth)
        for i in range(n):
            u_true = utility(truth[i], x, p[i])
            for lie in type_sets[i]:
                rep = truth[:i] + [lie] + truth[i + 1:]
                y, q = mech(outcomes, rep)
                if utility(truth[i], y, q[i]) > u_true:
                    return (i, prof, lie)
    return None


def test_vickrey_check_value():
    outs, vals = single_item([10, 7, 3])
    x, p = vcg(outs, vals)
    assert x == 0
    assert p == [7, 0, 0]


def test_single_item_is_second_price():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 6)
        values = [rng.randint(0, 9) for _ in range(n)]
        x, p = vcg(*single_item(values))
        top = max(values)
        assert x == values.index(top)
        others = values[:x] + values[x + 1:]
        assert p[x] == (max(others) if others else 0)
        assert all(p[i] == 0 for i in range(n) if i != x)


def test_multi_unit_unit_demand_pays_the_next_bid():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(2, 5)
        k = rng.randint(1, n - 1)
        values = [rng.randint(0, 20) for _ in range(n)]
        outs = list(combinations(range(n), k))
        vals = [{s: F(values[i]) if i in s else F(0) for s in outs} for i in range(n)]
        x, p = vcg(outs, vals)
        price = sorted(values, reverse=True)[k]
        for i in range(n):
            assert p[i] == (price if i in x else 0)


def test_outcome_and_payments_match_a_second_method():
    rng = random.Random(3)
    for _ in range(60):
        n, m = rng.randint(1, 3), rng.randint(1, 3)
        bids = [random_xor_bids(rng, m, rng.randint(1, 3), 12) for _ in range(n)]
        outs, vals = auction_valuations(bids, m)
        x, p = vcg(outs, vals)
        opt = opt_by_dp(bids, m)
        assert welfare(vals, x) == opt
        for i in range(n):
            vi = xor_value(bids[i], bundle(x, i))
            # externality form: the best welfare of the others without i, minus what they get now
            assert p[i] == opt_by_dp(bids, m, skip=i) - (opt - vi)
            # the price is at most the value of i for its bundle (IR) and at least 0
            assert 0 <= p[i] <= vi


def test_dsic_on_general_outcome_sets_with_negative_values():
    rng = random.Random(4)
    for _ in range(8):
        outs = list(range(rng.randint(2, 4)))
        n = 3
        type_sets = [random_valuations(rng, outs, 3, -3, 3) for _ in range(n)]
        # add a type with a tie between two outcomes
        for t in type_sets:
            t.append({o: F(1) if o < 2 else F(0) for o in outs})
        assert check_dsic(outs, type_sets, vcg) is None


def test_dsic_in_a_combinatorial_auction():
    rng = random.Random(5)
    m = 2
    type_sets = []
    for _ in range(3):
        ts = [random_xor_bids(rng, m, 2, 6) for _ in range(3)]
        ts.append({frozenset([0, 1]): F(4)})
        type_sets.append(ts)
    outs, _ = auction_valuations([{} for _ in range(3)], m)

    def mech(outcomes, bids):
        _, vals = auction_valuations(bids, m)
        return vcg(outcomes, vals)

    def util(bids_i, x, p, i):
        return xor_value(bids_i, bundle(x, i)) - p[i]

    for prof in product(range(4), repeat=3):
        truth = [type_sets[i][prof[i]] for i in range(3)]
        x, p = mech(outs, truth)
        for i in range(3):
            for lie in type_sets[i]:
                y, q = mech(outs, truth[:i] + [lie] + truth[i + 1:])
                assert util(truth[i], y, q, i) <= util(truth[i], x, p, i)


def test_every_groves_mechanism_is_dsic():
    rng = random.Random(6)
    outs = [0, 1, 2]
    type_sets = [random_valuations(rng, outs, 3, -2, 4) for _ in range(3)]
    for c in range(3):
        h = [lambda others, c=c: c * sum(v[0] for v in others) + 5 for _ in range(3)]
        assert check_dsic(outs, type_sets, lambda o, v: groves(o, v, h)) is None
    zero = [lambda others: 0 for _ in range(3)]
    assert check_dsic(outs, type_sets, lambda o, v: groves(o, v, zero)) is None


def test_the_checker_finds_a_profitable_lie():
    # the same outcome with pay-your-bid payments is not DSIC, and the checker must see it
    def pay_your_bid(outcomes, vals):
        x, _ = best_outcome(outcomes, vals)
        return x, [vals[i][x] for i in range(len(vals))]

    outs = [0, 1]
    type_sets = [[{0: F(v), 1: F(0)} for v in (0, 2, 5)], [{0: F(0), 1: F(v)} for v in (0, 2, 5)]]
    assert check_dsic(outs, type_sets, pay_your_bid) is not None
    assert check_dsic(outs, type_sets, vcg) is None


def test_clarke_is_groves_with_the_pivot_term():
    rng = random.Random(7)
    outs = list(range(4))
    pivot = [lambda others: best_outcome(outs, others)[1] for _ in range(3)]
    for _ in range(200):
        vals = random_valuations(rng, outs, 3, -5, 5)
        assert vcg(outs, vals) == groves(outs, vals, pivot)


def test_ir_and_no_positive_transfers_for_nonnegative_values():
    rng = random.Random(8)
    for _ in range(300):
        outs = list(range(rng.randint(1, 5)))
        n = rng.randint(1, 4)
        vals = random_valuations(rng, outs, n, 0, 9)
        x, p = vcg(outs, vals)
        for i in range(n):
            assert p[i] >= 0
            assert utility(vals[i], x, p[i]) >= 0


def test_ir_can_fail_with_a_negative_value():
    # outcome 1 builds a project; agent 1 is hurt by it
    outs = [0, 1]
    vals = [{0: F(0), 1: F(5)}, {0: F(0), 1: F(-2)}]
    x, p = vcg(outs, vals)
    assert x == 1 and p == [2, 0]
    assert utility(vals[1], x, p[1]) == -2


def test_public_project_does_not_cover_its_cost():
    # citizens with values for a bridge of cost 300, and the government as one more agent
    c = F(300)
    values = [F(150), F(120), F(60)]
    outs = [0, 1]
    vals = [{0: F(0), 1: v} for v in values] + [{0: F(0), 1: -c}]
    x, p = vcg(outs, vals)
    assert x == 1
    assert p[:3] == [120, 90, 30]
    assert p[3] == 0  # the government has a single type and is never pivotal for itself here
    assert sum(p[:3]) == 240 < c
    for i, v in enumerate(values):
        rest = sum(values) - v
        assert p[i] == (c - rest if rest < c else 0)


def test_zero_revenue_and_collusion_with_complements():
    ab, a, b = frozenset([0, 1]), frozenset([0]), frozenset([1])
    outs, vals = auction_valuations([{ab: 2}, {a: 2}, {b: 2}], 2)
    x, p = vcg(outs, vals)
    assert x == (1, 2) and p == [0, 0, 0]
    # true values 1/2 for the two small bidders: the big bidder wins and pays 1
    outs, vals = auction_valuations([{ab: 2}, {a: F(1, 2)}, {b: F(1, 2)}], 2)
    x, p = vcg(outs, vals)
    assert x == (0, 0) and p == [1, 0, 0]
    # both small bidders overbid 2: they win, pay 0, and each gains 1/2
    _, lie = auction_valuations([{ab: 2}, {a: 2}, {b: 2}], 2)
    y, q = vcg(outs, lie)
    assert y == (1, 2) and q == [0, 0, 0]
    assert utility(vals[1], y, q[1]) == F(1, 2) and utility(vals[2], y, q[2]) == F(1, 2)


def test_no_groves_mechanism_is_budget_balanced():
    # binary project, values in {-1/2, 1/2}: the alternating sum of the total payment over
    # the four profiles does not depend on h and is never 0, so the total cannot be 0 always
    rng = random.Random(9)
    outs = [0, 1]
    pts = [F(-1, 2), F(1, 2)]
    for _ in range(50):
        table = [{t: F(rng.randint(-9, 9)) for t in pts} for _ in range(2)]
        h = [lambda others, i=i: table[i][others[0][1]] for i in range(2)]
        alt = F(0)
        for t1, t2 in product(pts, repeat=2):
            vals = [{0: F(0), 1: t1}, {0: F(0), 1: t2}]
            _, p = groves(outs, vals, h)
            sign = 1 if (t1 == t2) else -1
            alt += sign * sum(p)
        assert alt == -1
