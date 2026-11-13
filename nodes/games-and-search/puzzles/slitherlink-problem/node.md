---
tag: 0NPZ8T
kind: problem
slug: slitherlink-problem
name: Slitherlink problem
aliases:
- Slitherlink
- Loop puzzle
area: games-and-search/puzzles
level: advanced
summary: Draw one simple closed loop on the lattice of a grid so that each clued cell has as many loop edges as its clue. NP-complete and ASP-complete.
prereqs: [constraint-satisfaction-problem, np-complete, hamiltonian-cycle-problem]
see_also: [sat, planar-graph, gadget-reduction, parsimonious-reduction, generic-backtracking-algorithm, constraint-propagation, numberlink-problem, nurikabe-problem]
sources:
  - paper: "Takayuki Yato, On the NP-completeness of the Slither Link puzzle, IPSJ SIG Notes 2000-AL-74-4, 2000 (in Japanese)"
    locator: the first NP-completeness proof of Slither Link
  - paper: "Takayuki Yato and Takahiro Seta, Complexity and completeness of finding another solution and its application to puzzles, IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences E86-A(5), 2003, 1052 to 1060"
    locator: the ASP-completeness of Slither Link
  - paper: "Takayuki Yato, Complexity and completeness of finding another solution and its application to puzzles, MS thesis, Graduate School of Science, University of Tokyo, January 2003"
    locator: Section 3.1, Lemma 3.1, Lemma 3.2 and Theorem 3.3, the reduction from Hamiltonian circuit in planar graphs of degree at most 3
  - paper: "Alon Itai, Christos H. Papadimitriou and Jayme Luiz Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 1982, 676 to 686"
    locator: the NP-completeness of Hamiltonian circuit in grid graphs
---

The Slitherlink problem gives a rectangular grid of cells in which some cells hold a clue 0, 1, 2 or 3, and asks for one simple closed loop along the grid lines such that each clued cell has exactly as many of its four sides on the loop as its clue. The loop runs through the lattice points of the grid, and it may not cross or touch itself. Yato (2000) proved that deciding whether a board has a solution is [NP-complete](/np-complete/), and Yato and Seta (2003) proved it ASP-complete by a [parsimonious reduction](/parsimonious-reduction/) from the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) on [planar graphs](/planar-graph/) of degree at most 3.

## In plain words

The board is a grid of dots, and some of the squares between the dots hold a number from zero to three. You draw lines between neighboring dots to make one closed loop. The loop may not cross itself or branch, and it may not split into several loops.

The number in a square tells how many of the four sides of that square the loop uses. A zero means that the loop does not touch the square at all. A three means that the loop goes around three of its sides.

Players solve it with small patterns, such as a three in a corner, and with the rule that there is only one loop.

For large boards, no method is known that is always fast.

## Definition

The board has $h \times w$ cells. Its *lattice* is the grid graph $G_{h,w}$ on the $(h+1)(w+1)$ points $\{0, \ldots, h\} \times \{0, \ldots, w\}$, with an edge between points at distance 1, so it has $E = h(w+1) + w(h+1)$ edges. Each cell $(r, c)$ has four sides, the edges of the unit square with corners $(r, c)$ and $(r+1, c+1)$. An *instance* is a partial map $\kappa$ from cells to $\{0, 1, 2, 3\}$. A *solution* is a set $L$ of edges such that

1. $L$ is the edge set of one simple cycle of $G_{h,w}$: every point has 0 or 2 edges of $L$, and the edges of $L$ are connected and nonempty;
2. every clued cell $x$ has exactly $\kappa(x)$ sides in $L$.

- **Decision.** Does the instance have a solution?
- **Another solution (ASP).** Given one solution, is there a different one?
- **Search and uniqueness.** Find a solution, or decide whether it is unique. Published puzzles have exactly one.

A set of edges is checked in $O(E)$ time, so the problem is in [NP](/np/). The search space is the $2^E$ edge sets. A board of fixed size is a finite problem; the hardness results are for the family of all boards.

**Inside and outside.** By the Jordan curve theorem a simple loop $L$ splits the cells into those inside and those outside, and $L$ is exactly the set of sides between an inside cell and an outside cell or the border. So each loop is the boundary of exactly one set of cells, and a clue $\kappa(x)$ counts the sides of $x$ where the status changes, with the area beyond the border counted as outside. This gives a second model: color the cells inside or outside so that the clues count the changes and the boundary of the inside cells is one simple cycle.

## Variants

- **Other lattices.** Slitherlink is also played on hexagonal and other tilings, with clues up to the number of sides of a cell.
- **Only some clue values.** The Yato and Seta construction uses only the clues 0 and 1, so the problem stays hard with these two values.
- **Related loop puzzles.** Masyu and other loop puzzles ask for one loop with other local rules.

## Examples

**A 4 by 4 puzzle.** Four clues fix the loop. On the left the board, on the right the solution (+ is a lattice point):

