---
tag: EJ7NFT
kind: technique
slug: late-move-reductions
name: Late move reductions
aliases:
- LMR
area: games-and-search/game-tree-search
level: advanced
summary: Searches later moves in the ordering to reduced depth, assuming good ordering makes them less promising.
prereqs: [alpha-beta-pruning, move-ordering, principal-variation-search]
see_also: [null-move-pruning, futility-pruning, search-extensions, history-heuristic, killer-heuristic, knuth-moore-theorem, iterative-deepening-search, pruning]
sources:
  - paper: doi:10.1016/j.entcom.2011.11.003
    title: Kunihito Hoki and Masakazu Muramatsu, Efficiency of three forward-pruning techniques in shogi, Futility pruning, null-move pruning, and Late Move Reduction (LMR), Entertainment Computing 3(3) (2012)
    locator: pp. 51 to 57 (LMR measured in the shogi program Bonanza, together with futility and null-move pruning)
  - url: https://www.chessprogramming.org/Late_Move_Reductions
    title: Chess Programming Wiki, Late Move Reductions
    locator: the history section (LMR became widely used in 2005 with the programs Fruit and Glaurung) and the list of common conditions
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the three types of nodes of a minimal tree, which explain why late moves at some nodes all fail low)
---

Late move reductions (LMR) is a selective search rule for [alpha-beta](/alpha-beta-pruning/) that makes the search depth depend on the place of a move in the [move order](/move-ordering/). The first few moves of a node, and the captures and checks, are searched to the full depth. Every later quiet move is first searched to a depth reduced by $R$ plies, usually one ply, with a null window at $\alpha$. If that cheap search shows the move to be no better than the best move so far, as it usually is when the order is good, the move is dropped. If it fails high, the move is searched again at the full depth. LMR rests on the claim that a good move order puts the best move early, so the late moves are rarely best. When the claim is false, LMR returns a wrong value, so it is a heuristic, not a sound rule. It has no founding paper: it spread among chess programs in the 2000s, and its history is mostly program practice.

## In plain words

A chess program sorts its moves so that the best ones come first: captures, then moves that were good before, then the rest. After a few moves, the rest are usually poor.

So the program looks at the late moves less deeply. It asks a cheap question: "Is this move better than what I have?" If the quick look says no, the program believes it and moves on.

If the quick look says yes, the program does not trust it either. It searches that move again at the full depth.

This saves much time when the sort is good. It can be wrong when a late quiet move has a deep idea that only the full search can see.

## When it applies

- The search is alpha-beta with iterative deepening, a [transposition table](/transposition-table/), [killer moves](/killer-heuristic/) and a [history table](/history-heuristic/), so that the move order is good.
- Most nodes are expected to fail low, the ALL nodes of Knuth and Moore (1975). At such a node every move fails low, so the late moves only need to be shown no better than $\alpha$, and a reduced search is a cheap way to show that.
- The program uses null windows, as in [principal variation search](/principal-variation-search/), so the re-search on a fail high is part of the normal control flow.

## The template

The search is fail-soft negamax alpha-beta, and $K$ is the number of moves that are always searched in full.

```pseudo
SEARCH(n, d, α, β)
    if n is terminal or d = 0 then return QUIESCE(n, α, β) or EVALUATE(n)
    m ← −∞
    for each move to a child c of n, in order, with index i = 0, 1, ... do
        a ← max(m, α)
        if i ≥ K and c is quiet and not a check and d − 1 − R ≥ 0 then
            t ← −SEARCH(c, d − 1 − R, −a − 1, −a)       ▷ reduced depth, null window
            if t > a then t ← −SEARCH(c, d − 1, −β, −a)  ▷ fail high: search again in full
        else
            t ← −SEARCH(c, d − 1, −β, −a)
        m ← max(m, t)
        if m ≥ β then return m
    return m
```

Programs that use [principal variation search](/principal-variation-search/) do the re-search in two steps: first at the full depth with the null window, then with the full window only if that fails high too.

**What the template keeps.** With $K$ at least the number of moves, no move is reduced, and the search is plain alpha-beta. The tests check that it then returns the same value and visits exactly the same nodes as plain alpha-beta, on 500 random trees. With $K$ smaller, LMR is not exact.

## Classic examples

