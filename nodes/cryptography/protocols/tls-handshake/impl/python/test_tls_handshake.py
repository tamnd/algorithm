# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tls-handshake/. The authors are listed in prov/VZ8M1C.jsonl.
#
# Official vectors, copied by hand:
# * RFC 8448 (January 2019), Section 3 "Simple 1-RTT Handshake": the X25519
#   keys, the key schedule, the traffic keys, the client Finished and the
#   resumption secret. RFC 8448 does not print the transcript hash for the
#   server Finished, so the server verify_data is not tested.
# * RFC 7748, Section 5.2 (X25519), RFC 5869, Appendix A.1 (HKDF-SHA256),
#   RFC 8032, Section 7.1, TEST 1 (Ed25519).
# The simulated handshake has no official vectors: its message bodies are
# not the TLS wire format.

import pytest

from tls_handshake import (
    BASE_U,
    EMPTY_HASH,
    FINISHED,
    Client,
    HandshakeError,
    Server,
    connect,
    derive_secret,
    early_secret,
    ed25519_public,
    ed25519_sign,
    ed25519_verify,
    expand_label,
    finished_key,
    handshake,
    handshake_secret,
    hkdf_expand,
    hkdf_extract,
    hkdf_label,
    master_secret,
    message_hash,
    protect,
    resumption_psk,
    traffic_keys,
    transcript_hash,
    verify_data,
    x25519,
)

h = bytes.fromhex

# RFC 8448 Section 3
C_PRIV = h("49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005")
C_PUB = h("99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c")
S_PRIV = h("b1580eeadf6dd589b8ef4f2d5652578cc810e9980191ec8d058308cea216a21e")
S_PUB = h("c9828876112095fe66762bdbf7c672e156d6cc253b833df1dd69b1b04e751f0f")
SHARED = h("8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d")
CLIENT_HELLO = h(
    "010000c00303cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283024dece7000006130113031302010000910000000b0009000006736572766572ff01000100000a00140012001d0017001800190100010101020103010400230000003300260024001d002099381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c002b0003020304000d0020001e040305030603020308040805080604010501060102010402050206020202002d00020101001c00024001"
)
SERVER_HELLO = h(
    "020000560303a6af06a4121860dc5e6e60249cd34c95930c8ac5cb1434dac155772ed3e2692800130100002e00330024001d0020c9828876112095fe66762bdbf7c672e156d6cc253b833df1dd69b1b04e751f0f002b00020304"
)
EARLY = h("33ad0a1c607ec03b09e6cd9893680ce210adf300aa1f2660e1b22e10f170f92a")
DERIVED1 = h("6f2615a108c702c5678f54fc9dbab69716c076189c48250cebeac3576c3611ba")
HS = h("1dc826e93606aa6fdc0aadc12f741b01046aa6b99f691ed221a9f0ca043fbeac")
TH_CH_SH = h("860c06edc07858ee8e78f0e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8")
C_HS = h("b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21")
S_HS = h("b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38")
DERIVED2 = h("43de77e0c77713859a944db9db2590b53190a65b3ee2e4f12dd7a0bb7ce254b4")
MS = h("18df06843d13a08bf2a449844c5f8a478001bc4d4c627984d5a41da8d0402919")
TH_SF = h("9608102a0f1ccc6db6250b7b7e417b1a000eaada3daae4777a7686c9ff83df13")
C_AP = h("9e40646ce79a7f9dc05af8889bce6552875afa0b06df0087f792ebb7c17504a5")
S_AP = h("a11af9f05531f856ad47116b45a950328204b4f44bfb6b3a4b4f1f3fcb631643")
EXP = h("fe22f881176eda18eb8f44529e6792c50c9a3f89452f68d8ae311b4309d3cf50")
TH_CF = h("209145a96ee8e2a122ff810047cc952684658d6049e86429426db87c54ad143d")
RMS = h("7df235f2031d2a051287d02b0241b0bfdaf86cc856231f2d5aba46c434ec196c")
PSK = h("4ecd0eb6ec3b4d87f5d6028f922ca4c5851a277fd41311c9e62d2c9492e1c4f3")


