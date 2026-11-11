# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistency-models/. The authors are listed in prov/RP1X08.jsonl.

import itertools
import random

from consistency_models import (
    CAUSAL_NOT_SEQ,
    NOT_PRAM,
    PRAM_NOT_CAUSAL,
    SEQ_NOT_LIN,
    STORE_BUFFER,
    History,
    Op,
    classify,
    is_causal,
    is_linearizable,
    is_pram,
    is_sequential,
    r,
    w,
)


def test_seq_not_lin() -> None:
    assert classify(SEQ_NOT_LIN) == {"linearizable": False, "sequential": True, "causal": True, "pram": True}


def test_causal_not_seq() -> None:
    assert classify(CAUSAL_NOT_SEQ) == {"linearizable": False, "sequential": False, "causal": True, "pram": True}


def test_store_buffer() -> None:
    assert classify(STORE_BUFFER) == {"linearizable": False, "sequential": False, "causal": True, "pram": True}


def test_pram_not_causal() -> None:
    assert classify(PRAM_NOT_CAUSAL) == {"linearizable": False, "sequential": False, "causal": False, "pram": True}


def test_not_pram() -> None:
    assert classify(NOT_PRAM) == {"linearizable": False, "sequential": False, "causal": False, "pram": False}


def test_linearizable_examples() -> None:
    # Overlapping write and read: the read may return the old or the new value.
    for v in (0, 1):
        h = [w(1, "x", 1, 0, 2), r(2, "x", v, 1, 3)]
        assert is_linearizable(h)
    # A read after the write ends must see it.
    assert is_linearizable([w(1, "x", 1, 0, 1), r(2, "x", 1, 2, 3)])
    # New-old inversion: two reads in real-time order see new then old.
    h = [w(1, "x", 1, 0, 10), r(2, "x", 1, 1, 2), r(3, "x", 0, 3, 4)]
    assert not is_linearizable(h) and is_sequential(h)


def test_unwritten_value() -> None:
    h = [r(1, "x", 7)]
    assert classify(h) == {"linearizable": False, "sequential": False, "causal": False, "pram": False}


def random_history(rng: random.Random) -> History:
    procs = rng.randint(1, 3)
    n = rng.randint(1, 6)
    counters = {"x": 0, "y": 0}
    written: dict[str, list[int]] = {"x": [0], "y": [0]}
    h: list[Op] = []
    clock = {p: 0.0 for p in range(procs)}
    for _ in range(n):
        p = rng.randrange(procs)
        var = rng.choice("xy")
        start = clock[p] + rng.random() * 3
        end = start + rng.random() * 3
        clock[p] = end
        if rng.random() < 0.5:
            counters[var] += 1
            written[var].append(counters[var])
            h.append(Op(p, "w", var, counters[var], start, end))
        else:
            h.append(Op(p, "r", var, rng.choice(written[var] + [counters[var] + 1]), start, end))
    # list order must be program order: sort by process, then by start time
    h.sort(key=lambda op: (op.inv, op.proc))
    return h


def test_inclusions_on_random_histories() -> None:
    rng = random.Random(20240611)
    counts = {"linearizable": 0, "sequential": 0, "causal": 0, "pram": 0}
    for _ in range(600):
        h = random_history(rng)
        c = classify(h)
        assert not c["linearizable"] or c["sequential"]
        assert not c["sequential"] or c["causal"]
        assert not c["causal"] or c["pram"]
        for k in counts:
            counts[k] += c[k]
    assert counts["linearizable"] <= counts["sequential"] <= counts["causal"] <= counts["pram"]
    assert counts["linearizable"] > 0


def brute_force_sequential(h: History) -> bool:
    """Oracle: try every permutation."""
    for perm in itertools.permutations(range(len(h))):
        pos = {i: k for k, i in enumerate(perm)}
        if any(h[i].proc == h[j].proc and i < j and pos[i] > pos[j] for i in range(len(h)) for j in range(len(h))):
            continue
        vals = {"x": 0, "y": 0}
        ok = True
        for i in perm:
            if h[i].kind == "w":
                vals[h[i].var] = h[i].val
            elif vals[h[i].var] != h[i].val:
                ok = False
                break
        if ok:
            return True
    return False


def test_sequential_against_permutations() -> None:
    rng = random.Random(77)
    for _ in range(300):
        h = random_history(rng)
        assert is_sequential(h) == brute_force_sequential(h)


def test_causal_and_pram_on_eight_ops() -> None:
    # Eight operations, two registers: process 3 reads y = 1 and then x = 1,
    # which respects causality, so the history is causal and PRAM.
    h = [
        w(1, "x", 1), w(1, "x", 2),
        r(2, "x", 2), w(2, "y", 1),
        r(3, "y", 1), r(3, "x", 2),
        r(4, "x", 1), r(4, "x", 2),
    ]
    assert is_causal(h) and is_pram(h) and is_sequential(h)
    # Process 3 now sees x = 1 after y = 1, which breaks causality only.
    h2 = h[:5] + [r(3, "x", 1)] + h[6:]
    assert not is_causal(h2) and is_pram(h2)
