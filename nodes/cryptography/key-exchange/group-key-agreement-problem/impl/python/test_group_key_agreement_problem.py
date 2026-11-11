# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-key-agreement-problem/. The authors are listed in prov/67D8KM.jsonl.

import random

import pytest

from group_key_agreement_problem import G, P, Q, bd, gdh2, itw, leader, secrets_for


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


def product_key(xs):
    e = 1
    for x in xs:
        e = e * x % Q
    return pow(G, e, P)


def bd_key(xs):
    n = len(xs)
    return pow(G, sum(xs[i] * xs[(i + 1) % n] for i in range(n)) % Q, P)


@pytest.mark.parametrize("n", [2, 3, 5, 8])
def test_all_members_agree(n):
    xs = secrets_for(n, seeded(n))
    for proto, expected in ((itw, product_key(xs)), (gdh2, product_key(xs)), (bd, bd_key(xs))):
        keys, _ = proto(xs)
        assert keys == [expected] * n
    keys, _ = leader(xs, rng=seeded(99))
    assert len(set(keys)) == 1


@pytest.mark.parametrize("n", [3, 4, 6, 10])
def test_costs(n):
    xs = secrets_for(n, seeded(10 + n))
    _, m = leader(xs, rng=seeded(1))
    assert (m.rounds, m.messages, sum(m.exps)) == (2, n + 1, 3 * n - 2)
    assert m.exps[0] == n                         # the leader does n, the others 2 each
    _, m = itw(xs)
    assert (m.rounds, m.messages, sum(m.exps)) == (n - 1, n * (n - 1), n * n)
    assert m.exps == [n] * n
    _, m = gdh2(xs)
    assert (m.rounds, m.messages, sum(m.exps)) == (n, n, (n * n + 3 * n) // 2 - 1)
    assert m.exps == [i + 1 for i in range(1, n)] + [n]
    _, m = bd(xs)
    assert (m.rounds, m.messages, sum(m.exps)) == (2, 2 * n, 3 * n)


def test_leader_is_not_contributory():
    # The leader alone fixes the key; it can even force a chosen value.
    xs = secrets_for(4, seeded(5))
    keys, _ = leader(xs, chosen=42)
    assert keys == [42] * 4


def test_contributory_protocols_depend_on_every_member():
    xs = secrets_for(5, seeded(6))
    for proto in (itw, gdh2, bd):
        base = proto(xs)[0][0]
        for i in range(5):
            ys = list(xs)
            ys[i] = ys[i] % (Q - 1) + 1
            assert proto(ys)[0][0] != base
