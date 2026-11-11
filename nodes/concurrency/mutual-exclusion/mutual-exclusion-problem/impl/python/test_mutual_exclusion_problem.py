# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-problem/. The authors are listed in prov/0XYD33.jsonl.
from mutual_exclusion_problem import (TWO, alternation_lock, alternation_unlock, check, flag_unlock,
                                      one_flag_lock, one_flag_unlock, peterson_lock, stuck_run,
                                      two_flags_lock)


def test_one_flag_breaks_mutual_exclusion():
    res = check(one_flag_lock, one_flag_unlock, TWO)
    assert not res["mutual_exclusion"]
    # Both processes read busy = false before either writes it.
    labels = [lab[0] for _, lab in res["bad"]]
    assert labels.count("w") == 2


def test_one_flag_schedule():
    ex, s = stuck_run(one_flag_lock, one_flag_unlock, TWO, [0, 1, 0, 1, 0, 1])
    assert ex.inside(s) == [0, 1]


def test_alternation_is_safe_but_not_deadlock_free():
    res = check(alternation_lock, alternation_unlock, TWO)
    assert res["mutual_exclusion"]
    # Process 1 stays in its remainder section, so process 0 waits for a turn that never comes.
    assert not res["deadlock_free"]


def test_two_flags_deadlock():
    res = check(two_flags_lock, flag_unlock, TWO)
    assert res["mutual_exclusion"]
    assert not res["deadlock_free"]
    # Both raise their flags, then each waits for the other forever.
    ex, s = stuck_run(two_flags_lock, flag_unlock, TWO, [0, 1, 0, 1])
    assert [r[2] for r in s[1]] == ["T", "T"]
    for _ in range(5):
        s = ex.run([0, 1], s)
        assert [r[2] for r in s[1]] == ["T", "T"]


def test_peterson_meets_every_requirement():
    for rounds in (1, 2, -1):
        res = check(peterson_lock, flag_unlock, TWO, rounds=rounds)
        assert res["mutual_exclusion"] and res["deadlock_free"] and res["starvation_free"]
        assert res["bypass_from_door"] <= 1 and res["fcfs"]
