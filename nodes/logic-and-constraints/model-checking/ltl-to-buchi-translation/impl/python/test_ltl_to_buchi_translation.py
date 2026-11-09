# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ltl-to-buchi-translation/. The authors are listed in prov/WRYARR.jsonl.

import itertools
import random

from ltl_to_buchi_translation import (
    core,
    degeneralize,
    ltl_model_check,
    ltl_to_buchi_translation,
    ltl_to_gba,
    subformulas,
)

P, Q = ("ap", "p"), ("ap", "q")
LETTERS = [frozenset(s) for s in ([], ["p"], ["q"], ["p", "q"])]


def evaluate(f, word, loop):
    """Truth of f at each position of the lasso word: positions 0..n-1, then back to loop."""
    n = len(word)
    nxt = [i + 1 if i + 1 < n else loop for i in range(n)]
    op = f[0]
    if op == "true":
        return [True] * n
    if op == "false":
        return [False] * n
    if op == "ap":
        return [f[1] in a for a in word]
    if op == "not":
        return [not x for x in evaluate(f[1], word, loop)]
    if op in ("and", "or", "implies", "U", "R"):
        a = evaluate(f[1], word, loop)
        b = evaluate(f[2], word, loop)
        if op == "and":
            return [x and y for x, y in zip(a, b)]
        if op == "or":
            return [x or y for x, y in zip(a, b)]
        if op == "implies":
            return [(not x) or y for x, y in zip(a, b)]
        val = [op == "R"] * n  # least fixed point for U, greatest for R
        changed = True
        while changed:
            changed = False
            for i in reversed(range(n)):
                v = (b[i] or (a[i] and val[nxt[i]])) if op == "U" else (b[i] and (a[i] or val[nxt[i]]))
                if v != val[i]:
                    val[i], changed = v, True
        return val
    a = evaluate(f[1], word, loop)
    if op == "X":
        return [a[nxt[i]] for i in range(n)]
    if op in ("F", "G"):
        val = [op == "G"] * n
        changed = True
        while changed:
            changed = False
            for i in reversed(range(n)):
                v = (a[i] or val[nxt[i]]) if op == "F" else (a[i] and val[nxt[i]])
                if v != val[i]:
                    val[i], changed = v, True
        return val
    raise ValueError(op)


def accepts(ba, word, loop):
    """Does the Büchi automaton accept the lasso word? Search of the product with the word."""
    n = len(word)
    nxt = [i + 1 if i + 1 < n else loop for i in range(n)]

    def ok(q, i):
        return word[i] & ba["aps"] == ba["label"][q]

    def succ(x):
        q, i = x
        return [(r, nxt[i]) for r in ba["succ"][q] if ok(r, nxt[i])]

    start = [(q, 0) for q in ba["init"] if ok(q, 0)]
    seen, todo = set(start), list(start)
    while todo:
        for y in succ(todo.pop()):
            if y not in seen:
                seen.add(y)
                todo.append(y)
    for x in seen:
        if x[0] not in ba["accepting"]:
            continue
        back, todo = set(), succ(x)
        while todo:
            y = todo.pop()
            if y == x:
                return True
            if y not in back:
                back.add(y)
                todo.extend(succ(y))
    return False


def lasso_words(max_stem, max_loop):
    for a in range(max_stem + 1):
        for b in range(1, max_loop + 1):
            for w in itertools.product(LETTERS, repeat=a + b):
                yield list(w), a


