---
tag: QESA6R
kind: problem
slug: tetris-problem
name: Tetris problem
aliases:
- Tetris complexity
- Optimal Tetris placement
area: games-and-search/puzzles
level: advanced
summary: Given a Tetris board and the whole piece sequence in advance, place the pieces to clear the most rows or to survive. NP-complete and hard to approximate (Demaine et al. 2003).
prereqs: [np-complete, three-partition]
see_also: [strong-np-hardness, gadget-reduction, approximation-threshold, dag-dynamic-programming, polyomino-tiling-problem, markov-decision-process, online-algorithm]
sources:
  - paper: doi:10.1007/3-540-45071-8_36
    title: Erik D. Demaine, Susan Hohenberger and David Liben-Nowell, Tetris is hard, even to approximate, Computing and Combinatorics (COCOON 2003), Lecture Notes in Computer Science 2697, Springer, 2003, 351 to 363
    locator: the whole paper (the offline model, and NP-completeness by a reduction from 3-partition)
  - paper: doi:10.1142/S0218195904001354
    title: Ron Breukelaar, Erik D. Demaine, Susan Hohenberger, Hendrik Jan Hoogeboom, Walter A. Kosters and David Liben-Nowell, Tetris is hard, even to approximate, International Journal of Computational Geometry and Applications 14(1-2), 2004, 41 to 68
    locator: the whole paper (the full proofs, and the bounds on approximation for rows, pieces and height)
  - paper: doi:10.2307/3619195
    title: Heidi Burgiel, How to lose at Tetris, The Mathematical Gazette 81(491), 1997, 194 to 200
    locator: the whole note (alternating S and Z pieces force a loss on the standard well, so a random game ends with probability 1)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 and problem SP15 (3-partition and its strong NP-completeness)
---

The Tetris problem is the *offline* version of the game. It gives a well of $w$ columns and $h$ rows, a starting board of filled cells, and the full finite sequence of tetrominoes that will fall. Decide how to place each piece to reach a goal: clear the most rows, place the most pieces before the game is lost, get the most four-row clears, or keep the highest filled cell low. Demaine, Hohenberger and Liben-Nowell (2003) showed that all these goals are [NP-complete](/np-complete/) by a reduction from [3-partition](/three-partition/). Breukelaar et al. (2004) showed they are also hard to approximate. In the usual *online* game the pieces are not known ahead, and Burgiel (1997) showed that some sequences end the game whatever the player does.

## In plain words

In Tetris, shapes made of four squares fall into a narrow box one at a time. You can turn each shape and move it left or right before it lands. When a row is full, it disappears. The game ends when the shapes pile up to the top.

Suppose you knew every shape that will come, in order. Could you plan where to put each one to clear the most rows? This sounds easier than the real game, but it is still hard: no fast method is known, and even a plan that is close to the best is hard to find.

It also turns out that the game cannot go on forever. Some runs of shapes force a loss whatever you do, and in a long random game such a run comes sooner or later.

## Definition

A *board* is a $w \times h$ grid of filled and empty cells. The *pieces* are the seven tetrominoes I, O, T, S, Z, L and J. A piece enters at the top, and while it falls the player may move it left, right or down by one cell, or turn it by 90 degrees, as long as it stays in empty cells. It *lands* when it cannot move down. Every full row is then removed, and the rows above it move down. The game is *lost* when a piece cannot enter or lands partly above row $h$.

**Offline Tetris.** Given a board $B$ and a finite sequence $P = p_1, \ldots, p_n$ of pieces, choose a reachable landing place for each piece in turn. The goals are:

- **Clear.** Can the player clear at least $k$ rows?
- **Survive.** Can the player place all $n$ pieces without losing?
- **Tetrises.** Can the player clear four rows at once at least $k$ times?
- **Height.** Can the player keep the highest filled cell at height at most $k$ at all times?

Each is in NP: a list of landing places is a certificate that can be checked by playing it out. Demaine, Hohenberger and Liben-Nowell (2003) proved all four NP-complete.

## Variants

