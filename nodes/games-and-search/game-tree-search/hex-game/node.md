---
tag: S7E34P
kind: problem
slug: hex-game
name: Hex
aliases:
- Hex game winner determination
- generalized Hex
area: games-and-search/game-tree-search
level: advanced
summary: Two players join opposite sides of a rhombus of hexagons; a full board always has exactly one winner. Deciding who wins from a position is PSPACE-complete (Even and Tarjan; Reisch).
prereqs: [perfect-information-game, zermelo-theorem, pspace]
see_also: [strategy-stealing-argument, generalized-geography, solved-game, df-pn, proof-number-search, monte-carlo-tree-search, graphic-matroid, disjoint-set]
sources:
  - paper: doi:10.1080/00029890.1979.11994922
    title: David Gale, The game of Hex and the Brouwer fixed-point theorem, The American Mathematical Monthly 86(10) (1979)
    locator: pp. 818 to 827 (the Hex theorem that a full board has a winner, its proof by a walk along the boundary between the colors, and its equivalence with the Brouwer fixed-point theorem; the history of the game)
  - paper: doi:10.1145/321978.321989
    title: Shimon Even and Robert E. Tarjan, A combinatorial problem which is complete in polynomial space, Journal of the ACM 23(4) (1976)
    locator: pp. 710 to 719 (generalized Hex, the Shannon switching game on the vertices of a graph, is PSPACE-complete)
  - paper: doi:10.1007/BF00288964
    title: Stefan Reisch, Hex ist PSPACE-vollständig, Acta Informatica 15 (1981)
    locator: pp. 167 to 191 (deciding the winner of a Hex position on an n x n board is PSPACE-complete)
  - paper: doi:10.1137/0112059
    title: Alfred Lehman, A solution of the Shannon switching game, Journal of the Society for Industrial and Applied Mathematics 12(4) (1964)
    locator: pp. 687 to 725 (the edge version is solved by a condition on edge-disjoint spanning trees)
  - paper: "\"Solving 8x8 Hex\""
    title: Philip Henderson, Broderick Arneson and Ryan B. Hayward, Solving 8x8 Hex, Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI 2009)
    locator: pp. 505 to 510 (every opening on the 8 x 8 board solved)
  - paper: "\"Solving Hex: Beyond humans\""
    title: Broderick Arneson, Ryan B. Hayward and Philip Henderson, Solving Hex, Beyond humans, Computers and Games 2010, Lecture Notes in Computer Science 6515
    locator: pp. 1 to 10 (9 x 9 Hex, with a winning opening proved)
  - paper: doi:10.1007/978-3-319-09165-5_12
    title: Jakub Pawlewicz and Ryan B. Hayward, Scalable parallel DFPN search, Computers and Games 2013, Lecture Notes in Computer Science 8427
    locator: pp. 138 to 150 (all remaining 9 x 9 openings and one 10 x 10 opening solved by parallel df-pn)
---

Hex is a two-player board game on a rhombus of hexagonal cells, in which Red tries to join the top and bottom sides with a chain of red stones and Blue tries to join the left and right sides with blue stones. The players place one stone per turn, a full board always has exactly one winner, and the [strategy-stealing argument](/strategy-stealing-argument/) shows that the first player has a winning strategy on every empty $n \times n$ board. As a decision problem, *Hex winner determination* asks who wins from a given position with best play; it is PSPACE-complete on $n \times n$ boards (Reisch 1981), and on arbitrary graphs (generalized Hex, Even and Tarjan 1976).

## In plain words

The board is a diamond made of hexagons, like a tilted honeycomb. Red owns the top and bottom edges, Blue owns the left and right edges. Players take turns to put a stone of their color on any empty cell. Stones never move and are never taken.

Red wins with an unbroken path of red cells from the top edge to the bottom edge. Blue wins with a path from left to right.

Hex can never end in a draw. When the board is full, one player has a path, and only one. A red path from top to bottom cuts the board in two, so no blue path can cross it, and if Red has no path, the blue cells along the edge of the red groups form a blue path.

The first player always wins with perfect play. But for large boards, nobody knows how.

## Definition

