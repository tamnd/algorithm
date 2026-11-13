---
tag: G792KA
kind: problem
slug: minesweeper-consistency
name: Minesweeper consistency problem
aliases:
- Minesweeper
area: games-and-search/puzzles
level: advanced
summary: Decide whether some placement of mines in the hidden cells fits all revealed numbers of a Minesweeper board. NP-complete (Kaye 2000); finding a safe cell is coNP-complete.
prereqs: [constraint-satisfaction-problem, np-complete, co-np-complete]
see_also: [sat, circuit-sat, boolean-circuit, model-counting, counting-csp, nurikabe-problem, nonogram-problem, undecidability]
sources:
  - paper: doi:10.1007/BF03025367
    title: Richard Kaye, Minesweeper is NP-complete, The Mathematical Intelligencer 22(2), 2000, 9 to 15
    locator: the reduction from circuit satisfiability with wire, splitter, crossover and logic gate gadgets
  - paper: doi:10.1007/s00283-011-9256-x
    title: Allan Scott, Ulrike Stege and Iris van Rooij, Minesweeper may not be NP-complete but is hard nonetheless, The Mathematical Intelligencer 33(4), 2011
    locator: the inference problem that a player faces, and its coNP-completeness
  - paper: "Richard Kaye, Infinite versions of minesweeper are Turing complete, manuscript, University of Birmingham, 2000"
    locator: the undecidability of consistency for infinite boards
---

The Minesweeper consistency problem gives a grid in which some cells are revealed and show a number from 0 to 8, and the other cells are hidden, and asks whether the hidden cells can hold mines so that every revealed number equals the count of mines among its up to eight neighbors. Kaye (2000) proved the problem [NP-complete](/np-complete/) by building [Boolean circuits](/boolean-circuit/) out of Minesweeper patterns. The question a player really faces is different: is a given hidden cell safe in every consistent placement? Scott, Stege and van Rooij (2011) proved this inference problem [coNP-complete](/co-np-complete/).

## In plain words

In the game Minesweeper, some squares of a grid hide mines. When you open a safe square, it shows how many of its eight neighbors hold a mine.

Consistency asks: here is a board with some numbers showing; could the mines be placed so that every number is right? If not, someone made a mistake.

A player wants more: which closed square is surely safe to open? That is a harder kind of question. Both questions have no known fast method for large boards.

A solver looks only at the closed squares next to numbers, splits them into groups that do not touch the same numbers, and tries all mine patterns in each group.

## Definition

The board is an $h \times w$ grid with the king-move neighborhood $N(v)$, at most 8 cells. An *instance* is a partition of the cells into revealed cells $R$ and hidden cells $U$, and a number $n(v) \in \{0, \ldots, 8\}$ for each $v \in R$. A *placement* is a set $M \subseteq U$ of mines. It is *consistent* when

$$|N(v) \cap M| = n(v) \quad \text{for every } v \in R.$$

- **Consistency.** Is there a consistent placement? Kaye's version also allows cells marked as mines, which are fixed members of $M$.
- **Consistency with a total.** Is there a consistent placement with $|M| = T$ for a given total $T$, as in the game?
- **Inference.** Given a board with a consistent placement and a hidden cell $u$, is $u$ free of mines in every consistent placement? Its complement asks for a consistent placement with a mine on $u$, which is a consistency question with one more fixed mine.
- **Probability.** For each hidden cell, the fraction of consistent placements that put a mine on it.

A placement is checked in $O(hw)$ time, so consistency is in [NP](/np/), and inference is in [coNP](/co-np/).

## Variants

- **Infinite boards.** Kaye also considered infinite boards with finitely described patterns and showed that consistency is undecidable there, since the patterns can simulate a Turing machine; see [undecidability](/undecidability/).
- **Fixed mine count.** The game states the total number of mines, which adds one global cardinality constraint. Consistency stays in NP, and the solver below handles it with a binomial weight.
- **Counting.** The number of consistent placements, needed for exact probabilities, is a [model counting](/model-counting/) problem; see also [counting CSPs](/counting-csp/).

## Examples

**The 1-2-1 pattern.** Revealed cells in a row show 1, 2, 1, and the three cells above them are hidden:

```
? ? ?
1 2 1
```

