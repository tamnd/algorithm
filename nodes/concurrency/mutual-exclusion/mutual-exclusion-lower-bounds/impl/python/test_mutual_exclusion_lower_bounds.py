# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-lower-bounds/. The authors are listed in prov/44E0B1.jsonl.
import random

from mutual_exclusion_lower_bounds import can_both_enter, covering_run, replay


def read(reg, f):
    return ("r", reg, f)


def write(reg, v, pc):
    return ("w", reg, v, pc)


# One register x. Each process waits for x = 0, then writes its name.
def check_then_set(i, pc):
    return [read("x", lambda v: 1 if v == 0 else 0), write("x", i + 1, 2), ("cs",)][pc]


# Fischer's algorithm without the delay: wait for x = 0, write the name, check it.
def fischer_no_delay(i, pc):
    return [read("x", lambda v: 1 if v == 0 else 0), write("x", i + 1, 2),
            read("x", lambda v: 3 if v == i + 1 else 0), ("cs",)][pc]


# Write the name first, then check it.
def write_then_check(i, pc):
    return [write("x", i + 1, 1), read("x", lambda v: 2 if v == i + 1 else 0), ("cs",)][pc]


# Strict alternation on one register: process i waits until x = i. Not deadlock free.
def alternation(i, pc):
    return [read("x", lambda v: 1 if v == i else 0), ("cs",)][pc]


# The Burns-Lamport algorithm for two processes: two one-bit registers b0 and b1.
def burns_lamport(i, pc):
    if i == 0:
        return [write("b0", 1, 1), read("b1", lambda v: 2 if v == 0 else 1), ("cs",)][pc]
    return [write("b1", 1, 1), read("b0", lambda v: 2 if v == 1 else 3), write("b1", 0, 4),
            ("cs",), read("b0", lambda v: 0 if v == 0 else 4)][pc]


# Peterson's algorithm for two processes: flag0, flag1 and turn.
def peterson(i, pc):
    j = 1 - i
    return [write(f"flag{i}", 1, 1), write("turn", i, 2),
            read(f"flag{j}", lambda v: 4 if v == 0 else 3),
            read("turn", lambda v: 4 if v != i else 2), ("cs",)][pc]


ONE = {"x": 0}


def test_covering_run_of_the_page():
    # The example of the page: p reads x = 0 and covers x; q enters alone; p writes and enters.
    r = covering_run(fischer_no_delay, ONE)
    assert r["result"] == "violation" and r["covered"] == "x"
    assert r["run"] == [0, 1, 1, 1, 0, 0]
    pcs, mem = replay(fischer_no_delay, ONE, r["run"])
    assert pcs == (3, 3) and mem == {"x": 1}


def test_one_register_candidates_fail():
    for alg in (check_then_set, fischer_no_delay, write_then_check):
        r = covering_run(alg, ONE)
        assert r["result"] == "violation", alg.__name__
        pcs, _ = replay(alg, ONE, r["run"])
        assert all(alg(i, pcs[i]) == ("cs",) for i in (0, 1))
        assert can_both_enter(alg, ONE)


def test_not_deadlock_free_is_outside_the_theorem():
    # Process 0 enters without a write, but process 1 alone never enters.
    r = covering_run(alternation, ONE)
    assert r["result"] == "q alone does not enter"
    assert not can_both_enter(alternation, ONE)


def test_two_register_algorithms_escape():
    # In a correct algorithm, q must write a register that p does not cover.
    r = covering_run(burns_lamport, {"b0": 0, "b1": 0})
    assert r == {"result": "escape", "covered": "b0", "q_writes": {"b1"}}
    assert not can_both_enter(burns_lamport, {"b0": 0, "b1": 0})
    r = covering_run(peterson, {"flag0": 0, "flag1": 0, "turn": 0})
    assert r["result"] == "escape" and r["covered"] == "flag0" and r["q_writes"] == {"flag1", "turn"}
    assert not can_both_enter(peterson, {"flag0": 0, "flag1": 0, "turn": 0})


def random_program(rng, k):
    # States 0 to k - 1; the state k is the critical section. Values 0, 1, 2; the name of i is i + 1.
    table = []
    for _ in range(k):
        if rng.random() < 0.5:
            table.append(("r", tuple(rng.randrange(k + 1) for _ in range(3))))
        else:
            table.append(("w", rng.choice([0, 1, 2, "name"]), rng.randrange(k + 1)))

    def act(i, pc):
        if pc == k:
            return ("cs",)
        t = table[pc]
        if t[0] == "r":
            return ("r", "x", lambda v: t[1][v])
        return ("w", "x", i + 1 if t[1] == "name" else t[1], t[2])

    return act


def test_every_one_register_program_fails():
    # The theorem for n = 2 on 600 random one-register programs: each one is not
    # deadlock free alone, or the covering run puts both processes in the CS.
    rng = random.Random(44)
    seen = {"violation": 0, "p alone does not enter": 0, "q alone does not enter": 0}
    for _ in range(600):
        alg = random_program(rng, rng.randint(1, 4))
        r = covering_run(alg, ONE)
        seen[r["result"]] += 1
        if r["result"] == "violation":
            pcs, _ = replay(alg, ONE, r["run"])
            assert all(alg(i, pcs[i]) == ("cs",) for i in (0, 1))
            assert can_both_enter(alg, ONE)
    assert all(c > 0 for c in seen.values())
