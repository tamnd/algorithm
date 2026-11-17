# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magic-sets/. The authors are listed in prov/SCYM7S.jsonl.
"""The magic sets transformation of a Datalog program for a query with constants.

A term is a variable (a str) or a constant (an int). An atom is (predicate, tuple of terms).
A rule is (head atom, list of body atoms); a rule with an empty body and a ground head is a
fact. A program is a list of rules; the IDB predicates are those that occur in a head.
The adorned copy of predicate p with adornment a (a string of 'b' and 'f') is named
"p_a", and its magic predicate is "magic_p_a".
"""


def _is_var(t) -> bool:
    return isinstance(t, str)


def idb_predicates(program) -> set:
    return {head[0] for head, _ in program}


def _adornment(terms, bound: set) -> str:
    return "".join("b" if (not _is_var(t) or t in bound) else "f" for t in terms)


def _bound_part(terms, adornment: str) -> tuple:
    return tuple(t for t, c in zip(terms, adornment) if c == "b")


def magic_rewrite(program, query) -> tuple[list, str]:
    """Rewrite program for the query atom. Return the new program and the name of the
    adorned query predicate. Uses the left-to-right sideways information passing."""
    idb = idb_predicates(program)
    qpred, qterms = query
    a = _adornment(qterms, set())  # @line L1
    todo, done, out = [(qpred, a)], set(), []  # @line L2
    while todo:  # @line L3
        p, a = todo.pop()  # @line L4
        if (p, a) in done:
            continue
        done.add((p, a))
        for (hp, hterms), body in program:  # @line L5
            if hp != p:
                continue
            magic_head = ("magic_%s_%s" % (p, a), _bound_part(hterms, a))
            bound = {t for t, c in zip(hterms, a) if c == "b" and _is_var(t)}  # @line L6
            new_body = []
            for bp, bterms in body:  # @line L7
                if bp in idb:  # @line L8
                    b = _adornment(bterms, bound)  # @line L9
                    if (bp, b) not in done:
                        todo.append((bp, b))
                    magic_atom = ("magic_%s_%s" % (bp, b), _bound_part(bterms, b))
                    out.append((magic_atom, [magic_head] + list(new_body)))  # @line L10
                    new_body.append(("%s_%s" % (bp, b), bterms))
                else:
                    new_body.append((bp, bterms))
                bound |= {t for t in bterms if _is_var(t)}  # @line L11
            out.append((("%s_%s" % (p, a), hterms), [magic_head] + new_body))  # @line L12
    q_adornment = _adornment(qterms, set())
    seed = ("magic_%s_%s" % (qpred, q_adornment), _bound_part(qterms, q_adornment))
    out.append((seed, []))  # @line L13
    return out, "%s_%s" % (qpred, q_adornment)


def _fire(head, body, sources, out: set) -> None:
    def search(i: int, theta: dict) -> None:
        if i == len(body):
            out.add((head[0], tuple(theta[t] if _is_var(t) else t for t in head[1])))
            return
        pred, terms = body[i]
        for args in sources[i].get(pred, ()):
            if len(args) != len(terms):
                continue
            new = dict(theta)
            ok = True
            for t, v in zip(terms, args):
                if _is_var(t):
                    if new.setdefault(t, v) != v:
                        ok = False
                        break
                elif t != v:
                    ok = False
                    break
            if ok:
                search(i + 1, new)

    search(0, {})


def _index(facts) -> dict:
    out = {}
    for pred, args in facts:
        out.setdefault(pred, set()).add(args)
    return out


def evaluate(program, database) -> set:
    """The least model, by semi-naive evaluation (IDB atoms before the new one read old facts)."""
    idb = idb_predicates(program)
    base = _index(database)
    found = set()
    for head, body in program:
        if not any(p in idb for p, _ in body):
            _fire(head, body, [base] * len(body), found)
    delta = found - set(database)
    model = set(database) | delta
    while delta:
        old, new, full = _index(model - delta), _index(delta), _index(model)
        found = set()
        for head, body in program:
            pos = [k for k, (p, _) in enumerate(body) if p in idb]
            for j in pos:
                sources = [old if (k in pos and k < j) else full for k in range(len(body))]
                sources[j] = new
                _fire(head, body, sources, found)
        delta = found - model
        model |= delta
    return model


def _matches(args, terms) -> bool:
    theta = {}
    for t, v in zip(terms, args):
        if _is_var(t):
            if theta.setdefault(t, v) != v:
                return False
        elif t != v:
            return False
    return True


def answer_with_magic(program, database, query) -> tuple[set, int]:
    """Answers of the query by the rewritten program, and the number of IDB facts it derived."""
    rewritten, qname = magic_rewrite(program, query)
    model = evaluate(rewritten, database)  # @line L14
    answers = {args for p, args in model if p == qname and _matches(args, query[1])}
    return answers, len(model) - len(set(database))


def answer_full(program, database, query) -> tuple[set, int]:
    """Answers of the query from the whole least model, and the number of IDB facts derived."""
    model = evaluate(program, database)
    answers = {args for p, args in model if p == query[0] and _matches(args, query[1])}
    return answers, len(model) - len(set(database))
