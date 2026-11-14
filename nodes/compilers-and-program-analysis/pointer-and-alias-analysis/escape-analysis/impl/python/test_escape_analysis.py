# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/escape-analysis/. The authors are listed in prov/JVVDBX.jsonl.

import random

from escape_analysis import ARG, GLOBAL, NONE, escape, points_to

PAGE = {
    "main": ([], [
        ("new", "a", "s1"),
        ("new", "b", "s2"),
        ("store", "a", "f", "b"),
        ("call", "c", "make", []),
        ("new", "t", "s3"),
        ("start", "worker", ["t"]),
    ]),
    "make": ([], [
        ("new", "d", "s4"),
        ("new", "e", "s5"),
        ("store", "d", "f", "e"),
        ("new", "w", "s6"),
        ("store", "w", "f", "d"),
        ("ret", "d"),
    ]),
    "worker": (["p"], [
        ("new", "q", "s7"),
        ("store", "p", "f", "q"),
        ("new", "r", "s8"),
        ("gstore", "G", "r"),
    ]),
}


def test_page_example():
    assert escape(PAGE) == {
        "s1": NONE, "s2": NONE, "s3": GLOBAL, "s4": ARG,
        "s5": ARG, "s6": NONE, "s7": GLOBAL, "s8": GLOBAL,
    }


def test_storing_into_a_parameter_escapes_to_the_caller():
    prog = {
        "main": ([], [("new", "a", "s1"), ("call", "x", "fill", ["a"])]),
        "fill": (["p"], [("new", "q", "s2"), ("store", "p", "f", "q")]),
    }
    assert escape(prog) == {"s1": NONE, "s2": ARG}


def test_passing_to_a_callee_that_keeps_it_local_does_not_escape():
    prog = {
        "main": ([], [("new", "a", "s1"), ("call", "x", "use", ["a"])]),
        "use": (["p"], [("load", "y", "p", "f")]),
    }
    assert escape(prog) == {"s1": NONE}


def test_reading_a_global_and_writing_into_it():
    prog = {
        "main": ([], [("gload", "x", "G"), ("new", "a", "s1"), ("store", "x", "f", "a")]),
        "init": ([], [("new", "b", "s2"), ("gstore", "G", "b")]),
    }
    assert escape(prog) == {"s1": GLOBAL, "s2": GLOBAL}


def test_recursion_that_passes_its_object_on():
    prog = {"main": (["p"], [("new", "a", "s1"), ("call", "x", "main", ["a"])])}
    assert escape(prog) == {"s1": ARG}


# Random programs and a concrete interpreter with threads.

FIELDS = ["f0", "f1"]
GLOBALS = ["G0", "G1"]
LOCALS = ["l0", "l1", "l2"]


def random_program(rng, nmethods, nstmts):
    methods = ["m%d" % i for i in range(nmethods)]
    params = {m: ["p%d" % j for j in range(0 if m == "m0" else rng.randint(0, 2))] for m in methods}
    kinds = ["new", "copy", "load", "store", "gload", "gstore", "call", "start", "ret"]
    weights = [4, 2, 2, 3, 1, 1, 3, 1, 2]
    site = 0
    prog = {}
    for m in methods:
        names = params[m] + LOCALS
        body = []
        for x in LOCALS:
            site += 1
            body.append(("new", x, "s%d" % site))
        for _ in range(nstmts):
            kind = rng.choices(kinds, weights)[0]
            if kind == "new":
                site += 1
                body.append(("new", rng.choice(LOCALS), "s%d" % site))
            elif kind == "copy":
                body.append(("copy", rng.choice(LOCALS), rng.choice(names)))
            elif kind == "load":
                body.append(("load", rng.choice(LOCALS), rng.choice(names), rng.choice(FIELDS)))
            elif kind == "store":
                x = rng.choice(params[m] if params[m] and rng.random() < 0.5 else names)
                body.append(("store", x, rng.choice(FIELDS), rng.choice(names)))
            elif kind == "gload":
                body.append(("gload", rng.choice(LOCALS), rng.choice(GLOBALS)))
            elif kind == "gstore":
                body.append(("gstore", rng.choice(GLOBALS), rng.choice(names)))
            elif kind in ("call", "start"):
                callee = rng.choice(methods)
                args = [rng.choice(names) for _ in params[callee]]
                if kind == "call":
                    body.append(("call", rng.choice(LOCALS), callee, args))
                else:
                    body.append(("start", callee, args))
            else:
                body.append(("ret", rng.choice(names)))
        prog[m] = (params[m], body)
    return prog


class Frame:
    def __init__(self, method, env, dest, ident):
        self.method, self.env, self.dest, self.ident = method, env, dest, ident
        self.pc = 0
        self.ret = None


