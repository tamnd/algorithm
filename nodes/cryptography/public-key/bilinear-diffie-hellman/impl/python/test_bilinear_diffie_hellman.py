# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-diffie-hellman/. The authors are listed in prov/42KE82.jsonl.
#
# BDH is an assumption, so there are no official test vectors. The tests check the worked example
# of the page on p = 59, the reductions from CDH in G1 and in GT with simulated oracles, and that
# the pairing decides DDH in G1, with fixed seeds. The curves are NOT secure.

import random

import bilinear_diffie_hellman as bdh


def test_worked_example_p59() -> None:
    C = bdh.TINY
    G = C.generator()
    assert G == (35, 31)
    assert [C.mul(k, G) for k in range(1, 6)] == [(35, 31), (25, 29), (25, 30), (35, 28), None]
    z = C.pairing(G, G)
    assert z == (42, 19)
    assert [C.f2_pow(z, k) for k in range(1, 6)] == [(42, 19), (46, 3), (46, 56), (42, 40), (1, 0)]
    # a = 2, b = 3, c = 4: abc = 24 = 4 (mod 5), so the BDH answer is z^4.
    inst = (G, C.mul(2, G), C.mul(3, G), C.mul(4, G))
    assert inst[1:] == ((25, 29), (25, 30), (35, 28))
    assert bdh.bdh_by_discrete_log(C, inst) == (42, 40)
    # DDH in G1: (G, 2G, 3G, D) is a DH tuple exactly for D = 6G = G.
    assert C.pairing(inst[1], inst[2]) == (42, 19)
    assert bdh.ddh_test(C, G, inst[1], inst[2], G)
    assert C.pairing(G, inst[1]) == (46, 3)
    assert not bdh.ddh_test(C, G, inst[1], inst[2], inst[1])


def test_tiny_all_instances() -> None:
    C = bdh.TINY
    G = C.generator()
    z = C.pairing(G, G)
    for a in range(1, 5):
        for b in range(1, 5):
            for c in range(1, 5):
                inst = (G, C.mul(a, G), C.mul(b, G), C.mul(c, G))
                assert bdh.bdh_by_discrete_log(C, inst) == C.f2_pow(z, a * b * c)
                for d in range(1, 5):
                    assert bdh.ddh_test(C, G, inst[1], inst[2], C.mul(d, G)) == (d == a * b % 5)


def test_toy_pairing_symmetric_bilinear() -> None:
    C = bdh.TOY
    G = C.generator()
    assert C.mul(C.r, G) is None
    z = C.pairing(G, G)
    assert z != (1, 0) and C.f2_pow(z, C.r) == (1, 0)
    rng = random.Random(2001)
    a, b = rng.randrange(1, C.r), rng.randrange(1, C.r)
    A, B = C.mul(a, G), C.mul(b, G)
    assert C.pairing(A, B) == C.pairing(B, A) == C.f2_pow(z, a * b % C.r)


def test_toy_bdh_from_cdh_oracles() -> None:
    C = bdh.TOY
    rng = random.Random(42)
    a, b, c = (rng.randrange(1, C.r) for _ in range(3))
    G = C.generator()
    inst = (G, C.mul(a, G), C.mul(b, G), C.mul(c, G))
    answer = C.f2_pow(C.pairing(G, G), a * b * c % C.r)
    # Simulated oracles: they know the exponents. A real solver would not.
    cdh_g1 = lambda A, B: C.mul(a * b, G)
    cdh_gt = lambda g, ga, gb: C.f2_pow(g, (a * b) * c % C.r)
    assert bdh.bdh_from_cdh_in_g1(C, cdh_g1, inst) == answer
    assert bdh.bdh_from_cdh_in_gt(C, cdh_gt, inst) == answer
    _, real = bdh.bdh_instance(C, random.Random(42))
    assert real == answer


def test_toy_ddh_is_easy_in_g1() -> None:
    C = bdh.TOY
    G = C.generator()
    rng = random.Random(1984)
    for _ in range(3):
        a, b = rng.randrange(1, C.r), rng.randrange(1, C.r)
        A, B = C.mul(a, G), C.mul(b, G)
        assert bdh.ddh_test(C, G, A, B, C.mul(a * b, G))
        assert not bdh.ddh_test(C, G, A, B, C.mul(rng.randrange(1, C.r), G))


def test_dbdh_instances() -> None:
    C = bdh.TINY
    for seed in range(6):
        P, A, B, Cc, Z = bdh.dbdh_instance(C, random.Random(seed), real=True)
        assert bdh.bdh_by_discrete_log(C, (P, A, B, Cc)) == Z
