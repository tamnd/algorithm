# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isolation-levels/. The authors are listed in prov/VCE808.jsonl.

import random
from itertools import permutations

from isolation_levels import adya, adya_level, ansi_level, berenson


def parse(s: str) -> list[tuple]:
    """'r1x w2y c1 a2 p1{xy}' -> operations; p is a predicate read."""
    out = []
    for tok in s.split():
        k, t = tok[0], int(tok[1])
        if k in "ca":
            out.append((k, t))
        elif k == "p":
            out.append(("rp", t, frozenset(tok[3:-1])))
        else:
            out.append((k, t, tok[2:]))
    return out


CANON = {
    # name: (history, Berenson phenomena, ANSI level, Adya phenomena, PL level)
    "dirty write": ("w1x w2x w2y c2 w1y c1", {"P0"}, "NONE", {"G0", "G1c"}, "NONE"),
    "H1 dirty read": ("r1x w1x r2x r2y c2 r1y w1y c1", {"P1"}, "READ UNCOMMITTED", {"G2-item", "G2"}, "PL-2"),
    "A1 aborted read": ("w1x r2x c2 a1", {"P1", "A1"}, "READ UNCOMMITTED", {"G1a"}, "PL-1"),
    "intermediate read": ("w1x r2x w1x c1 c2", {"P1", "P2"}, "READ UNCOMMITTED", {"G1b"}, "PL-1"),
    "H2 read skew": ("r1x r2x w2x r2y w2y c2 r1y c1", {"P2", "A5A"}, "READ COMMITTED", {"G2-item", "G2"}, "PL-2"),
    "A2 fuzzy read": ("r1x w2x c2 r1x c1", {"P2", "A2"}, "READ COMMITTED", {"G2-item", "G2"}, "PL-2"),
    "H4 lost update": ("r1x r2x w2x c2 w1x c1", {"P2", "P4"}, "READ COMMITTED", {"G2-item", "G2"}, "PL-2"),
    "H5 write skew": ("r1x r1y r2x r2y w1y w2x c1 c2", {"P2", "A5B"}, "READ COMMITTED", {"G2-item", "G2"}, "PL-2"),
    "H3 phantom": ("p1{y} w2y r2z w2z c2 r1z c1", {"P3"}, "REPEATABLE READ", {"G2"}, "PL-2.99"),
    "A3 phantom": ("p1{y} w2y c2 p1{y} c1", {"P3", "A3"}, "REPEATABLE READ", {"G2"}, "PL-2.99"),
    "serial": ("r1x w1x c1 r2x w2x c2", set(), "SERIALIZABLE", set(), "PL-3"),
}


def test_canonical_anomalies() -> None:
    for name, (s, ber, lvl, ady, pl) in CANON.items():
        h = parse(s)
        assert berenson(h) == ber, (name, berenson(h))
        assert ansi_level(h) == lvl, name
        assert adya(h) == ady, (name, adya(h))
        assert adya_level(h) == pl, name


def test_snapshot_write_skew_with_versions() -> None:
    # Doctors on call under snapshot isolation: both read the snapshot.
    h = [("r", 1, "x", 0), ("r", 1, "y", 0), ("r", 2, "x", 0), ("r", 2, "y", 0),
         ("w", 1, "x"), ("w", 2, "y"), ("c", 1), ("c", 2)]
    assert "A5B" in berenson(h) and adya(h) == {"G2-item", "G2"}
    # A read skew is impossible when both reads come from one snapshot.
    h = [("r", 1, "x", 0), ("w", 2, "x"), ("w", 2, "y"), ("c", 2), ("r", 1, "y", 0), ("c", 1)]
    assert adya_level(h) == "PL-3"


def random_history(rng: random.Random, n_txn: int, items: str) -> list[tuple]:
    """Each transaction touches each chosen item once: r, w, or r then w."""
    progs = []
    for t in range(1, n_txn + 1):
        ops = []
        for x in rng.sample(items, rng.randrange(1, len(items) + 1)):
            k = rng.choice(["r", "w", "rw"])
            ops += [(c, t, x) for c in k]
        progs.append(ops + [("c", t)])
    h = []
    while any(progs):
        p = rng.choice([p for p in progs if p])
        h.append(p.pop(0))
    return h


def conflict_serializable(h) -> bool:
    txns = sorted({op[1] for op in h})
    pairs = [(a[1], b[1]) for i, a in enumerate(h) for b in h[i + 1:]
             if a[0] in "rw" and b[0] in "rw" and a[1] != b[1] and a[2] == b[2] and "w" in (a[0], b[0])]
    for perm in permutations(txns):
        pos = {t: i for i, t in enumerate(perm)}
        if all(pos[a] < pos[b] for a, b in pairs):
            return True
    return False


def test_pl3_is_conflict_serializability_on_random_histories() -> None:
    rng = random.Random(5)
    for _ in range(3000):
        h = random_history(rng, rng.randrange(2, 5), "xyz")
        assert (adya_level(h) == "PL-3") == conflict_serializable(h)


def test_broad_ansi_serializable_implies_serializable() -> None:
    rng = random.Random(6)
    hits = 0
    for _ in range(3000):
        h = random_history(rng, rng.randrange(2, 4), "xyz")
        if ansi_level(h) == "SERIALIZABLE":
            hits += 1
            assert conflict_serializable(h)
    assert hits > 50
    # The converse fails: a serializable history can show P2.
    assert conflict_serializable(parse("r1x w2x c2 c1")) and ansi_level(parse("r1x w2x c2 c1")) == "READ COMMITTED"


def test_levels_are_nested() -> None:
    rng = random.Random(7)
    order = ["NONE", "READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
    for _ in range(2000):
        h = random_history(rng, 3, "xy")
        f = berenson(h)
        lvl = order.index(ansi_level(h))
        assert ("P0" in f) == (lvl == 0)
        assert ("P1" in f or "P0" in f) == (lvl <= 1)