def random_formula(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return rng.choice([P, Q, P, Q, ("true",)])
    op = rng.choice(["not", "and", "or", "X", "U", "R", "F", "G", "implies"])
    if op in ("not", "X", "F", "G"):
        return (op, random_formula(rng, depth - 1))
    return (op, random_formula(rng, depth - 1), random_formula(rng, depth - 1))


FIXED = [
    ("G", ("F", P)),
    ("F", ("G", P)),
    ("U", P, Q),
    ("R", P, Q),
    ("X", ("X", P)),
    ("G", ("implies", P, ("F", Q))),
    ("not", ("G", ("F", P))),
    ("and", ("G", ("F", P)), ("G", ("F", Q))),
    ("false",),
    ("true",),
]


def check_formula(f, words):
    ba = ltl_to_buchi_translation(f)
    for word, loop in words:
        assert accepts(ba, word, loop) == evaluate(f, word, loop)[0], (f, word, loop)


def test_fixed_formulas_on_all_short_lassos() -> None:
    words = list(lasso_words(2, 2))
    for f in FIXED:
        check_formula(f, words)


def test_random_formulas_on_all_short_lassos() -> None:
    rng = random.Random(7)
    words = list(lasso_words(2, 2))
    for _ in range(120):
        check_formula(random_formula(rng, 3), words)


def test_example_p_until_q() -> None:
    gba = ltl_to_gba(("U", P, Q))
    assert len(gba["states"]) == 5
    assert len(gba["init"]) == 3
    assert len(gba["acc"]) == 1 and len(gba["acc"][0]) == 4
    ba = degeneralize(gba)
    assert len(ba["states"]) == 5 and len(ba["accepting"]) == 4


def test_example_gf_p() -> None:
    gba = ltl_to_gba(("G", ("F", P)))
    assert len(gba["states"]) == 5
    assert len(gba["acc"]) == 2
    assert len(degeneralize(gba)["states"]) == 10


def test_state_bound() -> None:
    rng = random.Random(11)
    for _ in range(200):
        f = random_formula(rng, 3)
        sub = subformulas(core(f))
        e = sum(1 for g in sub if g[0] in ("ap", "X", "U"))
        k = sum(1 for g in sub if g[0] == "U")
        gba = ltl_to_gba(f)
        assert len(gba["states"]) <= 2**e
        assert len(gba["acc"]) == k
        assert len(degeneralize(gba)["states"]) == len(gba["states"]) * max(k, 1)


# ---------------------------------------------------------------- model checking


def random_model(rng, n):
    succ = {s: rng.sample(range(n), rng.randint(1, min(2, n))) for s in range(n)}
    label = {s: {a for a in ("p", "q") if rng.random() < 0.5} for s in range(n)}
    return {"init": [0], "succ": succ, "label": label}


def violating_lasso(model, phi, bound):
    """Reference: search all lasso paths of the model with at most bound states."""
    stack = [[s] for s in model["init"]]
    while stack:
        path = stack.pop()
        for t in model["succ"][path[-1]]:
            if t in path:
                loop = path.index(t)
                word = [frozenset(model["label"][s]) for s in path]
                if not evaluate(phi, word, loop)[0]:
                    return path, loop
            if len(path) < bound:
                stack.append(path + [t])
    return None


def replay(model, phi, cex):
    stem, cycle = cex
    path = stem + cycle
    assert path[0] in model["init"]
    for a, b in zip(path, path[1:] + [cycle[0]]):
        assert b in model["succ"][a]
    word = [frozenset(model["label"][s]) for s in path]
    assert not evaluate(phi, word, len(stem))[0]


def test_model_checking_against_lasso_enumeration() -> None:
    rng = random.Random(2024)
    formulas = FIXED + [random_formula(rng, 2) for _ in range(30)]
    for trial in range(60):
        model = random_model(rng, rng.randint(1, 4))
        for phi in rng.sample(formulas, 8):
            cex = ltl_model_check(model, phi)
            ref = violating_lasso(model, phi, 8)
            if cex is None:
                assert ref is None, (model, phi, ref)
            else:
                replay(model, phi, cex)


def test_model_checking_example() -> None:
    # 0 -> 1 -> 2 -> 0 and 2 -> 2; p holds in 1 only.
    model = {"init": [0], "succ": {0: [1], 1: [2], 2: [0, 2]}, "label": {0: set(), 1: {"p"}, 2: set()}}
    assert ltl_model_check(model, ("G", ("F", ("not", P)))) is None
    cex = ltl_model_check(model, ("G", ("F", P)))
    assert cex is not None
    replay(model, ("G", ("F", P)), cex)
    assert ltl_model_check(model, ("F", P)) is None
