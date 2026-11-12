# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-bitmap/. The authors are listed in prov/FD46E0.jsonl.

import random

from tree_bitmap import TreeBitmap, brute_force_lpm, rank


def random_prefix(rng, w):
    l = rng.randint(0, w)
    return rng.getrandbits(l) if l else 0, l


def test_rank():
    assert rank(0b101101, 0) == 0
    assert rank(0b101101, 3) == 2
    assert rank(0b101101, 6) == 4


def test_page_example():
    # Stride 4, W = 8: the example of the page.
    tb = TreeBitmap(8, 4)
    table = {(0, 0): "A", (0b1, 1): "B", (0b101, 3): "C", (0b10110, 5): "D", (0b1011011, 7): "E", (0b0110, 4): "F"}
    for (p, l), hop in table.items():
        tb.insert(p, l, hop)
    root = tb.root
    # Internal bits: * -> 0, 1* -> 2, 101* -> 7 + 5 = 12.
    assert root.internal == (1 << 0) | (1 << 2) | (1 << 12)
    # External bits: chunks 1011 (11) for D and E, 0110 (6) for F.
    assert root.external == (1 << 6) | (1 << 11)
    assert root.results == ["A", "B", "C"]
    child_f, child_de = root.children
    assert child_f.internal == 1 and child_f.results == ["F"]
    # D = 1011 0* -> j = 1, v = 0 -> bit 1; E = 1011 011* -> j = 3, v = 3 -> bit 10.
    assert child_de.internal == (1 << 1) | (1 << 10)
    assert child_de.results == ["D", "E"]
    assert tb.lookup(0b10110110) == ("E", 3)
    assert tb.lookup(0b10110001) == ("D", 3)
    assert tb.lookup(0b10111111) == ("C", 3)
    assert tb.lookup(0b01100000) == ("F", 3)
    assert tb.lookup(0b01110000) == ("A", 2)
    assert tb.check_layout() == 3


def test_against_brute_force_exhaustive():
    rng = random.Random(5)
    for w, s in [(8, 4), (8, 3), (9, 4), (6, 1), (8, 8)]:
        for _ in range(6):
            tb = TreeBitmap(w, s)
            table = {}
            for _ in range(rng.randint(1, 50)):
                p, l = random_prefix(rng, w)
                table[(p, l)] = rng.randint(0, 99)
                tb.insert(p, l, table[(p, l)])
            tb.check_layout()
            assert tb.prefixes() == table
            levels = -(-w // s) + 1
            for addr in range(1 << w):
                hop, reads = tb.lookup(addr)
                assert hop == brute_force_lpm(table, addr, w)
                assert reads <= levels + 1


def test_random_updates_keep_layout():
    rng = random.Random(42)
    w, s = 12, 4
    tb = TreeBitmap(w, s)
    table = {}
    for step in range(1500):
        if table and rng.random() < 0.45:
            key = rng.choice(list(table))
            assert tb.delete(*key)
            del table[key]
            assert not tb.delete(*key)
        else:
            p, l = random_prefix(rng, w)
            table[(p, l)] = step
            tb.insert(p, l, step)
        tb.check_layout()
        if step % 100 == 0:
            assert tb.prefixes() == table
            for addr in range(0, 1 << w, 7):
                assert tb.lookup(addr)[0] == brute_force_lpm(table, addr, w)
    for key in list(table):
        tb.delete(*key)
    assert tb.check_layout() == 1
    assert tb.root.internal == 0 and tb.root.external == 0


def test_ipv4():
    rng = random.Random(9)
    w = 32
    tb = TreeBitmap(w, 4)
    table = {(0, 0): "default"}
    tb.insert(0, 0, "default")
    for i in range(600):
        p, l = random_prefix(rng, w)
        table[(p, l)] = i
        tb.insert(p, l, i)
    tb.check_layout()
    keys = list(table)
    for _ in range(3000):
        p, l = rng.choice(keys)
        addr = (p << (w - l)) | rng.getrandbits(w - l) if l < w else p
        hop, reads = tb.lookup(addr)
        assert hop == brute_force_lpm(table, addr, w)
        assert reads <= 10  # at most 9 nodes and 1 result read
