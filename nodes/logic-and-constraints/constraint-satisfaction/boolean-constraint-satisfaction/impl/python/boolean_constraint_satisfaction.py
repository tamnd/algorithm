# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boolean-constraint-satisfaction/. The authors are listed in prov/3NGE2G.jsonl.

"""Schaefer's six classes of Boolean relations, and a solver for each class.

A Boolean relation of arity r is a set of r-tuples of 0 and 1. An instance has
the variables 0 .. n-1 and a list of constraints (scope, relation), where scope
is a tuple of distinct variables with one entry for each place of the relation.
"""

import itertools
from collections.abc import Callable, Iterable, Sequence

Relation = set[tuple[int, ...]]
Instance = Sequence[tuple[tuple[int, ...], Relation]]

# The polymorphism of each class: (arity, operation on 0/1 values).
POLYMORPHISM: dict[str, tuple[int, Callable[..., int]]] = {
    "0-valid": (1, lambda x: 0),
    "1-valid": (1, lambda x: 1),
    "horn": (2, lambda x, y: x & y),
    "dual-horn": (2, lambda x, y: x | y),
    "bijunctive": (3, lambda x, y, z: (x & y) | (x & z) | (y & z)),
    "affine": (3, lambda x, y, z: x ^ y ^ z),
}


def closed_under(rel: Relation, k: int, op: Callable[..., int]) -> bool:
    """True if applying op coordinate by coordinate to any k tuples of rel gives a tuple of rel."""
    for rows in itertools.product(rel, repeat=k):
        if tuple(op(*col) for col in zip(*rows)) not in rel:
            return False
    return True


# A clause over the places 0 .. r-1 is a tuple of literals (place, sign); sign 1 is x, sign 0 is not x.
def _clauses(r: int, ok: Callable[[int, int], bool]) -> list[tuple[tuple[int, int], ...]]:
    out = []
    for choice in itertools.product((None, 0, 1), repeat=r):
        lits = tuple((i, s) for i, s in enumerate(choice) if s is not None)
        pos = sum(1 for _, s in lits if s == 1)
        if ok(pos, len(lits) - pos):
            out.append(lits)
    return out


def _sat(t: tuple[int, ...], clause: tuple[tuple[int, int], ...]) -> bool:
    return any(t[i] == s for i, s in clause)


def _defined_by_clauses(r: int, rel: Relation, ok: Callable[[int, int], bool]) -> bool:
    """True if rel is the set of models of the clauses of the given shape that rel satisfies."""
    implied = [c for c in _clauses(r, ok) if all(_sat(t, c) for t in rel)]
    models = {t for t in itertools.product((0, 1), repeat=r) if all(_sat(t, c) for c in implied)}
    return models == rel


def _affine_equations(r: int, rel: Relation) -> list[tuple[tuple[int, ...], int]]:
    """All equations a . x = c over GF(2) that every tuple of rel satisfies."""
    eqs = []
    for a in itertools.product((0, 1), repeat=r):
        for c in (0, 1):
            if all(sum(x & y for x, y in zip(a, t)) % 2 == c for t in rel):
                eqs.append((a, c))
    return eqs


def is_in_class(name: str, r: int, rel: Relation) -> bool:
    """Recognize Schaefer's classes from their definitions, not from the polymorphisms."""
    if name == "0-valid":
        return (0,) * r in rel
    if name == "1-valid":
        return (1,) * r in rel
    if name == "horn":
        return _defined_by_clauses(r, rel, lambda pos, neg: pos <= 1)
    if name == "dual-horn":
        return _defined_by_clauses(r, rel, lambda pos, neg: neg <= 1)
    if name == "bijunctive":
        return _defined_by_clauses(r, rel, lambda pos, neg: pos + neg <= 2)
    if name == "affine":
        eqs = _affine_equations(r, rel)
        models = {t for t in itertools.product((0, 1), repeat=r)
                  if all(sum(x & y for x, y in zip(a, t)) % 2 == c for a, c in eqs)}
        return models == rel
    raise ValueError(name)


def schaefer_classes(language: Iterable[tuple[int, Relation]]) -> list[str]:
    """The classes that contain every relation (arity, rel) of the language."""
    lang = list(language)
    return [name for name in POLYMORPHISM if all(is_in_class(name, r, rel) for r, rel in lang)]


def _horn(n: int, clauses: list[tuple[list[int], int | None]]) -> list[int] | None:
    """Least model of Horn clauses (body, head) by forward chaining, in linear time."""
    value = [0] * n
    missing = [len(set(body)) for body, _ in clauses]
    watch: list[list[int]] = [[] for _ in range(n)]
    for k, (body, _) in enumerate(clauses):
        for v in set(body):
            watch[v].append(k)
    stack = [k for k in range(len(clauses)) if missing[k] == 0]
    while stack:
        k = stack.pop()
        head = clauses[k][1]
        if head is None:
            return None
        if value[head]:
            continue
        value[head] = 1
        for k2 in watch[head]:
            missing[k2] -= 1
            if missing[k2] == 0:
                stack.append(k2)
    return value


