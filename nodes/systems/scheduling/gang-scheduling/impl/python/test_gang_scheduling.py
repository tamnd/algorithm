# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gang-scheduling/. The authors are listed in prov/YGJAGZ.jsonl.

import random

import pytest

from gang_scheduling import Gang, Matrix, gang_schedule


def show(cells):
    return "".join("." if c is None else c[0] for c in cells)


def test_matrix_example() -> None:
    gangs = [Gang("A", 0, 2, 2), Gang("B", 0, 3, 1), Gang("C", 0, 2, 3), Gang("D", 0, 1, 2)]
    m = Matrix(4)
    for g in gangs:
        m.place(g)
    assert [show(row) for row in m.rows] == ["AACC", "BBBD"]
    tr = gang_schedule(4, gangs)
    assert [show(s) for s in tr.slots] == ["AACC", "BBBD", "AACC", "...D", "..CC"]
    assert tr.done == {"B": 2, "A": 3, "D": 4, "C": 5}


def test_alternate_selection_fills_idle_columns() -> None:
    gangs = [Gang("A", 0, 3, 4), Gang("B", 0, 2, 4), Gang("C", 0, 1, 4)]
    plain = gang_schedule(4, gangs)
    assert [show(s) for s in plain.slots[:2]] == ["AAAC", "BB.."]
    assert plain.done == {"A": 7, "C": 7, "B": 8}
    alt = gang_schedule(4, gangs, alternate=True)
    assert [show(s) for s in alt.slots[:2]] == ["AAAC", "BB.C"]
    assert alt.done == {"C": 4, "A": 7, "B": 8}


def check_trace(processors, gangs, tr):
    by_name = {g.name: g for g in gangs}
    runs = {g.name: [] for g in gangs}
    for t, cells in enumerate(tr.slots):
        assert len(cells) == processors
        present = {}
        for c in cells:
            if c is not None:
                present.setdefault(c[0], set()).add(c[1])
        for name, threads in present.items():
            # all threads of the gang run in this slot, each exactly once
            assert threads == set(range(by_name[name].size))
            assert sum(1 for c in cells if c is not None and c[0] == name) == by_name[name].size
            assert by_name[name].arrival <= t < tr.done[name]
            runs[name].append(t)
    for g in gangs:
        assert len(runs[g.name]) == g.work and runs[g.name][-1] + 1 == tr.done[g.name]
    return runs


def test_gang_threads_always_run_together() -> None:
    rng = random.Random(6)
    for _ in range(200):
        p = rng.randrange(1, 7)
        gangs = [
            Gang(f"g{i}", rng.randrange(0, 8), rng.randrange(1, p + 1), rng.randrange(1, 6))
            for i in range(rng.randrange(1, 8))
        ]
        for alternate in (False, True):
            check_trace(p, gangs, gang_schedule(p, gangs, alternate))


def test_every_gang_runs_once_per_round_of_rows() -> None:
    rng = random.Random(7)
    for _ in range(200):
        p = rng.randrange(1, 6)
        gangs = [Gang(f"g{i}", 0, rng.randrange(1, p + 1), rng.randrange(1, 6)) for i in range(rng.randrange(1, 8))]
        m = Matrix(p)
        for g in sorted(gangs, key=lambda g: g.name):
            m.place(g)
        rows = len(m.rows)
        for alternate in (False, True):
            tr = gang_schedule(p, gangs, alternate)
            for g, ts in check_trace(p, gangs, tr).items():
                gaps = [ts[0] + 1] + [b - a for a, b in zip(ts, ts[1:])]
                assert max(gaps) <= rows


def test_independent_round_robin_splits_gangs() -> None:
    # Without coordination: threads are dealt to processors in turn, and each
    # processor runs its own round robin. Gang B is split in the first slot.
    gangs = [Gang("A", 0, 2, 2), Gang("B", 0, 3, 1), Gang("C", 0, 2, 3), Gang("D", 0, 1, 2)]
    local = [[] for _ in range(4)]
    k = 0
    for g in gangs:
        for i in range(g.size):
            local[k % 4].append((g.name, i))
            k += 1
    first_slot = [q[0] for q in local]
    assert first_slot == [("A", 0), ("A", 1), ("B", 0), ("B", 1)]  # B2 waits on processor 0
    tr = gang_schedule(4, gangs)
    assert all(
        sum(1 for c in cells if c is not None and c[0] == "B") in (0, 3) for cells in tr.slots
    )


def test_edges() -> None:
    assert gang_schedule(2, []).slots == []
    with pytest.raises(ValueError):
        Matrix(0)
    with pytest.raises(ValueError):
        gang_schedule(2, [Gang("X", 0, 3, 1)])
    tr = gang_schedule(2, [Gang("X", 2, 2, 1)])
    assert [show(s) for s in tr.slots] == ["..", "..", "XX"] and tr.done == {"X": 3}
