# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interprocedural-constant-propagation/. The authors are listed in prov/D7W565.jsonl.
import random

import toyir
import interprocedural_constant_propagation as I

PAGE = {
    "main": """# params: n
B0:
  w = 4
  a = call scale(n, w)
  b = call scale(a, 4)
  c = call count(0, 5)
  d = b + c
  ret d
""",
    "scale": """# params: x, k
B0:
  t = call mul(x, k)
  ret t
""",
    "mul": """# params: u, v
B0:
  t = u * v
  ret t
""",
    "count": """# params: i, lim
B0:
  c = i < lim
  br c B1 B2
B1:
  j = i + 1
  r = call count(j, lim)
  ret r
B2:
  ret i
""",
}

PAGE_COUNT_AFTER = """# params: i, lim
ipcp.entry:
  lim = 5
  jump B0
B0:
  c = i < lim
  br c B1 B2
B1:
  j = i + 1
  r = call count(j, lim)
  ret r
B2:
  ret i
"""

FUEL = 20000  # the random runs below finish in under 3000 steps


def parse_all(texts):
    return {f: toyir.parse(t) for f, t in texts.items()}


def outcome(procs, args, fuel=FUEL):
    return toyir.run(procs["main"], args, fuel=fuel, funcs=procs)


def with_checks(procs, val):
    """A copy of procs where each procedure first tests every claimed
    constant formal and spins forever if one of them is wrong."""
    out = {}
    for f, prog in procs.items():
        consts = [(p, v[1]) for p, v in val[f].items() if v[0] == "const"]
        if not consts:
            out[f] = prog
            continue
        instrs = [("const", "chk.ok", 1)]
        for i, (p, k) in enumerate(consts):
            instrs.append(("op", "chk.t%d" % i, "==", p, k))
            instrs.append(("op", "chk.ok", "&", "chk.ok", "chk.t%d" % i))
        blocks = {
            "chk.entry": toyir.Block(instrs, ("br", "chk.ok", prog.entry, "chk.spin")),
            "chk.spin": toyir.Block([], ("jump", "chk.spin")),
        }
        blocks.update(prog.blocks)
        out[f] = toyir.Program(list(prog.params), blocks)
    return out


def random_procs(rng, recursive):
    """Procedures main, P1, P2, P3 with the formals x0 and x1. A procedure
    calls only later ones, so the call graph is acyclic, except that with
    recursive=True some procedures also call themselves under a depth test
    on x0 that allows at most 3 nested self calls."""
    names = ["main", "P1", "P2", "P3"]
    procs = {}
    ncalls = 0
    for i, f in enumerate(names):
        nvars = rng.randint(2, 4)
        prog = toyir.random_program(rng, nvars, rng.randint(1, 4), rng.random() < 0.5)
        xs = ["x%d" % j for j in range(nvars)]
        later = names[i + 1:]
        for _ in range(rng.randint(1, 2) if later else 0):
            g = rng.choice(later)
            blk = prog.blocks[rng.choice(list(prog.blocks))]
            args = []
            for _ in range(2):
                r = rng.random()
                if r < 0.35:
                    args.append(rng.choice((2, 2, 3)))
                elif r < 0.5:
                    k = "k%d" % ncalls
                    ncalls += 1
                    blk.instrs.append(("const", k, rng.choice((2, 3))))
                    args.append(k)
                elif r < 0.8:
                    args.append(rng.choice(prog.params))
                else:
                    args.append(rng.choice(xs))
            blk.instrs.append(("call", rng.choice(xs), g, args))
        if recursive and i > 0 and rng.random() < 0.6:
            arg = rng.choice(("x1", "x1", 2, 3))
            dest = rng.choice(("rec.r", "x1"))
            blocks = {
                "R0": toyir.Block(
                    [("op", "rec.a", "<", 0, "x0"), ("op", "rec.b", "<", "x0", 4), ("op", "rec.g", "&", "rec.a", "rec.b")],
                    ("br", "rec.g", "R1", prog.entry),
                ),
                "R1": toyir.Block([("op", "rec.d", "-", "x0", 1), ("call", dest, f, ["rec.d", arg])], ("jump", prog.entry)),
            }
            blocks.update(prog.blocks)
            prog = toyir.Program(prog.params, blocks)
        procs[f] = prog
    return procs


def cases(seed, n, recursive):
    rng = random.Random(seed)
    for _ in range(n):
        procs = random_procs(rng, recursive)
        inputs = [[rng.randint(-4, 6), rng.choice((2, 3, rng.randint(-4, 6)))] for _ in range(4)]
        yield procs, inputs


