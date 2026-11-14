---
tag: A010Z6
kind: problem
slug: placement-legalization
name: Placement legalization
aliases:
- legalization
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Move the cells of a global placement into legal sites in rows, without overlap and with little total movement.
prereqs: [placement-problem, np-hard]
see_also: [tetris-legalization, abacus-legalization, detailed-placement, three-partition, bin-packing, assignment-problem, isotonic-regression, min-cost-flow-problem]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (legalization after global placement; general locator)
  - paper: doi:10.1145/1353629.1353640
    title: Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Abacus, fast legalization of standard cell circuits with minimal movement, Proceedings of the International Symposium on Physical Design (ISPD), 47 to 53, 2008
    locator: the movement objective, the one-row problem with a fixed order as a quadratic program, and the comparison with Tetris
  - paper: doi:10.1109/TCAD.2004.836733
    title: Ulrich Brenner and Jens Vygen, Legalizing a placement with minimum total movement, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(12), 1597 to 1613, 2004
    locator: the problem of least total movement, and a legalizer that balances the cell area between regions by a minimum cost flow (general locator)
  - paper: doi:10.1287/moor.13.2.330
    title: Michael R. Garey, Robert E. Tarjan and Gordon T. Wilfong, One-processor scheduling with symmetric earliness and tardiness penalties, Mathematics of Operations Research 13(2), 330 to 348, 1988
    locator: the algorithm in O(n log n) time for a fixed order of the jobs, which is the one-row problem with linear movement
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Appendix, problem SP15 (3-partition, NP-complete in the strong sense)
---

Placement legalization is the step of chip design that takes a global placement, in which the standard cells may overlap and sit between sites, and moves every cell onto a site of a row so that no two cells overlap, with as little movement as possible. It comes after global placement and before [detailed placement](/detailed-placement/) in the flow of the [placement problem](/placement-problem/). The global placement already has a good wirelength, so the legalizer should change it little; the total movement stands in for the wirelength that the movement destroys. The problem is [NP-hard](/np-hard/) in the strong sense, even to decide whether any legal placement exists. It is easy in special cases: one row with a fixed order of cells, or cells all one site wide. This page states the problem; the methods are on the pages of the legalizers.

## In plain words

A global placer puts the parts of a circuit roughly where they should be, but some lie on top of each other and many are not on the grid of allowed places. Legalization slides each part to an allowed place in a row, so that no two parts touch the same place, and moves the parts as little as it can.

If there is plenty of room, this is easy. If the rows are nearly full, it is like packing boxes into shelves of a fixed length, which is hard. Even when the order of the parts in a row is wrong, moving them a little in a better order can be cheaper.

## Definition

**Input.**

- Rows $r = 1, \ldots, K$ at the heights $y_1 < \cdots < y_K$, each with the sites $x = 0, s, 2 s, \ldots$ up to its width $S$, and fixed blockages that no cell may overlap. Below, $s = 1$.
- For each cell $i$ a width $W_i$, a multiple of the site width, the row height $h$, a weight $e_i > 0$, and a global position $(x'_i, y'_i)$ of its lower left corner, from global placement.

**Output.** A legal placement $(x_i, y_i)$: each $y_i$ is a row height, each $x_i$ is a site with $0 \le x_i$ and $x_i + W_i \le S$, the cell does not overlap a blockage, and the intervals $[x_i, x_i + W_i)$ of the cells of a row are pairwise disjoint.

**Objective.** Minimize the total weighted movement

$$ D = \sum_i e_i \, d\bigl( (x_i, y_i), (x'_i, y'_i) \bigr), $$

where $d$ is the Manhattan distance $|x_i - x'_i| + |y_i - y'_i|$, or the squared Euclidean distance $(x_i - x'_i)^2 + (y_i - y'_i)^2$. The page or tool must say which one it uses.

**Feasibility.** The decision version asks whether a legal placement exists at all. A legal placement always fixes a row for each cell and an order of the cells in each row. The rest of the problem, given these two choices, is a small convex program per row.

## Variants

- **Maximum movement.** Minimize $\max_i d$, or bound it by a constant as a constraint, so that no single cell moves far. This protects timing better than the total.
- **Fixed rows and order.** Give the row of each cell and the order in each row. Then the rows are independent, and each is the convex problem: minimize $\sum e_j \, d_j(x_j)$ subject to $x_1 \ge 0$, $x_j + W_j \le x_{j+1}$ and $x_k + W_k \le S$, with real $x_j$. With the squared cost it is [isotonic regression](/isotonic-regression/) with bounds after the shift $u_j = x_j - \sum_{l < j} W_l$. With the linear cost it is one-machine scheduling with earliness and tardiness penalties for a fixed job order.
- **One row, free order.** The order is part of the answer. With the cell as a job of length $W_i$ and due date $x'_i + W_i$, the movement $|x_i - x'_i|$ is the earliness or tardiness of the job, so this is one-machine scheduling with earliness and tardiness costs, with the row ends as limits.
- **Unit cells.** All cells are one site wide, as in a gate array. Each cell takes one site, so a legal placement is an injective map from cells to sites.
- **Mixed heights and macros.** Cells of two or more row heights must take the same $x$ in several adjacent rows, and large macros must be placed or fixed first.
- **Incremental legalization.** After an engineering change, a few cells are new or larger, and the legalizer must move few others. This is the same problem with most cells already legal.

## Examples

**The order matters.** One row of 7 sites and three cells of weight 1: $a$ of width 3 at $x' = 1$, $b$ of width 1 at $x' = \frac32$, and $c$ of width 2 at $x' = 2$. For each of the 6 orders, the least Manhattan movement on integer sites, by enumeration of all positions:

