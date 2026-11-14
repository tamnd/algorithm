# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-cfa/. The authors are listed in prov/WSCAQ1.jsonl.

import random

import toylam
from k_cfa import call_graph, free_names, k_cfa, label, project


class Halt(Exception):
    pass


def run(nodes, k, fuel=3000, max_depth=150):
    """An environment-based call-by-value interpreter that keeps, for each
    binding, the contour in which it was made: the last k call sites. Records
    every closure that a node produces in a contour, every binding and every
    call, with the closures cut down to (function, contours of its free
    variables)."""
    fv = free_names(nodes)
    seen, binds, calls = [], [], []
    budget = [fuel]

    def abstract(v):
        lam, env = v[1], v[2]
        return (lam, tuple(sorted((x, env[x][0]) for x in fv[lam])))

    def ev(t, env, d, depth):
        budget[0] -= 1
        if budget[0] < 0 or depth > max_depth:
            raise Halt("fuel")
        node = nodes[t]
        tag = node[0]
        if tag == "var":
            if node[1] not in env:
                raise Halt("stuck")
            v = env[node[1]][1]
        elif tag in ("int", "bool"):
            v = node
        elif tag in ("lam", "fix"):
            v = ("clo", t, env)
        elif tag == "app":
            f = ev(node[1], env, d, depth + 1)
            a = ev(node[2], env, d, depth + 1)
            if f[0] != "clo":
                raise Halt("stuck")
            lam = f[1]
            fun = nodes[lam]
            d2 = (d + (t,))[-k:] if k > 0 else ()
            calls.append((t, lam))
            inner = dict(f[2])
            if fun[0] == "fix":
                inner[fun[1]] = (d2, f)
                binds.append((((lam, fun[1]), d2), f))
                x, body = fun[2], fun[3]
            else:
                x, body = fun[1], fun[2]
            inner[x] = (d2, a)
            binds.append((((lam, x), d2), a))
            v = ev(body, inner, d2, depth + 1)
        elif tag == "let":
            a = ev(node[2], env, d, depth + 1)
            binds.append((((t, node[1]), d), a))
            v = ev(node[3], {**env, node[1]: (d, a)}, d, depth + 1)
        elif tag == "if":
            c = ev(node[1], env, d, depth + 1)
            if c[0] != "bool":
                raise Halt("stuck")
            v = ev(node[2] if c[1] else node[3], env, d, depth + 1)
        else:
            a = ev(node[2], env, d, depth + 1)
            b = ev(node[3], env, d, depth + 1)
            if a[0] != "int" or b[0] != "int":
                raise Halt("stuck")
            v = toylam._prim(node[1], a[1], b[1])
        seen.append(((t, d), v))
        return v

    try:
        ev(0, {}, (), 0)
    except Halt:
        pass
    seen = [(key, abstract(v)) for key, v in seen if v[0] == "clo"]
    binds = [(key, abstract(v)) for key, v in binds if v[0] == "clo"]
    return seen, binds, calls


def plain_zero_cfa(nodes):
    """The 0-CFA rules of the 0-CFA page applied round after round."""
    C = {t: set() for t in range(len(nodes))}
    R = {}
    reached = {0}
    changed = True

    def put(s, items):
        if not items <= s:
            s |= items
            return True
        return False

    while changed:
        changed = False
        for t in sorted(reached):
            node = nodes[t]
            tag = node[0]
            kids = []
            if tag in ("lam", "fix"):
                changed |= put(C[t], {t})
            elif tag == "var" and node[2] is not None:
                changed |= put(C[t], R.setdefault(node[2], set()))
            elif tag == "let":
                changed |= put(R.setdefault((t, node[1]), set()), C[node[2]])
                changed |= put(C[t], C[node[3]])
                kids = [node[2], node[3]]
            elif tag == "if":
                changed |= put(C[t], C[node[2]] | C[node[3]])
                kids = [node[1], node[2], node[3]]
            elif tag == "prim":
                kids = [node[2], node[3]]
            elif tag == "app":
                kids = [node[1], node[2]]
                for lam in list(C[node[1]]):
                    fun = nodes[lam]
                    if fun[0] == "fix":
                        changed |= put(R.setdefault((lam, fun[1]), set()), {lam})
                        binder, body = (lam, fun[2]), fun[3]
                    else:
                        binder, body = (lam, fun[1]), fun[2]
                    changed |= put(R.setdefault(binder, set()), C[node[2]])
                    changed |= put(C[t], C[body])
                    kids.append(body)
            for u in kids:
                if u not in reached:
                    reached.add(u)
                    changed = True
    return {t: s for t, s in C.items() if s}, {b: s for b, s in R.items() if s}


