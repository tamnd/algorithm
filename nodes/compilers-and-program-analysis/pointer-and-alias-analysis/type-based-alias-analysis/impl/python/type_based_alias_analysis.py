# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/type-based-alias-analysis/. The authors are listed in prov/FMJ8XA.jsonl.
"""Type-based alias analysis for a small type-safe language with classes.

A program has a class tree (each class has one parent, the root has none),
fields (each declared in one class, with a declared class as its type),
variables (each with a declared class), and statements in four forms:

    ("new", p, C)          p = new C        needs C <= T(p)
    ("copy", p, q)         p = q            needs T(q) <= T(p)
    ("load", p, q, f)      p = q.f          needs f in T(q), FT(f) <= T(p)
    ("store", q, f, p)     q.f = p          needs f in T(q), T(p) <= FT(f)

The memory references are the loads and stores, written q.f. The three
analyses of Diwan, McKinley and Moss answer whether two references may
touch the same field of the same object:

* type_decl: the declared types of the two locations, FT(f1) and FT(f2),
  have a common subtype;
* field_type_decl: the fields are the same and the declared types of the
  two bases have a common subtype;
* SMTypeRefs (selective merging), used here with fields as in their
  SMFieldTypeRefs: the fields are the same and TypeRefs(T(q1)) meets
  TypeRefs(T(q2)), where TypeRefs(T) holds the subtypes of T that are in
  the same group as T after merging the two types of every assignment
  between different types.

run(prog, rng) executes the program with the statements in random order and
reports the pairs of references that touched the same field of the same
object, and the dynamic types that each variable held.
"""


class Program:
    def __init__(self, parent, fields, types, stmts):
        self.parent = dict(parent)  # class -> parent class or None
        self.fields = dict(fields)  # field -> (declaring class, field type)
        self.types = dict(types)  # variable -> declared class
        self.stmts = list(stmts)

    def is_sub(self, c, d):
        while c is not None:
            if c == d:
                return True
            c = self.parent[c]
        return False

    def subtypes(self, t):
        return {c for c in self.parent if self.is_sub(c, t)}

    def has_field(self, t, f):
        return self.is_sub(t, self.fields[f][0])

    def field_type(self, f):
        return self.fields[f][1]

    def check(self):
        """Raise TypeError if a statement breaks the typing rules."""
        T = self.types
        for s in self.stmts:
            kind = s[0]
            if kind == "new":
                ok = self.is_sub(s[2], T[s[1]])
            elif kind == "copy":
                ok = self.is_sub(T[s[2]], T[s[1]])
            elif kind == "load":
                _, p, q, f = s
                ok = self.has_field(T[q], f) and self.is_sub(self.field_type(f), T[p])
            else:
                _, q, f, p = s
                ok = self.has_field(T[q], f) and self.is_sub(T[p], self.field_type(f))
            if not ok:
                raise TypeError("ill-typed statement: %r" % (s,))

    def references(self):
        """The memory references: (statement index, base variable, field)."""
        out = []
        for i, s in enumerate(self.stmts):
            if s[0] == "load":
                out.append((i, s[2], s[3]))
            elif s[0] == "store":
                out.append((i, s[1], s[2]))
        return out


def type_refs(prog):
    """TypeRefs(T) for each class T, by selective merging."""
    group = {c: c for c in prog.parent}  # @line L1

    def find(c):
        while group[c] != c:
            group[c] = group[group[c]]
            c = group[c]
        return c

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            group[max(a, b)] = min(a, b)

    T = prog.types
    for s in prog.stmts:  # @line L2
        kind = s[0]
        if kind == "new":
            src, dst = s[2], T[s[1]]
        elif kind == "copy":
            src, dst = T[s[2]], T[s[1]]
        elif kind == "load":
            src, dst = prog.field_type(s[3]), T[s[1]]
        else:
            src, dst = T[s[3]], prog.field_type(s[2])
        if src != dst:
            union(src, dst)  # @line L3
    return {t: {c for c in prog.subtypes(t) if find(c) == find(t)}  # @line L4
            for t in prog.parent}  # @line L5


