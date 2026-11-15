# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slope-one/. The authors are listed in prov/2RYX1J.jsonl.

"""Slope One and Weighted Slope One (Lemire and Maclachlan 2005).

For two items j and i, S(j, i) is the set of users who rated both, and

    dev(j, i) = sum over S(j, i) of (r_uj - r_ui) / |S(j, i)|.

The tables keep the sum of the differences and the count c(j, i) for
each pair, so a new or removed rating updates them in time linear in the
number of items its user rated. For user u and item j, R_j is the set of
items i != j that u rated with c(j, i) > 0. Slope One predicts

    mean over i in R_j of (dev(j, i) + r_ui)

and Weighted Slope One predicts

    sum over i in R_j of (dev(j, i) + r_ui) c(j, i) / sum of c(j, i).

If R_j is empty, both return the mean of user u, or the mean of all
ratings if u has none.
"""


class SlopeOne:
    def __init__(self):
        self.ratings = {}  # user -> {item: rating}
        self.diff = {}  # (j, i) -> sum of r_uj - r_ui over S(j, i)
        self.count = {}  # (j, i) -> |S(j, i)|
        self.total = 0.0
        self.n = 0

    def add(self, u, i, v):
        """Add the rating v of user u for item i (replaces an old one)."""
        row = self.ratings.setdefault(u, {})
        if i in row:  # @line L1
            self.remove(u, i)
            row = self.ratings.setdefault(u, {})
        for j, w in row.items():  # @line L2
            self.diff[(i, j)] = self.diff.get((i, j), 0.0) + (v - w)  # @line L3
            self.diff[(j, i)] = self.diff.get((j, i), 0.0) + (w - v)
            self.count[(i, j)] = self.count.get((i, j), 0) + 1  # @line L4
            self.count[(j, i)] = self.count.get((j, i), 0) + 1
        row[i] = float(v)  # @line L5
        self.total += v
        self.n += 1

    def remove(self, u, i):
        """Remove the rating of user u for item i."""
        row = self.ratings[u]
        v = row.pop(i)
        for j, w in row.items():
            for key, d in (((i, j), v - w), ((j, i), w - v)):
                c = self.count[key] - 1
                if c == 0:
                    del self.count[key]
                    del self.diff[key]
                else:
                    self.count[key] = c
                    self.diff[key] -= d
        if not row:
            del self.ratings[u]
        self.total -= v
        self.n -= 1

    def dev(self, j, i):
        """The average of r_uj - r_ui over the users who rated both."""
        return self.diff[(j, i)] / self.count[(j, i)]

    def _fallback(self, u):
        row = self.ratings.get(u)
        if row:
            return sum(row.values()) / len(row)
        if self.n == 0:
            raise ValueError("no ratings")
        return self.total / self.n

    def predict(self, u, j, weighted=False):
        row = self.ratings.get(u, {})
        num = den = 0.0
        for i, r in row.items():
            if i == j:  # @line L6
                continue
            c = self.count.get((j, i), 0)
            if c == 0:
                continue
            w = c if weighted else 1  # @line L8
            num += (self.dev(j, i) + r) * w
            den += w
        if den == 0:  # @line L7
            return self._fallback(u)
        return num / den  # @line L9


def fit(train):
    """A SlopeOne model with all ratings of the dict train added."""
    model = SlopeOne()
    for (u, i), v in sorted(train.items()):
        model.add(u, i, v)
    return model
