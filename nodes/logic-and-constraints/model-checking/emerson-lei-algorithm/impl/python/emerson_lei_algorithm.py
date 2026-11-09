# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/emerson-lei-algorithm/. The authors are listed in prov/N9RYM5.jsonl.

"""Model checking of the modal mu-calculus by fixed-point iteration.

The Kripke structure is given by plain values:
- states: a list of hashable states,
- succ: a dict that maps each state to the list of its successors,
- label: a dict that maps each state to the set of atomic propositions true there.

A formula is a nested tuple in positive normal form:
("true",), ("false",), ("ap", p), ("nap", p) for "not p", ("and", f, g),
("or", f, g), ("dia", f) for "some successor satisfies f", ("box", f) for
"each successor satisfies f", ("var", X), ("mu", X, f), ("nu", X, f).
Each variable is bound once, and only negated atoms are allowed, so each body
is monotone in each variable.

emerson_lei(...) keeps the value of an inner fixed point between iterations of
an outer fixed point of the same sign, and resets it only when a fixed point of
the opposite sign around it changes. naive_iteration(...) restarts each inner
fixed point at each entry. Both return the same set of states.

Cost (this page proves it): with d the alternation depth and k the number of
fixed points, the bodies are evaluated at most k (k + 1)^d |S|^d times, so the
time is O(|phi| (|S| + |R|) (k + 1)^d |S|^d). The naive form evaluates them up
to k (|S| + 1)^q times, where q is the nesting depth. The recursion depth is
the syntactic depth of phi.
"""

from typing import Hashable, Sequence

State = Hashable
Formula = tuple


def fixpoints(phi: Formula) -> dict:
    """Map each bound variable to (sign, body, opposite), where `opposite` lists
    the variables of the fixed points inside the body that have the other sign.
    """
    info: dict = {}
    stack = [phi]
    while stack:
        f = stack.pop()
        op = f[0]
        if op in ("mu", "nu"):
            x, body = f[1], f[2]
            if x in info:
                raise ValueError(f"variable {x!r} is bound twice")
            inner, todo = [], [body]
            while todo:
                g = todo.pop()
                if g[0] in ("mu", "nu") and g[0] != op:
                    inner.append(g[1])
                if g[0] in ("and", "or"):
                    todo.extend(g[1:])
                elif g[0] in ("dia", "box"):
                    todo.append(g[1])
                elif g[0] in ("mu", "nu"):
                    todo.append(g[2])
            info[x] = (op, body, inner)
            stack.append(body)
        elif op in ("and", "or"):
            stack.extend(f[1:])
        elif op in ("dia", "box"):
            stack.append(f[1])
        elif op not in ("true", "false", "ap", "nap", "var"):
            raise ValueError(f"unknown operator {op!r}")
    return info


def alternation_depth(phi: Formula) -> int:
    """The largest number of sign blocks on a chain of nested fixed points.

    It is 0 with no fixed point, 1 when all nested fixed points have one sign,
    and grows by one at each change from mu to nu or from nu to mu.
    """
    best = 0
    stack = [(phi, None, 0)]
    while stack:
        f, sign, blocks = stack.pop()
        op = f[0]
        if op in ("mu", "nu"):
            blocks = blocks + 1 if op != sign else blocks
            best = max(best, blocks)
            stack.append((f[2], op, blocks))
        elif op in ("and", "or"):
            stack.extend((g, sign, blocks) for g in f[1:])
        elif op in ("dia", "box"):
            stack.append((f[1], sign, blocks))
    return best


def nesting_depth(phi: Formula) -> int:
    """The largest number of fixed points on a chain of nested fixed points."""
    best = 0
    stack = [(phi, 0)]
    while stack:
        f, depth = stack.pop()
        op = f[0]
        if op in ("mu", "nu"):
            best = max(best, depth + 1)
            stack.append((f[2], depth + 1))
        elif op in ("and", "or"):
            stack.extend((g, depth) for g in f[1:])
        elif op in ("dia", "box"):
            stack.append((f[1], depth))
    return best


def evaluate(states: Sequence[State], succ: dict, label: dict, phi: Formula, reuse: bool) -> tuple:
    """Return (the set of states that satisfy phi, the number of body evaluations).

    reuse=True is the Emerson-Lei algorithm; reuse=False is naive iteration.
    Precondition: phi is closed, in positive normal form, with each variable
    bound once.
    """
    all_states = frozenset(states)
    info = fixpoints(phi)

    def start(x) -> frozenset:
        return frozenset() if info[x][0] == "mu" else all_states

    value = {x: start(x) for x in info}  # @line L13
    count = 0

    def ev(f: Formula) -> frozenset:
        nonlocal count
        op = f[0]  # @line L1
        if op == "true":  # @line L2
            return all_states
        if op == "false":
            return frozenset()
        if op == "ap":
            return frozenset(s for s in states if f[1] in label[s])
        if op == "nap":
            return frozenset(s for s in states if f[1] not in label[s])
        if op == "var":
            if f[1] not in value:
                raise ValueError(f"free variable {f[1]!r}")
            return value[f[1]]  # @line L3
        if op == "and":
            return ev(f[1]) & ev(f[2])  # @line L4
        if op == "or":
            return ev(f[1]) | ev(f[2])
        if op == "dia":
            a = ev(f[1])
            return frozenset(s for s in states if any(t in a for t in succ[s]))  # @line L5
        if op == "box":
            a = ev(f[1])
            return frozenset(s for s in states if all(t in a for t in succ[s]))
        x, body = f[1], f[2]  # @line L6
        if not reuse:
            value[x] = start(x)
        while True:  # @line L7
            new = ev(body)  # @line L8
            count += 1
            if new == value[x]:  # @line L9
                return new
            value[x] = new  # @line L10
            for y in info[x][2]:  # @line L11
                value[y] = start(y)  # @line L12

    result = ev(phi)  # @line L14
    return set(result), count


def emerson_lei(states: Sequence[State], succ: dict, label: dict, phi: Formula) -> set:
    """The set of states that satisfy phi, by the Emerson-Lei algorithm."""
    return evaluate(states, succ, label, phi, reuse=True)[0]


def naive_iteration(states: Sequence[State], succ: dict, label: dict, phi: Formula) -> set:
    """The set of states that satisfy phi, with each fixed point restarted at each entry."""
    return evaluate(states, succ, label, phi, reuse=False)[0]