def reach(heap, start):
    seen = set()
    stack = [o for o in start if o is not None]
    while stack:
        o = stack.pop()
        if o in seen:
            continue
        seen.add(o)
        stack.extend(v for v in heap[o].values() if v is not None)
    return seen


def frame_roots(fr):
    return list(fr.env.values()) + [fr.ret]


def run_and_check(prog, state, pts, rng, steps=120, max_depth=4, max_threads=3):
    """Run the program from m0 with random interleaving of threads, and skip
    each statement with probability 0.2, which models a branch. After every
    step, check the escape claims and that the heap matches pts."""
    heap, glob, made = {}, {}, {}
    threads = [[Frame("m0", {}, None, 0)]]
    idents = 1
    checked = 0
    for _ in range(steps):
        live = [t for t in range(len(threads)) if threads[t]]
        if not live:
            break
        t = rng.choice(live)
        stack = threads[t]
        fr = stack[-1]
        params, body = prog[fr.method]
        if fr.pc == len(body):
            stack.pop()
            if stack and fr.dest is not None:
                stack[-1].env[fr.dest] = fr.ret
        else:
            st = body[fr.pc]
            fr.pc += 1
            env = fr.env
            kind = st[0]
            if rng.random() < 0.2:
                pass
            elif kind == "new":
                o = len(heap)
                heap[o] = {}
                made[o] = (st[2], t, fr.ident)
                env[st[1]] = o
            elif kind == "copy":
                env[st[1]] = env.get(st[2])
            elif kind == "load":
                if env.get(st[2]) is not None:
                    env[st[1]] = heap[env[st[2]]].get(st[3])
            elif kind == "store":
                if env.get(st[1]) is not None:
                    heap[env[st[1]]][st[2]] = env.get(st[3])
            elif kind == "gload":
                env[st[1]] = glob.get(st[2])
            elif kind == "gstore":
                glob[st[1]] = env.get(st[2])
            elif kind == "call":
                if len(stack) < max_depth:
                    cparams = prog[st[2]][0]
                    stack.append(Frame(st[2], {p: env.get(a) for p, a in zip(cparams, st[3])}, st[1], idents))
                    idents += 1
            elif kind == "start":
                if len(threads) < max_threads:
                    cparams = prog[st[1]][0]
                    threads.append([Frame(st[1], {p: env.get(a) for p, a in zip(cparams, st[2])}, None, idents)])
                    idents += 1
            else:
                fr.ret = env.get(st[1])
        checked += check(prog, state, pts, heap, glob, made, threads)
    return checked


def check(prog, state, pts, heap, glob, made, threads):
    from_globals = reach(heap, glob.values())
    per_frame = [[reach(heap, frame_roots(fr)) for fr in stack] for stack in threads]
    # The heap and the variables are inside the points-to result.
    for o, fields in heap.items():
        for f, v in fields.items():
            if v is not None:
                assert made[v][0] in pts[("f", made[o][0], f)]
    for stack in threads:
        for fr in stack:
            for x, v in fr.env.items():
                if v is not None:
                    assert made[v][0] in pts[("v", fr.method, x)]
    count = 0
    for o, (site, t, ident) in made.items():
        if state[site] != GLOBAL:
            assert o not in from_globals, site
            for u, frames in enumerate(per_frame):
                if u != t:
                    assert all(o not in r for r in frames), site
            count += 1
        if state[site] == NONE:
            idents = [fr.ident for fr in threads[t]]
            below = idents.index(ident) if ident in idents else len(idents)
            assert all(o not in r for r in per_frame[t][:below]), site
            count += 1
    return count


def test_escape_claims_hold_on_concrete_runs():
    rng = random.Random(2024)
    checked = 0
    kinds = {NONE: 0, ARG: 0, GLOBAL: 0}
    for _ in range(250):
        prog = random_program(rng, rng.randint(1, 4), rng.randint(2, 9))
        state = escape(prog)
        pts = points_to(prog)
        for s in state.values():
            kinds[s] += 1
        for _ in range(3):
            checked += run_and_check(prog, state, pts, rng)
    assert checked > 5000
    assert min(kinds.values()) > 50


def test_a_returned_none_object_is_garbage():
    """After the activation that made a NONE object returns, no root reaches
    the object, so it could have lived in that activation's stack frame."""
    prog = {
        "m0": ([], [("call", "x", "m1", []), ("new", "y", "s9")]),
        "m1": ([], [("new", "a", "s1"), ("new", "b", "s2"), ("store", "a", "f0", "b"), ("ret", "b")]),
    }
    state = escape(prog)
    assert state["s1"] == NONE and state["s2"] == ARG
    rng = random.Random(7)
    assert run_and_check(prog, state, points_to(prog), rng, steps=30) > 0
