---
tag: 69KGGJ
kind: problem
slug: nurikabe-problem
name: Nurikabe problem
aliases:
- Nurikabe
area: games-and-search/puzzles
level: advanced
summary: Shade cells so that each clue gets an island of its size and the shaded sea is connected with no 2 by 2 pool. NP-complete, even with clues 1 and 2 only.
prereqs: [constraint-satisfaction-problem, np-complete, connected-components]
see_also: [sat, circuit-sat, generic-backtracking-algorithm, constraint-propagation, flood-fill, gadget-reduction, minesweeper-consistency, slitherlink-problem]
sources:
  - paper: "Brandon P. McPhail, The Complexity of Puzzles: NP-Completeness Results for Nurikabe and Minesweeper, BA thesis, Reed College, 2003"
    locator: chapter 4, the reduction from circuit satisfiability to Nurikabe
  - paper: "Markus Holzer, Andreas Klein and Martin Kutrib, On the NP-completeness of the Nurikabe pencil puzzle and variants thereof, Proceedings of the 3rd International Conference on Fun with Algorithms (FUN 2004), 77 to 89"
    locator: NP-completeness when all clues are 1 or 2, by the simulation of Boolean gates, and the variants
---

The Nurikabe problem gives a rectangular grid in which some cells hold positive numbers, the clues, and asks which cells to shade. The unshaded cells must split into *islands*, connected groups that each hold exactly one clue and have as many cells as that clue. The shaded cells, the *sea*, must be connected, and no 2 by 2 block may be all shaded. McPhail (2003) proved the problem [NP-complete](/np-complete/) by a reduction from [circuit satisfiability](/circuit-sat/), and Holzer, Klein and Kutrib (2004) proved it stays NP-complete when every clue is 1 or 2.

## In plain words

Some squares of a grid hold numbers. You color other squares black, so that the white squares form islands in a black sea.

Each island holds one number, and the number tells how many squares the island has. Two islands may not touch along a side. All the black squares must link up into one sea, and the sea may not have a solid two by two pool.

A solver uses simple facts. A one is an island by itself, so its neighbors are black. A square between two numbers is black, since otherwise the two islands would join. Then the solver guesses where an island grows and checks that the sea stays in one piece.

For large grids, no method is known that is always fast.

## Definition

The grid has cells $V = \{0, \ldots, h-1\} \times \{0, \ldots, w-1\}$, with two cells adjacent when they share a side. An *instance* is a partial map $\kappa$ from $V$ to the positive integers, the clues. A *solution* is a set $B \subseteq V$ of shaded cells such that

1. no clue cell is shaded: $\operatorname{dom} \kappa \cap B = \emptyset$;
2. each [connected component](/connected-components/) $I$ of $V \setminus B$ contains exactly one clue cell $v$, and $|I| = \kappa(v)$;
3. $B$ is connected;
4. no four cells $\{(r, c), (r+1, c), (r, c+1), (r+1, c+1)\}$ all lie in $B$.

Condition 2 gives $|V \setminus B| = \sum_v \kappa(v)$, so the number of shaded cells is fixed by the clues.

- **Decision.** Does the instance have a solution?
- **Search and uniqueness.** Find one, or decide whether it is unique. Published puzzles have exactly one.

The instance size is $\Theta(hw)$ and the search space is the $2^{hw - |\operatorname{dom} \kappa|}$ shadings of the cells without a clue. A shading is checked in $O(hw)$ time with one [flood fill](/flood-fill/) for the islands and one for the sea, so the problem is in [NP](/np/). As for all pencil puzzles, a board of fixed size is a finite problem, and the hardness results are for the family of all boards.

## Variants

- **Rule variants.** Holzer, Klein and Kutrib also study variants of the rules and show that they remain NP-complete.
- **Small clues.** The problem stays NP-complete when every clue is 1 or 2 (Holzer, Klein and Kutrib).
- **Related shading puzzles.** Light Up, Heyawake and Yin-Yang ask for shadings with other local and connectivity rules, and they have NP-completeness proofs of the same style.

## Examples

