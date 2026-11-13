---
tag: B6JK8Y
kind: problem
slug: kakuro-problem
name: Kakuro problem
aliases:
- Kakuro
- Cross sums
area: games-and-search/puzzles
level: advanced
summary: Fill the white cells of a grid with digits 1 to 9 so that each run has distinct digits with the given sum. NP-complete and ASP-complete on general boards (Seta 2002).
prereqs: [constraint-satisfaction-problem, np-complete, all-different-constraint]
see_also: [sudoku, sat, subset-sum-problem, global-constraint, constraint-propagation, parsimonious-reduction, one-in-three-sat, nonogram-problem]
sources:
  - paper: "Takahiro Seta, The complexity of CROSS SUM, IPSJ SIG Notes 2002-AL-84, 2002, 51 to 58 (in Japanese)"
    locator: the NP-completeness of Cross Sum, from the author's senior thesis at the University of Tokyo
  - paper: "Takayuki Yato and Takahiro Seta, Complexity and completeness of finding another solution and its application to puzzles, IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences E86-A(5), 2003, 1052 to 1060"
    locator: the ASP-completeness of Cross Sum
  - paper: doi:10.1007/978-3-642-13122-6_31
    title: Oliver Ruepp and Markus Holzer, The computational complexity of the Kakuro puzzle, revisited, Fun with Algorithms (FUN 2010), LNCS 6099, 319 to 330
    locator: a new NP-completeness proof for a more restricted variant, with gadgets found by a SAT solver
---

The Kakuro problem gives a grid of white and black cells and, for each run of white cells in a row or a column, a clue sum, and asks for digits from 1 to 9 in the white cells so that the digits of each run are all different and add up to its clue. A run is a maximal horizontal or vertical segment of white cells, and each white cell lies in one horizontal and one vertical run. Seta (2002) proved that deciding whether a board has a solution is [NP-complete](/np-complete/), and Yato and Seta (2003) proved it ASP-complete, so even the question "is there a second solution?" is hard. A solver treats each run as a sum constraint combined with an [all-different constraint](/all-different-constraint/) and uses the small table of digit sets that each run length and sum allow.

## In plain words

The board looks like a crossword, but the answers are numbers. Each row piece and column piece of white cells has a target number written in the black cell before it. You write a digit from one to nine in every white cell. The digits of each piece must add up to its target, and no digit may appear twice in the same piece.

Players solve it by known facts about sums. Two cells that add to three must hold one and two, and two cells that add to seventeen must hold eight and nine. Where a row piece and a column piece cross, the digit must fit both lists, and that often leaves one choice.

On big boards no method is known that is always fast, even though checking a filled board is easy.

## Definition

A *board* is an $h \times w$ grid whose cells are white or black. A *run* (or *entry*) is a maximal set of white cells that are consecutive in one row, or consecutive in one column. Each white cell lies in exactly one horizontal run and one vertical run. An *instance* gives the board and a clue $\sigma(R) \in \mathbb{Z}_{>0}$ for each run $R$.

A *solution* is a map $x$ from the white cells to $\{1, \ldots, 9\}$ such that, for every run $R$,

$$x(a) \ne x(b) \text{ for distinct } a, b \in R, \qquad \sum_{a \in R} x(a) = \sigma(R).$$

- **Decision.** Does the instance have a solution?
- **Another solution (ASP).** Given one solution, is there a different one?
- **Search and uniqueness.** Find a solution, or decide whether it is unique. Published puzzles have exactly one.

Because the digits in a run are distinct, a run has at most 9 cells and a clue at most $1 + 2 + \cdots + 9 = 45$, so each run has $O(1)$ possible digit sets. The size of an instance is $\Theta(hw)$. The family of all boards is infinite, and the hardness results are about it: a board of a fixed size is a finite problem. Usual rules also ask that each run has at least two cells, and the hardness proofs work under this rule.

## Variants

- **Other digit ranges.** Digits $1, \ldots, m$ for a fixed $m$. With $m = 9$ this is the standard puzzle.
- **Killer Sudoku.** Cages with sums laid over a [Sudoku](/sudoku/) grid; the cage constraint is the Kakuro run constraint.
- **Puzzle design.** Choose clues for a board so that the solution is unique.

## Examples

**The digit table.** A *digit set* of a run is a set of distinct digits with the right size and sum. Every nonempty subset of $\{1, \ldots, 9\}$ has one size and one sum, so over all pairs (length, sum) there are exactly $2^9 - 1 = 511$ digit sets. The pair with the most digit sets is length 4 with sum 20, together with length 5 with sum 25, with 12 sets each. For a run of $k \ge 2$ cells, 34 pairs have a single digit set: the sums $k(k+1)/2$ and $k(k+1)/2 + 1$, the sums $45 - (9-k)(10-k)/2$ and one less, and for $k = 8$ all nine sums, for $k = 9$ the sum 45. *Proof for the low end:* the $k$ smallest digits give the least sum $1 + \cdots + k$, and no other set reaches it. A sum one larger needs one element raised by one, and only the largest element $k$ can move, to $k + 1$, without a collision. The high end follows by the map $d \mapsto 10 - d$, which turns a set of sum $s$ into a set of sum $10k - s$. For $k = 8$ the set misses one digit $d$, so its sum $45 - d$ fixes $d$.

