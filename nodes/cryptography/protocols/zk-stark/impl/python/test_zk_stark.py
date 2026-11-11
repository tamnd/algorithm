# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zk-stark/. The authors are listed in prov/7RSZSV.jsonl.
# There are no official test vectors for FRI. The tests check the field and
# domain, the fold identity on polynomials, that low-degree functions pass,
# that random and too-high-degree functions fail, and that a cheater who
# corrupts part of a low-degree function is accepted exactly when no query
# touches a corrupted pair.

import random

from zk_stark import (
    BLOWUP,
    GENERATOR,
    P,
    MerkleTree,
    domain,
    evaluate,
    fold,
    merkle_verify,
    proof_size,
    prove,
    replay,
    root_of_unity,
    verify,
)

D = 16                  # degree bound
N = BLOWUP * D          # domain size 128


def low_degree(rng, d=D):
    coeffs = [rng.randrange(P) for _ in range(d)]
    return coeffs, evaluate(coeffs, domain(N))


def test_field_and_generator():
    assert P == 3221225473
    for q in (2, 3):
        assert pow(GENERATOR, (P - 1) // q, P) != 1     # 5 generates the whole group
    w = root_of_unity(N)
    assert pow(w, N, P) == 1 and pow(w, N // 2, P) == P - 1


def test_fold_halves_the_degree():
    rng = random.Random(1)
    coeffs, values = low_degree(rng)
    alpha = rng.randrange(P)
    folded = fold(values, alpha)
    # f(x) = E(x^2) + x O(x^2), and the fold is E + alpha O on the squares.
    even, odd = coeffs[0::2], coeffs[1::2]
    want = [(e + alpha * o) % P for e, o in zip(even, odd)]
    assert folded == evaluate(want, domain(N // 2))


def test_merkle_paths():
    rng = random.Random(2)
    values = [rng.randrange(P) for _ in range(16)]
    tree = MerkleTree(values)
    for k in range(16):
        assert merkle_verify(tree.root, k, values[k], tree.path(k))
        assert not merkle_verify(tree.root, k, (values[k] + 1) % P, tree.path(k))


def test_low_degree_passes():
    rng = random.Random(3)
    for trial in range(5):
        _, values = low_degree(rng)
        proof = prove(values, D, queries=10, salt=bytes([trial]))
        assert verify(proof, N, D, 10)
    # Every degree below the bound passes, including constants.
    for d in (1, 2, 8):
        _, values = low_degree(rng, d)
        assert verify(prove(values, D, 10), N, D, 10)


def test_random_function_and_degree_d_fail():
    rng = random.Random(4)
    for _ in range(5):
        values = [rng.randrange(P) for _ in range(N)]
        assert not verify(prove(values, D, 10), N, D, 10)
    # Degree exactly D is one too many: the last layer is not constant.
    _, values = low_degree(rng, D + 1)
    assert not verify(prove(values, D, 10), N, D, 10)


def test_tampered_proof_fails():
    rng = random.Random(5)
    _, values = low_degree(rng)
    proof = prove(values, D, 10, salt=b"s")
    a, pa, b, pb = proof["openings"][0][1]
    proof["openings"][0][1] = ((a + 1) % P, pa, b, pb)
    assert not verify(proof, N, D, 10)
    proof = prove(values, D, 10, salt=b"s")
    proof["salt"] = b"t"         # other challenges, so the openings no longer fit
    assert not verify(proof, N, D, 10)


def test_corrupted_cheater_acceptance():
    # The cheater takes a low-degree g, changes a fraction of its values to get
    # f, commits f in layer 0 and the honest folds of g in later layers. A
    # query j passes exactly when f = g at both x_j and -x_j.
    rng = random.Random(6)
    _, g = low_degree(rng)
    bad = set(rng.sample(range(N), 12))               # delta = 12/128
    f = [(v + 1 + rng.randrange(P - 1)) % P if k in bad else v for k, v in enumerate(g)]
    good = {j for j in range(N // 2) if j not in bad and j + N // 2 not in bad}
    u = len(good) / (N // 2)                          # Pr[x and -x both unchanged]
    assert 52 / 64 <= u <= 58 / 64
    queries, trials, accepted = 3, 150, 0
    for t in range(trials):
        proof = prove(f, D, queries, salt=t.to_bytes(4, "big"), shadow=g)
        ok = verify(proof, N, D, queries)
        _, js = replay(proof, N, D.bit_length() - 1, queries)
        assert ok == all(j in good for j in js)
        accepted += ok
    rate = accepted / trials
    expect = u ** queries
    sigma = (expect * (1 - expect) / trials) ** 0.5
    assert abs(rate - expect) < 4 * sigma
    # The honest prover with g itself is always accepted.
    assert verify(prove(g, D, queries, salt=b"g"), N, D, queries)


def test_proof_size_is_polylog():
    rng = random.Random(7)
    _, values = low_degree(rng)
    size = proof_size(prove(values, D, 10, salt=b"x"))
    # 10 queries * 4 layers * 2 openings * (4 bytes + up to 7 hashes) and change.
    assert size < 20000
