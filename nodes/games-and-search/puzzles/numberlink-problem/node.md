---
tag: KZXTYY
kind: problem
slug: numberlink-problem
name: Numberlink problem
aliases:
- Flow Free
- Pipe puzzle
- Number link
area: games-and-search/puzzles
level: advanced
summary: Join each pair of equal numbers on a grid by a path of cells, with no two paths sharing a cell. NP-complete, both when the paths must cover every cell and when they need not.
prereqs: [constraint-satisfaction-problem, np-complete, simple-path]
see_also: [sat, parameterized-disjoint-paths, vertex-disjoint-paths, depth-first-search, generic-backtracking-algorithm, slitherlink-problem, hashiwokakero-problem, nurikabe-problem]
sources:
  - paper: doi:10.1145/1061425.1061430
    title: James F. Lynch, The equivalence of theorem proving and the interconnection problem, ACM SIGDA Newsletter 5(3), 1975, 31 to 36
    locator: the NP-completeness of vertex-disjoint paths between terminal pairs in grid graphs
  - paper: doi:10.2197/ipsjjip.23.239
    title: Aaron Adcock, Erik D. Demaine, Martin L. Demaine, Michael P. O'Brien, Felix Reidl, Fernando Sánchez Villaamil and Blair D. Sullivan, Zig-Zag Numberlink is NP-complete, Journal of Information Processing 23(3), 2015, 239 to 245
    locator: the NP-completeness of the variant in which the paths must cover all cells, and the comparison with Lynch and with Kotsuma and Takenaga
  - paper: "Neil Robertson and Paul D. Seymour, Graph minors. XIII. The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 1995, 65 to 110"
    locator: the polynomial algorithm for a fixed number of terminal pairs
---

The Numberlink problem gives an $h \times w$ grid and $k$ pairs of *terminal* cells, shown as equal numbers, and asks for $k$ paths of side-adjacent cells, the $i$-th path joining the two cells of pair $i$, such that no cell lies on two paths. In the *covering* variant, popular as the game Flow Free and called Zig-Zag Numberlink, the paths must also use every cell of the grid. Lynch (1975) proved the non-covering variant [NP-complete](/np-complete/) as a routing problem for circuit layout, and Adcock et al. (2015) proved the covering variant NP-complete. A solver grows the paths one cell at a time and cuts every branch in which some pair can no longer be joined.

## In plain words

Some squares of a grid hold numbers, and each number appears exactly twice. You draw a line from each number to its twin. A line moves from square to square through shared sides, never diagonally.

Two lines may not cross or share a square, and a line may not pass through a third number. In the game Flow Free, the lines must also fill the whole grid.

When there are only a few pairs, a computer can find the lines quickly. When the number of pairs grows with the board, no method is known that is always fast.

## Definition

Let $G_{h,w}$ be the grid graph whose vertices are the cells and whose edges join cells that share a side. An *instance* is $h, w$ and pairs $(s_1, t_1), \ldots, (s_k, t_k)$ of cells, all $2k$ cells distinct. A *solution* is a list of [simple paths](/simple-path/) $P_1, \ldots, P_k$ in $G_{h,w}$ such that

1. $P_i$ starts at $s_i$ and ends at $t_i$;
2. the paths are pairwise vertex-disjoint;
3. in the covering variant, every cell lies on some path.

A list of paths is checked in $O(hw)$ time, so both variants are in [NP](/np/). The terminals are part of the input, and the hardness is for the family of all boards with an unbounded number of pairs.

- **Decision.** Does the instance have a solution?
- **Search and uniqueness.** Find one, or decide whether it is unique. Published puzzles have exactly one, usually in the covering variant.

## Variants

