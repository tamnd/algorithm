---
tag: DKMSBW
kind: problem
slug: rectilinear-steiner-tree-problem
name: Rectilinear Steiner tree problem
aliases:
- rectilinear Steiner minimal tree
- RSMT problem
- Manhattan Steiner tree
- L1 Steiner tree problem
area: geometry/geometric-optimization
level: advanced
summary: Connect n points with horizontal and vertical segments of least total length, extra junctions allowed. NP-hard; Hanan's grid holds an optimum; MST is within 3/2.
prereqs: [steiner-tree-problem, minimum-spanning-tree, euclidean-steiner-tree-problem]
see_also: [euclidean-steiner-tree-problem, steiner-ratio, steiner-tree-problem, minimum-spanning-tree, arora-euclidean-tsp-ptas, planar-steiner-tree-ptas, np-hard, rectilinear-polygon]
sources:
  - paper: doi:10.1137/0114025
    title: "M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 1966"
    locator: the theorem that some rectilinear Steiner minimal tree has all Steiner points on the grid of terminal coordinates, and exact solutions for small n
  - paper: doi:10.1137/0130013
    title: "F. K. Hwang, On Steiner minimal trees with rectilinear distance, SIAM Journal on Applied Mathematics 30(1), 1976"
    locator: the bound MST ≤ (3/2) RSMT, tight, and the shape of full rectilinear Steiner trees
  - paper: doi:10.1137/0132071
    title: "M. R. Garey and D. S. Johnson, The rectilinear Steiner tree problem is NP-complete, SIAM Journal on Applied Mathematics 32(4), 1977"
    locator: NP-completeness of the decision version
  - paper: doi:10.1145/290179.290180
    title: "Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998"
    locator: the approximation scheme, which also covers the rectilinear Steiner tree
  - paper: "Frank K. Hwang, Dana S. Richards and Pawel Winter, The Steiner Tree Problem, Annals of Discrete Mathematics 53, North-Holland, 1992"
    locator: Part III, the rectilinear Steiner problem (Hanan grid, full trees, heuristics and exact algorithms)
  - paper: "David M. Warme, Pawel Winter and Martin Zachariasen, Exact algorithms for plane Steiner tree problems, a computational study, in Advances in Steiner Trees, Kluwer, 2000"
    locator: the GeoSteiner method for rectilinear instances, full Steiner tree generation and concatenation
---

The rectilinear Steiner tree problem asks for a network of horizontal and vertical segments, of least total length, that connects $n$ given points called terminals. The network may branch at extra points, called Steiner points. Lengths are measured in the $L_1$ (Manhattan) metric. The problem models wiring in chip design, where wires run along two perpendicular directions. Hanan (1966) proved that some optimal tree has all its Steiner points on the *Hanan grid*, the crossings of the horizontal and vertical lines through the terminals, so the problem is a [Steiner tree problem](/steiner-tree-problem/) on a graph with at most $n^2$ vertices. It is NP-complete (Garey and Johnson 1977), the rectilinear [minimum spanning tree](/minimum-spanning-tree/) is within a factor $3/2$ of optimal (Hwang 1976), and Arora's scheme gives a $(1+\varepsilon)$-approximation. It is the $L_1$ version of the [Euclidean Steiner tree problem](/euclidean-steiner-tree-problem/).

## In plain words

You must join some points on a chip with wires, and every wire must run straight left-right or straight up-down. You want the least total wire.

Joining the points directly, two at a time, is not the best. Wires can meet at new junction points, and shared wire saves length. For four points in a plus shape, one junction in the middle uses 4 units of wire, while joining the points directly needs 6.

A useful fact: you never need junctions in odd places. Draw a line across and a line up and down through every point. Some best network has all its junctions where these lines cross. This turns the problem into choosing among a finite set of crossings, but there are still too many choices to try them all for large inputs.

## Definition

Notation: $T$ is a set of $n$ terminals in the plane. A *rectilinear tree* for $T$ is a connected union of finitely many horizontal and vertical segments that contains $T$. Its length is the total length of its segments. $\mathrm{RSMT}(T)$ is the least length, and $\mathrm{RMST}(T)$ is the length of a minimum spanning tree of $T$ with $L_1$ edge weights $|x_1 - x_2| + |y_1 - y_2|$.

**Input.** $T$, with exact coordinates.

**Output.** A rectilinear tree for $T$ of length $\mathrm{RSMT}(T)$, a *rectilinear Steiner minimal tree*.

**Hanan grid.** Let $X$ and $Y$ be the sets of $x$ and $y$ coordinates of the terminals. The Hanan grid is the set of points $X \times Y$, with the grid segments between neighbors. It has at most $n^2$ points.

**Theorem (Hanan 1966).** Some rectilinear Steiner minimal tree for $T$ lies on the Hanan grid; in particular its Steiner points are in $X \times Y$.

*Proof sketch.* Take an optimal tree and a vertical line $x = a$ with $a \notin X$ that contains tree segments. Shift all tree segments on that line to $x = a + t$, and stretch or shrink the horizontal segments that end on it. The length changes by $t(\ell - r)$, where $\ell$ and $r$ count the horizontal segments that meet the line from the left and from the right. This is linear in $t$, so one direction does not increase the length. Shift in that direction until the line reaches a value of $X$ or another vertical line of the tree. Each step lowers the number of vertical lines off $X$. Do the same for horizontal lines. $\square$

