# SPDX-License-Identifier: MIT
# Shared helper of the compilers and program analysis pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Points-to constraints in the four basic forms, for the pointer analysis pages.

A program is a list of statements. Each statement is a tuple with the same
shape as the pointer instructions of the toy IR (toyir.py):

    ("addr", p, a)    p = &a
    ("copy", p, q)    p = q
    ("load", p, q)    p = *q
    ("store", p, q)   *p = q

Every name is a pointer variable, and every variable is also a memory
location whose address the program may take. A points-to solution is a dict
from each variable to a set of variables. The order of the statements does
not matter to a flow-insensitive analysis.

parse(text) and show(stmts) convert to and from the toy IR notation.
random_program(rng, nvars, nstmts) builds a random program.
least_solution(stmts) is a slow reference: it applies the four rules to
every statement, round after round, until nothing changes.
is_solution(stmts, pts) checks that pts meets every constraint.
concrete_facts(stmts, rng, runs, steps) runs the program concretely, with
the statements in random order, and returns the facts (p, a) that some run
saw: p held the address of a.
"""

import re

_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
_FORMS = [
    ("addr", re.compile(r"(%s) = &(%s)" % (_NAME, _NAME))),
    ("load", re.compile(r"(%s) = \*(%s)" % (_NAME, _NAME))),
    ("store", re.compile(r"\*(%s) = (%s)" % (_NAME, _NAME))),
    ("copy", re.compile(r"(%s) = (%s)" % (_NAME, _NAME))),
]


def parse(text):
    """Parse lines such as "p = &a", "p = q", "p = *q" and "*p = q".
    The k-th "p = alloc" becomes "p = &hk", one location per allocation
    site. Blank lines, lines that start with #, block labels and the
    terminators jump, br and ret are skipped, so a toy IR program with only
    pointer instructions can be read as it is. A flow-insensitive analysis
    ignores the order of the statements, so the blocks do not matter."""
    stmts = []
    sites = 0
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if not line or line.startswith("#") or line.endswith(":"):
            continue
        if line.split()[0] in ("jump", "br", "ret"):
            continue
        m = re.fullmatch(r"(%s) = alloc" % _NAME, line)
        if m:
            sites += 1
            stmts.append(("addr", m.group(1), "h%d" % sites))
            continue
        for kind, rx in _FORMS:
            m = rx.fullmatch(line)
            if m:
                stmts.append((kind, m.group(1), m.group(2)))
                break
        else:
            raise ValueError("not a pointer statement: %r" % raw)
    return stmts


def show(stmts):
    out = []
    for kind, x, y in stmts:
        if kind == "addr":
            out.append("%s = &%s" % (x, y))
        elif kind == "copy":
            out.append("%s = %s" % (x, y))
        elif kind == "load":
            out.append("%s = *%s" % (x, y))
        else:
            out.append("*%s = %s" % (x, y))
    return "\n".join(out)


def variables(stmts):
    """All names, in the order of their first use."""
    seen = {}
    for _, x, y in stmts:
        seen.setdefault(x, None)
        seen.setdefault(y, None)
    return list(seen)


def random_program(rng, nvars=8, nstmts=30, weights=(3, 4, 2, 2)):
    """A random list of nstmts statements over the names v0 .. v(nvars-1).
    weights gives the relative number of addr, copy, load and store forms."""
    names = ["v%d" % i for i in range(nvars)]
    kinds = ["addr", "copy", "load", "store"]
    return [
        (rng.choices(kinds, weights)[0], rng.choice(names), rng.choice(names))
        for _ in range(nstmts)
    ]


def least_solution(stmts):
    """The least solution of the inclusion constraints, by plain iteration."""
    pts = {v: set() for v in variables(stmts)}
    changed = True
    while changed:
        changed = False
        for kind, x, y in stmts:
            if kind == "addr":
                new = {y}
                targets = [x]
            elif kind == "copy":
                new = pts[y]
                targets = [x]
            elif kind == "load":
                new = set()
                for a in pts[y]:
                    new |= pts[a]
                targets = [x]
            else:
                new = pts[y]
                targets = list(pts[x])
            for t in targets:
                if not new <= pts[t]:
                    pts[t] |= new
                    changed = True
    return pts


def is_solution(stmts, pts):
    """True if pts satisfies every constraint of stmts."""
    for kind, x, y in stmts:
        if kind == "addr" and y not in pts[x]:
            return False
        if kind == "copy" and not pts[y] <= pts[x]:
            return False
        if kind == "load" and any(not pts[a] <= pts[x] for a in pts[y]):
            return False
        if kind == "store" and any(not pts[y] <= pts[a] for a in pts[x]):
            return False
    return True


def concrete_facts(stmts, rng, runs=20, steps=120):
    """Run the program concretely. Each variable holds no value at the start.
    A run is a sequence of statements in any order, with repeats, which is the
    semantics that a flow-insensitive analysis must cover; every path of a
    real control flow graph over these statements is such a sequence. A
    statement that reads a variable with no value, or goes through one,
    cannot run, so the run picks another. Returns the set of pairs (p, a)
    such that p held the address of a at some moment of some run."""
    seen = set()
    for _ in range(runs):
        val = {v: None for v in variables(stmts)}
        for _ in range(steps):
            kind, x, y = stmts[rng.randrange(len(stmts))]
            if kind == "addr":
                val[x] = y
                dst = x
            elif kind == "copy":
                if val[y] is None:
                    continue
                val[x] = val[y]
                dst = x
            elif kind == "load":
                if val[y] is None or val[val[y]] is None:
                    continue
                val[x] = val[val[y]]
                dst = x
            else:
                if val[x] is None or val[y] is None:
                    continue
                dst = val[x]
                val[dst] = val[y]
            seen.add((dst, val[dst]))
    return seen