```
+   +   +   +   +        +   +   +   +   +
      0                        0
+   +   +   +   +        +---+   +   +   +
                         |   |
+   +   +   +   +        +   +   +---+   +
  2       3              | 2 |   | 3 |
+   +   +   +   +        +   +---+   +   +
              1          |           | 1
+   +   +   +   +        +---+---+---+   +
```

The loop has 14 edges and encloses 6 cells. Among all 9,349 simple loops of the 4 by 4 board, it is the only one that fits the four clues.

**Number of loops.** By the inside and outside view, the loops of an $h \times w$ board are in bijection with the nonempty sets of cells whose boundary is one simple cycle. Enumerating the $2^{hw}$ cell sets gives 1, 13, 213 and 9,349 loops for the $n \times n$ boards with $n = 1, 2, 3, 4$, and 40 loops for the $2 \times 3$ board.

**A local deduction.** A 3 in a corner cell has both of its outer sides on the loop. *Proof.* The corner point of the board lies on exactly two edges, the two outer sides of the cell. The loop uses 0 or 2 edges at each point, so it uses both or neither. If it used neither, the cell would have at most 2 sides on the loop, not 3. $\square$ In the same way a 0 removes all four sides of its cell, and a point with two removed edges out of three has no loop edge at all.

**Even length.** Every loop has an even number of edges, because $G_{h,w}$ is bipartite (color point $(r, c)$ by the parity of $r + c$) and every cycle of a bipartite graph has even length.

## Known algorithms

**Backtracking over edges with propagation.** Each edge is on, off or unknown. Two kinds of local rules propagate: at each point the number of on edges is 0 or 2, and at each clued cell it is the clue. A rule whose count can be reached in only one way fixes all its unknown edges. A global rule removes early loops: a closed cycle of on edges is allowed only when it is the whole answer.

```pseudo id=main
SLITHERLINK-SOLVE(clues)
L1  set all edges unknown and propagate the point and cell rules
L2  S ← a stack with this assignment; while S is not empty, pop an assignment x
L3      if the on edges of x hold a closed cycle and other on edges then continue
L4      if no edge is unknown then output x if its on edges form one loop that fits the clues; continue
L5      pick an unknown edge e
L6      for v in (off, on): let y be x with e set to v
L7          propagate the point and cell rules that contain e, and those reached from them
L8          if no rule is broken then push y onto S
```

*Correctness.* The propagation sets an edge only when every solution that extends the assignment has that value on it: if a rule needs all its unknown edges on, or all off, to reach an allowed count, no other choice satisfies it. A broken rule, or a closed cycle with extra on edges, cannot be repaired by setting more edges, because on edges stay on. Line L6 splits the remaining solutions into two disjoint sets. So every solution is output once, and line L4 outputs nothing else. The worst case is $2^E$ leaves.

Practical solvers add many more patterns (adjacent 3s, diagonal 3s, the parity of loop crossings along a line) and reasoning on the inside and outside colors of cells.

**SAT and CSP models.** A [SAT](/sat/) encoding gives one variable per edge, encodes each point rule and each clue as a small cardinality constraint, and handles the single loop rule either lazily, by adding a clause that forbids each subloop the solver finds, or by an encoding of connectivity. The local part is a [CSP](/constraint-satisfaction-problem/) with constraints of arity at most 4.

## Bounds

- **NP-completeness.** Yato (2000) proved Slitherlink NP-complete. Yato and Seta (2003) proved it ASP-complete, which also gives NP-completeness.
- **The Yato and Seta reduction.** It starts from Hamiltonian circuit on planar graphs of degree at most 3, which is ASP-complete by a reduction of Seta from 3-SAT. Such a graph with $n$ vertices embeds in an $O(n) \times O(n)$ grid in polynomial time. Each grid point becomes a $6 \times 6$ board of cells. A point that is not a vertex gets a gadget that holds either no line or one path between two of its four exits; a vertex gets a gadget with clues 1 inside that forces a path through it. Walls of 0 clues join neighboring gadgets, with an opening only where the embedded graph has an edge. Loops of the board then correspond one to one to Hamiltonian circuits of the graph.
- **Brute force.** $2^E$ edge sets, or $2^{hw}$ inside sets by the inside and outside view, each checked in $O(hw)$ time.

## Reductions

- **From Hamiltonian cycle.** As above. Itai, Papadimitriou and Szwarcfiter (1982) proved Hamiltonian circuit NP-complete in grid graphs, the induced subgraphs of the integer lattice. A Slitherlink loop is a cycle in a grid graph, so this is the natural source problem for loop puzzles; the Yato and Seta proof uses planar graphs of degree at most 3 embedded in the grid instead.
- **To SAT and CSP.** By the models in Known algorithms.

## Applications

- **Puzzle generation.** A generator draws a random loop, writes all clues, and removes clues while a solver still finds a unique solution.
- **Benchmarks.** Slitherlink tests SAT and CSP solvers on a global connectivity constraint with very local clues.

## References
