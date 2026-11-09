# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sldnf-resolution/. The authors are listed in prov/N5VQ4A.jsonl.
"""SLDNF resolution for normal programs, with a safe leftmost computation rule.

A term is a variable, written as a string, or a tuple (f, t1, ..., tn); a
constant is (c,). An atom is a tuple (p, t1, ...). A literal is an atom or
("not", atom). A program is a list of clauses (head, [body literals]).

sldnf(program, goal, depth) returns (answers, status). The answers are the
computed answers found, as dicts from the goal variables to terms. The status
is "finite" if the whole SLDNF tree (with its subsidiary trees) was explored,
"cut" if the depth bound cut some branch, and "flounder" if some goal had only
negative literals that are not ground.
"""

FINITE, CUT, FLOUNDER = "finite", "cut", "flounder"


def is_var(t):
    return isinstance(t, str)


def walk(t, s):
    while is_var(t) and t in s:
        t = s[t]
    return t


def resolve(t, s):
    t = walk(t, s)
    if is_var(t):
        return t
    return (t[0],) + tuple(resolve(a, s) for a in t[1:])


def occurs(x, t, s):
    t = walk(t, s)
    if is_var(t):
        return t == x
    return any(occurs(x, a, s) for a in t[1:])


def unify(a, b, s):
    s = dict(s)
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        x, y = walk(x, s), walk(y, s)
        if x == y:
            continue
        if is_var(y) and not is_var(x):
            x, y = y, x
        if is_var(x):
            if occurs(x, y, s):
                return None
            s[x] = y
        elif x[0] != y[0] or len(x) != len(y):
            return None
        else:
            stack.extend(zip(x[1:], y[1:]))
    return s


def is_ground(t):
    return not is_var(t) and all(is_ground(a) for a in t[1:])


def term_vars(t, out):
    if is_var(t):
        if t not in out:
            out.append(t)
    else:
        for a in t[1:]:
            term_vars(a, out)
    return out


def negative(lit):
    return lit[0] == "not"


def rename(lit, k):
    if is_var(lit):
        return f"{lit}#{k}"
    return (lit[0],) + tuple(rename(a, k) for a in lit[1:])


def worst(a, b):
    order = {FINITE: 0, CUT: 1, FLOUNDER: 2}
    return a if order[a] >= order[b] else b


class _Counter:
    n = 0


def _tree(program, goal, s, depth, counter):
    """Explore the SLDNF tree below (goal, s). Return (list of substitutions at success leaves, status)."""
    if not goal:
        return [s], FINITE  # @line L1
    if depth == 0:
        return [], CUT  # @line L2
    goal = [resolve(lit, s) for lit in goal]
    pick = next((i for i, lit in enumerate(goal) if not negative(lit) or is_ground(lit)), None)  # @line L3
    if pick is None:
        return [], FLOUNDER  # @line L4
    lit = goal[pick]
    rest = goal[:pick] + goal[pick + 1 :]
    if negative(lit):  # @line L5
        sub, status = _tree(program, [lit[1]], {}, depth - 1, counter)  # @line L6
        if sub:
            return [], FINITE  # @line L7
        if status != FINITE:
            return [], status  # @line L8
        return _tree(program, rest, s, depth - 1, counter)  # @line L9
    found, status = [], FINITE  # @line L10
    for head, body in program:  # @line L11
        counter.n += 1
        head, body = rename(head, counter.n), [rename(b, counter.n) for b in body]
        mu = unify(lit, head, s)  # @line L12
        if mu is not None:
            new_goal = goal[:pick] + body + goal[pick + 1 :]
            sub, st = _tree(program, new_goal, mu, depth - 1, counter)  # @line L13
            found += sub
            status = worst(status, st)
    return found, status  # @line L14


def sldnf(program, goal, depth=50):
    qvars = []
    for lit in goal:
        term_vars(lit, qvars)
    leaves, status = _tree(program, list(goal), {}, depth, _Counter())
    return [{x: resolve(x, s) for x in qvars} for s in leaves], status
