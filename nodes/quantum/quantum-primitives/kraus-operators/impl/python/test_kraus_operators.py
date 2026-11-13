# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraus-operators/. The authors are listed in prov/XS6DA3.jsonl.

import math
import random

from kraus_operators import (
    amplitude_damping,
    apply_by_stinespring,
    apply_channel,
    bit_flip,
    choi_matrix,
    compose,
    depolarizing,
    is_trace_preserving,
    kraus_from_choi,
    mix_kraus,
    phase_damping,
    phase_flip,
    stinespring_isometry,
)
from qsim import (
    X,
    Y,
    Z,
    dagger,
    eigvalsh,
    identity,
    is_hermitian,
    matmul,
    max_abs_diff,
    random_density,
    random_unitary,
    scale,
    trace,
    trace_out_first,
)

TOL = 1e-9


def random_channel(rng, din, dout, r):
    """Kraus operators cut from the first din columns of a random unitary on C^(dout * r).

    An isometry from C^din needs dout * r >= din, so r is raised when it is too small.
    """
    r = max(r, -(-din // dout))
    u = random_unitary(rng, dout * r)
    return [[[u[o * r + k][i] for i in range(din)] for o in range(dout)] for k in range(r)]


def bloch(rho):
    return [trace(matmul(rho, m)).real for m in (X, Y, Z)]


def from_bloch(r):
    rx, ry, rz = r
    return [[(1 + rz) / 2, (rx - 1j * ry) / 2], [(rx + 1j * ry) / 2, (1 - rz) / 2]]


def is_state(rho, tol=TOL):
    return is_hermitian(rho, tol) and abs(trace(rho) - 1) < tol and eigvalsh(rho)[0] > -tol


def standard_channels():
    return [bit_flip(0.3), phase_flip(0.2), depolarizing(0.5), amplitude_damping(0.4), phase_damping(0.7)]


def test_trace_preserving():
    for ch in standard_channels():
        assert is_trace_preserving(ch)
    rng = random.Random(21)
    for _ in range(20):
        assert is_trace_preserving(random_channel(rng, rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 4)))
    assert not is_trace_preserving([[[1, 0], [0, 0.5]]])  # a contraction alone loses trace


def test_kraus_equals_stinespring():
    rng = random.Random(22)
    for _ in range(40):
        din, dout, r = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 4)
        ch = random_channel(rng, din, dout, r)
        v = stinespring_isometry(ch)
        assert max_abs_diff(matmul(dagger(v), v), identity(din)) < TOL  # V is an isometry
        rho = random_density(rng, din)
        out = apply_channel(ch, rho)
        assert max_abs_diff(out, apply_by_stinespring(ch, rho)) < TOL
        assert is_state(out)
    for ch in standard_channels():
        rho = random_density(rng, 2)
        assert max_abs_diff(apply_channel(ch, rho), apply_by_stinespring(ch, rho)) < TOL


def test_bloch_closed_forms():
    rng = random.Random(23)
    p, g = 0.3, 0.4
    s = 1 - 2 * p
    for _ in range(50):
        rho = random_density(rng, 2)
        rx, ry, rz = bloch(rho)
        cases = [
            (bit_flip(p), [rx, s * ry, s * rz]),
            (phase_flip(p), [s * rx, s * ry, rz]),
            (depolarizing(p), [(1 - p) * rx, (1 - p) * ry, (1 - p) * rz]),
            (amplitude_damping(g), [math.sqrt(1 - g) * rx, math.sqrt(1 - g) * ry, g + (1 - g) * rz]),
            (phase_damping(g), [math.sqrt(1 - g) * rx, math.sqrt(1 - g) * ry, rz]),
        ]
        for ch, expected in cases:
            assert max(abs(a - b) for a, b in zip(bloch(apply_channel(ch, rho)), expected)) < TOL
    full = depolarizing(1.0)
    assert max_abs_diff(apply_channel(full, from_bloch([0.6, 0, 0.8])), scale(0.5, identity(2))) < TOL
    assert max_abs_diff(apply_channel(amplitude_damping(1.0), [[0, 0], [0, 1]]), [[1, 0], [0, 0]]) < TOL


def test_choi_matrix_properties():
    rng = random.Random(24)
    for _ in range(20):
        din, dout, r = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 4)
        ch = random_channel(rng, din, dout, r)
        j = choi_matrix(ch)
        assert is_hermitian(j) and eigvalsh(j)[0] > -TOL  # completely positive
        assert max_abs_diff(trace_out_first(j, dout, din), identity(din)) < TOL  # trace preserving
        assert sum(1 for x in eigvalsh(j) if x > 1e-9) <= min(len(ch), din * dout)


def test_kraus_from_choi_is_minimal_and_equal():
    rng = random.Random(25)
    for _ in range(20):
        din, dout, r = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 6)
        ch = random_channel(rng, din, dout, r)
        new = kraus_from_choi(choi_matrix(ch), din, dout)
        assert len(new) <= min(len(ch), din * dout)
        rho = random_density(rng, din)
        assert max_abs_diff(apply_channel(ch, rho), apply_channel(new, rho)) < 1e-8
    assert len(kraus_from_choi(choi_matrix(depolarizing(1.0)), 2, 2)) == 4  # d^2 = 4 are needed
    assert len(kraus_from_choi(choi_matrix([random_unitary(rng, 3)]), 3, 3)) == 1


def test_unitary_freedom():
    rng = random.Random(26)
    for _ in range(20):
        ch = random_channel(rng, 2, 2, 3)
        mixed = mix_kraus(ch, random_unitary(rng, 3))
        assert max_abs_diff(choi_matrix(ch), choi_matrix(mixed)) < TOL
    # depolarizing with p = 1 is also the uniform Pauli twirl, a different list
    twirl = [scale(0.5, m) for m in (identity(2), X, Y, Z)]
    assert max_abs_diff(choi_matrix(twirl), choi_matrix(depolarizing(1.0))) < TOL
    # a non-unitary mix gives a different map
    bad = mix_kraus(bit_flip(0.3), [[1, 1], [0, 1]])
    assert max_abs_diff(choi_matrix(bad), choi_matrix(bit_flip(0.3))) > 0.1


def test_composition():
    rng = random.Random(27)
    a, b = random_channel(rng, 2, 3, 2), random_channel(rng, 3, 2, 3)
    ba = compose(b, a)
    assert is_trace_preserving(ba)
    for _ in range(10):
        rho = random_density(rng, 2)
        assert max_abs_diff(apply_channel(ba, rho), apply_channel(b, apply_channel(a, rho))) < TOL


def test_transpose_is_not_completely_positive():
    # J = sum_ij T(|i><j|) tensor |i><j| for the transpose T. It is SWAP, with eigenvalue -1,
    # so T has no Kraus form, although T maps every state to a state.
    j = [[0] * 4 for _ in range(4)]
    for i1 in range(2):
        for i2 in range(2):
            j[i2 * 2 + i1][i1 * 2 + i2] += 1  # T(|i1><i2|) = |i2><i1|, placed at (o1, i1), (o2, i2)
    vals = eigvalsh(j)
    assert abs(vals[0] + 1) < TOL and all(abs(x - 1) < TOL for x in vals[1:])
    rng = random.Random(28)
    rho = random_density(rng, 2)
    assert is_state([[rho[c][r] for c in range(2)] for r in range(2)])
