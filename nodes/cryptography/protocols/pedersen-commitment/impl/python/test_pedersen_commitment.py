# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pedersen-commitment/. The authors are listed in prov/VBNYFB.jsonl.
# There are no official test vectors for Pedersen commitments. The tests check
# the algebra, perfect hiding by enumeration, and the trapdoor attack, all on
# toy groups with local code.

import random

from pedersen_commitment import (
    MEDIUM,
    P128,
    TOY,
    Group,
    Pedersen,
    VectorPedersen,
    dlog_from_two_openings,
    equivocate,
)


def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0:
            return n == sp
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_groups_are_safe_prime_groups():
    for grp in (TOY, MEDIUM):
        assert is_probable_prime(grp.p) and is_probable_prime(grp.q)
        assert grp.is_element(grp.g) and grp.g != 1
    assert P128.bit_length() == 128


def test_commit_open_and_reject():
    for grp in (TOY, MEDIUM):
        ped = Pedersen(grp)
        assert grp.is_element(ped.h)
        c, r = ped.commit(42)
        assert ped.open(c, 42, r)
        assert not ped.open(c, 43, r)
        assert not ped.open(c, 42, (r + 1) % grp.q)
        assert not ped.open(0, 42, r)


def test_toy_example_values():
    ped = Pedersen(TOY)
    c, _ = ped.commit(5, 77)
    assert c == pow(TOY.g, 5, TOY.p) * pow(ped.h, 77, TOY.p) % TOY.p


def test_perfect_hiding_by_enumeration():
    # For each message m, the map r -> g^m h^r is a bijection from Z_q onto
    # the group. So the commitment is uniform on the group for every m.
    ped = Pedersen(TOY)
    group_elems = {pow(TOY.g, k, TOY.p) for k in range(TOY.q)}
    assert len(group_elems) == TOY.q
    for m in (0, 5, 1018):
        assert {ped.commit(m, r)[0] for r in range(TOY.q)} == group_elems


def test_additive_homomorphism():
    rng = random.Random(1)
    for grp in (TOY, MEDIUM):
        ped = Pedersen(grp)
        for _ in range(20):
            m1, m2 = rng.randrange(grp.q), rng.randrange(grp.q)
            c1, r1 = ped.commit(m1)
            c2, r2 = ped.commit(m2)
            assert ped.open(ped.add(c1, c2), (m1 + m2) % grp.q, (r1 + r2) % grp.q)


def test_known_trapdoor_breaks_binding():
    # If the committer chose h = g^t itself, it can open to any message.
    for grp in (TOY, MEDIUM):
        t = 123456789 % grp.q
        ped = Pedersen(grp, h=pow(grp.g, t, grp.p))
        c, r = ped.commit(1000)
        for m_new in (0, 1, 999, grp.q - 1):
            r_new = equivocate(grp.q, t, 1000, r, m_new)
            assert ped.open(c, m_new, r_new)


def test_two_openings_give_the_discrete_log():
    grp = TOY
    t = 777
    ped = Pedersen(grp, h=pow(grp.g, t, grp.p))
    c, r = ped.commit(10, 20)
    r2 = equivocate(grp.q, t, 10, 20, 500)
    assert dlog_from_two_openings(grp.q, 10, 20, 500, r2) == t


def test_hash_to_group_h_has_full_order():
    ped = Pedersen(TOY)
    # Brute force the log of h in the toy group: it exists, but no party
    # chose it, so no party knew it when h was fixed.
    logs = [k for k in range(TOY.q) if pow(TOY.g, k, TOY.p) == ped.h]
    assert len(logs) == 1 and logs[0] != 0


def test_vector_commitment():
    rng = random.Random(5)
    for grp in (TOY, MEDIUM):
        vp = VectorPedersen(grp, 4)
        assert len(set(vp.gens + [vp.h])) == 5
        ms = [rng.randrange(grp.q) for _ in range(4)]
        c, r = vp.commit(ms)
        assert vp.open(c, ms, r)
        ms2 = list(ms)
        ms2[2] = (ms2[2] + 1) % grp.q
        assert not vp.open(c, ms2, r)
        # Homomorphic in the vector too.
        ns = [rng.randrange(grp.q) for _ in range(4)]
        d, s = vp.commit(ns)
        sums = [(a + b) % grp.q for a, b in zip(ms, ns)]
        assert vp.open(c * d % grp.p, sums, (r + s) % grp.q)


def test_other_safe_prime():
    grp = Group(23)
    assert grp.q == 11
    ped = Pedersen(grp)
    c, r = ped.commit(3)
    assert ped.open(c, 3, r)