| order | best positions | least movement |
| --- | --- | --- |
| $a, b, c$ | $0, 3, 4$ | $\frac92$ |
| $a, c, b$ | $0, 3, 5$ | $\frac{11}{2}$ |
| $b, a, c$ | $0, 1, 4$ | $\frac72$ |
| $b, c, a$ | $1, 2, 4$ | $\frac72$ |
| $c, a, b$ | $0, 2, 5$ | $\frac{13}{2}$ |
| $c, b, a$ | $0, 2, 3$ | $\frac92$ |

The order of the global $x'$ is $a, b, c$, with the least movement $\frac92$. The orders $b, a, c$ and $b, c, a$ give $\frac72$: the narrow cell $b$ is cheaper to move to the left of the wide cell $a$ than to push past it. A legalizer that keeps the order of $x'$, as [Tetris](/tetris-legalization/) and [Abacus](/abacus-legalization/) do, cannot find them.

**Room is not enough.** Two rows of 5 sites, so the free width is 10. Cells of widths 3, 3, 2, 2 have the total 10 and fit, with $3 + 2$ in each row. Cells of widths 4, 4, 1, 1 also fit, with $4 + 1$ in each row. Cells of widths 3, 3, 3, 1 also have the total 10, but no row holds two cells of width 3, so three cells of width 3 need three rows, and no legal placement exists.

## Known algorithms

- **[Tetris legalization](/tetris-legalization/)** (Hill 2002). Sorts the cells by $x'$ and puts each at the cheapest place after the frontier of a row. $O(n \log n + n K)$; legal when it succeeds; can fail when room exists; no bound on the movement.
- **[Abacus legalization](/abacus-legalization/)** (Spindler, Schlichtmann and Johannes 2008). The same order, but each row is placed exactly for its fixed order by merging clusters. Legal when it succeeds; exact only for the fixed rows and orders; measured to move cells much less than Tetris.
- **Fixed order, linear cost.** Garey, Tarjan and Wilfong (1988) solve the one-row problem with a fixed order in $O(n \log n)$ time.
- **Flow-based legalization.** Brenner and Vygen (2004) first move cell area from overfull regions to free ones by a [minimum cost flow](/min-cost-flow-problem/), then place the rows. Later legalizers use flows or linear programs in the same way.
- **Unit cells.** The [assignment problem](/assignment-problem/) between cells and sites, solved by the [Hungarian algorithm](/hungarian-algorithm/), gives the exact least movement.

The legalizers are compared by their total and maximum movement and by the HPWL after legalization on the ISPD 2005 and 2006 placement contest benchmarks. Those are measurements; only the special cases have proofs.

## Bounds

- **Strongly NP-complete feasibility.** Deciding whether a legal placement exists is NP-complete in the strong sense, already with no blockages, by the reduction from 3-partition below. So no algorithm runs in time polynomial in $n$, $K$ and $S$ unless P = NP, and the least movement is strongly NP-hard, because any algorithm for it would decide feasibility.
- **In NP.** A placement on sites is a certificate of polynomial size, checked in polynomial time.
- **One row.** A legal placement exists if and only if $\sum W_i \le S$ (put the cells side by side from 0), with no blockage in the row.
- **Fixed rows and order.** Polynomial: $O(k)$ per row of $k$ cells for the squared cost with real positions (Abacus PlaceRow, the [pool adjacent violators](/pool-adjacent-violators/) idea), and $O(k \log k)$ for the linear cost (Garey, Tarjan and Wilfong).
- **Unit cells.** Polynomial for any cost per cell and site: the Hungarian algorithm on $n$ cells and $N \ge n$ free sites runs in $O(n^2 N)$ time.

## Reductions

- **From 3-partition.** Given $3m$ positive integers $a_1, \ldots, a_{3m}$ with sum $m B$ and $B/4 < a_j < B/2$ (the [3-partition problem](/three-partition/)), make $m$ rows of $B$ sites and a cell of width $a_j$ for each number, at any global position. A legal placement puts cells of total width at most $B$ in each row, and the total is $m B$, so each row holds width exactly $B$; the bounds on $a_j$ force exactly three cells per row. So a legal placement exists if and only if the numbers split into $m$ triples of sum $B$. The rows have $B$ sites, so the instance has a size polynomial in $m B$. That is allowed because 3-partition is NP-complete in the strong sense: it stays NP-complete when $B$ is at most a polynomial in $m$. This is also the reduction from [bin packing](/bin-packing/).
- **Unit cells to assignment.** With $W_i = 1$, a legal placement is an injective map from cells to free sites, and $D$ is a sum of costs $c(i, \text{site})$. So legalization is a rectangular [assignment problem](/assignment-problem/).
- **Fixed order to isotonic regression.** With fixed rows and orders and the squared cost, the substitution $u_j = x_j - \sum_{l < j} W_l$ turns the constraints into $0 \le u_1 \le \cdots \le u_k \le S - \sum_l W_l$, isotonic regression with bounds on the targets $x'_j - \sum_{l < j} W_l$.
- **To detailed placement.** Legalization keeps the wirelength of the global placement only as far as movement predicts it. [Detailed placement](/detailed-placement/) then improves the wirelength of the legal result directly.

## Applications

- **Every standard cell flow.** Global placers ([analytical](/analytical-placement/), [electrostatics-based](/electrostatics-based-placement/), [SimPL](/simpl-placement/)) produce overlap by design, and legalization turns their output into a placement that routing can use.
- **Inside global placement.** Some placers legalize many times during global placement to measure the wirelength of a legal placement and to steer the next step.
- **Engineering changes and timing fixes.** After [gate sizing](/gate-sizing/) or [buffer insertion](/van-ginneken-buffer-insertion/), larger or new cells overlap their neighbors, and an incremental legalizer fixes the overlap with small movement.

## References
