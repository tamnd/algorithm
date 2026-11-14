# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gemini-netlist-comparison/. The authors are listed in prov/N08Y88.jsonl.

import random
from collections import Counter
from itertools import permutations

import pytest

from gemini_netlist_comparison import compare

PINS = {
    "nmos": ("g", "sd", "sd"),
    "pmos": ("g", "sd", "sd"),
    "res": ("t", "t"),
    "diode": ("a", "k"),
}


def signature(t, pins, f):
    """Type and, for each pin class, the multiset of mapped nets."""
    by_class = {}
    for c, v in zip(PINS[t], pins):
        by_class.setdefault(c, []).append(f[v])
    return (t, tuple(sorted((c, tuple(sorted(vs))) for c, vs in by_class.items())))


def brute_isomorphic(a, b):
    """Try every bijection of nets. For a fixed net map, a device map exists
    exactly when the multisets of device signatures are equal."""
    (da, aa), (db, ab) = a, b
    na = sorted({v for _, p in da for v in p} | set(aa))
    nb = sorted({v for _, p in db for v in p} | set(ab))
    if len(na) != len(nb) or len(da) != len(db):
        return False
    target = Counter(signature(t, p, {v: v for v in nb}) for t, p in db)
    for perm in permutations(nb):
        f = dict(zip(na, perm))
        if any(aa.get(v) != ab.get(f[v]) for v in na):
            continue
        if Counter(signature(t, p, f) for t, p in da) == target:
            return True
    return False


def check_match(a, b, out):
    """The returned maps must be an isomorphism."""
    _, dmap, nmap = out
    (da, aa), (db, ab) = a, b
    assert sorted(dmap) == list(range(len(db)))
    assert len(set(nmap.values())) == len(nmap)
    for d, (t, p) in enumerate(da):
        tb, pb = db[dmap[d]]
        assert tb == t
        assert signature(t, p, nmap) == signature(tb, pb, {v: v for v in pb})
    for v, g in aa.items():
        assert ab.get(nmap[v]) == g


def random_netlist(rng, n_dev, n_net):
    nets = [f"n{i}" for i in range(n_net)]
    devs = []
    for _ in range(n_dev):
        t = rng.choice(sorted(PINS))
        devs.append((t, tuple(rng.choice(nets) for _ in PINS[t])))
    anchors = {}
    if rng.random() < 0.5:
        anchors[rng.choice(nets)] = "VDD"
    return devs, anchors


def scramble(rng, netlist):
    """An isomorphic copy: new net names, shuffled devices, swapped equal pins."""
    devs, anchors = netlist
    nets = sorted({v for _, p in devs for v in p} | set(anchors))
    new = [f"m{i}" for i in range(len(nets))]
    rng.shuffle(new)
    f = dict(zip(nets, new))
    out = []
    for t, p in devs:
        p = [f[v] for v in p]
        cls = PINS[t]
        for c in set(cls):
            idx = [i for i, x in enumerate(cls) if x == c]
            vals = [p[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                p[i] = v
        out.append((t, tuple(p)))
    rng.shuffle(out)
    return out, {f[v]: g for v, g in anchors.items()}


def mutate(rng, netlist):
    devs, anchors = netlist
    devs = list(devs)
    d = rng.randrange(len(devs))
    t, p = devs[d]
    nets = sorted({v for _, q in devs for v in q})
    p = list(p)
    p[rng.randrange(len(p))] = rng.choice(nets)
    devs[d] = (t, tuple(p))
    return devs, anchors


NAND2 = ([("pmos", ("A", "Y", "VDD")), ("pmos", ("B", "VDD", "Y")),
          ("nmos", ("A", "Y", "X")), ("nmos", ("B", "X", "GND"))],
         {"VDD": "VDD", "GND": "GND"})
LAYOUT = ([("nmos", ("n2", "n6", "n5")), ("pmos", ("n1", "n4", "n3")),
           ("nmos", ("n1", "n3", "n5")), ("pmos", ("n2", "n3", "n4"))],
          {"n4": "VDD", "n6": "GND"})


def test_nand2_page_example():
    # The layout lists the devices in another order, swaps some sources and
    # drains, and calls the nets n1 to n6.
    layout = LAYOUT
    out = compare(NAND2, layout, PINS)
    assert out[0] == "match"
    check_match(NAND2, layout, out)
    assert out[2] == {"A": "n1", "B": "n2", "Y": "n3", "VDD": "n4", "X": "n5", "GND": "n6"}


def test_swapped_inputs_need_port_names():
    swapped = ([("pmos", ("A", "Y", "VDD")), ("pmos", ("B", "VDD", "Y")),
                ("nmos", ("B", "Y", "X")), ("nmos", ("A", "X", "GND"))],
               {"VDD": "VDD", "GND": "GND"})
    assert compare(NAND2, swapped, PINS)[0] == "match"
    named = lambda n: (n[0], dict(n[1], A="A", B="B"))
    out = compare(named(NAND2), named(swapped), PINS)
    assert out[0] == "mismatch"
    assert not brute_isomorphic(named(NAND2), named(swapped))


def ring(nets):
    return [("res", (nets[i], nets[(i + 1) % len(nets)])) for i in range(len(nets))]


def test_regular_graphs_need_guesses():
    six = (ring([f"a{i}" for i in range(6)]), {})
    two_three = (ring(["b0", "b1", "b2"]) + ring(["c0", "c1", "c2"]), {})
    assert compare(six, two_three, PINS)[0] == "mismatch"
    assert not brute_isomorphic(six, two_three)
    stats = {}
    out = compare(six, (ring([f"z{i}" for i in (3, 1, 4, 0, 5, 2)]), {}), PINS, stats=stats)
    assert out[0] == "match" and stats["guesses"] >= 1


def test_wrong_guess_without_backtracking():
    # Both netlists are a 6-ring plus two 3-rings. All nets look alike to the
    # refinement. A guess that pairs a net of the 6-ring with a net of a
    # 3-ring fails, so the plain guessing comparator can report a false
    # mismatch, while the backtracking search finds the match.
    a = (ring([f"a{i}" for i in range(6)]) + ring(["b0", "b1", "b2"]) + ring(["c0", "c1", "c2"]), {})
    b = (ring(["p0", "p1", "p2"]) + ring([f"q{i}" for i in range(6)]) + ring(["r0", "r1", "r2"]), {})
    assert compare(a, b, PINS)[0] == "match"
    assert compare(a, b, PINS, backtrack=False)[0] == "mismatch"


@pytest.mark.parametrize("seed", range(150))
def test_random_against_brute_force(seed):
    rng = random.Random(seed)
    n_dev = rng.randint(1, 7)
    n_net = rng.randint(2, 6)
    a = random_netlist(rng, n_dev, n_net)
    b = scramble(rng, a)
    out = compare(a, b, PINS)
    assert out[0] == "match"
    check_match(a, b, out)
    for _ in range(3):
        c = scramble(rng, mutate(rng, a))
        want = brute_isomorphic(a, c)
        got = compare(a, c, PINS)
        assert (got[0] == "match") == want
        if want:
            check_match(a, c, got)
