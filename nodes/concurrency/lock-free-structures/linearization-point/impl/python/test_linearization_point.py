# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linearization-point/. The authors are listed in prov/X31NPD.jsonl.

from explorer import final_histories, random_run, replay
from lincheck import Stack, is_linearizable
from linearization_point import lp_order, setup_for

TWO = [[("push", 1), ("pop",)], [("push", 2), ("pop",)]]
THREE = [[("push", 1)], [("push", 2)], [("pop",)]]


def test_points_give_a_legal_order_in_every_run() -> None:
    for programs, init in ((TWO, ()), (THREE, (0,))):
        hs = final_histories(setup_for(programs, init))
        assert len(hs) > 10
        for h in hs:
            ok, info = lp_order(h, init)
            assert ok, info
            assert is_linearizable(h, Stack(init))


def test_point_at_the_read_is_wrong() -> None:
    bad = [h for h in final_histories(setup_for(TWO, (), lp_at="read")) if not lp_order(h)[0]]
    assert bad
    # The stack is still linearizable in those runs: only the choice of points is wrong.
    assert all(is_linearizable(h, Stack()) for h in bad)


def test_pop_with_a_plain_write_is_not_linearizable() -> None:
    progs = [[("pop",)], [("pop",)]]
    hs = final_histories(setup_for(progs, (1, 2), bad_pop=True))
    assert any(not is_linearizable(h, Stack((1, 2))) for h in hs)


def test_worked_example_schedule() -> None:
    # p0 push(1), p1 push(2), on an empty stack. p0 reads, p1 reads, p1 CAS wins,
    # p0 CAS fails, p0 reads again, p0 CAS wins. The order of points is push(2), push(1).
    w = replay(setup_for([[("push", 1)], [("push", 2)]]), [0, 1, 1, 0, 0, 0])
    assert all(w.done)
    ok, seq = lp_order(w.history)
    assert ok and [s[2] for s in seq] == [2, 1]
    assert w.mem.get("top")[1] == 1


def test_random_runs_with_three_processes() -> None:
    progs = [[("push", 1), ("pop",), ("push", 3)], [("pop",), ("push", 2)], [("push", 4), ("pop",)]]
    for seed in range(200):
        w = random_run(setup_for(progs), seed)
        assert all(w.done)
        assert lp_order(w.history)[0]
        assert is_linearizable(w.history, Stack())
