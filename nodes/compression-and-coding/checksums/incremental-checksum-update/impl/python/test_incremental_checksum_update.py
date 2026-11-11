# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-checksum-update/. The authors are listed in prov/RGZ1Q3.jsonl.

import random

from incremental_checksum_update import (
    decrement_ttl,
    update_rfc1141,
    update_rfc1624,
    update_rfc1624_eqn4,
    update_word,
)


def full_checksum(header: bytes, field: int = 10) -> int:
    """Independent full recompute: complement of the ones' complement sum with the field zeroed."""
    h = bytes(header[:field]) + b"\x00\x00" + bytes(header[field + 2 :])
    total = sum((h[i] << 8) | h[i + 1] for i in range(0, len(h), 2))
    s = 0 if total == 0 else (total - 1) % 0xFFFF + 1
    return ~s & 0xFFFF


def test_rfc1624_section4_example() -> None:
    # RFC 1624 Section 4: m = 0x5555 changes to m' = 0x3285, and the ones'
    # complement sum of the other header words is C = 0xCD7A.
    hc = 0xDD2F  # ~(0xCD7A + 0x5555) = ~0x22D0
    assert full_checksum(bytes.fromhex("cd7a55550000")[:4] + b"\x00\x00", 4) == 0xDD2F
    assert update_rfc1141(hc, 0x5555, 0x3285) == 0xFFFF  # Eqn. 2: -0, which no IP header can hold
    assert update_rfc1624(hc, 0x5555, 0x3285) == 0x0000  # Eqn. 3: matches the recompute
    assert update_rfc1624_eqn4(hc, 0x5555, 0x3285) == 0x0000  # Eqn. 4
    assert full_checksum(bytes.fromhex("cd7a32850000"), 4) == 0x0000
    # Section 5: an end system that sums the whole header accepts both values.
    for field in (0xFFFF, 0x0000):
        s = 0xCD7A + 0x3285 + field
        s = (s & 0xFFFF) + (s >> 16)
        assert s == 0xFFFF


def random_ipv4_header(rng: random.Random) -> bytearray:
    ihl = rng.randrange(5, 16)
    h = bytearray(rng.randrange(256) for _ in range(4 * ihl))
    h[0] = 0x40 | ihl
    h[8] = rng.randrange(1, 256)
    h[10:12] = full_checksum(bytes(h)).to_bytes(2, "big")
    return h


def test_ttl_decrement_matches_recompute() -> None:
    rng = random.Random(6101)
    for _ in range(1000):
        h = random_ipv4_header(rng)
        while h[8] > 0 and rng.random() < 0.9:
            decrement_ttl(h)
            assert int.from_bytes(h[10:12], "big") == full_checksum(bytes(h))


def test_known_header_ttl() -> None:
    # The header 4500 0073 0000 4000 4011 b861 c0a8 0001 c0a8 00c7 (Wikipedia,
    # "Internet checksum"). TTL 0x40 -> 0x3f adds 0x0100 to the checksum: b961.
    h = bytearray.fromhex("45000073000040004011b861c0a80001c0a800c7")
    decrement_ttl(h)
    assert h[8] == 0x3F
    assert h[10:12] == bytes.fromhex("b961")
    assert full_checksum(bytes(h)) == 0xB961


def test_random_edits_rfc1624_equals_recompute() -> None:
    rng = random.Random(6102)
    for _ in range(3000):
        h = random_ipv4_header(rng)
        off = rng.choice([o for o in range(0, len(h), 2) if o != 10])
        new = rng.choice([0, 0xFFFF, rng.randrange(0x10000)])
        g = bytearray(h)
        update_word(h, off, new)
        assert int.from_bytes(h[10:12], "big") == full_checksum(bytes(h))
        update_word(g, off, new, update_rfc1624_eqn4)
        assert g == h


def test_rfc1141_fails_exactly_when_the_true_checksum_is_zero() -> None:
    # Search for edits that make the true new checksum 0x0000; RFC 1141 then gives
    # 0xFFFF, and in every other case it agrees with the recompute.
    rng = random.Random(6103)
    zero_cases = 0
    for _ in range(4000):
        h = random_ipv4_header(rng)
        off = rng.choice([o for o in range(0, len(h), 2) if o != 10])
        m = int.from_bytes(h[off : off + 2], "big")
        hc = int.from_bytes(h[10:12], "big")
        if rng.random() < 0.5:
            # pick m' so that the new ones' complement sum is 0xFFFF (true HC' = 0)
            rest = ((~hc & 0xFFFF) - m) % 0xFFFF  # the sum of the other words, mod 0xFFFF
            m2 = (0xFFFF - rest) % 0xFFFF
        else:
            m2 = rng.randrange(0x10000)
        g = bytearray(h)
        g[off : off + 2] = m2.to_bytes(2, "big")
        truth = full_checksum(bytes(g))
        old = update_rfc1141(hc, m, m2)
        assert update_rfc1624(hc, m, m2) == truth
        if truth == 0:
            zero_cases += 1
            assert old == 0xFFFF
        else:
            assert old == truth
    assert zero_cases > 1000
    # The one corner where RFC 1141 still gives +0: HC = 0x0000, m = 0x0000, m' = 0xFFFF.
    h = bytes.fromhex("0000ffff0000")  # other words sum to 0xFFFF, field = ~0xFFFF = 0
    assert full_checksum(h, 4) == 0x0000
    g = bytes.fromhex("ffffffff0000")  # word 0 changed from 0x0000 to 0xFFFF
    assert full_checksum(g, 4) == 0x0000
    assert update_rfc1141(0x0000, 0x0000, 0xFFFF) == 0x0000 == update_rfc1624(0x0000, 0x0000, 0xFFFF)


def test_eqn4_never_returns_minus_zero_on_a_consistent_header() -> None:
    # Eqn. 4 gives 0xFFFF only for HC = 0xFFFF, m = 0xFFFF and m' = 0x0000, and no
    # header with the word m = 0xFFFF can have the checksum 0xFFFF.
    grid = list(range(0, 0x10000, 251)) + [0, 1, 0xFFFE, 0xFFFF]
    for hc in grid:
        for m in grid:
            for m2 in (0, 1, 0x7FFF, 0xFFFE, 0xFFFF):
                if update_rfc1624_eqn4(hc, m, m2) == 0xFFFF:
                    assert (hc, m, m2) == (0xFFFF, 0xFFFF, 0)


def test_exhaustive_small_model() -> None:
    # A two-word "header": word 0 is the field m, word 1 the checksum. Over all
    # m in a grid and all m', Eqn. 3 equals the recompute whenever the new data
    # word is not 0x0000 (a header with all words zero cannot occur in IPv4).
    grid = list(range(0, 0x10000, 97)) + [0, 1, 0xFFFE, 0xFFFF]
    for m in grid:
        hc = full_checksum(m.to_bytes(2, "big") + b"\x00\x00", 2)
        for m2 in grid:
            truth = full_checksum(m2.to_bytes(2, "big") + b"\x00\x00", 2)
            got = update_rfc1624(hc, m, m2)
            if m2 != 0:
                assert got == truth
            else:
                assert truth == 0xFFFF and got == 0x0000
