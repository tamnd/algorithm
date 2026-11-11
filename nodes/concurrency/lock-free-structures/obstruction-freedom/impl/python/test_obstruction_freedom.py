# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obstruction-freedom/. The authors are listed in prov/V63Y97.jsonl.

from explorer import replay
from lincheck import is_linearizable
from obstruction_freedom import Deque, bounded_states, contents, livelock, max_solo_steps, setup_for

CASES = [
    ([[("rightpush", "a")], [("leftpush", "b")]], ()),
    ([[("rightpop", None)], [("leftpop", None)]], ("x",)),
    ([[("rightpop", None)], [("leftpop", None)]], ("x", "y")),
    ([[("rightpush", "a")], [("rightpop", None)]], ()),
    ([[("leftpush", "a")], [("rightpop", None)]], ()),
    ([[("rightpush", "a")], [("leftpop", None)]], ()),
    ([[("rightpush", "a")], [("rightpush", "b")]], ()),
]
TWO_OPS = ([[("rightpush", "a"), ("rightpop", None)], [("leftpush", "b"), ("leftpop", None)]], ())


def histories(setup, depth):
    return {tuple(replay(setup, s).history) for s in bounded_states(setup, depth)}


def test_sequential_use() -> None:
    progs = [[("rightpush", 1), ("rightpush", 2), ("leftpush", 0), ("leftpop", None),
              ("rightpop", None), ("rightpop", None), ("rightpop", None)]]
    w = replay(setup_for(progs, (), 3, 3), [])
    while w.enabled():
        w.step(0)
    assert [e[2] for e in w.history if e[0] == "res"] == ["ok", "ok", "ok", 0, 2, 1, "empty"]
    assert contents(w) == ()


def test_full_ends() -> None:
    w = replay(setup_for([[("rightpush", 1), ("rightpush", 2)]], (), 2, 2), [])
    while w.enabled():
        w.step(0)
    assert [e[2] for e in w.history if e[0] == "res"] == ["ok", "full"]


def test_linearizable_in_all_short_runs() -> None:
    # Every history of every run of up to 24 steps, including the ones with
    # pending operations, is linearizable.
    for progs, items in CASES + [TWO_OPS]:
        setup = setup_for(progs, items, 3, 3)
        for h in histories(setup, 24):
            assert is_linearizable(list(h), Deque(items)), h


def test_obstruction_free() -> None:
    # From every state reached in up to 24 steps, each process that runs
    # alone finishes: at most the rest of one attempt plus one full attempt.
    for progs, items in CASES:
        steps = max_solo_steps(setup_for(progs, items, 3, 3), 24)
        assert steps is not None and steps <= 11
    assert max_solo_steps(setup_for(*TWO_OPS, 3, 3), 24) == 17


def test_livelock_so_not_lock_free() -> None:
    w = livelock(1000)
    assert w.steps == [6000, 6000]
    assert not [e for e in w.history if e[0] == "res"]   # no operation completes
    assert contents(w) == ()
