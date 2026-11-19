# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yarowsky-algorithm/. The authors are listed in prov/89R7KS.jsonl.

import math
import random

from yarowsky_algorithm import (
    Occurrence,
    Rule,
    classify,
    features,
    seed_labels,
    train_decision_list,
    yarowsky,
)

DATA = [
    ("plant life needs water and light", "d1"),
    ("a green plant grows toward the light", "d1"),
    ("the plant needs water", "d1"),
    ("the manufacturing plant hired workers", "d2"),
    ("workers at the plant went on strike", "d2"),
    ("the car plant closed", "d3"),
    ("water the plant every day", "d4"),
    ("the plant workers were paid", "d5"),
    ("the car plant employs workers", "d6"),
]
SEEDS = {"+1:life": "A", "-1:manufacturing": "B"}


def occurrences(data: list[tuple[str, str]]) -> list[Occurrence]:
    out = []
    for s, d in data:
        t = tuple(s.split())
        out.append(Occurrence(t, t.index("plant"), d))
    return out


def test_worked_example() -> None:
    occ = occurrences(DATA)
    assert sorted(features(occ[2])) == ["+1:needs", "-1:the", "win:needs", "win:water"]
    r1 = yarowsky(occ, SEEDS, ["A", "B"], max_iter=1)
    assert r1.labels == ["A", "A", "A", "B", "B", None, "A", "B", "B"]
    assert all(abs(r.score - math.log(11)) < 1e-12 for r in r1.rules)
    result = yarowsky(occ, SEEDS, ["A", "B"])
    assert result.converged and result.iterations == 3
    assert result.labels == ["A", "A", "A", "B", "B", "B", "A", "B", "B"]
    top = [(r.feature, r.sense, round(r.score, 3)) for r in result.rules[:5]]
    assert top == [
        ("win:workers", "B", 3.714), ("win:water", "A", 3.434), ("-1:car", "B", 3.045),
        ("win:car", "B", 3.045), ("win:needs", "A", 3.045),
    ]
    assert result.rules[-1] == Rule(0.0, "-1:the", "A")
    plain = yarowsky(occ, SEEDS, ["A", "B"], one_sense_per_discourse=False)
    assert plain.converged and plain.labels == ["A", None, "A", "B", "B", "B", "A", "B", "B"]


def test_error_propagation() -> None:
    data = DATA[:-1] + [("a car plant needs workers", "d6")]
    result = yarowsky(occurrences(data), SEEDS, ["A", "B"])
    assert result.labels[5] == "A" and result.labels[8] == "A"


def test_label_can_be_lost() -> None:
    occ = [
        Occurrence(("a", "x", "f"), 1),
        Occurrence(("x", "f"), 0),
        Occurrence(("g", "x", "f"), 1),
        Occurrence(("g", "x", "b"), 1),
        Occurrence(("g", "x", "b"), 1),
    ]
    seeds = {"-1:a": "A", "+1:b": "B"}
    run = [yarowsky(occ, seeds, ["A", "B"], k=0, max_iter=t, one_sense_per_discourse=False) for t in (1, 2, 3)]
    assert run[0].labels == ["A", "A", "B", "B", "B"]
    assert run[1].labels == ["A", None, "B", "B", "B"]
    assert run[2].converged and run[2].labels == run[1].labels


def test_edges() -> None:
    occ = occurrences(DATA)
    none = yarowsky(occ, {}, ["A", "B"])
    assert none.converged and none.iterations == 1 and none.labels == [None] * 9 and none.rules == []
    both = seed_labels([frozenset({"x", "y"}), frozenset({"x"})], {"x": "A", "y": "B"})
    assert both == [None, "A"]
    assert features(Occurrence(("plant",), 0)) == frozenset()
    assert classify(frozenset({"f"}), [Rule(1.0, "f", "A")], 2.0) is None
    assert classify(frozenset({"g"}), [Rule(1.0, "f", "A")], 0.0) is None
    capped = yarowsky(occ, SEEDS, ["A", "B"], max_iter=2)
    assert not capped.converged and capped.iterations == 2
    try:
        yarowsky(occ, SEEDS, ["A", "B"], alpha=0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("alpha = 0 must fail")


def reference(occ, seeds, senses, k, alpha, threshold, max_iter, ospd):
    """A direct second version: counts by scanning, the best rule by max."""
    feats = [features(o, k) for o in occ]
    fixed = []
    for f in feats:
        s = sorted({seeds[x] for x in f if x in seeds})
        fixed.append(s[0] if len(s) == 1 else None)
    y = list(fixed)
    for t in range(1, max_iter + 1):
        allf = sorted({x for f, lab in zip(feats, y) if lab is not None for x in f})
        table = {}
        for x in allf:
            c = {s: sum(1 for f, lab in zip(feats, y) if lab == s and x in f) for s in senses}
            best = senses[0]
            for s in senses:
                if c[s] > c[best]:
                    best = s
            other = sum(c.values()) - c[best]
            table[x] = (math.log((c[best] + alpha) / (other + alpha)), best)
        new = []
        for i, f in enumerate(feats):
            if fixed[i] is not None:
                new.append(fixed[i])
                continue
            match = [x for x in f if x in table]
            if not match:
                new.append(None)
                continue
            x = min(match, key=lambda z: (-table[z][0], z))
            new.append(table[x][1] if table[x][0] >= threshold else None)
        if ospd:
            out = list(new)
            for i, o in enumerate(occ):
                if fixed[i] is not None or o.discourse is None:
                    continue
                c = {}
                for j, p in enumerate(occ):
                    if p.discourse == o.discourse and new[j] is not None:
                        c[new[j]] = c.get(new[j], 0) + 1
                if c:
                    m = max(c.values())
                    winners = [s for s in c if c[s] == m]
                    if len(winners) == 1:
                        out[i] = winners[0]
            new = out
        if new == y:
            return y, t, True
        y = new
    return y, max_iter, False


def test_against_reference() -> None:
    rng = random.Random(5)
    words = ["w%d" % i for i in range(8)]
    for _ in range(500):
        senses = ["A", "B", "C"][: rng.randrange(2, 4)]
        occ = []
        for _ in range(rng.randrange(1, 9)):
            n = rng.randrange(1, 7)
            t = tuple(rng.choice(words) for _ in range(n))
            occ.append(Occurrence(t, rng.randrange(n), rng.choice(["d1", "d2", "d3", None])))
        seeds = {}
        for _ in range(rng.randrange(0, 4)):
            seeds[rng.choice(["-1:", "+1:", "win:"]) + rng.choice(words)] = rng.choice(senses)
        k = rng.randrange(1, 4)
        alpha = rng.choice([0.1, 0.5, 1.0])
        threshold = rng.choice([0.0, 0.5, 1.5])
        ospd = rng.random() < 0.5
        got = yarowsky(occ, seeds, senses, k=k, alpha=alpha, threshold=threshold, max_iter=6, one_sense_per_discourse=ospd)
        want = reference(occ, seeds, senses, k, alpha, threshold, 6, ospd)
        assert (got.labels, got.iterations, got.converged) == want
        if got.converged:
            again = yarowsky(occ, seeds, senses, k=k, alpha=alpha, threshold=threshold, max_iter=got.iterations + 1,
                             one_sense_per_discourse=ospd)
            assert again.labels == got.labels
        fixed = seed_labels([features(o, k) for o in occ], seeds)
        assert all(f is None or f == y for f, y in zip(fixed, got.labels))
        rules = train_decision_list([features(o, k) for o in occ], got.labels, senses, alpha)
        assert all(a.score >= b.score for a, b in zip(rules, rules[1:]))