- **Online Tetris.** The next piece is known only when it enters, sometimes with a preview of one or a few. The player then faces a random or adversarial sequence, a [Markov decision process](/markov-decision-process/) or an [online](/online-algorithm/) game.
- **Adversarial sequence.** Burgiel (1997) showed that on the standard well of 10 columns and 20 rows, a sequence of alternating S and Z pieces always ends the game, within about 70 000 pieces. A sequence of random pieces contains such a run with probability 1, so every random game ends.
- **The width.** In a well whose width is a multiple of 4, alternating S and Z pieces can be played forever, by giving half of the columns to S and half to Z. In a well of odd width, O pieces alone always lose, since each O fills two cells of each row it touches and no row can be filled.
- **Fixed well.** For fixed $w$ and $h$ the board has at most $2^{w h}$ states. A [dynamic program](/dag-dynamic-programming/) over the set of reachable boards after each piece then solves offline Tetris in time linear in $n$. The constant is exponential in $w h$.
- **Other pieces.** The same questions with other polyominoes, or with tiling a fixed region, lead to [polyomino tiling](/polyomino-tiling-problem/) problems.

## Examples

**A small well.** Take a well of 4 columns and 4 rows, and drop pieces straight down with no moves during the fall. A flat I piece fills the bottom row and clears it at once. An O piece in columns 2 and 3 leaves the two bottom rows as `.XX.`. In this well, the sequence S, Z, S, Z, and so on can be played forever. Put every S upright in the left two columns and every Z upright in the right two. After the first S and Z, the bottom row is `.XX.` and the row above it is `X..X`. Each later pair of S and Z fills two rows, which are cleared, and the same two rows are left, so the board repeats forever.

**Odd width.** In a well of 3 or 5 columns, a long run of O pieces always loses: every row gets its cells two at a time, so no row of odd width is ever full, and the pile grows by two rows for every few pieces.

**The reduction.** For an instance $a_1, \ldots, a_{3s}$ of 3-partition with target $T$, Demaine, Hohenberger and Liben-Nowell build a board with $s$ narrow buckets of the same depth, separated by walls, with a lock at the top right. For each $a_i$ the sequence has a short opening, then a run of pieces whose length depends on $a_i$, then a closing, and it places all these pieces in one bucket. Pieces that do not go fully into one bucket leave holes that can never be cleared. A final run of pieces unlocks the board and clears every row exactly when each bucket received numbers with sum $T$, which is a solution to the 3-partition instance.

## Known algorithms

- **Exhaustive search.** For a short sequence, try every landing place of every piece. Each piece has at most $4 w$ landing places for straight drops, so the tree has at most $(4 w)^n$ leaves.
- **Dynamic programming on boards.** Merge equal boards after each piece. This turns the tree into a layered graph whose size is bounded by the number of distinct boards, which is the method for small fixed wells.
- **Heuristic play.** Practical players score each landing place by features of the board, such as the number of holes, the height of the pile and how uneven the top is, and take the best one. The weights can be tuned by search or by reinforcement learning. These methods work for the online game, but they give no guarantee.

## Bounds

- **NP-complete** for maximizing cleared rows, pieces placed, or four-row clears, and for minimizing the height (Demaine, Hohenberger and Liben-Nowell 2003). The reduction is from 3-partition, which is [strongly NP-complete](/strong-np-hardness/), so the hardness holds with numbers in unary.
- **Hard to approximate.** For a sequence of $p$ pieces it is NP-hard to approximate the most cleared rows or the most pieces placed within a factor $p^{1 - \varepsilon}$, and the least height within a factor $2 - \varepsilon$, for any $\varepsilon > 0$ (Breukelaar et al. 2004). See [approximation thresholds](/approximation-threshold/).
- **Fixed well.** Linear in $n$ with a constant of order $2^{w h}$ times the work per board.
- **Online.** On the standard well, no strategy survives every sequence, by Burgiel's alternating S and Z argument.

## Reductions

- **From 3-partition.** The buckets of the board hold the three numbers of each part, and the depth of each bucket matches the target sum $T$. This is a [gadget reduction](/gadget-reduction/), with gadgets for each number and a final unlock that pays off only when every bucket is full.
- **Between the goals.** The same construction shows hardness for all four goals at once, since the board is cleared, every piece fits, and the height stays low exactly in the yes case.
- **To graph search.** Offline Tetris is the search for a path through a layered graph of boards. This gives the dynamic program for fixed wells.

## Applications

- **Hardness of familiar games.** Tetris is a standard example of an everyday game whose planning problem is NP-complete, and of a reduction from a strongly NP-complete number problem.
- **Benchmarks for learning and control.** Tetris is a common test problem for reinforcement learning and for approximate dynamic programming, because its state space is huge but the rules are simple.

## References
