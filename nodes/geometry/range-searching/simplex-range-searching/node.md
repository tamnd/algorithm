---
tag: RE6ENQ
kind: problem
slug: simplex-range-searching
name: Simplex range searching
aliases:
- simplex range query
- polytope range searching
- triangle range searching
area: geometry/range-searching
level: advanced
summary: Range searching where each query range is a simplex, a general framework covering polyhedral ranges.
prereqs: [halfspace-range-searching, orientation-test]
see_also: [partition-tree, partition-tree-query, partition-theorem, geometric-cutting, halfspace-range-searching, epsilon-net-theorem, range-searching-lower-bound, orthogonal-range-searching]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.3, Simplex range searching (partition trees, cuttings, space and query trade-offs, lower bounds)
  - book: isbn:9780821806746
    title: Pankaj K. Agarwal and Jeff Erickson, Geometric range searching and its relatives, in Advances in Discrete and Computational Geometry, Contemporary Mathematics 223, American Mathematical Society, 1999, pages 1 to 56
    locator: Section 3 (lower bounds) and Section 4, Simplex range searching
  - paper: doi:10.1007/BF02293051
    title: Jiří Matoušek, Efficient partition trees, Discrete and Computational Geometry 8, 1992, pages 315 to 334
    locator: the partition theorem and linear-space partition trees with O(n^(1-1/d) log^(O(1)) n) query time (DOI to be checked)
  - paper: doi:10.1007/s00454-012-9410-z
    title: Timothy M. Chan, Optimal partition trees, Discrete and Computational Geometry 47(4), 2012, pages 661 to 690
    locator: O(n) space, O(n^(1-1/d)) query time, O(n log n) expected preprocessing (DOI to be checked)
  - paper: doi:10.1090/S0894-0347-1989-1001852-0
    title: Bernard Chazelle, Lower bounds on the complexity of polytope range searching, Journal of the American Mathematical Society 2(4), 1989, pages 637 to 666
    locator: the Omega(n/sqrt(m)) lower bound in the plane and Omega(n/(m^(1/d) log n)) in R^d, semigroup arithmetic model (DOI to be checked)
  - paper: doi:10.1137/0211012
    title: Dan E. Willard, Polygon retrieval, SIAM Journal on Computing 11(1), 1982, pages 149 to 165
    locator: the first partition tree, O(n) space and O(n^0.774) query time in the plane (DOI to be checked)
---

Simplex range searching stores a set $P$ of $n$ points in $\mathbb{R}^d$ so that, for a query simplex $\Delta$ (a triangle in the plane, a tetrahedron in space), the points of $P \cap \Delta$ can be counted, reported, or summed with semigroup weights. Every polyhedral range with $O(1)$ faces is a union of $O(1)$ simplices, and a halfspace is a limiting simplex, so this is the general problem for linear ranges. The answer is a space and time trade-off: with $O(m)$ space, $n \le m \le n^{d}$, a query takes $\tilde{O}(n / m^{1/d})$ time, from $O(n^{1 - 1/d})$ with linear space ([partition trees](/partition-tree/)) to $O(\log n)$ with about $n^{d}$ space ([cuttings](/geometric-cutting/)), and Chazelle's lower bound shows this is nearly optimal in the semigroup model.

## In plain words

A set of points is stored. A question gives a triangle, or its analogue in higher dimensions, and asks how many points are inside it, or which ones. Triangles can be tilted any way, so the tricks for upright rectangles do not work.

The main idea is to group the points into cells, each with about the same number of points, such that any straight line passes through only a few of the cells. A cell that lies completely inside the triangle is counted at once; a cell completely outside is skipped; only the few cells cut by the triangle's sides must be looked at more closely. Doing this again inside each cell gives a tree of groups. More memory allows faster answers, and there is a proven limit to how much faster.

## Definition

**Notation.** $P$ is a set of $n$ points in $\mathbb{R}^d$, $p$ a point, $k = |P \cap \Delta|$ the output size of a reporting query, and $m$ the space of a structure in words (or the number of stored semigroup sums). A simplex $\Delta$ is the convex hull of $d + 1$ affinely independent points, and it is the intersection of $d + 1$ closed halfspaces. In the plane, a point $p$ lies in the closed triangle with counterclockwise vertices $a, b, c$ exactly when $\mathrm{orient}(a, b, p) \ge 0$, $\mathrm{orient}(b, c, p) \ge 0$ and $\mathrm{orient}(c, a, p) \ge 0$; see the [orientation test](/orientation-test/). $\mathrm{incircle}$ is not used.

**Input.** $P$, optionally with a weight $w(p)$ in a commutative semigroup for each point, preprocessed once. Then queries, each a simplex $\Delta$.

**Output.** **Counting**: $|P \cap \Delta|$, or $\sum_{p \in P \cap \Delta} w(p)$. **Reporting**: the points of $P \cap \Delta$. **Emptiness**: whether $P \cap \Delta = \emptyset$.

**Degenerate input.** The simplex is closed, so points on its boundary count. Points may coincide or be collinear; the predicates are exact.

## Variants

