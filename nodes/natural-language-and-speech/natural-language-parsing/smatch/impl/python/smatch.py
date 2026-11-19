# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smatch/. The authors are listed in prov/SMYWR9.jsonl.

"""Smatch: the F1 of matching triples between two AMR graphs.

An AMR graph is a set of triples of three kinds:
  ("instance", v, concept)   the variable v is an instance of concept
  (role, v, w)               a relation between two variables
  (role, v, constant)        an attribute with a constant value
A value is a variable if it is the second field of an instance triple.

A mapping sends each variable of the test graph to a distinct variable of the
gold graph, or to None. A test triple matches if its image under the mapping
(constants map to themselves) is a gold triple. M(m) is the number of matched
test triples. Smatch is the F1 of the best mapping:
  P = M / |test|, R = M / |gold|, F = 2 M / (|test| + |gold|).

smatch_brute_force tries every mapping. smatch_hill_climb is the search of Cai
and Knight 2013: steepest ascent over two moves (remap one variable, swap the
images of two variables), started once from a concept-matching mapping and
then from random mappings. It returns a lower bound on the best M.
"""

from fractions import Fraction
from itertools import permutations
import random


def variables(triples):
    """The variables of a graph, in sorted order."""
    return sorted({t[1] for t in triples if t[0] == "instance"})


def match_count(test, gold, mapping):
    """Number of test triples whose image under mapping is in gold."""
    gold = set(gold)
    tvars = set(variables(test))
    count = 0
    for rel, a, b in set(test):
        a2 = mapping.get(a)
        if a2 is None:
            continue
        if rel == "instance" or b not in tvars:
            b2 = b
        else:
            b2 = mapping.get(b)
            if b2 is None:
                continue
        if (rel, a2, b2) in gold:
            count += 1
    return count


def all_mappings(tvars, gvars):
    """Every injective partial map from tvars to gvars (None means unmapped)."""
    m = len(tvars)
    slots = list(gvars) + [None] * m
    seen = set()
    for perm in permutations(slots, m):
        if perm in seen:
            continue
        seen.add(perm)
        yield dict(zip(tvars, perm))


def smatch_brute_force(test, gold):
    """Exact best match count and one best mapping, by trying every mapping."""
    best, best_map = -1, None
    for mapping in all_mappings(variables(test), variables(gold)):
        c = match_count(test, gold, mapping)
        if c > best:
            best, best_map = c, mapping
    return best, best_map


def smart_init(test, gold):
    """Map each test variable to an unused gold variable with the same concept."""
    concept_t = {t[1]: t[2] for t in test if t[0] == "instance"}
    by_concept = {}
    for t in sorted(set(gold)):
        if t[0] == "instance":
            by_concept.setdefault(t[2], []).append(t[1])
    used = set()
    mapping = {}
    for v in variables(test):
        mapping[v] = None
        for g in by_concept.get(concept_t[v], []):
            if g not in used:
                mapping[v] = g
                used.add(g)
                break
    return mapping


def random_init(test, gold, rng):
    """A random injective partial mapping."""
    tvars = variables(test)
    slots = variables(gold) + [None] * len(tvars)
    rng.shuffle(slots)
    return dict(zip(tvars, slots[: len(tvars)]))


def climb(test, gold, mapping):
    """Steepest ascent from mapping; return (M, mapping) at a local maximum."""
    tvars = variables(test)
    gvars = variables(gold)
    mapping = dict(mapping)  # @line L1
    score = match_count(test, gold, mapping)
    while True:  # @line L2
        best_gain, best_move = 0, None
        used = {g for g in mapping.values() if g is not None}
        for a in tvars:  # @line L3
            for g in gvars + [None]:
                if g == mapping[a] or (g is not None and g in used):
                    continue
                trial = dict(mapping)
                trial[a] = g
                gain = match_count(test, gold, trial) - score
                if gain > best_gain:
                    best_gain, best_move = gain, trial
        for i in range(len(tvars)):  # @line L4
            for j in range(i + 1, len(tvars)):
                a, b = tvars[i], tvars[j]
                if mapping[a] == mapping[b]:
                    continue
                trial = dict(mapping)
                trial[a], trial[b] = mapping[b], mapping[a]
                gain = match_count(test, gold, trial) - score
                if gain > best_gain:
                    best_gain, best_move = gain, trial
        if best_move is None:  # @line L5
            return score, mapping
        mapping, score = best_move, score + best_gain  # @line L6


