# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/user-based-collaborative-filtering/. The authors are listed in prov/SEEFZS.jsonl.

"""User-based collaborative filtering with Pearson weights.

The weight of two users is the Pearson correlation of their ratings on
the items that both rated, with each user's mean taken over all of that
user's ratings. The prediction for user u and item i is

    mu_u + sum_v w(u, v) (r_vi - mu_v) / sum_v |w(u, v)|

over the users v != u who rated i (or the k of them with the largest
weight). If the sum of the absolute weights is zero, the prediction is
mu_u.
"""

import math


def user_means(by_user):
    """The mean rating of each user."""
    return {u: sum(row.values()) / len(row) for u, row in by_user.items()}


def pearson(ru, rv, mu, mv):
    """Pearson weight of two users on their co-rated items.

    ru and rv map items to ratings; mu and mv are the users' means.
    The weight is 0 when the users share no item or when one of the
    centered vectors on the shared items is zero.
    """
    common = [i for i in ru if i in rv]  # @line L9
    num = su = sv = 0.0
    for i in common:
        a = ru[i] - mu  # @line L10
        b = rv[i] - mv
        num += a * b
        su += a * a
        sv += b * b
    if su == 0.0 or sv == 0.0:  # @line L11
        return 0.0
    return num / math.sqrt(su * sv)  # @line L12


class UserBasedCF:
    """Memory-based predictor. k=None uses all users who rated the item."""

    def __init__(self, train, k=None):
        self.k = k
        self.by_user = {}
        self.by_item = {}
        for (u, i), v in train.items():
            self.by_user.setdefault(u, {})[i] = v
            self.by_item.setdefault(i, {})[u] = v
        self.means = user_means(self.by_user)
        self.global_mean = sum(train.values()) / len(train)
        self._w = {}

    def weight(self, u, v):
        key = (u, v) if u <= v else (v, u)
        if key not in self._w:
            self._w[key] = pearson(
                self.by_user[u], self.by_user[v], self.means[u], self.means[v]
            )
        return self._w[key]

    def neighbors(self, u, i):
        """The list of (weight, v) used to predict r_ui."""
        raters = self.by_item.get(i, {})  # @line L2
        nb = [(self.weight(u, v), v) for v in raters if v != u]  # @line L3
        if self.k is not None:  # @line L4
            nb.sort(key=lambda t: (-t[0], t[1]))  # @line L5
            nb = nb[: self.k]
        return nb

    def predict(self, u, i):
        if u not in self.by_user:  # @line L1
            return self.global_mean
        mu = self.means[u]
        num = den = 0.0
        for w, v in self.neighbors(u, i):
            num += w * (self.by_item[i][v] - self.means[v])
            den += abs(w)  # @line L6
        if den == 0.0:  # @line L7
            return mu
        return mu + num / den  # @line L8
