# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-naive-evaluation/. The authors are listed in prov/EVCHB0.jsonl.
"""Naive and semi-naive bottom-up evaluation of Datalog programs.

A fact is (predicate, tuple of constants). An atom is (predicate, tuple of terms), where a
term is a variable (a str) or a constant (an int). A rule is (head atom, list of body atoms),
and every variable of the head occurs in the body. A program is a list of rules. The IDB
predicates are those that occur in some head; the others are EDB predicates.

Each function returns (model, firings), where firings counts the rule instances whose body
was found true, that is, the derivations done.
"""


def idb_predicates(program) -> set:
    return {head[0] for head, _ in program}


def _index(facts) -> dict:
    out = {}
    for pred, args in facts:
        out.setdefault(pred, set()).add(args)
    return out


def _fire(head, body, sources, out: set) -> int:
    """Add to out the head of each instance of the rule whose body atom i is in sources[i].

    sources[i] is a dict from predicate to a set of tuples. Return the number of instances."""
    count = 0

    def search(i: int, theta: dict) -> None:
        nonlocal count
        if i == len(body):
            out.add((head[0], tuple(theta[t] if isinstance(t, str) else t for t in head[1])))
            count += 1
            return
        pred, terms = body[i]
        for args in sources[i].get(pred, ()):
            if len(args) != len(terms):
                continue
            new = dict(theta)
            ok = True
            for t, a in zip(terms, args):
                if isinstance(t, str):
                    if new.setdefault(t, a) != a:
                        ok = False
                        break
                elif t != a:
                    ok = False
                    break
            if ok:
                search(i + 1, new)

    search(0, {})
    return count


def naive(program, database) -> tuple[set, int]:
    """Apply all rules to the whole set of facts until nothing new appears."""
    model = set(database)
    firings = 0
    while True:
        index = _index(model)
        new = set()
        for head, body in program:
            firings += _fire(head, body, [index] * len(body), new)
        if new <= model:
            return model, firings
        model |= new


def semi_naive(program, database) -> tuple[set, int]:
    """Semi-naive evaluation. In each round, a rule instance is used only if one of its IDB
    body atoms is a fact that is new in the last round. IDB atoms before that position use
    the old facts and atoms after it use all facts, so no instance is fired twice."""
    idb = idb_predicates(program)
    if any(pred in idb for pred, _ in database):
        raise ValueError("the database must hold EDB facts only")
    empty_idb = _index(database)
    out = set()
    firings = 0
    for head, body in program:
        if not any(pred in idb for pred, _ in body):
            firings += _fire(head, body, [empty_idb] * len(body), out)
    delta = out - set(database)  # @line L1
    model = set(database) | delta  # @line L2
    while delta:  # @line L3
        old = _index(model - delta)  # @line L4
        new_index = _index(delta)
        full = _index(model)
        found = set()  # @line L5
        for head, body in program:  # @line L6
            positions = [k for k, (pred, _) in enumerate(body) if pred in idb]
            for j in positions:
                sources = [old if (k in positions and k < j) else full for k in range(len(body))]
                sources[j] = new_index
                firings += _fire(head, body, sources, found)  # @line L7
        delta = found - model  # @line L8
        model |= delta  # @line L9
    return model, firings  # @line L10


def semi_naive_basic(program, database) -> tuple[set, int]:
    """The basic form: one IDB atom over the new facts and all other atoms over all facts.
    The model is the same, but a rule with two IDB atoms can fire an instance twice."""
    idb = idb_predicates(program)
    edb_only = {p: s for p, s in _index(database).items() if p not in idb}
    out = set()
    firings = 0
    for head, body in program:
        if not any(pred in idb for pred, _ in body):
            firings += _fire(head, body, [edb_only] * len(body), out)
    delta = out - set(database)
    model = set(database) | delta
    while delta:
        new_index = _index(delta)
        full = _index(model)
        found = set()
        for head, body in program:
            for j, (pred, _) in enumerate(body):
                if pred in idb:
                    sources = [full] * len(body)
                    sources[j] = new_index
                    firings += _fire(head, body, sources, found)
        delta = found - model
        model |= delta
    return model, firings


def count_true_instances(program, model) -> int:
    """The number of rule instances whose body is true in the model."""
    index = _index(model)
    sink = set()
    return sum(_fire(head, body, [index] * len(body), sink) for head, body in program)
