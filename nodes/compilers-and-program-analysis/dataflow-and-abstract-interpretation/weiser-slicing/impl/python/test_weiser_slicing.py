# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiser-slicing/. The authors are listed in prov/S2FQ4Y.jsonl.

import random

import toyir
from weiser_slicing import (
    DEF,
    EXIT,
    REF,
    executable_slice,
    influence,
    ipdom,
    observe,
    relevant_sets,
    slice_point,
    statements,
    stmt_succs,
    weiser_slice,
)

# The sum and product program of the page.
PAGE = """
B1:
  i = 1
  s = 0
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  u = i % 2
  br u B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
"""

PAGE_SLICE = """# params: n
B1:
  i = 1
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  jump B5
B4:
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret 0
"""


def test_page_example():
    prog = toyir.parse(PAGE)
    crit = ("B6", 0, {"p"})
    res = weiser_slice(prog, crit)
    assert res["S"] == {("B1", 0), ("B1", 2), ("B2", 0), ("B2", 1), ("B3", 0), ("B5", 0)}
    assert res["B"] == {("B2", 1)}
    assert res["rounds"] == 2
    assert res["R"][("B1", 0)] == {"n"}
    assert res["R"][("B2", 1)] == {"i", "n", "p", "t"}
    sl = executable_slice(prog, crit, res)
    assert toyir.show(sl) == PAGE_SLICE
    point = slice_point(prog, crit, res["S"])
    for n in range(-2, 9):
        o1, ob1 = observe(prog, [n], ("B6", 0), ["p"])
        o2, ob2 = observe(sl, [n], point, ["p"])
        assert ob1 == ob2
    assert observe(prog, [5], ("B6", 0), ["p"])[1] == [(120,)]


def _random_criterion(rng, prog):
    nodes = statements(prog)
    lab, i = rng.choice(nodes)
    names = sorted({v for n in nodes for v in DEF(prog, n)})
    V = set(rng.sample(names, rng.randint(1, min(2, len(names)))))
    return (lab, i, V)


def test_slice_keeps_criterion_values():
    rng = random.Random(2024)
    runs = 0
    for trial in range(400):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), trial % 2 == 0)
        crit = _random_criterion(rng, prog)
        res = weiser_slice(prog, crit)
        nbr = sum(1 for b in prog.blocks.values() if b.term[0] == "br")
        assert res["rounds"] <= nbr + 1
        sl = executable_slice(prog, crit, res)
        point = slice_point(prog, crit, res["S"])
        names = sorted(crit[2])
        for _ in range(8):
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            o1, ob1 = observe(prog, args, crit[:2], names)
            assert o1 == toyir.run(prog, args)
            o2, ob2 = observe(sl, args, point, names)
            if o1[0] == "ret":
                assert ob2 == ob1
            else:
                # The original stopped early; the slice may go further.
                assert ob2[: len(ob1)] == ob1
            runs += 1
    assert runs == 3200


def _postdominates(prog, y, x):
    """y post-dominates x, by definition: every path from x to EXIT meets y."""
    if x == y:
        return True
    seen = {x}
    stack = [x]
    while stack:
        a = stack.pop()
        s = toyir.succs(prog, a)
        if not s:
            return False  # reached a ret, so EXIT, without meeting y
        for b in s:
            if b != y and b not in seen:
                seen.add(b)
                stack.append(b)
    return True


def test_influence_is_control_dependence_closure():
    rng = random.Random(7)
    for trial in range(300):
        prog = toyir.random_program(rng, 3, rng.randint(2, 8), trial % 3 == 0)
        ip = ipdom(prog)
        labels = list(prog.blocks)
        for x in labels:
            strict = {y for y in labels if y != x and _postdominates(prog, y, x)}
            if strict:
                assert ip[x] in strict
                assert all(_postdominates(prog, z, ip[x]) for z in strict)
            else:
                assert ip[x] == EXIT
        cd = {
            x: {
                y
                for y in labels
                for s in toyir.succs(prog, x)
                if _postdominates(prog, y, s) and not (y != x and _postdominates(prog, y, x))
            }
            for x in labels
        }
        for x in labels:
            if prog.blocks[x].term[0] != "br":
                continue
            closure = set(cd[x])
            stack = list(closure)
            while stack:
                y = stack.pop()
                for z in cd[y]:
                    if z not in closure:
                        closure.add(z)
                        stack.append(z)
            assert influence(prog, x, ip) == closure


