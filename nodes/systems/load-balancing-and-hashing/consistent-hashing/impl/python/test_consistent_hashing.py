# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-hashing/. The authors are listed in prov/DAQ627.jsonl.

from consistent_hashing import RING, ConsistentHash, assignment, h, mod_hash, moved_fraction

KEYS = [f"key{i}" for i in range(20000)]


def naive_lookup(ch: ConsistentHash, key: str) -> str:
    """The first point clockwise from h(key), by a linear scan."""
    x = h(key)
    best = None
    for p, s in zip(ch.pos, ch.owner):
        d = (p - x) % RING
        if best is None or d < best[0]:
            best = (d, s)
    assert best is not None
    return best[1]


def test_lookup_matches_linear_scan() -> None:
    ch = ConsistentHash([f"s{i}" for i in range(7)], v=5)
    for k in KEYS[:2000]:
        assert ch.lookup(k) == naive_lookup(ch, k)


def test_sorted_and_wrap_around() -> None:
    ch = ConsistentHash(["a", "b", "c"], v=4)
    assert ch.pos == sorted(ch.pos) and len(ch.pos) == 12
    # a key past the last point goes to the first point
    last = ch.pos[-1]
    keys_after = [k for k in KEYS if h(k) > last]
    assert keys_after
    for k in keys_after:
        assert ch.lookup(k) == ch.owner[0]


def test_add_is_monotone() -> None:
    for v in (1, 20):
        ch = ConsistentHash([f"s{i}" for i in range(10)], v=v)
        before = assignment(KEYS, ch.lookup)
        ch.add("new")
        after = assignment(KEYS, ch.lookup)
        for k in KEYS:
            assert after[k] == before[k] or after[k] == "new"


def test_remove_moves_only_keys_of_removed_server() -> None:
    ch = ConsistentHash([f"s{i}" for i in range(10)], v=20)
    before = assignment(KEYS, ch.lookup)
    ch.remove("s3")
    after = assignment(KEYS, ch.lookup)
    for k in KEYS:
        if before[k] != "s3":
            assert after[k] == before[k]
        else:
            assert after[k] != "s3"


def test_add_then_remove_restores() -> None:
    ch = ConsistentHash([f"s{i}" for i in range(5)], v=8)
    before = assignment(KEYS, ch.lookup)
    ch.add("x")
    ch.remove("x")
    assert assignment(KEYS, ch.lookup) == before


def test_moved_fraction_ring_against_mod() -> None:
    n = 10
    servers = [f"s{i}" for i in range(n)]
    ch = ConsistentHash(servers, v=100)
    before = assignment(KEYS, ch.lookup)
    ch.add(f"s{n}")
    ring_moved = moved_fraction(before, assignment(KEYS, ch.lookup))
    mod_before = assignment(KEYS, lambda k: mod_hash(k, servers))
    mod_after = assignment(KEYS, lambda k: mod_hash(k, servers + [f"s{n}"]))
    mod_moved = moved_fraction(mod_before, mod_after)
    assert abs(ring_moved - 1 / (n + 1)) < 0.03
    assert abs(mod_moved - n / (n + 1)) < 0.02


def test_shares_sum_to_one_and_match_keys() -> None:
    ch = ConsistentHash([f"s{i}" for i in range(6)], v=50)
    shares = ch.shares()
    assert abs(sum(shares.values()) - 1) < 1e-9
    counts = {s: 0 for s in shares}
    for k in KEYS:
        counts[ch.lookup(k)] += 1
    for s in shares:
        assert abs(counts[s] / len(KEYS) - shares[s]) < 0.02


def test_position_is_in_range() -> None:
    xs = [h(k) for k in KEYS[:100]]
    assert all(0 <= x < RING for x in xs)
    assert len(set(xs)) == len(xs)
