---
tag: 8BMZ6Z
kind: problem
slug: sliding-tile-puzzle
name: Sliding tile puzzle
aliases:
- 15 puzzle
- Fifteen puzzle
- n-puzzle
- Sliding block puzzle
area: games-and-search/puzzles
level: intro
summary: "Slide numbered tiles into the one empty cell of a w x h board to reach the ordered arrangement; half of all arrangements are solvable, and a shortest solution is NP-hard to find on n x n boards."
prereqs: [state-space, breadth-first-search]
see_also: [sliding-puzzle-solvability, iterative-deepening-a-star, pattern-database, admissible-heuristic, a-star-search, rush-hour-problem, implicit-graph, rubiks-cube-problem]
sources:
  - paper: doi:10.1016/S0747-7171(08)80001-6
    title: "Daniel Ratner and Manfred Warmuth, The (n^2 - 1)-puzzle and related relocation problems, Journal of Symbolic Computation 10(2), 1990"
    locator: "pp. 111-137; a shortest solution is NP-hard to find, and a constant-factor approximation"
  - paper: doi:10.1016/j.tcs.2018.04.031
    title: "Erik D. Demaine and Mikhail Rudoy, A simple proof that the (n^2 - 1)-puzzle is hard, Theoretical Computer Science 732, 2018"
    locator: "pp. 80-84; NP-hardness by a reduction from rectilinear Steiner tree"
  - paper: doi:10.1016/0020-0190(95)00134-X
    title: "Ian Parberry, A real-time algorithm for the (n^2 - 1)-puzzle, Information Processing Letters 56(1), 1995"
    locator: "pp. 23-28; at most 5n^3 moves up to lower-order terms, and lower bounds of n^3 in the worst case and 2n^3/3 on average"
  - paper: "Alexander Reinefeld, Complete solution of the eight-puzzle and the benefit of node ordering in IDA*, Proceedings of the 13th International Joint Conference on Artificial Intelligence (IJCAI-93), 1993"
    locator: "pp. 248-253; the distance of every 8-puzzle state, diameter 31"
  - paper: doi:10.1023/A:1018972901171
    title: "Adrian Brüngger, Ambros Marzetta, Komei Fukuda and Jürg Nievergelt, The parallel search bench ZRAM and its applications, Annals of Operations Research 90, 1999"
    locator: "pp. 45-63; the 15 puzzle needs at most 80 moves"
  - paper: "Richard E. Korf and Peter Schultze, Large-scale parallel breadth-first search, Proceedings of the 20th National Conference on Artificial Intelligence (AAAI-05), 2005"
    locator: "pp. 1380-1385; a complete breadth-first search of the 15 puzzle"
  - paper: doi:10.1145/1455248.1455250
    title: "Richard E. Korf, Linear-time disk-based implicit graph search, Journal of the ACM 55(6), 2008"
    locator: "article 26, pp. 1-40; disk-based breadth-first search of the 15 puzzle"
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: "Richard E. Korf, Depth-first iterative-deepening: an optimal admissible tree search, Artificial Intelligence 27(1), 1985"
    locator: "pp. 97-109; IDA* with Manhattan distance solves 100 random instances of the 15 puzzle"
  - paper: doi:10.1016/0020-0255(92)90070-O
    title: "Othar Hansson, Andrew Mayer and Moti Yung, Criticizing solutions to relaxed models yields powerful admissible heuristics, Information Sciences 63(3), 1992"
    locator: "pp. 207-227; the linear conflict heuristic"
  - paper: doi:10.1016/j.tcs.2005.05.008
    title: "Robert A. Hearn and Erik D. Demaine, PSPACE-completeness of sliding-block puzzles and other problems through the nondeterministic constraint logic model of computation, Theoretical Computer Science 343(1-2), 2005"
    locator: "pp. 72-96; sliding block puzzles with blocks of several sizes are PSPACE-complete"
  - url: "https://oeis.org/A089473"
    locator: "OEIS A089473, the number of 8-puzzle states at each distance"
  - url: "https://oeis.org/A089484"
    locator: "OEIS A089484, the number of 15-puzzle states at each distance, 17 at distance 80"
---

