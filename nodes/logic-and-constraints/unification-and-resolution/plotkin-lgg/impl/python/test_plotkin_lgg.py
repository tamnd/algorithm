# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plotkin-lgg/. The authors are listed in prov/F51B82.jsonl.

import itertools
import random

from plotkin_lgg import plotkin_lgg

A, B = ("a",), ("b",)


def f(*args):
    return ("f", *args)


def g(*args):
    return ("g", *args)


def apply(t, sigma):
    out, stack = [], [(t, False)]
    while stack:
        u, done = stack.pop()
        if isinstance(u, str):
            out.append(sigma.get(u, u))
        elif done:
            k = len(u) - 1
            args = out[len(out) - k:] if k else []
            del out[len(out) - k:]
            out.append((u[0], *args))
        else:
            stack.append((u, True))
            stack.extend((a, False) for a in reversed(u[1:]))
    return out[0]


def size(t):
    n, stack = 0, [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def match_all(pairs):
    lam, stack = {}, list(pairs)
    while stack:
        p, q = stack.pop()
        if isinstance(p, str):
            if lam.setdefault(p, q) != q:
                return None
        elif isinstance(q, str) or p[0] != q[0] or len(p) != len(q):
            return None
        else:
            stack.extend(zip(p[1:], q[1:]))
    return lam


def instance_of(general, special):
    return match_all([(general, special)]) is not None


def variant(u, v):
    return instance_of(u, v) and instance_of(v, u)


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def generalizations(s):
    """All generalizations of s, one per renaming class, by brute force.

    A generalization replaces an antichain of positions of s by variables;
    positions with equal subterms may share a variable.
    """
    def shapes(u):
        yield ("?", u)
        if not isinstance(u, str):
            for args in itertools.product(*[list(shapes(a)) for a in u[1:]]):
                yield (u[0], *args)

    def holes(u, acc):
        if isinstance(u, tuple) and u[0] == "?":
            acc.append(u)
        elif not isinstance(u, str):
            for a in u[1:]:
                holes(a, acc)
        return acc

    for shape in shapes(s):
        hs = holes(shape, [])
        groups = {}
        for i, hole in enumerate(hs):
            groups.setdefault(repr(hole[1]), []).append(i)
        for choice in itertools.product(*[list(set_partitions(v)) for v in groups.values()]):
            name = {}
            k = 0
            for part in choice:
                for block in part:
                    for i in block:
                        name[i] = f"V{k}"
                    k += 1
            counter = itertools.count()

            def fill(u):
                if isinstance(u, tuple) and u[0] == "?":
                    return name[next(counter)]
                if isinstance(u, str):
                    return u
                return (u[0], *[fill(a) for a in u[1:]])

            yield fill(shape)


def random_term(rng, depth, xs=("x", "y")):
    r = rng.random()
    if depth == 0 or r < 0.3:
        return rng.choice(xs) if rng.random() < 0.3 else rng.choice([A, B])
    if r < 0.55:
        return g(random_term(rng, depth - 1, xs))
    return f(random_term(rng, depth - 1, xs), random_term(rng, depth - 1, xs))


def check(s, t):
    lgg, th1, th2 = plotkin_lgg(s, t)
    assert apply(lgg, th1) == s and apply(lgg, th2) == t
    return lgg


def test_example() -> None:
    s = f(g(A), A, g(A))
    t = f(g(B), B, g(B))
    lgg, th1, th2 = plotkin_lgg(s, t)
    assert lgg == f(g("Z0"), "Z0", g("Z0"))
    assert th1 == {"Z0": A} and th2 == {"Z0": B}
    s = f(A, B, A)
    t = f(B, A, B)
    assert plotkin_lgg(s, t)[0] == f("Z0", "Z1", "Z0")


def test_edges() -> None:
    assert plotkin_lgg(A, A)[0] == A
    assert plotkin_lgg("x", "x")[0] == "x"
    assert plotkin_lgg("x", "y")[0] == "Z0"
    assert plotkin_lgg(A, B)[0] == "Z0"
    assert plotkin_lgg(f(A), f(A, A))[0] == "Z0"
    assert plotkin_lgg(f("Z0", A), f("Z0", B))[0] == f("Z0", "Z1")
    s = f(g("x"), "x")
    assert plotkin_lgg(s, s)[0] == s


def test_least_against_brute_force() -> None:
    rng = random.Random(5151)
    tested = 0
    while tested < 500:
        s, t = random_term(rng, 3), random_term(rng, 3)
        if size(s) > 7:
            continue
        lgg = check(s, t)
        found_variant = False
        for h in generalizations(s):
            if instance_of(h, t):
                assert instance_of(h, lgg)
                found_variant = found_variant or variant(h, lgg)
        assert found_variant
        tested += 1


def test_linear_work_on_large_terms() -> None:
    rng = random.Random(8)
    for n in (100, 300, 600):
        s = A
        t = B
        for i in range(n):
            c = rng.random() < 0.5
            s = f(s, A if c else B)
            t = f(t, A)
        lgg = check(s, t)
        assert size(lgg) == size(s)
