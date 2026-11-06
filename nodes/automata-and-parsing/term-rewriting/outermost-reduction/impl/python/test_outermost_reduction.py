# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/outermost-reduction/. The authors are listed in prov/1DTK3Q.jsonl.

import random

import pytest

from outermost_reduction import outermost_normalize, term_eq

# ---------- an independent, naive oracle (recursive, for small terms) ----------


def o_match(p, t, s):
    if isinstance(p, str):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if isinstance(t, str) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_subst(t, s):
    if isinstance(t, str):
        return s.get(t, t)
    return (t[0],) + tuple(o_subst(a, s) for a in t[1:])


def o_positions(t, p=()):
    yield p, t
    if not isinstance(t, str):
        for i, a in enumerate(t[1:], 1):
            yield from o_positions(a, p + (i,))


def o_replace(t, p, u):
    if not p:
        return u
    i = p[0]
    return t[:i] + (o_replace(t[i], p[1:], u),) + t[i + 1:]


def o_rule_at(u, rules):
    for k, (l, r) in enumerate(rules):
        s = {}
        if o_match(l, u, s):
            return k, o_subst(r, s)
    return None


def o_outermost(t, rules, bound):
    """Leftmost-outermost by brute force: all redexes, keep those with no redex
    strictly above, take the leftmost."""
    trace = []
    while True:
        if sum(1 for _ in o_positions(t)) > 300:
            return "big", trace
        redexes = [p for p, u in o_positions(t) if o_rule_at(u, rules) is not None]
        if not redexes:
            return t, trace
        outer = [p for p in redexes if not any(q != p and p[:len(q)] == q for q in redexes)]
        p = min(outer)
        if len(trace) == bound:
            return None, trace
        k, v = o_rule_at(dict(o_positions(t))[p], rules)
        trace.append((p, k))
        t = o_replace(t, p, v)


def o_successors(t, rules):
    out = []
    for p, u in o_positions(t):
        for l, r in rules:
            s = {}
            if o_match(l, u, s):
                out.append(o_replace(t, p, o_subst(r, s)))
    return out


def o_reach(t, rules, limit, max_size=10**9):
    """The terms reachable from t, explored until limit terms are seen.
    Returns None when a term larger than max_size is reached."""
    seen, todo = {t}, [t]
    while todo and len(seen) < limit:
        u = todo.pop()
        if sum(1 for _ in o_positions(u)) > max_size:
            return None
        for v in o_successors(u, rules):
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def o_unify(s, t):
    """Most general unifier test, for the orthogonality filter."""
    sub = {}

    def walk(u):
        while isinstance(u, str) and u in sub:
            u = sub[u]
        return u

    def occurs(x, u):
        u = walk(u)
        if isinstance(u, str):
            return u == x
        return any(occurs(x, a) for a in u[1:])

    todo = [(s, t)]
    while todo:
        a, b = todo.pop()
        a, b = walk(a), walk(b)
        if a == b:
            continue
        if isinstance(a, str):
            if occurs(a, b):
                return False
            sub[a] = b
        elif isinstance(b, str):
            todo.append((b, a))
        elif a[0] != b[0] or len(a) != len(b):
            return False
        else:
            todo.extend(zip(a[1:], b[1:]))
    return True


def rename(t, suffix):
    if isinstance(t, str):
        return t + suffix
    return (t[0],) + tuple(rename(a, suffix) for a in t[1:])


def overlaps(rules):
    for i, (l1, _) in enumerate(rules):
        for j, (l2, _) in enumerate(rules):
            l2r = rename(l2, "'")
            for p, u in o_positions(l1):
                if isinstance(u, str) or (i == j and p == ()):
                    continue
                if o_unify(u, l2r):
                    return True
    return False


# ---------- page example and edge cases ----------

# rules 0 to 3: an infinite list of numbers and the head of a list
STREAM = [
    (("from", "x"), ("cons", "x", ("from", ("s", "x")))),
    (("hd", ("cons", "x", "y")), "x"),
    (("tl", ("cons", "x", "y")), "y"),
    (("loop",), ("loop",)),
]


def test_page_example():
    t = ("hd", ("tl", ("from", ("0",))))
    trace = []
    nf, steps = outermost_normalize(t, STREAM, trace=trace)
    assert nf == ("s", ("0",))
    assert trace == [((1, 1), 0), ((1,), 2), ((1,), 0), ((), 1)]
    assert steps == 4


def test_erasing_argument():
    rules = [(("k", "x", "y"), "x"), (("loop",), ("loop",))]
    nf, steps = outermost_normalize(("k", ("a",), ("loop",)), rules)
    assert nf == ("a",) and steps == 1


def test_empty_system_and_normal_forms():
    t = ("f", "x", ("g", ("a",)))
    assert outermost_normalize(t, []) == (t, 0)
    assert outermost_normalize("x", STREAM) == ("x", 0)


