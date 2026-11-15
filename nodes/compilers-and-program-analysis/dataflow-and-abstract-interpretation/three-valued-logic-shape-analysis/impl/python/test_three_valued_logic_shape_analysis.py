# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-valued-logic-shape-analysis/. The authors are listed in prov/BGQ8GB.jsonl.
import itertools
import random

from three_valued_logic_shape_analysis import HALF, analyze, blur, evaluate, from_heap, leq, node_of, predicates, thaw

V = ("x", "y", "t")
P = predicates(V)

# In-place reversal of the list at x into y.
REV = {
    0: [(("null", "y"), 1)],
    1: [(("assume", "nonnull", "x"), 2), (("assume", "null", "x"), 6)],
    2: [(("load", "t", "x"), 3)],
    3: [(("link", "x", "y"), 4)],
    4: [(("copy", "y", "x"), 5)],
    5: [(("copy", "x", "t"), 1)],
    6: [],
}

# Append a new cell at the end of the list at x.
APPEND = {
    0: [(("assume", "null", "x"), 8), (("assume", "nonnull", "x"), 1)],
    1: [(("copy", "y", "x"), 2)],
    2: [(("load", "t", "y"), 3)],
    3: [(("assume", "nonnull", "t"), 4), (("assume", "null", "t"), 5)],
    4: [(("copy", "y", "t"), 2)],
    5: [(("new", "t"), 6)],
    6: [(("link", "y", "t"), 7)],
    7: [],
    8: [(("new", "x"), 7)],
}

# Remove the second cell of the list at x.
DELETE = {
    0: [(("assume", "nonnull", "x"), 1), (("assume", "null", "x"), 6)],
    1: [(("load", "t", "x"), 2)],
    2: [(("assume", "nonnull", "t"), 3), (("assume", "null", "t"), 6)],
    3: [(("load", "y", "t"), 4)],
    4: [(("link", "x", "y"), 5)],
    5: [(("cut", "t"), 6)],
    6: [],
}

# Walk the list with no null test: it must fail at the end of an acyclic list.
WALK = {
    0: [(("copy", "y", "x"), 1)],
    1: [(("load", "t", "y"), 2)],
    2: [(("copy", "y", "t"), 1)],
}


# ------------------------------------------------------- concrete semantics


def step(st, env, nxt):
    """Successor states of one statement, or "err" on a null dereference."""
    kind = st[0]
    env, nxt = dict(env), dict(nxt)
    if kind == "assume":
        a = env[st[2]]
        if st[1] == "null":
            ok = a is None
        elif st[1] == "nonnull":
            ok = a is not None
        else:
            ok = (a == env[st[3]]) == (st[1] == "eq")
        return [(env, nxt)] if ok else []
    if kind == "null":
        env[st[1]] = None
    elif kind == "new":
        c = len(nxt)
        nxt[c] = None
        env[st[1]] = c
    elif kind == "copy":
        env[st[1]] = env[st[2]]
    else:
        base = env[st[2] if kind == "load" else st[1]]
        if base is None:
            return "err"
        if kind == "load":
            env[st[1]] = nxt[base]
        elif kind == "cut":
            nxt[base] = None
        else:
            nxt[base] = env[st[2]]
    return [(env, nxt)]


def canon(env, nxt):
    """A form of a heap that is equal for two heaps exactly when they are
    the same up to renaming of cells."""
    marks = {c: tuple(sorted(v for v in env if env[v] == c)) for c in nxt}
    kids = {c: [] for c in nxt}
    for d, c in nxt.items():
        if c is not None:
            kids[c].append(d)
    oncyc = set()
    for c in nxt:
        d, steps = nxt[c], 0
        while d is not None and d != c and steps <= len(nxt):
            d, steps = nxt[d], steps + 1
        if d == c:
            oncyc.add(c)

    def shape(c):
        return (marks[c], tuple(sorted(shape(d) for d in kids[c] if d not in oncyc)))

    roots = tuple(sorted(shape(c) for c in nxt if nxt[c] is None))
    cycles, done = [], set()
    for c in sorted(oncyc):
        if c in done:
            continue
        seq, d = [], c
        while d not in done:
            done.add(d)
            seq.append(shape(d))
            d = nxt[d]
        cycles.append(min(tuple(seq[i:] + seq[:i]) for i in range(len(seq))))
    return (tuple(sorted(v for v in env if env[v] is None)), roots, tuple(sorted(cycles)))


def heaps(maxk, free=("x",)):
    """One heap of each shape with at most maxk cells. Variables in free
    point anywhere, the others are null. Renaming cells shows that the
    first free variable that is not null can point to cell 0."""
    out = {}
    for k in range(maxk + 1):
        for nx in itertools.product([None] + list(range(k)), repeat=k):
            for targets in itertools.product([None] + list(range(k)), repeat=len(free)):
                if [c for c in targets if c is not None][:1] not in ([], [0]):
                    continue
                env = {v: None for v in V}
                env.update(zip(free, targets))
                nxt = dict(enumerate(nx))
                out.setdefault(canon(env, nxt), (env, nxt))
    return list(out.values())


