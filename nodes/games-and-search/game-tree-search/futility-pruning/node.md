---
tag: 9FWPSR
kind: technique
slug: futility-pruning
name: Futility pruning
aliases:
- forward pruning
area: games-and-search/game-tree-search
level: advanced
summary: Skips moves near the leaves when the static evaluation plus a margin cannot raise alpha.
prereqs: [alpha-beta-pruning, evaluation-function, pruning]
see_also: [quiescence-search, null-move-pruning, late-move-reductions, move-ordering, search-extensions, horizon-effect]
sources:
  - paper: "Jonathan Schaeffer, Experiments in Search and Knowledge, PhD thesis, University of Waterloo (1986), also Technical Report TR 86-12, University of Alberta"
    locator: the part on selective search near the leaves (futility cutoffs)
  - paper: doi:10.3233/ICG-1998-21202
    title: Ernst A. Heinz, Extended futility pruning, ICCA Journal 21(2) (1998)
    locator: pp. 75 to 83 (normal futility pruning at frontier nodes, extended futility pruning at pre-frontier nodes, limited razoring, and the tests in DarkThought)
  - paper: "John A. Birmingham and Peter Kent, Tree-searching and tree-pruning techniques, in M. R. B. Clarke (editor), Advances in Computer Chess 1, Edinburgh University Press (1977)"
    locator: the chapter (razoring, which cuts a move when its static score is below alpha before the depth runs out)
  - paper: doi:10.1016/j.entcom.2011.11.003
    title: Kunihito Hoki and Masakazu Muramatsu, Efficiency of three forward-pruning techniques in shogi, Futility pruning, null-move pruning, and Late Move Reduction (LMR), Entertainment Computing 3(3) (2012)
    locator: pp. 51 to 57 (futility pruning measured in the shogi program Bonanza)
---

Futility pruning is a selective search rule for [alpha-beta](/alpha-beta-pruning/) near the leaves. At a node with one ply left, the *frontier node*, the program knows that a quiet move, a move that captures nothing, can change the static score by only a small amount, the *margin*. So if the static score plus the margin is still at most $\alpha$, no quiet move can raise $\alpha$, and the program skips all of them without making them. It still searches the captures, or leaves them to the [quiescence search](/quiescence-search/). *Extended futility pruning* (Heinz 1998) uses a larger margin at nodes with two plies left. If the margin really bounds the change of every quiet move, the rule is sound and returns the same value as plain alpha-beta. Real programs use margins that do not always hold, and then it is a heuristic that can return wrong values when a quiet move changes the score by more than the margin.

## In plain words

Near the end of its search, a chess program has one move left to look at. It is behind, and only a big gain would help it. A move that captures nothing can change the score by a little, but it cannot win a rook.

So the program skips all such quiet moves. It does not even play them on its board. It only looks at captures, which could win back enough. This saves time at the many nodes near the bottom of the tree.

The rule is safe only if the "little" is really little. If one quiet move could change the score a lot, for example because it pushes a pawn to the last row, the program can miss it.

## When it applies

- The search is alpha-beta with a [static evaluation](/evaluation-function/) at the leaves, and most nodes are near the leaves.
- The moves split into noisy moves, such as captures and promotions, and quiet moves, which change the static score by at most a known or estimated amount $\Delta$.
- The node is not in check, and the side to move is not near a mate score, because a quiet move can give or avoid mate and the margin does not bound that.

## The template

The search is fail-soft negamax alpha-beta. MARGIN($d$) is the margin at a remaining depth $d$; a depth without a margin is not pruned.

```pseudo
SEARCH(n, d, α, β)
    if n is terminal or d = 0 then return QUIESCE(n, α, β) or EVALUATE(n)
    s ← EVALUATE(n)
    m ← −∞
    for each move to a child c of n do
        a ← max(m, α)
        if MARGIN(d) is defined and c is quiet and s + MARGIN(d) ≤ a then
            m ← max(m, s + MARGIN(d))          ▷ an upper bound for the skipped move
            continue
        t ← −SEARCH(c, d − 1, −β, −a)
        m ← max(m, t)
        if m ≥ β then return m
    return m
```

The skipped move adds the bound $s + $ MARGIN$(d)$ to $m$. This keeps the result fail-soft: when the node fails low, the returned value is still an upper bound on its true value. Programs that use fail-hard values can skip this line.

**When it is sound.** Let every quiet move change the static score of the mover by at most $\Delta$, and let no move lower it by more than $\Delta$. At a frontier node, a quiet move to $c$ has the value $-$EVALUATE$(c) \le s + \Delta$, so MARGIN$(1) = \Delta$ is sound. At a node with two plies left, the opponent's best reply after a quiet move lowers the opponent's score by at most $\Delta$, so the value of the quiet move is at most $s + 2\Delta$, and MARGIN$(2) = 2\Delta$ is sound if the nodes at depth 0 return EVALUATE. With a quiescence search there, a capture after the reply can raise the score by more, and the bound fails. The tests check that with these margins the search returns the same value as a plain [negamax](/negamax/) search, with the full window and with a random window, on 600 random trees with $\Delta = 2$.

