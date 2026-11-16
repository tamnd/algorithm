# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-based-bundle-algorithm/. The authors are listed in prov/FENCPV.jsonl.

"""Consensus-based bundle algorithm (CBBA) of Choi, Brunet and How (2009).

Agents are 0..u-1 and tasks are 0..t-1. Each agent i keeps
  b[i]  its bundle, the tasks it has claimed, in the order it added them,
  y[i]  its list of winning bids, y[i][j] is the best bid on task j it knows,
  z[i]  its list of winners, z[i][j] is the agent it believes wins task j (or None),
  s[i]  its timestamps, s[i][k] is the round of the latest information from agent k.

The score is the one used for diminishing marginal gain (DMG) in this file:
agent i that already holds n tasks gains a[i][j] * gamma**n from task j, with
0 < gamma <= 1, and holds at most cap tasks. The marginal gain never grows when
the bundle grows, which is the DMG condition that the convergence proof needs.

The network is a fixed undirected graph, and time is synchronous: in each round
every agent runs the bundle phase, sends (y, z, s) to its neighbors, and then
runs the consensus phase on the messages of that round.
"""

from typing import Optional, Sequence

UPDATE, RESET, LEAVE = "update", "reset", "leave"


def beats(y1: float, z1: Optional[int], y2: float, z2: Optional[int]) -> bool:
    """True if bid y1 of agent z1 is better than bid y2 of agent z2.

    Equal bids go to the agent with the smaller index; any bid beats no bid.
    """
    if z1 is None:
        return False
    if z2 is None:
        return y1 > 0 or y2 <= 0
    return y1 > y2 or (y1 == y2 and z1 < z2)


def decide(i, k, yk, zk, sk, yi, zi, si) -> str:
    """The action rule of CBBA for one task, when agent i receives from agent k.

    yk, zk are the winning bid and winner that sender k reports, and sk its
    timestamps; yi, zi, si are the values of receiver i. This is the decision
    table of Choi, Brunet and How (2009) for the sender's view (k, i, another
    agent m, or nobody) against the receiver's view.
    """
    if zk == k:
        if zi == i:
            return UPDATE if beats(yk, k, yi, i) else LEAVE
        if zi == k or zi is None:
            return UPDATE
        m = zi
        if sk[m] > si[m] or beats(yk, k, yi, m):
            return UPDATE
        return LEAVE
    if zk == i:
        if zi == i or zi is None:
            return LEAVE
        if zi == k:
            return RESET
        m = zi
        return RESET if sk[m] > si[m] else LEAVE
    if zk is None:
        if zi == i or zi is None:
            return LEAVE
        if zi == k:
            return UPDATE
        m = zi
        return UPDATE if sk[m] > si[m] else LEAVE
    m = zk  # the sender thinks a third agent m wins
    if zi == i:
        return UPDATE if sk[m] > si[m] and beats(yk, m, yi, i) else LEAVE
    if zi == k:
        return UPDATE if sk[m] > si[m] else RESET
    if zi == m or zi is None:
        return UPDATE if sk[m] > si[m] else LEAVE
    n = zi  # the receiver thinks a fourth agent n wins
    if sk[m] > si[m] and sk[n] > si[n]:
        return UPDATE
    if sk[m] > si[m] and beats(yk, m, yi, n):
        return UPDATE
    if sk[n] > si[n] and si[m] > sk[m]:
        return RESET
    return LEAVE


def bundle_phase(i, b, y, z, a, gamma, cap) -> None:
    """Agent i adds tasks greedily while it can outbid the winner it knows."""
    while len(b) < cap:  # @line L4
        best = None
        for j in range(len(a[i])):
            if j in b:
                continue
            c = a[i][j] * gamma ** len(b)  # @line L5
            if beats(c, i, y[j], z[j]):  # @line L6
                if best is None or c > best[0]:
                    best = (c, j)
        if best is None:  # @line L7
            break
        c, j = best
        b.append(j)  # @line L8
        y[j] = c
        z[j] = i


def cbba(
    a: Sequence[Sequence[float]],
    neighbors: Sequence[Sequence[int]],
    gamma: float = 1.0,
    cap: Optional[int] = None,
    max_rounds: int = 10000,
) -> dict:
    """Run CBBA on scores a[i][j] > 0 over the graph given by neighbor lists.

    Returns the final bundles, winners and winning bids of every agent, and the
    number of rounds until the last change.
    """
    u = len(a)
    t = len(a[0]) if u else 0
    cap = t if cap is None else cap
    b = [[] for _ in range(u)]  # @line L1
    y = [[0] * t for _ in range(u)]
    z = [[None] * t for _ in range(u)]
    s = [[0] * u for _ in range(u)]
    last_change = 0
    for rnd in range(1, max_rounds + 1):  # @line L2
        before = ([list(v) for v in b], [list(v) for v in y], [list(v) for v in z])
        for i in range(u):  # @line L3
            bundle_phase(i, b[i], y[i], z[i], a, gamma, cap)
        sent = [(list(y[k]), list(z[k]), list(s[k])) for k in range(u)]  # @line L9
        for i in range(u):
            si = list(s[i])
            for k in sorted(neighbors[i]):  # @line L10
                yk, zk, sk = sent[k]
                for j in range(t):
                    act = decide(i, k, yk[j], zk[j], sk, y[i][j], z[i][j], si)  # @line L11
                    if act == UPDATE:
                        y[i][j], z[i][j] = yk[j], zk[j]
                    elif act == RESET:
                        y[i][j], z[i][j] = 0, None
        for i in range(u):  # @line L12
            new = list(s[i])
            for k in neighbors[i]:
                new[k] = rnd
                for m in range(u):
                    if m != i and m not in neighbors[i]:
                        new[m] = max(new[m], sent[k][2][m])
            new[i] = rnd
            s[i] = new
        for i in range(u):  # @line L13
            lost = [n for n, j in enumerate(b[i]) if z[i][j] != i]
            if lost:
                first = lost[0]
                for j in b[i][first + 1:]:
                    # The bid on j assumed the lost task, so it is withdrawn.
                    # Information that another agent wins j is kept.
                    if z[i][j] == i:
                        y[i][j], z[i][j] = 0, None
                del b[i][first:]
        after = (b, y, z)
        if before != after:
            last_change = rnd
        elif rnd - last_change > u:  # @line L14
            break
    return {"bundles": b, "winners": z, "bids": y, "rounds": last_change}  # @line L15


def sequential_greedy(a, gamma=1.0, cap=None) -> dict:
    """The sequential greedy algorithm (SGA): take the best agent-task pair, repeat."""
    u = len(a)
    t = len(a[0]) if u else 0
    cap = t if cap is None else cap
    bundles = [[] for _ in range(u)]
    winner = [None] * t
    while True:
        best = None
        for i in range(u):
            if len(bundles[i]) >= cap:
                continue
            for j in range(t):
                if winner[j] is None:
                    c = a[i][j] * gamma ** len(bundles[i])
                    if best is None or c > best[0]:
                        best = (c, i, j)
        if best is None:
            break
        c, i, j = best
        bundles[i].append(j)
        winner[j] = i
    return {"bundles": bundles, "winners": winner}


def assignment_value(a, bundles, gamma=1.0) -> float:
    """Team score of the bundles, with each bundle in its best order."""
    total = 0
    for i, bundle in enumerate(bundles):
        vals = sorted((a[i][j] for j in bundle), reverse=True)
        total += sum(v * gamma ** n for n, v in enumerate(vals))
    return total