# ------------------------------------------------------------- embeddings


def masks(S):
    out = []
    for v in range(S.size()):
        d = b = 0
        for i, p in enumerate(S.preds):
            if S.u[p][v] != HALF:
                d |= 1 << i
                b |= (S.u[p][v] == 1) << i
        out.append((d, b))
    return out


def embedding(C, T, cm=None, tm=None):
    """A surjective map f from the nodes of C onto the nodes of T with
    C(p)(v) below T(p)(f v) for every predicate and tuple, and two nodes
    of C mapped together only onto a summary node; None if there is none."""
    k, m = C.size(), T.size()
    if k < m:
        return None
    cm, tm = cm or masks(C), tm or masks(T)
    cand = []
    for c in range(k):
        cs = [w for w in range(m) if (cm[c][1] ^ tm[w][1]) & tm[w][0] == 0]
        if not cs:
            return None
        cand.append(cs)
    f = [None] * k

    def go(i):
        if i == k:
            return len(set(f)) == m
        for w in cand[i]:
            ok = leq(C.n[i][i], T.n[w][w]) and (C.sm[i] == 0 or T.sm[w] == HALF)
            for j in range(i):
                if not ok:
                    break
                if f[j] == w and T.sm[w] != HALF:
                    ok = False
                elif not leq(C.n[i][j], T.n[w][f[j]]) or not leq(C.n[j][i], T.n[f[j]][w]):
                    ok = False
            if ok:
                f[i] = w
                if go(i + 1):
                    return True
        f[i] = None
        return False

    return list(f) if go(0) else None


def signature(S):
    nodes = [node_of(S, v) for v in V]
    return tuple(a is None for a in nodes) + tuple(a == b for a, b in itertools.combinations(nodes, 2))


def check_sound(prog, init, cap=6):
    """Run the analysis from the abstraction of init and the concrete
    program from every heap in init. Every concrete state must embed into
    a structure at its point, and every concrete null dereference must be
    reported. A loop around "new" grows the heap without end, so the
    concrete run stops at heaps of more than cap cells. Returns (states
    checked, analysis result, errors)."""
    A, errors = analyze(prog, V, [from_heap(V, e, n) for e, n in init])
    index = {}
    for p in A:
        for key in A[p]:
            T = thaw(P, key)
            index.setdefault((p, signature(T)), []).append((T, masks(T)))
    seen = set()
    for env, nxt in init:
        work = [(0, env, nxt)]
        while work:
            p, e, n = work.pop()
            if len(n) > cap:
                continue
            key = (p, canon(e, n))
            if key in seen:
                continue
            seen.add(key)
            C = from_heap(V, e, n)
            if blur(C).key() not in A[p]:
                cm = masks(C)
                bucket = index.get((p, signature(C)), [])
                hit = next((i for i, (T, tm) in enumerate(bucket) if embedding(C, T, cm, tm)), None)
                assert hit is not None, (p, e, n)
                bucket.insert(0, bucket.pop(hit))  # neighbouring states often share a structure
            for st, q in prog[p]:
                r = step(st, e, n)
                if r == "err":
                    assert p in errors, (p, e, n)
                    continue
                work.extend((q, e2, n2) for e2, n2 in r)
    return len(seen), A, errors


def list_heap(length, var="x"):
    env = {v: None for v in V}
    env[var] = 0 if length else None
    return env, {i: (i + 1 if i + 1 < length else None) for i in range(length)}


# ------------------------------------------------------------------ tests


def test_kleene_logic():
    vals = (0, HALF, 1)
    S = from_heap(V, {"x": None, "y": None, "t": None}, {})
    for a in vals:
        assert evaluate(S, ("not", ("const", a))) == 1 - a
        for b in vals:
            assert evaluate(S, ("and", ("const", a), ("const", b))) == min(a, b)
            assert evaluate(S, ("or", ("const", a), ("const", b))) == max(a, b)
    assert evaluate(S, ("or", ("const", HALF), ("not", ("const", HALF)))) == HALF
    assert [b for b in vals if leq(0, b)] == [0, HALF]
    assert [b for b in vals if leq(HALF, b)] == [HALF]


