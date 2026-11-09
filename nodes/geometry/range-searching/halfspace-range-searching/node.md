---
tag: MW3N3D
kind: problem
slug: halfspace-range-searching
name: Halfspace range searching
aliases:
- half-plane range searching
- linear constraint range query
- halfplane range query
area: geometry/range-searching
level: advanced
summary: Range searching where each query range is a halfplane in the plane or a halfspace in higher dimensions.
prereqs: [orthogonal-range-searching, orientation-test, convex-hull]
see_also: [simplex-range-searching, circular-range-searching, partition-tree, shallow-cutting, geometric-cutting, range-emptiness-query, convex-layers, range-searching-lower-bound]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.3 (simplex range searching) and Section 40.4 (halfspace range reporting and emptiness)
  - book: isbn:9780821806746
    title: Pankaj K. Agarwal and Jeff Erickson, Geometric range searching and its relatives, in Advances in Discrete and Computational Geometry, Contemporary Mathematics 223, American Mathematical Society, 1999, pages 1 to 56
    locator: Section 5, Halfspace range searching (Table 3 of reporting and emptiness bounds)
  - paper: doi:10.1007/BF01934990
    title: Bernard Chazelle, Leonidas J. Guibas and D. T. Lee, The power of geometric duality, BIT 25(1), 1985, pages 76 to 90
    locator: halfplane range reporting in O(log n + k) time with O(n) space via convex layers (DOI to be checked)
  - paper: doi:10.1016/0925-7721(92)90006-E
    title: Jiří Matoušek, Reporting points in halfspaces, Computational Geometry, Theory and Applications 2(3), 1992, pages 169 to 186
    locator: shallow cuttings and halfspace reporting in d dimensions
  - paper: doi:10.1137/1.9781611973068.21
    title: Peyman Afshani and Timothy M. Chan, Optimal halfspace range reporting in three dimensions, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2009, pages 180 to 186
    locator: O(n) space and O(log n + k) query time in R^3 (DOI to be checked)
  - paper: doi:10.1007/BF02573971
    title: Hervé Brönnimann, Bernard Chazelle and János Pach, How hard is half-space range searching?, Discrete and Computational Geometry 10, 1993, pages 143 to 155
    locator: the lower bound for halfspace counting in the semigroup arithmetic model (DOI to be checked)
---

Halfspace range searching stores a set $P$ of $n$ points in $\mathbb{R}^d$ so that, for a query halfspace $h = \{x : a \cdot x \le b\}$, the points of $P \cap h$ can be reported, counted or tested for existence. In the plane the ranges are halfplanes. Unlike boxes, halfspaces are not products of intervals, so range trees do not apply; the tools are convex layers and duality in the plane, and [partition trees](/partition-tree/), [cuttings](/geometric-cutting/) and [shallow cuttings](/shallow-cutting/) in general. Counting is as hard as [simplex range searching](/simplex-range-searching/) up to polylogarithmic factors, with $O(n)$-space structures answering in about $n^{1 - 1/d}$ time, while reporting in $\mathbb{R}^2$ and $\mathbb{R}^3$ takes $O(\log n + k)$ time with linear space.

## In plain words

A set of points is stored. A question gives a straight line and a side of it, and asks for the points on that side: list them, count them, or say whether there is any. In three or more dimensions the line becomes a flat plane that cuts space in two.

Rectangles can be cut into a few stretches along each axis, which makes them easy, but a slanted line cannot. So other ideas are used. The outermost points of the set form a convex shape, and a side of a line contains a point exactly when it contains one of the corners of that shape. For counting, the points are grouped into cells such that any line passes through only a few cells, and whole cells on one side are counted at once.

## Definition

**Notation.** $P$ is a set of $n$ points in $\mathbb{R}^d$, $p$ a point, and $k = |P \cap h|$ the output size of a reporting query. A query halfspace is $h = \{x \in \mathbb{R}^d : a \cdot x \le b\}$ with $a \ne 0$, closed; its bounding hyperplane is $\partial h = \{x : a \cdot x = b\}$. In the plane, the closed halfplane to the left of the directed line through $u$ and $v$ is $\{p : \mathrm{orient}(u, v, p) \ge 0\}$, where $\mathrm{orient}(u, v, p)$ is the sign of $(v_x - u_x)(p_y - u_y) - (v_y - u_y)(p_x - u_x)$; see the [orientation test](/orientation-test/). $\mathrm{incircle}$ is not used.

**Input.** $P$, preprocessed once. Then queries, each a halfspace $h$.

**Output.** One of: **reporting**, the points of $P \cap h$; **counting**, $|P \cap h|$, or more generally the sum of semigroup weights; **emptiness**, whether $P \cap h = \emptyset$.

**Degenerate input.** Points of $P$ on $\partial h$ belong to $h$. Points may coincide, and many may lie on one hyperplane; the structures below handle this with exact predicates and a consistent tie-break.

## Variants