**A late move with a threat.** White moves at R with two plies left. The first move "m0" wins 1 point. The late quiet move "m1" keeps the static score at 0, but it makes a threat that Black cannot meet: each Black reply leaves White 4 points up, so the depth-2 value of "m1" is 4. With $K = 1$ and $R = 1$, LMR searches "m1" to depth 0 with the null window at $\alpha = 1$. The static score of "m1" is 0, which fails low, so "m1" is dropped, and the root returns 1. Plain alpha-beta returns 4. With $K = 2$ the move is not reduced and the root returns 4.

**Measured on random trees.** The tests use 200 lazy random "material game" trees from the seeds 40000 to 40199 (Python's `random.Random`, seeded per node), with branching factor 4 and height 7. A move is a capture with probability 0.3 and wins 1, 3, 3, 5 or 9 points, and a quiet move changes the score by $-2$ to $+2$. Moves are ordered by their static score. Each tree is searched to depth 7, and plain alpha-beta visits 197,970 nodes in all.

| $K$ | $R$ | nodes visited, all 200 trees | root value equal to plain alpha-beta |
| --- | --- | --- | --- |
| 1 | 1 | 91,300 | 82 |
| 2 | 1 | 102,556 | 116 |
| 3 | 1 | 139,334 | 171 |
| 1 | 2 | 57,430 | 126 |

On these trees LMR saved between 30% and 71% of the nodes, and it changed the root value in 29 to 118 of the 200 trees. The random trees have little relation between the static order of the moves and their deep values, so the claim on which LMR rests is often false in them. In this sample the larger reduction $R = 2$ changed fewer values than $R = 1$; a random instance like this one does not show a general rule, and we draw none. In chess programs the order is much better, but we have no measured rate of changed values from a source that we have checked.

**Chess and shogi programs.** The Chess Programming Wiki dates the wide use of LMR to 2005, with the programs Fruit and Glaurung. This history is program practice and is not in a peer-reviewed paper that we have seen. Hoki and Muramatsu (2012) measured LMR, futility pruning and null-move pruning in the shogi program Bonanza.

## Variations

- **Reductions that grow.** Many programs reduce more for later moves and at larger depths, for example with a reduction that grows with the logarithm of the depth and of the move index. The formulas are tuned per program.
- **History-based conditions.** Do not reduce a move with a good [history](/history-heuristic/) score, a [killer move](/killer-heuristic/), or a move that escapes a threat.
- **Node type.** Reduce less on the [principal variation](/principal-variation/), where a wrong reduction changes the result of the whole search, and more at expected ALL nodes.
- **Late move pruning.** At small depths, skip the late quiet moves entirely instead of reducing them. This is closer to [futility pruning](/futility-pruning/).
- **Extensions and reductions together.** A move that gets a [search extension](/search-extensions/), such as a check, is not reduced.

## Pitfalls

- **A bad move order.** LMR assumes that the order is good. With a random order, as in the measured example above, it changes many values.
- **Tactical moves.** Do not reduce captures, promotions, checks or moves out of check. The template reduces quiet moves only.
- **No re-search.** Without the re-search on a fail high, a reduced move can never become the best move, and the search plays only its first $K$ moves at depth.
- **Interaction with null-move pruning.** Two reductions on the same line make the line very short, which brings the [horizon](/horizon-effect/) close.
- **Transposition table depth.** A value stored after a reduced search has the reduced depth. Store that depth, not the nominal one.
- **Measured gains.** A node saving or a rating gain in one program says little about another program. The numbers above are for one random instance only.

## Exercises

1. Show that with $K$ at least the number of moves at every node, LMR visits the same nodes as plain alpha-beta. *Hint.* No move takes the first branch.
2. In the late threat example, find the smallest depth $d$ at the root with $K = 1$ and $R = 1$ at which LMR returns the correct value, if one exists, and explain the answer.
3. At a node where every move fails low (an ALL node), show that the reduced search of a move with the null window $(a, a + 1)$ is a valid proof that the move is at most $a$ only if the reduced value bounds the full-depth value from above. When does this hold?
4. Change the template so that the reduction is $R = 1 + \lfloor i / 4 \rfloor$ for the move with index $i$, and count the nodes on a uniform tree in which no re-search happens.
5. Combine LMR with the two-step re-search of principal variation search, and compare the node counts of the two-step and the one-step versions on random trees.

## References
