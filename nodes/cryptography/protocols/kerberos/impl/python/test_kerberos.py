# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kerberos/. The authors are listed in prov/D7Z6QK.jsonl.
#
# RFC 4120 has no test vectors for the protocol flow, and this toy uses JSON
# and a study AEAD in place of ASN.1 and the real enctypes, so no official
# vector applies. The tests check the flow and the RFC 4120 checks: expiry,
# skew, replay and pre-authentication. All parties are local objects.

import pytest

from kerberos import (
    MAX_LIFE,
    SKEW,
    USAGE_AS_REP_ENC,
    USAGE_AP_REQ_AUTH,
    USAGE_TGS_REQ_AUTH,
    Client,
    Clock,
    KDC,
    KerberosError,
    Service,
    full_login,
    offline_guess,
    seal,
    string_to_key,
    unseal,
)

REALM = "EXAMPLE.ORG"
T0 = 1_700_000_000


def setup(preauth=True, password="correct horse battery staple"):
    clock = Clock(T0)
    kdc = KDC(REALM, clock)
    alice = Client("alice", password, REALM, Clock(T0))
    kdc.add_principal("alice", string_to_key(password, REALM, "alice"), require_preauth=preauth)
    skey = string_to_key("a long random service secret 7f3a", REALM, "host/files")
    kdc.add_principal("host/files", skey)
    files = Service("host/files", skey, Clock(T0))
    return kdc, alice, files


def advance(dt, *clocks):
    for c in clocks:
        c.t += dt


def test_full_flow_with_mutual_authentication():
    kdc, alice, files = setup()
    assert full_login(kdc, alice, files)
    assert len(files.sessions["alice"]) == 32
    assert files.sessions["alice"] != alice.tgs_key


def test_tgt_is_reused_for_many_services():
    kdc, alice, files = setup()
    skey2 = string_to_key("another service secret", REALM, "http/web")
    kdc.add_principal("http/web", skey2)
    web = Service("http/web", skey2, Clock(T0))
    alice.as_exchange(kdc)
    for svc in (files, web):
        alice.tgs_exchange(kdc, svc.name)
        req, stamp = alice.make_ap_req(svc.name)
        assert alice.check_ap_rep(svc.name, svc.ap_req(req), stamp)
    assert files.sessions["alice"] != web.sessions["alice"]


def test_ticket_expiry():
    kdc, alice, files = setup()
    alice.as_exchange(kdc, life=3600)
    alice.tgs_exchange(kdc, files.name, life=600)
    advance(600 + SKEW, kdc.clock, alice.clock, files.clock)
    req, _ = alice.make_ap_req(files.name)
    assert files.ap_req(req) is not None  # at endtime + skew the ticket is still accepted
    advance(1, kdc.clock, alice.clock, files.clock)
    req, _ = alice.make_ap_req(files.name)
    with pytest.raises(KerberosError) as e:
        files.ap_req(req)
    assert e.value.code == "KRB_AP_ERR_TKT_EXPIRED"
    # The TGT expires too: the TGS refuses to use it.
    advance(3600, kdc.clock, alice.clock, files.clock)
    with pytest.raises(KerberosError) as e:
        alice.tgs_exchange(kdc, files.name)
    assert e.value.code == "KRB_AP_ERR_TKT_EXPIRED"


def test_ticket_life_is_capped():
    kdc, alice, files = setup()
    alice.as_exchange(kdc, life=10 * MAX_LIFE)
    alice.tgs_exchange(kdc, files.name)
    advance(MAX_LIFE + SKEW + 1, kdc.clock, alice.clock, files.clock)
    req, _ = alice.make_ap_req(files.name)
    with pytest.raises(KerberosError):
        files.ap_req(req)


def test_replay_rejected_by_authenticator_cache():
    kdc, alice, files = setup()
    alice.as_exchange(kdc)
    alice.tgs_exchange(kdc, files.name)
    req, _ = alice.make_ap_req(files.name)
    files.ap_req(req)
    with pytest.raises(KerberosError) as e:
        files.ap_req(req)  # the same AP-REQ, recorded and sent again at once
    assert e.value.code == "KRB_AP_ERR_REPEAT"
    # After the window the cache has dropped the entry, but the skew check rejects the old authenticator.
    advance(SKEW + 1, files.clock)
    with pytest.raises(KerberosError) as e:
        files.ap_req(req)
    assert e.value.code == "KRB_AP_ERR_SKEW"
    # A fresh authenticator with the same ticket is fine.
    alice.clock.t = files.clock.t
    req2, _ = alice.make_ap_req(files.name)
    assert files.ap_req(req2) is not None


