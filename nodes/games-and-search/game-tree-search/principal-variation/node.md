---
tag: Z9NCM4
kind: concept
slug: principal-variation
name: Principal variation
aliases:
- PV
area: games-and-search/game-tree-search
level: advanced
summary: The line of play that the search expects, from the root to a leaf, where each side plays a best move. The value at its last position equals the value of the root.
prereqs: [alpha-beta-pruning]
see_also: [principal-variation-search, iterative-deepening-search, move-ordering, transposition-table, aspiration-search, best-move-selection, quiescence-search, knuth-moore-theorem]
sources:
  - paper: doi:10.1145/800179.810240
    title: Selim G. Akl and Monroe M. Newborn, The principal continuation and the killer heuristic, Proceedings of the ACM Annual Conference (ACM '77)
    locator: pp. 466 to 473 (the principal continuation, how to keep it during alpha-beta, and its use to order the next search)
  - paper: doi:10.1145/356893.356895
    title: T. A. Marsland and M. Campbell, Parallel search of strongly ordered game trees, ACM Computing Surveys 14(4) (1982)
    locator: pp. 533 to 551; the sections on the principal variation and the minimal tree
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: Section 6 (the positions of type 1 under perfect ordering, which form the principal variation)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5 (the best line of play in alpha-beta search and iterative deepening)
---

The principal variation, or PV, of a game-tree search is a line of play from the root to a leaf in which, at every position on the line, the side to move plays a move that is best by the search. A leaf here is a terminal position or a position at the depth limit. Because each move on the line keeps the value, the static value at the end of the line is the value of the root, seen from the right side. So the PV explains the value: it is the game that the search expects if both sides play well. A program prints it to show what it is thinking, plays its first move, and uses its next moves to order the next search. [Alpha-beta](/alpha-beta-pruning/) finds a PV for free when it gets the exact value of the root, by passing up the line of the best child at each node. It is the line that [principal variation search](/principal-variation-search/) is named after.

## In plain words

The search tells you more than "this move is best". It also tells you why: "I play this, then my opponent's best answer is that, then I play this, and so on." That chain of best moves is the principal variation.

At the end of the chain is a position that the program can score. That score is the same as the score of the whole search, because both sides played their best all the way.

The chain is useful. It shows you the plan. And when the program searches again, one move deeper, it tries the moves of the chain first, because they were best last time.

## The idea

Write $N(p)$ for the [negamax](/negamax/) value of a position $p$ for the side to move, with the search to a fixed depth. A line of moves $x_1, x_2, \ldots, x_k$ from the root $p_0$ leads to the positions $p_1, \ldots, p_k$. It is a *principal variation* if
- each move $x_i$ is legal at $p_{i-1}$,
- each move is best: $N(p_{i-1}) = -N(p_i)$ for $i = 1, \ldots, k$, and
- $p_k$ is a leaf: a terminal position, or a position at the depth limit.

By the second condition, $N(p_i) = (-1)^i N(p_0)$, so the static value at the end, $\text{EVALUATE}(p_k) = N(p_k)$, is $(-1)^k$ times the root value. In the minimax view, MAX and MIN get the root value at every position of the line.

**Finding it with alpha-beta.** Let each call of alpha-beta return a line as well as a value: a leaf returns the empty line, and an inner node returns its best move followed by the line of that child. If the result $r$ of a node is strictly inside its window $(\alpha, \beta)$, the line is a PV of the node. The reason is the proof on the [alpha-beta](/alpha-beta-pruning/) page: when $r$ is exact, the first child $c_j$ with $-t_j = r$ got a window $(-\beta, -a_j)$ with $a_j < r < \beta$, so its result $t_j$ was inside its own window too, and its value is exactly $-r$. By induction the line of $c_j$ is a PV of $c_j$, and the move to $c_j$ keeps the value. At a node that fails high or low, the result is only a bound, and its line means nothing. With the full window, the root is always exact, so the line is a PV.

Programs keep these lines in a *triangular array*: row $p$ holds the line from ply $p$, and a new best move at ply $p$ copies row $p + 1$ behind it. This is the same as the lists in the implementation, with $O(d)$ work for each new best move. Another way is to read the best moves back from the [transposition table](/transposition-table/), starting at the root. This needs no extra code in the search, but an entry can be overwritten or can hold the move of a bound, so the line can be cut short or wrong at its end.

**Not unique.** If two moves have the same value, there are two PVs. Alpha-beta returns the first one in its [move order](/move-ordering/). A PV is also only as good as the depth: past the depth limit the line stops, and a move that looks best at depth $d$ can be a mistake at depth $d + 1$. [Quiescence search](/quiescence-search/) lengthens the line with captures, so the last position is quiet.

## Examples

**A small tree.** In the minimax view, MAX is at the root and has the moves L and R to MIN nodes. Under L, MIN can choose 3 or 17, and under R, 2 or 12. So L is worth 3, R is worth 2, and the root is worth 3. The PV is L, then the move of MIN to 3. The value at its end, 3, is the root value. The test file checks this tree in negamax form.

**Tic-tac-toe.** Tic-tac-toe is a draw with best play. From the empty board, the PV found by the full search has 9 moves, since no side can win, and the board fills up. Its last position is a draw, value 0, which is the root value. The tests replay the line move by move, check that each move is legal, and check that each position on it has the root value, from the side to move. They do the same from random positions of tic-tac-toe and on random trees with integer and fractional leaves, with and without a depth limit.

**Chess output.** A chess program at depth 12 may print a line like "e4 e5 Nf3 Nc6 Bb5 a6 ..." with a score. The score is the evaluation at the end of the line, for the side to move at the root.

## Where it is used

- **[Iterative deepening](/iterative-deepening-search/).** The PV of the search to depth $d - 1$ is searched first in the search to depth $d$. Along the PV, the old best moves are usually best again, so the new search starts with a good [move order](/move-ordering/).
- **[Principal variation search](/principal-variation-search/).** It assumes that the first move at a PV node is best, searches it with the full window, and tests the other moves with null windows. Only the nodes on the expected PV get full windows.
- **[Aspiration search](/aspiration-search/).** The value of the last PV is the center of the window of the next search.
- **The minimal tree.** In the [Knuth-Moore theorem](/knuth-moore-theorem/), the positions of type 1 under perfect ordering are exactly the positions on the PV. Each of them is searched with the full window, and the rest of the minimal tree hangs off them.
- **Playing and pondering.** The program plays the first move of the PV. Its second move is the expected reply, and a program that thinks on the time of the opponent searches the position after that reply.
- **[Best move selection](/best-move-selection/).** The first move of the PV is the move that the search selects.

## References