def test_not_normalizing_without_left_normality():
    # orthogonal but not left-normal: f(x, b) has a variable before b
    rules = [(("f", "x", ("b",)), ("c",)), (("a",), ("a",)), (("d",), ("b",))]
    assert not overlaps(rules)
    nf, steps = outermost_normalize(("f", ("a",), ("d",)), rules, max_steps=200)
    assert nf is None and steps == 200
    assert ("c",) in o_reach(("f", ("a",), ("d",)), rules, 50)


def test_nonlinear_rule():
    rules = [(("eq", "x", "x"), ("t",)), (("d",), ("a",))]
    assert outermost_normalize(("eq", ("a",), ("d",)), rules)[0] == ("t",)


def test_bad_rules():
    with pytest.raises(ValueError):
        outermost_normalize(("a",), [("x", ("a",))])
    with pytest.raises(ValueError):
        outermost_normalize(("a",), [(("a",), "y")])


def num(k):
    t = ("0",)
    for _ in range(k):
        t = ("s", t)
    return t


def test_deep_terms():
    n = 20000
    t = ("hd", ("cons", num(n), ("loop",)))
    nf, steps = outermost_normalize(t, STREAM)
    assert steps == 1 and term_eq(nf, num(n))
    add = [(("add", ("0",), "y"), "y"), (("add", ("s", "x"), "y"), ("s", ("add", "x", "y")))]
    m = 1500
    nf, steps = outermost_normalize(("add", num(m), num(n)), add)
    assert steps == m + 1 and term_eq(nf, num(m + n))


# ---------- random tests ----------

SIG = [("f", 2), ("g", 1), ("h", 1), ("a", 0), ("b", 0)]


def rand_term(rng, depth, vs, sig=SIG):
    leaves = [f for f, n in sig if n == 0]
    inner = [(f, n) for f, n in sig if n > 0]
    if depth == 0 or rng.random() < 0.3:
        if vs and rng.random() < 0.5:
            return rng.choice(vs)
        return (rng.choice(leaves),)
    f, n = rng.choice(inner)
    return (f,) + tuple(rand_term(rng, depth - 1, vs, sig) for _ in range(n))


def lhs_vars(l):
    return sorted({u for _, u in o_positions(l) if isinstance(u, str)})


def rand_rules(rng):
    rules = []
    for _ in range(rng.randint(0, 4)):
        while True:
            l = rand_term(rng, 2, ["x", "y"])
            if not isinstance(l, str):
                break
        rules.append((l, rand_term(rng, 2, lhs_vars(l))))
    return rules


def test_random_trace_against_oracle():
    rng = random.Random(1977)
    compared = 0
    for _ in range(1500):
        rules = rand_rules(rng)
        t = rand_term(rng, 3, ["x", "y"])
        trace = []
        nf, steps = outermost_normalize(t, rules, max_steps=30, trace=trace)
        o_nf, o_trace = o_outermost(t, rules, 30)
        if o_nf == "big":
            assert trace[:len(o_trace)] == o_trace
            continue
        compared += 1
        assert trace == o_trace
        assert nf == o_nf
        if nf is not None:
            assert not o_successors(nf, rules)
    assert compared >= 1000


# constructor systems: defined symbols F and G, constructors c, s, a, b
CONS = [("c", 2), ("s", 1), ("a", 0), ("b", 0)]
ALL = CONS + [("F", 2), ("G", 1)]


def linear_pattern(rng, depth, counter):
    if depth == 0 or rng.random() < 0.4:
        if rng.random() < 0.6:
            counter[0] += 1
            return "x%d" % counter[0]
        return (rng.choice(["a", "b"]),)
    f, n = rng.choice([("c", 2), ("s", 1)])
    return (f,) + tuple(linear_pattern(rng, depth - 1, counter) for _ in range(n))


def left_normal(l):
    seen_var = False
    for _, u in o_positions(l):
        if isinstance(u, str):
            seen_var = True
        elif seen_var:
            return False
    return True


def rand_orthogonal(rng):
    rules = []
    for _ in range(rng.randint(0, 5)):
        f, n = rng.choice([("F", 2), ("G", 1)])
        counter = [0]
        l = (f,) + tuple(linear_pattern(rng, 2, counter) for _ in range(n))
        if not left_normal(l) or overlaps(rules + [(l, l)]):
            continue
        rules.append((l, rand_term(rng, 2, lhs_vars(l), ALL)))
    return rules


def test_normalizing_on_left_normal_orthogonal_systems():
    rng = random.Random(42)
    checked = with_nf = 0
    for _ in range(1500):
        rules = rand_orthogonal(rng)
        assert not overlaps(rules)
        t = rand_term(rng, 3, [], ALL)
        reach = o_reach(t, rules, 150, 40)
        if reach is None or len(reach) >= 150:
            continue
        checked += 1
        nfs = [u for u in reach if not o_successors(u, rules)]
        assert len(nfs) <= 1  # orthogonal systems are confluent
        nf, steps = outermost_normalize(t, rules, max_steps=len(reach) + 1)
        if nfs:
            with_nf += 1
            assert nf == nfs[0]
        else:
            assert nf is None
    assert checked >= 800 and with_nf >= 500
