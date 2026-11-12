# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dred-algorithm/. The authors are listed in prov/K2D6D5.jsonl.
"""DRed (delete and rederive): incremental maintenance of the least model of a Datalog program.

A term is a variable (a str) or a constant (an int). An atom is (predicate, tuple of terms),
a fact is (predicate, tuple of ints), and a rule is (head atom, list of body atoms). The IDB
predicates are those that occur in a head; the stored facts E use the other predicates.
The model M is E together with all derived facts.
"""


def _is_var(t) -> bool:
    return isinstance(t, str)


def idb_predicates(program) -> set:
    return {head[0] for head, _ in program}


def _index(facts) -> dict:
    out = {}
    for pred, args in facts:
        out.setdefault(pred, set()).add(args)
    return out


def _bind(terms, args, theta: dict):
    if len(terms) != len(args):
        return None
    new = dict(theta)
    for t, v in zip(terms, args):
        if _is_var(t):
            if new.setdefault(t, v) != v:
                return None
        elif t != v:
            return None
    return new


def _search(body, sources, theta: dict, i: int = 0):
    """Yield each map of the variables that makes body atom k a fact of sources[k], k >= i."""
    if i == len(body):
        yield theta
        return
    pred, terms = body[i]
    for args in sources[i].get(pred, ()):
        new = _bind(terms, args, theta)
        if new is not None:
            yield from _search(body, sources, new, i + 1)


def _head(head, theta: dict) -> tuple:
    return (head[0], tuple(theta[t] if _is_var(t) else t for t in head[1]))


def _consequences(program, model: dict, delta: dict) -> set:
    """Heads of the rule instances that are true in model and use a fact of delta."""
    out = set()
    for head, body in program:
        for j in range(len(body)):
            if body[j][0] not in delta:
                continue
            sources = [model] * len(body)
            sources[j] = delta
            for theta in _search(body, sources, {}):
                out.add(_head(head, theta))
    return out


def least_model(program, edb) -> set:
    """Recompute the least model from scratch, by naive evaluation. Used as the oracle."""
    model = set(edb)
    while True:
        index = _index(model)
        new = set()
        for head, body in program:
            for theta in _search(body, [index] * len(body), {}):
                new.add(_head(head, theta))
        if new <= model:
            return model
        model |= new


def dred(program, edb: set, model: set, deletions, insertions):
    """Apply the deletions and insertions of stored facts. Return the new stored facts, the new
    model, and the numbers of IDB facts that were overdeleted, rederived and inserted."""
    idb = idb_predicates(program)
    if any(p in idb for p, _ in list(deletions) + list(insertions)):
        raise ValueError("only stored (EDB) facts can be inserted or deleted")
    ins = set(insertions) - edb  # @line L1
    dels = (set(deletions) & edb) - set(insertions)
    gone, delta = set(dels), set(dels)  # @line L2
    old = _index(model)
    while delta:  # @line L3
        found = _consequences(program, old, _index(delta))  # @line L4
        delta = found - gone  # @line L5
        gone |= delta
    model = model - gone  # @line L6
    edb = (edb - dels) | ins
    current = _index(model)
    rederived = set()
    for head, body in program:  # @line L7
        for f in gone:
            if f[0] != head[0]:
                continue
            theta = _bind(head[1], f[1], {})
            if theta is not None and next(_search(body, [current] * len(body), theta), None) is not None:
                rederived.add(f)
    delta = rederived | ins  # @line L8
    model = model | delta
    inserted = 0
    while delta:  # @line L9
        found = _consequences(program, _index(model), _index(delta))  # @line L10
        delta = found - model  # @line L11
        model |= delta
        inserted += len(delta)
    overdeleted = len(gone) - len(dels)
    return edb, model, overdeleted, len(rederived), inserted  # @line L12
