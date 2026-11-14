# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asf-b-star-tree/. The authors are listed in prov/TQF55M.jsonl.

"""An ASF-B*-tree for one symmetric set of cells with a vertical axis at x = 0.

The group is a dict cells: name -> (kind, w, h), with kind "pair" for a
symmetric pair (two cells of size w x h, mirrored about the axis) and "self"
for a self-symmetric cell of size w x h (centered on the axis). The tree holds
one representative per entry: the right cell of a pair, of size w x h, and the
right half of a self-symmetric cell, of size w/2 x h.

As on the B*-tree page, the left child c of b has x_c = x_b + w_b, and the right
child has x_c = x_b. The tree is an ASF-B*-tree when every self-symmetric
representative is on the rightmost branch: the root and its chain of right
children, which is where x = 0.
"""

from fractions import Fraction


class ASFBStarTree:
    def __init__(self, cells: dict, root=None, left=None, right=None) -> None:
        self.cells = {b: (k, Fraction(w), Fraction(h)) for b, (k, w, h) in cells.items()}
        if root is None:
            # self representatives on the right chain from the root, pairs as a chain of left children
            selfs = [b for b in self.cells if self.cells[b][0] == "self"]
            pairs = [b for b in self.cells if self.cells[b][0] == "pair"]
            order = selfs + pairs
            self.root = order[0] if order else None
            self.left = {b: None for b in order}
            self.right = {b: None for b in order}
            for a, b in zip(selfs, selfs[1:]):
                self.right[a] = b
            prev = selfs[-1] if selfs else None
            for b in pairs:
                if prev is not None:
                    self.left[prev] = b
                prev = b
        else:
            self.root, self.left, self.right = root, dict(left), dict(right)

    def rep_size(self, b) -> tuple:
        k, w, h = self.cells[b]
        return (w / 2, h) if k == "self" else (w, h)

    def rightmost_branch(self) -> list:
        out, b = [], self.root
        while b is not None:
            out.append(b)
            b = self.right[b]
        return out

    def is_asf(self) -> bool:
        on = set(self.rightmost_branch())
        return all(b in on for b in self.left if self.cells[b][0] == "self")

    def preorder(self) -> list:
        out, stack = [], [self.root] if self.root is not None else []
        while stack:
            b = stack.pop()
            out.append(b)
            for c in (self.right[b], self.left[b]):
                if c is not None:
                    stack.append(c)
        return out

    def pack(self) -> dict:
        """Pack the representatives as a B*-tree, then mirror them about x = 0.
        Returns the rectangles (x, y, w, h) of the whole group, keyed by
        (name, "R") and (name, "L") for a pair and (name, "S") for a
        self-symmetric cell, with the width and the height of the group."""
        if not self.is_asf():
            raise ValueError("a self-symmetric representative is off the rightmost branch")
        pos = {}
        parent_x = {self.root: (None, None)}
        for b in self.preorder():  # @line L1
            w, h = self.rep_size(b)
            p, side = parent_x[b]
            if p is None:  # @line L2
                x = Fraction(0)
            elif side == "left":
                x = pos[p][0] + self.rep_size(p)[0]
            else:
                x = pos[p][0]
            # @line L3: the highest top among the placed representatives whose x-range meets [x, x + w)
            y = max((pos[c][1] + self.rep_size(c)[1] for c in pos if pos[c][0] < x + w and x < pos[c][0] + self.rep_size(c)[0]), default=Fraction(0))
            pos[b] = (x, y)  # @line L4
            if self.left[b] is not None:
                parent_x[self.left[b]] = (b, "left")
            if self.right[b] is not None:
                parent_x[self.right[b]] = (b, "right")
        rects = {}
        for b, (x, y) in pos.items():
            k, w, h = self.cells[b]
            if k == "pair":  # @line L5: the partner is the mirror image
                rects[(b, "R")] = (x, y, w, h)
                rects[(b, "L")] = (-x - w, y, w, h)
            else:  # @line L6: a self-symmetric cell is its half and the mirror of its half
                assert x == 0
                rects[(b, "S")] = (-w / 2, y, w, h)
        half = max((x + self.rep_size(b)[0] for b, (x, _) in pos.items()), default=Fraction(0))
        height = max((y + self.rep_size(b)[1] for b, (_, y) in pos.items()), default=Fraction(0))
        return {"rects": rects, "width": 2 * half, "height": height}  # @line L7

    # The moves of the annealing. Each keeps the tree an ASF-B*-tree.

    def rotate(self, b) -> None:
        k, w, h = self.cells[b]
        self.cells[b] = (k, h, w)

    def swap(self, a, b) -> None:
        """Exchange two labels. A self-symmetric label may only go to a node on
        the rightmost branch."""
        on = set(self.rightmost_branch())
        for u, v in ((a, b), (b, a)):
            if self.cells[u][0] == "self" and v not in on:
                raise ValueError("this swap would move a self-symmetric representative off the rightmost branch")
        m = {a: b, b: a}

        def rn(z):
            return m.get(z, z)

        self.root = rn(self.root)
        self.left = {rn(u): rn(c) for u, c in self.left.items()}
        self.right = {rn(u): rn(c) for u, c in self.right.items()}

    def _parent(self, b):
        for u in self.left:
            if self.left[u] == b:
                return u, "left"
            if self.right[u] == b:
                return u, "right"
        return None, None

    def delete(self, b) -> None:
        """Remove b. A node with two children is first swapped down along its
        left children, so the rightmost branch keeps its self-symmetric labels."""
        while self.left[b] is not None and self.right[b] is not None:
            c = self.left[b]
            m = {b: c, c: b}

            def rn(z):
                return m.get(z, z)

            self.root = rn(self.root)
            self.left = {rn(u): rn(v) for u, v in self.left.items()}
            self.right = {rn(u): rn(v) for u, v in self.right.items()}
        child = self.left[b] if self.left[b] is not None else self.right[b]
        p, side = self._parent(b)
        if p is None:
            self.root = child
        elif side == "left":
            self.left[p] = child
        else:
            self.right[p] = child
        del self.left[b], self.right[b]

    def insert(self, b, p, side: str) -> None:
        """Insert b as the side child of p; the old child becomes the child of b
        on the same side. With p None, b becomes the root and the old root its
        right child. A self-symmetric b may only go on the rightmost branch."""
        if self.cells[b][0] == "self" and not (p is None or (side == "right" and p in set(self.rightmost_branch()))):
            raise ValueError("a self-symmetric representative must be inserted on the rightmost branch")
        self.left[b], self.right[b] = None, None
        if p is None:
            self.right[b], self.root = self.root, b
        elif side == "left":
            self.left[b], self.left[p] = self.left[p], b
        else:
            self.right[b], self.right[p] = self.right[p], b
