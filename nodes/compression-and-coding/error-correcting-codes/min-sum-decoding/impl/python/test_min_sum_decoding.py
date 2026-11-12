# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-sum-decoding/. The authors are listed in prov/TA9NEY.jsonl.

import itertools
import math
import random

from min_sum_decoding import check_message, min_sum_decode

TREE = [
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 1],
]
H74 = [[1, 0, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]


def codewords(h):
    n = len(h[0])
    return [c for c in itertools.product((0, 1), repeat=n)
            if all(sum(a * b for a, b in zip(r, c)) % 2 == 0 for r in h)]


def max_log_llrs(h, llr):
    """min over codewords with c_i = 1 of sum c_j L_j, minus the min with c_i = 0."""
    words = codewords(h)
    out = []
    for i in range(len(llr)):
        best = [math.inf, math.inf]
        for c in words:
            best[c[i]] = min(best[c[i]], sum(cj * lj for cj, lj in zip(c, llr)))
        out.append(best[1] - best[0])
    return out


def naive(h, llr, iters, mode, alpha, beta):
    """Per-edge reference: each message recomputed from the other edges."""
    m, n = len(h), len(llr)
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    v2c = {(i, j): llr[j] for i in range(m) for j in chk[i]}
    post = list(llr)
    for _ in range(iters):
        c2v = {(i, j): check_message([v2c[(i, k)] for k in chk[i] if k != j], mode, alpha, beta)
               for (i, j) in v2c}
        post = [llr[j] + sum(c2v[(i, j)] for i in var[j]) for j in range(n)]
        v2c = {(i, j): post[j] - c2v[(i, j)] for (i, j) in v2c}
    return post


def gallager(n, dv, dc, rng):
    rows = n // dc
    band = [[1 if i * dc <= j < (i + 1) * dc else 0 for j in range(n)] for i in range(rows)]
    h = [r[:] for r in band]
    for _ in range(dv - 1):
        p = list(range(n))
        rng.shuffle(p)
        h += [[r[p[j]] for j in range(n)] for r in band]
    return h


def bit_flip(h, hard, iters):
    """Sequential hard-decision bit flipping, a test-local reference."""
    m, n = len(h), len(hard)
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    c = list(hard)
    for _ in range(iters):
        syn = [sum(c[j] for j in chk[i]) & 1 for i in range(m)]
        if not any(syn):
            return c
        cnt = [sum(syn[i] for i in var[j]) for j in range(n)]
        c[cnt.index(max(cnt))] ^= 1
    return c


def test_hamming_example() -> None:
    llr = [2.0, 1.5, -0.8, 2.2, 1.8, 2.5, 1.2]
    bits, post, it, ok = min_sum_decode(H74, llr, 20)
    assert bits == [0] * 7 and ok and it == 2
    # Iteration 1: position 2 is in all three checks, and each sends the least
    # other magnitude with a plus sign. Position 1 gets -0.8 from two checks.
    _, post, _, ok = min_sum_decode(H74, llr, 1)
    assert abs(post[2] - (-0.8 + 1.8 + 1.5 + 1.2)) < 1e-12
    assert abs(post[1] - (1.5 - 0.8 - 0.8)) < 1e-12 and not ok


def test_tree_gives_max_log_llrs() -> None:
    rng = random.Random(3)
    for _ in range(200):
        llr = [rng.uniform(-4, 4) for _ in range(8)]
        _, post, _, _ = min_sum_decode(TREE, llr, 8, early_stop=False)
        ref = max_log_llrs(TREE, llr)
        assert all(abs(a - b) < 1e-9 for a, b in zip(post, ref))


def test_two_least_trick_against_naive() -> None:
    rng = random.Random(11)
    for _ in range(200):
        m, n = rng.randrange(1, 5), rng.randrange(2, 9)
        h = [[rng.randrange(2) for _ in range(n)] for _ in range(m)]
        h = [r for r in h if sum(r) >= 2] or [[1] * n]
        llr = [rng.uniform(-3, 3) for _ in range(n)]
        for mode in ("plain", "normalized", "offset"):
            _, post, _, _ = min_sum_decode(h, llr, 5, mode, 0.75, 0.3, early_stop=False)
            ref = naive(h, llr, 5, mode, 0.75, 0.3)
            assert all(abs(a - b) < 1e-9 for a, b in zip(post, ref))


def test_corrections_reduce_to_plain_and_scale() -> None:
    rng = random.Random(7)
    h = gallager(24, 3, 6, rng)
    for _ in range(50):
        llr = [rng.gauss(2, 2) for _ in range(24)]
        plain = min_sum_decode(h, llr, 10, early_stop=False)
        assert min_sum_decode(h, llr, 10, "normalized", 1.0, early_stop=False) == plain
        assert min_sum_decode(h, llr, 10, "offset", beta=0.0, early_stop=False) == plain
        # Plain min-sum does not need the noise level: scaling all LLRs scales all messages.
        scaled = min_sum_decode(h, [4.0 * x for x in llr], 10, early_stop=False)
        assert scaled[0] == plain[0]
        assert all(abs(a - 4.0 * b) < 1e-9 for a, b in zip(scaled[1], plain[1]))


def test_monte_carlo_corrections_help() -> None:
    rng = random.Random(5)
    n = 96
    h = gallager(n, 3, 6, rng)
    s2 = 1 / (2 * 0.5 * 10 ** (2.0 / 10))  # rate 1/2, Eb/N0 = 2 dB
    err = {"plain": 0, "normalized": 0, "offset": 0, "flip": 0}
    for _ in range(60):
        y = [1 + rng.gauss(0, math.sqrt(s2)) for _ in range(n)]
        llr = [2 * v / s2 for v in y]
        err["plain"] += sum(min_sum_decode(h, llr, 30)[0])
        err["normalized"] += sum(min_sum_decode(h, llr, 30, "normalized", 0.8)[0])
        err["offset"] += sum(min_sum_decode(h, llr, 30, "offset", beta=0.5)[0])
        err["flip"] += sum(bit_flip(h, [0 if v >= 0 else 1 for v in y], 60))
    # With this seed: plain 125, normalized 107, offset 106, bit flipping 725 of 5760.
    assert err["normalized"] < err["plain"] and err["offset"] < err["plain"]
    assert err["plain"] < err["flip"]
