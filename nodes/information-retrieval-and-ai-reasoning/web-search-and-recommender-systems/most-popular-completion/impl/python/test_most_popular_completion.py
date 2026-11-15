# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/most-popular-completion/. The authors are listed in prov/PB06E3.jsonl.

import random

import pytest

from most_popular_completion import CompletionTrie, scan_top_k

# The log of the example on the page.
LOG = {
    "bing": 80,
    "binary search": 50,
    "bm25": 40,
    "binary search tree": 30,
    "bin packing": 25,
    "bit manipulation": 20,
    "binomial heap": 15,
}


def brute(log, prefix, k):
    """Sort the whole log by the tie rule: count descending, then query ascending."""
    ranked = sorted(log.items(), key=lambda qc: (-qc[1], qc[0]))
    return [qc for qc in ranked if qc[0].startswith(prefix)][:k]


def random_log(rng, size, alphabet, max_len, max_count):
    log = {}
    while len(log) < size:
        n = rng.randint(1, max_len)
        q = "".join(rng.choice(alphabet) for _ in range(n))
        log[q] = rng.randint(1, max_count)
    return log


def test_example_of_the_page():
    t = CompletionTrie(LOG)
    assert t.top_k("bin", 3) == [("bing", 80), ("binary search", 50), ("binary search tree", 30)]
    assert t.top_k("bi", 5) == [
        ("bing", 80),
        ("binary search", 50),
        ("binary search tree", 30),
        ("bin packing", 25),
        ("bit manipulation", 20),
    ]
    assert t.top_k("b", 2) == [("bing", 80), ("binary search", 50)]
    assert t.top_k("binary", 10) == [("binary search", 50), ("binary search tree", 30)]
    assert t.top_k("c", 3) == []
    assert t.top_k("bin", 0) == []


def test_tie_rule_uses_the_query_string():
    log = {"ab": 5, "aa": 5, "a": 5, "abc": 5, "b": 9}
    t = CompletionTrie(log)
    assert t.top_k("", 5) == [("b", 9), ("a", 5), ("aa", 5), ("ab", 5), ("abc", 5)]
    assert t.top_k("a", 2) == [("a", 5), ("aa", 5)]


@pytest.mark.parametrize("seed", range(40))
def test_every_prefix_matches_brute_force(seed):
    rng = random.Random(seed)
    alphabet = "abc" if seed % 2 == 0 else "ab c"
    log = random_log(rng, rng.randint(1, 40), alphabet, 6, rng.choice([3, 20, 1000]))
    t = CompletionTrie(log)
    longest = max(len(q) for q in log)
    prefixes = {""} | {q[:i] for q in log for i in range(len(q) + 1)}
    prefixes |= {"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4))) for _ in range(20)}
    for p in sorted(prefixes):
        n_p = sum(1 for q in log if q.startswith(p))
        for k in range(0, len(log) + 2):
            got = t.top_k(p, k)
            assert got == brute(log, p, k) == scan_top_k(log, p, k)
            # Every popped node lies on the path from the prefix node to an answer.
            assert t.pops <= min(k, n_p) * (longest - len(p) + 1)


def test_rejects_bad_logs():
    with pytest.raises(ValueError):
        CompletionTrie({"a": 0})
    with pytest.raises(ValueError):
        CompletionTrie({"": 3})
