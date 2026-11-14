# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-cfa/. The authors are listed in prov/JG6AT6.jsonl.

import random

import toylam
from zero_cfa import call_graph, label, param, zero_cfa


class Halt(Exception):
    pass


def run(nodes, fuel=4000, max_depth=150):
    """An environment-based call-by-value interpreter over the labelled
    nodes. It records every value that a node produces and every binding.
    Returns (outcome, seen, binds, calls), where outcome is ("value", v),
    ("stuck",) or ("fuel",)."""
    seen, binds, calls = [], [], []
    budget = [fuel]

    def ev(t, env, depth):
        budget[0] -= 1
        if budget[0] < 0 or depth > max_depth:
            raise Halt("fuel")
        node = nodes[t]
        tag = node[0]
        if tag == "var":
            if node[1] not in env:
                raise Halt("stuck")
            v = env[node[1]]
        elif tag in ("int", "bool"):
            v = node
        elif tag in ("lam", "fix"):
            v = ("clo", t, env)
        elif tag == "app":
            f = ev(node[1], env, depth + 1)
            a = ev(node[2], env, depth + 1)
            if f[0] != "clo":
                raise Halt("stuck")
            lam = f[1]
            calls.append((t, lam))
            binder, body = param(nodes[lam], lam)
            inner = dict(f[2])
            if nodes[lam][0] == "fix":
                inner[nodes[lam][1]] = f
                binds.append(((lam, nodes[lam][1]), f))
            inner[binder[1]] = a
            binds.append((binder, a))
            v = ev(body, inner, depth + 1)
        elif tag == "let":
            a = ev(node[2], env, depth + 1)
            binds.append(((t, node[1]), a))
            v = ev(node[3], {**env, node[1]: a}, depth + 1)
        elif tag == "if":
            c = ev(node[1], env, depth + 1)
            if c[0] != "bool":
                raise Halt("stuck")
            v = ev(node[2] if c[1] else node[3], env, depth + 1)
        else:
            a = ev(node[2], env, depth + 1)
            b = ev(node[3], env, depth + 1)
            if a[0] != "int" or b[0] != "int":
                raise Halt("stuck")
            v = toylam._prim(node[1], a[1], b[1])
        seen.append((t, v))
        return v

    try:
        outcome = ("value", ev(0, {}, 0))
    except Halt as h:
        outcome = (str(h),)
    return outcome, seen, binds, calls


def plain_cfa(nodes):
    """The 0-CFA rules applied to every reached node, round after round."""
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
                    binder, body = param(nodes[lam], lam)
                    if nodes[lam][0] == "fix":
                        changed |= put(R.setdefault((lam, nodes[lam][1]), set()), {lam})
                    changed |= put(R.setdefault(binder, set()), C[node[2]])
                    changed |= put(C[t], C[body])
                    kids.append(body)
            for k in kids:
                if k not in reached:
                    reached.add(k)
                    changed = True
    return C, {b: s for b, s in R.items() if s}


def same_outcome(mine, theirs, nodes):
    if mine[0] == "fuel" or theirs[0] == "fuel":
        return True
    if mine[0] != theirs[0]:
        return False
    if mine[0] == "stuck":
        return True
    v, w = mine[1], theirs[1]
    if v[0] == "clo":
        return nodes[v[1]][0] == w[0]
    return v == w


def find(nodes, tag, name):
    return next(t for t, n in enumerate(nodes) if n[0] == tag and n[1] == name)


ID_EXAMPLE = (
    "let", "id", ("lam", "x", ("var", "x")),
    ("let", "a", ("app", ("var", "id"), ("lam", "y", ("prim", "+", ("var", "y"), ("int", 1)))),
     ("let", "b", ("app", ("var", "id"), ("lam", "z", ("prim", "*", ("var", "z"), ("int", 2)))),
      ("app", ("var", "a"), ("int", 3)))),
)


def test_page_example_merges_the_two_calls_of_id():
    nodes, C, R = zero_cfa(ID_EXAMPLE)
    lx, ly, lz = find(nodes, "lam", "x"), find(nodes, "lam", "y"), find(nodes, "lam", "z")
    assert R[(lx, "x")] == {ly, lz}
    assert R[(find(nodes, "let", "a"), "a")] == {ly, lz}
    last = max(t for t, n in enumerate(nodes) if n[0] == "app")
    assert {lam for t, lam in call_graph(nodes, C) if t == last} == {ly, lz}
    assert toylam.evaluate(ID_EXAMPLE) == ("value", ("int", 4))


def test_body_of_an_uncalled_function_is_not_analysed():
    term = ("lam", "x", ("app", ("lam", "y", ("var", "y")), ("lam", "z", ("var", "z"))))
    nodes, C, R = zero_cfa(term)
    assert call_graph(nodes, C) == set()
    assert C[0] == {0}
    assert R == {}


def test_recursive_function():
    body = ("if", ("prim", "<", ("var", "x"), ("int", 1)), ("int", 0),
            ("app", ("var", "f"), ("prim", "-", ("var", "x"), ("int", 1))))
    term = ("app", ("fix", "f", "x", body), ("int", 3))
    nodes, C, R = zero_cfa(term)
    fix = find(nodes, "fix", "f")
    apps = [t for t, n in enumerate(nodes) if n[0] == "app"]
    assert len(apps) == 2 and apps[0] == 0
    assert call_graph(nodes, C) == {(0, fix), (apps[1], fix)}
    assert R[(fix, "f")] == {fix}


def test_labels_are_preorder():
    nodes = label(ID_EXAMPLE)
    assert nodes[0][0] == "let" and nodes[1] == ("lam", "x", 2) and nodes[2] == ("var", "x", (1, "x"))


def terms(seed, count, depth=6):
    rng = random.Random(seed)
    for _ in range(count):
        yield toylam.random_term(rng, rng.randint(1, depth))


def test_same_as_plain_iteration():
    for term in terms(1991, 500):
        nodes, C, R = zero_cfa(term)
        C2, R2 = plain_cfa(nodes)
        assert C == C2, toylam.show(term)
        assert R == R2, toylam.show(term)


def test_sound_against_concrete_runs():
    runs = 0
    for term in terms(1988, 2000, depth=7):
        nodes, C, R = zero_cfa(term)
        graph = call_graph(nodes, C)
        outcome, seen, binds, calls = run(nodes)
        runs += len(calls) > 0
        for t, v in seen:
            if v[0] == "clo":
                assert v[1] in C[t], toylam.show(term)
        for b, v in binds:
            if v[0] == "clo":
                assert v[1] in R.get(b, ()), toylam.show(term)
        assert set(calls) <= graph
    assert runs > 100


def test_interpreter_agrees_with_toylam():
    for term in terms(7, 500, depth=7):
        nodes = label(term)
        mine = run(nodes)[0]
        assert same_outcome(mine, toylam.evaluate(term, 4000), nodes), toylam.show(term)
