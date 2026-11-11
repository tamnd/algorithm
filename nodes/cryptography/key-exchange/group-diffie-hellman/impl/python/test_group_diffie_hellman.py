# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-diffie-hellman/. The authors are listed in prov/YAZFG4.jsonl.
#
# GDH.2 has no official test vectors. These tests check agreement against
# g^(x_1 ... x_n) and count the exponentiations.

import random

import pytest

from group_diffie_hellman import G, P, Q, Member, run


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


@pytest.mark.parametrize("n", [2, 3, 4])
def test_agreement(n):
    members, rounds, messages = run(n, seeded(n))
    e = 1
    for m in members:
        e = e * m.x % Q
    assert [m.key for m in members] == [pow(G, e, P)] * n
    assert (rounds, messages) == (n, n)


@pytest.mark.parametrize("n", [2, 3, 5])
def test_exponentiation_count(n):
    members, _, _ = run(n, seeded(10 + n))
    assert [m.exps for m in members] == [i + 1 for i in range(1, n)] + [n]
    assert sum(m.exps for m in members) == (n * n + 3 * n) // 2 - 1


def test_value_outside_the_group_is_rejected():
    m = Member(0, seeded(1))
    with pytest.raises(ValueError):
        m.upflow(([], P - G))      # -4 is not a quadratic residue mod p


def test_broadcast_values_are_not_the_key():
    members, _, _ = run(4, seeded(2))
    key = members[0].key
    assert all(pow(G, m.x, P) != key for m in members)