def _control_deps(prog):
    """Block y is control dependent on block x, by the definition."""
    labels = list(prog.blocks)
    return {
        x: {
            y
            for y in labels
            for s in toyir.succs(prog, x)
            if _postdominates(prog, y, s) and not (y != x and _postdominates(prog, y, x))
        }
        for x in labels
    }


def _def_clear_reach(prog, start, x, target):
    """Some path from statement start to target has no definition of x
    before target (start itself is checked too)."""
    seen = set()
    stack = [start]
    while stack:
        n = stack.pop()
        if n == target:
            return True
        if n in seen or x in DEF(prog, n):
            continue
        seen.add(n)
        stack.extend(stmt_succs(prog, n))
    return False


def _dependence_slice(prog, crit):
    """The dependence slice of the page program-slicing, by its rules."""
    lab, i, V = crit
    nodes = statements(prog)
    cd = _control_deps(prog)
    parents = {}
    for n in nodes:
        ps = set()
        for s in nodes:
            d = DEF(prog, s)
            if d and d & REF(prog, n) and any(_def_clear_reach(prog, m, x, n) for x in d for m in stmt_succs(prog, s)):
                ps.add(s)
        for x in prog.blocks:
            if n[0] in cd[x]:
                ps.add((x, len(prog.blocks[x].instrs)))
        parents[n] = ps
    K = set()
    for s in nodes:
        d = DEF(prog, s)
        if d & V and any(_def_clear_reach(prog, m, x, (lab, i)) for x in d & V for m in stmt_succs(prog, s)):
            K.add(s)
    for x in prog.blocks:
        if lab in cd[x]:
            K.add((x, len(prog.blocks[x].instrs)))
    stack = list(K)
    while stack:
        n = stack.pop()
        for s in parents[n]:
            if s not in K:
                K.add(s)
                stack.append(s)
    return K


def test_weiser_slice_equals_dependence_slice():
    rng = random.Random(5)
    for trial in range(250):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(1, 7), trial % 2 == 0)
        crit = _random_criterion(rng, prog)
        assert weiser_slice(prog, crit)["S"] == _dependence_slice(prog, crit)


def test_relevant_sets_are_least_solution():
    rng = random.Random(11)
    for trial in range(200):
        prog = toyir.random_program(rng, 4, rng.randint(1, 7), trial % 2 == 1)
        nodes = statements(prog)
        seeds = {}
        for _ in range(rng.randint(1, 3)):
            lab, i, V = _random_criterion(rng, prog)
            seeds.setdefault((lab, i), set()).update(V)
        R = relevant_sets(prog, seeds)
        # Round-robin iteration from the seeds gives the least solution.
        L = {n: set(seeds.get(n, ())) for n in nodes}
        changed = True
        while changed:
            changed = False
            for n in nodes:
                new = set(L[n])
                for m in stmt_succs(prog, n):
                    new |= L[m] - DEF(prog, n)
                    if DEF(prog, n) & L[m]:
                        new |= REF(prog, n)
                if new != L[n]:
                    L[n] = new
                    changed = True
        assert R == L


def test_single_seed_union():
    # The equations are distributive: the solution for two seeds is the union.
    rng = random.Random(13)
    for trial in range(150):
        prog = toyir.random_program(rng, 4, rng.randint(1, 7), trial % 2 == 0)
        a, b = _random_criterion(rng, prog), _random_criterion(rng, prog)
        Ra = relevant_sets(prog, {a[:2]: a[2]})
        Rb = relevant_sets(prog, {b[:2]: b[2]})
        seeds = {a[:2]: set(a[2])}
        seeds.setdefault(b[:2], set()).update(b[2])
        Rab = relevant_sets(prog, seeds)
        assert all(Rab[n] == Ra[n] | Rb[n] for n in statements(prog))