def find(nodes, tag, name):
    return next(t for t, n in enumerate(nodes) if n[0] == tag and n[1] == name)


def last_app(nodes):
    return max(t for t, n in enumerate(nodes) if n[0] == "app")


def fun(x, body):
    return ("lam", x, body)


ID_EXAMPLE = (
    "let", "id", fun("x", ("var", "x")),
    ("let", "a", ("app", ("var", "id"), fun("y", ("prim", "+", ("var", "y"), ("int", 1)))),
     ("let", "b", ("app", ("var", "id"), fun("z", ("prim", "*", ("var", "z"), ("int", 2)))),
      ("app", ("var", "a"), ("int", 3)))),
)

WRAPPED = (
    "let", "id", fun("x", ("var", "x")),
    ("let", "g", fun("w", ("app", ("var", "id"), ("var", "w"))),
     ("let", "a", ("app", ("var", "g"), fun("y", ("prim", "+", ("var", "y"), ("int", 1)))),
      ("let", "b", ("app", ("var", "g"), fun("z", ("prim", "*", ("var", "z"), ("int", 2)))),
       ("app", ("var", "a"), ("int", 3))))),
)


def targets_of_last_call(term, k):
    nodes, C, R = k_cfa(term, k)
    last = last_app(nodes)
    return {lam for t, lam in call_graph(nodes, C) if t == last}, nodes


def test_page_example_one_cfa_splits_the_calls_of_id():
    zero, nodes = targets_of_last_call(ID_EXAMPLE, 0)
    one, _ = targets_of_last_call(ID_EXAMPLE, 1)
    ly, lz = find(nodes, "lam", "y"), find(nodes, "lam", "z")
    assert zero == {ly, lz}
    assert one == {ly}
    nodes, C, R = k_cfa(ID_EXAMPLE, 1)
    lx = find(nodes, "lam", "x")
    assert {d for (b, d) in R if b == (lx, "x")} == {(t,) for t, n in enumerate(nodes) if n[0] == "app"} - {(last_app(nodes),)}


def test_a_wrapper_needs_two_call_sites():
    one, nodes = targets_of_last_call(WRAPPED, 1)
    two, _ = targets_of_last_call(WRAPPED, 2)
    ly, lz = find(nodes, "lam", "y"), find(nodes, "lam", "z")
    assert one == {ly, lz}
    assert two == {ly}
    assert toylam.evaluate(WRAPPED) == ("value", ("int", 4))


def terms(seed, count, depth=6):
    rng = random.Random(seed)
    for _ in range(count):
        yield toylam.random_term(rng, rng.randint(1, depth))


def test_zero_contours_is_zero_cfa():
    for term in terms(1991, 400):
        nodes, C, R = k_cfa(term, 0)
        assert (project(C), project(R)) == plain_zero_cfa(nodes), toylam.show(term)


def test_more_contours_never_lose_precision():
    for term in terms(2007, 300):
        flat = [k_cfa(term, k) for k in (0, 1, 2)]
        for small, big in ((1, 0), (2, 1)):
            cs, cb = project(flat[small][1]), project(flat[big][1])
            assert all(s <= cb.get(t, set()) for t, s in cs.items()), toylam.show(term)
            rs, rb = project(flat[small][2]), project(flat[big][2])
            assert all(s <= rb.get(b, set()) for b, s in rs.items()), toylam.show(term)


def test_sound_against_concrete_runs():
    with_calls = 0
    for term in terms(1988, 1500, depth=7):
        nodes = label(term)
        for k in (1, 2):
            _, C, R = k_cfa(term, k)
            seen, binds, calls = run(nodes, k)
            with_calls += bool(calls)
            for key, clo in seen:
                assert clo in C.get(key, ()), toylam.show(term)
            for key, clo in binds:
                assert clo in R.get(key, ()), toylam.show(term)
            assert set(calls) <= call_graph(nodes, C)
    assert with_calls > 100
