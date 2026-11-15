# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-scan-register-allocation/. The authors are listed in prov/5E24WB.jsonl.

import itertools
import random

import toyir
from linear_scan_register_allocation import (
    allocate,
    intervals,
    is_mem,
    linear_order,
    linear_scan,
    max_overlap,
    prepare,
)

DIAMOND = """# params: p
entry:
  a = p + 1
  br p B1 B2
B1:
  b = p * 2
  c = b + p
  ret c
B2:
  d = a - p
  ret d
"""


def brute_live(prog):
    """Liveness by search on the graph of single items: x is live before
    item n when some path from n reaches a use of x and no item before that
    use on the path defines x. This does not use the block fixed point."""
    order = linear_order(prog)
    first = {}
    for n, (label, _, _) in enumerate(order):
        first.setdefault(label, n)
    nxt = []
    for n, (label, item, is_term) in enumerate(order):
        nxt.append([first[s] for s in toyir.succs(prog, label)] if is_term else [n + 1])
    prv = [[] for _ in order]
    for n, ss in enumerate(nxt):
        for s in ss:
            prv[s].append(n)
    names = set()
    used = [set() for _ in order]
    defined = [None] * len(order)
    for n, (_, item, is_term) in enumerate(order):
        used[n] = set(toyir.term_uses(item) if is_term else toyir.uses(item))
        if not is_term:
            defined[n] = item[1]
        names |= used[n]
    live = [set() for _ in order]
    for x in names:
        work = [n for n in range(len(order)) if x in used[n]]
        seen = set(work)
        while work:
            v = work.pop()
            for p in prv[v]:
                if p not in seen and defined[p] != x:
                    seen.add(p)
                    work.append(p)
        for n in seen:
            live[n].add(x)
    return order, nxt, live


def check_registers(prog, k):
    """No two values that are live at the same time share a register, by the
    independent liveness above. Returns the number of spilled names."""
    work = prepare(prog)
    out, reg, spilled = allocate(prog, k)
    assert set(reg) | spilled == set(intervals(work))
    assert not (set(reg) & spilled)
    assert all(0 <= r < k for r in reg.values())
    order, nxt, live = brute_live(work)
    for n in range(len(order)):
        held = [reg[x] for x in live[n] if x in reg]
        assert len(held) == len(set(held)), (n, live[n])
        _, item, is_term = order[n]
        y = None if is_term else item[1]
        if y in reg:
            after = set().union(*(live[s] for s in nxt[n]))
            for x in after:
                if x != y and x in reg:
                    assert reg[x] != reg[y], (n, x, y)
    allowed = {"r%d" % i for i in range(k)} | {"s0", "s1"}
    for b in out.blocks.values():
        for ins in b.instrs:
            for a in [ins[1]] + toyir.uses(ins):
                assert a in allowed or is_mem(a), a
    return len(spilled)


def test_random_programs_keep_their_outputs():
    rng = random.Random(5)
    spills = 0
    for trial in range(250):
        prog = toyir.random_program(rng, rng.randint(2, 7), rng.randint(1, 7), acyclic=trial % 2 == 0)
        for k in (1, 2, 3, 5):
            spills += check_registers(prog, k)
            out, _, _ = allocate(prog, k)
            for _ in range(4):
                args = [rng.randint(-6, 6), rng.randint(-6, 6)]
                assert toyir.run(out, args, fuel=100000) == toyir.run(prog, args, fuel=100000)
    assert spills > 0


def test_registers_used_is_max_overlap():
    rng = random.Random(11)
    seen_no_spill = seen_spill = 0
    for trial in range(200):
        prog = toyir.random_program(rng, rng.randint(2, 7), rng.randint(1, 6), acyclic=trial % 3 != 0)
        iv = intervals(prepare(prog))
        m = max_overlap(iv)
        for k in range(1, 7):
            reg, spilled = linear_scan(iv, k)
            if m <= k:
                assert not spilled
                assert len(set(reg.values())) == m
                seen_no_spill += 1
            else:
                assert spilled
                seen_spill += 1
    assert seen_no_spill and seen_spill


def overlap_of(iv, keep):
    return max_overlap({x: iv[x] for x in keep}) if keep else 0


def test_spill_count_is_minimum_on_intervals():
    rng = random.Random(3)
    for trial in range(400):
        n = rng.randint(1, 8)
        iv = {}
        for i in range(n):
            s = rng.randint(0, 12)
            iv["v%d" % i] = (s, s + rng.randint(0, 8))
        for k in range(0, 4):
            reg, spilled = linear_scan(iv, k)
            keep = set(reg)
            assert overlap_of(iv, keep) <= k
            for a, b in itertools.combinations(sorted(keep), 2):
                if iv[a][0] <= iv[b][1] and iv[b][0] <= iv[a][1]:
                    assert reg[a] != reg[b]
            best = min(
                n - len(sub)
                for r in range(n + 1)
                for sub in itertools.combinations(sorted(iv), r)
                if overlap_of(iv, sub) <= k
            )
            assert len(spilled) == best, (iv, k, spilled, best)


def two_colorable(prog):
    """The interference graph of prog by the independent liveness, and an
    exhaustive check that two colors suffice."""
    order, nxt, live = brute_live(prog)
    names = sorted(set().union(*live) | {item[1] for _, item, t in order if not t})
    adj = {x: set() for x in names}
    for n, (_, item, is_term) in enumerate(order):
        if is_term:
            continue
        y = item[1]
        for x in set().union(*(live[s] for s in nxt[n])):
            if x != y:
                adj[x].add(y)
                adj[y].add(x)
    for colors in itertools.product(range(2), repeat=len(names)):
        c = dict(zip(names, colors))
        if all(c[a] != c[b] for a in adj for b in adj[a]):
            return adj, True
    return adj, False


def test_diamond_spills_although_two_colors_suffice():
    prog = toyir.parse(DIAMOND)
    iv = intervals(prog)
    assert iv == {"p": (0, 10), "a": (1, 10), "b": (5, 6), "c": (7, 8), "d": (11, 12)}
    assert max_overlap(iv) == 3
    reg, spilled = linear_scan(iv, 2)
    assert spilled == {"a"}
    adj, ok = two_colorable(prog)
    assert ok
    assert adj["a"] == {"p"} and adj["b"] == {"p"}
    out, _, spilled = allocate(prog, 2)
    assert spilled == {"a"}
    for p in range(-5, 6):
        assert toyir.run(out, [p]) == toyir.run(prog, [p])


def test_block_order_changes_the_result():
    # The same program with B2 placed before B1: now a ends before b starts.
    text = DIAMOND.replace("B1:\n  b = p * 2\n  c = b + p\n  ret c\n", "")
    text += "B1:\n  b = p * 2\n  c = b + p\n  ret c\n"
    prog = toyir.parse(text)
    iv = intervals(prog)
    assert max_overlap(iv) == 2
    reg, spilled = linear_scan(iv, 2)
    assert not spilled
