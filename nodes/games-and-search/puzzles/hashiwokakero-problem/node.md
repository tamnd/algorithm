---
tag: BYSQMT
kind: problem
slug: hashiwokakero-problem
name: Hashiwokakero problem
aliases:
- Hashi
- Bridges puzzle
area: games-and-search/puzzles
level: advanced
summary: Join numbered islands by straight bridges, at most two per pair and none crossing, so that each island has its number of bridges and all are connected. NP-complete.
prereqs: [constraint-satisfaction-problem, np-complete, hamiltonian-cycle-problem]
see_also: [sat, b-matching, branch-and-cut, gadget-reduction, generic-backtracking-algorithm, constraint-propagation, slitherlink-problem, numberlink-problem]
sources:
  - paper: doi:10.1016/j.ipl.2009.07.017
    title: Daniel Andersson, Hashiwokakero is NP-complete, Information Processing Letters 109(19), 2009, 1145 to 1146
    locator: the reduction from Hamiltonian circuit in grid graphs
  - paper: "Leandro C. Coelho, Gilbert Laporte, Arinei Lindbeck and Thibaut Vidal, Benchmark instances and branch-and-cut algorithm for the Hashiwokakero puzzle, arXiv:1905.00973, 2019"
    locator: the integer programming model with connectivity cuts, the benchmark set, and NP-completeness without the connectivity rule
  - paper: "Alon Itai, Christos H. Papadimitriou and Jayme Luiz Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 1982, 676 to 686"
    locator: the NP-completeness of Hamiltonian circuit in grid graphs
---

The Hashiwokakero problem gives a rectangular grid in which some cells are *islands*, each with a number from 1 to 8, and asks for *bridges* between islands. A bridge runs straight along a row or a column between two islands with no island between them, at most two bridges join the same pair, no two bridges cross, each island has exactly as many bridges as its number, and all islands are connected by the bridges. Andersson (2009) proved the problem [NP-complete](/np-complete/) by a reduction from the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) on grid graphs. Without the crossing and connectivity rules, the problem is a degree problem on a graph and is solvable in polynomial time; the two global rules make it hard.

## In plain words

Some squares of a grid are islands with numbers. You join islands by bridges. A bridge goes straight across, left to right or up and down, from one island to the next island in that line. Two islands may have one bridge or two bridges between them, but not more.

The number on an island says how many bridges end at it. Bridges may not cross each other. At the end, you must be able to walk from every island to every other island over the bridges.

Players start with islands whose numbers leave no choice, such as an island with only one neighbor. For large boards, no method is known that is always fast.

## Definition

An *instance* is a set $I$ of cells of an $h \times w$ grid with a number $\beta(v) \in \{1, \ldots, 8\}$ for each $v \in I$. A *slot* is a pair $\{u, v\} \subseteq I$ in the same row or column with no island strictly between them; it is a segment of the grid. Let $S$ be the set of slots. The slots form a planar drawing except where a horizontal slot and a vertical slot cross; let $X \subseteq S \times S$ be the crossing pairs. A *solution* is a map $x : S \to \{0, 1, 2\}$ such that

1. $\sum_{s \ni v} x(s) = \beta(v)$ for every island $v$;
2. $x(s) = 0$ or $x(t) = 0$ for every crossing pair $(s, t) \in X$;
3. the graph on $I$ with the slots $\{s : x(s) > 0\}$ is connected.

Each island has at most 4 slots, so $|S| \le 2|I|$ and $\beta(v) \le 8$. A map $x$ is checked in $O(|I| + |X|)$ time, so the problem is in [NP](/np/). The search space is the $3^{|S|}$ maps.

- **Decision.** Does the instance have a solution?
- **Search and uniqueness.** Find one, or decide whether it is unique. Published puzzles have exactly one.

## Variants

- **Without connectivity.** Rules 1 and 2 only. Coelho, Laporte, Lindbeck and Vidal (2019) show that this variant is still NP-complete, by a different reduction, so the crossing rule alone gives hardness.
- **Without crossings and connectivity.** Rule 1 only. This is a perfect [b-matching](/b-matching/) problem with edge capacity 2 on the slot graph, and capacitated b-matching is solvable in polynomial time by reduction to matching.
- **Other bounds.** Some versions allow up to $k$ bridges per slot, with numbers up to $4k$.

## Examples

**A 7 by 7 puzzle.** On the left the islands; on the right the unique solution, with `-` and `|` for one bridge and `=` and `H` for two:

```
1 . 3 . 4 . 4        1 - 3 - 4 = 4
. . . . . . .        . . | . | . H
2 . . . 1 . .        2 . | . 1 . H
. . . . . . .        H . | . . . H
. . . . . . 2        H . | . . . 2
. . . . . . .        H . | . . . .
3 . 2 . . . .        3 - 2 . . . .
```

The 4 in the top right corner has two slots, so it takes two bridges on each. The 1 in the top left corner has one slot. The slot from the 2 at row 2 to the 1 in the middle crosses the bridge from the top 3 to the bottom 2, and it stays empty.

**Why connectivity matters.** Four islands with the number 2 at the corners of a square have three plans that meet rule 1: one bridge on each side, two bridges on the top and bottom sides, or two bridges on the left and right sides. Only the first is connected, so the puzzle has one solution.

**Local deductions.** Each follows from rule 1 and the limit of two bridges per slot.

- An island with $d$ slots and number $2d$ takes two bridges on every slot.
- An island with $d$ slots and number $2d - 1$ takes at least one bridge on every slot: otherwise its slots carry at most $2(d - 1) < 2d - 1$ bridges.
- A slot between two islands with number 1 stays empty unless these are the only two islands, by rule 3: the two islands would form a connected part with no other bridge.

## Known algorithms

**Backtracking with propagation.** Keep for each slot the set of counts it may still take. For each island, a count $k$ survives on a slot when the other slots of the island can still make up $\beta(v) - k$, given their least and greatest possible counts. A slot with a positive count clears all slots that cross it. A branch is cut when the islands cannot be connected even if every slot that may be used is used.

```pseudo id=main
HASHI-SOLVE(islands)
L1  give each slot the counts {0, 1, 2} and propagate the island sums
L2  S ← a stack with this state; while S is not empty, pop a state x
L3      if the slots that may be positive do not connect all islands then continue
L4      if every slot has one count then output x if it satisfies all rules; continue
L5      pick a slot s with the fewest counts left
L6      for each count k of s, largest first: let y be x with s fixed to k, and clear the slots that cross s if k > 0
L7          propagate the island sums from the islands touched
L8          if no island is broken then push y onto S
```

*Correctness.* Propagation removes a count only when no solution extending the state uses it: rule 1 at that island, or rule 2 at a crossing, would fail. The test in line L3 cuts only states with no solution, because using fewer slots never connects more islands. Line L6 splits the solutions by the count of $s$. So every solution is output once. The worst case is $3^{|S|}$ leaves.

**Integer programming.** Coelho, Laporte, Lindbeck and Vidal model rules 1 and 2 as linear constraints on integer variables and add connectivity constraints on demand in a [branch-and-cut](/branch-and-cut/) algorithm. They solve hard instances with up to 400 islands. A [SAT](/sat/) encoding uses two Boolean variables per slot and the same lazy treatment of connectivity.

## Bounds

- **NP-completeness.** Andersson (2009) reduces Hamiltonian circuit in grid graphs, which Itai, Papadimitriou and Szwarcfiter (1982) proved NP-complete, to Hashiwokakero.
- **Without connectivity.** Still NP-complete (Coelho, Laporte, Lindbeck and Vidal 2019).
- **Without crossings and connectivity.** Polynomial, by capacitated b-matching.
- **Brute force.** $3^{|S|} \le 9^{|I|}$ maps, each checked in polynomial time.

## Reductions

- **From Hamiltonian cycle in grid graphs (Andersson).** In outline: each vertex of the grid graph becomes an island, placed so that two vertex islands share a slot exactly when the vertices are adjacent. A vertex with $b$ missing neighbor directions gets the number $2 + b$, and in each missing direction an island with number 1 is added whose only use is a bridge to that vertex. These 1-islands use up the $b$ extra bridges, so each vertex has exactly 2 bridges to other vertices. Two bridges on one slot would close off two vertices from the rest, which connectivity forbids, so the bridges between vertices form a 2-regular connected spanning subgraph: a Hamiltonian cycle.
- **To SAT, CSP and integer programming.** By the models in Known algorithms.

## Applications

- **Benchmarks.** The Coelho et al. benchmark set is a test bed for branch-and-cut with lazy connectivity constraints.
- **Puzzle generation.** A generator builds a connected bridge plan, writes the numbers, and keeps the puzzle when a solver finds one solution.

## References
