# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ltl-to-buchi-translation/. The authors are listed in prov/WRYARR.jsonl.

"""Translate an LTL formula into a Büchi automaton with the tableau of elementary sets.

A formula is a nested tuple:
    ("true",), ("false",), ("ap", "p"), ("not", f), ("and", f, g), ("or", f, g),
    ("implies", f, g), ("X", f), ("U", f, g), ("R", f, g), ("F", f), ("G", f).
A letter is a frozenset of atomic propositions (the ones that are true).

The generalized Büchi automaton (GBA) is a dict with the keys
    states: list of states, init: set, succ: dict state -> list of states,
    label: dict state -> frozenset (the letter that the state reads, restricted to aps),
    aps: frozenset of the atomic propositions of the formula,
    acc: list of sets of states (a run must visit each set infinitely often).
The automaton is state-labelled: a run q0 q1 q2 ... reads the word a0 a1 a2 ...
when a_i & aps == label[q_i] for each i.

Cost: the GBA has at most 2^e states, where e <= |phi| is the number of
subformulas of the forms p, X f and f U g. Degeneralization multiplies the
number of states by the number k of until subformulas (or by 1 when k = 0).
"""

from itertools import product

TRUE = ("true",)


def neg(f: tuple) -> tuple:
    """The negation of f, with a double negation removed."""
    return f[1] if f[0] == "not" else ("not", f)


def core(f: tuple) -> tuple:
    """Rewrite f with only true, ap, not, and, X and U."""
    op = f[0]
    if op in ("true", "ap"):
        return f
    if op == "false":
        return neg(TRUE)
    if op == "not":
        return neg(core(f[1]))
    if op == "and":
        return ("and", core(f[1]), core(f[2]))
    if op == "or":
        return neg(("and", neg(core(f[1])), neg(core(f[2]))))
    if op == "implies":
        return neg(("and", core(f[1]), neg(core(f[2]))))
    if op == "X":
        return ("X", core(f[1]))
    if op == "U":
        return ("U", core(f[1]), core(f[2]))
    if op == "R":
        return neg(("U", neg(core(f[1])), neg(core(f[2]))))
    if op == "F":
        return ("U", TRUE, core(f[1]))
    if op == "G":
        return neg(("U", TRUE, neg(core(f[1]))))
    raise ValueError(f"unknown operator {op!r}")


def subformulas(f: tuple) -> list[tuple]:
    """The subformulas of a core formula, children before parents, without repeats."""
    out: list[tuple] = []
    seen: set[tuple] = set()
    stack = [(f, False)]
    while stack:
        g, done = stack.pop()
        if g in seen:
            continue
        if done or g[0] in ("true", "ap"):
            seen.add(g)
            out.append(g)
            continue
        stack.append((g, True))
        for child in g[1:]:
            stack.append((child, False))
    return out


def elementary_sets(sub: list[tuple]) -> list[frozenset]:
    """All elementary sets, each given by the set of subformulas in sub that it holds."""
    base = [g for g in sub if g[0] in ("ap", "X", "U")]
    out = []
    for bits in product((False, True), repeat=len(base)):
        val = dict(zip(base, bits))
        val[TRUE] = True
        for g in sub:
            if g[0] == "not":
                val[g] = not val[g[1]]
            elif g[0] == "and":
                val[g] = val[g[1]] and val[g[2]]
        ok = True
        for g in sub:
            if g[0] == "U":
                if val[g[2]] and not val[g]:
                    ok = False
                if val[g] and not val[g[2]] and not val[g[1]]:
                    ok = False
        if ok:
            out.append(frozenset(g for g in sub if val[g]))
    return out


