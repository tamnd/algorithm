# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-damgard-construction/. The authors are listed in prov/FVJZV5.jsonl.

from itertools import product

from merkle_damgard_construction import joux_multicollision, md_continue, md_hash, md_pad, toy_f

IV = 0x2468


def H(msg: bytes) -> int:
    return md_hash(toy_f, IV, msg, 2, 2)


def test_padding_shape() -> None:
    for n in range(0, 40):
        p = md_pad(n, 64, 8)
        assert (n + len(p)) % 64 == 0
        assert p[0] == 0x80 and int.from_bytes(p[-8:], "big") == 8 * n
    # MD5 and SHA-256 pad to 64 bytes with an 8-byte length: 55 bytes fit in one block, 56 do not.
    assert 55 + len(md_pad(55, 64, 8)) == 64
    assert 56 + len(md_pad(56, 64, 8)) == 128


def test_iteration_is_blockwise() -> None:
    msg = b"abcdef"
    data = msg + md_pad(len(msg), 2, 2)
    h = IV
    for i in range(0, len(data), 2):
        h = toy_f(h, data[i:i + 2])
    assert h == H(msg)


def test_length_extension() -> None:
    secret = b"secret key"
    known = b"&amount=10"
    tag = H(secret + known)  # what the attacker sees
    glue = md_pad(len(secret + known), 2, 2)
    suffix = b"&amount=9999"
    # The attacker knows only the tag and the length of secret + known.
    forged = md_continue(toy_f, tag, len(secret + known) + len(glue), suffix, 2, 2)
    assert forged == H(secret + known + glue + suffix)


def test_joux_multicollision() -> None:
    k = 4
    pairs, h = joux_multicollision(toy_f, IV, k, 2)
    msgs = [b"".join(choice) for choice in product(*pairs)]
    assert len(set(msgs)) == 2 ** k
    digests = {H(m) for m in msgs}
    # All 16 messages have the same length and the same chain, so the same hash.
    assert len(digests) == 1


def test_strengthening_separates_lengths() -> None:
    assert H(b"") != H(b"\x00")
    assert H(b"ab") != H(b"ab\x80\x00")
