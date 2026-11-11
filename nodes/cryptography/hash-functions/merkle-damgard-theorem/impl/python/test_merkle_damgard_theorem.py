# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-damgard-theorem/. The authors are listed in prov/0WC6B8.jsonl.

from merkle_damgard_theorem import (
    birthday_md_collision,
    extract_collision,
    make_f,
    md,
    pad_no_length,
    pad_strengthened,
    plant_fixed_point,
    toy_decrypt,
    toy_encrypt,
)


def test_toy_cipher_inverts() -> None:
    for k in (0, 1, 0xBEEF, 0xFFFF):
        for x in range(0, 1 << 16, 997):
            assert toy_decrypt(k, toy_encrypt(k, x)) == x


def test_padding_without_length_breaks_md() -> None:
    f = make_f(16)
    fixed_block = 0x1234
    iv = plant_fixed_point(fixed_block)
    assert f(iv, fixed_block) == iv  # a fixed point at the IV, which is not a collision of f
    for msg in (b"", b"a", b"hello world"):
        longer = fixed_block.to_bytes(2, "big") + msg
        # Without the length, the extra first block is invisible: a collision of the hash.
        assert md(f, iv, pad_no_length(longer))[-1] == md(f, iv, pad_no_length(msg))[-1]
        # With MD strengthening, the last blocks differ, so the same trick fails.
        assert md(f, iv, pad_strengthened(longer))[-1] != md(f, iv, pad_strengthened(msg))[-1]


def test_padding_without_length_is_injective() -> None:
    # The failure is not a loss of information: the padding alone is injective.
    seen = {}
    for n in range(4):
        for v in range(0, 256 ** n, max(1, 256 ** n // 300)):
            msg = v.to_bytes(n, "big")
            key = tuple(pad_no_length(msg))
            assert seen.setdefault(key, msg) == msg


def test_reduction_finds_compression_collision() -> None:
    # A weak f with 10-bit output, so a hash collision appears after about 2^5 messages.
    f = make_f(10)
    iv = 0x0155
    found = 0
    for start in range(5):
        pair = birthday_md_collision(f, iv ^ start)
        assert pair is not None
        m1, m2 = pair
        (h, m), (h2, m2b) = extract_collision(f, iv ^ start, m1, m2)
        assert (h, m) != (h2, m2b)
        assert f(h, m) == f(h2, m2b)
        found += 1
    assert found == 5


def test_reduction_with_different_lengths() -> None:
    # Build messages of different lengths with equal hash by search, then extract.
    f = make_f(8)
    iv = 0x21
    table: dict[int, bytes] = {}
    pair = None
    for t in range(1 << 12):
        msg = t.to_bytes(2 + t % 3, "big")
        d = md(f, iv, pad_strengthened(msg))[-1]
        if d in table and len(table[d]) != len(msg):
            pair = (table[d], msg)
            break
        table.setdefault(d, msg)
    assert pair is not None
    x, y = extract_collision(f, iv, *pair)
    assert x != y and f(*x) == f(*y)
    # With different lengths, the collision is found at the last (length) block.
    assert x[1] != y[1]
