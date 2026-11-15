# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/system-z/. The authors are listed in prov/8532GG.jsonl.
"""Pearl's System Z for a finite set of propositional conditionals.

A formula is a nested tuple: ("var", name), ("not", f), ("and", f, ...),
("or", f, ...), ("true",) or ("false",). The helpers var, neg, conj, disj and
implies build them. A conditional "if alpha then normally beta" is a pair
(alpha, beta).

partition(rules) returns (layers, rest). layers[i] is the list of the indices
of the rules with Z-rank i. rest holds the indices of the rules that are never
tolerated; it is empty exactly when the set is consistent in Pearl's sense.
kappa(phi, rules) is the Z-rank of a formula, with INF for a formula that no
ranked world satisfies. entails(rules, alpha, beta) decides alpha |~ beta in
System Z, which is the same relation as rational closure.

The only oracle is a satisfiability test: the Tseitin transformation followed
by a small DPLL solver.
"""

from typing import Dict, List, Optional, Tuple

Formula = tuple
Rule = Tuple[Formula, Formula]
Split = Tuple[List[List[int]], List[int]]

INF = float("inf")
TRUE = ("true",)
FALSE = ("false",)


def var(name):
    return ("var", name)


def neg(f):
    return ("not", f)


def conj(*fs):
    return ("and",) + fs if fs else TRUE


def disj(*fs):
    return ("or",) + fs if fs else FALSE


def implies(f, g):
    return disj(neg(f), g)


def evaluate(f, world):
    """The truth value of f in a world, given as a dict from atom names to booleans."""
    op = f[0]
    if op == "var":
        return world[f[1]]
    if op == "not":
        return not evaluate(f[1], world)
    if op == "and":
        return all(evaluate(g, world) for g in f[1:])
    if op == "or":
        return any(evaluate(g, world) for g in f[1:])
    return op == "true"


def atoms(f, out=None):
    out = set() if out is None else out
    if f[0] == "var":
        out.add(f[1])
    else:
        for g in f[1:]:
            atoms(g, out)
    return out


# ---- the satisfiability oracle ----

def _tseitin(f):
    """Clauses over positive and negative ints that are satisfiable exactly when f is."""
    ids, clauses = {}, []

    def lit(g):
        op = g[0]
        if op == "var":
            key = ("var", g[1])
            if key not in ids:
                ids[key] = len(ids) + 1
            return ids[key]
        if op == "not":
            return -lit(g[1])
        x = len(ids) + 1
        ids[("gate", x)] = x
        if op in ("true", "false"):
            clauses.append([x] if op == "true" else [-x])
            return x
        kids = [lit(h) for h in g[1:]]
        if op == "and":
            for k in kids:
                clauses.append([-x, k])
            clauses.append([x] + [-k for k in kids])
        else:
            for k in kids:
                clauses.append([x, -k])
            clauses.append([-x] + kids)
        return x

    clauses.append([lit(f)])
    return clauses


def _dpll(clauses, assignment):
    while True:
        unit = None
        simplified = []
        for c in clauses:
            if any(assignment.get(abs(l)) == (l > 0) for l in c):
                continue
            rest = [l for l in c if abs(l) not in assignment]
            if not rest:
                return False
            if len(rest) == 1 and unit is None:
                unit = rest[0]
            simplified.append(rest)
        clauses = simplified
        if not clauses:
            return True
        if unit is None:
            break
        assignment[abs(unit)] = unit > 0
    pick = clauses[0][0]
    for value in (pick > 0, pick < 0):
        trial = dict(assignment)
        trial[abs(pick)] = value
        if _dpll(clauses, trial):
            return True
    return False


def satisfiable(f: Formula) -> bool:
    """Whether some world satisfies f. Exponential time in the worst case."""
    return _dpll(_tseitin(f), {})


# ---- System Z ----

def material(rule):
    """The material counterpart alpha -> beta of a conditional."""
    return implies(rule[0], rule[1])


def partition(rules: List[Rule]) -> Split:
    """Pearl's tolerance partition. Returns (layers, rest) as lists of rule indices.

    Cost: at most r (r + 1) / 2 satisfiability tests for r rules.
    """
    rest, layers = list(range(len(rules))), []  # @line L1
    while rest:  # @line L2
        m = [material(rules[j]) for j in rest]
        layer = [i for i in rest if satisfiable(conj(rules[i][0], rules[i][1], *m))]  # @line L3
        if not layer:  # @line L4
            return layers, rest
        layers.append(layer)  # @line L5
        rest = [i for i in rest if i not in layer]  # @line L6
    return layers, []  # @line L7


def z_ranks(rules: List[Rule]) -> Dict[int, int]:
    """A dict from rule index to its Z-rank, for the rules that have one."""
    layers, _ = partition(rules)
    return {i: z for z, layer in enumerate(layers) for i in layer}


def _above(rules, layers, rest, i):
    """The material counterparts of the rules in rest and in the layers from i on."""
    chosen = list(rest) + [j for layer in layers[i:] for j in layer]
    return [material(rules[j]) for j in chosen]


def kappa(phi: Formula, rules: List[Rule], split: Optional[Split] = None) -> float:
    """The Z-rank of the formula phi: the least rank of a world that satisfies it.

    Cost after the partition: one test plus a binary search over the layers.
    """
    layers, rest = partition(rules) if split is None else split
    if not satisfiable(conj(phi, *_above(rules, layers, rest, len(layers)))):  # @line L8
        return INF
    lo, hi = 0, len(layers)  # @line L9
    while lo < hi:  # @line L10
        mid = (lo + hi) // 2  # @line L11
        if satisfiable(conj(phi, *_above(rules, layers, rest, mid))):  # @line L12
            hi = mid
        else:
            lo = mid + 1
    return lo  # @line L13


def rank_world(world: Dict[str, bool], rules: List[Rule], split: Optional[Split] = None) -> float:
    """The Z-rank of one world: 0 if it falsifies no rule, else 1 + the largest Z-rank it falsifies."""
    layers, rest = partition(rules) if split is None else split
    falsified = [i for i, (a, b) in enumerate(rules) if evaluate(a, world) and not evaluate(b, world)]
    if any(i in rest for i in falsified):
        return INF
    z = {i: k for k, layer in enumerate(layers) for i in layer}
    return 1 + max(z[i] for i in falsified) if falsified else 0


def entails(rules: List[Rule], alpha: Formula, beta: Formula, split: Optional[Split] = None) -> bool:
    """alpha |~ beta in System Z, which is rational closure."""
    split = partition(rules) if split is None else split  # @line L14
    a = kappa(conj(alpha, beta), rules, split)  # @line L15
    b = kappa(conj(alpha, neg(beta)), rules, split)
    return a < b or b == INF  # @line L16
