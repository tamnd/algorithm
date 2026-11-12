# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-decision-process/. The authors are listed in prov/W1VDJ0.jsonl.
"""A finite Markov decision process (S, A, P, R, gamma) with exact policy evaluation.

States are 0 .. n-1 and actions are 0 .. m-1 in every state. P[s][a][t] is the
probability of the move from s to t under action a, and R[s][a] is the expected
reward of action a in state s. Use fractions.Fraction entries for exact answers.
A Markov stationary policy is a list pi with pi[s][a] the probability of action a
in state s. A deterministic stationary policy is a tuple d with d[s] an action.
"""

from fractions import Fraction
from itertools import product
from typing import Iterator, List, Sequence, Tuple

Number = Fraction


def solve_linear(a: List[List[Number]], b: List[Number]) -> List[Number]:
    """Solve a x = b by Gaussian elimination with row pivoting. Cost O(n^3)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


class MDP:
    """A finite MDP with the discounted criterion, 0 <= gamma < 1."""

    def __init__(self, P, R, gamma) -> None:
        self.P, self.R, self.gamma = P, R, gamma
        self.n, self.m = len(P), len(P[0])
        if not 0 <= gamma < 1:
            raise ValueError("need 0 <= gamma < 1")
        for s in range(self.n):
            if len(P[s]) != self.m or len(R[s]) != self.m:
                raise ValueError("every state needs the same number of actions")
            for a in range(self.m):
                row = P[s][a]
                if len(row) != self.n or min(row) < 0 or sum(row) != 1:
                    raise ValueError("P[s][a] must be a probability vector")

    def policy_matrices(self, pi) -> Tuple[List[List[Number]], List[Number]]:
        """Return P^pi and R^pi of a Markov stationary policy. Cost O(n^2 m)."""
        n, m = self.n, self.m
        p_pi = [[sum(pi[s][a] * self.P[s][a][t] for a in range(m)) for t in range(n)] for s in range(n)]
        r_pi = [sum(pi[s][a] * self.R[s][a] for a in range(m)) for s in range(n)]
        return p_pi, r_pi

    def evaluate(self, pi) -> List[Number]:
        """Return V^pi = (I - gamma P^pi)^(-1) R^pi by one linear solve. Cost O(n^3)."""
        p_pi, r_pi = self.policy_matrices(pi)
        n, g = self.n, self.gamma
        a = [[(1 if s == t else 0) - g * p_pi[s][t] for t in range(n)] for s in range(n)]
        return solve_linear(a, r_pi)

    def as_stochastic(self, d: Sequence[int]):
        """Write a deterministic policy as a table of probabilities."""
        return [[Fraction(1 if a == d[s] else 0) for a in range(self.m)] for s in range(self.n)]

    def deterministic_policies(self) -> Iterator[Tuple[int, ...]]:
        """All m^n deterministic stationary policies."""
        return product(range(self.m), repeat=self.n)

    def best_deterministic(self) -> Tuple[Tuple[int, ...], List[Number]]:
        """Enumerate the m^n deterministic stationary policies and return one
        whose value is at least the value of every other one in every state.
        Raise if no such policy exists. Cost O(m^n n^3)."""
        values = {d: self.evaluate(self.as_stochastic(d)) for d in self.deterministic_policies()}
        upper = [max(v[s] for v in values.values()) for s in range(self.n)]
        for d, v in values.items():
            if v == upper:
                return d, v
        raise AssertionError("no deterministic policy is best in every state")

    def finite_horizon(self, horizon: int) -> Tuple[List[Number], List[Tuple[int, ...]]]:
        """Backward induction for the undiscounted total reward over `horizon` steps.
        Return the optimal values and the decision rules d_0 .. d_(horizon-1).
        Cost O(horizon n^2 m)."""
        v = [Fraction(0)] * self.n
        rules: List[Tuple[int, ...]] = []
        for _ in range(horizon):
            q = [[self.R[s][a] + sum(self.P[s][a][t] * v[t] for t in range(self.n)) for a in range(self.m)] for s in range(self.n)]
            d = tuple(max(range(self.m), key=lambda a, s=s: q[s][a]) for s in range(self.n))
            v = [q[s][d[s]] for s in range(self.n)]
            rules.append(d)
        rules.reverse()
        return v, rules


def random_mdp(n: int, m: int, gamma: Fraction, rng, scale: int = 6) -> MDP:
    """A random MDP with rational probabilities and integer rewards in [-scale, scale]."""
    P, R = [], []
    for _ in range(n):
        ps, rs = [], []
        for _ in range(m):
            w = [rng.randint(0, 4) for _ in range(n)]
            if sum(w) == 0:
                w[rng.randrange(n)] = 1
            ps.append([Fraction(x, sum(w)) for x in w])
            rs.append(Fraction(rng.randint(-scale, scale)))
        P.append(ps)
        R.append(rs)
    return MDP(P, R, gamma)


def example_mdp() -> MDP:
    """The two-state example of the page, gamma = 9/10."""
    F = Fraction
    P = [[[F(1), F(0)], [F(1, 2), F(1, 2)]],
         [[F(1, 4), F(3, 4)], [F(1), F(0)]]]
    R = [[F(1), F(0)], [F(2), F(3)]]
    return MDP(P, R, F(9, 10))
