# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-bendix-completion/. The authors are listed in prov/WM035M.jsonl.

import itertools
import random

from knuth_bendix_completion import (
    canonical,
    complete,
    critical_pairs,
    lpo,
    normalize,
    term_eq,
    unify,
)


def P(text):
    """Parse 'f(x, g(a))' into a term; names starting with u..z are variables."""
    pos = 0

    def term():
        nonlocal pos
        start = pos
        while pos < len(text) and (text[pos].isalnum() or text[pos] == "_"):
            pos += 1
        name = text[start:pos]
        if pos < len(text) and text[pos] == "(":
            pos += 1
            args = [term()]
            while text[pos] == ",":
                pos += 1
                while text[pos] == " ":
                    pos += 1
                args.append(term())
            pos += 1
            return (name,) + tuple(args)
        return name if name[0] in "uvwxyz" else (name,)

    text = text.replace(" ", "")
    return term()


def E(*pairs):
    return [(P(a), P(b)) for a, b in pairs]


GROUP = E(("m(e, x)", "x"), ("m(i(x), x)", "e"), ("m(m(x, y), z)", "m(x, m(y, z))"))
GROUP_RULES = E(
    ("m(e, x)", "x"), ("m(x, e)", "x"), ("m(i(x), x)", "e"), ("m(x, i(x))", "e"),
    ("m(m(x, y), z)", "m(x, m(y, z))"), ("i(e)", "e"), ("i(i(x))", "x"),
    ("m(i(x), m(x, y))", "y"), ("m(x, m(i(x), y))", "y"), ("i(m(x, y))", "m(i(y), i(x))"),
)
GROUP_PREC = {"i": 3, "m": 2, "e": 1}


def as_set(rules):
    return {canonical(r) for r in rules}


# ---------- an independent, naive oracle (recursive, for small terms) ----------

def o_var(t):
    return isinstance(t, str)


def o_vars(t):
    return {t} if o_var(t) else set().union(*[o_vars(a) for a in t[1:]]) if len(t) > 1 else set()


def o_sub(t, s):
    return s.get(t, t) if o_var(t) else (t[0],) + tuple(o_sub(a, s) for a in t[1:])


def o_match(p, t, s):
    if o_var(p):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if o_var(t) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_steps(t, rules):
    out = []
    for l, r in rules:
        s = {}
        if o_match(l, t, s):
            out.append(o_sub(r, s))
    if not o_var(t):
        for i in range(1, len(t)):
            for u in o_steps(t[i], rules):
                out.append(t[:i] + (u,) + t[i + 1:])
    return out


def o_nf(t, rules):
    while True:
        nxt = o_steps(t, rules)
        if not nxt:
            return t
        t = nxt[-1]  # any strategy: the rules are convergent when this is used


def o_unify(eqs):
    s = {}
    eqs = list(eqs)
    while eqs:
        a, b = eqs.pop()
        a, b = o_sub(a, s), o_sub(b, s)
        if a == b:
            continue
        if not o_var(a) and o_var(b):
            a, b = b, a
        if o_var(a):
            if a in o_vars(b):
                return None
            s = {x: o_sub(v, {a: b}) for x, v in s.items()}
            s[a] = b
            continue
        if a[0] != b[0] or len(a) != len(b):
            return None
        eqs.extend(zip(a[1:], b[1:]))
    return s


def o_positions(t, p=()):
    yield p, t
    if not o_var(t):
        for i in range(1, len(t)):
            yield from o_positions(t[i], p + (i,))


def o_put(t, p, s):
    if not p:
        return s
    i = p[0]
    return t[:i] + (o_put(t[i], p[1:], s),) + t[i + 1:]


def o_cps(rules):
    out = []
    for i, (l1, r1) in enumerate(rules):
        for j, (l2, r2) in enumerate(rules):
            ren = {x: x + "'" for x in o_vars(l2)}
            l2r, r2r = o_sub(l2, ren), o_sub(r2, ren)
            for p, u in o_positions(l1):
                if o_var(u) or (i == j and p == ()):
                    continue
                s = o_unify([(u, l2r)])
                if s is not None:
                    out.append((o_put(o_sub(l1, s), p, o_sub(r2r, s)), o_sub(r1, s)))
    return out


def o_lpo(s, t, prec):
    if o_var(s):
        return False
    if o_var(t):
        return t in o_vars(s) and s != t
    if any(a == t or o_lpo(a, t, prec) for a in s[1:]):
        return True
    f, g = s[0], t[0]
    if f != g and f in prec and g in prec and prec[f] > prec[g]:
        return all(o_lpo(s, b, prec) for b in t[1:])
    if f == g and len(s) == len(t):
        for a, b in zip(s[1:], t[1:]):
            if a != b:
                return o_lpo(a, b, prec) and all(o_lpo(s, c, prec) for c in t[1:])
        return False
    return False