- **Dimension.** The plane, $\mathbb{R}^3$ and higher dimensions behave differently for reporting: $\mathbb{R}^2$ and $\mathbb{R}^3$ have optimal linear-space structures, while for $d \ge 4$ reporting uses [shallow cuttings](/shallow-cutting/) and costs about $n^{1 - 1/\lfloor d/2 \rfloor}$ with linear space.
- **Static or dynamic.** Points may be inserted and deleted between queries; see [dynamic range searching](/dynamic-range-searching/).
- **Dual form.** By point-hyperplane duality, reporting the points below a query hyperplane is the same as reporting the hyperplanes above a query point, that is, the hyperplanes of an arrangement that a vertical ray from the point crosses.
- **Approximate.** The halfspace may be fattened by a factor $(1 + \varepsilon)$, and points near its boundary may be reported or not; this has polylogarithmic query time.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| query halfplane | points in it | $k$ |
|---|---|---|
| $y \le x - 1$ | $(5,4)$ on the line, $(9,6)$, $(8,1)$, $(7,2)$ | 4 |
| $y \ge 7$ | $(4,7)$ on the line, $(3,8)$ | 2 |
| $x + y \le 4$ | none | 0 |
| left of the directed line from $(0, 0)$ to $(1, 1)$, that is $y \ge x$ | $(2,3)$, $(4,7)$, $(3,8)$, $(6,6)$ on the line | 4 |

For the last row, $\mathrm{orient}((0,0), (1,1), (6,6)) = 1 \cdot 6 - 1 \cdot 6 = 0$, so $(6,6)$ lies on the bounding line and is reported. The convex hull of $P$ has the vertices $(8,1), (9,6), (3,8), (2,3)$, and the third query is empty because the hull vertex minimizing $x + y$, $(2,3)$, has $x + y = 5 > 4$.

## Known algorithms

| problem | space | query | model and case | reference |
|---|---|---|---|---|
| reporting, $d = 2$ | $O(n)$ | $O(\log n + k)$ | real RAM, worst case | Chazelle, Guibas and Lee (1985), [convex layers](/convex-layers/) |
| reporting, $d = 3$ | $O(n)$ | $O(\log n + k)$ | real RAM, worst case; expected $O(n \log n)$ preprocessing | Afshani and Chan (2009) |
| reporting, $d \ge 4$ | $O(n \log \log n)$ | $O(n^{1 - 1/\lfloor d/2 \rfloor} \log^{O(1)} n + k)$ | real RAM, worst case | Matoušek (1992), [shallow cutting](/shallow-cutting/) |
| emptiness, $d = 2$ | $O(n)$ | $O(\log n)$ | real RAM, worst case | extreme vertex of the [convex hull](/convex-hull/) by binary search |
| emptiness, $d = 3$ | $O(n)$ | $O(\log n)$ | real RAM, worst case | extreme vertex by the Dobkin and Kirkpatrick hierarchy |
| counting, any $d$ | $O(n)$ | $O(n^{1 - 1/d})$ | real RAM, worst case; expected $O(n \log n)$ preprocessing | Chan (2012), [partition tree](/partition-tree/) |
| counting, any $d$ | $O(n^{d} / \log^{d} n)$ | $O(\log n)$ | real RAM, worst case | Matoušek (1993), hierarchical [cuttings](/geometric-cutting/) |
| counting, trade-off, $n \le m \le n^{d}$ | $O(m)$ | $O((n / m^{1/d}) \log^{O(1)} (m/n))$ | real RAM, worst case | Matoušek (1993), partition trees with cuttings at the top |

Emptiness in the plane uses the fact that a halfplane $a \cdot x \le b$ meets $P$ exactly when the hull vertex minimizing $a \cdot x$ satisfies it, and that vertex is found by binary search on the hull's edge directions. Every reporting structure answers emptiness by stopping at the first point.

## Bounds

- **Counting, semigroup arithmetic model.** Brönnimann, Chazelle and Pach (1993) proved that a structure with $m$ semigroup sums stored needs $\Omega((n / \log n)^{1 - (d-1)/(d(d+1))} / m^{1/d})$ semigroup operations per query in the worst case. For $d = 2$ this is $\Omega((n/\log n)^{5/6} / m^{1/2})$, weaker than the $\Omega(n / \sqrt{m})$ known for [simplex range searching](/simplex-range-searching/); see [range searching lower bound](/range-searching-lower-bound/).
- **Reporting.** $\Omega(\log n + k)$ in the comparison model, met in $\mathbb{R}^2$ and $\mathbb{R}^3$. For $d \ge 4$ the upper and lower bounds differ; the known structures with polylogarithmic query time use about $n^{\lfloor d/2 \rfloor}$ space.
- **Emptiness.** Upper bound $n^{1 - 1/\lfloor d/2 \rfloor} 2^{O(\log^{*} n)}$ with linear space, by Matoušek and Schwarzkopf.

## Reductions

- **From disks.** By the [paraboloid lifting map](/paraboloid-lifting-map/), a disk in the plane becomes a lower halfspace in $\mathbb{R}^3$; see [circular range searching](/circular-range-searching/).
- **To simplex range searching.** A halfspace is the limit of a simplex, and counting structures for simplices handle it directly; conversely a simplex is the intersection of $d + 1$ halfspaces, which multi-level partition trees exploit.
- **Nearest neighbors.** By the same lifting, the $k$ nearest neighbors of a point $q$ in the plane are the points of a halfspace in $\mathbb{R}^3$, so halfspace reporting gives [k-nearest neighbor search](/k-nearest-neighbor-search/) in $O(\log n + k)$ time.
- **Duality.** In the plane, the point $(p_x, p_y)$ maps to the line $y = p_x x - p_y$ and the line $y = m x + c$ to the point $(m, -c)$; a point lies above a line exactly when the dual line lies above the dual point. So reporting the points below a line becomes reporting the lines below a point.

## Applications

- **Linear constraint queries in databases**: report the records with $\sum_i a_i x_i \le b$.
- **Nearest neighbors and circular queries** through lifting, as above.
- **Collision and visibility tests**: is any point on the far side of a plane?
- **Building block** of simplex range searching, ray shooting and linear programming queries.

## References
