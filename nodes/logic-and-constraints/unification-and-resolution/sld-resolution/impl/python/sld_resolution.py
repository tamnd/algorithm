# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sld-resolution/. The authors are listed in prov/1G4RR0.jsonl.
"""SLD resolution for definite programs, with any computation rule.

A term is a variable, written as a string, or a tuple (f, t1, ..., tn); a
constant is (c,). An atom is a tuple (p, t1, ..., tn). A program is a list of
clauses (head, [body atoms]); a fact has an empty body. A goal is a list of atoms.

solve() searches the SLD tree depth first, with the clauses tried in program
order. A depth bound makes the search finite; without it, the search is
Prolog's search and can run forever.
"""


class StepLimit(Exception):
    """Raised when the search uses more steps than allowed. args[0] holds the answers found so far."""


def is_var(t):
    return isinstance(t, str)


def walk(t, s):
    while is_var(t) and t in s:
        t = s[t]
    return t


def resolve(t, s):
    """Apply the triangular substitution s to t completely."""
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
    """Extend s to a most general unifier of a and b, or return None. s is not changed."""
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


def term_vars(t, out):
    if is_var(t):
        if t not in out:
            out.append(t)
    else:
        for a in t[1:]:
            term_vars(a, out)
    return out


def rename(t, k):
    if is_var(t):
        return f"{t}#{k}"
    return (t[0],) + tuple(rename(a, k) for a in t[1:])


def leftmost(goal):
    return 0


def rightmost(goal):
    return len(goal) - 1


def solve(program, query, rule=leftmost, depth=None, max_steps=None):
    """The computed answers of the query, as dicts from its variables to terms, in the order found."""
    qvars = []
    for atom in query:
        term_vars(atom, qvars)
    answers = []
    fresh = 0
    steps = 0
    stack = [(tuple(query), {}, 0)]  # @line L1
    while stack:  # @line L2
        goal, s, n = stack.pop()  # @line L3
        if not goal:
            answers.append({x: resolve(x, s) for x in qvars})  # @line L4
            continue
        if depth is not None and n >= depth:
            continue  # @line L5
        steps += 1
        if max_steps is not None and steps > max_steps:
            raise StepLimit(answers)
        i = rule([resolve(a, s) for a in goal])  # @line L6
        selected = goal[i]
        children = []
        for head, body in program:  # @line L7
            fresh += 1
            head, body = rename(head, fresh), [rename(b, fresh) for b in body]  # @line L8
            mu = unify(selected, head, s)  # @line L9
            if mu is not None:  # @line L10
                new_goal = goal[:i] + tuple(body) + goal[i + 1 :]  # @line L11
                children.append((new_goal, mu, n + 1))
        stack.extend(reversed(children))  # @line L12
    return answers
