# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/race-condition/. The authors are listed in prov/TVHXNT.jsonl.
from race_condition import (atomic_rw_increment, data_race, faa_increment, increment, locked_increment,
                            outcomes, schedule, set_done, withdraw)


def test_lost_update_schedule():
    # p0 reads 0, p1 reads 0, p0 writes 1, p1 writes 1: one update is lost.
    assert schedule([increment, increment], {"c": 0}, [0, 1, 0, 1], "c") == 1
    assert schedule([increment, increment], {"c": 0}, [0, 0, 1, 1], "c") == 2


def test_lost_update_all_interleavings():
    assert outcomes([increment] * 2, {"c": 0}, ["c"]) == {(1,), (2,)}
    assert outcomes([increment] * 3, {"c": 0}, ["c"]) == {(1,), (2,), (3,)}


def test_plain_increment_has_data_race():
    race = data_race([increment, increment], {"c": 0})
    assert race is not None
    assert {race[3][0], race[4][0]} <= {"r", "w"}


def test_race_condition_without_data_race():
    makes = [atomic_rw_increment] * 2
    assert data_race(makes, {"c": 0}) is None
    assert outcomes(makes, {"c": 0}, ["c"]) == {(1,), (2,)}


def test_check_then_act_without_data_race():
    mem = {"bal": 150, "paid": 0}
    assert data_race([withdraw, withdraw], mem) is None
    # The bank pays 200 from an account that held 150 in some runs.
    assert outcomes([withdraw, withdraw], mem, ["bal", "paid"]) == {(50, 100), (50, 200)}


def test_data_race_without_race_condition():
    assert data_race([set_done, set_done], {"done": False}) is not None
    assert outcomes([set_done, set_done], {"done": False}, ["done"]) == {(True,)}


def test_fixes():
    for makes in ([faa_increment] * 3, [locked_increment] * 3):
        mem = {"c": 0, "lock": 0}
        assert outcomes(makes, mem, ["c"]) == {(3,)}
        assert data_race(makes, mem) is None
