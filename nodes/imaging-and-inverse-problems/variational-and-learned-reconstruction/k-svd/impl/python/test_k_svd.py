# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-svd/. The authors are listed in prov/0XCKNF.jsonl.

import math
import random
from itertools import combinations

from imgla import sym_eig
from k_svd import exact_code, ksvd, objective, omp, update_atom


def unit(v):
    s = math.sqrt(sum(t * t for t in v))
    return [t / s for t in v]


def planted(rng, n, kk, s, count):
    true = [unit([rng.gauss(0.0, 1.0) for _ in range(n)]) for _ in range(kk)]
    signals = []
    for _ in range(count):
        y = [0.0] * n
        for k in rng.sample(range(kk), s):
            c = rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 1.5)
            y = [a + c * b for a, b in zip(y, true[k])]
        signals.append(y)
    return true, signals


def recovered(true, atoms):
    # Aharon, Elad and Bruckstein count an atom as found when 1 - |<d, d_true>| < 0.01.
    count = 0
    for d in true:
        best = max(abs(sum(p * q for p, q in zip(d, a))) for a in atoms)
        if 1.0 - best < 0.01:
            count += 1
    return count


def test_hand_example():
    # D = (e1, e2), s = 1, signals (2, 1), (4, 2), (1, -2). The objective goes 6 -> 1 -> 0.
    signals = [[2.0, 1.0], [4.0, 2.0], [1.0, -2.0]]
    atoms = [[1.0, 0.0], [0.0, 1.0]]
    codes = [omp(atoms, y, 1) for y in signals]
    assert codes == [[2.0, 0.0], [4.0, 0.0], [0.0, -2.0]]
    assert abs(objective(signals, atoms, codes) - 6.0) <= 1e-12
    update_atom(signals, atoms, codes, 0)
    assert abs(abs(atoms[0][0]) - 2.0 / math.sqrt(5.0)) <= 1e-12
    assert abs(abs(codes[1][0]) - 2.0 * math.sqrt(5.0)) <= 1e-12
    assert abs(objective(signals, atoms, codes) - 1.0) <= 1e-12
    update_atom(signals, atoms, codes, 1)
    assert objective(signals, atoms, codes) <= 1e-24


def test_exact_coder_against_enumeration_of_supports():
    rng = random.Random(1)
    atoms = [unit([rng.gauss(0.0, 1.0) for _ in range(4)]) for _ in range(6)]
    for _ in range(5):
        y = [rng.gauss(0.0, 1.0) for _ in range(4)]
        x = exact_code(atoms, y, 2)
        assert sum(1 for v in x if v != 0.0) <= 2
        r = objective([y], atoms, [x])
        # No pair of atoms gives a smaller residual: solve the 2 x 2 normal
        # equations of each pair directly.
        for i, j in combinations(range(6), 2):
            a, b = atoms[i], atoms[j]
            g11 = sum(p * p for p in a)
            g12 = sum(p * q for p, q in zip(a, b))
            g22 = sum(q * q for q in b)
            h1 = sum(p * q for p, q in zip(a, y))
            h2 = sum(p * q for p, q in zip(b, y))
            det = g11 * g22 - g12 * g12
            c1 = (g22 * h1 - g12 * h2) / det
            c2 = (g11 * h2 - g12 * h1) / det
            res = sum((yy - c1 * p - c2 * q) ** 2 for yy, p, q in zip(y, a, b))
            assert r <= res + 1e-12
        # OMP is never better than the exact coder.
        assert r <= objective([y], atoms, [omp(atoms, y, 2)]) + 1e-12


def test_atom_update_is_the_best_rank_one_fit_and_does_not_increase_the_objective():
    rng = random.Random(2)
    n, kk, s = 6, 9, 2
    _, signals = planted(rng, n, kk, s, 40)
    atoms = [unit([rng.gauss(0.0, 1.0) for _ in range(n)]) for _ in range(kk)]
    codes = [omp(atoms, y, s) for y in signals]
    for k in range(kk):
        omega = [i for i, x in enumerate(codes) if x[k] != 0.0]
        before = objective(signals, atoms, codes)
        # The restricted error matrix E (columns indexed by omega) and its
        # largest singular value, from the eigenvalues of E E^T.
        rest = 0.0
        cols = []
        for i, (y, x) in enumerate(zip(signals, codes)):
            xr = list(x)
            if i in omega:
                xr[k] = 0.0
            approx = [sum(xr[j] * atoms[j][t] for j in range(kk)) for t in range(n)]
            e = [a - b for a, b in zip(y, approx)]
            if i in omega:
                cols.append(e)
            else:
                rest += sum(v * v for v in e)
        update_atom(signals, atoms, codes, k)
        after = objective(signals, atoms, codes)
        assert after <= before + 1e-10
        assert abs(sum(v * v for v in atoms[k]) - 1.0) <= 1e-12
        if cols:
            eet = [[sum(c[p] * c[q] for c in cols) for q in range(n)] for p in range(n)]
            w, _ = sym_eig(eet)
            frob = sum(v * v for c in cols for v in c)
            assert abs(after - (rest + frob - w[-1])) <= 1e-9 * (1.0 + frob)


def test_monotone_with_the_exact_coder():
    rng = random.Random(3)
    n, kk, s = 5, 7, 2
    _, signals = planted(rng, n, kk, s, 20)
    signals = [[v + rng.gauss(0.0, 0.05) for v in y] for y in signals]
    init = [unit(signals[i]) for i in range(kk)]
    _, _, hist = ksvd(signals, init, s, iters=4, coder=exact_code)
    prev = math.inf
    for after_coding, after_update in hist:
        assert after_coding <= prev + 1e-10
        assert after_update <= after_coding + 1e-10
        prev = after_update


def test_local_recovery_of_a_planted_dictionary():
    # Start near the true dictionary: K-SVD with OMP moves every atom onto
    # the true one (up to sign).
    rng = random.Random(40)
    n, kk, s = 8, 10, 2
    true, signals = planted(rng, n, kk, s, 120)
    init = [unit([v + 0.15 * rng.gauss(0.0, 1.0) for v in d]) for d in true]
    assert recovered(true, init) < kk
    atoms, _, hist = ksvd(signals, init, s, iters=8)
    assert recovered(true, atoms) == kk
    # The objective falls, but not to 0: OMP picks a wrong support for some signals.
    assert hist[-1][1] < 0.5 * hist[0][0]


def test_global_recovery_from_data_initialization():
    # Initialized with normalized signals. This is not guaranteed: on other
    # seeds the method stops in a local minimum with fewer atoms found.
    rng = random.Random(0)
    n, kk, s = 8, 10, 2
    true, signals = planted(rng, n, kk, s, 150)
    init = [unit(signals[i]) for i in rng.sample(range(len(signals)), kk)]
    atoms, _, _ = ksvd(signals, init, s, iters=15)
    assert recovered(true, atoms) >= 8
