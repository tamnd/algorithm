---
tag: KBQ5V3
kind: problem
slug: nesting-problem
name: Irregular nesting problem
aliases:
- nesting
- irregular strip packing
area: cad/cam-and-additive-manufacturing
level: core
summary: Place irregular polygons without overlap on sheets or a strip to minimize waste, as in sheet metal, textile and laser cutting.
prereqs: [bin-packing, strip-packing]
see_also: [no-fit-polygon, bottom-left-fill, cutting-stock-problem, rectangle-packing, three-partition, mixed-integer-programming, genetic-algorithm, simulated-annealing]
sources:
  - paper: doi:10.1016/j.ejor.2006.11.038
    title: Julia A. Bennell and José F. Oliveira, The geometry of nesting problems, a tutorial, European Journal of Operational Research 184(2), 2008, 397 to 415
    locator: the geometric tools (raster methods, direct trigonometry, the no-fit polygon and phi-functions) and the treatment of rotations
  - paper: doi:10.1057/jors.2008.169
    title: Julia A. Bennell and José F. Oliveira, A tutorial in irregular shape packing problems, Journal of the Operational Research Society 60(S1), 2009, S93 to S105
    locator: the problem variants, the solution approaches (constructive, search over orders, search over layouts, exact models)
  - paper: doi:10.1007/s10732-008-9088-9
    title: Matteo Fischetti and Ivan Luzzi, Mixed-integer programming models for nesting problems, Journal of Heuristics 15(3), 2009, 201 to 226
    locator: the MIP model with one binary variable per pair of parts and convex slice of the outside of their no-fit polygon
  - paper: doi:10.1109/FOCS46700.2020.00098
    title: Mikkel Abrahamsen, Tillmann Miltzow and Nadja Seiferth, Framework for ER-completeness of two-dimensional packing problems, FOCS 2020
    locator: the existential theory of the reals completeness of packing with translations when the pieces or the container have curved boundaries
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2, the strong NP-completeness of 3-PARTITION, and problem SR1 (bin packing) in the appendix
  - paper: doi:10.1016/S0377-2217(02)00131-5
    title: Kathryn A. Dowsland, Subodh Vaid and William B. Dowsland, An algorithm for polygon placement using a bottom-left strategy, European Journal of Operational Research 141(2), 2002, 371 to 381
    locator: the bottom-left placement of polygons from no-fit polygons
---

The irregular nesting problem asks for positions of a set of polygonal parts on a sheet or on a strip of material, so that no two parts overlap and as little material as possible is used. It is a placement problem of manufacturing, not of chip design: the parts are the shapes cut from sheet metal, cloth, leather, wood or glass, and the waste is the material left between them. The parts may only translate, or also rotate by a few fixed angles. The problem contains [bin packing](/bin-packing/) and [strip packing](/strip-packing/) of rectangles as special cases, so it is NP-hard in the strong sense. The main geometric tool is the [no-fit polygon](/no-fit-polygon/), which turns "these two parts do not overlap" into "this point is outside a polygon". Practical solvers are heuristics such as [bottom-left fill](/bottom-left-fill/) inside a search over orders, and exact [mixed-integer](/mixed-integer-programming/) models solve only small instances. This page states the problem and its hardness. The algorithms are on their own pages.

## In plain words

A factory cuts parts for a shirt, a car seat or a steel bracket from long rolls or large sheets. The parts have curved and jagged outlines. The material between the parts is thrown away.

The task is to lay out all the parts on the roll so that no two of them overlap, each stays inside the roll, and the roll used is as short as possible. Sometimes a part may be turned upside down or by a quarter turn. Sometimes it may not, for example when the cloth has a grain.

Rectangles are already hard to lay out well. Irregular shapes add a second difficulty: even deciding whether two shapes overlap at given positions needs geometry, and a good layout puts parts into the hollows of other parts.

## Definition

**Input.** A container and a list of parts.

- Parts $P_1, \dots, P_n$, each a polygon (possibly with holes) given by its vertices with rational coordinates, and for each part a finite set $\Theta_i$ of allowed rotation angles. A part needed $k$ times appears $k$ times.
- A container. In the open dimension variant, the main one in the literature, it is the strip $S_L = [0, W] \times [0, L]$ of fixed width $W$ and free length $L$.

**Output.** For each part an angle $\theta_i \in \Theta_i$ and a translation $t_i \in \mathbb{R}^2$. Write $Q_i = R_{\theta_i} P_i + t_i$ for the placed part.

