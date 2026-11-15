# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-slicing/. The authors are listed in prov/1V18D7.jsonl.
import random

import toyir
from dynamic_slicing import DEF, EXIT, REF, dynamic_slice, ipdom, statements

LOOP = """
# params: n, k
B0:
  i = 0
  s = 0
  p = 1
  jump B1
B1:
  c = i < n
  br c B2 B5
B2:
  d = i == k
  br d B3 B4
B3:
  s = s + i
  jump B4
B4:
  p = p * 2
  i = i + 1
  jump B1
B5:
  ret s
"""


# ------------------------------------------------- an independent recorder


def _eval(ins, env):
    def val(a):
        return a if isinstance(a, int) else env[a]

    if ins[0] == "const":
        return ins[2]
    if ins[0] == "copy":
        return val(ins[2])
    return toyir._binop(ins[2], val(ins[3]), val(ins[4]))


def _record(prog, args, fuel=10000):
    """Run prog and return the list of blocks it enters, in order, and the
    statement instances as (statement, index of its block visit)."""
    env = dict(zip(prog.params, args))
    blocks = []
    trace = []
    lab = prog.entry
    while fuel > 0:
        blocks.append(lab)
        b = prog.blocks[lab]
        for i, ins in enumerate(b.instrs):
            fuel -= 1
            trace.append(((lab, i), len(blocks) - 1))
            try:
                env[ins[1]] = _eval(ins, env)
            except toyir._Trap:
                return blocks, trace, "trap"
        fuel -= 1
        trace.append(((lab, len(b.instrs)), len(blocks) - 1))
        t = b.term
        if t[0] == "ret":
            return blocks, trace, "ret"
        if t[0] == "br":
            c = t[1] if isinstance(t[1], int) else env[t[1]]
            lab = t[2] if c != 0 else t[3]
        else:
            lab = t[1]
    return blocks, trace, "fuel"


def _reference(prog, args, crit):
    """Closure over the full graph of statement instances, built the naive
    way: for each instance, scan back for the last write of each name it
    reads and for the most recent branch instance whose ipdom block was not
    entered after it."""
    plab, pi, q, V = crit
    ip = ipdom(prog)
    blocks, trace, _ = _record(prog, args)
    occ = [k for k, (node, _) in enumerate(trace) if node == (plab, pi)]
    if len(occ) < q:
        return None
    target = occ[q - 1]

    def last_write(k, x):
        for j in range(k - 1, -1, -1):
            if x in DEF(prog, trace[j][0]):
                return j
        return None

    def ctrl(k):
        visit = trace[k][1]
        for j in range(k - 1, -1, -1):
            node, vj = trace[j]
            if node[1] == len(prog.blocks[node[0]].instrs) and prog.blocks[node[0]].term[0] == "br":
                if ip[node[0]] not in blocks[vj + 1 : visit + 1]:
                    return j
        return None

    def parents(k, names):
        out = {last_write(k, x) for x in names} | {ctrl(k)}
        return out - {None}

    roots = parents(target, V)
    seen = set(roots)
    stack = list(roots)
    while stack:
        k = stack.pop()
        for j in parents(k, REF(prog, trace[k][0])):
            if j not in seen:
                seen.add(j)
                stack.append(j)
    return {trace[k][0] for k in seen}


# --------------------------------------------------- an independent static slice


def _succ_stmts(prog, node):
    lab, i = node
    if i < len(prog.blocks[lab].instrs):
        return [(lab, i + 1)]
    return [(s, 0) for s in toyir.succs(prog, lab)]


def _postdominates(prog, y, x):
    """Every path from block x to the exit passes block y."""
    if x == y:
        return True
    seen = {x}
    stack = [x]
    while stack:
        a = stack.pop()
        nxt = toyir.succs(prog, a)
        if not nxt:
            return False
        for s in nxt:
            if s != y and s not in seen:
                seen.add(s)
                stack.append(s)
    return True


def _static_slice(prog, crit):
    plab, pi, _, V = crit

    def data_parents(n, names):
        out = set()
        for d in statements(prog):
            for x in DEF(prog, d) & names:
                seen = set()
                stack = list(_succ_stmts(prog, d))
                while stack:
                    m = stack.pop()
                    if m in seen:
                        continue
                    seen.add(m)
                    if m == n:
                        out.add(d)
                        break
                    if x not in DEF(prog, m):
                        stack.extend(_succ_stmts(prog, m))
        return out

    def control_parents(n):
        y = n[0]
        out = set()
        for x, b in prog.blocks.items():
            if b.term[0] != "br":
                continue
            strict = y != x and _postdominates(prog, y, x)
            if not strict and any(_postdominates(prog, y, s) for s in toyir.succs(prog, x)):
                out.add((x, len(b.instrs)))
        return out

    start = data_parents((plab, pi), set(V)) | control_parents((plab, pi))
    S = set(start)
    stack = list(start)
    while stack:
        n = stack.pop()
        for m in data_parents(n, REF(prog, n)) | control_parents(n):
            if m not in S:
                S.add(m)
                stack.append(m)
    return S


# ------------------------------------------------------- perturbed reruns


