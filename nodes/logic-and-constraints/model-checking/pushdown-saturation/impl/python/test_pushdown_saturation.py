# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pushdown-saturation/. The authors are listed in prov/KE52MW.jsonl.

import itertools
import random
from collections import deque

from pushdown_saturation import EPS, accepts, post_star, pre_star

# The worked example: main calls p; p either returns or calls itself first.
EXAMPLE = [
    ("g", "m0", "g", ("p0", "m1")),
    ("g", "p0", "g", ("p1",)),
    ("g", "p0", "g", ("p2",)),
    ("g", "p1", "g", ("p0", "p2")),
    ("g", "p2", "g", ()),
    ("g", "m1", "g", ("m1",)),
]


def single(configs):
    """A P-automaton (a trie) for a finite set of configurations."""
    trans, finals, fresh = set(), set(), itertools.count()
    nodes = {}
    for p, w in configs:
        state = p
        for i, a in enumerate(w):
            key = (p, w[: i + 1])
            if key not in nodes:
                nodes[key] = ("s", next(fresh))
                trans.add((state, a, nodes[key]))
            state = nodes[key]
        finals.add(state)  # for an empty stack, the control location p is final
    return trans, finals


def successors(rules, conf):
    p, w = conf
    if not w:
        return
    for q, g, q2, rhs in rules:
        if q == p and g == w[0]:
            yield (q2, rhs + w[1:])


def bounded_post(rules, starts, height):
    """All configurations reachable from starts by runs whose stack stays within height."""
    seen = set(starts)
    queue = deque(starts)
    while queue:
        c = queue.popleft()
        for d in successors(rules, c):
            if len(d[1]) <= height and d not in seen:
                seen.add(d)
                queue.append(d)
    return seen


def random_pds(rng, controls, letters, n_rules):
    rules = set()
    for _ in range(n_rules):
        k = rng.choice([0, 1, 1, 2, 2])
        rules.add((rng.choice(controls), rng.choice(letters), rng.choice(controls), tuple(rng.choice(letters) for _ in range(k))))
    return sorted(rules)


def all_configs(controls, letters, h):
    for p in controls:
        for n in range(h + 1):
            for w in itertools.product(letters, repeat=n):
                yield (p, w)


def test_example_post_star() -> None:
    rel = post_star(EXAMPLE, {("g", "m0", "f")})
    finals = {"f"}
    want = {("g", ("m0",)), ("g", ("m1",))}
    want |= {("g", (x,) + ("p2",) * k + ("m1",)) for x in ("p0", "p1", "p2") for k in range(4)}
    for conf in all_configs(["g"], ["m0", "m1", "p0", "p1", "p2"], 5):
        assert accepts(rel, finals, *conf) == (conf in want), conf


def test_example_pre_star() -> None:
    # which configurations can reach <g, m1>, the return to main?
    rel = pre_star(EXAMPLE, {("g", "m1", "f")})
    assert accepts(rel, {"f"}, "g", ("m0",))
    assert accepts(rel, {"f"}, "g", ("p1", "p2", "m1"))
    assert not accepts(rel, {"f"}, "g", ("m1", "m1"))
    assert not accepts(rel, {"f"}, "g", ("p0",))


def test_against_bounded_search() -> None:
    rng = random.Random(5)
    for _ in range(150):
        controls = ["a", "b", "c"][: rng.randint(1, 3)]
        letters = ["x", "y", "z"][: rng.randint(1, 3)]
        rules = random_pds(rng, controls, letters, rng.randint(1, 8))
        start = (rng.choice(controls), tuple(rng.choice(letters) for _ in range(rng.randint(1, 2))))
        h = 3
        # A shortest run to a configuration of height h never needs a stack
        # higher than |start| + h + |P|^2 |Gamma| + 2: two nested stack cells
        # that are both popped later, with equal (state, letter, state after
        # the pop), could be short-cut. So this bound makes the search exact.
        bound = len(start[1]) + h + len(controls) ** 2 * len(letters) + 2
        reach = bounded_post(rules, [start], bound)
        trans, finals = single([start])
        post = post_star(rules, trans)
        for conf in all_configs(controls, letters, h):
            assert accepts(post, finals, *conf) == (conf in reach), (rules, start, conf)
        # pre* of a small finite target set, checked from each small configuration
        targets = [c for c in all_configs(controls, letters, 2) if rng.random() < 0.15]
        trans, finals = single(targets)
        pre = pre_star(rules, trans)
        tset = set(targets)
        for conf in all_configs(controls, letters, 2):
            bnd = len(conf[1]) + 2 + len(controls) ** 2 * len(letters) + 2
            want = bool(bounded_post(rules, [conf], bnd) & tset)
            assert accepts(pre, finals, *conf) == want, (rules, targets, conf)


def random_automaton(rng, controls, letters):
    """A random P-automaton with no transition into a control location."""
    others = [("q", i) for i in range(rng.randint(1, 3))]
    trans = set()
    for _ in range(rng.randint(1, 6)):
        trans.add((rng.choice(controls + others), rng.choice(letters), rng.choice(others)))
    finals = {q for q in others if rng.random() < 0.5} or {others[0]}
    if rng.random() < 0.3:
        finals.add(rng.choice(controls))
    return trans, finals


def intersects(rel, finals, p, trans2, finals2):
    """Is some <p, w> accepted by both automata? The second has no empty moves."""
    out1, out2 = {}, {}
    for q, a, q2 in rel:
        out1.setdefault(q, []).append((a, q2))
    for q, a, q2 in trans2:
        out2.setdefault(q, []).append((a, q2))
    seen = {(p, p)}
    stack = [(p, p)]
    while stack:
        s1, s2 = stack.pop()
        if s1 in finals and s2 in finals2:
            return True
        nxt = []
        for a, t1 in out1.get(s1, []):
            if a is EPS:
                nxt.append((t1, s2))
            else:
                nxt.extend((t1, t2) for b, t2 in out2.get(s2, []) if b == a)
        for pair in nxt:
            if pair not in seen:
                seen.add(pair)
                stack.append(pair)
    return False


def test_pre_and_post_are_dual() -> None:
    # c is in pre*(C) exactly when post*({c}) meets C, for random regular C
    rng = random.Random(6)
    for _ in range(150):
        controls = ["a", "b", "c"][: rng.randint(1, 3)]
        letters = ["x", "y"][: rng.randint(1, 2)]
        rules = random_pds(rng, controls, letters, rng.randint(1, 7))
        trans, finals = random_automaton(rng, controls, letters)
        pre = pre_star(rules, trans)
        for conf in all_configs(controls, letters, 3):
            t1, f1 = single([conf])
            post = post_star(rules, t1)
            want = any(intersects(post, f1, p, trans, finals) for p in controls)
            assert accepts(pre, finals, *conf) == want, (rules, trans, finals, conf)


def test_edges() -> None:
    # no rules: pre* and post* are the input sets
    assert pre_star([], {("a", "x", "f")}) == {("a", "x", "f")}
    rel = post_star([], {("a", "x", "f")})
    assert accepts(rel, {"f"}, "a", ("x",)) and not accepts(rel, {"f"}, "a", ())
    # a pop to the empty stack
    rel = post_star([("a", "x", "b", ())], {("a", "x", "f")})
    assert accepts(rel, {"f"}, "b", ())
    rel = pre_star([("a", "x", "b", ())], set())
    assert accepts(rel, {"b"}, "a", ("x",))
