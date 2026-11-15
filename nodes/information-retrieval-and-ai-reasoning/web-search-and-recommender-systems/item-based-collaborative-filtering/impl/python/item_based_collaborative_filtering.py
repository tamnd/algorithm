# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/item-based-collaborative-filtering/. The authors are listed in prov/Z4THKH.jsonl.

"""Item-based collaborative filtering with adjusted cosine similarity.

The similarity of items i and j is the cosine of the two columns after
each rating has its user's mean subtracted, with all three sums over the
users who rated both items (Sarwar et al. 2001, adjusted cosine). The
model keeps, for each item, the k items with the largest positive
similarity (all of them when k is None). The prediction for user u and
item i is the weighted mean

    sum_j s(i, j) r_uj / sum_j s(i, j)

over the items j of the model of i that u rated. Only positive
similarities enter, so the prediction lies between the smallest and the
largest of the ratings it uses. With no such item the prediction is the
mean of user u.
"""

import math


def adjusted_cosine(ci, cj):
    """Adjusted cosine of two items.

    ci and cj map users to centered ratings r_ui - mu_u. The value is 0
    when the items share no user or a centered vector on the shared
    users is zero.
    """
    num = si = sj = 0.0
    for u, a in ci.items():
        if u in cj:  # @line L4
            b = cj[u]
            num += a * b
            si += a * a
            sj += b * b
    if si == 0.0 or sj == 0.0:
        return 0.0
    return num / math.sqrt(si * sj)  # @line L5


class ItemBasedCF:
    """Model-based form: the item neighbor lists are built once."""

    def __init__(self, train, k=None):
        self.k = k
        self.by_user = {}
        for (u, i), v in train.items():
            self.by_user.setdefault(u, {})[i] = v
        self.means = {u: sum(r.values()) / len(r) for u, r in self.by_user.items()}  # @line L1
        self.global_mean = sum(train.values()) / len(train)
        centered = {}
        for (u, i), v in train.items():
            centered.setdefault(i, {})[u] = v - self.means[u]  # @line L2
        items = sorted(centered)
        sim = {}
        for a in range(len(items)):  # @line L3
            for b in range(a + 1, len(items)):
                i, j = items[a], items[b]
                s = adjusted_cosine(centered[i], centered[j])
                sim[(i, j)] = sim[(j, i)] = s
        self.sim = sim
        self.model = {}
        for i in items:  # @line L6
            cand = [(sim[(i, j)], j) for j in items if j != i and sim[(i, j)] > 0.0]  # @line L7
            cand.sort(key=lambda t: (-t[0], t[1]))
            if k is not None:
                cand = cand[:k]
            self.model[i] = cand

    def similarity(self, i, j):
        return self.sim.get((i, j), 0.0)

    def predict(self, u, i):
        if u not in self.by_user:  # @line L8
            return self.global_mean
        row = self.by_user[u]
        num = den = 0.0
        for s, j in self.model.get(i, []):
            if j in row:  # @line L9
                num += s * row[j]
                den += s
        if den == 0.0:  # @line L10
            return self.means[u]
        return num / den  # @line L11
