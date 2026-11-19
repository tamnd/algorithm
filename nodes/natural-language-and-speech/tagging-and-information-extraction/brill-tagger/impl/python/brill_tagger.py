# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brill-tagger/. The authors are listed in prov/W3YAEV.jsonl.

"""Transformation-based error-driven learning of tagging rules (Brill 1995).

Initial state: each known word gets its most frequent training tag (ties go
to the smallest tag name); an unknown word gets a default tag.

A rule is (template, args, a, b): "change tag a to tag b when the template
holds with these arguments". The templates are the eleven nonlexicalized
templates of Brill (1995), Section 4.1, and the lexicalized template "the
current word is w". Positions before the sentence read the tag "<s>" and
positions after it read "</s>".

Application has delayed effect, as in Brill's experiments: all positions
where the rule triggers are found first, then all of them are changed. With
the lexicon rule of Brill's Section 4.1, a known word may only change to a
tag it had at least once in training; an unknown word may change to any tag.

The score of a rule is the net number of errors it removes on the training
corpus: good (wrong tag a becomes the right tag b) minus bad (right tag a
becomes wrong). The learner picks the best rule, with ties broken by the
smallest rule in the order of rule_key, applies it, and repeats while the
best score is at least the threshold.
"""

from typing import Dict, Iterable, List, Sequence, Set, Tuple

LEFT, RIGHT = "<s>", "</s>"

TEMPLATES = ["PREV1", "NEXT1", "PREV2", "NEXT2", "PREV1OR2", "NEXT1OR2", "PREV1OR2OR3",
             "NEXT1OR2OR3", "SURROUND", "PREVBIGRAM", "NEXTBIGRAM", "CURWD"]

Rule = Tuple[str, Tuple[str, ...], str, str]


def tag_at(tags: Sequence[str], p: int) -> str:
    if p < 0:
        return LEFT
    if p >= len(tags):
        return RIGHT
    return tags[p]


def instances(words: Sequence[str], tags: Sequence[str], p: int) -> Set[Tuple[str, Tuple[str, ...]]]:
    """Every (template, args) that is true at position p."""
    t = lambda d: tag_at(tags, p + d)  # noqa: E731
    out = {
        ("PREV1", (t(-1),)), ("NEXT1", (t(1),)), ("PREV2", (t(-2),)), ("NEXT2", (t(2),)),
        ("SURROUND", (t(-1), t(1))), ("PREVBIGRAM", (t(-2), t(-1))), ("NEXTBIGRAM", (t(1), t(2))),
        ("CURWD", (words[p],)),
    }
    for z in {t(-1), t(-2)}:
        out.add(("PREV1OR2", (z,)))
    for z in {t(1), t(2)}:
        out.add(("NEXT1OR2", (z,)))
    for z in {t(-1), t(-2), t(-3)}:
        out.add(("PREV1OR2OR3", (z,)))
    for z in {t(1), t(2), t(3)}:
        out.add(("NEXT1OR2OR3", (z,)))
    return out


def holds(template: str, args: Tuple[str, ...], words: Sequence[str], tags: Sequence[str], p: int) -> bool:
    """True when the template with these arguments holds at position p."""
    t = lambda d: tag_at(tags, p + d)  # noqa: E731
    if template == "PREV1":
        return t(-1) == args[0]
    if template == "NEXT1":
        return t(1) == args[0]
    if template == "PREV2":
        return t(-2) == args[0]
    if template == "NEXT2":
        return t(2) == args[0]
    if template == "PREV1OR2":
        return args[0] in (t(-1), t(-2))
    if template == "NEXT1OR2":
        return args[0] in (t(1), t(2))
    if template == "PREV1OR2OR3":
        return args[0] in (t(-1), t(-2), t(-3))
    if template == "NEXT1OR2OR3":
        return args[0] in (t(1), t(2), t(3))
    if template == "SURROUND":
        return (t(-1), t(1)) == args
    if template == "PREVBIGRAM":
        return (t(-2), t(-1)) == args
    if template == "NEXTBIGRAM":
        return (t(1), t(2)) == args
    if template == "CURWD":
        return words[p] == args[0]
    raise ValueError("unknown template " + template)


def rule_key(r: Rule):
    """The tie order: template index, then arguments, then from tag, then to tag."""
    return (TEMPLATES.index(r[0]), r[1], r[2], r[3])


