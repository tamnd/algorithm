# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-based-ip-traceback/. The authors are listed in prov/3RR23Q.jsonl.

import random
from collections import deque

from hash_based_ip_traceback import DigestTable, false_positive_rate, forward, invariant, trace

G = {
    "V": ["R1"],
    "R1": ["V", "R2"],
    "R2": ["R1", "R3", "R4"],
    "R3": ["R2", "R5", "R6"],
    "R4": ["R2", "R7"],
    "R5": ["R3"],
    "R6": ["R3"],
    "R7": ["R4"],
}
ROUTES = {
    "R5": ["R5", "R3", "R2", "R1"],
    "R6": ["R6", "R3", "R2", "R1"],
    "R7": ["R7", "R4", "R2", "R1"],
}
X = ("198.51.100.7", "192.0.2.1", 4242, 60, b"example payload")


def example_tables() -> dict:
    tables = {r: DigestTable(32, 3, f"key-{r}".encode()) for r in G if r != "V"}
    for i in range(4):
        src = ("R5", "R7")[i % 2]
        forward(ROUTES[src], (f"203.0.113.{i + 1}", "192.0.2.1", i + 1, 64, b"background"), tables)
    forward(ROUTES["R6"], X, tables)
    return tables


def test_example() -> None:
    t = example_tables()
    assert t["R4"].indices(X) == [7, 23, 26]
    assert [t["R4"].bits[j] for j in (7, 23, 26)] == [0, 0, 1]
    assert [t["R5"].bits[j] for j in t["R5"].indices(X)] == [0, 0, 1]
    assert sum(t["R1"].bits) == 14 and sum(t["R4"].bits) == 6
    assert trace(G, "V", X, t) == {"R1", "R2", "R3", "R6"}
    exact = {r: set() for r in G if r != "V"}
    for r in ROUTES["R6"]:
        exact[r].add(X)
    assert trace(G, "V", X, exact) == {"R1", "R2", "R3", "R6"}
    assert abs(false_positive_rate(32, 3, 2) - 0.00522) < 1e-5
    assert abs(false_positive_rate(32, 3, 5) - 0.05439) < 1e-5


def test_edges() -> None:
    t = DigestTable(64, 4, b"k")
    assert not t.query(X)
    t.insert(X)
    assert t.query(X)
    # A router decrements the TTL; the digest does not change.
    y = X[:3] + (17,) + X[4:]
    assert invariant(y) == invariant(X) and t.query(y)
    # Payload bytes after the first 8 are not part of the digest.
    assert invariant(X[:4] + (b"example other",)) == invariant(X)
    one = DigestTable(1, 3, b"k")
    one.insert(("192.0.2.9", "192.0.2.1", 1, 64, b""))
    assert one.query(X)  # a full table answers yes to everything
    assert trace({"V": []}, "V", X, {}) == set()
    empty = {r: DigestTable(32, 3, f"key-{r}".encode()) for r in G if r != "V"}
    assert trace(G, "V", X, empty) == set()
    # Different keys give different positions (independence across routers).
    assert example_tables()["R1"].indices(X) != example_tables()["R2"].indices(X)


def random_graph(rng: random.Random, n: int) -> dict:
    names = ["V"] + [f"R{i}" for i in range(1, n)]
    g = {a: set() for a in names}
    for i in range(1, n):
        j = rng.randrange(0, i)
        g[names[i]].add(names[j])
        g[names[j]].add(names[i])
    for _ in range(rng.randrange(0, n)):
        a, b = rng.sample(names[1:], 2) if n > 2 else (names[0], names[-1])
        if a != b:
            g[a].add(b)
            g[b].add(a)
    return {a: sorted(b) for a, b in g.items()}


def route_to(g: dict, src: str) -> list:
    """The shortest path from src to V, without V, by breadth-first search from V."""
    parent = {"V": None}
    q = deque(["V"])
    while q:
        u = q.popleft()
        for r in g[u]:
            if r not in parent:
                parent[r] = u
                q.append(r)
    path = [src]
    while parent[path[-1]] != "V":
        path.append(parent[path[-1]])
    return path


def test_random_graphs() -> None:
    """Exact sets give the path exactly; Bloom filters give a superset with no false negatives."""
    rng = random.Random(2001)
    supersets = 0
    for trial in range(500):
        n = rng.randrange(2, 21)
        g = random_graph(rng, n)
        routers = [r for r in g if r != "V"]
        keys = {r: rng.randbytes(16) for r in routers}
        m = rng.choice((16, 32, 64))
        k = rng.randrange(1, 4)
        bloom = {r: DigestTable(m, k, keys[r]) for r in routers}
        exact = {r: set() for r in routers}
        for i in range(rng.randrange(0, 8)):
            y = (f"203.0.113.{rng.randrange(1, 255)}", "192.0.2.1", 10000 + i, 64, rng.randbytes(8))
            p = route_to(g, rng.choice(routers))
            forward(p, y, bloom)
            for r in p:
                exact[r].add(y)
        x = (f"198.51.100.{rng.randrange(1, 255)}", "192.0.2.1", trial, 64, rng.randbytes(8))
        path = route_to(g, rng.choice(routers))
        forward(path, x, bloom)
        for r in path:
            exact[r].add(x)
        assert trace(g, "V", x, exact) == set(path)
        got = trace(g, "V", x, bloom)
        assert set(path) <= got <= set(routers)
        for r in got:  # every yes is a forwarder or a false positive of its own filter
            assert x in exact[r] or bloom[r].query(x)
        supersets += got != set(path)
    assert supersets > 0  # the oracle comparison exercised false positives


def test_false_positive_rate() -> None:
    """The measured rate matches (1 - (1 - 1/m)^(k n))^k for m = 256, k = 3, n = 40."""
    rng = random.Random(7)
    m, k, n = 256, 3, 40
    hits = queries = 0
    for t in range(25):
        table = DigestTable(m, k, rng.randbytes(16))
        for i in range(n):
            table.insert(("203.0.113.1", "192.0.2.1", i, 64, rng.randbytes(8)))
        for i in range(400):
            queries += 1
            hits += table.query(("198.51.100.1", "192.0.2.1", i, 64, rng.randbytes(8)))
    rate = hits / queries
    assert abs(rate - false_positive_rate(m, k, n)) < 0.015
