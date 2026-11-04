# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-tree/. The authors are listed in prov/A58YZQ.jsonl.

from typing import Any, Generic, Iterable, Iterator, Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class WinnerTree(Generic[K]):
    """A winner tree on k players, in an array t[1 .. 2k-1].

    The leaves are t[k .. 2k-1], and t[k + i] = i. An internal node j holds the
    index of the winner of the match between its children 2j and 2j + 1. The
    player with the smaller key wins; on equal keys the smaller index wins.
    A key of None means "infinity": the player has left the tournament.
    """

    def __init__(self, keys: Sequence[K | None]) -> None:
        """Play all k - 1 matches in O(k) time."""
        k = len(keys)
        if k == 0:
            raise ValueError("a tournament needs at least one player")
        self.k = k
        self.key: list[K | None] = list(keys)
        self.t = [0] * (2 * k)
        for i in range(k):
            self.t[k + i] = i  # @line L1
        for j in range(k - 1, 0, -1):  # @line L2
            self.t[j] = self._play(self.t[2 * j], self.t[2 * j + 1])  # @line L3

    def _beats(self, a: int, b: int) -> bool:
        """True if player a beats player b."""
        ka, kb = self.key[a], self.key[b]
        if ka is None:
            return False if kb is not None else a < b
        if kb is None:
            return True
        if ka < kb:
            return True
        if kb < ka:
            return False
        return a < b

    def _play(self, a: int, b: int) -> int:
        return a if self._beats(a, b) else b

    def winner(self) -> int:
        """Return the index of the current winner."""
        return self.t[1] if self.k > 1 else 0  # @line L8

    def update(self, i: int, key: K | None) -> None:
        """Give player i a new key and replay its path to the root in O(log k)."""
        self.key[i] = key
        j = (self.k + i) // 2  # @line L4
        while j >= 1:  # @line L5
            self.t[j] = self._play(self.t[2 * j], self.t[2 * j + 1])  # @line L6
            j //= 2  # @line L7

    def check_invariant(self) -> None:
        """Check that every internal node holds the winner of its children."""
        k = self.k
        assert all(self.t[k + i] == i for i in range(k))
        for j in range(1, k):
            assert self.t[j] == self._play(self.t[2 * j], self.t[2 * j + 1])


class LoserTree(Generic[K]):
    """A loser tree on k players: l[j] holds the loser of the match at node j.

    l[0] holds the overall winner. A replay compares only along the path of
    the player that changed, one comparison per level.
    """

    def __init__(self, keys: Sequence[K | None]) -> None:
        """Play all matches in O(k) time and keep the losers."""
        k = len(keys)
        if k == 0:
            raise ValueError("a tournament needs at least one player")
        self.k = k
        self.key: list[K | None] = list(keys)
        self.l = [0] * k
        self.comparisons = 0
        win = [0] * (2 * k)
        for i in range(k):
            win[k + i] = i
        for j in range(k - 1, 0, -1):
            a, b = win[2 * j], win[2 * j + 1]
            if self._beats(a, b):
                win[j], self.l[j] = a, b
            else:
                win[j], self.l[j] = b, a
        self.l[0] = win[1] if k > 1 else 0

    def _beats(self, a: int, b: int) -> bool:
        self.comparisons += 1
        ka, kb = self.key[a], self.key[b]
        if ka is None:
            return False if kb is not None else a < b
        if kb is None:
            return True
        if ka < kb:
            return True
        if kb < ka:
            return False
        return a < b

    def winner(self) -> int:
        """Return the index of the current winner."""
        return self.l[0]

    def update(self, i: int, key: K | None) -> None:
        """Give player i, the current winner, a new key and replay its path."""
        self.key[i] = key
        w = i  # @line L9
        j = (self.k + i) // 2
        while j >= 1:  # @line L10
            if self._beats(self.l[j], w):  # @line L11
                w, self.l[j] = self.l[j], w
            j //= 2  # @line L12
        self.l[0] = w  # @line L13

    def check_invariant(self) -> None:
        """Rebuild the tournament from scratch and compare the losers and the winner."""
        fresh = LoserTree(self.key)
        assert fresh.l == self.l


def k_way_merge(runs: Sequence[Iterable[K]]) -> Iterator[K]:
    """Merge k sorted runs with a loser tree; ties go to the run of smaller index."""
    its = [iter(r) for r in runs]
    if not its:
        return
    heads: list[K | None] = [next(it, None) for it in its]
    tree = LoserTree(heads)
    while True:
        i = tree.winner()
        x = tree.key[i]
        if x is None:
            return
        yield x
        tree.update(i, next(its[i], None))


def tournament_sort(a: Sequence[K]) -> list[K]:
    """Sort by repeated winner extraction from a winner tree: O(n log n)."""
    if not a:
        return []
    tree = WinnerTree(list(a))
    out: list[K] = []
    for _ in range(len(a)):
        i = tree.winner()
        out.append(a[i])
        tree.update(i, None)
    return out
