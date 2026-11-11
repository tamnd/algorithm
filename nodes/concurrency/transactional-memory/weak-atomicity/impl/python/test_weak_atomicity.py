# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-atomicity/. The authors are listed in prov/NZDH5H.jsonl.

import random

from sched import System, explore, random_run
from stm import TL2, EagerSTM
from weak_atomicity import PROGRAMS, anomaly


def count(name, cls, strong):
    runs = bad = 0
    for mem, sys in explore(PROGRAMS[name](cls, strong), 100):
        assert sys.finished()
        assert sys.error == [None, None]
        runs += 1
        bad += anomaly(name, mem, sys.result)
    return runs, bad


# (program, STM) pairs where weak atomicity shows the anomaly
WEAK_CASES = [
    ("NR", TL2), ("NR", EagerSTM),
    ("ILU", TL2), ("ILU", EagerSTM),
    ("GLU", TL2),
    ("IDR", EagerSTM),
]


def test_weak_atomicity_shows_each_anomaly():
    for name, cls in WEAK_CASES:
        runs, bad = count(name, cls, strong=False)
        assert runs > 0 and bad > 0, (name, cls.__name__)


def test_strong_atomicity_removes_each_anomaly():
    for name, cls in WEAK_CASES:
        runs, bad = count(name, cls, strong=True)
        assert runs > 0 and bad == 0, (name, cls.__name__)


def test_no_anomaly_where_the_design_prevents_it():
    # a redo log writes only final values, so TL2 has no dirty read;
    # in-place writes of one word do not touch the other word of the block
    assert count("IDR", TL2, strong=False)[1] == 0
    assert count("GLU", EagerSTM, strong=False)[1] == 0


def test_without_concurrency_there_is_no_anomaly():
    for name, make_prog in PROGRAMS.items():
        for cls in (TL2, EagerSTM):
            for order in ([0] * 50 + [1] * 50, [1] * 50 + [0] * 50):
                mem, procs = make_prog(cls, False)()
                sys = System(procs)
                for p in order:
                    if p in sys.runnable():
                        sys.step(p)
                assert sys.finished()
                assert not anomaly(name, mem, sys.result)


def test_random_schedules():
    rng = random.Random(2006)
    names = sorted(PROGRAMS)
    for i in range(800):
        name = names[i % 4]
        cls = (TL2, EagerSTM)[(i // 4) % 2]
        mem, sys = random_run(PROGRAMS[name](cls, True), rng, 1000)
        assert sys.finished()
        assert not anomaly(name, mem, sys.result)
