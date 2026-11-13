---
tag: 4VF43D
kind: technique
slug: move-ordering
name: Move ordering
aliases:
- move sorting
area: games-and-search/game-tree-search
level: advanced
summary: Trying the moves of each node in the order of a cheap guess of their quality, best first, so that alpha-beta finds its cutoffs early. The value stays the same and the tree gets smaller.
prereqs: [alpha-beta-pruning]
see_also: [killer-heuristic, history-heuristic, transposition-table, iterative-deepening-search, principal-variation, knuth-moore-theorem, quiescence-search, principal-variation-search]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: Section 6 (perfect ordering, the minimal tree, and the best case count)
  - paper: doi:10.1109/34.42858
    title: Jonathan Schaeffer, The history heuristic and alpha-beta search enhancements in practice, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(11) (1989)
    locator: pp. 1203 to 1212 (the effect of transposition tables, killer moves, history and other orderings, alone and together, measured in chess)
  - paper: doi:10.1145/356893.356895
    title: T. A. Marsland and M. Campbell, Parallel search of strongly ordered game trees, ACM Computing Surveys 14(4) (1982)
    locator: pp. 533 to 551; the section on strongly ordered trees and the sources of move ordering
  - book: isbn:9780387908151
    title: David J. Slate and Lawrence R. Atkin, CHESS 4.5, the Northwestern University chess program, in Peter W. Frey (ed.), Chess Skill in Man and Machine, Springer
    locator: pp. 82 to 118 (iterative deepening and the use of the previous iteration and of the table to order moves)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Section 5.2 (move ordering for alpha-beta, killer moves and iterative deepening)
---

Move ordering is the technique of trying the moves of each node of an [alpha-beta](/alpha-beta-pruning/) search in a chosen order, best first by some cheap guess. Alpha-beta returns the same value in every order, but its work depends a great deal on the order. When the best move comes first at every node, a uniform tree of branching factor $b$ and depth $d$ needs only about $2 b^{d/2}$ leaves, the bound of the [Knuth-Moore theorem](/knuth-moore-theorem/). In the worst order it can need all $b^d$. Since nobody knows the best move before the search, a program guesses it from cheap sources: the best move of an earlier search of the same position, captures of valuable pieces, moves that refuted other moves nearby, and a static score of the child. The order is a pure speed choice. A bad order costs time but never changes the answer.

## In plain words

When you look for the best move, try first the move that looks best. If it really is best, it gives you a strong score early, and a strong score lets you drop the other moves fast: as soon as one reply to a weaker move is bad enough for you, you stop looking at that move.

If you try the moves in a random order, you find the strong score late, so you look at more replies before you can drop a move.

The order never changes what the search finds. It only changes how much work the search does. So the guess can be rough, as long as it is cheap and right most of the time.

## When it applies

Move ordering applies to every search that prunes by bounds, such as alpha-beta, [principal variation search](/principal-variation-search/), [aspiration search](/aspiration-search/) and [MTD(f)](/mtdf/). It pays most when:
- a cheap score is known that is right most of the time about which move is best, and
- the tree is deep enough that the saving at the root multiplies over many levels.

It does not help plain [minimax](/minimax/), which visits every node in any order.

## The template

```pseudo id=main
ORDERED-ALPHABETA(n, d, α, β)
L1  if d = 0 or n is terminal then return EVALUATE(n)
L2  for each move x of n do s(x) ← SCORE(n, x)      ▷ hole: the guess of the quality of x
L3  sort the moves by s, highest first              ▷ hole: a full sort, or pick the best one at a time
L4  m ← −∞
L5  for each move x in this order, giving the child c, do
L6      t ← −ORDERED-ALPHABETA(c, d − 1, −β, −max(m, α))
L7      if t > m then m ← t
L8      if m ≥ β then return m                      ▷ cutoff: the later moves are skipped
L9  return m
```

**The holes.** SCORE in line L2 is where the knowledge goes. In a chess program it is usually a sum of tiers: the move from the [transposition table](/transposition-table/) first, then captures by the value of the captured piece and the capturing piece, then the [killer moves](/killer-heuristic/), then the other quiet moves by their [history](/history-heuristic/) score. Line L3 can sort all moves, or select the best remaining move each time line L5 asks for one. The selection is better in practice, because a cutoff after the first move or two saves the rest of the sort.

