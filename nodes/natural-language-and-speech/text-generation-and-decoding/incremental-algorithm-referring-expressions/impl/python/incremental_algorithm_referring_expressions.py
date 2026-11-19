# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-algorithm-referring-expressions/. The authors are listed in prov/NEB4RM.jsonl.

"""The incremental algorithm of Dale and Reiter (1995) for referring expressions.

An object is a dict from attribute names to values, for example
{"type": "dog", "size": "small", "colour": "black"}. The referent r is an
object, the distractors are a list of objects, and the preference order P is
a list of attribute names.

A property <A, V> rules out a distractor x when x has a value for A and that
value is not V. A distractor without the attribute A is not ruled out: the
hearer is not known to believe that it lacks the property (UserKnows is not
false). This is the flat form of the algorithm: there is no value taxonomy, so
FindBestValue returns the value of the referent, and BasicLevelValue of the
type is the type of the referent.

The result is a list of (attribute, value) pairs in the order they were
added, or None for failure.
"""

from itertools import combinations
from typing import Dict, Hashable, List, Optional, Sequence, Tuple

Obj = Dict[str, Hashable]
Pair = Tuple[str, Hashable]


def rules_out(attr: str, value: Hashable, distractors: Sequence[Obj]) -> List[int]:
    """Return the indices of the distractors that the property <attr, value> rules out."""
    return [i for i, x in enumerate(distractors) if attr in x and x[attr] != value]


def make_referring_expression(
    r: Obj, distractors: Sequence[Obj], preferred: Sequence[str], type_attr: str = "type"
) -> Optional[List[Pair]]:
    """Run the incremental algorithm (Figure 6 of Dale and Reiter 1995)."""
    chosen: List[Pair] = []  # @line L1
    c = list(distractors)
    for a in preferred:  # @line L2
        v = r.get(a)  # @line L3
        out = set(rules_out(a, v, c)) if a in r else set()  # @line L4
        if out:  # @line L5
            chosen.append((a, v))  # @line L6
            c = [x for i, x in enumerate(c) if i not in out]  # @line L7
        if not c:  # @line L8
            if type_attr in r and all(p[0] != type_attr for p in chosen):  # @line L9
                chosen.append((type_attr, r[type_attr]))
            return chosen  # @line L10
    return None  # @line L11


def distinguishes(pairs: Sequence[Pair], distractors: Sequence[Obj]) -> bool:
    """True when every distractor is ruled out by some pair."""
    return all(any(a in x and x[a] != v for a, v in pairs) for x in distractors)


def minimal_description(
    r: Obj, distractors: Sequence[Obj], attrs: Sequence[str]
) -> Optional[List[Pair]]:
    """Brute force: a smallest set of the referent's attributes that rules out every distractor.

    Tries all subsets by size, in the order of attrs, so it takes O(2^m) time
    for m attributes. Returns None when no subset works.
    """
    own = [a for a in attrs if a in r]
    for size in range(len(own) + 1):
        for sub in combinations(own, size):
            pairs = [(a, r[a]) for a in sub]
            if distinguishes(pairs, distractors):
                return pairs
    return None


def greedy_description(
    r: Obj, distractors: Sequence[Obj], attrs: Sequence[str]
) -> Optional[List[Pair]]:
    """The greedy set cover heuristic: add the attribute that rules out the most remaining distractors."""
    own = [a for a in attrs if a in r]
    c = list(distractors)
    pairs: List[Pair] = []
    while c:
        best, gain = None, 0
        for a in own:
            g = len(rules_out(a, r[a], c))
            if g > gain:
                best, gain = a, g
        if best is None:
            return None
        pairs.append((best, r[best]))
        c = [x for x in c if not (best in x and x[best] != r[best])]
        own.remove(best)
    return pairs