**A 5 by 5 puzzle.** The board, with dots for cells without a clue, and its unique solution (# is sea):

```
. . . . .        # # # . .
1 . 1 . .        1 # 1 # .
. . . . 7        # # # # 7
. . 2 . .        # . 2 # .
. . . . .        # # # . .
```

The two 1s are islands by themselves, so all their neighbors are sea, and $(2, 2)$ is sea. The clues sum to 11, so 14 of the 25 cells are sea. The 2 must take one of $(3, 1)$, $(3, 3)$ and $(4, 2)$, and the pool rule and the connectivity of the sea leave one choice for the 2 and one shape for the 7.

**Local deductions.** Each is a consequence of the rules, not of a guess.

- A clue 1 is a whole island, so its neighbors are sea.
- A cell adjacent to two cells of different clued islands is sea, since otherwise the two islands merge.
- An island that has reached its size is walled in by sea.
- A cell that no clued island can reach in the cells it still needs is sea.

## Known algorithms

**Backtracking with propagation.** Keep a partial shading with cells white, sea or unknown. Propagate the local deductions above, and reject the partial shading when a 2 by 2 pool is all sea, an island has two clues, an island is larger than its clue or can no longer grow, a white group without a clue is enclosed by sea, or the sea cells are no longer in one component of sea and unknown cells. Then branch on an unknown cell.

```pseudo id=main
NURIKABE-SOLVE(board)
L1  S ← a stack holding the shading with clue cells white and all other cells unknown
L2  while S is not empty do
L3      pop a partial shading x from S
L4      propagate the deductions on x and test the rules on its fixed part
L5      if x breaks a rule then continue
L6      if no cell of x is unknown then output x if it satisfies all rules; continue
L7      pick an unknown cell a
L8      push x with a shaded, and x with a white
```

*Correctness.* Each deduction in line L4 sets only values that every solution extending $x$ has, and each test rejects only partial shadings that no solution extends, because a rule broken by fixed cells stays broken. Line L8 splits the remaining solutions into two disjoint sets. So by induction on the number of unknown cells, every solution is output once, and line L6 outputs nothing else. The worst case is $2^{hw}$ leaves, and each node costs $O(hw)$ time per round of propagation.

**SAT and CSP models.** A [SAT](/sat/) encoding has one variable per cell for "shaded", a clause per 2 by 2 block, and an encoding of connectivity, which is the hard part: islands are often encoded by giving each white cell the index of its clue and a distance from it, and the sea by a spanning tree with distances. CSP solvers use the same model with a global connectivity constraint, see [constraint-satisfaction-problem](/constraint-satisfaction-problem/).

**Heuristic search.** Ant colony optimization and variable neighborhood search have also been applied to Nurikabe; they find solutions of some puzzles quickly, but they cannot prove that no solution exists.

## Bounds

- **NP-completeness.** McPhail (2003) reduces circuit satisfiability to Nurikabe with gadgets on the grid for wires and gates. Holzer, Klein and Kutrib (2004) give a reduction in which all clues are 1 or 2.
- **Membership.** In NP by the flood fill check above.
- **Brute force.** $2^{hw - k}$ shadings for $k$ clues, each checked in $O(hw)$ time.
- **Fixed size.** A board of fixed size is a finite problem.

## Reductions

- **From circuit satisfiability.** Both proofs build a [Boolean circuit](/boolean-circuit/) on the board, in the style of a [gadget reduction](/gadget-reduction/). A wire is a strip of cells in which small islands have two possible positions, and the choice is the truth value. The islands of one strip must all take the same choice, so the value moves along the wire. Gate gadgets allow a filling exactly when the output value is the gate of the input values, and a final gadget forces the output wire to true. The connectivity of the sea and the pool rule hold for every intended choice, so the board has a solution exactly when the circuit is satisfiable.
- **To SAT and CSP.** By the models in Known algorithms.

## Applications

- **Puzzle design.** Generators place islands, compute the clues, and keep a board when a solver proves the solution unique and can find it by deductions alone.
- **Benchmarks.** Nurikabe tests how SAT and CSP solvers handle connectivity constraints, which are not local.

## References
