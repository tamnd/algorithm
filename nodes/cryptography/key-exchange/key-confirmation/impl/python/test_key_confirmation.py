# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-confirmation/. The authors are listed in prov/YSM480.jsonl.

import hashlib
import random

from key_confirmation import (
    G,
    P,
    Q,
    check_tag,
    client_hello,
    hkdf_expand,
    hkdf_expand_label,
    hkdf_extract,
    keys_and_finished,
    mac_tag,
    schnorr_verify,
    server_hello,
    split_dkm,
    tls13_finished,
)

# RFC 8448, Section 3 (simple 1-RTT handshake): the handshake messages up to CertificateVerify.
CLIENT_HELLO = (
    "010000c00303cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283024dece7000006130113"
    "031302010000910000000b0009000006736572766572ff01000100000a00140012001d001700180019010001"
    "0101020103010400230000003300260024001d002099381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae"
    "4d5413691e529aaf2c002b0003020304000d0020001e04030503060302030804080508060401050106010201"
    "0402050206020202002d00020101001c00024001"
)
SERVER_HELLO = (
    "020000560303a6af06a4121860dc5e6e60249cd34c95930c8ac5cb1434dac155772ed3e2692800130100002e"
    "00330024001d0020c9828876112095fe66762bdbf7c672e156d6cc253b833df1dd69b1b04e751f0f002b0002"
    "0304"
)
ENCRYPTED_EXTENSIONS = "080000240022000a00140012001d00170018001901000101010201030104001c0002400100000000"
CERTIFICATE = (
    "0b0001b9000001b50001b0308201ac30820115a003020102020102300d06092a864886f70d01010b0500300e"
    "310c300a06035504031303727361301e170d3136303733303031323335395a170d3236303733303031323335"
    "395a300e310c300a0603550403130372736130819f300d06092a864886f70d010101050003818d0030818902"
    "818100b4bb498f8279303d980836399b36c6988c0c68de55e1bdb826d3901a2461eafd2de49a91d015abbc9a"
    "95137ace6c1af19eaa6af98c7ced43120998e187a80ee0ccb0524b1b018c3e0b63264d449a6d38e22a5fda43"
    "0846748030530ef0461c8ca9d9efbfae8ea6d1d03e2bd193eff0ab9a8002c47428a6d35a8d88d79f7f1e3f02"
    "03010001a31a301830090603551d1304023000300b0603551d0f0404030205a0300d06092a864886f70d0101"
    "0b05000381810085aad2a0e5b9276b908c65f73a7267170618a54c5f8a7b337d2df7a594365417f2eae8f8a5"
    "8c8f8172f9319cf36b7fd6c55b80f21a03015156726096fd335e5e67f2dbf102702e608ccae6bec1fc63a42a"
    "99be5c3eb7107c3c54e9b9eb2bd5203b1c3b84e0a8b2f759409ba3eac9d91d402dcc0cc8f8961229ac9187b4"
    "2b4de10000"
)
CERTIFICATE_VERIFY = (
    "0f000084080400805a747c5d88fa9bd2e55ab085a61015b7211f824cd484145ab3ff52f1fda8477b0b7abc90"
    "db78e2d33a5c141a078653fa6bef780c5ea248eeaaa785c4f394cab6d30bbe8d4859ee511f602957b15411ac"
    "027671459e46445c9ea58c181e818e95b8c3fb0bf3278409d3be152a3da5043e063dda65cdf5aea20d53dfac"
    "d42f74f3"
)
SERVER_HS_TRAFFIC = "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38"
FINISHED_KEY = "008d3b66f816ea559f96b537e885c31fc068bf492c652f01f288a1d8cdc19fc8"
SERVER_FINISHED = "9b9b141d906337fbd2cbdce71df4deda4ab42c309572cb7fffee5454b78f0718"


def rfc8448_transcript() -> bytes:
    parts = (CLIENT_HELLO, SERVER_HELLO, ENCRYPTED_EXTENSIONS, CERTIFICATE, CERTIFICATE_VERIFY)
    return b"".join(bytes.fromhex(p) for p in parts)


def test_rfc5869_case_1() -> None:
    prk = hkdf_extract(bytes(range(13)), b"\x0b" * 22)
    assert prk.hex() == "077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5"
    okm = hkdf_expand(prk, bytes(range(0xF0, 0xFA)), 42)
    assert okm.hex() == "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865"


def test_rfc8448_server_finished() -> None:
    base = bytes.fromhex(SERVER_HS_TRAFFIC)
    assert hkdf_expand_label(base, "finished", b"", 32).hex() == FINISHED_KEY
    th = hashlib.sha256(rfc8448_transcript()).digest()
    assert tls13_finished(base, th).hex() == SERVER_FINISHED


