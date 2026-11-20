# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-response-dynamics/. The authors are listed in prov/0D2G4K.jsonl.
"""Best-response dynamics on a finite game in normal form, with cycle detection.

The game is a pair (sizes, pay) as in the shared helper agtgame: sizes[i] is the number of
pure strategies of player i, and pay maps each pure profile to a tuple of utilities, which
the players maximize. A cost game passes the utilities u = -c.

At each step, the smallest player who is not playing a best response to the others switches
to its smallest best response. The next profile depends only on the current one, so the run
either reaches a pure Nash equilibrium or repeats a profile, and then it cycles for ever.
"""


def _replace(s, i, a):
    return s[:i] + (a,) + s[i + 1:]


def best_responses(game, s, i):
    """Return the sorted list of the pure best responses of player i to s_-i.

    Cost: sizes[i] payoff lookups.
    """
    sizes, pay = game
    vals = [pay[_replace(s, i, b)][i] for b in range(sizes[i])]
    best = max(vals)
    return [b for b, v in enumerate(vals) if v == best]


def best_response_dynamics(game, start):
    """Run best-response dynamics from the pure profile start.

    Return (s, status, path). status is "equilibrium" when s is a pure Nash equilibrium, and
    "cycle" when s is a profile that the run has visited before. path is the list of the
    profiles visited, start first and s last.

    Precondition: start is a pure profile of the game. Cost: at most |S| steps, where |S| is
    the number of profiles, and O(n k) payoff lookups per step, where n is the number of
    players and k the largest number of strategies; the seen set holds at most |S| profiles.
    """
    sizes, _ = game
    s = tuple(start)
    if len(s) != len(sizes) or any(not 0 <= a < k for a, k in zip(s, sizes)):
        raise ValueError("start must be a pure profile of the game")
    seen = set()  # @line L1
    path = [s]
    while True:  # @line L2
        unhappy = [i for i in range(len(sizes)) if s[i] not in best_responses(game, s, i)]  # @line L3
        if not unhappy:  # @line L4
            return s, "equilibrium", path
        if s in seen:  # @line L5
            return s, "cycle", path
        seen.add(s)  # @line L6
        i = unhappy[0]  # @line L7
        s = _replace(s, i, best_responses(game, s, i)[0])  # @line L8
        path.append(s)
