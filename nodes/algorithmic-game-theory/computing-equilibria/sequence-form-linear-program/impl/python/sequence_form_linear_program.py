# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequence-form-linear-program/. The authors are listed in prov/7V6BC9.jsonl.
"""The sequence-form linear program for two-player zero-sum games in extensive form, in Fraction.

A game tree is made of tuples:
  ("leaf", u)                          u is the payoff to player 1; player 2 gets -u
  ("chance", [(p, child), ...])        the probabilities p sum to 1
  ("move", player, h, [(a, child), ...])  player is 1 or 2, h names the information set
All nodes with the same h must belong to the same player and have the same list of actions.
Perfect recall is checked: all nodes of an information set must have the same sequence of
own (information set, action) pairs above them.

A sequence of a player is () or a tuple of (h, a) pairs. A realization plan x gives each
sequence the probability that the player's own moves follow it; it satisfies x[()] = 1 and
x[s] = sum of x[s + ((h, a),)] over the actions a of each information set h with parent s.
"""

from fractions import Fraction

from agtlp import lp_max


class SequenceForm:
    """The sequences, information sets and sequence payoff matrix of a game tree."""

    def __init__(self, tree):
        self.seqs = [[()], [()]]          # seqs[p][k]: sequence number k of player p + 1
        self.index = [{(): 0}, {(): 0}]
        self.infosets = [{}, {}]          # h -> (parent sequence, list of actions)
        self.payoff = {}                  # (k1, k2) -> expected payoff to player 1
        self._walk(tree, Fraction(1), [(), ()])  # @line L1
        self.E = self._constraints(0)
        self.F = self._constraints(1)  # @line L3

    def _walk(self, node, prob, seq):
        kind = node[0]
        if kind == "leaf":
            key = (self.index[0][seq[0]], self.index[1][seq[1]])
            self.payoff[key] = self.payoff.get(key, Fraction(0)) + prob * Fraction(node[1])  # @line L2
        elif kind == "chance":
            for p, child in node[1]:
                self._walk(child, prob * Fraction(p), seq)
        elif kind == "move":
            _, player, h, moves = node
            p = player - 1
            if h in self.infosets[1 - p]:
                raise ValueError("information set %r belongs to both players" % (h,))
            actions = [a for a, _ in moves]
            known = self.infosets[p].setdefault(h, (seq[p], actions))
            if known[0] != seq[p]:
                raise ValueError("no perfect recall at information set %r" % (h,))
            if known[1] != actions:
                raise ValueError("information set %r has different actions" % (h,))
            for a, child in moves:
                s = seq[p] + ((h, a),)
                if s not in self.index[p]:
                    self.index[p][s] = len(self.seqs[p])
                    self.seqs[p].append(s)
                nxt = list(seq)
                nxt[p] = s
                self._walk(child, prob, nxt)
        else:
            raise ValueError("unknown node kind %r" % (kind,))

    def _constraints(self, p):
        """Rows of E x = e: x[()] = 1, then x[parent(h)] - sum_a x[parent(h) + (h, a)] = 0."""
        n = len(self.seqs[p])
        rows = [[Fraction(int(k == 0)) for k in range(n)]]
        for h, (parent, actions) in self.infosets[p].items():
            row = [Fraction(0)] * n
            row[self.index[p][parent]] = Fraction(1)
            for a in actions:
                row[self.index[p][parent + ((h, a),)]] = Fraction(-1)
            rows.append(row)
        return rows

    def matrix(self):
        """The sequence payoff matrix A, with A[k1][k2] the payoff to player 1."""
        A = [[Fraction(0)] * len(self.seqs[1]) for _ in self.seqs[0]]
        for (i, j), v in self.payoff.items():
            A[i][j] = v
        return A


def solve(tree):
    """Return (value, x, y): the value for player 1 and optimal realization plans as dicts.

    The LP has variables q (free, one per row of F) and x >= 0:
        maximize q[0]  subject to  F^T q - A^T x <= 0,  E x = e.
    The constraint of player 2's sequence j says that j costs player 1 at least the
    payoff that the subtree of j can guarantee; the duals of these rows are an optimal y.
    """
    sf = SequenceForm(tree)
    A = sf.matrix()
    E, F = sf.E, sf.F
    n1, n2, r2 = len(sf.seqs[0]), len(sf.seqs[1]), len(F)
    # Columns: q+ (r2), q- (r2), x (n1).
    c = [Fraction(int(k == 0)) for k in range(r2)] + [-Fraction(int(k == 0)) for k in range(r2)] + [Fraction(0)] * n1
    A_ub = [[F[k][j] for k in range(r2)] + [-F[k][j] for k in range(r2)] + [-A[i][j] for i in range(n1)]
            for j in range(n2)]  # @line L4
    A_eq = [[Fraction(0)] * (2 * r2) + E[k] for k in range(len(E))]
    status, sol, value, dual = lp_max(c, A_ub, [0] * n2, A_eq, [1] + [0] * (len(E) - 1))  # @line L5
    if status != "optimal":
        raise AssertionError("the sequence-form LP of a finite game always has an optimum")
    x = {s: sol[2 * r2 + k] for k, s in enumerate(sf.seqs[0])}
    y = {s: dual[j] for j, s in enumerate(sf.seqs[1])}  # @line L6
    return value, x, y


def behavior(sf, p, plan):
    """Turn a realization plan of player p + 1 into a behavior strategy: h -> {a: probability}.

    At an information set that the plan reaches with probability 0 the actions are uniform.
    """
    out = {}
    for h, (parent, actions) in sf.infosets[p].items():
        total = plan[parent]
        if total == 0:
            out[h] = {a: Fraction(1, len(actions)) for a in actions}
        else:
            out[h] = {a: plan[parent + ((h, a),)] / total for a in actions}
    return out
