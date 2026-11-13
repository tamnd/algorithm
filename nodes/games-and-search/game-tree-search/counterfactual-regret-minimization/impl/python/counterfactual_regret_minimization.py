# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counterfactual-regret-minimization/. The authors are listed in prov/XFPEGD.jsonl.

"""Counterfactual regret minimization (vanilla CFR, Zinkevich et al. 2007) for two-player zero-sum
extensive games, with an exact best response and the exploitability of a strategy profile.

A game object has these methods, where a history h is any hashable value:
    root() -> h
    is_terminal(h), is_chance(h) -> bool
    utility(h) -> payoff to player 0 at a terminal h (player 1 gets the negative)
    chance_outcomes(h) -> [(probability, action), ...] at a chance node
    player(h) -> 0 or 1 at a decision node
    infoset(h) -> key of the information set of h (equal keys have equal action lists)
    actions(h) -> list of actions
    child(h, a) -> history after action a
A strategy is a dict that maps an information set key to a list of probabilities, one per action.
"""

from fractions import Fraction
from itertools import product


class KuhnPoker:
    """Kuhn's poker with cards 1 < 2 < 3 (J, Q, K), an ante of 1 and bets of 1.

    A history is (deal, moves) with deal = (card of player 0, card of player 1) and moves a
    string over 'p' (check or fold) and 'b' (bet or call). The root (None, '') is the deal.
    """

    TERMINAL = ("pp", "pbp", "pbb", "bp", "bb")

    def root(self):
        return (None, "")

    def is_chance(self, h):
        return h[0] is None

    def chance_outcomes(self, h):
        deals = [(a, b) for a in (1, 2, 3) for b in (1, 2, 3) if a != b]
        return [(Fraction(1, 6), d) for d in deals]

    def is_terminal(self, h):
        return h[1] in self.TERMINAL

    def utility(self, h):
        (c0, c1), m = h
        if m == "pbp":
            return -1
        if m == "bp":
            return 1
        stake = 1 if m == "pp" else 2
        return stake if c0 > c1 else -stake

    def player(self, h):
        return len(h[1]) % 2

    def infoset(self, h):
        return (h[0][self.player(h)], h[1])

    def actions(self, h):
        return ["p", "b"]

    def child(self, h, a):
        if h[0] is None:
            return (a, "")
        return (h[0], h[1] + a)


class MatrixGame:
    """A zero-sum matrix game as an extensive game: player 0 picks a row, then player 1 picks a
    column without seeing it, so both of player 1's nodes form one information set."""

    def __init__(self, a):
        self.a = a

    def root(self):
        return ()

    def is_chance(self, h):
        return False

    def is_terminal(self, h):
        return len(h) == 2

    def utility(self, h):
        return self.a[h[0]][h[1]]

    def player(self, h):
        return len(h)

    def infoset(self, h):
        return ("row",) if len(h) == 0 else ("column",)

    def actions(self, h):
        return list(range(len(self.a) if len(h) == 0 else len(self.a[0])))

    def child(self, h, a):
        return h + (a,)


def regret_matching(r: list[float]) -> list[float]:
    """Probabilities proportional to the positive parts of the regrets, or uniform if none is positive."""
    pos = [x if x > 0 else 0.0 for x in r]
    s = sum(pos)
    if s > 0:
        return [x / s for x in pos]
    return [1.0 / len(r)] * len(r)


class CFR:
    """Vanilla CFR with simultaneous updates of both players, as in Zinkevich et al. (2007).

    Cost per iteration: one walk of the whole game tree, O(|H|) time; O(|I| A) memory for the
    regret and strategy tables, where |I| is the number of information sets.
    """

    def __init__(self, game):
        self.game = game
        # Tables start empty: a missing entry means regrets and strategy sums of 0.
        self.regret: dict = {}  # @line L1
        self.strategy_sum: dict = {}
        self.sigma: dict = {}
        self.iterations = 0

    def run(self, t: int) -> dict:
        for _ in range(t):  # @line L2
            self.sigma = {key: regret_matching(r) for key, r in self.regret.items()}  # @line L3
            self._walk(self.game.root(), 1.0, 1.0, 1.0)  # @line L4
            self.iterations += 1
        return self.average_strategy()  # @line L5

    def _walk(self, h, p0: float, p1: float, pc: float) -> float:
        g = self.game
        if g.is_terminal(h):
            return float(g.utility(h))  # @line L6
        if g.is_chance(h):
            return sum(float(q) * self._walk(g.child(h, a), p0, p1, pc * float(q)) for q, a in g.chance_outcomes(h))  # @line L7
        i, key, acts = g.player(h), g.infoset(h), g.actions(h)  # @line L8
        sigma = self.sigma.get(key)
        if sigma is None:
            sigma = [1.0 / len(acts)] * len(acts)
        values = []
        for a, s in zip(acts, sigma):
            if i == 0:
                values.append(self._walk(g.child(h, a), p0 * s, p1, pc))  # @line L9
            else:
                values.append(self._walk(g.child(h, a), p0, p1 * s, pc))
        v = sum(s * x for s, x in zip(sigma, values))  # @line L10
        own, other = (p0, p1) if i == 0 else (p1, p0)
        sign = 1.0 if i == 0 else -1.0
        r = self.regret.setdefault(key, [0.0] * len(acts))
        ssum = self.strategy_sum.setdefault(key, [0.0] * len(acts))
        for k in range(len(acts)):
            r[k] += sign * other * pc * (values[k] - v)  # @line L11
            ssum[k] += own * sigma[k]  # @line L12
        return v  # @line L13

    def average_strategy(self) -> dict:
        """The average of the strategies of all iterations, weighted by the player's own reach (Eq. 4)."""
        out = {}
        for key, s in self.strategy_sum.items():
            total = sum(s)
            out[key] = [x / total for x in s] if total > 0 else [1.0 / len(s)] * len(s)
        return out