**Constraints.** Every $Q_i \subseteq S_L$, and $\operatorname{int} Q_i \cap \operatorname{int} Q_j = \emptyset$ for $i \ne j$. Parts may touch.

**Objective.** Minimize $L$. Equivalently, maximize the utilization $\sum_i \operatorname{area}(P_i) / (W L)$, since the area of the parts is fixed.

**Decision version.** Given $W$, $L$ and the parts, is there a feasible placement in $S_L$?

With the [no-fit polygon](/no-fit-polygon/) the constraints become point conditions. For each pair with chosen angles, the reference point $t_j$ must lie outside the open set $\operatorname{int} Q'_i \oplus (-\operatorname{int} Q'_j)$ translated by $t_i$ (where $Q'$ is the rotated part before translation), and each $t_i$ must lie in the inner-fit polygon of the strip.

## Variants

- **Sheets.** Fixed sheets of size $W \times L$, and the goal is the least number of sheets, as in [bin packing](/bin-packing/), or the most valuable subset of parts on one sheet, as in the [knapsack problem](/knapsack-problem/). With many copies of a few shapes, it is a [cutting stock problem](/cutting-stock-problem/).
- **Rotations.** No rotation (textiles with a grain or a pattern), a finite set such as $\{0^\circ, 180^\circ\}$ or $\{0^\circ, 90^\circ, 180^\circ, 270^\circ\}$ (sheet metal), or free rotation. The no-fit polygon covers the first two cases. Free rotation needs other tools, for example the phi-functions described in the tutorial of Bennell and Oliveira (2008).
- **Irregular containers.** A hide of leather has an irregular outline and defects that must be avoided. The defects are fixed parts.
- **Spacing.** A cutting process removes a strip of material (the kerf) and parts may need a gap between them. Growing each part by half the gap with an [offset curve](/offset-curve/) reduces this to the plain problem.
- **Rectangles.** When all parts are rectangles that do not rotate, the problem is [strip packing](/strip-packing/) or [rectangle packing](/rectangle-packing/), which have their own pages and their own approximation results.
- **Three dimensions.** Packing parts into the build volume of an additive manufacturing machine is the same problem in space. It is not covered here.

## Examples

**Rotation halves the length.** Let $W = 4$ and take two copies of the right triangle $T$ with vertices $(0, 0)$, $(4, 0)$ and $(0, 2)$, of area $4$.

- Any feasible placement has $L \ge (4 + 4)/4 = 2$, by area.
- With $\Theta = \{0^\circ, 180^\circ\}$: place $T$ at the origin, and turn the second copy by $180^\circ$ and translate it so that its vertices are $(4, 2)$, $(0, 2)$ and $(4, 0)$. The two triangles share the hypotenuse and fill $[0, 4] \times [0, 2]$, so $L = 2$, which meets the area bound and is optimal. The utilization is $100\%$.
- With translations only: each copy is $4$ wide, so in a strip of width $4$ both copies have $x$ offset $0$, and then a copy at height $s$ and a copy at height $s'$ overlap unless $|s - s'| \ge 2$. So $L = 4$ is optimal, and the utilization is $50\%$.

**A rectangle instance.** With unit-height rectangles of widths $5, 4, 3, 3, 2, 2, 1$ in a strip of width $W = 10$, the area bound gives $L \ge 20/10 = 2$, and the rows $\{5, 3, 2\}$ and $\{4, 3, 2, 1\}$ reach it. Finding such a split of the widths into rows of sum exactly $W$ is a partition problem, which is the source of the hardness below.

## Known algorithms

The pages below give each method with what it guarantees. Here is the list, by kind.

- **Exact models.** Fischetti and Luzzi (2009) write the problem with fixed angles as a [mixed-integer program](/mixed-integer-programming/): continuous reference points, and for each pair of parts one binary variable per convex slice of the outside of their no-fit polygon, of which one must be chosen. It is exact, with exponential worst-case time, and is used on small instances.
- **[Bottom-left fill](/bottom-left-fill/).** Places the parts one by one, each at its lowest, then leftmost, feasible point, found with no-fit polygons (Dowsland, Vaid and Dowsland 2002). It is fast. For rectangles sorted by decreasing width it uses at most 3 times the optimal length. For polygons no ratio is proved.
- **Search over orders.** A [genetic algorithm](/genetic-algorithm/), [simulated annealing](/simulated-annealing/) or [tabu search](/tabu-search/) changes the order and the angles of the parts and uses bottom-left fill to decode each order into a layout. These are heuristics. They are compared by measurement, not by proof.
- **Search over layouts.** Other methods fix a length, allow overlaps, and move parts by [local search](/local-search/) to reduce a penalty for overlap. Each time the penalty reaches zero, they shorten the strip and start again. These are also heuristics.
- **Pixel methods.** Some early methods put the parts and the sheet on a grid of cells and forbid shared cells. They are simple, but a part can only move by whole cells, and the grid limits the precision.

What is measured: papers on the heuristics report the best length or utilization on public benchmark instances, most of them collected by the EURO working group on cutting and packing (ESICUP). Such figures compare heuristics with each other. They bound the gap to the optimum only for instances that an exact method has solved. This page gives no figures from them.

## Bounds

- **Strongly NP-hard.** The decision version is NP-hard in the strong sense, already for rectangles of height 1 with no rotation (see Reductions).
- **In NP for polygons and finite rotations.** With polygonal parts, a finite set of angles with rational sines and cosines, and rational input, the decision version is in NP. A certificate chooses the angles and, for each pair of parts, one convex slice of the outside of their no-fit polygon. With these choices all the constraints are linear inequalities in the $t_i$, and a feasible system of linear inequalities has a rational solution of size polynomial in the input, which [linear programming](/linear-programming-problem/) finds. The number of slices per pair is polynomial in the number of vertices, since it is bounded by the size of the no-fit polygon.
- **Curved shapes.** Abrahamsen, Miltzow and Seiferth (2020) proved that deciding whether the pieces fit into a container is complete for the existential theory of the reals for several variants, among them packing with translations when the pieces or the container have curved boundaries. So such variants are not believed to be in NP.
- **Approximation.** For rectangles, the [strip packing](/strip-packing/) page gives algorithms with proved ratios. For general polygons this page gives no approximation ratio, and the heuristics above have none.
- **Area bound.** $L \ge \sum_i \operatorname{area}(P_i) / W$, and $L$ is at least the least height of each single part over its angles. These bounds are the usual way to judge a layout when the optimum is unknown.

## Reductions

**From 3-PARTITION.** An instance of [3-partition](/three-partition/) is $3m$ positive integers $a_1, \dots, a_{3m}$ with sum $mB$ and $B/4 < a_i < B/2$, and it asks for a split into $m$ triples of sum $B$. It is NP-complete in the strong sense (Garey and Johnson 1979). Map it to the decision version with rectangles $a_i \times 1$, no rotation, $W = B$ and $L = m$.

- If the triples exist, put triple $k$ side by side in the row $[0, B] \times [k - 1, k]$.
- Conversely, take a feasible placement. The rectangles have total area $mB$, which is the area of the strip, so they cover the strip up to a set of measure zero. Choose $c \in (0, 1)$ that differs from the fractional part of every $y_i$, and look at the $m$ lines $y = c + k$, $k = 0, \dots, m - 1$. Each rectangle spans an open height interval of length $1$, so it crosses exactly one of these lines. On almost every choice of $c$, each line is covered up to measure zero, so the widths of the rectangles on it add up to at least $B$. They add up to at most $B$ since the rectangles do not overlap, so each line carries a set of widths of sum exactly $B$, and by $B/4 < a_i < B/2$ each such set is a triple.

The map takes polynomial time, and the numbers in the new instance are bounded by a polynomial in the size and the largest number of the 3-PARTITION instance. Since 3-PARTITION is NP-complete in the strong sense, the nesting problem is NP-hard in the [strong sense](/strong-np-hardness/). The same map with $m$ sheets of size $B \times 1$ shows the hardness of the sheet variant.

**To mixed-integer programming.** The Fischetti and Luzzi model above is a reduction of the problem with fixed angles to a MIP whose size is the total size of the pairwise no-fit polygons.

## Applications

- **Sheet metal and laser cutting.** Parts cut by laser, plasma or punch from steel sheets, usually with rotations by $90^\circ$ or $180^\circ$.
- **Garments and upholstery.** Pattern pieces on a roll of cloth, often with no rotation or only $180^\circ$ because of the grain. The open dimension variant comes from here.
- **Leather.** Hides with irregular outlines and defects.
- **Wood, glass and paper.** Irregular parts from boards and panels, often with extra rules on the cuts.

In all of them the parts are first placed by one of the methods above and then cut by a toolpath, so the layout also affects the cutting time.

## References
