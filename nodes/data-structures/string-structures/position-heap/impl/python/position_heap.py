# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-heap/. The authors are listed in prov/PDF2MC.jsonl.


class PositionHeap:
    """The position heap of a text, built by prepending symbols.

    The suffixes are inserted from the shortest to the longest, each as the
    shortest prefix of it that is not yet a node. Every node but the root holds
    one suffix, stored by its length so that prepending does not renumber it.
    Seen from the reversed text, the suffixes are its reversed prefixes, and
    prepending to the text is appending to the reversed text.
    """

    def __init__(self, text: str = "") -> None:
        self.rev: list[str] = []  # the text, reversed
        self.children: list[dict[str, int]] = [{}]  # node 0 is the root
        self.length: list[int] = [0]  # suffix length held by each node
        self.depth: list[int] = [0]
        for c in reversed(text):
            self.prepend(c)

    @property
    def text(self) -> str:
        return "".join(reversed(self.rev))

    def _sym(self, ell: int, k: int) -> str:
        """Symbol k of the suffix of length ell."""
        return self.rev[ell - 1 - k]

    def prepend(self, c: str) -> None:
        """Make the text c + text and insert its new longest suffix."""
        self.rev.append(c)
        ell = len(self.rev)
        x, k = 0, 0  # @line L1
        while self._sym(ell, k) in self.children[x]:  # @line L2
            x = self.children[x][self._sym(ell, k)]
            k += 1
        y = len(self.length)  # @line L3
        self.children.append({})
        self.length.append(ell)
        self.depth.append(k + 1)
        self.children[x][self._sym(ell, k)] = y

    def _occurs_at(self, p: str, ell: int) -> bool:
        return ell >= len(p) and all(self._sym(ell, k) == p[k] for k in range(len(p)))

    def search(self, p: str) -> list[int]:
        """The sorted start positions of the occurrences of p in the text."""
        if p == "":
            raise ValueError("the pattern must be nonempty")
        n = len(self.rev)
        found: list[int] = []
        x, k = 0, 0  # @line L4
        while k < len(p) and p[k] in self.children[x]:
            x = self.children[x][p[k]]
            k += 1
            if k < len(p) and self._occurs_at(p, self.length[x]):  # @line L5
                found.append(self.length[x])
        if k == len(p):  # @line L6
            stack = [x]
            while stack:
                y = stack.pop()
                found.append(self.length[y])
                stack.extend(self.children[y].values())
        return sorted(n - ell for ell in found)  # @line L7

    def check_invariant(self) -> None:
        n = len(self.rev)
        assert len(self.length) == n + 1 and sorted(self.length) == list(range(n + 1))
        stack = [(0, "")]
        seen = 0
        while stack:
            x, s = stack.pop()
            seen += 1
            assert self.depth[x] == len(s)
            ell = self.length[x]
            assert ell >= len(s) and all(self._sym(ell, k) == s[k] for k in range(len(s)))
            for c, y in self.children[x].items():
                assert self.length[y] > ell, "heap order"
                stack.append((y, s + c))
        assert seen == n + 1
