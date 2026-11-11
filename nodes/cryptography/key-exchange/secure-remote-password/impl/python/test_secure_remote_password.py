# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-remote-password/. The authors are listed in prov/KNRW9R.jsonl.

import random

import pytest

from secure_remote_password import (
    G_1024,
    N_1024,
    SRPError,
    client_premaster,
    client_public,
    multiplier,
    private_key,
    run,
    scrambler,
    server_premaster,
    server_public,
    verifier,
)


def hx(s: str) -> int:
    return int("".join(s.split()), 16)


# RFC 5054, Appendix B, "SRP Test Vectors", copied by hand.
I = b"alice"
P = b"password123"
S_SALT = bytes.fromhex("BEB25379D1A8581EB5A727673A2441EE")
K_EXP = hx("7556AA04 5AEF2CDD 07ABAF0F 665C3E81 8913186F")
X_EXP = hx("94B7555A ABE9127C C58CCF49 93DB6CF8 4D16C124")
V_EXP = hx("""
7E273DE8 696FFC4F 4E337D05 B4B375BE B0DDE156 9E8FA00A 9886D812
9BADA1F1 822223CA 1A605B53 0E379BA4 729FDC59 F105B478 7E5186F5
C671085A 1447B52A 48CF1970 B4FB6F84 00BBF4CE BFBB1681 52E08AB5
EA53D15C 1AFF87B2 B9DA6E04 E058AD51 CC72BFC9 033B564E 26480D78
E955A5E2 9E7AB245 DB2BE315 E2099AFB""")
A_PRIV = hx("""
60975527 035CF2AD 1989806F 0407210B C81EDC04 E2762A56 AFD529DD
DA2D4393""")
B_PRIV = hx("""
E487CB59 D31AC550 471E81F0 0F6928E0 1DDA08E9 74A004F4 9E61F5D1
05284D20""")
A_EXP = hx("""
61D5E490 F6F1B795 47B0704C 436F523D D0E560F0 C64115BB 72557EC4
4352E890 3211C046 92272D8B 2D1A5358 A2CF1B6E 0BFCF99F 921530EC
8E393561 79EAE45E 42BA92AE ACED8251 71E1E8B9 AF6D9C03 E1327F44
BE087EF0 6530E69F 66615261 EEF54073 CA11CF58 58F0EDFD FE15EFEA
B349EF5D 76988A36 72FAC47B 0769447B""")
B_EXP = hx("""
BD0C6151 2C692C0C B6D041FA 01BB152D 4916A1E7 7AF46AE1 05393011
BAF38964 DC46A067 0DD125B9 5A981652 236F99D9 B681CBF8 7837EC99
6C6DA044 53728610 D0C6DDB5 8B318885 D7D82C7F 8DEB75CE 7BD4FBAA
37089E6F 9C6059F3 88838E7A 00030B33 1EB76840 910440B1 B27AAEAE
EB4012B7 D7665238 A8E3FB00 4B117B58""")
U_EXP = hx("CE38B959 3487DA98 554ED47D 70A7AE5F 462EF019")
PREMASTER_EXP = hx("""
B0DC82BA BCF30674 AE450C02 87745E79 90A3381F 63B387AA F271A10D
233861E3 59B48220 F7C4693C 9AE12B0A 6F67809F 0876E2D0 13800D6C
41BB59B6 D5979B5C 00A172B4 A2A5903A 0BDCAF8A 709585EB 2AFAFA8F
3499B200 210DCC1F 10EB3394 3CD67FC8 8A2F39A4 BE5BEC4E C0A3212D
C346D7E4 74B29EDE 8A469FFE CA686E5A""")


def _probably_prime(n: int, rounds: int = 16) -> bool:
    if n < 4:
        return n in (2, 3)
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = random.Random(1)
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        y = pow(a, d, n)
        if y in (1, n - 1):
            continue
        for _ in range(s - 1):
            y = y * y % n
            if y == n - 1:
                break
        else:
            return False
    return True


def test_group_is_safe_prime():
    assert N_1024.bit_length() == 1024
    assert _probably_prime(N_1024)
    assert _probably_prime((N_1024 - 1) // 2)


def test_rfc5054_k_x_v():
    assert multiplier() == K_EXP
    assert private_key(S_SALT, I, P) == X_EXP
    assert verifier(S_SALT, I, P) == V_EXP


def test_rfc5054_public_values_and_u():
    assert client_public(A_PRIV) == A_EXP
    assert server_public(B_PRIV, V_EXP) == B_EXP
    assert scrambler(A_EXP, B_EXP) == U_EXP


def test_rfc5054_premaster_both_sides():
    assert client_premaster(I, P, S_SALT, A_PRIV, B_EXP) == PREMASTER_EXP
    assert server_premaster(A_EXP, B_PRIV, V_EXP) == PREMASTER_EXP


def test_full_run_agrees():
    rng = random.Random(7)
    Kc, Ks = run(b"bob", b"correct horse", b"correct horse", rng=rng.getrandbits)
    assert Kc == Ks and len(Kc) == 20


def test_wrong_password_fails():
    rng = random.Random(8)
    with pytest.raises(SRPError):
        run(b"bob", b"wrong horse", b"correct horse", rng=rng.getrandbits)


@pytest.mark.parametrize("bad_A", [0, N_1024, 2 * N_1024])
def test_server_rejects_A_zero_mod_N(bad_A):
    # With A = 0 mod N, S = (A v^u)^b = 0 and a client with no password would know S.
    with pytest.raises(SRPError):
        server_premaster(bad_A, B_PRIV, V_EXP)


def test_client_rejects_B_zero_mod_N():
    with pytest.raises(SRPError):
        client_premaster(I, P, S_SALT, A_PRIV, N_1024)


def test_verifier_is_not_password_equivalent_but_allows_offline_guessing():
    # A stolen verifier lets the thief test guesses offline (one exponentiation each),
    # which is the reason SRP is augmented but not secure against precomputation of
    # a per-user salt that is sent in the clear.
    dictionary = [b"letmein", b"123456", b"password123", b"qwerty"]
    found = [w for w in dictionary if verifier(S_SALT, I, w) == V_EXP]
    assert found == [P]


def test_k_and_g_values():
    assert G_1024 == 2
    assert 0 < K_EXP < 2**160