def ltl_to_gba(phi: tuple) -> dict:
    """The tableau GBA of phi: it accepts exactly the words that satisfy phi."""
    f = core(phi)
    sub = subformulas(f)  # @line L1
    states = elementary_sets(sub)  # @line L2
    aps = frozenset(g[1] for g in sub if g[0] == "ap")
    nexts = [g for g in sub if g[0] == "X"]
    untils = [g for g in sub if g[0] == "U"]
    init = {b for b in states if f in b}  # @line L3
    label = {b: frozenset(g[1] for g in b if g[0] == "ap") for b in states}
    succ: dict = {}
    for b in states:  # @line L4
        out = []
        for c in states:  # @line L5
            if all((x in b) == (x[1] in c) for x in nexts) and all(  # @line L6
                (u in b) == (u[2] in b or (u[1] in b and u in c)) for u in untils  # @line L7
            ):
                out.append(c)  # @line L8
        succ[b] = out
    acc = [{b for b in states if u not in b or u[2] in b} for u in untils]  # @line L9
    return {"states": states, "init": init, "succ": succ, "label": label, "aps": aps, "acc": acc}  # @line L10


def degeneralize(gba: dict) -> dict:
    """A Büchi automaton with the same language: states (q, i), with one accepting set."""
    acc = gba["acc"]
    k = len(acc)
    if k == 0:
        acc = [set(gba["states"])]
        k = 1
    states = [(q, i) for q in gba["states"] for i in range(k)]  # @line L11
    succ = {}
    for q, i in states:
        j = (i + 1) % k if q in acc[i] else i  # @line L12
        succ[(q, i)] = [(r, j) for r in gba["succ"][q]]
    return {
        "states": states,
        "init": {(q, 0) for q in gba["init"]},
        "succ": succ,
        "label": {(q, i): gba["label"][q] for q, i in states},
        "aps": gba["aps"],
        "accepting": {(q, 0) for q in gba["states"] if q in acc[0]},  # @line L13
    }


def ltl_to_buchi_translation(phi: tuple) -> dict:
    """A Büchi automaton (keys states, init, succ, label, aps, accepting) for phi."""
    return degeneralize(ltl_to_gba(phi))


# ---------------------------------------------------------------- use: model checking


def nested_dfs(init, succ, accepting):
    """Find a reachable accepting cycle; return (stem, cycle) or None. Linear time."""
    end = object()
    visited: set = set()
    flagged: set = set()
    for s0 in init:
        if s0 in visited:
            continue
        visited.add(s0)
        outer = [(s0, iter(succ(s0)))]
        while outer:
            s, it = outer[-1]
            t = next(it, end)
            if t is not end:
                if t not in visited:
                    visited.add(t)
                    outer.append((t, iter(succ(t))))
                continue
            if s in accepting:
                inner = [(s, iter(succ(s)))]
                while inner:
                    x, it2 = inner[-1]
                    y = next(it2, end)
                    if y is end:
                        inner.pop()
                    elif y == s:
                        return [v for v, _ in outer[:-1]], [v for v, _ in inner]
                    elif y not in flagged:
                        flagged.add(y)
                        inner.append((y, iter(succ(y))))
            outer.pop()
    return None


def ltl_model_check(model: dict, phi: tuple):
    """Decide whether every path of the Kripke structure satisfies phi.

    model has the keys init (list), succ (dict state -> list, each list nonempty)
    and label (dict state -> set of atomic propositions). Returns None when the
    model satisfies phi, else a counterexample (stem, cycle): the path
    stem + cycle + cycle + ... of the model violates phi.
    Cost: O(|M| * 2^O(|phi|)) time.
    """
    ba = ltl_to_buchi_translation(("not", phi))
    aps = ba["aps"]

    def match(s, q):
        return frozenset(model["label"][s]) & aps == ba["label"][q]

    init = [(s, q) for s in model["init"] for q in ba["init"] if match(s, q)]

    def succ(p):
        s, q = p
        return [(t, r) for t in model["succ"][s] for r in ba["succ"][q] if match(t, r)]

    accepting = {(s, q) for s in model["succ"] for q in ba["accepting"]}
    found = nested_dfs(init, succ, accepting)
    if found is None:
        return None
    stem, cycle = found
    return [s for s, _ in stem], [s for s, _ in cycle]
