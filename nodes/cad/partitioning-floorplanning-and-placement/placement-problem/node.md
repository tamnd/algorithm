---
tag: YZHF10
kind: problem
slug: placement-problem
name: Placement
aliases:
- VLSI placement
- standard cell placement
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Assign positions to the cells of a netlist in rows of a chip without overlap, so that wire length, timing and routing congestion are small.
prereqs: [hypergraph, half-perimeter-wirelength, np-hard]
see_also: [min-cut-placement, quadratic-placement, analytical-placement, simulated-annealing-placement, placement-legalization, detailed-placement, hypergraph-partitioning, floorplanning]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (the placement problem, its objectives and constraints, global placement, legalization and detailed placement)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267, 1976
    locator: the NP-completeness of minimum bisection and of optimal linear arrangement, the two problems reduced to placement on this page
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on placement (problem formulation and the classes of placement algorithms)
  - paper: "M. A. Breuer, Min-cut placement, Journal of Design Automation and Fault-Tolerant Computing 1(4), 343 to 362, 1977"
    locator: the formulation of placement as repeated partitioning with cut lines
---

Placement is the step of chip design that gives every cell of a netlist a position on the chip. The cells must lie in the placement region, on the rows and sites of a standard cell layout, and must not overlap each other or the fixed blocks. Among the legal placements, one with small total wire length is wanted, usually measured by the [half-perimeter wirelength](/half-perimeter-wirelength/) (HPWL), with limits on the density of cells and on timing. The problem is [NP-hard](/np-hard/) even for unit cells in one row, so every placer in use is a heuristic. This page states the problem; the methods are on the pages of the placers.

## In plain words

A chip is like a city block with long, narrow streets of equal width. The parts of the circuit are houses of the same depth but different widths, and each must stand on one street, with no two houses on the same spot. Some parts must talk to each other through wires. Long wires are slow, use power and fill up the space for wiring.

So you want to put the houses that talk to each other close together. But the space is limited, the houses cannot pile up, and a few points on the edge of the block, the pads, are fixed. Finding the best layout is hard even when all houses are the same size and there is only one street.

## Definition

**Input.**

- A netlist: a [hypergraph](/hypergraph/) $H = (C \cup Q, N)$ with $n = |C|$ movable cells, a set $Q$ of fixed pins (pads, pins of fixed macros), $m = |N|$ nets and $P$ pins in total, and net weights $w_e \ge 0$.
- For each cell $c$ a width $W_c$ and a height $H_c$. For standard cells all heights equal the row height $h$, and widths are multiples of the site width $s$. Each pin has an offset inside its cell.
- A placement region $R$, here a rectangle, with rows at heights $y_1 < \cdots < y_K$, $y_{k+1} - y_k \ge h$, and in each row a set of sites at $x$-coordinates that are multiples of $s$.
- Fixed positions $(x_q, y_q)$ for every $q \in Q$, and fixed rectangles (macros, blockages) that no cell may overlap.

**Output.** A position $(x_c, y_c)$ of the lower left corner of each cell $c \in C$, and possibly an orientation.

**Legality.**

1. Each cell lies inside $R$ and outside every blockage.
2. Each standard cell sits in a row and on a site: $y_c \in \{y_1, \ldots, y_K\}$ and $x_c$ is a site position.
3. No two cells overlap: the open rectangles $(x_c, x_c + W_c) \times (y_c, y_c + H_c)$ are pairwise disjoint.

**Objective.** Minimize the total weighted wirelength

$$ \mathrm{WL} = \sum_{e \in N} w_e \, \mathrm{HPWL}(e), $$

where the HPWL of a net is computed from its pin positions, with pin offsets in the exact form and with every pin at its cell center in the simpler form that global placement uses. The page or tool must say which form it means.

**Further constraints that real flows add.**

- *Density.* Divide $R$ into bins. In each bin $b$ the area of the cells must be at most $\gamma \cdot \mathrm{area}(b)$ for a target density $\gamma \le 1$.
- *Timing.* With a delay model and a clock period, every path must meet its required time, or the objective becomes the worst or the total negative slack (see [timing-driven placement](/timing-driven-placement/)).
- *Routability.* The estimated routing demand at each place must not exceed the routing capacity.