In chess no small $\Delta$ holds for all quiet moves. A quiet move can promote, give mate, or change a term of the evaluation, such as king safety, by a lot. So the margins of real programs are guesses, such as a few pawns at the frontier and a rook at depth two, and the rule is a heuristic.

## Classic examples

**A margin that is too small.** White moves at a frontier node with static score 0. The capture "cap" wins 3 points and is searched first, so $\alpha$ becomes 3. The quiet move "q" raises the score by 5. With a margin of 1, the test $0 + 1 \le 3$ holds, "q" is skipped, and the node returns 3. Plain alpha-beta returns 5. With a margin of 5, the test fails, "q" is searched, and the node returns 5.

**Measured on random trees.** The tests use 200 lazy random "material game" trees from the seeds 30000 to 30199 (Python's `random.Random`, seeded per node), with branching factor 4 and height 6. A move is a capture with probability 0.3 and wins 1, 3, 3, 5 or 9 points, and a quiet move changes the score by $-2$ to $+2$, so $\Delta = 2$. Captures are ordered first. Each tree is searched to depth 6.

| margins | nodes visited, all 200 trees | root value equal to plain alpha-beta |
| --- | --- | --- |
| none (plain alpha-beta) | 89,977 | 200 |
| depth 1: 2 | 71,038 | 200 |
| depth 1: 2, depth 2: 4 | 55,380 | 200 |
| depth 1: 0 | 68,352 | 147 |
| depth 1: 1, depth 2: 2 | 49,941 | 169 |

The sound margins kept every value and saved 21% and 38% of the nodes on this instance. The margins below $\Delta$ saved more nodes but changed the value in 53 and 31 of the 200 trees.

**Chess and shogi programs.** Schaeffer's thesis (1986) describes futility cutoffs in a chess program. Heinz (1998) added extended futility pruning at pre-frontier nodes and limited razoring at nodes with three plies left, and reported trees 10 to 20% smaller than with normal futility pruning in DarkThought. Hoki and Muramatsu (2012) measured futility pruning, with null-move pruning and [late move reductions](/late-move-reductions/), in the shogi program Bonanza.

## Variations

- **Extended futility pruning.** The same test at nodes with two plies left, with a larger margin, as in Heinz (1998).
- **Razoring.** Birmingham and Kent (1977) introduced razoring: cut off a move when its static score is below $\alpha$ before the depth runs out. Programs today often use it in a weaker form: at a node with few plies left whose static score plus a large margin is below $\alpha$, the depth is reduced by one ply, or the node drops straight into quiescence. Heinz's limited razoring is of this kind.
- **Delta pruning.** The same idea inside [quiescence search](/quiescence-search/): skip a capture if the static score plus the value of the captured piece plus a margin cannot reach $\alpha$.
- **Margins by depth.** Programs use a table of margins that grows with the remaining depth, which extends the rule to more plies at a higher risk.
- **Reverse futility pruning.** The mirror test for a fail high: if the static score minus a margin is at least $\beta$, the node returns at once. It is a heuristic close to [null-move pruning](/null-move-pruning/), and it is engine practice that we have not seen in a primary source.

## Pitfalls

- **Check and mate.** Do not prune when the side to move is in check, or when a move gives check, or when the scores are near a mate value. A quiet move can give mate.
- **Promotions and threats.** Count pawn pushes to the last ranks as noisy moves, or the margin is wrong for them.
- **Large positional terms.** If the evaluation has terms that can change by more than the margin, such as king safety or a passed pawn, the rule prunes moves that matter.
- **Skipping all moves.** If every move is skipped, $m$ stays $-\infty$ in a fail-soft search without the bound line, which would look like a mate. Keep the bound $s + $ MARGIN$(d)$, or return $\alpha$.
- **Measured gains.** The node savings above are for one random instance. Savings in a real program depend on the evaluation, the move order and the other pruning methods, and we do not quote a general number.

## Exercises

1. Prove that MARGIN$(1) = \Delta$ is sound when every quiet move changes the static score by at most $\Delta$. *Hint.* The value of a quiet move at a frontier node is the negated static score of the child.
2. Prove that MARGIN$(2) = 2\Delta$ is sound when, in addition, no move lowers the mover's score by more than $\Delta$. Show by an example that the second condition is needed.
3. Why does the rule not prune captures? Give a case where pruning a capture at a frontier node with the margin $\Delta$ changes the value.
4. In the table above, the margins 1 at depth 1 and 2 at depth 2 visit fewer nodes than the margin 0 at depth 1. Explain why a smaller margin at one depth and a margin at a second depth can both matter.
5. Write the reverse futility test and show an example where it returns a wrong value.

## References
