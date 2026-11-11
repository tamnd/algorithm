# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/md5/. The authors are listed in prov/E0VM6D.jsonl.

import hashlib

from md5 import IV, T, compress, md5, pad

# RFC 1321 (April 1992), Appendix A.5, "Test suite", copied by hand.
RFC1321_A5 = [
    (b"", "d41d8cd98f00b204e9800998ecf8427e"),
    (b"a", "0cc175b9c0f1b6a831c399e269772661"),
    (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
    (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
    (b"abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "d174ab98d277d9f5a5611c2c9f419d9f"),
    (b"1234567890" * 8, "57edf4a22be3c955ac49da2e2107b67a"),
]

# The Wang-Yu collision pair as published by Peter Selinger, "MD5 Collision Demo",
# https://www.mscs.dal.ca/~selinger/md5collision/ (2006). Two blocks each, 128 bytes.
COLL1 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5b"
    "d8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
)
COLL2 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5b"
    "d8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
)
COLL_MD5 = "79054025255fb1a26e4bc422aef54eb4"


def test_rfc1321_appendix_a5() -> None:
    for msg, want in RFC1321_A5:
        assert md5(msg).hex() == want, msg


def test_sine_table() -> None:
    # RFC 1321, Appendix A.3: the constants of step 1 and step 64.
    assert T[0] == 0xD76AA478
    assert T[63] == 0xEB86D391


def test_collision_pair() -> None:
    assert COLL1 != COLL2
    assert md5(COLL1).hex() == COLL_MD5
    assert md5(COLL2).hex() == COLL_MD5
    # Second check with the library.
    assert hashlib.md5(COLL1).hexdigest() == COLL_MD5
    assert hashlib.md5(COLL2).hexdigest() == COLL_MD5


def test_collision_is_internal() -> None:
    # The chaining values after the two blocks are equal, so any common suffix keeps the collision.
    s1 = compress(compress(IV, COLL1[:64]), COLL1[64:])
    s2 = compress(compress(IV, COLL2[:64]), COLL2[64:])
    assert s1 == s2
    assert compress(IV, COLL1[:64]) != compress(IV, COLL2[:64])
    suffix = b"any common suffix"
    assert md5(COLL1 + suffix) == md5(COLL2 + suffix)


def test_padding_lengths() -> None:
    for n in range(0, 130):
        p = pad(b"y" * n)
        assert len(p) % 64 == 0 and p[n] == 0x80
        assert int.from_bytes(p[-8:], "little") == 8 * n


def test_against_hashlib() -> None:
    for n in range(0, 200, 7):
        msg = bytes(range(n % 256)) * 1 + b"z" * n
        assert md5(msg) == hashlib.md5(msg).digest()
