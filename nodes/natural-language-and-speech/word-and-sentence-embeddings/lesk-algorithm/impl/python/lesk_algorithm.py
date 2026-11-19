# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lesk-algorithm/. The authors are listed in prov/JX07Y6.jsonl.
"""The Lesk algorithm: choose the sense whose dictionary entry shares the most
words with the context.

simplified_lesk compares each gloss of the target word with the context
words. gloss_pair_lesk is the original form for two words: it compares the
glosses of the senses of one word with the glosses of the senses of the other.
"""

from dataclasses import dataclass, field
from itertools import product

STOP_WORDS = frozenset(
    "a an the of in on at to for from by with and or but is are was were be been "
    "it its this that these those he she they we you i his her their our my as "
    "which who what when where so not no do does did can will would".split()
)


@dataclass(frozen=True)
class Sense:
    """One dictionary sense: a name, the gloss and the example sentences, as tokens."""

    name: str
    gloss: tuple[str, ...]
    examples: tuple[str, ...] = field(default=())


def signature(sense: Sense, stop_words: frozenset[str] = STOP_WORDS) -> set[str]:
    """The set of lowercased words of the gloss and the examples, minus stop words."""
    return {w.lower() for w in sense.gloss + sense.examples} - stop_words


def simplified_lesk(
    word: str,
    context: list[str],
    senses: list[Sense],
    stop_words: frozenset[str] = STOP_WORDS,
) -> Sense:
    """The sense of word whose signature overlaps the context most.

    Precondition: senses is not empty and is in dictionary order, most
    frequent sense first. Ties, and a context with no overlap, give the
    earlier sense. Cost: O(r g + n) set operations for r senses with
    signatures of at most g words and a context of n tokens.
    """
    if not senses:
        raise ValueError("the word has no senses")
    best = senses[0]  # @line L1
    max_overlap = 0  # @line L2
    ctx = {w.lower() for w in context} - stop_words - {word.lower()}  # @line L3
    for sense in senses:  # @line L4
        sig = signature(sense, stop_words)  # @line L5
        overlap = len(sig & ctx)  # @line L6
        if overlap > max_overlap:  # @line L7
            max_overlap = overlap  # @line L8
            best = sense
    return best  # @line L9


def overlap_scores(
    word: str, context: list[str], senses: list[Sense], stop_words: frozenset[str] = STOP_WORDS
) -> list[int]:
    """The overlap of each sense with the context, in the order of senses."""
    ctx = {w.lower() for w in context} - stop_words - {word.lower()}
    return [len(signature(s, stop_words) & ctx) for s in senses]


def gloss_pair_lesk(
    senses_a: list[Sense], senses_b: list[Sense], stop_words: frozenset[str] = STOP_WORDS
) -> tuple[Sense, Sense, int]:
    """Lesk's original form for two words that occur together.

    Returns the pair of senses whose signatures share the most words, and
    the size of the overlap. Ties give the first pair in the order of
    (sense of a, sense of b). Cost: O(r_a r_b g) for r_a and r_b senses.
    """
    if not senses_a or not senses_b:
        raise ValueError("each word needs at least one sense")
    sigs_b = [signature(s, stop_words) for s in senses_b]
    best = (senses_a[0], senses_b[0], -1)
    for a in senses_a:
        sig_a = signature(a, stop_words)
        for b, sig_b in zip(senses_b, sigs_b):
            k = len(sig_a & sig_b)
            if k > best[2]:
                best = (a, b, k)
    return best


def all_pairs_lesk(
    inventory: dict[str, list[Sense]], words: list[str], stop_words: frozenset[str] = STOP_WORDS
) -> tuple[dict[str, Sense], int]:
    """Choose one sense for each of several words at once.

    The score of a choice is the sum of the overlaps of all pairs of chosen
    signatures. This tries every combination, so the cost grows as the
    product of the numbers of senses; use it only for a few words.
    """
    sigs = {w: [signature(s, stop_words) for s in inventory[w]] for w in words}
    best: tuple[tuple[int, ...], int] = ((), -1)
    for choice in product(*(range(len(inventory[w])) for w in words)):
        score = 0
        for x in range(len(words)):
            for y in range(x + 1, len(words)):
                score += len(sigs[words[x]][choice[x]] & sigs[words[y]][choice[y]])
        if score > best[1]:
            best = (choice, score)
    return {w: inventory[w][i] for w, i in zip(words, best[0])}, best[1]
