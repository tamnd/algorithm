# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-prefix-match/. The authors are listed in prov/X7VXG1.jsonl.

import random

from longest_prefix_match import (
    BinarySearchOnLengths,
    BinaryTrie,
    brute_force_lpm,
    random_table,
)


def build_trie(table, w):
    t = BinaryTrie(w)
    for (p, l), hop in table.items():
        t.insert(p, l, hop)
    return t


def test_example_table():
    # The 8-bit example of the page.
    w = 8
    table = {(0, 0): "A", (0b1, 1): "B", (0b101, 3): "C", (0b10110, 5): "D", (0b1011011, 7): "E"}
    trie = build_trie(table, w)
    bsl = BinarySearchOnLengths(table, w)
    cases = {0b10110110: (0b1011011, 7, "E"), 0b10110001: (0b10110, 5, "D"),
             0b10100000: (0b101, 3, "C"), 0b11000000: (0b1, 1, "B"), 0b01111111: (0, 0, "A")}
    for addr, want in cases.items():
        assert brute_force_lpm(table, addr, w) == want
        assert trie.lookup(addr)[0] == want
        assert bsl.lookup(addr)[0] == want
    assert trie.lookup(0b10110110)[1] == 8
    assert bsl.lengths == [0, 1, 3, 5, 7]
    assert bsl.markers == 0
    assert bsl.lookup(0b10110110)[1] == 3


def test_marker_needed():
    # A long prefix with no shorter prefix on its path needs markers.
    w = 8
    table = {(0, 0): "A", (0b0, 1): "B", (0b11, 2): "C", (0b1111, 4): "D", (0b0001111, 7): "E"}
    bsl = BinarySearchOnLengths(table, w)
    assert bsl.markers == 2  # "00" at length 2 and "0001" at length 4
    assert bsl.tables[2][0b00] == (0, 1, "B")
    assert bsl.tables[3][0b0001] == (0, 1, "B")
    assert bsl.lookup(0b00011110) == ((0b0001111, 7, "E"), 3)
    assert bsl.lookup(0b00010000) == ((0, 1, "B"), 3)
    assert bsl.lookup(0b11111111)[0] == (0b1111, 4, "D")
    assert bsl.lookup(0b10000000)[0] == (0, 0, "A")


def test_exhaustive_small_width():
    rng = random.Random(7)
    w = 8
    for trial in range(30):
        table = random_table(rng, rng.randint(1, 40), w, with_default=trial % 2 == 0)
        trie = build_trie(table, w)
        bsl = BinarySearchOnLengths(table, w)
        bound = len(bsl.lengths).bit_length()
        for addr in range(1 << w):
            want = brute_force_lpm(table, addr, w)
            got, reads = trie.lookup(addr)
            assert got == want
            assert reads <= w + 1
            got, probes = bsl.lookup(addr)
            assert got == want
            assert probes <= bound


def test_ipv4_random():
    rng = random.Random(2024)
    w = 32
    for _ in range(5):
        table = random_table(rng, 300, w)
        # Add nested prefixes so that long matches occur.
        for (p, l) in list(table):
            if l <= 24:
                ext = rng.randint(1, 8)
                table[((p << ext) | rng.getrandbits(ext), l + ext)] = "x"
        trie = build_trie(table, w)
        bsl = BinarySearchOnLengths(table, w)
        keys = list(table)
        for _ in range(2000):
            if rng.random() < 0.7:
                p, l = rng.choice(keys)
                addr = (p << (w - l)) | rng.getrandbits(w - l) if l < w else p
            else:
                addr = rng.getrandbits(w)
            want = brute_force_lpm(table, addr, w)
            assert trie.lookup(addr)[0] == want
            got, probes = bsl.lookup(addr)
            assert got == want
            assert probes <= 6  # at most 33 lengths: ceil(log2(34)) = 6


def test_trie_delete():
    rng = random.Random(11)
    w = 6
    table = random_table(rng, 30, w)
    trie = build_trie(table, w)
    keys = list(table)
    rng.shuffle(keys)
    for key in keys[:20]:
        assert trie.delete(*key)
        del table[key]
        assert not trie.delete(*key)
        for addr in range(1 << w):
            assert trie.lookup(addr)[0] == brute_force_lpm(table, addr, w)
    for key in keys[20:]:
        trie.delete(*key)
    assert trie.size == 0
    assert trie.node_count() == 1
