---
tag: M7HMAC
kind: algorithm
slug: tetris-legalization
name: Tetris legalization
aliases:
- Hill legalization
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Sorts cells by x and puts each in the nearest free position of any row, greedily like Tetris, fast but with large moves in dense parts.
solves: [placement-legalization]
model: word-ram
complexity:
  vars: {n: the number of cells, K: the number of rows}
  time: {worst: "O(n log n + n K)", average: "O(n log n + n K)", best: "O(n log n + n K)"}
  space: {extra: "O(n + K)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2002
  people: [Dwight Hill]
  note: The method is named after the game, where each falling piece stops at the first free place; it is known from Hill's US patent 6,370,673 of 2002.
prereqs: [placement-legalization, greedy-algorithm]
see_also: [abacus-legalization, detailed-placement, placement-problem, min-cut-placement, simpl-placement, list-scheduling]
sources:
  - paper: "Dwight Hill, Method and system for high speed detailed placement of cells within an integrated circuit design, US patent 6,370,673, 2002"
    locator: the patent that the name Tetris legalization refers to (general locator)
  - paper: doi:10.1145/1353629.1353640
    title: Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Abacus, fast legalization of standard cell circuits with minimal movement, Proceedings of the International Symposium on Physical Design (ISPD), 47 to 53, 2008
    locator: the description of Tetris as the baseline, and the comparison of its movement with Abacus
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (legalization; general locator)
---

Tetris legalization takes a global placement with overlap and moves every standard cell onto a site of a row so that no two cells overlap. It belongs to chip design (EDA): it is the simplest legalizer for the [placement legalization](/placement-legalization/) problem, and many placers use it or a variant after global placement. It sorts the cells by their $x$ position and puts each one, for good, at the cheapest place to the right of the cells already in a row. Each row keeps only a *frontier*, the right end of its last cell. The method is a [greedy algorithm](/greedy-algorithm/): it runs in $O(n \log n + n K)$ time for $n$ cells and $K$ rows and is always legal when it succeeds, but it can move cells far in dense areas, and it can fail while the rows still have room.

## In plain words

Think of the game Tetris turned on its side. Take the parts in order from left to right. For each part, look at every row of the chip. In each row the part can go at its own spot, or just after the last part already there if that one is in the way. Choose the row where the part moves least and put it there. It never moves again.

This is fast and simple. But a part never goes back into a gap to the left of the last part in a row, and parts already placed never make room. So a crowded area pushes parts far to the right.

## The problem

The rows $r = 0, \ldots, K - 1$ lie at the heights $y_r = r h$, and each row has the sites $0, 1, \ldots, S - 1$ of width 1. Cell $i$ has an integer width $W_i \ge 1$ in sites and a global position $(x'_i, y'_i)$ of its lower left corner. A legal placement gives each cell a row $y_i$ and an integer $x_i$ with $0 \le x_i$ and $x_i + W_i \le S$, with no overlap in a row. The goal is a small total movement, here the Manhattan movement $\sum_i |x_i - x'_i| + |y_i - y'_i|$. (The squared movement is also common; only the cost of line L7 changes.)

## The algorithm

```pseudo id=main
TETRIS(cells, K rows of S sites)
L1  sort the cells by x'_i
L2  for each cell i in this order
L3      for each row r
L4          want ← the site nearest to x'_i, clamped to [0, S − W_i]
L5          pos(r) ← max(frontier(r), want)
L6          if pos(r) + W_i > S then skip r
L7          cost(r) ← |pos(r) − x'_i| + |y_r − y'_i|
L8      if no row is left, stop with failure
L9      put i at (pos(r), y_r) for the row r of least cost (the first one on a tie)
L10     frontier(r) ← pos(r) + W_i
```

All frontiers start at 0. Line L4 rounds $x'_i$ to a site (a tie goes to the left) and keeps the cell inside the row. Line L5 is the best site at or after the frontier: the movement $|p - x'_i|$ over the integers $p$ in an interval is least at the clamp of the nearest site. Line L6 skips a row whose frontier leaves no room. Lines L9 and L10 place the cell and move the frontier past it.

## Example

**Too much push.** One row of 10 sites and three cells of width 1, all with $x' = 5$. Tetris puts the first at 5, the second at 6 and the third at 7, a total movement of $0 + 1 + 2 = 3$. The best legal placement is $4, 5, 6$, with the movement $1 + 0 + 1 = 2$. Tetris cannot use site 4, because the first cell was placed before it saw the others.

**Failure with room.** One row of 4 sites, a cell $a$ of width 1 with $x' = 2$, and a cell $b$ of width 2 with $x' = \frac52$. Tetris puts $a$ at 2, so the frontier is 3. Cell $b$ needs the sites 3 and 4, and site 4 does not exist, so Tetris fails, though the sites 0 and 1 are free and the placement $b$ at 0, $a$ at 2 is legal.

**Two rows.** Two rows of 6 sites at $y = 0$ and $y = 1$, and six cells:

| cell | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| width | 1 | 2 | 1 | 2 | 2 | 1 |
| $(x'_i, y'_i)$ | $(1, 0)$ | $(\frac32, 1)$ | $(2, 1)$ | $(\frac52, 1)$ | $(\frac52, 1)$ | $(\frac52, 0)$ |

The candidates of each step, from the implementation with Fractions (frontiers before the step):

| cell | frontiers | row 0: pos, cost | row 1: pos, cost | chosen |
| --- | --- | --- | --- | --- |
| 0 | 0, 0 | 1, 0 | 1, 1 | row 0 at 1 |
| 1 | 2, 0 | 2, $\frac32$ | 1, $\frac12$ | row 1 at 1 |
| 2 | 2, 3 | 2, 1 | 3, 1 | row 0 at 2 (tie) |
| 3 | 3, 3 | 3, $\frac32$ | 3, $\frac12$ | row 1 at 3 |
| 4 | 3, 5 | 3, $\frac32$ | no room | row 0 at 3 |
| 5 | 5, 5 | 5, $\frac52$ | 5, $\frac72$ | row 0 at 5 |

The result is $x = (1, 1, 2, 3, 3, 5)$ and $y = (0, 1, 0, 1, 0, 0)$, with the Manhattan movement 6 and the squared movement 9. Cell 5 wants $x = \frac52$, but the frontier of row 0 is already at 5. [Abacus](/abacus-legalization/) on the same input moves cells 0 and 4 to the left and gets the Manhattan movement 5 and the squared movement 6.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Frontier invariant.** At each step, every cell placed in row $r$ lies in $[0, \text{frontier}(r))$. The new cell starts at or after the frontier, so it overlaps no cell of its row, and it ends at most at $S$ by line L6. So the output is legal.
- **Best in the row.** Line L5 gives the least $|p - x'_i|$ over the integer positions $p$ that start at or after the frontier and end at most at $S$. So each step chooses the cheapest place that the frontiers allow, over all rows.
- **When it fails.** Tetris fails exactly when, for the current cell $i$, every row has $\text{frontier}(r) + W_i > S$. The frontier counts the gaps to its left as used, so this can happen while a row has enough free width in total, as the example shows.

## Complexity

- **Time.** The sort costs $O(n \log n)$. Each cell looks at each row in $O(1)$ time, so the loop costs $O(n K)$. In total $O(n \log n + n K)$. A bound on the number of rows tried, for example only rows within a distance of $y'_i$, gives $O(n \log n + n t)$ for $t$ rows per cell.
- **Space.** The frontiers and the output: $O(n + K)$.
- **The implementation** uses exact Fractions for the costs, so a tie between rows is decided exactly.

## Properties

**What is proved.** The output is legal when Tetris succeeds, each step takes the cheapest place that the current frontiers allow, and the running time is as above. Nothing bounds the movement against the least movement, and Tetris can fail when a legal placement exists. Finding the least movement is [NP-hard](/np-hard/) (see [placement legalization](/placement-legalization/)).

**What is measured.** Spindler, Schlichtmann and Johannes used Tetris as the baseline for Abacus and report that Tetris moves the cells clearly more on their benchmark circuits. On 200 random toy instances made with a fixed seed (4 rows of 12 sites, 18 cells of width 1 to 3, a dense case), the implementation here failed on 84 instances where Abacus did not fail. On the 116 instances where both succeeded, the mean Manhattan movement was 20.8 for Tetris and 18.9 for Abacus. These are toy numbers, not benchmark results.

- **Order kept in a row.** Cells of a row are in the order of their $x'$, because they are placed in that order and each goes after the frontier.
- **Placed cells never move.** This is what makes it fast and what makes it push.
- **Stable on legal input.** If the global placement is already legal and on sites, each cell finds its own position with cost 0, and nothing moves.

## Variants and improvements

- **Free intervals instead of a frontier.** Keep the list of free intervals of each row, and let a cell go into any free gap. This removes the failure of the example and reduces the movement, at the cost of a search in the list.
- **Other sort keys.** Sort by the center $x'_i + W_i / 2$ instead of the left edge, or process from both sides toward the middle with a frontier at each end of a row.
- **Squared or weighted cost.** Use $(x - x'_i)^2 + (y - y'_i)^2$, or weight the movement of cells on critical nets more.
- **Moving placed cells.** [Abacus legalization](/abacus-legalization/) lets the cells of a row move again by merging clusters, which solves the row exactly for a fixed order.
- **Window limits.** Try only rows near $y'_i$, which is what makes the method fast for many rows.

## When to use it

Use Tetris when the global placement is already spread well and speed matters most, for example when a placer legalizes many times to measure the wirelength of a legal placement. For the final legalization of a dense design, use [Abacus](/abacus-legalization/) or a flow-based legalizer, and then [detailed placement](/detailed-placement/). [Min-cut placement](/min-cut-placement/) does not need a legalizer of this kind, because it places cells in rows from the start.

## Pitfalls

- **Ignoring the frontier gaps.** A row with a small total width can still be full for Tetris, because a gap to the left of the frontier is lost. Check failures against the free intervals before calling a design too dense.
- **Rounding at the row ends.** Clamp the nearest site to $[0, S - W_i]$ before the frontier, or a cell near the right end gets a position that runs past the row.
- **Ties.** With floating point costs, a tie between rows is decided by rounding errors. Use exact costs or a fixed tie rule.
- **Sort order of equal $x'$.** Cells with the same $x'$ need a fixed second key, or the result depends on the sort.

## Implementations

## History

The greedy rule is old: it is the same idea as [list scheduling](/list-scheduling/), which puts each job at the earliest free time on some machine. In placement, the name Tetris comes from Hill's US patent 6,370,673 of 2002, and the method became the standard baseline for legalization. Spindler, Schlichtmann and Johannes compared Abacus with it in 2008. Many later legalizers start from its greedy order and add ways to move cells that were placed before.

## References
