# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-decoding/. The authors are listed in prov/SCF5ND.jsonl.

import itertools
import math
import random

from turbo_decoding import encode, log_map, rsc_trellis, turbo_decode


def channel(e, rng, s2):
    return {key: [2 * (1 - 2 * b + rng.gauss(0, math.sqrt(s2))) / s2 for b in v] for key, v in e.items()}


def test_log_map_equals_brute_force() -> None:
    rng = random.Random(31)
    edges = rsc_trellis(7, 5, 3)
    for _ in range(300):
        n = rng.randrange(1, 6)
        steps = n + 2
        ls = [rng.gauss(0, 2) for _ in range(steps)]
        lp = [rng.gauss(0, 2) for _ in range(steps)]
        la = [rng.gauss(0, 1) for _ in range(n)] + [0.0, 0.0]
        got = log_map(edges, 4, ls, lp, la)
        paths = []
        for us in itertools.product((0, 1), repeat=steps):
            s, m = 0, 0.0
            for t, u in enumerate(us):
                e = next(x for x in edges if x[0] == s and x[1] == u)
                m += 0.5 * ((1 - 2 * u) * (ls[t] + la[t]) + (1 - 2 * e[3]) * lp[t])
                s = e[2]
            if s == 0:
                paths.append((us, m))
        for t in range(n):
            p0 = math.fsum(math.exp(m) for us, m in paths if us[t] == 0)
            p1 = math.fsum(math.exp(m) for us, m in paths if us[t] == 1)
            assert abs(got[t] - math.log(p0 / p1)) < 1e-9


def test_extrinsic_excludes_own_inputs() -> None:
    # posterior - prior - systematic does not depend on the bit's own prior
    # and systematic LLR: it is what the rest of the code says about the bit.
    rng = random.Random(4)
    edges = rsc_trellis(7, 5, 3)
    for _ in range(200):
        ls = [rng.gauss(0, 2) for _ in range(6)]
        lp = [rng.gauss(0, 2) for _ in range(6)]
        la = [rng.gauss(0, 1) for _ in range(4)] + [0.0, 0.0]
        t = rng.randrange(4)
        post = log_map(edges, 4, ls, lp, la)
        ext = post[t] - la[t] - ls[t]
        ls2, la2 = list(ls), list(la)
        ls2[t] += rng.gauss(0, 3)
        la2[t] += rng.gauss(0, 3)
        post2 = log_map(edges, 4, ls2, lp, la2)
        assert abs(post2[t] - la2[t] - ls2[t] - ext) < 1e-9


def test_noiseless_decodes_in_one_iteration() -> None:
    rng = random.Random(2)
    perm = list(range(40))
    rng.shuffle(perm)
    m = [rng.randrange(2) for _ in range(40)]
    e = encode(m, perm, 7, 5, 3)
    ch = {key: [6.0 * (1 - 2 * b) for b in v] for key, v in e.items()}
    assert turbo_decode(ch, perm, 7, 5, 3, 1)[0] == m


def test_iterations_help_monte_carlo() -> None:
    # Rate 1/3 turbo code, (1, 5/7) constituents, K = 128, seeded random
    # interleaver, BPSK on AWGN at Eb/N0 = 1 dB: s^2 = 1 / (2 R Eb/N0).
    rng = random.Random(99)
    size = 128
    perm = list(range(size))
    rng.shuffle(perm)
    s2 = 1 / (2 * (1 / 3) * 10 ** 0.1)
    errs = [0] * 6
    for _ in range(30):
        m = [rng.randrange(2) for _ in range(size)]
        hist = turbo_decode(channel(encode(m, perm, 7, 5, 3), rng, s2), perm, 7, 5, 3, 6)
        for i, h in enumerate(hist):
            errs[i] += sum(a != b for a, b in zip(h, m))
    total = 30 * size
    assert errs[5] < 0.5 * errs[0]
    assert errs[0] / total < 0.08
    assert errs[5] / total < 0.03
