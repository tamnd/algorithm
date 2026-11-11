# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-messaging/. The authors are listed in prov/8PE1DX.jsonl.
#
# The toy protocols have no official vectors. The X25519 copy is checked with
# RFC 7748 Section 5.2, copied by hand. The other tests check the FS and PCS
# pattern that each design is known to have (Unger et al., IEEE S&P 2015;
# Cohn-Gordon, Cremers and Garratt, CSF 2016).

from secure_messaging import DHRatchet, HashRatchet, SessionDH, StaticKey, run, score_all, x25519


def test_rfc7748_x25519():
    k = bytes.fromhex("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = bytes.fromhex("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    assert x25519(k, u) == bytes.fromhex("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")


def test_score_table():
    s = score_all(n=16, compromise_at=6, session_len=4)
    static, session, hashr, dhr = (s[p.name] for p in (StaticKey, SessionDH, HashRatchet, DHRatchet))
    assert static.past == list(range(6)) and static.future == list(range(6, 16))
    assert not static.fs and not static.pcs
    assert session.past == [4, 5] and session.future == [6, 7]  # the current session only
    assert not session.fs and session.pcs
    assert hashr.past == [] and hashr.future == list(range(6, 16))
    assert hashr.fs and not hashr.pcs
    assert dhr.past == [] and dhr.future == [6, 7]  # one message each way, then healed
    assert dhr.fs and dhr.pcs


def test_dh_ratchet_heals_within_one_round_trip_for_both_victims():
    for victim in ("A", "B"):
        for t in (1, 4, 7, 10):
            r = run(DHRatchet, n=14, compromise_at=t, victim=victim)
            assert r.fs and r.pcs and len(r.future) <= 2
            assert all(f in (t, t + 1) for f in r.future)
            h = run(HashRatchet, n=14, compromise_at=t, victim=victim)
            assert h.fs and h.future == list(range(t, 14))


def test_session_dh_exposes_exactly_the_current_session():
    for t in (2, 5, 8, 11):
        r = run(SessionDH, n=16, compromise_at=t, session_len=4)
        assert r.past == [i for i in range(t) if i // 4 == t // 4]
        assert r.future == [i for i in range(t, 16) if i // 4 == t // 4]


def test_one_long_session_is_no_better_than_a_static_key():
    r = run(SessionDH, n=10, compromise_at=5, session_len=100)
    assert r.past == list(range(5)) and r.future == list(range(5, 10))
