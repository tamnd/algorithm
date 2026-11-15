# SPDX-License-Identifier: MIT
# Forward chaining for the page https://algorithm.tamnd.com/forward-chaining/. The authors are listed in prov/.
"""Forward chaining over definite rules with variables, driven by an agenda of new facts.

A fact is a tuple of constants, for example ("parent", "ann", "bob"). A pattern
is a tuple of the same shape in which a term may be a variable, a string that
starts with "?". A rule is (name, body, head): body is a tuple of patterns and
head is one pattern. Each variable of the head must occur in the body (a safe
rule). A rule with an empty body must have a ground head; it is a fact.

forward_chain(rules, facts, goal) returns (found, memory, fired):
- found is True when goal is in the least model (always False when goal is None),
- memory is the set of facts derived so far (the whole least model when the
  run does not stop early at the goal),
- fired is the list of (rule name, new fact) in the order the rules added them.
"""

from collections import deque


def is_var(term):
    return isinstance(term, str) and term.startswith("?")


def match(pattern, fact, binding):
    """Extend binding so that pattern equals fact, or return None."""
    if len(pattern) != len(fact):
        return None
    out = dict(binding)
    for p, f in zip(pattern, fact):
        if is_var(p):
            if p in out:
                if out[p] != f:
                    return None
            else:
                out[p] = f
        elif p != f:
            return None
    return out


def substitute(pattern, binding):
    return tuple(binding[t] if is_var(t) else t for t in pattern)


def check_safe(rules):
    for name, body, head in rules:
        body_vars = {t for p in body for t in p if is_var(t)}
        head_vars = {t for t in head if is_var(t)}
        if not head_vars <= body_vars:
            raise ValueError(f"rule {name} is not safe")


def _joins(body, skip, binding, memory):
    """All extensions of binding that match every body pattern except index skip to facts in memory."""
    rest = [p for j, p in enumerate(body) if j != skip]

    def go(k, b):
        if k == len(rest):
            yield b
            return
        for fact in list(memory):
            b2 = match(rest[k], fact, b)
            if b2 is not None:
                yield from go(k + 1, b2)

    yield from go(0, binding)


def forward_chain(rules, facts, goal=None):
    check_safe(rules)
    memory, agenda = set(), deque()  # @line L1
    fired = []

    def add(fact, name):
        memory.add(fact)
        agenda.append(fact)
        if name is not None:
            fired.append((name, fact))
        return fact == goal

    start = [(tuple(head), name) for name, body, head in rules if not body] + [(tuple(f), None) for f in facts]
    for f, name in start:  # @line L2
        if f not in memory:  # @line L3
            if add(f, name):  # @line L4
                return True, memory, fired
    while agenda:  # @line L5
        f = agenda.popleft()  # @line L6
        for name, body, head in rules:  # @line L7
            for i, pattern in enumerate(body):
                b = match(pattern, f, {})  # @line L8
                if b is None:
                    continue
                for full in _joins(body, i, b, memory):  # @line L9
                    new = substitute(head, full)
                    if new not in memory:  # @line L10
                        if add(new, name):  # @line L11
                            return True, memory, fired
    return False, memory, fired  # @line L12
