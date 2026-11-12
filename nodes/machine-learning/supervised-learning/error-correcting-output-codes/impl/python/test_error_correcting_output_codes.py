# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-correcting-output-codes/. The authors are listed in prov/05H9N7.jsonl.

import random
from itertools import combinations, product

from error_correcting_output_codes import (all_pairs_code, exhaustive_code, exp_loss, hamming_decode,
                                           hinge_loss, logistic_loss, loss_decode, min_row_distance,
                                           one_vs_rest_code, predict, rho, train,
                                           training_error_bound)


def hamming_7_4_rows() -> list[list[int]]:
    """The 16 codewords of the [7, 4] Hamming code, as rows in {-1, +1}."""
    rows = []
    for d in product((0, 1), repeat=4):
        p1, p2, p3 = d[0] ^ d[1] ^ d[3], d[0] ^ d[2] ^ d[3], d[1] ^ d[2] ^ d[3]
        bits = [p1, p2, d[0], p3, d[1], d[2], d[3]]
        rows.append([1 if b else -1 for b in bits])
    return rows


def test_exhaustive_code_shape_and_distance() -> None:
    for k in range(3, 8):
        M = exhaustive_code(k)
        assert len(M) == k and len(M[0]) == 2 ** (k - 1) - 1
        assert min_row_distance(M) == 2 ** (k - 2)
        # every pair of rows is at exactly that distance
        assert all(sum(a != b for a, b in zip(M[r], M[s])) == 2 ** (k - 2)
                   for r, s in combinations(range(k), 2))
        # the columns are all nonconstant columns with a +1 in row 1, each once
        cols = {tuple(M[r][c] for r in range(k)) for c in range(len(M[0]))}
        assert len(cols) == len(M[0]) and all(col[0] == 1 and -1 in col for col in cols)
    assert exhaustive_code(4) == [[1, 1, 1, 1, 1, 1, 1],
                                  [-1, -1, -1, -1, 1, 1, 1],
                                  [-1, -1, 1, 1, -1, -1, 1],
                                  [-1, 1, -1, 1, -1, 1, -1]]


def corrects_exactly(M: list[list[int]]) -> None:
    """Every pattern of at most t = (d - 1) // 2 flips decodes to the sent row as the unique
    nearest row; some pattern of t + 1 flips does not."""
    d = min_row_distance(M)
    t = (d - 1) // 2
    ell = len(M[0])
    for r, row in enumerate(M):
        for w in range(t + 1):
            for pos in combinations(range(ell), w):
                z = [-v if c in pos else v for c, v in enumerate(row)]
                dist = [sum(a != b for a, b in zip(z, other)) for other in M]
                assert dist[r] < min(dist[s] for s in range(len(M)) if s != r)
                assert hamming_decode(M, z) == r
    r, s = next((r, s) for r, s in combinations(range(len(M)), 2)
                if sum(a != b for a, b in zip(M[r], M[s])) == d)
    diff = [c for c in range(ell) if M[r][c] != M[s][c]]
    z = [-v if c in diff[:t + 1] else v for c, v in enumerate(M[r])]
    dist = [sum(a != b for a, b in zip(z, other)) for other in M]
    assert dist[s] <= dist[r]  # r is no longer the unique nearest row


def test_minimum_distance_corrects_floor_d_minus_1_over_2_errors() -> None:
    for k in (3, 4, 5):
        corrects_exactly(exhaustive_code(k))
    corrects_exactly(hamming_7_4_rows())
    corrects_exactly(one_vs_rest_code(5))


def test_hamming_decoding_with_zero_outputs_and_zero_entries() -> None:
    M = all_pairs_code(3)  # columns (0,1), (0,2), (1,2)
    assert M == [[1, 1, 0], [-1, 0, 1], [0, -1, -1]]
    assert hamming_decode(M, [0.7, 0.2, -0.4]) == 0
    assert hamming_decode(M, [0.0, 0.0, 0.0]) == 0  # all distances are 3/2: the tie rule decides


def test_rho_of_standard_codes() -> None:
    for k in range(3, 8):
        assert rho(one_vs_rest_code(k)) == 2
        ell = k * (k - 1) // 2
        assert rho(all_pairs_code(k)) == (ell + 1) / 2


def test_allwein_bound_holds_for_any_outputs() -> None:
    rng = random.Random(7)
    for _ in range(400):
        k, ell = rng.randint(3, 6), rng.randint(3, 10)
        M = [[rng.choice((-1, 0, 1)) for _ in range(ell)] for _ in range(k)]
        if rho(M) == 0:
            continue
        n = rng.randint(1, 30)
        y = [rng.randrange(k) for _ in range(n)]
        Z = [[rng.gauss(0, 1.5) for _ in range(ell)] for _ in range(n)]
        for L in (exp_loss, logistic_loss, hinge_loss):
            eps = sum(L(M[y[i]][s] * Z[i][s]) for i in range(n) for s in range(ell)) / (n * ell)
            err = sum(loss_decode(M, Z[i], L) != y[i] for i in range(n)) / n
            assert err <= training_error_bound(M, eps, L) + 1e-12


def test_end_to_end_with_a_nearest_neighbor_learner() -> None:
    def knn(X, t, m=5):
        def score(x):
            near = sorted(range(len(X)), key=lambda i: abs(X[i][0] - x[0]))[:m]
            return sum(t[i] for i in near) / m  # a real score in [-1, 1]
        return score

    rng = random.Random(2)
    k = 4
    X = [[rng.gauss(10.0 * c, 1.0)] for c in range(k) for _ in range(30)]
    y = [c for c in range(k) for _ in range(30)]
    M = exhaustive_code(k)
    fs = train(X, y, M, knn)
    Xt = [[rng.gauss(10.0 * c, 1.0)] for c in range(k) for _ in range(30)]
    acc = sum(predict(fs, M, x) == c for x, c in zip(Xt, y)) / len(y)
    acc_loss = sum(predict(fs, M, x, exp_loss) == c for x, c in zip(Xt, y)) / len(y)
    assert acc > 0.95 and acc_loss > 0.95
    # one column made useless (always the wrong sign) is corrected, since d = 4 gives t = 1
    broken = fs[:]
    broken[3] = (lambda f: (lambda x: -f(x)))(fs[3])
    assert sum(predict(broken, M, x) == c for x, c in zip(Xt, y)) / len(y) > 0.95
