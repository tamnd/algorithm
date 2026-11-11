# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/redo-log/. The authors are listed in prov/H76MZA.jsonl.

import math
import random

from redo_log import MISS, AppendOnlyRedoLog, RedoLog


def test_worked_example():
    mem = {"x": 0, "y": 0, "z": 0}
    log = RedoLog()
    log.write("x", 1)
    log.write("y", 2)
    log.write("x", 3)
    assert log.entries == [["x", 3], ["y", 2]]
    assert log.lookup("x") == 3 and log.lookup("y") == 2 and log.lookup("z") is MISS
    assert mem == {"x": 0, "y": 0, "z": 0}  # nothing reaches memory before commit
    assert log.write_back(mem) == 2
    assert mem == {"x": 3, "y": 2, "z": 0}


def test_random_operations_match_a_model():
    rng = random.Random(1)
    for trial in range(200):
        words = [f"w{i}" for i in range(6)]
        mem = {a: -1 for a in words}
        log, model = RedoLog(filter_bits=16), {}
        for _ in range(rng.randrange(1, 40)):
            a = rng.choice(words)
            if rng.random() < 0.5:
                v = rng.randrange(100)
                log.write(a, v)
                model[a] = v
            else:
                got = log.lookup(a)
                assert (got is MISS and a not in model) or got == model.get(a)
        assert len(log) == len(model)
        assert [e[0] for e in log.entries] == list(model)  # one entry per word, in first-write order
        log.write_back(mem)
        assert mem == {a: model.get(a, -1) for a in words}


def test_discard_leaves_memory_unchanged():
    mem = {"x": 5}
    log = RedoLog()
    log.write("x", 6)
    log.discard()
    assert log.lookup("x") is MISS and len(log) == 0
    assert log.write_back(mem) == 0 and mem == {"x": 5}


def test_scan_costs_w_squared_probes_and_the_index_2w():
    for w in (1, 5, 20, 50):
        costs = {}
        for indexed in (True, False):
            log = RedoLog(filter_bits=1, hashes=1, indexed=indexed)  # one filter bit: every lookup probes
            for i in range(w):
                log.write(i, i)
            for i in range(w):
                assert log.lookup(i) == i
            costs[indexed] = log.probes
        assert costs[True] == 2 * w
        assert costs[False] == w * (w - 1) // 2 + w * (w + 1) // 2 == w * w


def test_filter_has_no_false_negatives_and_few_false_positives():
    log = RedoLog(filter_bits=64, hashes=2)
    for i in range(8):
        log.write(("w", i), i)
    assert all(log.may_contain(("w", i)) for i in range(8))
    false_pos = sum(log.may_contain(("u", i)) for i in range(10000))
    expected = 10000 * (1 - math.exp(-2 * 8 / 64)) ** 2  # about 489
    set_bits = bin(log.filter).count("1")
    assert false_pos == sum(1 for i in range(10000) if log.may_contain(("u", i)))
    assert abs(false_pos - 10000 * (set_bits / 64) ** 2) < 150
    assert 300 < false_pos < 700, (false_pos, expected, set_bits)
    print("false positives", false_pos, "set bits", set_bits, "expected", round(expected))


def test_append_only_log_gives_the_same_memory_with_more_entries():
    rng = random.Random(7)
    words = ["a", "b", "c"]
    writes = [(rng.choice(words), rng.randrange(10)) for _ in range(30)]
    m1, m2 = {a: 0 for a in words}, {a: 0 for a in words}
    log, app = RedoLog(), AppendOnlyRedoLog()
    for a, v in writes:
        log.write(a, v)
        app.write(a, v)
        assert log.lookup(a) == app.lookup(a) == v
    assert log.write_back(m1) == 3 and app.write_back(m2) == 30
    assert m1 == m2
