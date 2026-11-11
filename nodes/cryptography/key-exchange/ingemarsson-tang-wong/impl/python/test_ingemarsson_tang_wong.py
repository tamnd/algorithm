# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ingemarsson-tang-wong/. The authors are listed in prov/EHMDDS.jsonl.
#
# The 1982 paper has no test vectors. These tests check agreement against
# g^(x_1 ... x_n) and the counts of rounds, messages and exponentiations.

import random

import pytest

from ingemarsson_tang_wong import G, P, Q, run


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


@pytest.mark.parametrize("n", [2, 3, 4, 6])
def test_agreement_and_costs(n):
    xs, keys, rounds, messages, exps = run(n, seeded(n))
    e = 1
    for x in xs:
        e = e * x % Q
    assert keys == [pow(G, e, P)] * n
    assert (rounds, messages) == (n - 1, n * (n - 1))
    assert exps == [n] * n and sum(exps) == n * n


def test_three_members_see_pairs_but_not_the_key():
    # With n = 3 the wire carries g^x_i and g^(x_i x_j), never g^(x_1 x_2 x_3).
    xs, keys, _, _, _ = run(3, seeded(7))
    wire = {pow(G, x, P) for x in xs}
    wire |= {pow(G, xs[i] * xs[(i - 1) % 3] % Q, P) for i in range(3)}
    assert keys[0] not in wire