**Why the value does not change.** The proof on the [alpha-beta](/alpha-beta-pruning/) page holds for any order of the children, so lines L2 and L3 do not affect the result. With the full window the result is the [negamax](/negamax/) value of $n$.

**Why the order matters.** A cutoff happens at a node as soon as one move scores at least $\beta$. The earlier such a move comes, the fewer moves are searched. And the first move of a node also sets the bound $\max(m, \alpha)$ that its later moves pass down, so a good first move makes all later searches cheaper. In the perfect order, the [Knuth-Moore theorem](/knuth-moore-theorem/) shows that alpha-beta visits exactly $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves of a uniform tree, and the tests check this count for $b$ from 2 to 4 and $d$ from 1 to 5, with the perfect order made by a full search of each child.

**What the tests measure.** In tic-tac-toe from the empty board, with the squares in a random fixed order for each of 10 seeds, alpha-beta visits 194578 nodes in total. With the score "win first, then block a win, then the center, the corners and the edges", it visits 20968 nodes, about a ninth. In a random game where each move adds a gain to the score of the mover, with $b = 4$ and $d = 6$, the static score of the child cuts the total over 20 seeds from 27496 to 6932 nodes. The value is the same in every run.

## Classic examples

- **The move from the table and from the last iteration.** With [iterative deepening](/iterative-deepening-search/), the best move of the search to depth $d - 1$ is tried first in the search to depth $d$. The [transposition table](/transposition-table/) keeps a best move for each position, and the [principal variation](/principal-variation/) of the last iteration gives the first moves along the main line.
- **Captures by victim and attacker.** In chess, captures of the most valuable piece by the least valuable attacker come first. This is also the order used in [quiescence search](/quiescence-search/).
- **Killer moves.** A quiet move that caused a cutoff at another node of the same depth is tried early. See the [killer heuristic](/killer-heuristic/).
- **The history table.** Each move gets a score that grows each time it is best somewhere in the tree, and quiet moves are sorted by it. See the [history heuristic](/history-heuristic/).
- **Shallow searches.** Internal iterative deepening runs a shallow search at a node that has no move from the table, only to find a first move to try.

## Variations

- **Static or dynamic.** A static order depends only on the position, like the order by the type of the captured piece. A dynamic order learns during the search, like killers and history.
- **Order at the root.** At the root, programs often sort the moves by the size of their subtrees in the last iteration, because a move with a large subtree was hard to refute.
- **Ordering in other searches.** [Monte Carlo tree search](/monte-carlo-tree-search/) uses a policy to choose which moves to expand, and [proof-number search](/proof-number-search/) chooses by proof numbers. These play the same role as the order in alpha-beta.
- **Learned orders.** Modern programs score moves with a learned policy, as in programs for Go and chess that use neural networks.

## Pitfalls

- **Expensive scores.** A score that costs as much as a search of the child loses the gain. Most programs use a few table lookups per move.
- **A full sort too early.** Sorting all moves before the first one is searched wastes time at the nodes that cut off at once, which are many of the inner nodes in a well-ordered tree. Pick the best move one at a time.
- **Unstable ties.** If the sort is not stable, two runs with the same input can visit different nodes. This makes the node counts hard to reproduce and the bugs hard to find.
- **Ordering that hides a bug.** Since the value does not depend on the order, a bug that depends on the order shows up only as a change in the value with a new order. Compare the result with plain [negamax](/negamax/) on small trees and several orders, as the tests do.

## Exercises

1. Take the tree of the example on the [alpha-beta](/alpha-beta-pruning/) page and search it with the children of every node in the reverse order. Count the leaves, and compare them with the 5 of the original order.
2. Show that if every node is searched with its best move first, a cutoff at a node of type 2 happens after its first child. Use this to count the leaves of a uniform tree with $b = 3$ and $d = 4$.
3. The perfect order is not always the cheapest one. Find a small tree where another order of the children makes alpha-beta visit fewer leaves than the order with the best move first at every node. (Knuth and Moore give such a tree in Section 6 of their paper.)

## References
