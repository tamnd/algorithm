# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packed-trie/. The authors are listed in prov/JVDGBF.jsonl.

import random

from packed_trie import PackedTrie

# The nine patterns of the example in The TeXbook, Appendix H, as letters -> gap values.
TEXBOOK = {
    "hyph": (0, 0, 3, 0, 0),
    "hen": (0, 0, 2, 0),
    "hena": (0, 0, 0, 0, 4),
    "henat": (0, 0, 0, 5, 0, 0),
    "na": (1, 0, 0),
    "nat": (0, 2, 0, 0),
    "tio": (1, 0, 0, 0),
    "io": (2, 0, 0),
    "on": (0, 2, 0),
}


def check_invariants(t, keys):
    t.check_invariant()
    # every slot is claimed by at most one family: the owner list records one family per slot
    claimed = [s for s, ch in enumerate(t.char) if ch is not None]
    assert len(claimed) == t.transitions
    assert len(t.taken) == t.families  # distinct bases
    # each family's slots are exactly base + code(letter) for its letters
    trie_transitions = len({k[:i] for k in keys for i in range(1, len(k) + 1)})
    assert t.transitions == trie_transitions
    assert t.size() >= t.transitions


def test_texbook_patterns():
    t = PackedTrie(TEXBOOK)
    for k, v in TEXBOOK.items():
        assert t.get(k) == v
    for k in ["h", "he", "hy", "hyp", "henx", "x", "", "nati", "o", "tion"]:
        assert t.get(k) is None
    check_invariants(t, TEXBOOK)
    # the walk of Liang's method on .hyphenation. finds the same patterns as a scan
    w = ".hyphenation."
    found = sorted((i, w[i:e]) for i in range(len(w)) for e, _ in t.prefix_values(w, i))
    scan = sorted((i, k) for k in TEXBOOK for i in range(len(w)) if w.startswith(k, i))
    assert found == scan
    v = [0] * (len(w) + 1)
    for i in range(len(w)):
        for _, vals in t.prefix_values(w, i):
            for d, x in enumerate(vals):
                v[i + d] = max(v[i + d], x)
    assert v[2:12] == [0, 3, 0, 0, 2, 5, 4, 2, 0, 2]


def random_keys(rng, n, alphabet, kmax):
    keys = {}
    while len(keys) < n:
        k = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, kmax)))
        keys[k] = len(keys)
    return keys


def test_lookup_agrees_with_a_dict():
    rng = random.Random(5)
    for trial in range(30):
        alphabet = "abcdefghij"[: rng.randint(2, 10)]
        keys = random_keys(rng, rng.randint(1, 60), alphabet, 6)
        t = PackedTrie(keys, alphabet=alphabet)
        check_invariants(t, keys)
        for k, v in keys.items():
            assert t.get(k) == v and k in t
        for _ in range(200):
            q = "".join(rng.choice(alphabet + "z") for _ in range(rng.randint(0, 7)))
            assert t.get(q) == keys.get(q)


def test_no_slot_is_shared_and_lookups_never_cross_families():
    rng = random.Random(9)
    keys = random_keys(rng, 300, "abcdefghijklmnopqrstuvwxyz", 7)
    t = PackedTrie(keys)
    check_invariants(t, keys)
    # follow every transition and check that it lands in a slot owned by the right family
    fam_of_base = {}
    stack = [(t.root_base, "")]
    seen = 0
    while stack:
        base, prefix = stack.pop()
        fams = set()
        for ch in t.code:
            s = t._slot(base, ch)
            if s is not None:
                fams.add(t.owner[s])
                seen += 1
                if t.link[s] is not None:
                    stack.append((t.link[s], prefix + ch))
        assert len(fams) == 1  # all transitions found from one base belong to one family
        assert base not in fam_of_base
        fam_of_base[base] = fams.pop()
    assert seen == t.transitions


def test_size_against_sum_of_node_sizes():
    # The density of first fit is a measurement, not a guarantee. On this fixed
    # random set of 1000 keys the table must beat the unpacked indexed trie by far.
    # Measured: 3563 transitions, 2670 families, 3654 slots, density 0.975.
    rng = random.Random(1983)
    keys = random_keys(rng, 1000, "abcdefghijklmnopqrstuvwxyz", 8)
    t = PackedTrie(keys)
    sigma = len(t.code)
    unpacked = t.families * sigma  # one array of sigma slots per family
    assert t.transitions <= t.size() <= t.transitions + 2 * sigma + t.families // 10
    assert t.size() * 5 < unpacked
    assert t.density() > 0.85
