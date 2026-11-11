# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burmester-desmedt/. The authors are listed in prov/BRF2MN.jsonl.
#
# The 1994 paper has no test vectors. These tests check agreement against
# g^(x_1 x_2 + ... + x_n x_1).

import random

import pytest

from burmester_desmedt import G, P, Q, check_broadcast, key, round1, round2, run


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


@pytest.mark.parametrize("n", [2, 3, 4, 7])
def test_agreement(n):
    xs, keys = run(n, seeded(n))
    expected = pow(G, sum(xs[i] * xs[(i + 1) % n] for i in range(n)) % Q, P)
    assert keys == [expected] * n


def test_round2_values_multiply_to_one():
    # The product of all X_i is g^0 = 1: the telescoping sum of the exponents is 0.
    rng = seeded(3)
    xs = [1 + rng(Q - 1) for _ in range(5)]
    z = [round1(x) for x in xs]
    X = [round2(i, xs[i], z) for i in range(5)]
    prod = 1
    for v in X:
        prod = prod * v % P
    assert prod == 1


def test_value_outside_the_group_is_rejected():
    rng = seeded(4)
    xs = [1 + rng(Q - 1) for _ in range(3)]
    z = [round1(x) for x in xs]
    z[1] = P - z[1]
    with pytest.raises(ValueError):
        check_broadcast(z)


def test_one_changed_secret_changes_the_key():
    rng = seeded(5)
    xs = [1 + rng(Q - 1) for _ in range(4)]
    z = [round1(x) for x in xs]
    X = [round2(i, xs[i], z) for i in range(4)]
    k = key(0, xs[0], z, X)
    xs[2] += 1
    z = [round1(x) for x in xs]
    X = [round2(i, xs[i], z) for i in range(4)]
    assert key(0, xs[0], z, X) != k
