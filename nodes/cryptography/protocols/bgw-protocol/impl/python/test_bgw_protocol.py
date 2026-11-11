# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bgw-protocol/. The authors are listed in prov/DSEB3X.jsonl.
# There are no official test vectors for BGW. The tests compare the protocol
# with plain evaluation on random arithmetic circuits with n = 5 and t = 2,
# check the degree of every product sharing, and run the wrong-share attack
# on local simulated parties.

import random

import pytest

from bgw_protocol import (
    P61,
    Circuit,
    bgw,
    candidates,
    decode_with_errors,
    degree,
    lagrange_at_zero,
    plain_eval,
    random_circuit,
    reconstruct,
    share,
    truncation_matrix,
)

N, T = 5, 2


@pytest.mark.parametrize("mode", ("grr", "bgw"))
def test_random_circuits_n5_t2(mode: str) -> None:
    rng = random.Random(1988)
    for _ in range(30):
        circ = random_circuit(N, 5, 15, 3, P61, rng)
        inputs = {w: rng.randrange(P61) for w in circ.inputs}
        out, st = bgw(circ, inputs, N, T, P61, rng, mode)
        assert out == plain_eval(circ, inputs, P61)
        if st.multiplications:
            assert st.max_degree_after_mul <= T


def test_product_without_reduction_has_degree_2t() -> None:
    rng = random.Random(2)
    a, b = share(3, T, N, P61, rng), share(4, T, N, P61, rng)
    h = [x * y % P61 for x, y in zip(a, b)]
    assert degree(a, P61) == T and degree(h, P61) == 2 * T
    assert reconstruct(h, P61) == 12          # n = 2t + 1 points still determine it


def test_lagrange_coefficients_for_five_points() -> None:
    lam = lagrange_at_zero([1, 2, 3, 4, 5], P61)
    assert lam == [5, P61 - 10, 10, P61 - 5, 1]


def test_truncation_matrix_cuts_high_coefficients() -> None:
    p = 101
    a = truncation_matrix(N, T, p)
    coeffs = [7, 1, 2, 3, 4]                        # degree 4 = 2t
    vals = [sum(c * pow(x, k, p) for k, c in enumerate(coeffs)) % p for x in range(1, N + 1)]
    cut = [sum(a[j][i] * vals[i] for i in range(N)) % p for j in range(N)]
    assert cut == [(7 + 1 * x + 2 * x * x) % p for x in range(1, N + 1)]


def test_message_counts() -> None:
    rng = random.Random(3)
    circ = Circuit(3, {0: 1, 1: 2}, [2], [("MUL", 0, 1, 2)])
    _, st = bgw(circ, {0: 6, 1: 7}, N, T, P61, rng, "grr")
    assert st.messages == 2 * (N - 1) + N * (N - 1) + N * (N - 1)
    _, st = bgw(circ, {0: 6, 1: 7}, N, T, P61, rng, "bgw")
    assert st.messages == 2 * (N - 1) + 3 * N * (N - 1) + N * (N - 1)


def test_t_must_be_below_half() -> None:
    circ = Circuit(3, {0: 1, 1: 2}, [2], [("MUL", 0, 1, 2)])
    with pytest.raises(ValueError):
        bgw(circ, {0: 1, 1: 1}, 4, 2, P61, random.Random(0))


def test_one_wrong_share_breaks_plain_reconstruction() -> None:
    # A malicious party sends a wrong share at the output. Plain Lagrange
    # interpolation gives a wrong value, and the honest parties cannot tell.
    rng = random.Random(4)
    s = 123456789
    shares = share(s, T, N, P61, rng)
    bad = list(shares)
    bad[2] = (bad[2] + 1) % P61
    assert reconstruct(bad, P61) != s
    assert reconstruct(bad[:T + 1], P61, [1, 2, 3]) != s
    # No polynomial of degree t fits all 5 points, so the error is detected.
    assert degree(bad, P61) > T


def test_two_malicious_parties_win_when_n_is_5() -> None:
    # n = 5, t = 2: parties 4 and 5 replace their shares by the values of
    # g = f + c (x - 1)(x - 2). Then g fits 4 shares and f fits only 3, so
    # "f with 2 errors" and "g with 1 error" both explain what the honest
    # parties see, and g(0) = f(0) + 2c. No decoder can tell the two apart.
    rng = random.Random(6)
    f = [42, rng.randrange(P61), rng.randrange(P61)]
    c = 1000
    g = [(f[0] + 2 * c) % P61, (f[1] - 3 * c) % P61, (f[2] + c) % P61]
    ev = lambda q, x: (q[0] + q[1] * x + q[2] * x * x) % P61  # noqa: E731
    seen = [ev(f, 1), ev(f, 2), ev(f, 3), ev(g, 4), ev(g, 5)]
    assert all(ev(g, x) == ev(f, x) for x in (1, 2))
    found = candidates(seen, T, T, P61)
    assert {42, 42 + 2 * c} <= {q[0] for q in found}
    assert decode_with_errors(seen, T, P61) is None
    # Decoding for one error picks g: the wrong secret.
    assert decode_with_errors(seen, T, P61, e=1) == 42 + 2 * c


def test_reed_solomon_decoding_corrects_t_errors_when_n_is_3t_plus_1() -> None:
    rng = random.Random(5)
    n = 3 * T + 1
    for _ in range(50):
        s = rng.randrange(P61)
        shares = share(s, T, n, P61, rng)
        for i in rng.sample(range(n), T):
            shares[i] = rng.randrange(P61)
        assert decode_with_errors(shares, T, P61) == s
