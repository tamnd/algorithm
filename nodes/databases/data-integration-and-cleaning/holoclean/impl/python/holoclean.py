# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holoclean/. The authors are listed in prov/DV1WKR.jsonl.

"""A small model of the HoloClean repair pipeline, for teaching and testing.

This is not the HoloClean system. It keeps its main steps: error detection
by denial constraints, domain pruning by co-occurrence, features from
co-occurrence statistics, a minimality prior and relaxed denial constraints,
weights learned on the clean cells, and inference of the most likely value of
each noisy cell. It also has a joint model with pairwise constraint factors
and a Gibbs sampler for it.

A table is a list of rows; each row is a tuple of strings, one per attribute.
A cell is a pair (row index, attribute index). A denial constraint is a list
of predicates (a, op, b), read as t1[a] op t2[b] for two different rows t1
and t2, and the constraint says that no pair of rows makes all predicates
true. op is one of "=", "!=", "<", ">".
"""

import math

OPS = {
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
}


def violates(dc, r1, r2):
    """True if the ordered pair of rows (r1, r2) makes every predicate of dc true."""
    return all(OPS[op](r1[a], r2[b]) for a, op, b in dc)


def dc_attributes(dc):
    return sorted({a for a, _, _ in dc} | {b for _, _, b in dc})


def detect_errors(rows, dcs):
    """The noisy cells: the cells of the attributes of a constraint, in each pair of rows that violates it."""
    noisy = set()
    for dc in dcs:
        attrs = dc_attributes(dc)
        for i, r1 in enumerate(rows):
            for j, r2 in enumerate(rows):
                if i != j and violates(dc, r1, r2):
                    for a in attrs:
                        noisy.add((i, a))
                        noisy.add((j, a))
    return noisy


def cooccurrence(rows):
    """Counts of single values and of value pairs within a row."""
    single, pair = {}, {}
    for r in rows:
        for a, v in enumerate(r):
            single[(a, v)] = single.get((a, v), 0) + 1
            for b, u in enumerate(r):
                if a != b:
                    pair[(a, v, b, u)] = pair.get((a, v, b, u), 0) + 1
    return single, pair


def prune_domain(rows, cell, tau, stats):
    """The candidate values of a cell: its own value and each value v of its
    attribute with Pr[v | value of another cell of the row] >= tau."""
    single, pair = stats
    i, a = cell
    row = rows[i]
    values = sorted({r[a] for r in rows})
    dom = {row[a]}
    for v in values:
        for b, u in enumerate(row):
            if b != a and pair.get((a, v, b, u), 0) >= tau * single[(b, u)]:
                dom.add(v)
                break
    return sorted(dom)


def relaxed_violations(rows, cell, value, dc):
    """The number of other rows that form a violation of dc with row i when the
    cell takes value and every other cell keeps its observed value."""
    i, a = cell
    r = list(rows[i])
    r[a] = value
    count = 0
    for j, other in enumerate(rows):
        if j != i and (violates(dc, r, other) or violates(dc, other, r)):
            count += 1
    return count


def features(rows, cell, value, dcs, stats):
    """The learnable features of a candidate value: the co-occurrence statistic
    Pr[value | value of cell (i, b)] for each other attribute b, and the relaxed
    violation count of each constraint."""
    single, pair = stats
    i, a = cell
    f = {}
    for b, u in enumerate(rows[i]):
        if b != a:
            f[("co", a, b)] = pair.get((a, value, b, u), 0) / single[(b, u)]
    for k, dc in enumerate(dcs):
        if a in dc_attributes(dc):
            n = relaxed_violations(rows, cell, value, dc)
            if n:
                f[("dc", k)] = float(n)
    return f


def _softmax(scores):
    top = max(scores)
    ex = [math.exp(s - top) for s in scores]
    z = sum(ex)
    return [e / z for e in ex]


def _score(w, f, prior, is_init):
    return sum(w.get(k, 0.0) * x for k, x in f.items()) + (prior if is_init else 0.0)


def learn(examples, prior, epochs=60, rate=0.5, l2=0.01):
    """Full-batch gradient ascent on the regularized log-likelihood of the labels.

    Each example is a list of (features, is_initial_value, is_label), one entry
    per candidate value of a clean cell.
    """
    w = {}
    n = max(1, len(examples))
    for _ in range(epochs):
        grad = {}
        for cands in examples:
            probs = _softmax([_score(w, f, prior, init) for f, init, _ in cands])
            for (f, _, label), p in zip(cands, probs):
                for k, x in f.items():
                    grad[k] = grad.get(k, 0.0) + ((1.0 if label else 0.0) - p) * x
        for k in set(grad) | set(w):
            w[k] = w.get(k, 0.0) + rate * (grad.get(k, 0.0) / n - l2 * w.get(k, 0.0))
    return w


