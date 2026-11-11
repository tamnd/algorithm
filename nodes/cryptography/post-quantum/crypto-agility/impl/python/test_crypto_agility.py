# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crypto-agility/. The authors are listed in prov/YNGHPQ.jsonl.

import pytest

from crypto_agility import (
    DISALLOWED,
    Algorithm,
    handshake,
    inventory,
    negotiate,
    tls_groups,
    transcript_hash,
)

HYBRID, P256_HYBRID, X25519, P256, FFDHE, EXPORT = 0x11EC, 0x11EB, 0x001D, 0x0017, 0x0100, 0xFF01
CLIENT = [HYBRID, X25519, P256, EXPORT]
SERVER = [HYBRID, P256_HYBRID, X25519, P256, FFDHE, EXPORT]


def test_negotiation_picks_best_common_algorithm():
    r = tls_groups()
    assert negotiate(r, CLIENT, SERVER) == HYBRID
    assert negotiate(r, [P256, X25519], SERVER) == X25519
    assert negotiate(r, [0x1234], SERVER) is None


def test_duplicate_code_point_rejected():
    r = tls_groups()
    with pytest.raises(ValueError):
        r.register(Algorithm("clash", X25519))


def test_policy_change_without_code_change():
    r = tls_groups()
    r.set_status(HYBRID, DISALLOWED)
    assert negotiate(r, CLIENT, SERVER) == X25519


@pytest.mark.parametrize("protection", ["none", "session-mac", "signed-transcript"])
def test_no_false_alarm(protection):
    result = handshake(tls_groups(), CLIENT, SERVER, protection)
    assert result.chosen == HYBRID and not result.detected


def test_downgrade_without_protection_succeeds():
    result = handshake(tls_groups(), CLIENT, SERVER, "none", strip={HYBRID, X25519, P256})
    assert result.chosen == EXPORT and not result.detected


def test_session_mac_fails_when_weak_algorithm_is_breakable():
    # Logjam: the attacker breaks the export group and fixes the Finished MAC.
    result = handshake(tls_groups(), CLIENT, SERVER, "session-mac", strip={HYBRID, X25519, P256})
    assert result.chosen == EXPORT and not result.detected


def test_session_mac_detects_downgrade_to_unbroken_algorithm():
    result = handshake(tls_groups(), CLIENT, SERVER, "session-mac", strip={HYBRID})
    assert result.chosen == X25519 and result.detected


@pytest.mark.parametrize("strip", [{HYBRID}, {HYBRID, X25519}, {HYBRID, X25519, P256}])
def test_signed_transcript_detects_every_downgrade(strip):
    result = handshake(tls_groups(), CLIENT, SERVER, "signed-transcript", strip=strip)
    assert result.chosen != HYBRID and result.detected


def test_disallowing_weak_algorithm_removes_the_target():
    r = tls_groups()
    r.set_status(EXPORT, DISALLOWED)
    result = handshake(r, CLIENT, SERVER, "none", strip={HYBRID, X25519, P256})
    assert result.chosen is None


def test_transcript_hash_covers_order():
    assert transcript_hash([HYBRID, X25519], X25519) != transcript_hash([X25519, HYBRID], X25519)


def test_inventory():
    r = tls_groups()
    usages = [("web", HYBRID), ("web", X25519), ("vpn", FFDHE), ("legacy", EXPORT), ("iot", 0x9999)]
    inv = inventory(r, usages)
    assert inv == {
        "total": 5,
        "quantum_vulnerable": 3,
        "approved": 3,
        "deprecated": 1,
        "disallowed": 0,
        "unknown": 1,
    }
