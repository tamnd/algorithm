# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zaks-tree-generation/. The authors are listed in prov/R3V9R0.jsonl.

import itertools
import math
import random

import pytest

from zaks_tree_generation import next_z, z_sequences, z_to_bits, z_to_dyck


def fuss_catalan(n: int, t: int) -> int:
    return math.comb(t * n, n) // ((t - 1) * n + 1)


def is_tree_word(w: str, t: int) -> bool:
    """Preorder word of an extended t-ary tree: weight t - 1 per '1', -1 per '0'."""
    s = 0
    for k, c in enumerate(w):
        s += t - 1 if c == "1" else -1
        if s < 0 and k != len(w) - 1:
            return False
    return s == -1


def brute_force(n: int, t: int) -> list[tuple[int, ...]]:
    out = []
    for pos in itertools.combinations(range(1, t * n + 2), n):
        w = ["0"] * (t * n + 1)
        for p in pos:
            w[p - 1] = "1"
        if is_tree_word("".join(w), t):
            out.append(pos)
    return out  # combinations come in lexicographic order


def test_example() -> None:
    z = [1, 2, 4, 7]
    assert next_z(z)
    assert z == [1, 2, 5, 6]
    z = [1, 2, 5, 7]
    assert next_z(z)
    assert z == [1, 3, 4, 5]
    assert z_to_dyck((1, 3, 4, 5)) == "()((()))"


def test_edges() -> None:
    assert list(z_sequences(0)) == [()]
    assert list(z_sequences(1)) == [(1,)]
    assert list(z_sequences(1, 5)) == [(1,)]
    z: list[int] = []
    assert not next_z(z)
    last = [1, 3, 5, 7]
    assert not next_z(last) and last == [1, 3, 5, 7]
    with pytest.raises(ValueError):
        list(z_sequences(-1))
    with pytest.raises(ValueError):
        list(z_sequences(2, 1))


def test_brute_force() -> None:
    for t in (2, 3, 4):
        for n in range(0, 7 if t == 2 else 6):
            assert list(z_sequences(n, t)) == brute_force(n, t)


def test_counts() -> None:
    for t in (2, 3, 5):
        for n in range(0, 10 if t == 2 else 8):
            assert sum(1 for _ in z_sequences(n, t)) == fuss_catalan(n, t)


def test_same_order_as_dyck_words() -> None:
    for n in range(0, 9):
        words = [z_to_dyck(z) for z in z_sequences(n)]
        assert words == sorted(words)  # '(' < ')' in ASCII
        assert len(set(words)) == math.comb(2 * n, n) // (n + 1)


def test_amortized_cost() -> None:
    # Cells read and written by next_z, summed over the whole list, stay below 4 per tree.
    for t in (2, 3):
        for n in range(1, 10 if t == 2 else 7):
            total = 0
            count = 0
            z = list(range(1, n + 1))
            while True:
                count += 1
                r = 0
                while r < n and z[n - 1 - r] == t * (n - 1 - r) + 1:
                    r += 1
                total += 2 * r + 2
                if not next_z(z, t):
                    break
            assert count == fuss_catalan(n, t)
            assert total <= 4 * count


def test_random_successors() -> None:
    rng = random.Random(6)
    for _ in range(400):
        t = rng.randint(2, 4)
        n = rng.randint(1, 30)
        # Build a random valid sequence greedily from a random tree word.
        z = [1]
        for i in range(2, n + 1):
            z.append(rng.randint(z[-1] + 1, t * (i - 1) + 1))
        w = z_to_bits(z, t)
        assert is_tree_word(w, t)
        nz = list(z)
        if next_z(nz, t):
            assert tuple(nz) > tuple(z)
            assert is_tree_word(z_to_bits(nz, t), t)
            # No valid sequence lies strictly between z and nz: check the suffix is minimal.
            j = next(k for k in range(n) if nz[k] != z[k])
            assert nz[j] == z[j] + 1
            assert all(nz[k] == nz[k - 1] + 1 for k in range(j + 1, n))
            assert all(z[k] == t * k + 1 for k in range(j + 1, n))
        else:
            assert all(z[k] == t * k + 1 for k in range(n))