**Structure.** A Steiner point of a minimal tree has degree 3 or 4, and there are at most $n - 2$ Steiner points. A minimal tree splits at terminals of degree more than 1 into *full* components, in which all terminals are leaves. Hwang (1976) showed that some optimal full tree has a simple shape: a straight backbone with legs that alternate sides, or a corner form of it.

**Degeneracies.** Duplicate terminals can be removed. Terminals with equal coordinates make the Hanan grid smaller. Optimal trees are often not unique, since a segment can usually be routed as two different L shapes of the same length.

## Variants

- **Euclidean.** Any edge direction, Euclidean length: the [Euclidean Steiner tree problem](/euclidean-steiner-tree-problem/).
- **$\lambda$-geometry.** Edges in $\lambda$ uniformly spaced directions; the rectilinear case is $\lambda = 2$, and the octilinear case $\lambda = 4$ models newer chip wiring.
- **With obstacles.** Wires must avoid rectangles or a [rectilinear polygon](/rectilinear-polygon/) region; the grid of all obstacle and terminal coordinates plays the role of the Hanan grid.
- **Rectilinear Steiner arborescence.** Every terminal must be reached from a root by a monotone path, which models signal delay.
- **Higher dimensions.** The $L_1$ problem in $\mathbb{R}^d$; Hanan's argument works on each coordinate.

## Examples

| terminals | $\mathrm{RMST}$ | $\mathrm{RSMT}$ | Steiner points | ratio |
|---|---|---|---|---|
| $(1,0), (0,1), (2,1), (1,2)$ | 6 | 4 | $(1,1)$ | $3/2$ |
| $(0,0), (4,1), (1,4), (5,5), (2,3)$ | 16 | 13 | $(1,3), (4,3)$ | $16/13$ |
| any 3 points | | $\Delta x + \Delta y$ | (median $x$, median $y$) | |

**The plus shape.** Every pair of the four terminals is at $L_1$ distance 2, so every spanning tree has length 6. The Steiner point $(1,1)$ has distance 1 to each, so $\mathrm{RSMT} = 4$. This attains Hwang's bound $3/2$.

**Five points.** With Steiner points $s_1 = (1,3)$ and $s_2 = (4,3)$, the tree has the edges $(0,0)s_1$ of length 4, $s_1(1,4)$ of length 1, $s_1(2,3)$ of length 1, $(2,3)s_2$ of length 2, $s_2(4,1)$ of length 2 and $s_2(5,5)$ of length 3, in total 13. Both Steiner points are Hanan grid points. An exhaustive search over all sets of at most $n - 2$ Hanan grid points, with an $L_1$ minimum spanning tree on each, confirms 13.

**Three points.** Any rectilinear tree that connects the terminals spans the range of $x$ values and the range of $y$ values, so its length is at least $\Delta x + \Delta y$, the half perimeter of the bounding box. The point (median $x$, median $y$) attains it.

## Known algorithms

| algorithm | guarantee | time |
|---|---|---|
| rectilinear minimum spanning tree | factor $3/2$ | $O(n \log n)$ |
| graph Steiner tree on the Hanan grid, by dynamic programming over terminal subsets | exact | exponential in $n$ |
| best set of at most $n - 2$ Hanan points with a spanning tree on each | exact | exponential in $n$ |
| GeoSteiner: generate full Steiner trees, then combine them by integer programming | exact | exponential in the worst case; practical for large instances |
| Arora (1998) | factor $1 + \varepsilon$ | $n (\log n)^{O(1/\varepsilon)}$ |
| iterated 1-Steiner and similar heuristics | close to optimal in practice | polynomial |

The spanning tree bound uses the $L_1$ minimum spanning tree, which can be found in $O(n \log n)$ time from a sparse candidate graph, since each point needs only one candidate neighbor in each of eight angular regions.

## Bounds

- **Hardness.** The decision version is NP-complete (Garey and Johnson 1977). Unlike the Euclidean case, it is in NP, because by Hanan's theorem a certificate is a set of grid points and the length is an integer combination of coordinate differences.
- **Spanning tree ratio.** $\mathrm{RMST}(T) \le \frac{3}{2}\, \mathrm{RSMT}(T)$ for every $T$ (Hwang 1976), and the plus shape shows the constant is tight. So the rectilinear [Steiner ratio](/steiner-ratio/) is $2/3$.
- **Bounding box.** $\mathrm{RSMT}(T) \ge \Delta x + \Delta y$, with equality for $n \le 3$. Chip placement tools use this half perimeter as a fast wire length estimate.
- **Steiner points.** At most $n - 2$, each of degree 3 or 4.

## Reductions

- **To the Steiner tree problem in graphs.** By Hanan's theorem, solve the [Steiner tree problem](/steiner-tree-problem/) in the Hanan grid graph with $O(n^2)$ vertices and edge weights equal to the grid distances. Exact graph methods and graph approximation algorithms then apply.
- **NP-hardness.** Garey and Johnson reduce a known NP-complete problem to the rectilinear case with integer coordinates of polynomial size, so the problem stays hard when all coordinates are small integers.
- **To spanning trees.** For a fixed set $S$ of Steiner points, the best tree is an $L_1$ minimum spanning tree of $T \cup S$, so the problem is to choose $S$.

## Applications

- **VLSI routing.** Global routing connects the pins of each net with a short rectilinear tree; many tools build such trees millions of times.
- **Wire length estimation.** Placement tools estimate wire length by fast Steiner tree approximations or by the half perimeter bound.
- **Printed circuit boards and floor plans.** Pipes, cables and corridors that follow two perpendicular directions.

## References