**The board.** The $n \times n$ Hex board has cells $(r, c)$ with $0 \le r, c < n$. Cell $(r, c)$ is adjacent to the six cells $(r-1, c)$, $(r-1, c+1)$, $(r, c-1)$, $(r, c+1)$, $(r+1, c-1)$, $(r+1, c)$ that lie on the board. Red's sides are row $0$ and row $n-1$; Blue's sides are column $0$ and column $n-1$. The corners $(0, n-1)$ and $(n-1, 0)$ have three neighbors and are the *obtuse* corners, the line between them is the *short diagonal*; the corners $(0,0)$ and $(n-1,n-1)$ have two neighbors and are *acute*.

**The game.** Red moves first. A move puts a stone of the mover's color on an empty cell. A player wins when their stones contain a path of adjacent cells between their two sides. Every play ends after at most $n^2$ moves.

**The problem.** *Hex*: given $n$ and a position (a set of red and of blue cells, with the player to move), does the player to move have a winning strategy?

**Generalized Hex.** Given a graph $G$ with two marked vertices $s$ and $t$, two players alternately claim unclaimed vertices other than $s$ and $t$. The connecting player wins by claiming the vertices of a path from $s$ to $t$; the cutting player wins by preventing it. This is the *Shannon switching game on vertices*. Hex is the case where $G$ is the board graph, with $s$ and $t$ joined to Red's two sides.

**The Hex theorem.** On a full board, exactly one player has a winning path. *At most one*: a red top-to-bottom path and a blue left-to-right path on the plane board would cross, and two paths of hexagons can only cross at a shared cell. *At least one*: add a row of red cells above and below the board and a column of blue cells to its left and right. Start at a corner where a red and a blue border meet, and walk along the edges of the hexagons that have red on one side and blue on the other. At each vertex of the hex grid exactly three cells meet, so the walk always has one way forward and never repeats an edge; it is finite, so it ends at another corner where the borders meet. The red cells along one side of the walk form a connected chain that joins the two red borders, or the blue cells along the other side join the blue borders (Gale 1979). The proof uses that three cells meet at each corner; on a square grid with four-neighbor adjacency both players can fail, and with eight-neighbor adjacency both can succeed.

## Variants

- **Board size.** The common competition size is $11 \times 11$, and larger boards are also played. On boards that are not square, one player has a shorter distance to cover, and the game is no longer fair.
- **The swap rule.** Because the first player wins, tournament Hex uses the *swap rule* (or pie rule): after the first stone, the second player may take that stone as their own and become the first player. The first player must then open with a move that is neither too strong nor too weak.
- **Generalized Hex** on arbitrary graphs, defined above.
- **The Shannon switching game on edges.** Players claim edges instead of vertices. Lehman solved it in 1964: the outcome is decided by whether the graph has a subgraph containing $s$ and $t$ with two edge-disjoint spanning trees, a question in [matroid](/matroid/) theory with a polynomial algorithm. So the edge version is easy and the vertex version is PSPACE-complete.
- **Misère Hex,** where the player who completes a chain loses.

## Examples

**The $2 \times 2$ board.** Red wins by opening in an obtuse corner, say $(0,1)$: this top cell touches both bottom cells $(1,0)$ and $(1,1)$, Blue can take only one, and Red takes the other. The acute corner $(0,0)$ loses: Blue answers $(1,0)$, and then whichever of $(0,1)$ and $(1,1)$ Red takes, Blue takes the other and joins left to right through $(1,0)$.

**Exhaustive search on small boards.** Searching every position gives the winning first moves:

| board | Red wins | winning openings |
|---|---|---|
| $1 \times 1$ | yes | the only cell |
| $2 \times 2$ | yes | the two obtuse corners $(0,1)$ and $(1,0)$ |
| $3 \times 3$ | yes | 5 of 9 cells: the short diagonal $(0,2)$, $(1,1)$, $(2,0)$, and $(1,0)$, $(1,2)$ |
| $4 \times 4$ | yes | 4 of 16 cells: the short diagonal $(0,3)$, $(1,2)$, $(2,1)$, $(3,0)$ |

On $4 \times 4$ the central cells $(1,1)$ and $(2,2)$ lose for the first player, which shows that "play in the center" is not always right.

