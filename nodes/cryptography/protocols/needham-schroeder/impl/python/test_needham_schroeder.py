# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needham-schroeder/. The authors are listed in prov/0T48C0.jsonl.
#
# There are no official test vectors for a protocol model checker. The
# expected attack is the one in Lowe, Information Processing Letters 56(3),
# 1995, and Lowe, TACAS 1996, Section 3: A starts a run with the intruder,
# and the intruder replays it to B as if it came from A.

from needham_schroeder import (
    check,
    check_all,
    close,
    derive,
    enc,
    msg1,
    msg2,
    tup,
)

LOWE_TRACE = [
    "A sends {N1, A}pk(I)",
    "B receives {N1, A}pk(B)",
    "B sends {N1, N2}pk(A)",
    "A receives {N1, N2}pk(A)",
    "A sends {N2}pk(I)",
    "B receives {N2}pk(B)",
]


def test_deduction():
    k = close(frozenset({"A", "B", "I", "Ni", enc("I", tup("N1", "A")), enc("B", "N2")}))
    assert "N1" in k  # the intruder opens messages sent to it
    assert "N2" not in k  # but not messages for B
    assert derive(k, enc("B", tup("N1", "A")))  # it re-encrypts N1 for B, posing as A
    assert derive(k, enc("B", "N2"))  # it forwards what it has seen
    assert not derive(k, enc("A", tup("N1", "N2")))
    assert close(frozenset({tup("x", tup("y", "z"))})) >= {"x", "y", "z"}


def test_lowe_attack_on_nspk():
    r = check("nspk", [("init", "A", "I"), ("resp", "B")])
    assert r.attack == LOWE_TRACE
    assert any(g.startswith("agreement: B finished a run with A") for g in r.goals)
    assert any(g.startswith("secrecy: B's run with A") for g in r.goals)


def test_no_attack_on_nsl_same_scenario():
    r = check("nsl", [("init", "A", "I"), ("resp", "B")])
    assert r.attack is None and r.states > 0


def test_honest_scenario_has_no_attack():
    for proto in ("nspk", "nsl"):
        assert check(proto, [("init", "A", "B"), ("resp", "B")]).attack is None


def test_nsl_message_2_is_what_blocks_the_replay():
    # In NSL, B's reply names B. A expects {N1, z, I}pk(A) in her run with I and
    # cannot accept {N1, N2, B}pk(A).
    assert msg2("nsl", "B", "A", "N1", "N2") != msg2("nsl", "I", "A", "N1", "N2")
    assert msg2("nspk", "B", "A", "N1", "N2") == msg2("nspk", "I", "A", "N1", "N2")
    assert msg1("A", "I", "N1") == enc("I", tup("N1", "A"))


def test_all_scenarios_up_to_three_sessions():
    nspk = check_all("nspk", 3)
    nsl = check_all("nsl", 3)
    assert len(nspk) == len(nsl) == 6 + 21 + 56
    attacked = [s for s, r in nspk.items() if r.attack is not None]
    assert attacked
    # every attack needs an initiator who talks to the intruder and an honest responder
    for scen in attacked:
        assert any(s[0] == "init" and s[2] == "I" for s in scen)
        assert any(s[0] == "resp" for s in scen)
    assert all(r.attack is None for r in nsl.values())
