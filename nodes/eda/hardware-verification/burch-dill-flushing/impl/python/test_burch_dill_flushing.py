# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burch-dill-flushing/. The authors are listed in prov/W76CN0.jsonl.

import random
from collections import deque
from itertools import product

from burch_dill_flushing import (OPS, Machine, Pipe, commuting_check, concrete_states, euf_check,
                                 term, word_alu)

BUGS = (None, "no-bypass", "bypass-rs1-only", "tag")


def test_euf_check_passes_on_the_correct_pipeline():
    for nregs in (1, 2, 3):
        assert euf_check(nregs) is None


def test_euf_check_finds_each_bug():
    q, i, left, right = euf_check(3, "no-bypass")
    rf, p = q
    assert p.valid and i is not None and p.rd in (i[2], i[3])
    q, i, left, right = euf_check(3, "bypass-rs1-only")
    assert q[1].valid and q[1].rd == i[3]
    # The tag design fails only on a state where the copy of rd is wrong.
    q, i, left, right = euf_check(3, "tag")
    assert q[1].valid and q[1].tag != q[1].rd


def test_example_of_the_page():
    # P holds ADD r1 <- pa + pb; the next instruction is ADD r2 <- r1 + r0.
    m = Machine(3, term, "z", "no-bypass")
    q = (("r0", "r1", "r2"), Pipe(True, "ADD", 1, 1, "pa", "pb"))
    ins = ("ADD", 2, 1, 0)
    left = m.abstraction(m.impl_step(q, ins))
    right = m.spec_step(m.abstraction(q), ins)
    assert right == ("r0", ("ADD", "pa", "pb"), ("ADD", ("ADD", "pa", "pb"), "r0"))
    assert left == ("r0", ("ADD", "pa", "pb"), ("ADD", "r1", "r0"))


def test_concrete_exhaustive_with_a_real_alu():
    for bug, ok in ((None, True), ("no-bypass", False), ("bypass-rs1-only", False), ("tag", False)):
        m = Machine(2, word_alu(2), 0, bug)
        res = commuting_check(m, concrete_states(m, 2), [None] + m.instructions())
        assert (res is None) == ok


def test_euf_pass_covers_every_alu():
    # A term-level pass holds for every interpretation of the ALU, here random tables.
    rng = random.Random(31)
    for _ in range(5):
        table = {(op, a, b): rng.randrange(2) for op in OPS for a in range(2) for b in range(2)}
        m = Machine(2, lambda op, a, b: table[(op, a, b)], 0)
        assert commuting_check(m, concrete_states(m, 1), [None] + m.instructions()) is None


# ---------------------------------------------------------------- the theorem by brute force

def reachable(m, width):
    """All implementation states reachable from an empty pipeline, by breadth-first search."""
    start = [(rf, m.bubble()) for rf in concrete_states_rf(m, width)]
    seen = set(start)
    todo = deque(start)
    inputs = [None] + m.instructions()
    while todo:
        q = todo.popleft()
        for i in inputs:
            q2 = m.impl_step(q, i)
            if q2 not in seen:
                seen.add(q2)
                todo.append(q2)
    return seen


def concrete_states_rf(m, width):
    return list(product(range(1 << width), repeat=m.nregs))


def flushed_runs_match(m, width):
    """Search the pairs (implementation state, ISA state) reachable together.

    Returns None when every run, flushed, ends in the ISA state of the fetched
    program, else a failing program.
    """
    inputs = [None] + m.instructions()
    start = [((rf, m.bubble()), rf) for rf in concrete_states_rf(m, width)]
    parent = {pair: None for pair in start}
    todo = deque(start)
    while todo:
        pair = todo.popleft()
        q, s = pair
        if m.abstraction(q) != s:
            prog = []
            while parent[pair] is not None:
                pair, i = parent[pair]
                prog.append(i)
            return pair[1], prog[::-1]
        for i in inputs:
            nxt = (m.impl_step(q, i), m.spec_step(s, i) if m.fetched(q, i) else s)
            if nxt not in parent:
                parent[nxt] = (pair, i)
                todo.append(nxt)
    return None


def run_program(m, rf, prog):
    q = (rf, m.bubble())
    s = rf
    for i in prog:
        if m.fetched(q, i):
            s = m.spec_step(s, i)
        q = m.impl_step(q, i)
    return m.flush(q)[0], s


def test_diagram_on_reachable_states_iff_all_flushed_runs_match():
    for bug in BUGS:
        m = Machine(2, word_alu(1), 0, bug)
        diagram = commuting_check(m, reachable(m, 1), [None] + m.instructions()) is None
        runs = flushed_runs_match(m, 1)
        assert diagram == (runs is None), bug
        if runs is not None:
            rf, prog = runs
            impl, isa = run_program(m, rf, prog)
            assert impl != isa                      # a real failing program
    # The tag design is correct on reachable states though the all-states check fails.
    m = Machine(2, word_alu(1), 0, "tag")
    assert flushed_runs_match(m, 1) is None


def test_random_programs_against_the_isa():
    rng = random.Random(2026)
    alu = word_alu(4)
    bad = 0
    for _ in range(600):
        nregs = rng.randint(1, 4)
        rf = tuple(rng.randrange(16) for _ in range(nregs))
        prog = []
        for _ in range(rng.randint(1, 8)):
            if rng.random() < 0.2:
                prog.append(None)
            else:
                prog.append((rng.choice(OPS), rng.randrange(nregs), rng.randrange(nregs), rng.randrange(nregs)))
        for bug in (None, "tag"):
            impl, isa = run_program(Machine(nregs, alu, 0, bug), rf, prog)
            assert impl == isa
        impl, isa = run_program(Machine(nregs, alu, 0, "no-bypass"), rf, prog)
        bad += impl != isa
    assert bad > 50