**Full boards.** All $2^{16} = 65536$ ways to fill the $4 \times 4$ board with the two colors have exactly one winner, as the Hex theorem says. On a full board the numbers of stones need not be equal for this; the theorem is about colorings.

**Larger boards.** All openings on $8 \times 8$ were solved by computer in 2009 (Henderson, Arneson and Hayward), a winning opening on $9 \times 9$ in 2010, and all $9 \times 9$ openings and one $10 \times 10$ opening by 2013 (Pawlewicz and Hayward). $11 \times 11$ is open.

## Known algorithms

- **Win detection.** A chain test is a [depth-first search](/depth-first-search/) over the player's stones from one side, in $O(n^2)$ time. During play, a [disjoint-set](/disjoint-set/) structure that unions each new stone with its neighbors, plus four virtual cells for the sides, updates in near-constant time per move.
- **Exhaustive search** with a [transposition table](/transposition-table/) over positions, as in [winning and losing states](/winning-losing-states/): up to $3^{n^2}$ positions, practical up to $4 \times 4$ in a few seconds of interpreted code, since a win can be proved after one good move per Red turn.
- **Solvers for larger boards** combine search with Hex-specific knowledge: *virtual connections* (groups of cells that a player can join whatever the opponent does) and the pruning of *inferior cells*, whose filling cannot change the outcome. The 2013 results used a parallel version of [df-pn](/df-pn/) ([proof-number search](/proof-number-search/)).
- **Playing programs** for boards that are not solved use [Monte Carlo tree search](/monte-carlo-tree-search/). Hex has no draws, so every random play-out ends with a winner, which suits Monte Carlo methods.

## Bounds

- **Hex is PSPACE-complete** (Reisch 1981): deciding the winner of a given position on an $n \times n$ board is PSPACE-hard, and it is in PSPACE because a play has at most $n^2$ moves, so depth-first [minimax](/minimax/) needs polynomial space.
- **Generalized Hex is PSPACE-complete** (Even and Tarjan 1976), for the vertex game on arbitrary graphs.
- **The empty board.** The first player wins on every empty $n \times n$ board, by the strategy-stealing argument, but the proof gives no strategy and no fast algorithm. The empty-board question has one instance per $n$, so its hardness is not covered by the PSPACE result.
- **Size of the search.** The number of positions is at most $3^{n^2}$, and a full search of the tree has at most $(n^2)!$ plays; already for $11 \times 11$ both are far too large.

## Reductions

- **From formula games to generalized Hex.** Even and Tarjan reduce the evaluation of quantified Boolean formulas ([QSAT](/qsat/)) to the vertex Shannon switching game, with graph gadgets for the variables and the clauses.
- **To Hex boards.** Reisch builds the gadgets from cells of a Hex board, which needs planar gadgets with a fixed geometry, and so shows that Hex positions on $n \times n$ boards are PSPACE-hard.
- **Hex and fixed points.** Gale shows that the Hex theorem implies the two-dimensional Brouwer fixed-point theorem, and that the $d$-dimensional Hex theorem is equivalent to the $d$-dimensional Brouwer theorem. The walk in the Hex theorem is also an algorithm: it finds a winning chain of a full board in time linear in its length.
- **Related games.** [Generalized geography](/generalized-geography/) is another PSPACE-complete game used as a source of reductions; Hex is the vertex form of a connection game, while geography is a path-forming game.

## Applications

- **Strategy stealing.** Hex is the standard example of the [strategy-stealing argument](/strategy-stealing-argument/): no draws, an extra stone never hurts, so the first player wins, with no strategy known.
- **Fixed-point theory.** Gale's proof gives a combinatorial route to the Brouwer fixed-point theorem, and the walk along the color boundary has the same form as the path-following methods for computing fixed points.
- **Game solving.** Hex is a test bed for [proof-number search](/proof-number-search/), [df-pn](/df-pn/) and [Monte Carlo tree search](/monte-carlo-tree-search/), because it has no draws, a simple rule set and a deep tactical structure; it is a [solved game](/solved-game/) for boards up to $9 \times 9$.
- **Teaching PSPACE.** Generalized Hex was one of the first natural games shown PSPACE-complete.

## References
