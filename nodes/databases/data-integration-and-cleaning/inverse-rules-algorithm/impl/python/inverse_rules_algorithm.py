# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-rules-algorithm/. The authors are listed in prov/TPC6ZK.jsonl.

"""The inverse rules algorithm of Duschka and Genesereth.

An atom is a pair (predicate, tuple of terms). In a rule, every term is a
variable (a string) or, in the head of an inverse rule only, a Skolem term
("f", view, variable, tuple of head variables). A rule is a pair (head atom,
list of body atoms). A Datalog query is a pair (rules, goal predicate); its
rules use the global predicates and their own predicates. A view is a pair
(head, body) of a conjunctive query whose head has distinct variables, and
views is a dict from view name to view. A view instance is a dict from view
name to a set of tuples of constants. A value in a derived fact is a constant
(a string) or a ground Skolem term ("f", view, variable, tuple of values).
Set semantics holds throughout.
"""


def is_function_term(v):
    return isinstance(v, tuple)


def inverse_rules(views):
    """For each view and each atom of its body, one rule that derives the atom."""
    rules = []  # @line L1
    for name in sorted(views):  # @line L2
        vhead, vbody = views[name]
        sigma = {y: y for y in vhead}  # @line L3
        for _, args in vbody:
            for u in args:
                if u not in sigma:
                    sigma[u] = ("f", name, u, tuple(vhead))
        for pred, args in vbody:  # @line L4
            rules.append(((pred, tuple(sigma[u] for u in args)), [(name, tuple(vhead))]))  # @line L5
    return rules


def _matches(atoms, facts, binding):
    """Yield each extension of binding that maps every atom to a fact."""
    if not atoms:
        yield binding
        return
    pred, args = atoms[0]
    for tup in facts.get(pred, ()):
        if len(tup) != len(args):
            continue
        new = dict(binding)
        ok = True
        for a, v in zip(args, tup):
            if new.setdefault(a, v) != v:
                ok = False
                break
        if ok:
            yield from _matches(atoms[1:], facts, new)


def _ground(term, binding):
    if is_function_term(term):
        f, view, var, args = term
        return (f, view, var, tuple(binding[a] for a in args))
    return binding[term]


def fixpoint(rules, facts):
    """The least model of the rules over the facts, by naive iteration."""
    model = {p: set(ts) for p, ts in facts.items()}
    changed = True
    while changed:
        changed = False
        for (hpred, hargs), body in rules:
            new = set()
            for m in _matches(list(body), model, {}):
                new.add(tuple(_ground(t, m) for t in hargs))
            target = model.setdefault(hpred, set())
            if not new <= target:
                target |= new
                changed = True
    return model


def inverse_rules_answers(query, views, view_instance):
    """The certain answers of a Datalog query over the views, under the open world assumption."""
    rules, goal = query
    program = list(rules) + inverse_rules(views)  # @line L6
    model = fixpoint(program, view_instance)  # @line L7
    return {t for t in model.get(goal, set()) if not any(is_function_term(v) for v in t)}  # @line L8


def cq_as_program(query):
    """A conjunctive query (head, body) as a one-rule Datalog query with goal 'q'."""
    head, body = query
    return ([(("q", tuple(head)), list(body))], "q")