- **Non-covering (Lynch).** Rules 1 and 2. This is vertex-disjoint paths between given pairs in a grid graph, the routing problem of wires on a circuit board.
- **Covering, or Zig-Zag Numberlink (Adcock et al.).** Rules 1 to 3.
- **Fewest corners (Kotsuma and Takenaga 2010).** Each path must have the fewest corners within its homotopy class; Adcock et al. cite this variant as NP-complete by Kotsuma and Takenaga.
- **Fixed number of pairs.** For each fixed $k$, vertex-disjoint paths for $k$ pairs is solvable in polynomial time in any graph by the method of Robertson and Seymour, see [parameterized disjoint paths](/parameterized-disjoint-paths/). For $k = 1$ it is one [depth-first search](/depth-first-search/), and for one pair of terminals with several paths it is [Menger's theorem](/vertex-disjoint-paths/).

## Examples

**A 5 by 5 puzzle.** Five pairs; on the left the terminals, on the right the unique covering solution, each cell marked with the number of its path:

```
. 3 4 . .        3 3 4 4 4
. . . 4 .        3 3 3 4 4
1 . 3 5 .        1 1 3 5 5
5 1 2 2 .        5 1 2 2 5
. . . . .        5 5 5 5 5
```

Path 5 runs from $(2, 3)$ right, down the right edge, along the bottom row, and up to $(3, 0)$. Without the cover rule the same terminals have 4 solutions, so here the cover rule is what makes the answer unique.

**A blocked instance.** On a $3 \times 3$ board, the pairs $(0, 1), (2, 1)$ and $(1, 0), (1, 2)$ have no solution in either variant. *Proof.* The cells $(0, 1)$, $(1, 0)$, $(2, 1)$, $(1, 2)$ are terminals, so the first path can use only the corners and the center $(1, 1)$, and it cannot reach a corner from $(0, 1)$ and continue: each corner's only other neighbor is a terminal of pair 2. So path 1 is $(0, 1), (1, 1), (2, 1)$. Then path 2 must leave $(1, 0)$ through a corner, whose other neighbor is a terminal of pair 1, or through the center, which is taken. $\square$

## Known algorithms

**Backtracking on path heads.** Grow each path from its first terminal. At each step pick the open pair whose head has the fewest possible moves, and try each free neighbor of the head, or the second terminal if it is adjacent. Before branching, check with a flood fill over the free cells that every open pair can still reach its second terminal, and, in the covering variant, that every free cell can still be reached from some open pair.

```pseudo id=main
NUMBERLINK-SEARCH(paths, free)
L1  if every pair is joined then output the paths if the cover rule holds; return
L2  if some open pair cannot reach its target through free cells, or a free cell is out of reach in the covering variant, then return
L3  pick the open pair i whose head has the fewest moves
L4  for each free neighbor or target v of the head of path i do
L5      append v to path i and mark v used
L6      NUMBERLINK-SEARCH(paths, free)
L7      unmark v
L8      remove v from path i
```

*Correctness.* Every solution is found once: it fixes, for the pair chosen at each step, the next cell of that path, and line L4 tries every possible next cell. Line L2 cuts only states with no solution, because cells only leave the free set as the search goes deeper, so a target that is out of reach stays out of reach. The worst case is exponential in $hw$.

**SAT and CSP models.** A [SAT](/sat/) encoding gives each cell one variable per pair for its label, and requires that a terminal has exactly one neighbor with its label and a non-terminal labeled cell exactly two. These local rules allow detached cycles of one label, which the encoding rules out by distance variables or by adding a clause for each cycle found. In the covering variant, every cell must have a label. The model is a [CSP](/constraint-satisfaction-problem/) with neighbor-count constraints.

## Bounds

- **Non-covering variant.** NP-complete (Lynch 1975), for grid graphs with an unbounded number of pairs.
- **Covering variant.** NP-complete (Adcock et al. 2015).
- **Fixed $k$.** Polynomial for each fixed number of pairs, by Robertson and Seymour.
- **Brute force.** Enumerate the simple paths of pair 1, then those of pair 2 on the cells left, and so on. The number of simple paths in a grid grows exponentially in its size.

## Reductions

- **From satisfiability (Lynch).** Lynch reduces satisfiability to the interconnection problem, the routing of terminal pairs by vertex-disjoint paths in a grid; the title of his paper states this equivalence.
- **To the covering variant (Adcock et al.).** A separate reduction is needed, because a solution of the non-covering variant may leave cells empty, and a covering solution must use them all.
- **To SAT and CSP.** By the models in Known algorithms.

## Applications

- **Circuit and board routing.** Joining terminals by disjoint wires on a grid is the problem Lynch studied.
- **Puzzle apps.** Flow Free and similar games generate covering instances with a unique solution and check them with a solver.

## References
