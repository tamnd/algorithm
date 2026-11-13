---
tag: XSFAN1
kind: technique
slug: history-heuristic
name: History heuristic
aliases:
- history table
area: games-and-search/game-tree-search
level: advanced
summary: Move ordering that keeps one score per move for the whole search, adds a bonus that grows with the depth each time the move is best at a node, and tries high scores first.
prereqs: [move-ordering]
see_also: [killer-heuristic, alpha-beta-pruning, transposition-table, iterative-deepening-search, late-move-reductions, principal-variation-search]
sources:
  - paper: "Jonathan Schaeffer, The history heuristic, ICCA Journal 6(3) (1983), pp. 16 to 19"
    title: Schaeffer 1983
    locator: the whole paper (the table indexed by the from-square and the to-square, and the bonus for the best move)
  - paper: doi:10.1109/34.42858
    title: Jonathan Schaeffer, The history heuristic and alpha-beta search enhancements in practice, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(11) (1989)
    locator: pp. 1203 to 1212 (the bonus 2^depth, and the history heuristic compared with killer moves, transposition tables and other enhancements in chess)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Section 5.2 (move ordering from earlier search results)
---

The history heuristic is a [move ordering](/move-ordering/) rule for [alpha-beta](/alpha-beta-pruning/) search, introduced by Jonathan Schaeffer in 1983. It keeps a table with one score for each move, where a move is named in a way that does not depend on the position, such as the pair (from-square, to-square) in chess. Each time a move is the best move at a node of the search, its score grows by a bonus that is larger for a deeper remaining search, often $2^d$ or $d^2$. At each node, the moves are tried in the order of their scores. So the table learns, over the whole tree, which moves tend to be good in this game and this part of it. The [killer heuristic](/killer-heuristic/) remembers the last cutoff moves of one ply, and the history heuristic is its generalization to all moves and all plies. The value of the search does not change.

## In plain words

Keep a scoreboard with one line for every kind of move, such as "the knight from this square to that square". Every time a move turns out to be the best one somewhere in the search, give it points. Give more points when the search below that spot was deep, because then the result is more reliable.

When you come to a new position, try the moves with the most points first.

A move that worked in many positions will often work in the next one too. If it does not, you try the other moves as usual, so the answer stays the same, and only the amount of work changes.

## When it applies

The history heuristic applies to an alpha-beta search where:
- moves have names that make sense across many positions, so the same name in two positions means a similar action, and
- a good move in one part of the tree is often good in many others.

It is the main order for quiet moves in chess, after the move from the [transposition table](/transposition-table/), the good captures and the killers. It needs no knowledge of the game, only the names of the moves.

## The template

```pseudo id=main
HISTORY-ALPHABETA(n, d, α, β)
L1  if d = 0 or n is terminal then return EVALUATE(n)
L2  sort the moves of n by H[x], highest first, keeping the base order for ties
L3  m ← −∞; best ← NIL
L4  for each move x in this order, giving the child c, do
L5      t ← −HISTORY-ALPHABETA(c, d − 1, −β, −max(m, α))
L6      if t > m then m ← t; best ← x
L7      if m ≥ β then break
L8  if m > α then                                 ▷ a cutoff or a new best value, not a fail low
L9      H[best] ← H[best] + BONUS(d)              ▷ hole: the bonus, 2^d or d·d
L10 return m
```

**The holes.** BONUS gives more weight to results from deeper searches, which cover more of the tree and come up less often. Schaeffer used $2^d$. Many programs use $d^2$, which grows slower and keeps the scores in range. The name of a move is the other hole. In chess it is the pair of squares, a table of $64 \times 64$ entries, sometimes with one table per side or per piece type.

**Which nodes give a bonus.** Line L8 rewards the best move of a node only if its result is above $\alpha$. Such a node either had a cutoff, so its move was good enough to refute the move of the opponent, or found an exact value, so its move was the best one. A node that fails low has no good move, and its "best" move is only the least bad bound, so it gives no bonus.

**Why the value does not change.** The table only changes the order of the moves at line L2, and the proof on the [alpha-beta](/alpha-beta-pruning/) page holds for any order. The tests also start a search with a table filled by another tree, and the result is still exact.

**Cost.** Line L2 is a sort of the $k$ moves of the node, $O(k \log k)$, or less with a partial selection. The update in line L9 is $O(1)$.

**What the tests measure.** In tic-tac-toe from the empty board, with the squares in a random fixed order for each of 10 seeds, plain alpha-beta visits 194578 nodes in total, and alpha-beta with the history heuristic and the bonus $2^d$ visits 106163. In a random game where move $m$ adds a gain $w_m$ plus noise to the score of the mover, with $b = 4$ and $d = 6$, the total over 20 seeds falls from 27496 to 12705 nodes. In that game the history heuristic does better than two killers per ply, which give 16943 nodes in the same test on the [killer heuristic](/killer-heuristic/) page. In tic-tac-toe it is the other way around: the killers give 75093 nodes, since the best square depends a great deal on the position.

## Classic examples

- **Chess programs.** After the move from the [transposition table](/transposition-table/), the good captures and the [killer moves](/killer-heuristic/), the quiet moves are sorted by a history table indexed by the piece or the from-square, and the to-square.
- **Late move reductions.** [Late move reductions](/late-move-reductions/) search the moves late in the order with less depth. The history score decides which moves come late, and some programs also reduce less for a move with a high score.
- **Iterative deepening.** With [iterative deepening](/iterative-deepening-search/), the table of the search to depth $d - 1$ already orders the search to depth $d$, so the deep search starts with a good order.
- **Other board games.** Programs for checkers, Othello and other games use the history heuristic, since it needs no game knowledge, only a name for each move.

## Variations

- **Aging.** Between two searches, divide all scores by 2 (or clear the table), so the results of an old position fade. The implementation has a method for this.
- **Butterfly and relative history.** Count also how often each move was searched, and order by the ratio of the history score to that count. A move that is searched often then needs more cutoffs to rank high.
- **Penalties.** Subtract a bonus from the moves that were searched before the cutoff move and failed. The score then measures the gain over the other moves, not only the cutoffs.
- **Continuation history.** Index the table by the previous move as well as by the current one. This combines the history heuristic with the idea of counter moves.
- **Bounded updates.** Some programs keep each score in a fixed range by a rule that moves it a fraction of the way toward a limit. This avoids overflow and gives recent results more weight.

## Pitfalls

- **Overflow.** With the bonus $2^d$ and a deep search, the scores grow fast. In a fixed-width integer they overflow and the order goes wrong. Age the table, use $d^2$, or bound the scores.
- **Rewarding fail-low nodes.** If line L8 is dropped, the "best" move of each fail-low node gets a bonus, although it is only the least bad move. This adds noise to the table and weakens the order.
- **Moves that mean different things.** A name that is too coarse, such as only the to-square, merges moves of different pieces. A name that is too fine, such as the full position and the move, never repeats and learns nothing.
- **Captures in the table.** Captures have their own order, so most programs keep a separate table for them or none at all.

## Exercises

1. A table starts empty. The moves a, b and a are rewarded at the remaining depths 1, 3 and 2, with the bonus $2^d$. Give the scores and the order of the moves a, c and b at the next node. Then halve the scores. The test file checks these values.
2. Show by an example that the history heuristic can make alpha-beta visit more nodes than the base order in one tree. Why does the average over many trees still improve in games like the random game of the tests?
3. Compare the bonuses $2^d$ and $d^2$ in a search to depth 12. How much more does a result at depth 12 weigh than one at depth 2 in each case?

## References