class Lexicon:
    """Tag counts of each training word, for the initial annotator and the lexicon rule."""

    def __init__(self, corpus, default: str = None):
        self.counts: Dict[str, Dict[str, int]] = {}
        total: Dict[str, int] = {}
        for words, tags in corpus:
            for w, g in zip(words, tags):
                row = self.counts.setdefault(w, {})
                row[g] = row.get(g, 0) + 1
                total[g] = total.get(g, 0) + 1
        self.default = default if default is not None else min(total, key=lambda g: (-total[g], g))

    def initial(self, words: Sequence[str]) -> List[str]:
        out = []
        for w in words:
            row = self.counts.get(w)
            out.append(min(row, key=lambda g: (-row[g], g)) if row else self.default)
        return out

    def allows(self, w: str, b: str) -> bool:
        return w not in self.counts or b in self.counts[w]


def apply_rule(rule: Rule, words: Sequence[str], tags: List[str], lex: Lexicon = None,
               delayed: bool = True) -> List[str]:
    """Apply one rule to a sentence and return the new tags.

    delayed=True finds every trigger first (Brill's choice); delayed=False
    changes the tags left to right at once, so a change can trigger the next.
    """
    template, args, a, b = rule
    new = list(tags)
    src = tags if delayed else new
    for p in range(len(words)):
        if new[p] == a and holds(template, args, words, src, p) and (lex is None or lex.allows(words[p], b)):
            new[p] = b
    return new


def errors(corpus_tags: Iterable[Sequence[str]], gold: Iterable[Sequence[str]]) -> int:
    return sum(1 for ts, gs in zip(corpus_tags, gold) for t, g in zip(ts, gs) if t != g)


def best_rule(words_list, cur, gold, lex: Lexicon = None):
    """Return (rule, score) of the best rule on the current tagging, or (None, 0)."""
    good: Dict[Rule, int] = {}
    for words, ts, gs in zip(words_list, cur, gold):  # @line L4
        for p in range(len(words)):
            if ts[p] != gs[p] and (lex is None or lex.allows(words[p], gs[p])):
                for template, args in instances(words, ts, p):
                    r = (template, args, ts[p], gs[p])
                    good[r] = good.get(r, 0) + 1
    by_env: Dict[Tuple[str, Tuple[str, ...], str], List[str]] = {}
    for (template, args, a, b) in good:
        by_env.setdefault((template, args, a), []).append(b)
    bad: Dict[Rule, int] = {}
    for words, ts, gs in zip(words_list, cur, gold):  # @line L5
        for p in range(len(words)):
            if ts[p] == gs[p]:
                for template, args in instances(words, ts, p):
                    for b in by_env.get((template, args, ts[p]), ()):
                        if lex is None or lex.allows(words[p], b):
                            r = (template, args, ts[p], b)
                            bad[r] = bad.get(r, 0) + 1
    best, best_score = None, 0
    for r in sorted(good, key=rule_key):  # @line L6
        s = good[r] - bad.get(r, 0)
        if best is None or s > best_score:
            best, best_score = r, s
    return best, best_score


def train(corpus, threshold: int = 1, max_rules: int = 1000, default: str = None,
          use_lexicon: bool = True):
    """Learn an ordered list of rules. Return (lexicon, rules, scores)."""
    if threshold < 1:
        raise ValueError("the threshold must be at least 1")
    lex = Lexicon(corpus, default)
    words_list = [list(w) for w, _ in corpus]
    gold = [list(g) for _, g in corpus]
    cur = [lex.initial(w) for w in words_list]  # @line L1
    rules: List[Rule] = []  # @line L2
    scores: List[int] = []
    while len(rules) < max_rules:  # @line L3
        r, s = best_rule(words_list, cur, gold, lex if use_lexicon else None)
        if r is None or s < threshold:  # @line L7
            break
        cur = [apply_rule(r, w, ts, lex if use_lexicon else None) for w, ts in zip(words_list, cur)]  # @line L8
        rules.append(r)  # @line L9
        scores.append(s)
    return lex, rules, scores


def tag(words: Sequence[str], lex: Lexicon, rules: Sequence[Rule], use_lexicon: bool = True) -> List[str]:
    """Tag a sentence: the initial annotator, then every rule in order."""
    ts = lex.initial(words)
    for r in rules:
        ts = apply_rule(r, words, ts, lex if use_lexicon else None)
    return ts