def o_eval(t, alg, env):
    if o_var(t):
        return env[t]
    return alg[t[0]][tuple(o_eval(a, alg, env) for a in t[1:])]


def o_holds(eq, alg, dom):
    s, t = eq
    vs = sorted(o_vars(s) | o_vars(t))
    for vals in itertools.product(dom, repeat=len(vs)):
        env = dict(zip(vs, vals))
        if o_eval(s, alg, env) != o_eval(t, alg, env):
            return False
    return True


def all_algebras(sig, dom):
    """Every algebra over the domain for the signature {symbol: arity}."""
    names = sorted(sig)
    choices = []
    for f in names:
        keys = list(itertools.product(dom, repeat=sig[f]))
        choices.append([dict(zip(keys, vals)) for vals in itertools.product(dom, repeat=len(keys))])
    for combo in itertools.product(*choices):
        yield dict(zip(names, combo))


def o_bfs(t, eqs, depth, max_size):
    """Terms reachable from t by at most depth replacements with eqs, both ways."""
    both = eqs + [(b, a) for a, b in eqs if not o_var(b) and o_vars(a) <= o_vars(b)]
    seen = {t}
    frontier = [t]
    for _ in range(depth):
        nxt = []
        for u in frontier:
            for v in o_steps(u, both):
                if v not in seen and len(repr(v)) <= max_size:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return seen


# ---------- the examples of the page ----------

def test_page_example():
    status, rules = complete(E(("f(f(x))", "g(x)")), lpo({"f": 2, "g": 1}))
    assert status == "success"
    assert rules == E(("f(f(x))", "g(x)"), ("f(g(x))", "g(f(x))"))


def test_groups():
    status, rules = complete(GROUP, lpo(GROUP_PREC))
    assert status == "success"
    assert as_set(rules) == as_set(GROUP_RULES)


def test_groups_any_input_order_gives_the_same_reduced_system():
    for perm in itertools.permutations(GROUP):
        status, rules = complete(list(perm), lpo(GROUP_PREC))
        assert status == "success" and as_set(rules) == as_set(GROUP_RULES)


def test_divergence_gives_up():
    status, rules = complete(E(("f(g(f(x)))", "g(f(x))")), lpo({"f": 2, "g": 1}), max_steps=20)
    assert status == "give up"
    assert canonical((P("f(g(g(g(f(x)))))"), P("g(g(g(f(x))))"))) in as_set(rules)


def test_commutativity_fails():
    status, eq = complete(E(("p(x, y)", "p(y, x)")), lpo({"p": 1}))
    assert status == "fail" and as_set([eq]) == as_set(E(("p(x, y)", "p(y, x)")))


def test_empty_and_trivial():
    assert complete([], lpo({})) == ("success", [])
    assert complete([("x", "x")], lpo({})) == ("success", [])
    assert complete([(P("f(x)"), P("f(x)"))], lpo({"f": 1})) == ("success", [])
    assert complete([("x", "y")], lpo({}))[0] == "fail"


def test_non_linear_and_shared_variables():
    status, rules = complete(E(("f(x, x)", "x")), lpo({"f": 1}))
    assert status == "success" and rules == E(("f(x, x)", "x"))
    # x occurs on both sides; the right side has fewer variables
    status, rules = complete(E(("h(x, y)", "g(x)")), lpo({"h": 2, "g": 1}))
    assert status == "success" and rules == E(("h(x, y)", "g(x)"))
    # the other orientation would introduce a variable
    status, eq = complete(E(("h(x, y)", "g(x)")), lpo({"h": 1, "g": 2}))
    assert status == "fail"


def test_collapse_and_compose():
    # a = b, f(a) = c, then b = c makes f(a) -> c's left side reducible
    status, rules = complete(E(("f(a)", "c"), ("a", "b")), lpo({"f": 4, "a": 3, "b": 2, "c": 1}))
    assert status == "success"
    assert as_set(rules) == as_set(E(("a", "b"), ("f(b)", "c")))


def test_deep_terms():
    n = 2000
    t = ("a",)
    for _ in range(n):
        t = ("g", t)
    status, rules = complete([(t, ("a",))], lpo({"g": 2, "a": 1}))
    assert status == "success" and len(rules) == 1 and term_eq(rules[0][0], t)
    u = ("b",)
    for _ in range(n):
        u = ("g", u)
    assert unify(t, u) is None
    deep = ("a",)
    for _ in range(3 * n):
        deep = ("g", deep)
    assert term_eq(normalize(deep, rules), ("a",))  # g^6000(a) -> g^4000(a) -> g^2000(a) -> a
    deep = ("g", deep)
    assert term_eq(normalize(deep, rules), ("g", ("a",)))