**A small puzzle.** The board (white cells as dots) and the clues:

```
. . #       rows:    16, 11, 4
. . .       columns: 17, 10, 4
# . .
```

Row 0 has 2 cells with sum 16, so its digits are $\{7, 9\}$; column 0 has 2 cells with sum 17, so $\{8, 9\}$. The shared cell $(0, 0)$ is therefore 9, which gives $(0, 1) = 7$ and $(1, 0) = 8$. Row 2 and column 2 both have 2 cells with sum 4, so both use $\{1, 3\}$. Row 1 now needs $(1, 1) + (1, 2) = 3$, so its two cells hold $\{1, 2\}$, and $(1, 2) \in \{1, 3\} \cap \{1, 2\}$ is 1. Then $(1, 1) = 2$, column 1 gives $(2, 1) = 10 - 7 - 2 = 1$, and $(2, 2) = 3$. The solution is unique:

```
9 7 #
8 2 1
# 1 3
```

## Known algorithms

**Backtracking with the digit table.** For each run keep the set of used digits, the remaining sum and the number of empty cells. A digit $d$ is a candidate for a cell when $d$ is new in both runs of the cell and, in each run, the remaining sum minus $d$ can be written as a sum of the remaining number of distinct unused digits. This test is a small [subset sum](/subset-sum-problem/) question over at most 9 digits and is memoized. The search fills the cell with the fewest candidates first.

```pseudo id=main
KAKURO-SOLVE(board, σ)
L1  if every white cell is filled then output the filling and return
L2  for each empty cell a: cand(a) ← the digits d new in both runs of a such that each run can still reach its sum
L3  pick the empty cell a with the fewest candidates
L4  for each d ∈ cand(a) do
L5      x(a) ← d, and update the used digits and remaining sums of the two runs of a
L6      KAKURO-SOLVE(board, σ)
L7      undo line L5
```

The search is complete, because line L2 removes only digits that no solution can use: a digit that repeats in a run, or after which a run can no longer reach its sum, appears in no solution of the current partial filling. Each node costs $O(9 W)$ reachability tests for $W$ white cells, and each test is a table lookup after memoization. The worst case is $9^W$ leaves.

**CSP and SAT models.** Each run is one [global constraint](/global-constraint/) "all different with sum $\sigma$". Because a run has at most 9 cells, it can be stored as a table of allowed tuples, and generalized arc consistency on the table is exactly the human technique of intersecting digit sets at a crossing. A [SAT](/sat/) encoding uses 9 Boolean variables per cell, at-most-one and at-least-one clauses per cell, at-most-one clauses for each digit in each run, and one clause set per run that forbids the digit sets with the wrong sum. Integer programming solves the same model with the sum as a linear equation.

## Bounds

- **NP-completeness.** The decision problem on general boards is NP-complete (Seta 2002). It is in NP because a filling is checked in $O(hw)$ time. The hardness proof is a [gadget reduction](/gadget-reduction/) from a satisfiability problem: groups of short runs with clues that allow exactly two fillings carry a truth value along the board, and clause gadgets have a filling exactly when one of their literals is true in the intended way. Yato and Seta (2003) gave a reduction that is [parsimonious](/parsimonious-reduction/) with a polynomial time bijection of solutions, which gives ASP-completeness.
- **Restricted variants.** Ruepp and Holzer (2010) gave a new proof of NP-completeness for a more restricted variant than Seta's, and found some of their gadgets automatically with a SAT solver.
- **Easy cases.** Build the *run graph*: one vertex for each run and one edge for each white cell, between its horizontal and its vertical run. When the run graph is a forest, the CSP is [tree structured](/tree-structured-csp/), and dynamic programming from the leaves solves it in time linear in the number of runs, because each run has at most $9!$ allowed fillings, a constant. Hardness therefore needs cycles of crossing runs.
- **Fixed size.** A board of fixed size is a finite problem with at most $9^{W}$ fillings.

## Reductions

- **From SAT.** As above, by gadgets that carry truth values and test clauses.
- **To CSP and SAT.** By the models in Known algorithms. The run graph is the dual of the [constraint graph](/constraint-graph/) of the CSP: runs are the constraints and cells are the variables, each shared by two constraints.

## Applications

- **Benchmarks for propagation.** Kakuro is a standard example of a global constraint that combines all-different with a sum, and of how table constraints with small arity give strong propagation.
- **Teaching.** The puzzle shows on one page the CSP model, the digit set table as a precomputed constraint, and the effect of the variable order.
- **Puzzle generation.** Generators fill a board, compute the sums, and keep a puzzle when a solver confirms that the solution is unique.

## References