def test_rfc7748_x25519():
    k = h("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = h("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    assert x25519(k, u) == h("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")
    k = h("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d")
    u = h("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493")
    assert x25519(k, u) == h("95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957")


def test_rfc5869_a1():
    prk = hkdf_extract(h("000102030405060708090a0b0c"), bytes([0x0B]) * 22)
    assert prk == h("077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5")
    okm = hkdf_expand(prk, h("f0f1f2f3f4f5f6f7f8f9"), 42)
    assert okm == h("3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865")


def test_rfc8032_test1():
    sk = h("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
    pk = h("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    sig = h("e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
    assert ed25519_public(sk) == pk
    assert ed25519_sign(sk, b"") == sig
    assert ed25519_verify(pk, b"", sig)
    assert not ed25519_verify(pk, b"x", sig)


def test_rfc8448_key_exchange():
    assert x25519(C_PRIV, BASE_U) == C_PUB
    assert x25519(S_PRIV, BASE_U) == S_PUB
    assert x25519(C_PRIV, S_PUB) == SHARED == x25519(S_PRIV, C_PUB)
    assert CLIENT_HELLO[:4] == h("010000c0") and len(CLIENT_HELLO) == 196
    assert C_PUB in CLIENT_HELLO and S_PUB in SERVER_HELLO


def test_rfc8448_hkdf_labels():
    assert hkdf_label(b"key", b"", 16) == h("001009746c733133206b657900")
    assert hkdf_label(b"iv", b"", 12) == h("000c08746c73313320697600")
    assert hkdf_label(b"finished", b"", 32) == h("00200e746c7331332066696e697368656400")


def test_rfc8448_handshake_secrets():
    assert EMPTY_HASH == h("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    es = early_secret(None)
    assert es == EARLY
    assert derive_secret(es, b"derived", EMPTY_HASH) == DERIVED1
    hs = handshake_secret(es, SHARED)
    assert hs == HS
    th = transcript_hash(CLIENT_HELLO, SERVER_HELLO)
    assert th == TH_CH_SH
    assert derive_secret(hs, b"c hs traffic", th) == C_HS
    assert derive_secret(hs, b"s hs traffic", th) == S_HS
    assert derive_secret(hs, b"derived", EMPTY_HASH) == DERIVED2
    assert master_secret(hs) == MS
    assert traffic_keys(S_HS) == (h("3fce516009c21727d0f2e4e86ee403bc"), h("5d313eb2671276ee13000b30"))
    assert traffic_keys(C_HS) == (h("dbfaa693d1762c5b666af5d950258d01"), h("5bd3c71b836e0b76bb73265f"))
    assert finished_key(S_HS) == h("008d3b66f816ea559f96b537e885c31fc068bf492c652f01f288a1d8cdc19fc8")


def test_rfc8448_application_and_resumption():
    # The transcript hashes below are copied from RFC 8448; the messages that
    # they cover are encrypted in the trace and are not rebuilt here.
    assert derive_secret(MS, b"c ap traffic", TH_SF) == C_AP
    assert derive_secret(MS, b"s ap traffic", TH_SF) == S_AP
    assert derive_secret(MS, b"exp master", TH_SF) == EXP
    assert traffic_keys(S_AP) == (h("9f02283b6c9c07efc26bb9f2ac92e356"), h("cf782b88dd83549aadf1e984"))
    assert traffic_keys(C_AP) == (h("17422dda596ed5d9acd890e3c63f5051"), h("5b78923dee08579033e523d9"))
    assert finished_key(C_HS) == h("b80ad01015fb2f0bd65ff7d4da5d6bf83f84821d1f87fdc7d3c75b5a7b42d9c4")
    vd = h("a8ec436d677634ae525ac1fcebe11a039ec17694fac6e98527b642f2edd5ce61")
    assert verify_data(C_HS, TH_SF) == vd
    assert handshake(FINISHED, vd) == h("14000020") + vd
    assert derive_secret(MS, b"res master", TH_CF) == RMS
    assert resumption_psk(RMS, h("0000")) == PSK
    assert expand_label(RMS, b"resumption", h("0000"), 32) == PSK


def test_hello_retry_message_hash_format():
    ch1 = CLIENT_HELLO
    mh = message_hash(ch1)
    assert mh[:4] == bytes([254, 0, 0, 32]) and mh[4:] == transcript_hash(ch1)


def make_pair(single_use: bool = True):
    server = Server("example.com", bytes(range(32)), single_use_tickets=single_use)
    client = Client({"example.com": server.public})
    return client, server


def test_full_handshake_agrees():
    client, server = make_pair()
    cst, sst, ticket = connect(client, server, "example.com")
    assert cst["c_ap"] == sst["c_ap"] and cst["s_ap"] == sst["s_ap"] and cst["ms"] == sst["ms"]
    assert cst["transcript"] == sst["transcript"]
    assert [m[0] for m in cst["transcript"]] == [1, 2, 8, 11, 15, 20, 20]
    assert ticket.psk in server.tickets.values()


def test_fresh_keys_each_handshake():
    client, server = make_pair()
    a = connect(client, server, "example.com")[0]["c_ap"]
    b = connect(client, server, "example.com")[0]["c_ap"]
    assert a != b


def test_impostor_without_the_signing_key_fails():
    client, server = make_pair()
    fake = Server("example.com", bytes([7]) * 32)
    fake.public = server.public  # the impostor shows the real key but signs with its own
    ch, _ = client.hello()
    sh, *records = fake.respond(ch)
    with pytest.raises(HandshakeError, match="CertificateVerify"):
        client.handle("example.com", sh, records)


def test_unknown_key_or_wrong_name_fails():
    client, server = make_pair()
    ch, _ = client.hello()
    sh, *records = Server("example.com", bytes([9]) * 32).respond(ch)
    with pytest.raises(HandshakeError, match="bad_certificate"):
        client.handle("example.com", sh, records)
    ch, _ = client.hello()
    sh, *records = server.respond(ch)
    with pytest.raises(HandshakeError, match="bad_certificate"):
        client.handle("other.example", sh, records)


def test_key_share_substitution_fails():
    # A network attacker replaces the server's key share with its own.
    client, server = make_pair()
    ch, _ = client.hello()
    sh, *records = server.respond(ch)
    evil = sh[:36] + x25519(bytes([5]) * 32, BASE_U) + sh[68:]
    with pytest.raises(HandshakeError):
        client.handle("example.com", evil, records)


def test_wrong_client_finished_is_rejected():
    client, server = make_pair()
    ch, _ = client.hello()
    sh, *records = server.respond(ch)
    client.handle("example.com", sh, records)
    forged = protect(client.state["c_hs"], 0, handshake(FINISHED, bytes(32)))
    with pytest.raises(HandshakeError, match="client Finished"):
        server.finish(sh[4:36], forged)


def test_psk_resumption():
    client, server = make_pair()
    ticket = connect(client, server, "example.com")[2]
    cst, sst, _ = connect(client, server, "example.com", ticket=ticket)
    assert cst["c_ap"] == sst["c_ap"]
    assert [m[0] for m in cst["transcript"]] == [1, 2, 8, 20, 20]  # no Certificate, no CertificateVerify


def test_bad_binder_is_rejected():
    client, server = make_pair()
    ticket = connect(client, server, "example.com")[2]
    ch, _ = client.hello(ticket)
    bad = ch[:-1] + bytes([ch[-1] ^ 1])
    with pytest.raises(HandshakeError, match="binder"):
        server.respond(bad)


def test_zero_rtt_is_delivered():
    client, server = make_pair()
    ticket = connect(client, server, "example.com")[2]
    cst, _, _ = connect(client, server, "example.com", ticket=ticket, early=b"GET /")
    assert server.early_data_log == [b"GET /"] and cst["early_accepted"]


def test_zero_rtt_replay_without_and_with_single_use_tickets():
    for single_use, expect in ((False, 2), (True, 1)):
        client, server = make_pair(single_use)
        ticket = connect(client, server, "example.com")[2]
        ch, early = client.hello(ticket, b"pay 10")
        server.respond(ch, early)
        server.respond(ch, early)  # an attacker sends a copy of the first flight
        assert server.early_data_log == [b"pay 10"] * expect