def _probs(game, strategy, h):
    acts = game.actions(h)
    p = strategy.get(game.infoset(h))
    return p if p is not None else [Fraction(1, len(acts))] * len(acts)


def expected_value(game, strategy, h=None):
    """Expected payoff to player 0 when both players follow strategy. Exact if the input is exact."""
    h = game.root() if h is None else h
    if game.is_terminal(h):
        return game.utility(h)
    if game.is_chance(h):
        return sum(q * expected_value(game, strategy, game.child(h, a)) for q, a in game.chance_outcomes(h))
    return sum(p * expected_value(game, strategy, game.child(h, a)) for p, a in zip(_probs(game, strategy, h), game.actions(h)) if p)


def best_response_value(game, strategy, player: int):
    """Payoff to player 0 when `player` plays a best response to the other player's part of strategy.

    Player 0 maximizes and player 1 minimizes. The best response picks, at each information set of
    `player`, the action with the best sum over the histories of the set of (reach of the others)
    times (value below, with `player` playing the best response deeper down). Perfect recall makes
    this well defined. Cost O(|H|) evaluations per information set.
    """
    members: dict = {}

    def collect(h, reach):
        if game.is_terminal(h):
            return
        if game.is_chance(h):
            for q, a in game.chance_outcomes(h):
                collect(game.child(h, a), reach * q)
            return
        if game.player(h) == player:
            members.setdefault(game.infoset(h), []).append((h, reach))
            for a in game.actions(h):
                collect(game.child(h, a), reach)
        else:
            for p, a in zip(_probs(game, strategy, h), game.actions(h)):
                collect(game.child(h, a), reach * p)

    collect(game.root(), 1)
    choice: dict = {}

    def value(h):
        if game.is_terminal(h):
            return game.utility(h)
        if game.is_chance(h):
            return sum(q * value(game.child(h, a)) for q, a in game.chance_outcomes(h))
        if game.player(h) == player:
            return value(game.child(h, decide(game.infoset(h))))
        return sum(p * value(game.child(h, a)) for p, a in zip(_probs(game, strategy, h), game.actions(h)) if p)

    def decide(key):
        if key not in choice:
            hs = members[key]
            acts = game.actions(hs[0][0])
            scores = [sum(r * value(game.child(h, a)) for h, r in hs if r) for a in acts]
            best = max(scores) if player == 0 else min(scores)
            choice[key] = acts[scores.index(best)]
        return choice[key]

    return value(game.root())


def exploitability(game, strategy):
    """max over player 0 deviations minus min over player 1 deviations, in player 0 payoff.

    It is >= 0, and it is 0 exactly when the profile is a Nash equilibrium.
    """
    return best_response_value(game, strategy, 0) - best_response_value(game, strategy, 1)


def pure_strategies(game, player: int):
    """All pure strategies of `player`, as strategy dicts (used by tests as a brute force)."""
    sets: dict = {}

    def collect(h):
        if game.is_terminal(h):
            return
        if game.is_chance(h):
            for _, a in game.chance_outcomes(h):
                collect(game.child(h, a))
            return
        if game.player(h) == player:
            sets[game.infoset(h)] = len(game.actions(h))
        for a in game.actions(h):
            collect(game.child(h, a))

    collect(game.root())
    keys = sorted(sets)
    for pick in product(*[range(sets[k]) for k in keys]):
        yield {k: [1 if j == c else 0 for j in range(sets[k])] for k, c in zip(keys, pick)}


def kuhn_equilibrium(alpha: Fraction) -> dict:
    """Kuhn's equilibrium family. Player 0 bets J with probability alpha (0 <= alpha <= 1/3), bets K
    with 3 alpha, and calls a bet with Q with alpha + 1/3. Player 1 bets after a check with K always
    and with J with 1/3, and calls a bet with K always and with Q with 1/3."""
    alpha = Fraction(alpha)
    if not 0 <= alpha <= Fraction(1, 3):
        raise ValueError("alpha must be in [0, 1/3]")
    third = Fraction(1, 3)

    def bet(p):
        return [1 - p, p]

    return {
        (1, ""): bet(alpha), (2, ""): bet(Fraction(0)), (3, ""): bet(3 * alpha),
        (1, "pb"): bet(Fraction(0)), (2, "pb"): bet(alpha + third), (3, "pb"): bet(Fraction(1)),
        (1, "p"): bet(third), (2, "p"): bet(Fraction(0)), (3, "p"): bet(Fraction(1)),
        (1, "b"): bet(Fraction(0)), (2, "b"): bet(third), (3, "b"): bet(Fraction(1)),
    }
