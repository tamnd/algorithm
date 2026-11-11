# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secret-sharing/. The authors are listed in prov/P8BB3K.jsonl.
# There are no official test vectors for these schemes. The tests check
# reconstruction, and check perfect secrecy exactly: in a small field they
# enumerate all the dealer's random choices and verify that the shares of each
# unauthorized set have the same distribution for every secret.

import itertools
import random
from collections import Counter

from secret_sharing import (
    additive_reconstruct,
    additive_share,
    bl_reconstruct,
    bl_satisfies,
    bl_share,
    blakley_normals,
    blakley_normals_ok,
    blakley_reconstruct,
    blakley_share,
    counting_rand,
    rank,
    solve,
)


def views(share_fn, secret, n_random, p, parties):
    """Counter of the joint shares of `parties`, over all random choices."""
    c = Counter()
    for r in itertools.product(range(p), repeat=n_random):
        shares = share_fn(secret, counting_rand(r))
        c[tuple(repr(shares[i]) for i in parties)] += 1
    return c


def test_additive():
    p = 2**61 - 1
    rng = random.Random(1)
    for _ in range(20):
        s = rng.randrange(p)
        shares = additive_share(s, 5, p, lambda: rng.randrange(p))
        assert additive_reconstruct(shares, p) == s
        assert additive_reconstruct(shares[:4], p) != s or shares[4] == 0


def test_additive_perfect_secrecy():
    p, n = 5, 3
    fn = lambda s, rand: additive_share(s, n, p, rand)
    for k in range(1, n):
        for parties in itertools.combinations(range(n), k):
            base = views(fn, 0, n - 1, p, parties)
            assert all(views(fn, s, n - 1, p, parties) == base for s in range(1, p))
            assert len(base) == p**k and set(base.values()) == {p ** (n - 1 - k)}


def test_linear_algebra():
    p = 7
    x = solve([[1, 2], [3, 4]], [5, 6], p)
    assert ((x[0] + 2 * x[1]) % p, (3 * x[0] + 4 * x[1]) % p) == (5, 6)
    assert solve([[1, 2], [2, 4]], [1, 2], p) is None
    assert rank([[1, 2, 3], [2, 4, 6], [0, 1, 0]], p) == 2


def test_blakley_reconstruction_and_secrecy():
    p, t, n = 7, 3, 4
    rng = random.Random(2)
    normals = blakley_normals(t, n, p, lambda: rng.randrange(p))
    assert blakley_normals_ok(normals, t, p)
    fn = lambda s, rand: blakley_share(s, normals, p, rand)
    for s in range(p):
        for r in itertools.product(range(p), repeat=t - 1):
            shares = fn(s, counting_rand(r))
            for ids in itertools.combinations(range(n), t):
                assert blakley_reconstruct(normals, ids, [shares[i] for i in ids], p) == s
    for parties in itertools.combinations(range(n), t - 1):
        base = views(fn, 0, t - 1, p, parties)
        assert len(base) == p ** (t - 1)                 # uniform over GF(7)^2
        assert all(views(fn, s, t - 1, p, parties) == base for s in range(1, p))


def test_blakley_bad_normals_leak():
    # e_1 = (1,1,0) - (0,1,0) is in the span of the first two normals, so these
    # two parties learn s: b_1 - b_2 = x_1.
    p = 7
    normals = [[1, 1, 0], [0, 1, 0], [1, 2, 3], [2, 5, 1]]
    assert not blakley_normals_ok(normals, 3, p)
    rng = random.Random(3)
    for s in range(p):
        b = blakley_share(s, normals, p, lambda: rng.randrange(p))
        assert (b[0] - b[1]) % p == s


BL_FORMULA = ("or", ("and", 1, 2), ("and", 3, ("or", 1, 4)))   # {1,2}, {1,3}, {3,4}


def test_benaloh_leichter_access_structure():
    p, parties = 5, [1, 2, 3, 4]
    fn = lambda s, rand: bl_share(s, BL_FORMULA, p, rand)
    n_random = 2                                    # one per AND gate with 2 children
    for k in range(1, 5):
        for subset in itertools.combinations(parties, k):
            if bl_satisfies(BL_FORMULA, set(subset)):
                for s in range(p):
                    for r in itertools.product(range(p), repeat=n_random):
                        shares = fn(s, counting_rand(r))
                        mine = {i: shares[i] for i in subset}
                        assert bl_reconstruct(BL_FORMULA, mine, p) == s
            else:
                def fn2(s, rand):
                    shares = bl_share(s, BL_FORMULA, p, rand)
                    return [None] + [shares.get(i) for i in parties]
                base = views(fn2, 0, n_random, p, subset)
                assert all(views(fn2, s, n_random, p, subset) == base for s in range(1, p))
    authorized = [set(c) for k in range(1, 5) for c in itertools.combinations(parties, k)
                  if bl_satisfies(BL_FORMULA, set(c))]
    minimal = [a for a in authorized if not any(b < a for b in authorized)]
    assert sorted(map(sorted, minimal)) == [[1, 2], [1, 3], [3, 4]]


def test_benaloh_leichter_threshold_formula():
    # 2-of-3 written as a formula: (1 and 2) or (1 and 3) or (2 and 3).
    f = ("or", ("and", 1, 2), ("and", 1, 3), ("and", 2, 3))
    p = 2**31 - 1
    rng = random.Random(4)
    shares = bl_share(123456, f, p, lambda: rng.randrange(p))
    assert all(len(v) == 2 for v in shares.values())     # two field elements each
    for pair in itertools.combinations([1, 2, 3], 2):
        assert bl_reconstruct(f, {i: shares[i] for i in pair}, p) == 123456
    assert bl_reconstruct(f, {1: shares[1]}, p) is None
