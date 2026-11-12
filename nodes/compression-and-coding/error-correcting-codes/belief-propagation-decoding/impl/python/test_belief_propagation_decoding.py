# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-propagation-decoding/. The authors are listed in prov/RMPGHV.jsonl.

import itertools
import math
import random

from belief_propagation_decoding import bp_decode

# Checks {0,1,2}, {2,3,4}, {4,5}, {1,6,7}: 12 nodes, 11 edges, connected, so a tree.
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


def exact_llrs(h, llr):
    """Bitwise MAP by enumeration: P(c | y) is proportional to exp(-sum c_j L_j)."""
    words = codewords(h)
    out = []
    for i in range(len(llr)):
        z = [0.0, 0.0]
        for c in words:
            z[c[i]] += math.exp(-sum(cj * lj for cj, lj in zip(c, llr)))
        out.append(math.log(z[0] / z[1]))
    return out


def gallager(n, dv, dc, rng):
    rows = n // dc
    band = [[1 if i * dc <= j < (i + 1) * dc else 0 for j in range(n)] for i in range(rows)]
    h = [r[:] for r in band]
    for _ in range(dv - 1):
        p = list(range(n))
        rng.shuffle(p)
        h += [[r[p[j]] for j in range(n)] for r in band]
    return h


def min_sum(h, llr, iters):
    """Plain min-sum, a test-local reference with the same schedule."""
    m, n = len(h), len(llr)
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    v2c = {(i, j): llr[j] for i in range(m) for j in chk[i]}
    c2v = {}
    bits = [0 if x >= 0 else 1 for x in llr]
    for _ in range(iters):
        for i in range(m):
            for j in chk[i]:
                others = [v2c[(i, k)] for k in chk[i] if k != j]
                s = 1
                for x in others:
                    if x < 0:
                        s = -s
                c2v[(i, j)] = s * min(abs(x) for x in others)
        post = [llr[j] + sum(c2v[(i, j)] for i in var[j]) for j in range(n)]
        bits = [0 if x >= 0 else 1 for x in post]
        if all(sum(bits[j] for j in chk[i]) % 2 == 0 for i in range(m)):
            return bits
        for e in v2c:
            v2c[e] = post[e[1]] - c2v[e]
    return bits


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
    # Codeword 0000000 sent on BPSK; position 2 arrives with the wrong sign.
    llr = [2.0, 1.5, -0.8, 2.2, 1.8, 2.5, 1.2]
    bits, post, it, ok = bp_decode(H74, llr, 20)
    assert bits == [0] * 7 and ok and it == 1
    assert post[2] > 0


def test_exact_on_a_tree() -> None:
    rng = random.Random(3)
    for _ in range(200):
        llr = [rng.uniform(-4, 4) for _ in range(8)]
        _, post, _, _ = bp_decode(TREE, llr, 8, early_stop=False)
        ref = exact_llrs(TREE, llr)
        assert all(abs(a - b) < 1e-9 for a, b in zip(post, ref))


def test_not_exact_with_cycles_but_close() -> None:
    llr = [0.9, -0.4, 1.1, 0.3, -0.7, 1.4, 0.2]
    _, post, _, _ = bp_decode(H74, llr, 1, early_stop=False)
    ref = exact_llrs(H74, llr)
    assert max(abs(a - b) for a, b in zip(post, ref)) > 1e-3  # girth 4: not exact


def test_monte_carlo_ordering() -> None:
    rng = random.Random(5)
    n = 96
    h = gallager(n, 3, 6, rng)
    s2 = 1 / (2 * 0.5 * 10 ** (2.0 / 10))  # rate 1/2, Eb/N0 = 2 dB
    err = [0, 0, 0]
    for _ in range(60):
        y = [1 + rng.gauss(0, math.sqrt(s2)) for _ in range(n)]
        llr = [2 * v / s2 for v in y]
        hard = [0 if v >= 0 else 1 for v in y]
        err[0] += sum(bp_decode(h, llr, 30)[0])
        err[1] += sum(min_sum(h, llr, 30))
        err[2] += sum(bit_flip(h, hard, 60))
    # BP 83, min-sum 125, bit flipping 725 bit errors out of 5760 with this seed;
    # the raw hard decisions have 552, so at this noise level flipping does not help.
    assert err[0] < err[1] < err[2]