The sliding tile puzzle is a puzzle on a board of $w \times h$ cells holding $wh - 1$ numbered tiles and one empty cell, in which a move slides a tile next to the empty cell into it, and the goal is to put the tiles in order. The $3 \times 3$ board is the 8-puzzle and the $4 \times 4$ board is the 15 puzzle. Exactly half of all arrangements can be solved, by the [sliding puzzle solvability](/sliding-puzzle-solvability/) theorem, and any solvable arrangement of the $n \times n$ board can be solved in $O(n^3)$ moves, but finding a shortest solution is NP-hard (Ratner and Warmuth 1990). The puzzle is the classic test domain of heuristic search: the 8-puzzle needs at most 31 moves and the 15 puzzle at most 80.

## In plain words

Picture a square tray with fifteen numbered tiles and one empty space. You can slide any tile next to the space into it, which moves the space to where the tile was. The goal is to get the tiles back in order, 1 to 15 row by row, with the space in the last corner. Half of all mixed-up trays can never be put in order, and a simple counting rule tells which half. For the other half, a patient method always works: place the first row, then the first column, and shrink the tray. That uses many more moves than needed. Finding the fewest moves is much harder. Computers do it for this tray size by smart search with good guesses of the remaining distance, but for large trays no fast method is known.

## Definition

**Board and arrangements.** The board has $h$ rows and $w$ columns, $N = wh$ cells and $N - 1$ tiles numbered $1, \dots, N - 1$. An arrangement places the tiles and one blank on the cells, one item to a cell, so there are $N!$ arrangements.

**Moves.** A move exchanges the blank with a tile in a cell that shares a side with it. Moves are reversible, and the blank has 2, 3 or 4 possible moves.

**Goal.** Tiles $1, \dots, N - 1$ in reading order, row by row, with the blank in the bottom right corner.

**Problems.**

- *Solvability:* can the goal be reached from a given arrangement?
- *Solution:* find some sequence of moves to the goal.
- *Shortest solution:* find a sequence with the fewest moves. As a decision problem: given arrangements $s, t$ and a number $k$, can $s$ be turned into $t$ in at most $k$ moves?

The [state space](/state-space/) is an undirected [implicit graph](/implicit-graph/) with $N!$ vertices. For $w, h \ge 2$ it has two connected components of $N!/2$ vertices each. It is bipartite, because each move exchanges two items and so changes the parity of the arrangement read as a permutation of $N$ items.

## Variants

- **Board sizes.** The 8-puzzle ($3 \times 3$), the 15 puzzle ($4 \times 4$), the 24-puzzle ($5 \times 5$), the general $(n^2 - 1)$-puzzle, and rectangles $w \times h$.
- **Move metric.** In the single-tile metric used here each tile moved counts as one move. In the multi-tile metric, sliding several tiles of one row or column at once counts as one move.
- **Graphs.** The same puzzle on any graph, with tokens on all vertices but one; Wilson's theorem, on the [solvability](/sliding-puzzle-solvability/) page, says which arrangements are reachable.
- **Sliding block puzzles.** These form a wider class, with blocks of several sizes and shapes and often no numbering, such as the [Rush Hour](/rush-hour-problem/) puzzle. Deciding whether a given block can reach a given place is PSPACE-complete in general (Hearn and Demaine 2005). The $(n^2 - 1)$-puzzle is not in this hard class: its solvability is a parity test, and its shortest-solution problem is in NP, since a shortest solution has $O(n^3)$ moves.

## Examples

**The $2 \times 3$ board.** It has $6!/2 = 360$ solvable arrangements. A full [breadth-first search](/breadth-first-search/) from the goal gives diameter 21, and exactly one arrangement needs 21 moves:

```
4 5 .        1 2 3
1 2 3   ->   4 5 .
```

The $2 \times 4$ board has $8!/2 = 20{,}160$ solvable arrangements and diameter 36.

**The 8-puzzle.** It has $9!/2 = 181{,}440$ solvable arrangements and diameter 31. The number of arrangements at each distance $d$ from the goal is:

| $d$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| count | 1 | 2 | 4 | 8 | 16 | 20 | 39 | 62 | 116 | 152 | 286 | 396 | 748 | 1024 | 1893 | 2512 |

| $d$ | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| count | 4485 | 5638 | 9529 | 10878 | 16993 | 17110 | 23952 | 20224 | 24047 | 15578 | 14560 | 6274 | 3910 | 760 | 221 | 2 |

The two arrangements at distance 31 are

```
8 6 7        6 4 7
2 5 4        8 5 .
3 . 1        3 2 1
```

The mean distance is about 21.97. Over all solvable arrangements the Manhattan distance averages 14.0 and the linear conflict heuristic 15.12, so both stay far below the true distance on average.

