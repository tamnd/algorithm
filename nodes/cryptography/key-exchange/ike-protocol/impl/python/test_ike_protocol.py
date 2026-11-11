# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ike-protocol/. The authors are listed in prov/FRQGKN.jsonl.

import random

from ike_protocol import G, P, Initiator, Responder, b32, lp, prf_plus, sig_keypair, skeyseed, unlp


def test_nist_cavp_ikev2_vector() -> None:
    # NIST CAVP SP 800-135 KDF tests, ikev2.rsp, [SHA-256] [g^ir length = 1024] [DKM length = 1056], COUNT = 0
    ni, nr = bytes.fromhex("ed80dc79912c32a9"), bytes.fromhex("35fb6d1a3feac078")
    g_ir = bytes.fromhex(
        "42968e5d0ccc3cfc5a3e4bc1bba370cea1fae0d54c49ccba34b2bee804beeb2e9e8c57a4e01bd45102cf2433aacc6cfe"
        "c06792f363e5170e6aa6650274e906648e449d27a8f00b5b44261982c9835c748a751ec5138eaacc5e025661339538a6"
        "1bf418e454699e19c32db8d9ce5dd86b220f1e89afc5872e68be36cb1a0c8866"
    )
    spi_i, spi_r = bytes.fromhex("47c1858efc932ea4"), bytes.fromhex("606fd05609624002")
    seed = skeyseed(ni, nr, g_ir)
    assert seed.hex() == "37fde90b81d63692620f67367b62092e3efdc6a03509137d731004767ff35010"
    dkm = prf_plus(seed, ni + nr + spi_i + spi_r, 132)
    assert dkm.hex() == (
        "63d018a08f7a29daa7d1f92cb63f45fa39bbaf5e5f1a78139613bb891e3e6bf9d0448f7c74e05b4c1a25c0b61e62c875"
        "e852f287e192d4ae536112db5197216400bd5e123470efc15f53161865fe8b19a1416518a157d651ecd2caddab6a9eae"
        "6a27a55af088218d5156edaa9789f934d9836ed43edffda553822202ff9f7d4860ca72e0"
    )


def setup(seed: int):
    rng = random.Random(seed)
    (si, pi), (sr, pr) = sig_keypair(rng), sig_keypair(rng)
    directory = {b"alice@example.org": pi, b"gw.example.org": pr}
    ini = Initiator(b"alice@example.org", si, directory, rng)
    res = Responder(b"gw.example.org", sr, directory, rng)
    return ini, res


def run(ini, res, m1):
    m2 = res.respond(m1)
    m3 = ini.auth(m2)
    m4 = res.auth(unlp(m1)[1], m3)
    return m4 is not None and ini.finish(m4)


def test_honest_run() -> None:
    ini, res = setup(1)
    assert run(ini, res, ini.message1())
    assert ini.peer == b"gw.example.org" and res.peer == b"alice@example.org"
    assert ini.keymat == res.keymat and len(ini.keymat) == 64


def test_cookie_exchange() -> None:
    ini, res = setup(2)
    res.under_load = True
    reply = res.respond(ini.message1())
    tag, cookie = unlp(reply)
    assert tag == b"COOKIE" and res.sessions == {}  # no state for unproven addresses
    # A forged or stale cookie gets another cookie request, not a session.
    m1 = ini.msg1
    spi_i, ni = unlp(m1)[1], unlp(m1)[4]
    bad = lp(b"INIT", spi_i, unlp(m1)[2], unlp(m1)[3], ni, b"\x00" * 32)
    assert unlp(res.respond(bad))[0] == b"COOKIE"
    # The initiator repeats message 1 with the cookie (same SPIi and Ni).
    good = lp(b"INIT", spi_i, unlp(m1)[2], unlp(m1)[3], ni, cookie)
    ini.msg1 = good
    assert run(ini, res, good)
    assert ini.keymat == res.keymat


def test_man_in_the_middle_on_ke_is_caught_by_auth() -> None:
    ini, res = setup(3)
    m1 = ini.message1()
    tag, spi_i, sa, _, ni, cookie = unlp(m1)
    e = 12345
    m1_eve = lp(tag, spi_i, sa, b32(pow(G, e, P)), ni, cookie)
    m2 = res.respond(m1_eve)
    # Eve replaces KEr as well, so that she shares a DH value with each side.
    t2, s_i, s_r, sa2, _, nr = unlp(m2)
    m2_eve = lp(t2, s_i, s_r, sa2, b32(pow(G, e, P)), nr)
    m3 = ini.auth(m2_eve)
    assert m3 is not None
    # The responder cannot even open SK{...}: the keys differ. Re-encrypting does not help Eve,
    # because AUTHi signs message 1 as the initiator sent it, with the real KEi.
    assert res.auth(spi_i, m3) is None and res.keymat is None


def test_tampered_auth_payload_is_rejected() -> None:
    ini, res = setup(4)
    m1 = ini.message1()
    m3 = ini.auth(res.respond(m1))
    box = bytearray(unlp(m3)[1])
    box[20] ^= 1
    assert res.auth(unlp(m1)[1], lp(b"AUTH", bytes(box))) is None


def test_ke_outside_the_group_is_rejected() -> None:
    _, res = setup(5)
    for bad in (0, 1, P - 1):
        m1 = lp(b"INIT", b"\x01" * 8, b"ENCR_TOY|PRF_HMAC_SHA2_256|AUTH_TOY|GROUP_TOY256", b32(bad), b"\x02" * 32, b"")
        assert res.respond(m1) is None
