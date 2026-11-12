# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pomdp/. The authors are listed in prov/F8X6BC.jsonl.
"""A finite POMDP (S, A, P, R, Omega, O, gamma): the belief update, the value of
a belief by the finite horizon recursion, and exact alpha vectors by
enumeration (Monahan 1982, with no pruning).

P[s][a][t] = Pr(next state t | state s, action a)
O[a][t][o] = Pr(observation o | action a, next state t)
R[s][a]    = expected reward
Beliefs are lists of probabilities over S. Use Fractions for exact values.
"""

from itertools import product
from typing import List, Tuple


class POMDP:
    def __init__(self, P, R, O, gamma):
        self.P, self.R, self.O, self.gamma = P, R, O, gamma
        self.n, self.m, self.k = len(P), len(P[0]), len(O[0][0])
        for s in range(self.n):
            for a in range(self.m):
                if sum(P[s][a]) != 1:
                    raise ValueError("each row of P must sum to 1")
        for a in range(self.m):
            for t in range(self.n):
                if sum(O[a][t]) != 1:
                    raise ValueError("each row of O must sum to 1")

    def predict(self, b, a) -> List:
        """Pr(S' = t | b, a) = sum_s b(s) P(t | s, a)."""
        return [sum(b[s] * self.P[s][a][t] for s in range(self.n)) for t in range(self.n)]

    def obs_prob(self, b, a, o):
        """Pr(o | b, a) = sum_t O(o | a, t) sum_s P(t | s, a) b(s)."""
        return sum(self.O[a][t][o] * x for t, x in enumerate(self.predict(b, a)))

    def belief_update(self, b, a, o) -> Tuple[List, object]:
        """Bayes rule: b'(t) is proportional to O(o | a, t) sum_s P(t | s, a) b(s).
        Returns (b', Pr(o | b, a)). Cost O(n^2)."""
        pred = self.predict(b, a)
        w = [self.O[a][t][o] * pred[t] for t in range(self.n)]
        z = sum(w)
        if z == 0:
            raise ValueError("observation has probability 0 under this belief")
        return [x / z for x in w], z

    def expected_reward(self, b, a):
        return sum(b[s] * self.R[s][a] for s in range(self.n))

    def value(self, b, horizon: int):
        """V_H(b) = max_a [ rho(b, a) + gamma sum_o Pr(o | b, a) V_(H-1)(b') ], V_0 = 0.
        Cost O((m k)^H n^2): it expands the full tree of actions and observations."""
        if horizon == 0:
            return 0 * self.R[0][0]
        best = None
        for a in range(self.m):
            total = self.expected_reward(b, a)
            for o in range(self.k):
                z = self.obs_prob(b, a, o)
                if z == 0:
                    continue
                b2, _ = self.belief_update(b, a, o)
                total += self.gamma * z * self.value(b2, horizon - 1)
            best = total if best is None or total > best else best
        return best

    def alpha_vectors(self, horizon: int) -> List[Tuple[int, List]]:
        """Exact alpha vectors for V_H by enumeration, with the first action of each.
        Gamma_t has m |Gamma_(t-1)|^k members, since nothing is pruned."""
        gam = [(None, [0 * self.R[0][0]] * self.n)]
        for _ in range(horizon):
            new = []
            for a in range(self.m):
                # g[o][i](s) = sum_t P(t | s, a) O(o | a, t) alpha_i(t)
                g = [[[sum(self.P[s][a][t] * self.O[a][t][o] * alpha[t] for t in range(self.n))
                       for s in range(self.n)] for _, alpha in gam] for o in range(self.k)]
                for choice in product(range(len(gam)), repeat=self.k):
                    vec = [self.R[s][a] + self.gamma * sum(g[o][choice[o]][s] for o in range(self.k))
                           for s in range(self.n)]
                    new.append((a, vec))
            gam = new
        return gam

    @staticmethod
    def value_from_alphas(alphas, b):
        """V(b) = max over alpha of the dot product alpha . b; the max is piecewise linear and convex."""
        return max(sum(x * y for x, y in zip(vec, b)) for _, vec in alphas)


def tiger(gamma=1, accuracy=None):
    """The tiger problem of Kaelbling, Littman and Cassandra (1998).
    States: 0 tiger left, 1 tiger right. Actions: 0 listen, 1 open left, 2 open right.
    Observations: 0 hear left, 1 hear right. Opening a door resets the tiger at random."""
    from fractions import Fraction as F
    acc = F(17, 20) if accuracy is None else accuracy
    half = [F(1, 2), F(1, 2)]
    P = [[[F(1), F(0)], half, half], [[F(0), F(1)], half, half]]
    R = [[F(-1), F(-100), F(10)], [F(-1), F(10), F(-100)]]
    O = [[[acc, 1 - acc], [1 - acc, acc]], [half, half], [half, half]]
    return POMDP(P, R, O, gamma)