def test_page_example():
    """Reversal of lists of up to 4 cells: the exit point has the empty list,
    one cell, two cells and a summary; y is an acyclic list that holds every
    cell, and no step can dereference null."""
    A, errors = analyze(REV, V, [from_heap(V, *list_heap(k)) for k in range(5)])
    assert errors == set()
    exit_ = [thaw(P, key) for key in A[6]]
    assert sorted(S.size() for S in exit_) == [0, 1, 2, 2]
    acyclic = ("not", ("exists", "v", ("p", "c", "v")))
    owned = ("forall", "v", ("p", "r:y", "v"))
    for S in exit_:
        assert evaluate(S, acyclic) == 1 and evaluate(S, owned) == 1
        assert node_of(S, "x") is None
    summary = [S for S in exit_ if HALF in S.sm]
    assert len(summary) == 1
    S = summary[0]
    h = node_of(S, "y")
    w = 1 - h
    assert S.sm == [HALF if v == w else 0 for v in range(2)]
    assert S.n[h][w] == HALF and S.n[w][w] == HALF and S.n[w][h] == 0
    assert {p: len(keys) for p, keys in A.items()} == {0: 4, 1: 13, 2: 9, 3: 12, 4: 12, 5: 9, 6: 4}
    longer, _ = analyze(REV, V, [from_heap(V, *list_heap(k)) for k in range(9)])
    assert longer == A


def test_blur_is_canonical():
    rng = random.Random(1)
    for _ in range(300):
        k = rng.randint(0, 6)
        nxt = {c: rng.choice([None] + list(range(k))) for c in range(k)}
        env = {v: rng.choice([None] + list(range(k))) for v in V}
        B = blur(from_heap(V, env, nxt))
        assert blur(B).key() == B.key()
        perm = list(range(k))
        rng.shuffle(perm)
        nxt2 = {perm[c]: (None if d is None else perm[d]) for c, d in nxt.items()}
        env2 = {v: (None if c is None else perm[c]) for v, c in env.items()}
        assert blur(from_heap(V, env2, nxt2)).key() == B.key()
        assert embedding(from_heap(V, env, nxt), B) is not None


def test_embedding_theorem():
    """A formula has a value on the blurred structure that is at least as
    weak as its value on the heap."""
    formulas = [
        ("exists", "v", ("p", "c", "v")),
        ("forall", "v", ("or", ("p", "r:x", "v"), ("p", "r:y", "v"))),
        ("exists", "v", ("exists", "w", ("and", ("n", "v", "w"), ("n", "w", "v")))),
        ("exists", "v", ("exists", "w", ("and", ("not", ("eq", "v", "w")), ("and", ("p", "r:x", "v"), ("p", "r:x", "w"))))),
        ("forall", "v", ("forall", "w", ("or", ("not", ("n", "v", "w")), ("p", "r:t", "w")))),
        ("exists", "v", ("and", ("p", "x", "v"), ("p", "y", "v"))),
        ("exists", "v", ("exists", "w", ("and", ("p", "y", "w"), ("n", "v", "w")))),
    ]
    rng = random.Random(2)
    weak = 0
    for _ in range(400):
        k = rng.randint(0, 6)
        nxt = {c: rng.choice([None] + list(range(k))) for c in range(k)}
        env = {v: rng.choice([None] + list(range(k))) for v in V}
        C = from_heap(V, env, nxt)
        B = blur(C)
        for phi in formulas:
            a, b = evaluate(C, phi), evaluate(B, phi)
            assert a in (0, 1) and leq(a, b)
            weak += b == HALF
    assert weak > 60


def test_reversal_sound_for_all_heaps_up_to_5_cells():
    init = heaps(5)
    assert len(init) == 818
    states, A, errors = check_sound(REV, init)
    assert states > 10000
    assert errors == set()


def test_other_programs_sound_for_all_heaps_up_to_4_cells():
    init = heaps(4)
    for prog in (APPEND, DELETE, WALK):
        check_sound(prog, init)
    _, _, errors = check_sound(WALK, [list_heap(k) for k in range(5)])
    assert errors == {1}
    _, A, errors = check_sound(APPEND, [list_heap(k) for k in range(5)])
    assert errors == set()
    for key in A[7]:
        S = thaw(P, key)
        assert evaluate(S, ("not", ("exists", "v", ("p", "c", "v")))) == 1
        assert evaluate(S, ("forall", "v", ("p", "r:x", "v"))) == 1


def test_random_programs_sound_for_all_heaps_up_to_3_cells():
    pool = [("null", "x"), ("new", "y"), ("copy", "t", "x"), ("copy", "x", "y"), ("load", "x", "y"), ("load", "t", "t"), ("load", "y", "x"), ("cut", "x"), ("cut", "t"), ("link", "x", "y"), ("link", "y", "x"), ("link", "t", "t"), ("link", "x", "t")]
    tests = [("assume", "null", "x"), ("assume", "nonnull", "y"), ("assume", "eq", "x", "t"), ("assume", "neq", "x", "y")]
    init = heaps(3, free=V)
    rng = random.Random(3)
    for _ in range(10):
        prog = {}
        for p in range(6):
            succ = [(rng.choice(pool), p + 1)]
            if rng.random() < 0.3:
                succ.append((rng.choice(tests), rng.randrange(6)))
            prog[p] = succ
        prog[6] = []
        check_sound(prog, init)
