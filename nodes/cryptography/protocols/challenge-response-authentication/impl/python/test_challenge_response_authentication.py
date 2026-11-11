# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/challenge-response-authentication/. The authors are listed in prov/53493G.jsonl.
#
# Official vectors, copied by hand:
#   RFC 4226, Appendix D, Tables 1 and 2 (HOTP, secret "12345678901234567890").
#   RFC 6238, Appendix B, Table 1 (TOTP, 8 digits, step 30, T0 = 0). The
#   SHA-256 and SHA-512 rows use the 32-byte and 64-byte seeds of the
#   reference code in RFC 6238 Appendix A, not the 20-byte seed that the text
#   of Appendix B names.

import hashlib
import hmac

from challenge_response_authentication import (
    FixedParty,
    HotpVerifier,
    NaiveParty,
    TimestampVerifier,
    TotpVerifier,
    dynamic_truncation,
    hotp,
    reflection_attack,
    timestamp_token,
    totp,
)

SECRET = b"12345678901234567890"
SEED32 = bytes.fromhex("3132333435363738393031323334353637383930" "313233343536373839303132")
SEED64 = bytes.fromhex(
    "3132333435363738393031323334353637383930"
    "3132333435363738393031323334353637383930"
    "3132333435363738393031323334353637383930"
    "31323334"
)

# RFC 4226, Appendix D, Table 1: HMAC-SHA-1(secret, count)
HMAC_TABLE = [
    "cc93cf18508d94934c64b65d8ba7667fb7cde4b0",
    "75a48a19d4cbe100644e8ac1397eea747a2d33ab",
    "0bacb7fa082fef30782211938bc1c5e70416ff44",
    "66c28227d03a2d5529262ff016a1e6ef76557ece",
    "a904c900a64b35909874b33e61c5938a8e15ed1c",
    "a37e783d7b7233c083d4f62926c7a25f238d0316",
    "bc9cd28561042c83f219324d3c607256c03272ae",
    "a4fb960c0bc06e1eabb804e5b397cdc4b45596fa",
    "1b3c89f65e6c9e883012052823443f048b4332db",
    "1637409809a679dc698207310c8c7fc07290d9e5",
]
# RFC 4226, Appendix D, Table 2: truncated value (decimal) and HOTP
TRUNC_TABLE = [
    (1284755224, "755224"),
    (1094287082, "287082"),
    (137359152, "359152"),
    (1726969429, "969429"),
    (1640338314, "338314"),
    (868254676, "254676"),
    (1918287922, "287922"),
    (82162583, "162583"),
    (673399871, "399871"),
    (645520489, "520489"),
]

# RFC 6238, Appendix B, Table 1: time, SHA1, SHA256, SHA512
TOTP_TABLE = [
    (59, "94287082", "46119246", "90693936"),
    (1111111109, "07081804", "68084774", "25091201"),
    (1111111111, "14050471", "67062674", "99943326"),
    (1234567890, "89005924", "91819424", "93441116"),
    (2000000000, "69279037", "90698825", "38618901"),
    (20000000000, "65353130", "77737706", "47863826"),
]


def test_hotp_rfc4226_appendix_d():
    for count in range(10):
        m = hmac.new(SECRET, count.to_bytes(8, "big"), hashlib.sha1).digest()
        assert m.hex() == HMAC_TABLE[count]
        assert dynamic_truncation(m) == TRUNC_TABLE[count][0]
        assert hotp(SECRET, count) == TRUNC_TABLE[count][1]


def test_totp_rfc6238_appendix_b():
    for t, v1, v256, v512 in TOTP_TABLE:
        assert totp(SECRET, t) == v1
        assert totp(SEED32, t, digest="sha256") == v256
        assert totp(SEED64, t, digest="sha512") == v512


def test_totp_step_boundaries():
    # 59 and 1111111109 are the last seconds of their steps; one second later the code changes.
    assert totp(SECRET, 59) == totp(SECRET, 30)
    assert totp(SECRET, 60) != totp(SECRET, 59)
    assert totp(SECRET, 1111111109) != totp(SECRET, 1111111111)


def test_hotp_verifier_window_and_no_reuse():
    server = HotpVerifier(SECRET, window=3)
    assert server.check("755224")  # counter 0
    assert not server.check("755224")  # a replay fails
    assert server.check("969429")  # counter 3: the token was pressed twice without login
    assert not server.check("520489")  # counter 9 is past the window
    assert server.check(TRUNC_TABLE[4][1])


def test_totp_verifier_accepts_once():
    server = TotpVerifier(SECRET)
    code = totp(SECRET, 1111111109)
    assert server.check(code, 1111111109)
    assert not server.check(code, 1111111110)  # same step again: rejected
    server2 = TotpVerifier(SECRET)
    assert server2.check(code, 1111111109 + 30)  # one step of clock delay is allowed
    assert not TotpVerifier(SECRET).check(code, 1111111109 + 90)


def test_honest_runs():
    k = b"k" * 32
    a, b = NaiveParty(b"A", k), NaiveParty(b"B", k)
    c = a.start()
    assert a.finish(b.respond(c))
    fa, fb = FixedParty(b"A", k, b"B"), FixedParty(b"B", k, b"A")
    c = fa.start()
    assert fa.finish(fb.respond(c))
    c = fb.start()
    assert fb.finish(fa.respond(c))


def test_reflection_attack_on_naive_protocol():
    victim = NaiveParty(b"B", b"k" * 32)
    for _ in range(20):
        assert reflection_attack(victim)


def test_reflection_attack_fails_with_identity_in_mac():
    victim = FixedParty(b"B", b"k" * 32, b"A")
    for _ in range(20):
        assert not reflection_attack(victim)


def test_wrong_key_fails():
    a = FixedParty(b"A", b"k" * 32, b"B")
    eve = FixedParty(b"B", b"e" * 32, b"A")
    c = a.start()
    assert not a.finish(eve.respond(c))


def test_timestamp_variant():
    k = b"t" * 32
    bob = TimestampVerifier(k, b"B", window=120)
    tok = timestamp_token(k, b"A", b"B", 1000)
    assert bob.check(b"A", tok, 1010)
    assert not bob.check(b"A", tok, 1020)  # a replay inside the window
    assert not bob.check(b"A", timestamp_token(k, b"A", b"B", 800), 1010)  # too old
    assert not bob.check(b"A", timestamp_token(k, b"A", b"C", 1005), 1010)  # made for another receiver
    # Reflection: B's own token toward A does not pass at B.
    assert not bob.check(b"A", timestamp_token(k, b"B", b"A", 1006), 1010)
