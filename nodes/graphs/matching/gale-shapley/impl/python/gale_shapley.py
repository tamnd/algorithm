# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gale-shapley/. The authors are listed in prov/9YR7J5.jsonl.

from typing import Callable, NamedTuple, Optional


class StableMatching(NamedTuple):
    partner_of_proposer: list[int]  # receiver held by each proposer at the end, or -1
    partner_of_receiver: list[int]  # proposer held by each receiver at the end, or -1
    proposals: int  # number of proposals made


def gale_shapley(
    proposer_prefs: list[list[int]],
    receiver_prefs: list[list[int]],
    on_proposal: Optional[Callable[[int, int, str], None]] = None,
) -> StableMatching:
    """Proposer-optimal stable matching by deferred acceptance.

    proposer_prefs[p] lists the receivers acceptable to proposer p, best first;
    receiver_prefs[r] lists the proposers acceptable to receiver r, best first.
    Lists may be incomplete and of any length, but must not repeat an entry.
    A pair is acceptable when each side lists the other. The optional callback
    gets (p, r, outcome) for each proposal, where outcome is "accepted",
    "rejected", "unacceptable" or "replaces q" for the displaced proposer q.
    O(n + m) time and space, for n agents and m entries in all lists.
    """
    n_p, n_r = len(proposer_prefs), len(receiver_prefs)
    for prefs, size in ((proposer_prefs, n_r), (receiver_prefs, n_p)):
        for lst in prefs:
            if len(set(lst)) != len(lst) or any(not 0 <= a < size for a in lst):
                raise ValueError("a preference list repeats an entry or is out of range")
    # rank_at[p][i] is the rank of p in the list of the i-th receiver of p, or -1.
    incoming: list[list[tuple[int, int]]] = [[] for _ in range(n_r)]
    for p, lst in enumerate(proposer_prefs):
        for i, r in enumerate(lst):
            incoming[r].append((p, i))
    rank_at = [[-1] * len(lst) for lst in proposer_prefs]
    mark = [-1] * n_p
    for r in range(n_r):  # @line L1
        for k, p in enumerate(receiver_prefs[r]):
            mark[p] = k
        for p, i in incoming[r]:
            rank_at[p][i] = mark[p]
        for p in receiver_prefs[r]:
            mark[p] = -1
    nxt = [0] * n_p  # @line L2
    holder = [-1] * n_r
    holder_rank = [-1] * n_r
    free = list(range(n_p - 1, -1, -1))  # @line L3: popped in order 0, 1, 2, ...
    proposals = 0
    while free:  # @line L4
        p = free.pop()  # @line L5
        if nxt[p] == len(proposer_prefs[p]):  # @line L6
            continue
        i = nxt[p]
        r = proposer_prefs[p][i]  # @line L7
        nxt[p] = i + 1
        proposals += 1
        k = rank_at[p][i]
        if k < 0:  # @line L8
            free.append(p)
            outcome = "unacceptable"
        elif holder[r] < 0:  # @line L9
            holder[r], holder_rank[r] = p, k
            outcome = "accepted"
        elif k < holder_rank[r]:  # @line L10
            q = holder[r]
            free.append(q)
            holder[r], holder_rank[r] = p, k
            outcome = f"replaces {q}"
        else:
            free.append(p)  # @line L11
            outcome = "rejected"
        if on_proposal is not None:
            on_proposal(p, r, outcome)
    partner = [-1] * n_p  # @line L12
    for r in range(n_r):
        if holder[r] >= 0:
            partner[holder[r]] = r
    return StableMatching(partner, holder, proposals)
