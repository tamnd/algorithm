# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yarowsky-algorithm/. The authors are listed in prov/89R7KS.jsonl.
"""The Yarowsky algorithm: grow a decision list for word senses from seed
collocations, with the one sense per discourse constraint as an option.

Features of an occurrence are the word just before the target ("-1:w"), the
word just after it ("+1:w") and each non-stop word within k tokens
("win:w"). The score of a rule f -> s is the smoothed log ratio
log((c(f, s) + alpha) / (c(f, other senses) + alpha)), with natural logs.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from math import log

STOP_WORDS = frozenset("a an the of in on at to for and or is are was were be it its this that with by as".split())


@dataclass(frozen=True)
class Occurrence:
    """One occurrence of the target word: the tokens, its position, and its discourse (None if unknown)."""

    tokens: tuple[str, ...]
    position: int
    discourse: str | None = None


@dataclass(frozen=True)
class Rule:
    score: float
    feature: str
    sense: str


@dataclass(frozen=True)
class Result:
    rules: list[Rule]
    labels: list[str | None]
    iterations: int
    converged: bool


def features(occ: Occurrence, k: int = 4, stop_words: frozenset[str] = STOP_WORDS) -> frozenset[str]:
    """The collocation features of one occurrence."""
    t, i = occ.tokens, occ.position
    f = set()
    if i > 0:
        f.add("-1:" + t[i - 1])
    if i + 1 < len(t):
        f.add("+1:" + t[i + 1])
    for j in range(max(0, i - k), min(len(t), i + k + 1)):
        if j != i and t[j] not in stop_words:
            f.add("win:" + t[j])
    return frozenset(f)


def train_decision_list(
    feats: list[frozenset[str]], labels: list[str | None], senses: list[str], alpha: float
) -> list[Rule]:
    """One rule per feature seen in a labeled example, sorted by score, then by feature."""
    count: dict[str, Counter[str]] = defaultdict(Counter)
    for f, y in zip(feats, labels):
        if y is not None:
            for x in f:
                count[x][y] += 1
    rules = []
    for x, c in count.items():
        s = max(senses, key=lambda z: (c[z], -senses.index(z)))
        other = sum(c.values()) - c[s]
        rules.append(Rule(log((c[s] + alpha) / (other + alpha)), x, s))
    rules.sort(key=lambda r: (-r.score, r.feature))
    return rules


def classify(f: frozenset[str], rules: list[Rule], threshold: float) -> str | None:
    """The sense of the first rule that matches f, if its score reaches the threshold."""
    for r in rules:
        if r.feature in f:
            return r.sense if r.score >= threshold else None
    return None


def seed_labels(feats: list[frozenset[str]], seeds: dict[str, str]) -> list[str | None]:
    """The sense of the seed collocations of each example, or None for none or a conflict."""
    out: list[str | None] = []
    for f in feats:
        found = {seeds[x] for x in f if x in seeds}
        out.append(found.pop() if len(found) == 1 else None)
    return out


def yarowsky(
    occurrences: list[Occurrence],
    seeds: dict[str, str],
    senses: list[str],
    k: int = 4,
    alpha: float = 0.1,
    threshold: float = 2.0,
    max_iter: int = 50,
    one_sense_per_discourse: bool = True,
) -> Result:
    """Bootstrap a decision list from the seed collocations.

    Precondition: alpha > 0, and every seed sense is in senses (in order of
    preference for ties). Examples labeled by a seed keep that label. The
    loop stops when the labels repeat or after max_iter rounds. Cost per
    round, for F distinct features, n examples and at most m features per
    example: O(n m) to count, O(F log F) to sort, and O(n F) to scan the
    list once per example.
    """
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    feats = [features(o, k) for o in occurrences]
    fixed = seed_labels(feats, seeds)
    labels = list(fixed)  # @line L1
    rules: list[Rule] = []
    for t in range(1, max_iter + 1):  # @line L2
        rules = train_decision_list(feats, labels, senses, alpha)  # @line L3
        new = [fixed[i] or classify(feats[i], rules, threshold) for i in range(len(feats))]  # @line L4
        if one_sense_per_discourse:  # @line L5
            votes: dict[str, Counter[str]] = defaultdict(Counter)
            for o, y in zip(occurrences, new):
                if o.discourse is not None and y is not None:
                    votes[o.discourse][y] += 1
            for i, o in enumerate(occurrences):
                c = votes.get(o.discourse) if o.discourse is not None else None
                if c and fixed[i] is None:
                    top = c.most_common(2)
                    if len(top) == 1 or top[0][1] > top[1][1]:
                        new[i] = top[0][0]
        if new == labels:  # @line L6
            return Result(rules, labels, t, True)
        labels = new  # @line L7
    return Result(rules, labels, max_iter, False)  # @line L8
