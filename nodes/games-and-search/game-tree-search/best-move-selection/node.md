---
tag: Y4MTQZ
kind: problem
slug: best-move-selection
name: Best move selection
aliases:
- move selection
area: games-and-search/game-tree-search
level: advanced
summary: Given a game position and a search budget, return a move whose value equals the value of the position, with a rule for ties and for moves whose search returned only a bound.
prereqs: [minimax, negamax, iterative-deepening-search]
see_also: [alpha-beta-pruning, principal-variation, aspiration-search, move-ordering, game-tree-evaluation, transposition-table, monte-carlo-tree-search, knuth-moore-theorem]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.2 (MINIMAX-SEARCH returns the action with the best value) and Section 5.3 (iterative deepening and move ordering in heuristic alpha-beta search)
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (what the alpha-beta procedure returns when the value lies below, inside or above the window, and the minimal number of leaves)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (iterative deepening, and its use in game programs to fit the search to a time limit)
---

Best move selection is the problem that a game program solves at each turn: given a position, choose the move to play. In a finite game with [perfect information](/perfect-information-game/), a *best move* is one that leads to a position whose value is the value of the current position, so [game tree evaluation](/game-tree-evaluation/) and best move selection are close. They are not the same. A search that returns the right value can still return the wrong move, if it keeps a move whose value is only a bound, breaks ties in a way that changes from one run to the next, or stops in the middle of a search. This page states the problem and the rules that make the answer right. On this page all values are negamax values, from the point of view of the side to move.

## In plain words

Knowing that your position is worth a draw is not enough; you have to make a move, and you want one that keeps the draw.

A program finds the move by looking at each move and asking what it is worth. Fast searches do not find the exact worth of every move. For most moves they only find out that the move is "no better than" the best one so far, and they stop there. That is enough to reject the move, but not to pick it. So the program must change its choice only when a move is shown to be strictly better.

Programs also run out of time. They search one move deep, then two, then three, and when time is up they play the move from the last search that finished, not from the one that was cut off.

## Definition

**Input.** A position $r$ of a game, a move generator, an evaluation function EVALUATE for the side to move, and a search limit: a depth $d$ in plies, or a budget of time or nodes.

**Output.** A move $m^*$ of $r$ and a value $v$. Let $N_d(p)$ be the depth-$d$ [negamax](/negamax/) value: EVALUATE$(p)$ if $p$ is terminal or $d = 0$, and $\max_c \bigl(-N_{d-1}(c)\bigr)$ over the children $c$ otherwise. The output is correct for depth $d$ when
$$ v = N_d(r) \quad\text{and}\quad -N_{d-1}(r \cdot m^*) = v, $$
where $r \cdot m$ is the position after the move $m$. With $d$ at least the height of the tree, $N_d$ is the exact minimax value and $m^*$ is a best move of the game.

**Ties.** Several moves can have the value $v$. The problem allows any of them, but a program needs a fixed rule. The rule used here is "the first move in the search order with the value $v$", which follows from changing the choice only on a strict improvement.

**Search limit.** Under a time or node budget, the output is the answer for the largest depth $d$ whose search finished within the budget.

## Variants

- **Value and move.** The usual form, as above.
- **Move only.** A program that plays needs only $m^*$, so it can skip work that proves the exact value of $m^*$. It still needs a proof that no other move is better.
- **Principal variation.** Return the whole line of best moves for both sides, not only the first. See [principal variation](/principal-variation/).
- **Several best moves.** Return the $k$ best moves with their values, for analysis or to choose at random among equal moves for variety. This needs exact values for $k$ moves, so fewer cutoffs.
- **Chance and hidden information.** With chance nodes, the best move maximizes the expected value; see [expectiminimax](/expectiminimax/). In [Monte Carlo tree search](/monte-carlo-tree-search/), programs usually play the root move with the most visits, which is more stable than the move with the highest mean.

## Examples

**The tree of the minimax page.** MAX moves at the root, and the outcomes for MAX are the leaves 3, 17 and 2, 12 under the left MIN node, and 15, 25 and 2, 5 under the right one. The left move has value 12 and the right move 5, so the best move is the left one, with value 12. A full-width search and an [alpha-beta](/alpha-beta-pruning/) search both visit 15 nodes here, because the order gives no cutoff.

Now swap the two MAX nodes under the right MIN node, so that its children are 2, 5 first and 15, 25 second. Alpha-beta searches the left move first and gets 12. At the right move, the first reply already holds MAX to 5, which is below 12, so the second reply is skipped and the search returns 5. This 5 is only an upper bound: had the skipped reply led to 1, the move would be worth 1. The root keeps the left move, because $5 > 12$ is false. A program that compared the bound 5 with other bounds, or that took the last move searched, would be wrong.