With $a, b, c$ the mines on the hidden cells, the numbers say $a + b = 1$, $a + b + c = 2$ and $b + c = 1$. The second minus the first gives $c = 1$, then $b = 0$ and $a = 1$. So the outer cells hold mines in every consistent placement and the middle cell is safe.

**A forced guess.** Revealed cells 1, 1 below two hidden cells give $a + b = 1$ twice. Both placements are consistent, each hidden cell holds a mine with probability $1/2$, and no cell is safe.

**Inconsistent.** In the board below the 3 has only two hidden neighbors, so no placement fits it. The same holds for the same two hidden cells under 1 and 1 when the total is 0, since each 1 needs a mine.

```
? 3
1 ?
```

## Known algorithms

**Frontier backtracking.** Only the hidden cells next to a number, the *frontier*, are constrained. Join two frontier cells when they share a number; each connected group is an independent CSP with one linear equation per number. Enumerate the placements of each group by backtracking, and after each choice check every number on the chosen cell: its mines must not exceed $n(v)$, and its mines plus its open cells must reach $n(v)$. For each group record, for each mine count $m$, the number of placements with $m$ mines and, per cell, how many of them put a mine on the cell. With a total $T$, combine the groups by a knapsack over their mine counts, and give the $q$ hidden cells off the frontier the factor $\binom{q}{T - s}$ when the frontier holds $s$ mines.

```pseudo id=main
MINESWEEPER-ANALYZE(board, T)
L1  build one equation per number over its hidden neighbors; fail if some n(v) exceeds them
L2  split the frontier into groups that share no equation
L3  for each group, backtrack over its cells in order:
L4      try 0 and then 1 on the next cell
L5      keep the choice only if every equation on the cell can still be met
L6      at a full placement, add it to the count for its number of mines
L7  combine the groups by a knapsack over mine counts, with the binomial weight of the off-frontier cells
L8  if the total weight is 0 then the board is inconsistent; else return the mine probabilities
```

*Correctness.* The equations of two groups share no cell, so the consistent placements of the frontier are exactly the products of consistent placements of the groups. Off-frontier hidden cells appear in no equation, so with a total $T$ the placements with $s$ frontier mines extend in exactly $\binom{q}{T - s}$ ways, and without a total in $2^q$ ways. The backtracking cuts only partial placements in which some equation already has too many mines or too few cells left, which no completion repairs. So the weights count all consistent placements, and the board is consistent exactly when the total weight is positive. A cell is safe exactly when its probability is 0. The time is exponential only in the size of the largest group, and polynomial in the number of groups.

**SAT and CSP.** Each number is a cardinality constraint on its at most 8 neighbors, so the board is a small [CSP](/constraint-satisfaction-problem/) and has a direct [SAT](/sat/) encoding; inference is one SAT call with the cell fixed to a mine. Players use the same reasoning by hand: subtracting one equation from another, as in the 1-2-1 pattern, is Gaussian elimination over the integers, and it finds many safe cells without search.

## Bounds

- **NP-completeness of consistency.** Kaye (2000) reduces [circuit satisfiability](/circuit-sat/). A *wire* is a strip of hidden cells along which the mines can lie in one of two phases, true or false, and the numbers beside the strip force the phase to stay the same along it. Gadgets for bends, splitting a wire, NOT, AND and OR gates and a crossing of two wires are patterns of numbers whose consistent placements realize exactly the gate's truth table. A final cell forces the output wire to true. The board is consistent exactly when the circuit is satisfiable.
- **coNP-completeness of inference.** Scott, Stege and van Rooij (2011) show that deciding whether a hidden cell is determined is coNP-complete, which is the hardness of the decision a player must make.
- **Infinite boards.** Consistency is undecidable (Kaye).
- **Brute force.** $2^{|U|}$ placements, each checked in $O(hw)$ time.

## Reductions

- **From circuit satisfiability.** As above, with planar layout by the crossing gadget.
- **To SAT and to counting.** By the models in Known algorithms; probabilities are ratios of model counts.

## Applications

- **Game play.** Strong Minesweeper programs compute safe cells and exact mine probabilities as above, and when no cell is safe they open the cell with the least chance of a mine.
- **Teaching.** Kaye's reduction shows NP-completeness by circuit gadgets on a familiar game, in the same way as the [gadget reductions](/gadget-reduction/) for other pencil puzzles.

## References