def smatch_hill_climb(test, gold, restarts=4, seed=0):
    """Best (M, mapping) over one smart start and `restarts` random starts."""
    rng = random.Random(seed)
    best, best_map = climb(test, gold, smart_init(test, gold))  # @line L7
    for _ in range(restarts):  # @line L8
        c, m = climb(test, gold, random_init(test, gold, rng))
        if c > best:  # @line L9
            best, best_map = c, m
    return best, best_map  # @line L10


def prf(match, n_test, n_gold):
    """Precision, recall and F1 as Fractions; 0 when undefined."""
    p = Fraction(match, n_test) if n_test else Fraction(0)
    r = Fraction(match, n_gold) if n_gold else Fraction(0)
    f = Fraction(2 * match, n_test + n_gold) if n_test + n_gold else Fraction(0)
    return p, r, f


def smatch(test, gold, exact=False, restarts=4, seed=0):
    """Return (P, R, F) of the best mapping found."""
    if exact:
        m, _ = smatch_brute_force(test, gold)
    else:
        m, _ = smatch_hill_climb(test, gold, restarts, seed)
    return prf(m, len(set(test)), len(set(gold)))


def corpus_smatch(pairs, exact=False, restarts=4, seed=0):
    """Corpus score: sum the matches and the triple counts over all pairs."""
    total_m = total_t = total_g = 0
    for test, gold in pairs:
        if exact:
            m, _ = smatch_brute_force(test, gold)
        else:
            m, _ = smatch_hill_climb(test, gold, restarts, seed)
        total_m += m
        total_t += len(set(test))
        total_g += len(set(gold))
    return prf(total_m, total_t, total_g)


def _tokens(text):
    out = []
    i = 0
    while i < len(text):
        c = text[i]
        if c.isspace():
            i += 1
        elif c in "()/":
            out.append(c)
            i += 1
        elif c == '"':
            j = text.index('"', i + 1)
            out.append(text[i : j + 1])
            i = j + 1
        else:
            j = i
            while j < len(text) and not text[j].isspace() and text[j] not in '()/"':
                j += 1
            out.append(text[i:j])
            i = j
    return out


def parse_penman(text, prefix=""):
    """Read one AMR in PENMAN notation and return its list of triples.

    Variables get the prefix, so that two graphs can share no names. A role
    that ends in "-of" (but not ":consist-of") is read as the inverse of the
    role without it. Constants keep their quotes off.
    """
    toks = _tokens(text)
    pos = 0
    triples = []
    names = set()

    def node():
        nonlocal pos
        assert toks[pos] == "("
        var = prefix + toks[pos + 1]
        assert toks[pos + 2] == "/"
        concept = toks[pos + 3]
        pos += 4
        names.add(var)
        triples.append(("instance", var, concept))
        while toks[pos] != ")":
            role = toks[pos]
            assert role.startswith(":")
            role = role[1:]
            pos += 1
            if toks[pos] == "(":
                value = node()
                is_var = True
            else:
                value = toks[pos].strip('"')
                pos += 1
                is_var = None
            pending.append((role, var, value, is_var))
        pos += 1
        return var

    pending = []
    node()
    for role, a, b, is_var in pending:
        if is_var is None and prefix + b in names:
            b = prefix + b
        if role.endswith("-of") and role != "consist-of" and b in names:
            triples.append((role[:-3], b, a))
        else:
            triples.append((role, a, b))
    return triples