def _values_at(prog, args, crit, keep=None, rng=None):
    """Walk the blocks of the run on args, in the same order, and return the
    values of V at the criterion. If keep is given, every instruction outside
    keep writes a random value instead of its own, and every branch goes the
    way it went in the real run."""
    plab, pi, q, V = crit
    blocks, _, _ = _record(prog, args)
    env = dict(zip(prog.params, args))
    seen = 0
    for lab in blocks:
        b = prog.blocks[lab]
        for i in range(len(b.instrs) + 1):
            if (lab, i) == (plab, pi):
                seen += 1
                if seen == q:
                    return {x: env[x] for x in V if x in env}
            if i == len(b.instrs):
                break
            ins = b.instrs[i]
            if keep is not None and (lab, i) not in keep:
                env[ins[1]] = rng.randint(-50, 50)
                continue
            try:
                env[ins[1]] = _eval(ins, env)
            except toyir._Trap:
                # The real run did not trap here, so this instance read a
                # random value and is not one the criterion depends on.
                env[ins[1]] = rng.randint(-50, 50)
    return None


def _random_criterion(rng, prog):
    nodes = statements(prog)
    lab, i = rng.choice(nodes)
    names = sorted({v for n in nodes for v in DEF(prog, n)} | set(prog.params))
    q = rng.randint(1, 3)
    return (lab, i, q, set(rng.sample(names, rng.randint(1, min(2, len(names))))))


def _programs(seed, count):
    rng = random.Random(seed)
    for trial in range(count):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(2, 8), trial % 2 == 0)
        yield rng, prog


# ----------------------------------------------------------------- tests


def test_page_example():
    prog = toyir.parse(LOOP)
    crit = ("B5", 0, 1, {"s"})
    static = {("B0", 0), ("B0", 1), ("B1", 0), ("B1", 1), ("B2", 0), ("B2", 1), ("B3", 0), ("B4", 1)}
    assert _static_slice(prog, crit) == static
    assert toyir.run(prog, [3, 5]) == ("ret", 0)
    assert dynamic_slice(prog, [3, 5], crit) == {("B0", 1)}
    assert toyir.run(prog, [3, 1]) == ("ret", 1)
    assert dynamic_slice(prog, [3, 1], crit) == static
    assert dynamic_slice(prog, [0, 0], crit) == {("B0", 1)}
    # The test of i == k in the second turn of the loop, for input (3, 1).
    assert dynamic_slice(prog, [3, 1], ("B2", 1, 2, {"d"})) =={("B0", 0), ("B1", 0), ("B1", 1), ("B2", 0), ("B4", 1)}
    # The run reaches B3 only once.
    assert dynamic_slice(prog, [3, 1], ("B3", 0, 2, {"s"})) is None


def test_ipdom_matches_definition():
    for rng, prog in _programs(1, 200):
        ip = ipdom(prog)
        for x in prog.blocks:
            strict = [y for y in prog.blocks if y != x and _postdominates(prog, y, x)]
            if not strict:
                assert ip[x] == EXIT
            else:
                assert ip[x] in strict
                assert all(_postdominates(prog, y, ip[x]) for y in strict)


def test_matches_instance_graph():
    found = 0
    for rng, prog in _programs(2, 300):
        for _ in range(4):
            crit = _random_criterion(rng, prog)
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            got = dynamic_slice(prog, args, crit)
            want = _reference(prog, args, crit)
            if want is None:
                # The reference stops at the end of the run; a trap ends it too.
                assert got is None
            else:
                assert got == want
                found += 1
    assert found > 350


def test_slice_holds_for_its_input():
    checked = broken = 0
    for rng, prog in _programs(3, 300):
        for _ in range(3):
            crit = _random_criterion(rng, prog)
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            S = dynamic_slice(prog, args, crit)
            if S is None:
                continue
            want = _values_at(prog, args, crit)
            for _ in range(5):
                assert _values_at(prog, args, crit, S, rng) == want
            checked += 1
            # The test can fail: without one assignment of the slice, the
            # values often change.
            assigns = sorted(n for n in S if DEF(prog, n))
            if assigns:
                fewer = S - {rng.choice(assigns)}
                broken += any(_values_at(prog, args, crit, fewer, rng) != want for _ in range(5))
    assert checked > 200
    assert broken > 100


def test_slice_is_inside_static_slice_and_often_smaller():
    smaller = 0
    for rng, prog in _programs(4, 250):
        crit = _random_criterion(rng, prog)
        static = _static_slice(prog, crit)
        for _ in range(4):
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            S = dynamic_slice(prog, args, crit)
            if S is None:
                continue
            assert S <= static
            smaller += S < static
    assert smaller > 60


def test_slice_does_not_hold_for_another_input():
    prog = toyir.parse(LOOP)
    crit = ("B5", 0, 1, {"s"})
    S = dynamic_slice(prog, [3, 5], crit)
    rng = random.Random(6)
    want = _values_at(prog, [3, 1], crit)
    assert want == {"s": 1}
    got = [_values_at(prog, [3, 1], crit, S, rng) for _ in range(10)]
    assert any(g != want for g in got)