def test_replay_at_the_tgs():
    kdc, alice, files = setup()
    alice.as_exchange(kdc)
    auth = seal(alice.tgs_key, USAGE_TGS_REQ_AUTH, {"cname": "alice", "ctime": T0, "cusec": 99})
    req = {"ap_req": {"ticket": alice.tgt, "authenticator": auth}, "sname": files.name, "nonce": 1, "till": T0 + 60}
    kdc.tgs_req(req)
    with pytest.raises(KerberosError) as e:
        kdc.tgs_req(req)
    assert e.value.code == "KRB_AP_ERR_REPEAT"


def test_clock_skew():
    kdc, alice, files = setup()
    alice.as_exchange(kdc)
    alice.tgs_exchange(kdc, files.name)
    alice.clock.t = T0 + SKEW + 5  # the client's clock runs fast
    req, _ = alice.make_ap_req(files.name)
    with pytest.raises(KerberosError) as e:
        files.ap_req(req)
    assert e.value.code == "KRB_AP_ERR_SKEW"
    alice.clock.t = T0 - SKEW - 5  # and with pre-authentication, the KDC sees the skew too
    with pytest.raises(KerberosError) as e:
        alice.as_exchange(kdc)
    assert e.value.code == "KRB_AP_ERR_SKEW"


def test_modified_or_misdirected_tickets():
    kdc, alice, files = setup()
    alice.as_exchange(kdc)
    alice.tgs_exchange(kdc, files.name)
    req, _ = alice.make_ap_req(files.name)
    bad = dict(req, ticket=req["ticket"][:-1] + bytes([req["ticket"][-1] ^ 1]))
    with pytest.raises(KerberosError) as e:
        files.ap_req(bad)
    assert e.value.code == "KRB_AP_ERR_MODIFIED"
    other = Service("host/other", string_to_key("x", REALM, "host/other"), Clock(T0))
    with pytest.raises(KerberosError) as e:
        other.ap_req(req)
    assert e.value.code == "KRB_AP_ERR_MODIFIED"
    # An authenticator under the wrong key (an attacker who has the ticket but not the session key)
    forged = dict(req, authenticator=seal(b"\x00" * 32, USAGE_AP_REQ_AUTH, {"cname": "alice", "ctime": T0, "cusec": 1}))
    with pytest.raises(KerberosError) as e:
        files.ap_req(forged)
    assert e.value.code == "KRB_AP_ERR_MODIFIED"


def test_preauthentication():
    kdc, alice, _ = setup(preauth=True)
    with pytest.raises(KerberosError) as e:
        alice.as_exchange(kdc, preauth=False)
    assert e.value.code == "KDC_ERR_PREAUTH_REQUIRED"
    mallory = Client("alice", "wrong guess", REALM, Clock(T0))
    with pytest.raises(KerberosError) as e:
        mallory.as_exchange(kdc)
    assert e.value.code == "KDC_ERR_PREAUTH_FAILED"
    alice.as_exchange(kdc)
    assert alice.tgt is not None


def test_offline_guess_without_preauthentication():
    weak = "sunshine"
    kdc, alice, _ = setup(preauth=False, password=weak)
    # Anyone may send an AS-REQ for alice; with pre-authentication off the KDC answers.
    req = {"cname": "alice", "sname": kdc.tgs_name, "nonce": 5, "till": T0 + 3600}
    rep = kdc.as_req(req)
    words = ["password", "123456", "letmein", "dragon", "qwerty", "monkey", "sunshine", "princess"]
    assert offline_guess(rep["enc_part"], USAGE_AS_REP_ENC, REALM, "alice", words) == weak
    assert offline_guess(rep["enc_part"], USAGE_AS_REP_ENC, REALM, "alice", ["password", "dragon"]) is None
    # With the guessed password the attacker has the TGT session key and acts as alice.
    k = string_to_key(weak, REALM, "alice")
    assert len(bytes.fromhex(unseal(k, USAGE_AS_REP_ENC, rep["enc_part"])["key"])) == 32


def test_unknown_principals():
    kdc, alice, _ = setup()
    with pytest.raises(KerberosError) as e:
        Client("bob", "pw", REALM, Clock(T0)).as_exchange(kdc)
    assert e.value.code == "KDC_ERR_C_PRINCIPAL_UNKNOWN"
    alice.as_exchange(kdc)
    with pytest.raises(KerberosError) as e:
        alice.tgs_exchange(kdc, "host/none")
    assert e.value.code == "KDC_ERR_S_PRINCIPAL_UNKNOWN"
