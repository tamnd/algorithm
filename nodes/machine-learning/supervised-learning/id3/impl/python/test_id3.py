# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/id3/. The authors are listed in prov/3VDGHC.jsonl.

import random
from collections import Counter
from math import log2

from id3 import gain, id3, id3_windowed, predict

# Quinlan 1986, Table 1 (the same 14 days as Mitchell 1997, Table 3.2).
TABLE = """sunny hot high false N
sunny hot high true N
overcast hot high false P
rain mild high false P
rain cool normal false P
rain cool normal true N
overcast cool normal true P
sunny mild high false N
sunny cool normal false P
rain mild normal false P
sunny mild normal true P
overcast mild high true P
overcast hot normal false P
rain mild high true N"""
ROWS = [r.split() for r in TABLE.splitlines()]
X = [tuple(r[:4]) for r in ROWS]
Y = [r[4] for r in ROWS]
OUTLOOK, TEMP, HUMIDITY, WINDY = range(4)


def ref_gain(X, y, a):
    """Information gain written out from the definition, independent of id3.py."""
    def h(ls):
        n = len(ls)
        return -sum(c / n * log2(c / n) for c in Counter(ls).values())
    n = len(y)
    rem = 0.0
    for v in set(x[a] for x in X):
        sub = [yi for xi, yi in zip(X, y) if xi[a] == v]
        rem += len(sub) / n * h(sub)
    return h(y) - rem


def test_playtennis_gains_against_printed_values():
    printed = {OUTLOOK: 0.246, TEMP: 0.029, HUMIDITY: 0.151, WINDY: 0.048}
    exact = {OUTLOOK: 0.2467, TEMP: 0.0292, HUMIDITY: 0.1518, WINDY: 0.0481}
    for a in range(4):
        g = gain(X, Y, a)
        assert abs(g - exact[a]) < 5e-5
        assert abs(g - printed[a]) < 1e-3  # the source subtracts rounded entropies
    assert max(range(4), key=lambda a: gain(X, Y, a)) == OUTLOOK


def test_playtennis_tree():
    t = id3(X, Y, [0, 1, 2, 3])
    assert t == ("node", OUTLOOK, {
        "overcast": ("leaf", "P"),
        "rain": ("node", WINDY, {"false": ("leaf", "P"), "true": ("leaf", "N")}, "P"),
        "sunny": ("node", HUMIDITY, {"high": ("leaf", "N"), "normal": ("leaf", "P")}, "N"),
    }, "P")
    assert all(predict(t, x) == y for x, y in zip(X, Y))


def test_edge_cases():
    assert id3([], [], [0], {0: ["a"]}, "z") == ("leaf", "z")
    assert id3([("a",), ("b",)], ["c", "c"], [0]) == ("leaf", "c")
    # Conflicting labels and no attribute left: the majority, ties to the smallest label.
    assert id3([("a",), ("a",), ("a",)], ["y", "x", "y"], [0]) == ("node", 0, {"a": ("leaf", "y")}, "y")
    t = id3([("a",), ("a",)], ["y", "x"], [])
    assert t == ("leaf", "x")
    # An unseen value goes to the node default.
    t = id3(X, Y, [0, 1, 2, 3])
    assert predict(t, ("fog", "hot", "high", "false")) == "P"


def check_node(tree, X, y, attrs):
    """Each internal node splits on an attribute of largest gain (first on ties); leaves are pure or attribute-exhausted."""
    if tree[0] == "leaf":
        if y and attrs:
            assert len(set(y)) == 1
        return
    _, a, children, _ = tree
    gains = [ref_gain(X, y, b) for b in attrs]
    top = max(gains)
    assert a == attrs[next(i for i, g in enumerate(gains) if g > top - 1e-9)]
    rest = [b for b in attrs if b != a]
    for v, sub in children.items():
        idx = [i for i, x in enumerate(X) if x[a] == v]
        check_node(sub, [X[i] for i in idx], [y[i] for i in idx], rest)


def test_random_against_definition():
    rng = random.Random(1986)
    for trial in range(500):
        n, d = rng.randint(1, 12), rng.randint(1, 4)
        Xr = [tuple(rng.choice("abc") for _ in range(d)) for _ in range(n)]
        target = rng.randrange(d)
        yr = [("+" if x[target] == "a" else "-") if rng.random() < 0.8 else rng.choice("+-") for x in Xr]
        t = id3(Xr, yr, list(range(d)))
        check_node(t, Xr, yr, list(range(d)))
        consistent = all(yr[i] == yr[j] for i in range(n) for j in range(n) if Xr[i] == Xr[j])
        if consistent:
            assert all(predict(t, x) == yy for x, yy in zip(Xr, yr))


def test_windowing_fits_consistent_data():
    rng = random.Random(42)
    for trial in range(100):
        n, d = rng.randint(5, 30), 4
        Xr = [tuple(rng.choice("abc") for _ in range(d)) for _ in range(n)]
        yr = ["+" if (x[0] == "a") != (x[1] == "b") else "-" for x in Xr]
        t = id3_windowed(Xr, yr, range(d), window=4, increment=3, rng=random.Random(trial))
        assert all(predict(t, x) == yy for x, yy in zip(Xr, yr))
