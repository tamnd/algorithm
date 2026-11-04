# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meet-in-the-middle-attack/. The authors are listed in prov/ZGTKX7.jsonl.

from collections.abc import Callable, Sequence

Cipher = Callable[[int, int], int]


def meet_in_the_middle_attack(
    encrypt: Cipher,
    decrypt: Cipher,
    key_count: int,
    pairs: Sequence[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Return every key pair (k1, k2) with encrypt(k2, encrypt(k1, p)) == c for all (p, c) in pairs.

    encrypt(k, x) and decrypt(k, y) take a key in range(key_count) and a block.
    Precondition: pairs is not empty, and for each key, decrypt(k, .) is the
    inverse of the permutation encrypt(k, .).
    The result is sorted by k2, then by k1.
    Cost: 2 * key_count + 2 * c * (len(pairs) - 1) cipher calls, where c is the
    number of key pairs that match the first pair, expected O(key_count + c)
    dictionary operations, and a table of key_count entries.
    """
    p1, c1 = pairs[0]
    table: dict[int, list[int]] = {}  # @line L1
    for k1 in range(key_count):  # @line L2
        table.setdefault(encrypt(k1, p1), []).append(k1)  # @line L3
    result: list[tuple[int, int]] = []  # @line L4
    for k2 in range(key_count):  # @line L5
        x = decrypt(k2, c1)  # @line L6
        for k1 in table.get(x, []):  # @line L7
            if all(encrypt(k2, encrypt(k1, p)) == c for p, c in pairs[1:]):  # @line L8
                result.append((k1, k2))  # @line L9
    return result  # @line L10