def _two_sat(n: int, clauses: list[list[tuple[int, int]]]) -> list[int] | None:
    """2-SAT by strongly connected components of the implication graph (Kosaraju)."""
    def node(v: int, s: int) -> int:
        return 2 * v + (1 - s)  # literal x_v = s; node 2v is "x_v = 1"

    graph: list[list[int]] = [[] for _ in range(2 * n)]
    for cl in clauses:
        if not cl:
            return None
        a = cl[0]
        b = cl[1] if len(cl) == 2 else cl[0]
        graph[node(a[0], 1 - a[1])].append(node(b[0], b[1]))
        graph[node(b[0], 1 - b[1])].append(node(a[0], a[1]))
    finish: list[int] = []
    seen = [False] * (2 * n)
    for s in range(2 * n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, 0)]
        while stack:
            v, k = stack.pop()
            if k < len(graph[v]):
                stack.append((v, k + 1))
                w = graph[v][k]
                if not seen[w]:
                    seen[w] = True
                    stack.append((w, 0))
            else:
                finish.append(v)
    rev: list[list[int]] = [[] for _ in range(2 * n)]
    for v in range(2 * n):
        for w in graph[v]:
            rev[w].append(v)
    comp = [-1] * (2 * n)
    c = 0
    for s in reversed(finish):
        if comp[s] >= 0:
            continue
        comp[s] = c
        stack2 = [s]
        while stack2:
            v = stack2.pop()
            for w in rev[v]:
                if comp[w] < 0:
                    comp[w] = c
                    stack2.append(w)
        c += 1
    value = []
    for v in range(n):
        if comp[2 * v] == comp[2 * v + 1]:
            return None
        value.append(1 if comp[2 * v] > comp[2 * v + 1] else 0)
    return value


def _gauss(n: int, eqs: list[tuple[int, int]]) -> tuple[int, list[int]] | None:
    """Solve equations (mask, c) over GF(2). Return (rank, one solution) or None."""
    pivots: dict[int, tuple[int, int]] = {}
    for mask, c in eqs:
        for p, (pm, pc) in pivots.items():
            if mask >> p & 1:
                mask ^= pm
                c ^= pc
        if mask == 0:
            if c:
                return None
            continue
        p = mask.bit_length() - 1
        for q, (qm, qc) in list(pivots.items()):
            if qm >> p & 1:
                pivots[q] = (qm ^ mask, qc ^ c)
        pivots[p] = (mask, c)
    value = [0] * n
    for p, (_, c) in pivots.items():
        value[p] = c  # free variables are 0; each pivot row holds one pivot only
    return len(pivots), value


def _check_scopes(n: int, instance: Instance) -> None:
    for scope, _ in instance:
        if len(set(scope)) != len(scope) or any(not 0 <= v < n for v in scope):
            raise ValueError("a scope is a tuple of distinct variables")


def solve(n: int, instance: Instance) -> list[int] | None:
    """Solve an instance whose relations all lie in one of Schaefer's classes."""
    _check_scopes(n, instance)
    classes = schaefer_classes((len(s), rel) for s, rel in instance)
    if not classes:
        raise ValueError("the relations are in none of Schaefer's classes")
    name = classes[0]
    if name == "0-valid":
        return [0] * n
    if name == "1-valid":
        return [1] * n
    if name in ("horn", "dual-horn"):
        flip = 1 if name == "dual-horn" else 0  # dual Horn becomes Horn when 0 and 1 swap
        horn: list[tuple[list[int], int | None]] = []
        for scope, rel in instance:
            r = len(scope)
            frel = {tuple(x ^ flip for x in t) for t in rel}
            for c in _clauses(r, lambda pos, neg: pos <= 1):
                if all(_sat(t, c) for t in frel):
                    body = [scope[i] for i, s in c if s == 0]
                    heads = [scope[i] for i, s in c if s == 1]
                    horn.append((body, heads[0] if heads else None))
        value = _horn(n, horn)
        return None if value is None else [x ^ flip for x in value]
    if name == "bijunctive":
        two: list[list[tuple[int, int]]] = []
        for scope, rel in instance:
            for c in _clauses(len(scope), lambda pos, neg: pos + neg <= 2):
                if all(_sat(t, c) for t in rel):
                    two.append([(scope[i], s) for i, s in c])
        return _two_sat(n, two)
    eqs = [(sum(1 << scope[i] for i in range(len(scope)) if a[i]), c)
           for scope, rel in instance for a, c in _affine_equations(len(scope), rel)]
    res = _gauss(n, eqs)
    return None if res is None else res[1]


def count_affine(n: int, instance: Instance) -> int:
    """Number of solutions of an instance whose relations are all affine: 0 or 2^(n - rank)."""
    _check_scopes(n, instance)
    if not all(is_in_class("affine", len(s), rel) for s, rel in instance):
        raise ValueError("a relation is not affine")
    eqs = [(sum(1 << scope[i] for i in range(len(scope)) if a[i]), c)
           for scope, rel in instance for a, c in _affine_equations(len(scope), rel)]
    res = _gauss(n, eqs)
    return 0 if res is None else 2 ** (n - res[0])
