# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/md4/. The authors are listed in prov/HK9M2T.jsonl.

from md4 import IV, compress, md4, pad

# RFC 1320 (April 1992), Appendix A.5, "Test suite", copied by hand.
RFC1320_A5 = [
    (b"", "31d6cfe0d16ae931b73c59d7e0c089c0"),
    (b"a", "bde52cb31de33e46245e05fbdbd6fb24"),
    (b"abc", "a448017aaf21d8525fc10ae87aa6729d"),
    (b"message digest", "d9130a8164549fe818874806e1c7014b"),
    (b"abcdefghijklmnopqrstuvwxyz", "d79e1c308aa5bbcdeea8ed63df412da9"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "043f8582f241db351ce627e153e7f0e4"),
    (b"1234567890" * 8, "e33b4ddc9c38f2199c3e7b164fcc0536"),
]


def test_rfc1320_appendix_a5() -> None:
    for msg, want in RFC1320_A5:
        assert md4(msg).hex() == want, msg


def test_padding_lengths() -> None:
    # 55 bytes fit in one block; 56 bytes need a second block for the length.
    for n in range(0, 130):
        p = pad(b"x" * n)
        assert len(p) % 64 == 0
        assert p[n] == 0x80
        assert int.from_bytes(p[-8:], "little") == 8 * n
    assert len(pad(b"x" * 55)) == 64
    assert len(pad(b"x" * 56)) == 128


def test_iteration_matches_blocks() -> None:
    # The hash is the compression function iterated over the padded blocks.
    msg = b"The quick brown fox jumps over the lazy dog" * 3
    data = pad(msg)
    state = IV
    for i in range(0, len(data), 64):
        state = compress(state, data[i:i + 64])
    assert b"".join(w.to_bytes(4, "little") for w in state) == md4(msg)


def test_avalanche_one_bit() -> None:
    a = md4(b"abc")
    b = md4(b"abb")
    diff = bin(int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).count("1")
    assert 30 < diff < 100