def test_deep_normalization_result():
    n = 1500
    t = ("a",)
    for _ in range(n):
        t = ("g", t)
    rules = [(("g", ("g", "x")), "x")]
    assert term_eq(normalize(t, rules), ("a",))
    assert lpo({"g": 1})(t, ("g", ("a",)))


# ---------- random systems against the oracle ----------

SIGS = [
    {"f": 2, "g": 1, "a": 0},
    {"m": 2, "i": 1, "e": 0},
    {"f": 1, "g": 1, "a": 0, "b": 0},
    {"h": 2, "a": 0, "b": 0},
]


def rand_term(rng, sig, vs, depth):
    if depth == 0 or rng.random() < 0.3:
        consts = [f for f, n in sig.items() if n == 0]
        if vs and (not consts or rng.random() < 0.6):
            return rng.choice(vs)
        return (rng.choice(consts),)
    f = rng.choice(sorted(sig))
    return (f,) + tuple(rand_term(rng, sig, vs, depth - 1) for _ in range(sig[f]))


def test_random_against_oracle():
    rng = random.Random(20261106)
    models_cache = {}
    stats = {"success": 0, "fail": 0, "give up": 0, "bfs": 0}
    cases = 0
    while cases < 600:
        k = rng.randrange(len(SIGS))
        sig = SIGS[k]
        if k not in models_cache:
            models_cache[k] = list(all_algebras(sig, (0, 1)))
        eqs = [(rand_term(rng, sig, ["x", "y"], 2), rand_term(rng, sig, ["x", "y"], 2))
               for _ in range(rng.randint(1, 3))]
        order = sorted(sig)
        rng.shuffle(order)
        prec = {f: i for i, f in enumerate(order)}
        status, out = complete(eqs, lpo(prec), max_steps=40)
        cases += 1
        stats[status] += 1
        models = [a for a in models_cache[k] if all(o_holds(e, a, (0, 1)) for e in eqs)]
        if status == "fail":
            s, t = out
            assert s != t and not o_lpo(s, t, prec) and not o_lpo(t, s, prec)
            assert all(o_holds((s, t), a, (0, 1)) for a in models)
            continue
        rules = out
        for l, r in rules:
            assert o_lpo(l, r, prec)  # every rule is oriented, so R terminates
            assert all(o_holds((l, r), a, (0, 1)) for a in models)  # sound
        if status == "give up":
            continue
        for i, (l, r) in enumerate(rules):  # the result is reduced
            assert o_steps(r, rules) == []
            assert o_steps(l, rules[:i] + rules[i + 1:]) == []
        for u, v in o_cps(rules):  # local confluence
            assert o_nf(u, rules) == o_nf(v, rules)
        for s, t in eqs:  # the input equations are decided
            assert o_nf(s, rules) == o_nf(t, rules)
        for _ in range(3):  # bounded search for E-equal terms
            s = rand_term(rng, sig, ["x"], 2)
            nf = o_nf(s, rules)
            for t in o_bfs(s, eqs, 2, 60):
                assert o_nf(t, rules) == nf
                stats["bfs"] += 1
    assert cases >= 500
    assert stats["success"] >= 150 and stats["fail"] >= 30 and stats["bfs"] >= 1000, stats


def test_critical_pairs_against_oracle():
    rng = random.Random(7)
    checked = 0
    for _ in range(800):
        sig = SIGS[rng.randrange(len(SIGS))]
        l1 = rand_term(rng, sig, ["x", "y"], 3)
        l2 = rand_term(rng, sig, ["x", "y"], 2)
        if o_var(l1) or o_var(l2):
            continue
        r1 = rand_term(rng, sig, sorted(o_vars(l1)), 2)
        r2 = rand_term(rng, sig, sorted(o_vars(l2)), 2)
        mine = sorted(map(repr, (canonical(p) for p in critical_pairs((l1, r1), (l2, r2)))))
        ref = []
        for p, u in o_positions(l1):
            if o_var(u):
                continue
            ren = {x: x + "'" for x in o_vars(l2)}
            s = o_unify([(u, o_sub(l2, ren))])
            if s is not None:
                ref.append(canonical((o_put(o_sub(l1, s), p, o_sub(o_sub(r2, ren), s)), o_sub(r1, s))))
        assert mine == sorted(map(repr, ref))
        checked += 1
    assert checked >= 500


def test_lpo_against_oracle():
    rng = random.Random(3)
    for _ in range(3000):
        sig = SIGS[rng.randrange(len(SIGS))]
        order = sorted(sig)
        rng.shuffle(order)
        prec = {f: i for i, f in enumerate(order)}
        s = rand_term(rng, sig, ["x", "y"], 3)
        t = rand_term(rng, sig, ["x", "y"], 3)
        assert lpo(prec)(s, t) == o_lpo(s, t, prec)
