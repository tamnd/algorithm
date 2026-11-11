# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/load-linked-store-conditional/. The authors are listed in prov/5J33C1.jsonl.

from explorer import final_histories, replay
from lincheck import is_linearizable
from load_linked_store_conditional import LLSC, setup_for

P = [("ll",), ("sc", "C")]
Q = [("ll",), ("sc", "B"), ("ll",), ("sc", "A")]
# p links, q changes A to B and back to A, then p tries its SC.
ABA_SCHEDULE = [0] + [1] * 4 + [0]


def test_llsc_from_cas_is_linearizable_two_processes() -> None:
    progs = [[("ll",), ("sc", "B"), ("vl",)], [("ll",), ("sc", "C"), ("vl",)]]
    hs = final_histories(setup_for(progs))
    assert len(hs) > 10
    assert all(is_linearizable(h, LLSC("A")) for h in hs)


def test_llsc_from_cas_is_linearizable_three_processes() -> None:
    progs = [[("ll",), ("sc", "B")], [("ll",), ("sc", "C")], [("vl",), ("ll",), ("sc", "D")]]
    hs = final_histories(setup_for(progs))
    assert all(is_linearizable(h, LLSC("A")) for h in hs)


def test_aba_is_caught_by_the_tag() -> None:
    w = replay(setup_for([P, Q]), ABA_SCHEDULE)
    assert all(w.done)
    assert w.history[-1] == ("res", 0, False)       # p's SC fails
    assert w.mem.get("X") == ("A", 2)
    assert is_linearizable(w.history, LLSC("A"))


def test_aba_fools_plain_cas() -> None:
    w = replay(setup_for([P, Q], tagged=False), ABA_SCHEDULE)
    assert w.history[-1] == ("res", 0, True)        # p's CAS succeeds
    assert w.mem.get("X") == "C"
    assert not is_linearizable(w.history, LLSC("A"))


def test_plain_cas_is_not_llsc_in_some_run() -> None:
    hs = final_histories(setup_for([P, Q], tagged=False))
    bad = [h for h in hs if not is_linearizable(h, LLSC("A"))]
    good = final_histories(setup_for([P, Q]))
    assert bad
    assert all(is_linearizable(h, LLSC("A")) for h in good)