def type_decl(prog, r1, r2):
    (_, _, f1), (_, _, f2) = r1, r2
    return bool(prog.subtypes(prog.field_type(f1)) & prog.subtypes(prog.field_type(f2)))


def field_type_decl(prog, r1, r2):
    (_, q1, f1), (_, q2, f2) = r1, r2
    if f1 != f2:
        return False
    return bool(prog.subtypes(prog.types[q1]) & prog.subtypes(prog.types[q2]))


def sm_type_refs(prog, r1, r2, refs=None):
    (_, q1, f1), (_, q2, f2) = r1, r2
    if f1 != f2:  # @line L6
        return False
    refs = refs if refs is not None else type_refs(prog)
    return bool(refs[prog.types[q1]] & refs[prog.types[q2]])  # @line L7


def may_alias_pairs(prog, method):
    """All pairs (i, j), i <= j, of reference sites that method says may
    alias. A site may alias itself when it can run on one object twice."""
    rs = prog.references()
    refs = type_refs(prog) if method is sm_type_refs else None
    out = set()
    for a in range(len(rs)):
        for b in range(a, len(rs)):
            if method is sm_type_refs:
                hit = method(prog, rs[a], rs[b], refs)
            else:
                hit = method(prog, rs[a], rs[b])
            if hit:
                out.add((rs[a][0], rs[b][0]))
    return out


def run(prog, rng, runs=20, steps=100):
    """Execute the program with the statements in random order. A statement
    that reads a variable or field with no value cannot run. Returns the set
    of pairs (i, j), i <= j, of reference sites that touched the same field
    of the same object, and the set of pairs (variable, dynamic class)."""
    touched_pairs, seen_types = set(), set()
    for _ in range(runs):
        val = {v: None for v in prog.types}
        heap = []  # object id -> (class, {field: object id})
        touched = {}  # (object id, field) -> set of sites
        for _ in range(steps):
            i = rng.randrange(len(prog.stmts))
            s = prog.stmts[i]
            kind = s[0]
            if kind == "new":
                heap.append((s[2], {}))
                val[s[1]] = len(heap) - 1
                dst = s[1]
            elif kind == "copy":
                if val[s[2]] is None:
                    continue
                val[s[1]] = val[s[2]]
                dst = s[1]
            elif kind == "load":
                _, p, q, f = s
                if val[q] is None or heap[val[q]][1].get(f) is None:
                    continue
                touched.setdefault((val[q], f), set()).add(i)
                val[p] = heap[val[q]][1][f]
                dst = p
            else:
                _, q, f, p = s
                if val[q] is None or val[p] is None:
                    continue
                touched.setdefault((val[q], f), set()).add(i)
                heap[val[q]][1][f] = val[p]
                dst = None
            if dst is not None:
                seen_types.add((dst, heap[val[dst]][0]))
        for sites in touched.values():
            for a in sites:
                for b in sites:
                    if a <= b:
                        touched_pairs.add((a, b))
    return touched_pairs, seen_types


HIERARCHY = {"Object": None, "A": "Object", "B": "Object",
             "A1": "A", "A2": "A", "B1": "B"}
FIELDS = {"val": ("Object", "Object"), "next": ("A", "A"),
          "left": ("A1", "A1"), "link": ("B", "A")}


def random_program(rng, nvars=8, nstmts=30):
    """A random well-typed program over the fixed class tree HIERARCHY and
    the fields FIELDS."""
    classes = list(HIERARCHY)
    types = {"x%d" % i: rng.choice(classes) for i in range(nvars)}
    prog = Program(HIERARCHY, FIELDS, types, [])
    names = list(types)
    fields = list(FIELDS)
    while len(prog.stmts) < nstmts:
        kind = rng.choice(["new", "new", "copy", "copy", "load", "store", "store"])
        p, q = rng.choice(names), rng.choice(names)
        if kind == "new":
            s = ("new", p, rng.choice(sorted(prog.subtypes(types[p]))))
        elif kind == "copy":
            s = ("copy", p, q)
        elif kind == "load":
            s = ("load", p, q, rng.choice(fields))
        else:
            s = ("store", q, rng.choice(fields), p)
        prog.stmts.append(s)
        try:
            prog.check()
        except TypeError:
            prog.stmts.pop()
    return prog