**The 15 puzzle.** It has $16!/2 = 10{,}461{,}394{,}944{,}000$ solvable arrangements. Brüngger, Marzetta, Fukuda and Nievergelt showed in 1999 that every one is solvable in at most 80 moves. The complete breadth-first search of Korf and Schultze (2005) confirmed the diameter 80 and found 17 arrangements at distance 80 (OEIS A089484).

## Known algorithms

- **Solvability test.** Count inversions and the row of the blank; see [sliding puzzle solvability](/sliding-puzzle-solvability/). It costs $O(N \log N)$ time, or $O(N)$ by counting cycles.
- **Constructive solution.** Place the first row and then the first column one tile at a time, which leaves an $(n - 1) \times (n - 1)$ puzzle, and finish the last $2 \times 2$ block by rotation. Parberry's real-time version makes at most $5n^3$ moves up to lower-order terms, with $O(1)$ work per move.
- **Exhaustive search.** A breadth-first search from the goal gives the distance of every state. It is easy for the 8-puzzle; for the 15 puzzle it needed a disk-based parallel search (Korf and Schultze 2005, Korf 2008).
- **Heuristic search.** For one instance, [iterative deepening A*](/iterative-deepening-a-star/) or [A*](/a-star-search/) with an [admissible heuristic](/admissible-heuristic/) finds a shortest solution. Korf used IDA* with the Manhattan distance to solve 100 random 15-puzzle instances in 1985. Stronger heuristics are:
  - *Manhattan distance:* the sum over tiles of the row and column distance to the goal cell. Each move changes it by exactly 1, so it is consistent and has the parity of the true distance.
  - *Linear conflict* (Hansson, Mayer and Yung 1992): two tiles in their goal row in the wrong order must pass each other, and one of them must leave the row and come back, which costs 2 more moves. Adding 2 for each tile that must leave its row or column keeps the bound admissible.
  - *[Pattern databases](/pattern-database/):* exact distances for a subset of the tiles, stored in a table.
- **Approximation.** Ratner and Warmuth give a polynomial-time method whose number of moves is within a constant factor of the optimum.

## Bounds

**Number of moves.** On the $n \times n$ board, every solvable arrangement needs at most $5n^3 + O(n^2)$ moves, by Parberry's algorithm, and some need at least $n^3$ minus lower-order terms, so the diameter is $\Theta(n^3)$. The lower bound comes from the Manhattan distance: each move changes it by 1, and in a random arrangement each tile is on average about $2n/3$ cells from its goal, so the average over all arrangements is about $2n^3/3$.

**Exact diameters.** 21 for $2 \times 3$, 36 for $2 \times 4$, 31 for $3 \times 3$ (Reinefeld 1993) and 80 for $4 \times 4$. The diameter of the 24-puzzle is not known.

**Complexity.**

- Solvability is decided in linear time.
- Finding a shortest solution of the $(n^2 - 1)$-puzzle is NP-hard (Ratner and Warmuth 1990); Demaine and Rudoy (2018) gave a simpler proof by a reduction from rectilinear Steiner tree. The decision version is in NP because a solution, if one exists, has $O(n^3)$ moves, so it is NP-complete.
- For sliding block puzzles with blocks of several sizes, reachability is already PSPACE-complete (Hearn and Demaine 2005).

## Reductions

- **To the permutation group.** An arrangement is a permutation of the $N$ items, and the solvable ones with the blank in a fixed cell form a group isomorphic to the alternating group $A_{N-1}$; the [solvability](/sliding-puzzle-solvability/) theorem and its proof use this.
- **From rectilinear Steiner tree.** Demaine and Rudoy map a Steiner tree instance to two arrangements whose move distance encodes the tree length, which shows NP-hardness.
- **Relaxations as heuristics.** Dropping rules gives admissible heuristics: a tile may move onto any neighbour (Manhattan distance), tiles in one line must pass each other (linear conflict), only some tiles matter (pattern databases).
- **Same shape as other puzzles.** Shortest solutions of the [Rubik's cube](/rubiks-cube-problem/) and of the [burnt pancake problem](/burnt-pancake-problem/) are also shortest paths in the Cayley graph of a group, and the same search methods apply.

## Applications

- The standard benchmark of heuristic search since the 1960s: A*, IDA*, pattern databases and disk-based breadth-first search were all tested on it.
- Motion planning of many robots or packages in a crowded grid, the relocation problems that Ratner and Warmuth name.
- Teaching parity arguments and state spaces, since the 8-puzzle is small enough to search in full.

## References