def test_changed_transcript_fails_confirmation() -> None:
    base = bytes.fromhex(SERVER_HS_TRAFFIC)
    good = bytes.fromhex(SERVER_FINISHED)
    t = bytearray(rfc8448_transcript())
    for pos in (5, 300, len(t) - 1):  # one bit flipped in ClientHello, Certificate, CertificateVerify
        bad = bytearray(t)
        bad[pos] ^= 1
        assert not check_tag(tls13_finished(base, hashlib.sha256(bytes(bad)).digest()), good)
    assert check_tag(tls13_finished(base, hashlib.sha256(bytes(t)).digest()), good)


def test_sp800_56a_tags() -> None:
    dkm = bytes(range(64))
    mac_key, key_data = split_dkm(dkm, 32)
    assert mac_key + key_data == dkm
    args = (b"alice", b"bob", b"X-bytes", b"Y-bytes")
    t1u = mac_tag(mac_key, b"KC_1_U", *args)
    t2u = mac_tag(mac_key, b"KC_2_U", *args)
    t2v = mac_tag(mac_key, b"KC_2_V", args[1], args[0], args[3], args[2])
    assert len(t1u) == 16 and len({t1u, t2u, t2v}) == 3  # domain separation by message_string
    # The recipient recomputes the tag; any change in an identity or ephemeral value fails.
    assert check_tag(mac_tag(mac_key, b"KC_2_U", *args), t2u)
    assert not check_tag(mac_tag(mac_key, b"KC_2_U", b"alice", b"eve", b"X-bytes", b"Y-bytes"), t2u)
    assert not check_tag(mac_tag(bytes(32), b"KC_2_U", *args), t2u)
    for bad_bits in (32, 63, 260):
        try:
            mac_tag(mac_key, b"KC_1_U", *args, tag_bits=bad_bits)
            raise AssertionError("short tag accepted")
        except ValueError:
            pass


def handshake(rng: random.Random, tamper: bool):
    """Client offers [strong, weak]; an attacker on the wire may strip 'strong'."""
    server_sk = rng.randrange(1, Q)
    server_pk = pow(G, server_sk, P)
    x, y = rng.randrange(1, Q), rng.randrange(1, Q)
    ch_client = client_hello(rng.randbytes(16), ["strong", "weak"], x)
    ch_server = dict(ch_client, suites=["weak"]) if tamper else ch_client
    sh = server_hello(ch_server, y, server_sk)
    assert schnorr_verify(server_pk, ch_client["nonce"] + sh["Y"].to_bytes(32, "big"), sh["sig"])
    k_c, sf_c, cf_c = keys_and_finished(pow(sh["Y"], x, P), ch_client, sh)
    k_s, sf_s, cf_s = keys_and_finished(pow(ch_server["X"], y, P), ch_server, sh)
    return sh["suite"], check_tag(sf_c, sf_s), check_tag(cf_s, cf_c), k_c == k_s


def test_downgrade_is_caught_by_finished_only() -> None:
    rng = random.Random(7)
    suite, server_ok, client_ok, same = handshake(rng, tamper=False)
    assert (suite, server_ok, client_ok, same) == ("strong", True, True, True)
    suite, server_ok, client_ok, same = handshake(rng, tamper=True)
    # The signature verified and Z is the same on both sides, but the views of the transcript differ.
    assert suite == "weak" and not server_ok and not client_ok and not same


def test_confirmation_without_authentication_passes_a_mitm() -> None:
    """HAC Definition 12.7: the peer is 'possibly unidentified'. Each leg confirms with Mallory."""
    rng = random.Random(8)
    x, y, m1, m2 = (rng.randrange(1, Q) for _ in range(4))
    ch_a = client_hello(b"n" * 16, ["strong"], x)
    sh_m = server_hello(ch_a, m1, None)  # Mallory answers Alice
    ch_m = client_hello(b"n" * 16, ["strong"], m2)  # Mallory calls Bob
    sh_b = server_hello(ch_m, y, None)
    alice = keys_and_finished(pow(sh_m["Y"], x, P), ch_a, sh_m)
    mallory_a = keys_and_finished(pow(ch_a["X"], m1, P), ch_a, sh_m)
    bob = keys_and_finished(pow(ch_m["X"], y, P), ch_m, sh_b)
    mallory_b = keys_and_finished(pow(sh_b["Y"], m2, P), ch_m, sh_b)
    assert alice == mallory_a and bob == mallory_b and alice[0] != bob[0]
