# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qubitization/. The authors are listed in prov/8Q7YB1.jsonl.

import cmath
import math
import random

from qubitization import hermitian_encoding, lcu_block_encoding, qubitize, walk_operator
from qsim import (
    chebyshev_t,
    dagger,
    eigh,
    hermitian_function,
    identity,
    kron,
    matmul,
    matvec,
    max_abs_diff,
    pauli_sum_matrix,
    random_unitary,
    scale,
    top_left_block,
)

TOL = 1e-10


def random_terms(rng, n, big_l):
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice("IXYZ") for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def unitary_eigenvalues(w, rng):
    """Eigenvalues of a unitary: diagonalize the Hermitian (W + W^dagger)/2 + c (W - W^dagger)/(2i) and take v^dagger W v."""
    c = rng.uniform(0.2, 0.5)
    wd = dagger(w)
    d = len(w)
    m = [[(w[i][j] + wd[i][j]) / 2 + c * (w[i][j] - wd[i][j]) / 2j for j in range(d)] for i in range(d)]
    _, vecs = eigh(m)
    out = []
    for k in range(d):
        v = [vecs[i][k] for i in range(d)]
        wv = matvec(w, v)
        out.append(sum(p.conjugate() * q for p, q in zip(v, wv)))
    return out


def match_spectrum(found, predicted):
    """Remove each predicted value from found (within TOL); return what is left."""
    left = list(found)
    for z in predicted:
        k = min(range(len(left)), key=lambda i: abs(left[i] - z))
        assert abs(left[k] - z) < 1e-8, (z, left[k])
        left.pop(k)
    return left


def test_hand_example_x_plus_z():
    # H = X + Z, alpha = 2, eigenvalues +-sqrt(2): x = +-0.7071, so the walk has eigenphases +-pi/4 and +-3pi/4.
    u, alpha, a = lcu_block_encoding([(1.0, "X"), (1.0, "Z")])
    assert alpha == 2 and a == 1
    w = walk_operator(u, a, 1)
    found = unitary_eigenvalues(w, random.Random(40))
    predicted = [cmath.exp(1j * s * k * math.pi / 4) for k in (1, 3) for s in (1, -1)]
    assert match_spectrum(found, predicted) == []


def test_walk_eigenvalues_are_exp_of_plus_minus_arccos():
    rng = random.Random(41)
    for n, big_l in [(1, 3), (2, 4)]:
        terms = random_terms(rng, n, big_l)
        u, alpha, a = lcu_block_encoding(terms)
        assert max_abs_diff(u, dagger(u)) < TOL  # Hermitian, and so U^2 = I
        w, planes = qubitize(u, a, n)
        h_vals, _ = eigh(pauli_sum_matrix(terms))
        predicted = []
        for g, gp, x, theta in planes:
            # The plane is invariant: W|G> = x|G> - s|G_perp> and W|G_perp> = s|G> + x|G_perp>.
            s = math.sqrt(1 - x * x)
            wg, wgp = matvec(w, g), matvec(w, gp)
            assert max(abs(p - (x * q - s * r)) for p, q, r in zip(wg, g, gp)) < TOL
            assert max(abs(p - (s * q + x * r)) for p, q, r in zip(wgp, g, gp)) < TOL
            # (|G> +- i|G_perp>)/sqrt(2) are eigenvectors with eigenvalues e^(+-i arccos x).
            for sign in (1, -1):
                v = [(q + sign * 1j * r) / math.sqrt(2) for q, r in zip(g, gp)]
                lam = cmath.exp(sign * 1j * theta)
                assert max(abs(p - lam * q) for p, q in zip(matvec(w, v), v)) < TOL
                predicted.append(lam)
        assert max(abs(x - v / alpha) for (_, _, x, _), v in zip(sorted(planes, key=lambda p: p[2]), sorted(h_vals))) < TOL
        # The full spectrum: the 2 * 2^n predicted values, and +-1 on the rest of the space.
        rest = match_spectrum(unitary_eigenvalues(w, rng), predicted)
        assert len(rest) == len(w) - 2 * (1 << n)
        assert all(min(abs(z - 1), abs(z + 1)) < 1e-8 for z in rest)


def test_powers_of_the_walk_give_chebyshev_polynomials():
    rng = random.Random(42)
    terms = random_terms(rng, 2, 4)
    u, alpha, a = lcu_block_encoding(terms)
    w = walk_operator(u, a, 2)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    p = identity(len(w))
    for k in range(7):
        target = hermitian_function(hn, lambda lam: chebyshev_t(k, lam))
        assert max_abs_diff(top_left_block(p, 4), target) < 1e-9
        p = matmul(w, p)


def non_hermitian_encoding(u, a, n, rng):
    """(B (x) I) U with B = 1 (+) a random unitary on the other ancilla states: the same block, but U is not Hermitian."""
    k = (1 << a) - 1
    v = random_unitary(k, rng)
    b = [[1 + 0j if i == j == 0 else 0j for j in range(k + 1)] for i in range(k + 1)]
    for i in range(k):
        for j in range(k):
            b[i + 1][j + 1] = v[i][j]
    return matmul(kron(b, identity(1 << n)), u)


def test_a_non_hermitian_encoding_must_be_made_hermitian_first():
    rng = random.Random(43)
    n = 1
    terms = random_terms(rng, n, 3)
    u, alpha, a = lcu_block_encoding(terms)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    v = non_hermitian_encoding(u, a, n, rng)
    assert max_abs_diff(top_left_block(v, 2), hn) < TOL
    assert max_abs_diff(v, dagger(v)) > 0.1
    w_bad = walk_operator(v, a, n)
    t2 = hermitian_function(hn, lambda lam: chebyshev_t(2, lam))
    assert max_abs_diff(top_left_block(matmul(w_bad, w_bad), 2), t2) > 1e-3  # the walk is wrong
    uh, ah = hermitian_encoding(v, a, n)
    assert ah == a + 1
    assert max_abs_diff(uh, dagger(uh)) < TOL
    assert max_abs_diff(matmul(uh, uh), identity(len(uh))) < TOL
    assert max_abs_diff(top_left_block(uh, 2), hn) < TOL
    w = walk_operator(uh, ah, n)
    p = identity(len(w))
    for k in range(5):
        target = hermitian_function(hn, lambda lam: chebyshev_t(k, lam))
        assert max_abs_diff(top_left_block(p, 2), target) < 1e-9
        p = matmul(w, p)
