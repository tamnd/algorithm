# SPDX-License-Identifier: MIT
# Shared helper of the compilers and program analysis pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small object-oriented program model, for the call graph pages.

A program is a dict with these keys:

    "classes"  dict from each class name to its parent, None for the root.
    "methods"  dict from each method name m to (decl, ptype, rtype): the
               class that introduces m, the declared type of its parameter
               p and the declared type of its result.
    "fields"   dict from each field name f to (decl, ftype): the class that
               declares f and the declared type of f.
    "bodies"   dict from each method id (C, m), the method m as class C
               defines it, to (locals, stmts). The root is MAIN, a static
               method with no this, p or ret. locals maps each variable to
               its declared class. Every other body has the variables
               "this" (of type C), "p" and "ret" among its locals.

The statements are tuples:

    ("new", x, C)              x = new C()
    ("copy", x, y)             x = y
    ("load", x, y, f)          x = y.f
    ("store", y, f, z)         y.f = z
    ("call", s, x, y, m, z)    x = y.m(z) at call site s; x or z may be None

A method returns the value of its variable ret. The programs of
random_program are well typed in the sense of Java: a variable or field only
receives objects of its declared class or of a subclass, and a call y.m(z)
has decl(y) <= decl(m), so the dispatch always finds a method.

lookup(prog, C, m) is the method that runs for m on an object of class C.
run(prog, rng) runs the program concretely and returns the call edges and
the methods that the run saw. cha_spec and rta_spec are slow reference
versions of class hierarchy analysis and rapid type analysis: they apply
their rules to every reachable method, round after round, until nothing
changes.
"""

MAIN = ("Main", "main")


def is_sub(prog, c, d):
    """True if class c is d or a subclass of d."""
    while c is not None:
        if c == d:
            return True
        c = prog["classes"][c]
    return False


def subclasses(prog):
    """A dict from each class d to the set of classes c with c <= d."""
    below = {d: set() for d in prog["classes"]}
    for c in prog["classes"]:
        a = c
        while a is not None:
            below[a].add(c)
            a = prog["classes"][a]
    return below


def lookup(prog, c, m):
    """The method id that runs when m is called on an object of class c."""
    while c is not None:
        if (c, m) in prog["bodies"]:
            return (c, m)
        c = prog["classes"][c]
    raise KeyError(f"no method {m} above the class")


def call_sites(prog, mid):
    """The call statements of the body of mid."""
    return [st for st in prog["bodies"][mid][1] if st[0] == "call"]


def all_sites(prog):
    """A dict from each call site to (method id, statement)."""
    out = {}
    for mid, (_, stmts) in prog["bodies"].items():
        for st in stmts:
            if st[0] == "call":
                out[st[1]] = (mid, st)
    return out


def shapes():
    """The example of the call graph pages: Shape, Circle, Square, Oval."""
    S = "Shape"
    return {
        "classes": {S: None, "Circle": S, "Square": S, "Oval": "Circle"},
        "methods": {"grow": (S, S, S)},
        "fields": {},
        "bodies": {
            (S, "grow"): ({"this": S, "p": S, "ret": S}, [("copy", "ret", "this")]),
            ("Circle", "grow"): ({"this": "Circle", "p": S, "ret": S}, [("new", "ret", "Square")]),
            ("Square", "grow"): ({"this": "Square", "p": S, "ret": S}, [("copy", "ret", "this")]),
            MAIN: (
                {"a": S, "b": S, "c": S, "d": S, "e": S},
                [
                    ("new", "a", "Circle"),
                    ("new", "b", "Square"),
                    ("call", "s1", "c", "a", "grow", None),
                    ("call", "s2", "d", "b", "grow", None),
                    ("call", "s3", "e", "c", "grow", None),
                ],
            ),
        },
    }


def random_program(rng, nclasses=5, nmethods=3, nfields=2, nstmts=6):
    """A random well-typed program. rng is a random.Random."""
    names = ["K%d" % i for i in range(nclasses)]
    classes = {names[0]: None}
    for i in range(1, nclasses):
        classes[names[i]] = names[rng.randrange(i)]
    prog = {"classes": classes, "methods": {}, "fields": {}, "bodies": {}}
    below = subclasses(prog)
    for i in range(nmethods):
        prog["methods"]["m%d" % i] = (rng.choice(names), rng.choice(names), rng.choice(names))
    for i in range(nfields):
        prog["fields"]["f%d" % i] = (rng.choice(names), rng.choice(names))
    sites = [0]

    def body(this, ptype, rtype, count):
        local = {"v%d" % i: rng.choice(names) for i in range(3)}
        if this is not None:
            local.update({"this": this, "p": ptype, "ret": rtype})
        allv = list(local)
        dest = [v for v in allv if v != "this"]

        def sub_vars(t):
            return [v for v in allv if is_sub(prog, local[v], t)]

        def super_vars(t):
            return [v for v in dest if is_sub(prog, t, local[v])]

        stmts = []
        if this is None:  # main starts by making objects for two variables
            stmts = [("new", x, rng.choice(sorted(below[local[x]]))) for x in rng.sample(dest, 2)]
        while len(stmts) < count:
            kind = rng.choices(["new", "copy", "load", "store", "call"], (3, 3, 2, 2, 4))[0]
            if kind == "new":
                x = rng.choice(dest)
                stmts.append(("new", x, rng.choice(sorted(below[local[x]]))))
            elif kind == "copy":
                x = rng.choice(dest)
                ys = sub_vars(local[x])
                if ys:
                    stmts.append(("copy", x, rng.choice(ys)))
            elif kind in ("load", "store"):
                if not prog["fields"]:
                    continue
                f = rng.choice(sorted(prog["fields"]))
                fdecl, ftype = prog["fields"][f]
                ys = sub_vars(fdecl)
                if not ys:
                    continue
                if kind == "load":
                    xs = super_vars(ftype)
                    if xs:
                        stmts.append(("load", rng.choice(xs), rng.choice(ys), f))
                else:
                    zs = sub_vars(ftype)
                    if zs:
                        stmts.append(("store", rng.choice(ys), f, rng.choice(zs)))
            else:
                m = rng.choice(sorted(prog["methods"]))
                mdecl, pt, rt = prog["methods"][m]
                ys = sub_vars(mdecl)
                if not ys:
                    continue
                zs = sub_vars(pt)
                xs = super_vars(rt)
                z = rng.choice(zs) if zs and rng.random() < 0.8 else None
                x = rng.choice(xs) if xs and rng.random() < 0.8 else None
                sites[0] += 1
                stmts.append(("call", "s%d" % sites[0], x, rng.choice(ys), m, z))
        return local, stmts

    for m, (mdecl, pt, rt) in sorted(prog["methods"].items()):
        for c in sorted(below[mdecl]):
            if c == mdecl or rng.random() < 0.4:
                prog["bodies"][(c, m)] = body(c, pt, rt, rng.randint(1, nstmts))
    prog["bodies"][MAIN] = body(None, None, None, nstmts + 2)
    return prog


class _Stop(Exception):
    pass


def run(prog, rng, steps=300, depth=6, skip=0.25):
    """One concrete run from MAIN. Variables start as null. Each statement is
    skipped with probability skip, and each body runs once or twice, which
    stands for branches and loops. A call on null or a field access on null
    is skipped, as if the program caught the exception. Returns (edges,
    entered): the pairs (site, method id) that the run executed and the
    methods it entered."""
    heap = []
    edges, entered = set(), {MAIN}
    budget = [steps]

    def execute(mid, env, level):
        stmts = prog["bodies"][mid][1]
        for _ in range(rng.randint(1, 2)):
            for st in stmts:
                budget[0] -= 1
                if budget[0] < 0:
                    raise _Stop
                if rng.random() < skip:
                    continue
                kind = st[0]
                if kind == "new":
                    heap.append((st[2], {}))
                    env[st[1]] = len(heap) - 1
                elif kind == "copy":
                    env[st[1]] = env.get(st[2])
                elif kind == "load":
                    o = env.get(st[2])
                    if o is None:
                        continue
                    env[st[1]] = heap[o][1].get(st[3])
                elif kind == "store":
                    o = env.get(st[1])
                    if o is None:
                        continue
                    heap[o][1][st[2]] = env.get(st[3])
                else:
                    _, s, x, y, m, z = st
                    o = env.get(y)
                    if o is None:
                        continue
                    target = lookup(prog, heap[o][0], m)
                    edges.add((s, target))
                    entered.add(target)
                    result = None
                    if level < depth:
                        callee = {"this": o, "p": env.get(z) if z is not None else None}
                        execute(target, callee, level + 1)
                        result = callee.get("ret")
                    if x is not None:
                        env[x] = result

    try:
        execute(MAIN, {}, 0)
    except _Stop:
        pass
    return edges, entered


def _fixpoint(prog, targets):
    """The least (R, E) closed under: MAIN in R, and for each site s of a
    method of R and each T in targets(s, R), (s, T) in E and T in R."""
    reach, edges = {MAIN}, set()
    changed = True
    while changed:
        changed = False
        for mid in sorted(reach):
            for st in call_sites(prog, mid):
                for t in targets(mid, st, reach):
                    if (st[1], t) not in edges:
                        edges.add((st[1], t))
                        changed = True
                    if t not in reach:
                        reach.add(t)
                        changed = True
    return reach, edges


def cha_spec(prog):
    """Class hierarchy analysis by plain iteration."""

    def targets(mid, st, reach):
        decl = prog["bodies"][mid][0][st[3]]
        return {lookup(prog, c, st[4]) for c in prog["classes"] if is_sub(prog, c, decl)}

    return _fixpoint(prog, targets)


def rta_spec(prog):
    """Rapid type analysis by plain iteration."""

    def targets(mid, st, reach):
        made = {s[2] for r in reach for s in prog["bodies"][r][1] if s[0] == "new"}
        decl = prog["bodies"][mid][0][st[3]]
        return {lookup(prog, c, st[4]) for c in made if is_sub(prog, c, decl)}

    return _fixpoint(prog, targets)


def show(prog):
    """The program in a short text form, for messages of failed tests."""
    out = []
    for c, p in prog["classes"].items():
        out.append(f"class {c}" + (f" : {p}" if p else ""))
    for m, sig in prog["methods"].items():
        out.append(f"method {m} {sig}")
    for f, sig in prog["fields"].items():
        out.append(f"field {f} {sig}")
    for mid, (local, stmts) in prog["bodies"].items():
        out.append(f"{mid[0]}.{mid[1]} {local}")
        out.extend(f"  {st}" for st in stmts)
    return "\n".join(out)
