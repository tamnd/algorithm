---
tag: 4DKME3
kind: algorithm
slug: abacus-legalization
name: Abacus legalization
aliases:
- Spindler Abacus
area: eda/partitioning-floorplanning-and-placement
level: advanced
summary: Spindler, Schlichtmann and Johannes's legalizer that tries each cell in nearby rows and places each row by merging clusters of cells, which minimizes squared moves for a fixed order.
solves: [placement-legalization]
model: real-ram
complexity:
  vars: {n: the number of cells, K: the number of rows, k: the largest number of cells that one row gets, t: the number of rows that a cell tries before line L4 stops the loop}
  time: {worst: "O(n log n + K n k)", average: "O(n log n + t n k)", best: "O(n log n + n)"}
  space: {extra: "O(n + K)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Peter Spindler, Ulf Schlichtmann, Frank M. Johannes]
  note: Abacus was presented at ISPD 2008 as a legalizer that moves already placed cells of a row, unlike Tetris, which never moves a placed cell.
prereqs: [placement-legalization, tetris-legalization, isotonic-regression, pool-adjacent-violators]
see_also: [detailed-placement, simpl-placement, quadratic-programming, kkt-conditions, placement-problem, analytical-placement]
sources:
  - paper: doi:10.1145/1353629.1353640
    title: Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Abacus, fast legalization of standard cell circuits with minimal movement, Proceedings of the International Symposium on Physical Design (ISPD), 47 to 53, 2008
    locator: the algorithm, the procedures PlaceRow, AddCell, AddCluster and Collapse, and the comparison of the movement with Tetris on benchmark circuits
  - paper: doi:10.1287/moor.13.2.330
    title: Michael R. Garey, Robert E. Tarjan and Gordon T. Wilfong, One-processor scheduling with symmetric earliness and tardiness penalties, Mathematics of Operations Research 13(2), 330 to 348, 1988
    locator: the same one-row problem with a fixed order and the linear (not squared) cost, solved in O(n log n) time
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (legalization; general locator)
---

Abacus legalization takes a global placement with overlap and moves every standard cell into a row and onto a site so that no two cells overlap, with a small total squared movement. It belongs to chip design (EDA): it is the step after global placement and before [detailed placement](/detailed-placement/), and it solves the [placement legalization](/placement-legalization/) problem by a heuristic. Like [Tetris legalization](/tetris-legalization/), it takes the cells in order of their $x$ position and puts each in a nearby row. Unlike Tetris, it lets the cells that are already in a row move again: for a fixed order of the cells in a row, its procedure PlaceRow finds the exact minimum of the squared movement by merging *clusters* of abutting cells. This step is the [pool adjacent violators](/pool-adjacent-violators/) algorithm of [isotonic regression](/isotonic-regression/) with two bounds. The choice of the row for each cell is greedy, so the result is legal but not optimal.

## In plain words

Think of beads on the wires of an abacus. Each wire is a row of the chip. Each bead wants to be at its own spot, but beads cannot pass or sit on each other.

Take the beads from left to right. Try a new bead on the wires near its spot. On each wire, slide it in at the right end. If it hits the beads before it, they form a group that moves as one piece, to the place where the group is happiest on average. That place can make the group hit the group before it, and then the two groups join. Keep the wire where the new bead ends nearest to its spot, and go on.

## The problem

The rows $r = 0, \ldots, K - 1$ lie at the heights $y_r = r h$, and each row has the sites $0, 1, \ldots, S - 1$ of width 1. Cell $i$ has an integer width $W_i \ge 1$ in sites, a weight $e_i > 0$ and a global position $(x'_i, y'_i)$ of its lower left corner. A legal placement gives each cell a row $y_i \in \{y_0, \ldots, y_{K-1}\}$ and an integer $x_i$ with $0 \le x_i$ and $x_i + W_i \le S$, and no two cells of the same row overlap. The goal is a legal placement with a small weighted squared movement

$$ \sum_i e_i \left( (x_i - x'_i)^2 + (y_i - y'_i)^2 \right). $$

Inside PlaceRow, the row is the interval $[a, b] = [0, S]$, the cells of the row are $1, \ldots, k$ in a fixed left to right order with $\sum W_j \le b - a$, and PlaceRow solves the quadratic program

$$ \min \sum_{j=1}^{k} e_j (x_j - x'_j)^2 \quad \text{subject to} \quad x_1 \ge a, \quad x_j + W_j \le x_{j+1}, \quad x_k + W_k \le b, $$

with real $x_j$. A *cluster* is a run of cells of the row that abut. It has a total weight $e_c$, a total width $W_c$, a position $x_c$ of its left edge, and the number $q_c = \sum e_j (x'_j - d_j)$, where $d_j$ is the offset of cell $j$ from the left edge of the cluster. The best position of a cluster alone is then $q_c / e_c$.

## The algorithm

```pseudo id=main
ABACUS(cells, K rows of S sites)
L1  sort the cells by x'_i
L2  for each cell i in this order
L3      for each row r in order of |y_r − y'_i|
L4          if some row has a cost already and (y_r − y'_i)^2 ≥ the best cost, then stop the loop over rows
L5          if the cells of r together with i are wider than S, then skip r
L6          place the cells of r followed by i with PLACEROW, as a trial
L7          cost(r) ← (x_i − x'_i)^2 + (y_r − y'_i)^2, with x_i the trial position of i
L8      append i to the row of least cost; if no row had room, stop with failure
L9  for each row: PLACEROW on its cells, round each x_c to the nearest site, and put the cells of each cluster side by side
PLACEROW(cells 1 .. k of the row, in order)
L10 for j ← 1 to k
L11     if there is no cluster, or the last cluster c has x_c + W_c ≤ x'_j, then start a new empty cluster c
L12     add j to c: q_c ← q_c + e_j (x'_j − W_c); e_c ← e_c + e_j; W_c ← W_c + W_j
L13     COLLAPSE(c)
COLLAPSE(c)
L14 x_c ← q_c / e_c
L15 if x_c < a then x_c ← a;  if x_c > b − W_c then x_c ← b − W_c
L16 if c has a cluster c' before it with x_{c'} + W_{c'} > x_c
L17     append c to c' as in L18, remove c, and COLLAPSE(c')
L18 q_{c'} ← q_{c'} + q_c − e_c W_{c'}; e_{c'} ← e_{c'} + e_c; W_{c'} ← W_{c'} + W_c
```

Lines L1 to L8 are the outer loop. Rows are tried in order of their vertical distance, and line L4 stops the loop when no farther row can be better, because the cost of a row is at least $(y_r - y'_i)^2$. The trial cost of line L7 counts only the movement of cell $i$; the other cells of the row may move in the trial too, and that is not counted. Line L9 runs PlaceRow once more on each row with its final cells. Lines L10 to L18 are PlaceRow. In line L12 the new cell sits at the offset $W_c$ (the width before the addition) from the left edge, so its term in $q_c$ is $e_j (x'_j - W_c)$. In line L18 every cell of $c$ gets the extra offset $W_{c'}$, which subtracts $e_c W_{c'}$ from its part of $q$. Line L16 is the merge test: the two clusters overlap.

## Example

**One row.** A row of $S = 9$ sites gets five cells, all of weight 1, in this order:

| cell | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| width $W_j$ | 2 | 1 | 2 | 1 | 2 |
| global $x'_j$ | 1 | 2 | $\frac52$ | 7 | 7 |

The clusters of PlaceRow after each cell, from the implementation with Fractions:

| after cell | clusters (cells at $x_c$) | what happens |
| --- | --- | --- |
| 0 | $\{0\}$ at 1 | a new cluster at $x'_0$ |
| 1 | $\{0, 1\}$ at $\frac12$ | cell 1 wants 2, but cell 0 ends at 3; $q = 1 + 0$, $e = 2$ |
| 2 | $\{0, 1, 2\}$ at $\frac16$ | $q = 1 + (\frac52 - 3) = \frac12$, $e = 3$ |
| 3 | $\{0, 1, 2\}$ at $\frac16$, $\{3\}$ at 7 | the first cluster ends at $\frac{31}{6} \le 7$, so a new cluster |
| 4 | $\{0, 1, 2\}$ at $\frac16$, $\{3, 4\}$ at 6 | $q = 7 + (7 - 1) = 13$, $e = 2$, so $x_c = \frac{13}{2}$, but the row ends at 9 and $W_c = 3$, so $x_c = 6$ |

The cells are at $\frac16, \frac{13}{6}, \frac{19}{6}, 6, 7$ with the squared movement $\frac{13}{6}$, the least for this order. Line L9 rounds $\frac16$ to 0 and keeps 6, so the legal positions are $0, 2, 3, 6, 7$ with the squared movement $\frac94$.

**Two rows, against Tetris.** Two rows of 6 sites at $y = 0$ and $y = 1$, and six cells of weight 1:

| cell | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| width | 1 | 2 | 1 | 2 | 2 | 1 |
| $(x'_i, y'_i)$ | $(1, 0)$ | $(\frac32, 1)$ | $(2, 1)$ | $(\frac52, 1)$ | $(\frac52, 1)$ | $(\frac52, 0)$ |

The trials of Abacus, from the implementation:

| cell | first row tried: trial $x_i$, cost | second row tried | chosen |
| --- | --- | --- | --- |
| 0 | row 0: 1, cost 0 | row 1: stopped by L4 | 0 |
| 1 | row 1: $\frac32$, cost 0 | row 0: stopped by L4 | 1 |
| 2 | row 1: $\frac{11}{4}$, cost $\frac{9}{16}$ | row 0: stopped by L4 | 1 |
| 3 | row 1: $\frac{10}{3}$, cost $\frac{25}{36}$ | row 0: stopped by L4 | 1 |
| 4 | row 1: full (width 7 > 6) | row 0: $\frac52$, cost 1 | 0 |
| 5 | row 0: $\frac{11}{3}$, cost $\frac{49}{36}$ | row 1: 5, cost $\frac{29}{4}$ | 0 |

At the end row 0 holds the cluster $\{0, 4, 5\}$ at $\frac23$ and row 1 the cluster $\{1, 2, 3\}$ at $\frac13$. After rounding, $x = (1, 0, 2, 3, 2, 4)$ and $y = (0, 1, 1, 1, 0, 0)$. The squared movement is 6 and the Manhattan movement is 5. Tetris on the same input gives $x = (1, 1, 2, 3, 3, 5)$ and $y = (0, 1, 0, 1, 0, 0)$, with the squared movement 9 and the Manhattan movement 6: cell 5 must go to $x = 5$, because Tetris cannot push cells 0 and 4 to the left.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **The substitution.** With $u_j = x_j - \sum_{l < j} W_l$ and $t_j = x'_j - \sum_{l < j} W_l$, the row problem becomes: minimize $\sum e_j (u_j - t_j)^2$ subject to $a \le u_1 \le u_2 \le \cdots \le u_k \le b - \sum_l W_l$. That is isotonic regression with a lower and an upper bound. A cluster is a block of equal $u$, its position $q_c / e_c$ is the weighted mean of $t$ over the block, and the merge test of line L16 is the test of a violated order between two blocks.
- **PlaceRow is exact.** After each cell $j$, the clusters are the unique minimum of the problem on the cells $1, \ldots, j$. The proof keeps an invariant on the prefix and suffix means of each cluster and checks the KKT conditions with explicit multipliers.
- **Legal output.** Rounding with $\lfloor x + \frac12 \rfloor$ keeps the clusters apart and inside the row, because it is nondecreasing and commutes with adding an integer. So line L9 gives a legal placement whenever no failure was reported.
- **Failure.** Abacus stops with failure only when cell $i$ is wider than the free width of every row. Inside a row it never fails, because it can move all the cells of the row.
- **The stop of line L4 is safe.** Each later row has a cost of at least its $(y_r - y'_i)^2$, so it cannot be strictly better.

## Complexity

- **PlaceRow.** Each cell starts at most one cluster, and each merge removes one, so a run on $k$ cells does at most $k$ merges and $O(k)$ work, if a cluster stores its first and last cell instead of a list (the cells of a cluster are consecutive in the row order).
- **The outer loop.** Each cell tries at most $K$ rows, and each trial is one PlaceRow on at most $k$ cells. With the sort, the worst case is $O(n \log n + K n k)$, and $k \le n$.
- **In practice.** Line L4 stops after $t$ rows on average, and $t$ is small when the global placement is good. An implementation can keep the clusters of each row and only add cell $i$ to the end and collapse, because PlaceRow on the cells of $r$ followed by $i$ makes the same clusters for the cells of $r$ before it reaches $i$. With this, a trial costs the number of merges it does. The best case, where every trial is a new cluster with no merge and only one row is tried, is $O(n \log n + n)$.
- **Space.** The clusters and the rows: $O(n + K)$.
- **The implementation** uses exact Fractions and runs PlaceRow from the start for each trial, which is simple and in the worst case above.

## Properties

**What is proved.** For a fixed assignment of cells to rows and a fixed order in each row, PlaceRow gives the exact minimum of the squared movement with real positions. Line L9 makes it legal, with each cell at most $\frac12$ from that minimum. No bound relates the result of Abacus to the least movement over all row assignments and orders. The full legalization problem is [NP-hard](/np-hard/) (see [placement legalization](/placement-legalization/)).

**What is measured.** Spindler, Schlichtmann and Johannes report that Abacus moves the cells much less than Tetris (about 30 percent less total movement on their benchmark circuits), with a small extra run time. On 200 random toy instances made with a fixed seed (4 rows of 12 sites, 18 cells of width 1 to 3), the implementations here gave the following. Tetris failed on 84 instances, Abacus on none. On the 116 instances where both succeeded, the mean Manhattan movement was 20.8 for Tetris and 18.9 for Abacus, and the mean squared movement was 24.9 and 18.8. These are toy numbers, not benchmark results.

- **Order kept.** The cells of a row keep the order of their $x'$, because they are added in that order and clusters never pass each other.
- **Stability.** If the global placement is already legal and on sites, every cell gets a new cluster at its own position, and nothing moves.
- **Rows do not interact.** A trial in row $r$ changes only row $r$.

## Variants and improvements

- **Linear movement.** With the cost $\sum e_j |x_j - x'_j|$ instead of the square, the one-row problem with a fixed order is the one-machine scheduling problem with symmetric earliness and tardiness penalties, which Garey, Tarjan and Wilfong solved in $O(n \log n)$ time in 1988. The clusters then sit at a weighted median instead of a weighted mean.
- **Cost of the whole row.** The trial cost of line L7 can count the change of movement of all cells of the row instead of cell $i$ alone. This is more exact and slower.
- **Several sites per cell and mixed heights.** Multi-row cells must take the same $x$ in several rows; extensions of Abacus handle them by placing them first or by coupling the rows.
- **Fixed blocks.** Macros and blockages split a row into segments, and PlaceRow runs on each segment with its own $[a, b]$.
- **Use in a placer.** Placers such as [SimPL](/simpl-placement/) and its successors call a legalizer of this kind at the end of global placement and before [detailed placement](/detailed-placement/).

## When to use it

Use Abacus when the global placement is good and the legalizer must not destroy it: it moves cells less than Tetris and almost never fails while there is room. It needs a fixed order of the cells in each row, which it takes from the global $x$; a legalizer that can swap cells, or the [assignment problem](/assignment-problem/) inside [detailed placement](/detailed-placement/), is needed to change that order. If speed is the only goal and the placement is sparse, [Tetris legalization](/tetris-legalization/) is simpler.

## Pitfalls

- **The order of the offset update.** In line L12 the term uses $W_c$ before the new width is added, and in line L18 it uses $W_{c'}$ before the merge. Updating the width first gives the wrong cluster position.
- **Clamping before the merge test.** The clamp of line L15 must come before the overlap test of line L16, or a cluster can leave the row.
- **Rounding each cell alone.** Rounding the cells of a cluster one by one can make neighbors overlap when the widths are not integers. Round the cluster, then place the cells side by side.
- **Counting only the cell.** The trial cost of line L7 ignores the movement of the other cells of the row. A row can look cheap for cell $i$ while it pushes many other cells. Count the whole row when quality matters more than time.
- **Full rows.** Line L5 checks only the total width. If the row has blockages, check the free width of each segment.

## Implementations

## History

Tetris legalization (Hill, US patent 6,370,673, 2002) puts each cell at the nearest free place and never moves it again. Spindler, Schlichtmann and Johannes presented Abacus at ISPD 2008; the same group made the Kraftwerk2 placer in the same year. Its name comes from the beads of an abacus, which slide on a wire and push each other. The idea of merging adjacent blocks whose order is violated is older: it is the pool adjacent violators algorithm of isotonic regression (Ayer, Brunk, Ewing, Reid and Silverman, 1955). The linear cost version of the one-row problem was solved as a scheduling problem by Garey, Tarjan and Wilfong in 1988.

## References
