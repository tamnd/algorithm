# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/commitment-scheme/. The authors are listed in prov/AZDCQJ.jsonl.
# There are no official test vectors for these commitment schemes. The tests
# check opening, hiding and binding on toy sizes against local code only.

import hashlib
import random

from commitment_scheme import (
    hash_commit,
    hash_open,
    naor_bad_strings,
    naor_commit,
    naor_open,
    naor_receiver_first,
    prg,
    truncated_commit,
)


def test_hash_commit_opens():
    for msg in [b"", b"a", b"attack at dawn"]:
        c, r = hash_commit(msg)
        assert len(c) == 32 and len(r) == 32
        assert hash_open(c, msg, r)
        assert not hash_open(c, msg + b"!", r)
        assert not hash_open(c, msg, bytes(32) if r != bytes(32) else b"\x01" * 32)


def test_hash_commit_fixed_value():
    # c = SHA-256(r || m), computed here with hashlib as a reference.
    r = bytes(range(32))
    c, _ = hash_commit(b"yes", r)
    assert c == hashlib.sha256(r + b"yes").digest()


def test_hash_commit_hiding_distribution():
    # The first byte of a commitment to 0 and of a commitment to 1 are both
    # close to uniform: a chi-square test on 256 bins for 8192 random r.
    rng = random.Random(1)
    for msg in [b"0", b"1"]:
        counts = [0] * 256
        for _ in range(8192):
            r = rng.getrandbits(256).to_bytes(32, "big")
            counts[hash_commit(msg, r)[0][0]] += 1
        expected = 8192 / 256
        chi2 = sum((x - expected) ** 2 / expected for x in counts)
        # 255 degrees of freedom: mean 255, standard deviation about 22.6.
        assert 160 < chi2 < 360


def test_no_randomness_is_not_hiding():
    # c = H(m) without r: for a small message space the receiver finds m by
    # trying every candidate. Here bids are numbers 0 to 999.
    secret_bid = 637
    c = hashlib.sha256(str(secret_bid).encode()).digest()
    found = [m for m in range(1000) if hashlib.sha256(str(m).encode()).digest() == c]
    assert found == [secret_bid]


def test_truncated_hash_is_not_binding():
    # With the commitment cut to 20 bits, a birthday search over random r
    # finds r0, r1 with the same commitment to "0" and to "1": the committer
    # can open one value both ways. Expected work is about 2^10 tries each.
    rng = random.Random(7)
    seen = {}
    for _ in range(1 << 14):
        r = rng.getrandbits(64).to_bytes(8, "big")
        seen[truncated_commit(b"0", r, 20)] = r
    found = None
    for _ in range(1 << 14):
        r1 = rng.getrandbits(64).to_bytes(8, "big")
        c = truncated_commit(b"1", r1, 20)
        if c in seen:
            found = (seen[c], r1, c)
            break
    assert found is not None
    r0, r1, c = found
    assert truncated_commit(b"0", r0, 20) == c == truncated_commit(b"1", r1, 20)


def test_prg_length_and_determinism():
    for n in [8, 16, 128]:
        y = prg(5, n)
        assert 0 <= y < (1 << (3 * n))
        assert prg(5, n) == y
    assert prg(5, 128) != prg(6, 128)


def test_naor_commit_open_real_size():
    n = 128
    for bit in (0, 1):
        r_string = naor_receiver_first(n)
        c, seed = naor_commit(bit, r_string, n)
        assert naor_open(c, r_string, n, bit, seed)
        assert not naor_open(c, r_string, n, 1 - bit, seed)


def test_naor_binding_exhaustive_toy():
    # n = 8: seeds of 8 bits, outputs of 24 bits. A string R lets the
    # committer cheat only if R = G(s0) xor G(s1). There are at most 2^16
    # such R among 2^24, so a random R is bad with probability at most 2^-8.
    n = 8
    bad = naor_bad_strings(n)
    assert len(bad) <= 1 << (2 * n)
    assert len(bad) / (1 << (3 * n)) <= 2 ** -n
    # For a bad R the committer can indeed open both ways.
    outs = [prg(s, n) for s in range(1 << n)]
    s0, s1 = 3, 200
    r_bad = outs[s0] ^ outs[s1]
    c, _ = naor_commit(0, r_bad, n, seed=s0)
    assert naor_open(c, r_bad, n, 0, s0)
    assert naor_open(c, r_bad, n, 1, s1)
    # For a good R no commitment opens both ways.
    rng = random.Random(3)
    good = next(x for x in iter(lambda: rng.getrandbits(3 * n), None) if x not in bad)
    for s in range(1 << n):
        c, _ = naor_commit(0, good, n, seed=s)
        assert not any(naor_open(c, good, n, 1, t) for t in range(1 << n))


def test_naor_toy_hiding_is_only_computational():
    # With n = 8 an unbounded receiver tells the bit: a commitment to 0 is one
    # of the 256 outputs of G. This is why the PRG must be secure for large n.
    n = 8
    outs = {prg(s, n) for s in range(1 << n)}
    rng = random.Random(4)
    r_string = rng.getrandbits(3 * n)
    wrong = 0
    for trial in range(200):
        bit = trial % 2
        c, _ = naor_commit(bit, r_string, n, seed=rng.getrandbits(n))
        guess = 0 if c in outs else 1
        wrong += guess != bit
    # A guess fails only when G(s) xor R is also an output of G.
    assert wrong <= 4
