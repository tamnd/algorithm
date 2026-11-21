# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/km-anonymity/. The authors are listed in prov/YFDA8G.jsonl.

from collections.abc import Hashable, Iterable, Mapping, Sequence
from itertools import combinations


def is_km_anonymous(transactions: Sequence[Iterable[Hashable]], k: int, m: int) -> bool:
    """Return True if every itemset of at most m items has support 0 or at least k.

    Each transaction is read as a set of items. Precondition: k >= 1, m >= 0.
    Cost: O(sum over transactions t of C(|t|, 1) + ... + C(|t|, m)) hash map
    updates, which is O(|D| tau^m) for transactions of at most tau items.
    """
    counts: dict[frozenset[Hashable], int] = {}  # @line L1
    for t in transactions:  # @line L2
        items = list(set(t))
        for size in range(1, m + 1):
            for subset in combinations(items, size):  # @line L3
                key = frozenset(subset)
                counts[key] = counts.get(key, 0) + 1  # @line L4
    for c in counts.values():  # @line L5
        if c < k:  # @line L6
            return False
    return True  # @line L7


def generalize(transactions: Sequence[Iterable[Hashable]], cut: Mapping[Hashable, Hashable]) -> list[frozenset[Hashable]]:
    """Apply a global recoding: replace each item by cut[item] (or keep it if absent), with set semantics.

    Cost: O(total number of items).
    """
    return [frozenset(cut.get(x, x) for x in t) for t in transactions]