def test_page_example():
    procs = parse_all(PAGE)
    sites = {f: I.jump_functions(p) for f, p in procs.items()}
    shown = {f: [[I.show_value(j) for j in s[3]] for s in sites[f]] for f in sites}
    assert shown == {
        "main": [["n", "4"], ["⊥", "4"], ["0", "5"]],
        "scale": [["x", "k"]],
        "mul": [],
        "count": [["⊥", "lim"]],
    }
    val, out = I.ipcp(procs)
    shown = {f: {p: I.show_value(v) for p, v in val[f].items()} for f in val}
    assert shown == {
        "main": {"n": "⊥"},
        "scale": {"x": "⊥", "k": "4"},
        "mul": {"u": "⊥", "v": "4"},
        "count": {"i": "⊥", "lim": "5"},
    }
    assert toyir.show(out["count"]) == PAGE_COUNT_AFTER
    assert toyir.show(out["main"]) == toyir.show(procs["main"])
    for n in range(-5, 8):
        assert outcome(out, [n]) == outcome(procs, [n])
    assert outcome(procs, [3]) == ("ret", 53)


def test_jump_functions_follow_the_local_values():
    procs = parse_all({
        "main": """# params: a, b
B0:
  c = a
  a = 1
  br b B1 B2
B1:
  d = 7
  e = b
  jump B3
B2:
  d = 7
  e = 5
  jump B3
B3:
  f = d * 2
  g = a + c
  r = call h(c, a, d, e, f, g)
  ret r
B4:
  s = call h(1, 1, 1, 1, 1, 1)
  ret s
""",
        "h": """# params: p, q, r, s, t, u
B0:
  ret p
""",
    })
    sites = I.jump_functions(procs["main"])
    assert len(sites) == 1  # B4 is not reachable
    assert [I.show_value(j) for j in sites[0][3]] == ["a", "1", "7", "⊥", "14", "⊥"]


def test_claims_hold_on_every_call():
    """Each procedure checks its claimed constants on entry and spins if one
    is wrong, so a false claim turns a finished run into a run out of fuel."""
    claimed = 0
    for recursive in (False, True):
        for procs, inputs in cases(11 + recursive, 250, recursive):
            val, _ = I.ipcp(procs)
            claimed += sum(v[0] == "const" for f in val for v in val[f].values())
            checked = with_checks(procs, val)
            for args in inputs:
                before = outcome(procs, args)
                if before == ("fuel",):
                    continue
                assert outcome(checked, args, fuel=4 * FUEL) == before
    assert claimed > 100


def test_checks_catch_a_wrong_claim():
    """The check in the test above has teeth: claiming k + 1 instead of k
    makes most runs that call the procedure spin."""
    caught = total = 0
    for procs, inputs in cases(5, 60, True):
        val, _ = I.ipcp(procs)
        bad = {f: {p: ("const", v[1] + 1) if v[0] == "const" else v for p, v in val[f].items()} for f in val}
        if bad == val:
            continue
        checked = with_checks(procs, bad)
        for args in inputs:
            total += 1
            caught += outcome(checked, args, fuel=6000) == ("fuel",)
    assert total > 50 and caught > total // 2


def test_same_outcome_on_random_programs():
    changed = 0
    for recursive in (False, True):
        for procs, inputs in cases(23 + recursive, 250, recursive):
            _, out = I.ipcp(procs)
            changed += sum(toyir.show(out[f]) != toyir.show(procs[f]) for f in procs)
            for args in inputs:
                before = outcome(procs, args)
                if before == ("fuel",):
                    continue
                assert outcome(out, args, fuel=4 * FUEL) == before
    assert changed > 100


def test_worklist_matches_one_pass_in_call_order():
    """Without recursion every caller comes before its callees in the list
    main, P1, P2, P3, so one pass in that order gives the final values."""
    for procs, _ in cases(37, 300, False):
        val, _ = I.ipcp(procs)
        ref = {f: {p: I.TOP for p in prog.params} for f, prog in procs.items()}
        ref["main"] = {p: I.BOT for p in procs["main"].params}
        reached = {"main"}
        for f in ("main", "P1", "P2", "P3"):
            if f not in reached:
                continue
            for _, _, g, jumps in I.jump_functions(procs[f]):
                reached.add(g)
                for p, j in zip(procs[g].params, jumps):
                    ref[g][p] = I.meet(ref[g][p], I.evaluate(j, ref[f]))
        assert val == ref


def test_unreached_procedure_stays_top_and_unchanged():
    procs = parse_all({
        "main": """# params: n
B0:
  ret n
""",
        "lost": """# params: a
B0:
  r = call leaf(3)
  ret r
""",
        "leaf": """# params: b
B0:
  ret b
""",
    })
    val, out = I.ipcp(procs)
    assert val["lost"] == {"a": I.TOP}
    assert val["leaf"] == {"b": I.TOP}
    assert all(toyir.show(out[f]) == toyir.show(procs[f]) for f in procs)


def test_recursion_through_a_changed_argument_is_not_constant():
    procs = parse_all({
        "main": """# params: n
B0:
  r = call down(3, 2)
  ret r
""",
        "down": """# params: d, k
B0:
  c = 0 < d
  br c B1 B2
B1:
  e = d - 1
  k2 = k + 0
  r = call down(e, k2)
  ret r
B2:
  ret k
""",
    })
    val, _ = I.ipcp(procs)
    # k + 0 is not a pass-through jump function, so k becomes BOT.
    assert val["down"] == {"d": I.BOT, "k": I.BOT}
