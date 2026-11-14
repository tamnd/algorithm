---
tag: CJ581B
kind: algorithm
slug: independent-set-matching
name: Independent set matching
aliases:
- cell matching detailed placement
area: eda/partitioning-floorplanning-and-placement
level: advanced
summary: Picks a set of cells that share no nets and reassigns them to their positions by an optimal bipartite matching of wire length cost.
solves: [detailed-placement]
model: word-ram
complexity:
  vars: {n: the number of cells, k: the size of each independent set, D: "the largest number of pins on the nets of one cell"}
  time: {worst: "O(n (n D + k^2 D + k^3))", average: "O(n (n D + k^2 D + k^3))", best: "O(n (n D + k^2 D + k^3))"}
  space: {extra: "O(n + k^2)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Tung-Chieh Chen, Zhe-Wei Jiang, Tien-Chang Hsu, Hsin-Chen Chen, Yao-Wen Chang]
  note: Independent set matching is a standard move of detailed placement; NTUplace3 (2008) is a well known placer that uses it, and earlier academic placers used matching of cells to slots in similar forms.
prereqs: [detailed-placement, assignment-problem, hungarian-algorithm, independent-set, half-perimeter-wirelength]
see_also: [bipartite-matching, maximum-independent-set, greedy-coloring, abacus-legalization, simulated-annealing-placement, local-search]
sources:
  - paper: doi:10.1109/TCAD.2008.923063
    title: Tung-Chieh Chen, Zhe-Wei Jiang, Tien-Chang Hsu, Hsin-Chen Chen and Yao-Wen Chang, NTUplace3, an analytical placer for large-scale mixed-size designs with preplaced blocks and density constraints, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(7), 1228 to 1240, 2008
    locator: the detailed placement stage, with the matching of independent cells (general locator)
  - paper: doi:10.1145/1353629.1353640
    title: Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Abacus, fast legalization of standard cell circuits with minimal movement, Proceedings of the International Symposium on Physical Design (ISPD), 47 to 53, 2008
    locator: the legal placements that detailed placement starts from (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (detailed placement by local moves; general locator)
---

Independent set matching is a move of [detailed placement](/detailed-placement/). It picks a set of cells of the same width, close to each other, such that no two of them are on a common net, and puts them back onto the same set of positions in the best order. Because the cells share no net, the wirelength of each cell depends only on its own position, so the change of the total [HPWL](/half-perimeter-wirelength/) is a sum of one term per cell and position. The best reassignment is then an [assignment problem](/assignment-problem/), solved exactly by the [Hungarian algorithm](/hungarian-algorithm/) in $O(k^3)$ time for $k$ cells. The placement stays legal, and the HPWL never goes up. The choice of the sets is a greedy [independent set](/independent-set/) in the graph of cells that share nets, so the method is a local search: it reaches a local minimum, not the best placement.

## In plain words

Take a few parts of the same size that are close together, and that are not wired to each other. Lift them off the board, keeping their places empty. Now each part can go back into any of these places. Since the parts are not wired to each other, the cost of putting a part in a place does not depend on where the other parts go.

So write a table: one row per part, one column per place, and in each box the wire length of that part at that place. Choosing one box in each row and each column with the least sum is a classic problem with a fast exact method. Put the parts back that way. Then take the next group.

## The problem

The input is a legal placement of a netlist $H = (C \cup Q, N)$ in rows: cell $i$ has its left edge $x_i$ on a site, its row, and an integer width $W_i$; the fixed pins $Q$ are pads. Every pin is at the center of its cell. Net $e$ has a weight $w_e$, and

$$ \mathrm{WL} = \sum_{e \in N} w_e \, \mathrm{HPWL}(e). $$

The output is a legal placement with a $\mathrm{WL}$ at most that of the input. One step takes a set $S = \{c_1, \ldots, c_k\}$ of cells of the same width with no net that contains two of them, the set of their positions (slots) $s_1, \ldots, s_k$, where $c_a$ is at $s_a$, and finds a permutation $\sigma$ that minimizes $\mathrm{WL}$ when $c_a$ moves to $s_{\sigma(a)}$. For a cell $c$ and a slot $s$ let

$$ \mathrm{cost}(c, s) = \sum_{e \ni c} w_e \, \mathrm{HPWL}(e) \quad \text{with } c \text{ at } s \text{ and every other cell where it is.} $$

## The algorithm

```pseudo id=main
INDEPENDENT-SET-MATCHING(placement, k, window)
L1  repeat for the given number of passes
L2      for each cell c₀ in the order of the rows
L3          S ← [c₀]; for each cell c of width W_{c₀} in the window of c₀, nearest first: if no net has both c and a cell of S, append c to S; stop at k cells
L4          if |S| ≥ 2
L5              s_a ← the position of S[a] for each a
L6              cost[a][b] ← cost(S[a], s_b) for all a, b
L7              σ ← the minimum cost assignment of cost, by the Hungarian algorithm
L8              move each S[a] to s_{σ(a)}
```

Line L3 is a greedy independent set in the graph whose vertices are the cells of width $W_{c_0}$ in the window and whose edges join two cells on a common net. The equal width makes any cell fit into any slot of the set. Line L6 computes $k^2$ costs; each one needs the nets of one cell. Line L7 is an exact solve of the assignment problem. Line L8 moves the cells. The identity is one of the permutations, so the step never makes $\mathrm{WL}$ larger.

## Example

**Three cells in a row.** One row; cells $a$, $b$, $c$ of width 1 at $x = 0, 2, 4$, so their centers are at $\frac12, \frac52, \frac92$, with $y = \frac12$. Three pads on the same line: $P$ at $x = 5$, $Q$ at $x = 0$, $R$ at $x = 3$. The nets $\{a, P\}$, $\{b, Q\}$, $\{c, R\}$ all have weight 1, so no two of the cells share a net. The total is $\frac92 + \frac52 + \frac32 = \frac{17}{2}$. The cost table, from the implementation with Fractions:

| cell | slot $x = 0$ | slot $x = 2$ | slot $x = 4$ |
| --- | --- | --- | --- |
| $a$ (pad at 5) | $\frac92$ | $\frac52$ | $\frac12$ |
| $b$ (pad at 0) | $\frac12$ | $\frac52$ | $\frac92$ |
| $c$ (pad at 3) | $\frac52$ | $\frac12$ | $\frac32$ |

The Hungarian algorithm gives $a \to 4$, $b \to 0$, $c \to 2$ with the cost $\frac12 + \frac12 + \frac12 = \frac32$. The 6 permutations give the totals $\frac{17}{2}$ (the identity), $\frac{19}{2}$, $\frac92$, $\frac{19}{2}$, $\frac32$ and $\frac{11}{2}$, each a sum of three boxes with one in each row and column, and $\frac32$ is the least. The HPWL drops from $\frac{17}{2}$ to $\frac32$. A swap of two cells could not get there in one move: it is a cycle of three.

**Why the cells must share no net.** Cells $a$ at $x = 0$ and $b$ at $x = 5$ share a net of weight 2; $a$ also has a net to a pad at $x = -1$, and $b$ a net to a pad at $x = 7$. The current $\mathrm{WL}$ is $2 \cdot 5 + \frac32 + \frac32 = 13$, and the swap gives 23. The cost table, computed as if the other cell stays put, is $\begin{pmatrix} \frac{23}{2} & \frac{13}{2} \\ \frac{13}{2} & \frac{23}{2} \end{pmatrix}$: in the swapped boxes each cell lands on the slot of the other and the shared net looks short. The table says the swap costs 13 and the identity 23, the wrong way round. So the matching would make the placement worse.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Separable cost.** If no net contains two cells of $S$, then for every permutation $\sigma$ the new wirelength is $\mathrm{WL}_0 + \sum_a \mathrm{cost}(c_a, s_{\sigma(a)})$, where $\mathrm{WL}_0$ is the wirelength of the nets with no pin in $S$. The reason is that a net with a pin on $c_a$ has all its other pins fixed during the step.
- **Best permutation.** So the minimum cost assignment of line L7 gives the least $\mathrm{WL}$ over all $k!$ permutations of the set, and $\mathrm{WL}$ does not go up.
- **Legal.** The cells of $S$ have the same width and only trade their positions, so the set of occupied sites is the same, and the placement stays legal.
- **Termination.** Each pass does $n$ steps; with a bound on the passes it stops.

The step is exact for its set; the method is not exact for detailed placement, because the sets are chosen greedily and the result is a local minimum.

## Complexity

- **One step.** Line L3 looks at the cells of the window, at most $n$ of them, and checks the at most $D$ nets of each against a hash set of the nets of $S$: $O(n D)$. Line L6 computes $k^2$ costs; each one recomputes the HPWL of the nets of one cell, $O(D)$ pins, so $O(k^2 D)$. The Hungarian algorithm costs $O(k^3)$.
- **One pass.** $n$ steps, so $O(n (n D + k^2 D + k^3))$. With a spatial index the window costs its own size instead of $n$, and a pass is close to linear in $n$ for windows of fixed size.
- **Choice of $k$.** The exact solve grows as $k^3$ and the quality gain flattens out, so placers use small sets, around ten cells or less.
- **Space.** The table $O(k^2)$ and the placement $O(n)$.
- **The implementation** uses exact Fractions for HPWL, so the tests compare totals exactly.

## Properties

**What is proved.** Each step gives the best positions for its set among the slots of the set, keeps the placement legal, and never increases $\mathrm{WL}$. Nothing bounds the result against the best detailed placement.

**What is measured.** Placers that use independent set matching in detailed placement, such as NTUplace3, report the HPWL after detailed placement on the ISPD 2005 and 2006 contest benchmarks; the gain of each move is measured there, not proved. The tests here only check the exact claims on small random instances: the separable sum equals the HPWL computed directly, and the Hungarian result equals the best of all 120 permutations of 5 cells.

- **Moves of many cells at once.** A step can carry out any permutation of $k$ cells, a cycle of length $k$ included, which a sequence of improving swaps may not reach.
- **Same width.** Cells of different widths cannot trade slots in this form.
- **Local.** The window keeps the cells close, so the wirelength model of the other nets stays valid and the step stays cheap.

## Variants and improvements

- **Mixed widths.** Allow cells of different widths by letting a slot be a gap of the right size, or by matching inside a row segment with a check of the total width.
- **Other independent sets.** Choose the set by a coloring of the shared-net graph ([greedy coloring](/greedy-coloring/)) and match each color class, so that a whole region is improved in parallel.
- **Other objectives.** Add timing or congestion terms to $\mathrm{cost}(c, s)$; any cost that depends only on the cell and the slot keeps the step exact.
- **Other detailed placement moves.** Global swap, vertical swap, local reordering and single-segment clustering (FastDP) are the moves that ISM is usually combined with; see [detailed placement](/detailed-placement/).

## When to use it

Use independent set matching in detailed placement after [legalization](/placement-legalization/), when many cells of the same width are in the same area, which is common for the most used standard cells. It is exact for its set and fast for small $k$. It cannot change the order of cells of different widths and cannot fix overlap, so it needs a legal input and other moves next to it.

## Pitfalls

- **Shared nets.** The cost is separable only if no net has two cells of the set. Without the check, the matching uses wrong costs and can make the placement worse, as the second example shows.
- **Pin offsets.** With pins at offsets inside the cell, cells of the same width can still have different pin offsets, which is fine, but flipped orientations change the offsets. Compute the cost with the orientation that the slot gives.
- **Large $k$.** The $O(k^3)$ solve and the $k^2$ cost evaluations grow fast: $k = 10$ needs 100 cost evaluations, a swap of two cells needs 4.
- **Ties.** Many permutations can tie, for example when a cell has no nets. Keep the identity on a tie, or the cells move without gain.

## Implementations

## History

Placing objects on slots as an assignment goes back to the [quadratic assignment](/quadratic-assignment-problem/) model of Koopmans and Beckmann (1957), in which the cost of an object depends on where the others go. The restriction to cells that share no nets makes the assignment exact for the wirelength. In academic placers of the 2000s it became a standard move of detailed placement; NTUplace3 by Chen, Jiang, Hsu, Chen and Chang (2008) is a well known placer that uses it, next to cell swapping and reordering.

## References