## Variants

- **Global and detailed placement.** Global placement finds rough positions that may overlap a little but satisfy the density bound. [Legalization](/placement-legalization/) moves the cells to legal sites with small displacement, and [detailed placement](/detailed-placement/) improves a legal placement by local moves. Each stage is a problem in its own right.
- **Standard cell, gate array and mixed size.** In a gate array all cells are unit sites, which turns placement into an assignment of cells to grid points. Mixed-size placement adds movable macros much larger than a row.
- **Other wirelength models.** Some placers minimize a quadratic sum over a [clique or star model](/clique-net-model/), or a smooth form such as the [log-sum-exp wirelength](/log-sum-exp-wirelength/), as a means to reduce HPWL. The problem stays defined by HPWL.
- **Fixed order in a row.** If the left-to-right order of the cells in each row is given, the remaining problem is continuous: the constraints $x_{c'} \ge x_c + W_c$ for neighbors and the bounding box form of HPWL make it a [linear program](/linear-programming-problem/), solvable in polynomial time if positions need not be on sites.
- **Floorplanning.** Placement of a few large blocks of free shape is [floorplanning](/floorplanning/), with area as a main objective.

## Examples

**One row, four cells.** Sites at $x = 0, 1, 2, 3$ in one row; unit cells $a, b, c, d$; a pad $P$ at $x = -1$ and a pad $Q$ at $x = 4$; pins at the cell centers. The nets, all of weight 1, are

$$ \{P, a\}, \; \{a, b, c\}, \; \{b, d\}, \; \{c, d, Q\}, \; \{a, d\}. $$

With integer positions, the HPWL of a net is the number of the lines $x = -\frac12, \frac12, \frac32, \frac52, \frac72$ that separate its pins. So the total is the sum over these 5 lines of the number of nets that cross them. The line $x = -\frac12$ is always crossed by $\{P, a\}$, and the line $x = \frac72$ by $\{c, d, Q\}$. For the inner lines, let $S$ be the set of cells to the left.

| line | $\lvert S \rvert$ | best $S$ | nets crossing | least count |
| --- | --- | --- | --- | --- |
| $x = \frac12$ | 1 | $\{a\}$ | $\{a, b, c\}$, $\{a, d\}$ | 2 |
| $x = \frac32$ | 2 | $\{a, b\}$, $\{a, c\}$ or $\{a, d\}$ | three of the five | 3 |
| $x = \frac52$ | 3 | $\{a, b, d\}$ | $\{a, b, c\}$, $\{c, d, Q\}$ | 2 |

So every placement has $\mathrm{WL} \ge 1 + 2 + 3 + 2 + 1 = 9$. The order $a, b, d, c$ meets every line at its least count, so it is optimal with $\mathrm{WL} = 9$. The order $a, d, b, c$ is also optimal. The order $a, b, c, d$ has $\mathrm{WL} = 10$, and the reverse order $d, c, b, a$ has 15, the worst of all 24 orders. This line-by-line view is the idea behind [min-cut placement](/min-cut-placement/).

**Density.** Place 6 unit cells in a $3 \times 2$ array of bins of area 1 with $\gamma = 1$. A global placement that puts all 6 cells in one bin may have small HPWL, but that bin holds 6 times the allowed area, and a legalizer must move 5 cells out, which makes the wirelength larger.

## Known algorithms

None of these has a proved approximation ratio for the placement problem. What each one guarantees is local.

- **[Min-cut placement](/min-cut-placement/)** (Breuer 1977). Bisects the netlist and the region again and again with a hypergraph partitioner. Heuristic; each step minimizes, approximately, the nets crossing one cut line. With [terminal propagation](/terminal-propagation/) the steps see the cells outside the region.
- **[Quadratic placement](/quadratic-placement/).** Minimizes a sum of squared lengths over a clique or star model, a convex problem solved exactly by a sparse linear system. The minimum ignores overlap, so the placer adds spreading forces or partitioning. Heuristic for the placement problem.
- **[Analytical placement](/analytical-placement/)**, [electrostatics-based placement](/electrostatics-based-placement/) and [SimPL](/simpl-placement/). Minimize a smooth wirelength plus a density penalty by gradient methods. Heuristic; the penalty enforces the density bound only approximately.
- **[Force-directed placement](/force-directed-placement/).** Moves cells by spring forces of the nets. Heuristic.
- **[Simulated annealing placement](/simulated-annealing-placement/)** (TimberWolf). Random swaps and moves with a cooling schedule. Converges in probability only with a logarithmic schedule that no placer uses.
- **Legalization and detailed placement.** [Tetris](/tetris-legalization/) and [Abacus](/abacus-legalization/) legalization, and [independent set matching](/independent-set-matching/) for detailed placement. Abacus solves the movement problem of one row exactly for a fixed order.

Placers are compared on benchmark suites, such as the ISPD 2005 and 2006 placement contests, by the HPWL of the legal result, scaled by a density penalty in the 2006 contest.

## Bounds

- **NP-hard.** The decision version (is there a legal placement with $\mathrm{WL} \le K$?) is NP-hard already for unit cells, 2-pin nets and one row, by the linear arrangement reduction below, and also for two blocks of sites, by the bisection reduction. Both use only numbers polynomial in the input size, so the problem is NP-hard in the strong sense.
- **In NP for site grids.** When every cell must sit on a site of a finite grid, a placement is a certificate of polynomial size, so the decision version is NP-complete.
- **Lower bounds used in practice.** The cut-line form gives lower bounds: for a fixed cut line, the number of nets crossing it is at least the least cut of the netlist that puts the right numbers of cells on the two sides. Quadratic and spectral relaxations give other bounds. No known bound is tight on large netlists.

## Reductions

- **From optimal linear arrangement.** Given a graph $G$ on $n$ vertices, make one row of $n$ unit sites, a unit cell per vertex and a 2-pin net per edge. Every legal placement fills all sites, so it is a bijection $\pi$ onto $\{0, \ldots, n - 1\}$, and $\mathrm{WL} = \sum_{\{u, v\} \in E} |\pi(u) - \pi(v)|$. This is the cost of a linear arrangement, and minimizing it is NP-complete (Garey, Johnson and Stockmeyer, 1976).
- **From minimum bisection.** Let $G$ have $n$ vertices ($n$ even) and $m$ edges. Make one row with a left block of $n/2$ unit sites, a blockage of width $D = 2mn$, and a right block of $n/2$ sites, with a unit cell per vertex and a 2-pin net per edge. A placement with $c$ edges across the blockage has $c (D + 1) \le \mathrm{WL} \le c (D + n - 1) + (m - c)(n/2 - 1)$. If $b$ is the bisection width, the placement built from a minimum bisection has $\mathrm{WL} \le b (D + n - 1) + m n/2$, and any placement with $c \ge b + 1$ has $\mathrm{WL} \ge (b + 1)(D + 1)$, which is larger because $D + 1 > b(n - 2) + mn/2$ when $b \le m$. So every optimal placement splits the vertices by a minimum bisection.
- **To hypergraph partitioning.** Cutting the region by a line and asking which cells go to each side, with a capacity per side, is [hypergraph partitioning](/hypergraph-partitioning/) with fixed vertices for the pads. Min-cut placement uses this relation, but it is not a reduction that keeps the optimum.

## Applications

- **Every digital chip.** Placement sits between floorplanning and routing in the physical design flow. Its result fixes most of the wire length, so it decides much of the delay, power and routability of the chip.
- **FPGAs.** Placement assigns logic blocks to the fixed slots of an FPGA, a gate array variant.
- **Printed circuit boards and packages.** Components on a board, with the same wirelength and overlap rules.
- **Related layout problems.** Arranging nodes in a line or on a grid to keep linked nodes close, as in graph drawing, sparse matrix ordering and the facility layout form of the [quadratic assignment problem](/quadratic-assignment-problem/).

## References
