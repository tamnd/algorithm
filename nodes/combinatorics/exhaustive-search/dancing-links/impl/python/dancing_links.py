# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dancing-links/. The authors are listed in prov/48VR35.jsonl.

from collections.abc import Hashable, Iterator, Sequence


class DancingLinks:
    """Knuth's dancing-links representation of an exact cover matrix.

    Node 0 is the root of the list of active primary items. Nodes 1 to N are
    the item headers, in the order primary items then secondary items. Then
    come the option nodes, with one spacer node before each option and one
    after the last option. A spacer x has top[x] <= 0; ulink[x] is the first
    node of the option before it and dlink[x] is the last node of the option
    after it, so that a walk along an option can wrap around.
    """

    def __init__(
        self,
        primary: Sequence[Hashable],
        options: Sequence[Sequence[Hashable]],
        secondary: Sequence[Hashable] = (),
    ) -> None:
        names = list(primary) + list(secondary)
        if len(set(names)) != len(names):
            raise ValueError("items must be distinct")
        self.names = names
        self.n_primary = len(primary)
        index = {name: k + 1 for k, name in enumerate(names)}
        n = len(names)
        self.llink = [0] * (n + 1)
        self.rlink = [0] * (n + 1)
        # The primary items form a circular list through the root 0.
        for k in range(1, self.n_primary + 1):
            self.llink[k] = k - 1
            self.rlink[k - 1] = k
        self.llink[0] = self.n_primary
        self.rlink[self.n_primary] = 0
        # A secondary item is a list of its own, so that cover and uncover
        # leave the root list alone.
        for k in range(self.n_primary + 1, n + 1):
            self.llink[k] = self.rlink[k] = k
        self.top = list(range(n + 1))
        self.top[0] = 0
        self.ulink = list(range(n + 1))
        self.dlink = list(range(n + 1))
        self.length = [0] * (n + 1)
        self.option_of = [-1] * (n + 1)
        prim = set(primary)
        last_spacer = len(self.top)
        self._push(0, -1)  # the first spacer
        spacer_count = 0
        for j, opt in enumerate(options):
            row = list(opt)
            if not row or len(set(row)) != len(row) or any(x not in index for x in row):
                raise ValueError("bad option")
            if not set(row) & prim:
                raise ValueError("each option must contain a primary item")
            first = len(self.top)
            for name in row:
                i = index[name]
                x = len(self.top)
                self._push(i, j)
                # Append x at the bottom of the column of item i.
                self.ulink[x] = self.ulink[i]
                self.dlink[x] = i
                self.dlink[self.ulink[i]] = x
                self.ulink[i] = x
                self.length[i] += 1
            spacer_count += 1
            self.dlink[last_spacer] = len(self.top) - 1  # the last node of this option
            last_spacer = len(self.top)
            self._push(-spacer_count, -1)
            self.ulink[last_spacer] = first
        self.dlink[last_spacer] = last_spacer  # nothing after the last spacer
        self.n_options = len(options)

    def _push(self, top: int, option: int) -> None:
        x = len(self.top)
        self.top.append(top)
        self.ulink.append(x)
        self.dlink.append(x)
        self.option_of.append(option)

    # The four list operations of the page.

    def hide(self, p: int) -> None:
        """Remove the other nodes of the option of node p from their columns."""
        q = p + 1  # @line L1
        while q != p:  # @line L2
            x, u, d = self.top[q], self.ulink[q], self.dlink[q]  # @line L3
            if x <= 0:  # @line L4
                q = u  # a spacer: go back to the first node of the option
            else:
                self.dlink[u] = d  # @line L5
                self.ulink[d] = u
                self.length[x] -= 1
                q += 1  # @line L6

    def unhide(self, p: int) -> None:
        """Undo hide(p)."""
        q = p - 1  # @line L13
        while q != p:  # @line L14
            x, u, d = self.top[q], self.ulink[q], self.dlink[q]  # @line L15
            if x <= 0:  # @line L16
                q = d  # a spacer: go forward to the last node of the option
            else:
                self.dlink[u] = q  # @line L17
                self.ulink[d] = q
                self.length[x] += 1
                q -= 1  # @line L18

    def cover(self, i: int) -> None:
        """Make item i inactive and hide every option that contains it."""
        p = self.dlink[i]  # @line L7
        while p != i:  # @line L8
            self.hide(p)  # @line L9
            p = self.dlink[p]  # @line L10
        left, right = self.llink[i], self.rlink[i]  # @line L11
        self.rlink[left] = right  # @line L12
        self.llink[right] = left

    def uncover(self, i: int) -> None:
        """Undo cover(i)."""
        left, right = self.llink[i], self.rlink[i]  # @line L19
        self.rlink[left] = i  # @line L20
        self.llink[right] = i
        p = self.ulink[i]  # @line L21
        while p != i:  # @line L22
            self.unhide(p)  # @line L23
            p = self.ulink[p]  # @line L24

    # Views used by the tests and by the search.

    def item(self, name: Hashable) -> int:
        return self.names.index(name) + 1

    def active_items(self) -> list[Hashable]:
        """The active primary items, in list order."""
        out = []
        i = self.rlink[0]
        while i != 0:
            out.append(self.names[i - 1])
            i = self.rlink[i]
        return out

    def active_options(self, name: Hashable) -> list[int]:
        """The indices of the options in the column of an item, top to bottom."""
        i = self.item(name)
        out = []
        p = self.dlink[i]
        while p != i:
            out.append(self.option_of[p])
            p = self.dlink[p]
        return out

    def state(self) -> tuple:
        """A copy of all links and lengths, to compare states."""
        return (tuple(self.llink), tuple(self.rlink), tuple(self.ulink), tuple(self.dlink), tuple(self.length))

    def solve(self) -> Iterator[list[int]]:
        """Yield every exact cover as a list of option indices, by Algorithm X.

        The search branches on the active primary item with the fewest active
        options (the first in list order on a tie). It uses an explicit stack.
        """
        chosen: list[int] = []  # the option node chosen at each level
        stack: list[tuple[int, int]] = []  # (item, current node) per level
        while True:
            if self.rlink[0] == 0:
                yield [self.option_of[x] for x in chosen]
                go_down = False
            else:
                i, best = self.rlink[0], -1
                while i != 0:
                    if best < 0 or self.length[i] < self.length[best]:
                        best = i
                    i = self.rlink[i]
                self.cover(best)
                stack.append((best, best))
                go_down = False
            # Advance to the next option at the deepest level, or backtrack.
            while stack:
                i, x = stack[-1]
                if x != i:
                    # Undo the choice of node x.
                    q = x - 1
                    while q != x:
                        j = self.top[q]
                        if j <= 0:
                            q = self.dlink[q]
                        else:
                            self.uncover(j)
                            q -= 1
                    chosen.pop()
                x = self.dlink[x]
                if x == i:
                    self.uncover(i)
                    stack.pop()
                    continue
                stack[-1] = (i, x)
                chosen.append(x)
                q = x + 1
                while q != x:
                    j = self.top[q]
                    if j <= 0:
                        q = self.ulink[q]
                    else:
                        self.cover(j)
                        q += 1
                go_down = True
                break
            if not go_down:
                return


def dancing_links_exact_covers(
    primary: Sequence[Hashable],
    options: Sequence[Sequence[Hashable]],
    secondary: Sequence[Hashable] = (),
) -> list[list[int]]:
    """Return all exact covers, each as a sorted list of option indices."""
    return [sorted(s) for s in DancingLinks(primary, options, secondary).solve()]
