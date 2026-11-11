# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rolling-checksum/. The authors are listed in prov/6HMBPD.jsonl.

import random

from rolling_checksum import (
    M,
    RABIN_POLY,
    RabinWindow,
    cdc_chunks,
    delta,
    pack,
    patch,
    poly_mod,
    roll,
    signature,
    weak,
)


def weak_oracle(block: bytes) -> int:
    """Independent form: b is the sum of the prefix sums of the block."""
    a = b = 0
    for x in block:
        a += x
        b += a
    return (a % M) | ((b % M) << 16)


def test_page_example() -> None:
    # Window "abcd" then roll to "bcde": a = 394 then 398, b = 980 then 990.
    a, b = weak(b"abcd")
    assert (a, b) == (394, 4 * 97 + 3 * 98 + 2 * 99 + 100) == (394, 980)
    a, b = roll(a, b, ord("a"), ord("e"), 4)
    assert (a, b) == weak(b"bcde") == (398, 990)


def test_roll_equals_recompute() -> None:
    rng = random.Random(9101)
    for _ in range(60):
        size = rng.choice([1, 2, 7, 64, 700])
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(size + 200))
        a, b = weak(data[:size])
        assert pack(a, b) == weak_oracle(data[:size])
        for k in range(1, len(data) - size + 1):
            a, b = roll(a, b, data[k - 1], data[k + size - 1], size)
            assert pack(a, b) == weak_oracle(data[k : k + size])


def edit(rng: random.Random, data: bytes) -> bytes:
    d = bytearray(data)
    for _ in range(rng.randrange(0, 5)):
        op = rng.randrange(3)
        i = rng.randrange(len(d) + 1)
        if op == 0:
            d[i:i] = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 40)))
        elif op == 1:
            del d[i : i + rng.randrange(1, 40)]
        elif d:
            d[min(i, len(d) - 1)] ^= 1 + rng.randrange(255)
    return bytes(d)


def test_delta_rebuilds_the_file() -> None:
    rng = random.Random(9102)
    for _ in range(500):
        old = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 600)))
        new = edit(rng, old) if rng.random() < 0.8 else bytes(rng.randrange(4) for _ in range(rng.randrange(0, 300)))
        size = rng.choice([1, 4, 16, 32])
        sig = signature(old, size)
        assert patch(old, delta(new, sig, size), size) == new


def test_delta_is_small_for_an_insertion() -> None:
    rng = random.Random(9103)
    old = bytes(rng.randrange(256) for _ in range(8000))
    new = old[:100] + b"INSERTED TEXT" + old[100:]
    size = 64
    ins = delta(new, signature(old, size), size)
    literal = sum(len(arg) for op, arg in ins if op == "data")  # type: ignore[arg-type]
    copies = sum(1 for op, _ in ins if op == "copy")
    assert patch(old, ins, size) == new
    assert literal <= size + 13
    assert copies >= 8000 // size - 2


def test_weak_collisions_are_resolved_by_the_strong_hash() -> None:
    # Two different blocks with the same a = 4 and b = 9: the weak checksum matches,
    # the strong hash does not, so the sender sends the bytes.
    assert weak(b"\x01\x03\x00") == weak(b"\x02\x01\x01")
    old = b"\x01\x03\x00"
    new = b"\x02\x01\x01"
    ins = delta(new, signature(old, 3), 3)
    assert ins == [("data", new)]


def is_irreducible(p: int) -> bool:
    """Rabin's test: x^(2^n) = x mod p and gcd(x^(2^(n/q)) - x, p) = 1 for primes q | n."""

    def mulmod(a: int, b: int) -> int:
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a = poly_mod(a << 1, p)
        return r

    def x_pow_2k(k: int) -> int:
        r = 2
        for _ in range(k):
            r = mulmod(r, r)
        return r

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, poly_mod(a, b)
        return a

    n = p.bit_length() - 1
    if x_pow_2k(n) != 2:
        return False
    primes = [q for q in range(2, n + 1) if n % q == 0 and all(q % r for r in range(2, q))]
    return all(gcd(x_pow_2k(n // q) ^ 2, p) == 1 for q in primes)


def test_rabin_polynomial_is_irreducible() -> None:
    assert RABIN_POLY.bit_length() - 1 == 63
    assert is_irreducible(RABIN_POLY)
    assert not is_irreducible(0b10101)  # x^4 + x^2 + 1 = (x^2 + x + 1)^2


def test_rabin_roll_equals_direct_fingerprint() -> None:
    rng = random.Random(9104)
    for w in (1, 8, 48):
        rw = RabinWindow(w)
        data = bytes(rng.randrange(256) for _ in range(300))
        for i, x in enumerate(data):
            fp = rw.slide(x)
            win = data[max(0, i + 1 - w) : i + 1]
            assert fp == poly_mod(int.from_bytes(win, "big"), RABIN_POLY)


def test_cdc_rebuilds_and_respects_bounds() -> None:
    rng = random.Random(9105)
    for _ in range(20):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 6000)))
        chunks = cdc_chunks(data)
        assert b"".join(chunks) == data
        assert all(len(c) <= 2048 for c in chunks)
        assert all(len(c) >= 64 for c in chunks[:-1])


def test_insertion_near_the_start_changes_few_chunks() -> None:
    rng = random.Random(9106)
    data = bytes(rng.randrange(256) for _ in range(20000))
    edited = data[:500] + b"a few new bytes" + data[500:]
    before = cdc_chunks(data)
    after = cdc_chunks(edited)
    assert len(before) > 40
    new_chunks = set(after) - set(before)
    assert len(new_chunks) <= 3
    # Fixed-size blocks lose almost every block after the insertion point.
    fixed = lambda d: {d[i : i + 256] for i in range(0, len(d), 256)}  # noqa: E731
    assert len(fixed(edited) - fixed(data)) > 70