**A tie.** Under a MAX root, two MIN nodes have the leaves 4, 9 and 7, 4. Both moves have value 4. The search picks the first move. If the program puts the second move first, for example because it was best in the last iteration, it picks the second. Both are correct; the value does not change.

**Tic-tac-toe.** On the empty board, a full search visits 549,946 nodes and alpha-beta at the root visits 18,297. Both return the first square with value 0, because every first move draws. After X takes a corner, the only reply of O that draws is the centre, and the search finds it. After X takes the centre, the first corner is the first reply that draws. With X X _ / O O _ / _ _ _ and X to move, the search plays the third square and wins.

## Known algorithms

### Root search with a strict comparison

The [minimax](/minimax/) and [negamax](/negamax/) pages compute the value; the root of the search is where the move is chosen. The root keeps the best value $\alpha$ found so far, starting at $-\infty$, and the move that gave it. It searches each move in turn, and it replaces the kept move only when the new move's value is strictly greater than $\alpha$.

With [alpha-beta](/alpha-beta-pruning/) under the root, the search of a move uses the window $(\alpha, +\infty)$ from the root's side. In fail-soft alpha-beta with the window $(\alpha, \beta)$, a returned value $w$ with $\alpha < w < \beta$ is exact, $w \le \alpha$ means that the true value is at most $w$, and $w \ge \beta$ means that it is at least $w$. So a move either gets its exact value, when that value is above $\alpha$, or a bound $w \le \alpha$. The strict test then takes exactly the moves that are better than all earlier ones, and it ends with the first move of the best value. A test of "greater or equal" would take the last move of the best value with plain negamax, and with alpha-beta it could take a move whose bound only equals $\alpha$ and whose true value is lower.

The tests of this page check the rule against a full-width search on random trees with fixed seeds: the chosen child's value equals the root value, ties go to the first best move, and alpha-beta and full-width search choose the same move.

### Iterative deepening

Search to depth 1, 2, 3 and so on, as in [iterative deepening search](/iterative-deepening-search/). Each iteration puts the best move of the last iteration first, which gives early cutoffs, so the series often costs little more than the last search. When the budget runs out during an iteration, the program throws that iteration away and plays the move of the last one that finished. A partial iteration can have searched only some moves, and its current best move may be one that a later move would beat. Programs often relax this rule a little: if the first move of the new iteration was searched in full, a move that beat it in the same iteration is also safe to play.

### Faster searches at the root

- **[Aspiration search](/aspiration-search/).** Search the root with a narrow window around the last value. If the result falls outside the window, the search failed high or low, and the move is not known; search again with a wider window before choosing.
- **[Principal variation search](/principal-variation-search/).** Search the first move with a full window and the others with a null window. A move that fails high on the null window is better, but its value is only a lower bound, so search it again with a full window to get its value and confirm it.
- **[MTD(f)](/mtdf/).** A series of null-window searches converges to the value. The move comes from the [transposition table](/transposition-table/) entry of the root, not from the last call.

## Bounds

**Upper bound.** One alpha-beta search at the root gives the move and the value. With perfect move ordering on a uniform tree of branching factor $b$ and depth $d$, it evaluates $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, the bound of the [Knuth-Moore theorem](/knuth-moore-theorem/). Without pruning it evaluates all $b^d$.

**Lower bound.** Best move selection is at least as hard as deciding the value of a Boolean game tree, by the reduction below. So a deterministic algorithm must read all $n$ leaves of some trees, and for uniform binary NAND trees a randomized one needs an expected $\Theta(n^{0.7537})$ leaves, as on [game tree evaluation](/game-tree-evaluation/).

## Reductions

**From game tree evaluation.** Let $T$ be a game tree with leaf values 0 and 1 for MAX. If MAX moves at the root of $T$, put above it a MIN node whose only child is the root of $T$; this does not change the value. Now build a MAX root with two moves: one to a leaf of value $1/2$, and one to the root of $T$ (or to the new MIN node). The best move goes to $T$ if and only if the value of $T$ is 1. The value of $T$ is never $1/2$, so there are no ties. Thus any algorithm for best move selection decides the value of $T$, with the same leaf reads plus one.

**To game tree evaluation.** With one evaluation per move of the root, and the strict test, the value gives the move. Alpha-beta does this in one search with shared bounds, as above.

## Applications

- **Game programs.** A chess engine answers "bestmove" after each search; a program for Go or Othello does the same.
- **Analysis.** A program that shows the best line, or several best moves with values, to a player who studies a position.
- **Testing searches.** The rule "the chosen child has the root value" is a simple check on any search, and the tests of this page use it on random trees.

## References