def holoclean(rows, dcs, tau=0.5, prior=1.0, epochs=60):
    """Repair the noisy cells. Returns (repaired rows, marginals, noisy cells).

    marginals maps each noisy cell to a dict from candidate value to probability.
    """
    noisy = detect_errors(rows, dcs)  # @line L1
    stats = cooccurrence(rows)
    ncols = len(rows[0]) if rows else 0
    cells = [(i, a) for i in range(len(rows)) for a in range(ncols)]
    dom = {}
    for c in cells:  # @line L2
        dom[c] = prune_domain(rows, c, tau, stats)  # @line L3
    feats = {}
    for c in cells:  # @line L4
        for d in dom[c]:
            feats[(c, d)] = features(rows, c, d, dcs, stats)  # @line L5
    examples = []
    for c in cells:
        if c not in noisy and len(dom[c]) > 1:
            init = rows[c[0]][c[1]]
            examples.append([(feats[(c, d)], d == init, d == init) for d in dom[c]])
    w = learn(examples, prior, epochs)  # @line L6
    repaired = [list(r) for r in rows]
    marginals = {}
    for c in sorted(noisy):  # @line L7
        init = rows[c[0]][c[1]]
        probs = _softmax([_score(w, feats[(c, d)], prior, d == init) for d in dom[c]])  # @line L8
        marginals[c] = dict(zip(dom[c], probs))
        best = max(range(len(probs)), key=lambda k: (probs[k], dom[c][k] == init))
        repaired[c[0]][c[1]] = dom[c][best]  # @line L9
    return [tuple(r) for r in repaired], marginals, noisy  # @line L10


def joint_model(rows, dcs, noisy, dom, unary, weight):
    """The pair factors of the joint model: for each constraint and each pair of
    rows that share a noisy cell of its attributes, one factor of the given weight.

    unary maps (cell, value) to a score. Returns (cells, dom, unary, factors).
    """
    cells = sorted(noisy)
    factors = []
    for k, dc in enumerate(dcs):
        attrs = dc_attributes(dc)
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                if any((i, a) in noisy or (j, a) in noisy for a in attrs):
                    factors.append((k, i, j, weight))
    return cells, dom, unary, factors


def _assignment_rows(rows, x):
    out = [list(r) for r in rows]
    for (i, a), v in x.items():
        out[i][a] = v
    return out


def log_weight(rows, dcs, model, x):
    """The unnormalized log-probability of a full assignment x of the noisy cells."""
    cells, dom, unary, factors = model
    cur = _assignment_rows(rows, x)
    s = sum(unary[(c, x[c])] for c in cells)
    for k, i, j, w in factors:
        if violates(dcs[k], cur[i], cur[j]) or violates(dcs[k], cur[j], cur[i]):
            s -= w
    return s


def gibbs(rows, dcs, model, sweeps, burn_in, rng):
    """Estimate the marginals of the noisy cells by Gibbs sampling."""
    cells, dom, unary, factors = model
    touching = {c: [f for f in factors if f[1] == c[0] or f[2] == c[0]] for c in cells}
    x = {c: rows[c[0]][c[1]] for c in cells}  # @line L11
    cur = _assignment_rows(rows, x)
    counts = {c: {d: 0 for d in dom[c]} for c in cells}
    for s in range(sweeps):  # @line L12
        for c in cells:  # @line L13
            i, a = c
            scores = []
            for d in dom[c]:
                cur[i][a] = d
                sc = unary[(c, d)]
                for k, p, q, w in touching[c]:
                    if violates(dcs[k], cur[p], cur[q]) or violates(dcs[k], cur[q], cur[p]):
                        sc -= w
                scores.append(sc)
            probs = _softmax(scores)
            u = rng.random()
            pick = len(probs) - 1
            acc = 0.0
            for k, p in enumerate(probs):
                acc += p
                if u < acc:
                    pick = k
                    break
            x[c] = dom[c][pick]  # @line L14
            cur[i][a] = x[c]
            if s >= burn_in:
                counts[c][x[c]] += 1  # @line L15
    n = sweeps - burn_in
    return {c: {d: counts[c][d] / n for d in dom[c]} for c in cells}  # @line L16