- **Polyhedral ranges.** A convex polytope with $O(1)$ faces is triangulated into $O(1)$ simplices, and its count is the sum of theirs if boundaries are assigned to one simplex each.
- **Semialgebraic ranges.** Disks, annuli and other ranges defined by polynomial inequalities of bounded degree are handled by linearization, which maps them to halfspaces or simplices in a higher dimension; see [circular range searching](/circular-range-searching/).
- **Reporting versus counting.** Reporting costs the counting bound plus $O(k)$; there is no structure with near-linear space and polylogarithmic reporting time.
- **Dynamic.** Partition trees can be made dynamic with polylogarithmic overhead by the [logarithmic method](/decomposable-searching-problem/); see [dynamic range searching](/dynamic-range-searching/).

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| triangle (counterclockwise) | points inside | $k$ | boundary points |
|---|---|---|---|
| $(2,2), (8,2), (5,8)$ | $(5,4), (7,2), (6,6)$ | 3 | $(7,2)$ on edge $ab$, $\mathrm{orient} = 0$; $(6,6)$ on edge $bc$ |
| $(1,2), (7,2), (4,8)$ | $(2,3), (5,4), (4,7), (7,2)$ | 4 | $(7,2)$ is the vertex $b$ |
| $(3,1), (9,7), (1,9)$ | $(5,4), (4,7), (3,8), (6,6)$ | 4 | none |

For $(7,2)$ and the first triangle, $\mathrm{orient}((2,2), (8,2), (7,2)) = 6 \cdot 0 - 0 \cdot 5 = 0$, so the point lies on the bottom edge and is counted.

## Known algorithms

| structure | space | counting query | model and case | reference |
|---|---|---|---|---|
| linear scan | $O(n)$ | $O(n)$ | real RAM, worst case | |
| partition tree, $d = 2$ | $O(n)$ | $O(n^{0.774})$ | real RAM, worst case | Willard (1982) |
| spanning tree with low crossing number | $O(n)$ | $O(n^{1 - 1/d} \log^{O(1)} n)$ | real RAM, worst case | Chazelle and Welzl (1989) |
| efficient [partition tree](/partition-tree/) | $O(n)$ | $O(n^{1 - 1/d} \log^{O(1)} n)$ | real RAM, worst case; $O(n \log n)$ preprocessing | Matoušek (1992) |
| optimal partition tree | $O(n)$ | $O(n^{1 - 1/d})$ | real RAM, worst case query; expected $O(n \log n)$ preprocessing | Chan (2012) |
| hierarchical [cuttings](/geometric-cutting/) | $O(n^{d + \varepsilon})$ | $O(\log n)$ | real RAM, worst case | Chazelle, Sharir and Welzl (1992) |
| partition tree with cuttings at the top | $O(m)$, $n \le m \le n^{d}$ | $O((n / m^{1/d}) \log^{d+1} (m/n))$ | real RAM, worst case | Matoušek (1993) |

Reporting adds $O(k)$ to each query bound. The query on a partition tree is described in [partition tree query](/partition-tree-query/); the linear-space bound rests on the [partition theorem](/partition-theorem/), whose proof uses [cuttings](/geometric-cutting/) and the [epsilon-net theorem](/epsilon-net-theorem/).

## Bounds

- **Semigroup arithmetic model (Fredman, Yao, Chazelle).** The structure stores $m$ sums of weights of subsets of $P$, and a query must add up stored sums whose subsets are disjoint and cover $P \cap \Delta$; only semigroup additions are counted. Chazelle (1989) proved that for some point sets, in fact for random points in the unit square, any such structure needs $\Omega(n / \sqrt{m})$ additions for some triangle, and $\Omega(n / (m^{1/d} \log n))$ for some simplex in $\mathbb{R}^d$, $d \ge 3$. With $m = O(n)$ this is $\Omega(\sqrt{n})$ in the plane, which Chan's partition tree meets. See [range searching lower bound](/range-searching-lower-bound/).
- **Pointer machine, reporting.** Chazelle and Rosenberg (1996) showed that a structure answering reporting queries in $O(n^{\delta} + k)$ time needs $\Omega(n^{d(1 - \delta) - \varepsilon})$ space for any fixed $\varepsilon > 0$.
- **Upper bound for the trade-off.** Matoušek's structure meets the lower bound up to polylogarithmic factors over the whole range $n \le m \le n^{d}$.

## Reductions

- **Halfspaces.** A [halfspace](/halfspace-range-searching/) query is a degenerate simplex query, so simplex structures answer it with the same bounds. A simplex is the intersection of $d + 1$ halfspaces, and a multi-level partition tree handles one halfspace per level, which multiplies the space or time by a polylogarithmic factor.
- **Disks and other semialgebraic ranges** by linearization to halfspaces in a higher dimension, at the cost of the higher dimension in the exponent.
- **Segments crossed by a line.** A segment crosses a query line exactly when one endpoint is on or above it and the other on or below it, so counting the crossed segments is a two-level halfplane query, answered by a two-level partition tree.
- **Orthogonal ranges** are special polyhedral ranges, but [orthogonal range searching](/orthogonal-range-searching/) has much faster polylogarithmic solutions.

## Applications

- **Geographic and spatial databases**: count or report the objects inside a polygonal region.
- **Ray shooting and segment queries** among segments and triangles, through multi-level partition trees.
- **Geometric optimization**: building block of parametric search and of algorithms for Hopcroft's problem and for counting line intersections.
- **Discrepancy and sampling**: the lower bound arguments connect range searching with [epsilon-nets](/epsilon-net-theorem/) and discrepancy theory.

## References
