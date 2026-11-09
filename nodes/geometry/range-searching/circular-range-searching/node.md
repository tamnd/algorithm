---
tag: 8V9E08
kind: problem
slug: circular-range-searching
name: Circular range searching
aliases:
- disk range searching
- disk range query
- fixed-radius and variable-radius disk queries
area: geometry/range-searching
level: core
summary: Range searching where each query range is a disk in the plane.
prereqs: [halfspace-range-searching, paraboloid-lifting-map]
see_also: [halfspace-range-searching, simplex-range-searching, paraboloid-lifting-map, in-circle-test, k-nearest-neighbor-search, kd-tree-range-search, partition-tree, shallow-cutting]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.4 (halfspace reporting and its use for disks by lifting) and Section 40.5 (semialgebraic range searching)
  - book: isbn:9780821806746
    title: Pankaj K. Agarwal and Jeff Erickson, Geometric range searching and its relatives, in Advances in Discrete and Computational Geometry, Contemporary Mathematics 223, American Mathematical Society, 1999, pages 1 to 56
    locator: Section 6, Semialgebraic range searching (linearization of disks)
  - paper: doi:10.1137/1.9781611973068.21
    title: Peyman Afshani and Timothy M. Chan, Optimal halfspace range reporting in three dimensions, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2009, pages 180 to 186
    locator: O(n) space and O(log n + k) query for halfspaces in R^3, hence for disks in the plane (DOI to be checked)
  - paper: doi:10.1137/120890855
    title: Pankaj K. Agarwal, Jiří Matoušek and Micha Sharir, On range searching with semialgebraic sets. II, SIAM Journal on Computing 42(6), 2013, pages 2039 to 2062
    locator: linear-space structures for semialgebraic ranges in R^d with O(n^(1-1/d) polylog n) query time, by polynomial partitioning (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9 (the lifting map and the Delaunay triangulation) and Chapter 16 (simplex range searching)
---

Circular range searching stores a set $P$ of $n$ points in the plane so that, for a query disk $D$ with center $c$ and radius $r$, the points of $P \cap D$ can be reported, counted or tested for existence. The [paraboloid lifting map](/paraboloid-lifting-map/) $p \mapsto (p_x, p_y, p_x^2 + p_y^2)$ turns every disk into a lower halfspace in $\mathbb{R}^3$, so disk reporting reduces to three-dimensional [halfspace range reporting](/halfspace-range-searching/) and takes $O(\log n + k)$ time with $O(n)$ space. Counting is harder: linear-space structures answer in about $\sqrt{n}$ time by polynomial partitioning, or $O(n^{2/3})$ time with a three-dimensional [partition tree](/partition-tree/).

## In plain words

A set of points is stored, such as the positions of shops on a map. A question gives a center and a radius, and asks for the points within that distance of the center: list them, count them, or say whether there is any.

Circles are curved, so the tricks for rectangles and straight lines do not apply directly. A classic trick fixes this. Lift every point up onto a bowl-shaped surface, at a height equal to its squared distance from the origin. Then the points inside any circle are exactly the lifted points that lie below a certain flat plane. So a circle question becomes a question about one side of a plane, in three dimensions, which has good solutions.

## Definition

**Notation.** $P$ is a set of $n$ points in the plane ($d = 2$), $p = (p_x, p_y)$ a point, and $k = |P \cap D|$ the output size of a reporting query. The query is the closed disk $D = \{p : (p_x - c_x)^2 + (p_y - c_y)^2 \le r^2\}$ with center $c$ and radius $r \ge 0$. When the disk is given by three points $a, b, e$ on its boundary in counterclockwise order, $p \in D$ exactly when $\mathrm{incircle}(a, b, e, p) \ge 0$; see the [in-circle test](/in-circle-test/). $\mathrm{orient}$ is not used.

**Input.** $P$, preprocessed once. Then queries, each a disk.

**Output.** **Reporting**: the points of $P \cap D$. **Counting**: $|P \cap D|$, or a semigroup sum of weights. **Emptiness**: whether $P \cap D = \emptyset$.

**Degenerate input.** Points on the circle belong to $D$. With integer or rational coordinates and $r^2$ rational, the test $(p_x - c_x)^2 + (p_y - c_y)^2 \le r^2$ is exact; computing $r$ by a square root and comparing distances in floating point misclassifies points on the circle.

## Variants

- **Fixed radius.** All queries have the same radius $r$, known in advance (fixed-radius near neighbors). A grid of cells of side $r$ reduces a query to the points of $9$ cells, which is fast on well-spread inputs but not output sensitive in the worst case.
- **Approximate disks.** Points within distance $(1 + \varepsilon) r$ may also be reported. Quadtrees and similar structures answer in $O(\log n + \varepsilon^{-1})$ time plus output.
- **Higher dimensions.** Balls in $\mathbb{R}^d$ lift to halfspaces in $\mathbb{R}^{d+1}$.
- **Annuli and other curved ranges** are semialgebraic ranges, handled by linearization or by polynomial partitioning.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| center $c$ | $r^2$ | points inside, with squared distance | $k$ |
|---|---|---|---|
| $(6, 4)$ | 5 | $(5,4)$: 1; $(6,6)$: 4; $(7,2)$: 5, on the circle | 3 |
| $(3, 6)$ | 5 | $(4,7)$: 2; $(3,8)$: 4 | 2 |
| $(5, 4)$ | 0 | $(5,4)$: 0 | 1 |

For the first disk, the lifting map sends $p$ to $(p_x, p_y, p_x^2 + p_y^2)$, and $p \in D$ exactly when $p_x^2 + p_y^2 \le 2 c_x p_x + 2 c_y p_y + r^2 - c_x^2 - c_y^2 = 12 p_x + 8 p_y - 47$. For $(7,2)$ both sides are $53$, so the lifted point is on the plane; for $(8,1)$ the left side is $65$ and the right side $57$, so it is outside.

## Known algorithms

| structure | space | query | model and case | reference |
|---|---|---|---|---|
| linear scan | $O(n)$ | $O(n)$ | real RAM, worst case | |
| lifting and 3D halfspace reporting | $O(n)$ | $O(\log n + k)$ | real RAM, worst case; expected $O(n \log n)$ preprocessing | Afshani and Chan (2009) |
| emptiness by [nearest neighbor search](/nearest-neighbor-search/) on the Voronoi diagram | $O(n)$ | $O(\log n)$ | real RAM, worst case | the disk is empty when the nearest point to $c$ is farther than $r$ |
| lifting and 3D [partition tree](/partition-tree/), counting | $O(n)$ | $O(n^{2/3})$ | real RAM, worst case | Chan (2012) |
| polynomial partitioning, counting | $O(n)$ | $O(n^{1/2} \log^{O(1)} n)$ | real RAM, worst case | Agarwal, Matoušek and Sharir (2013) |
| lifting and 3D cuttings, counting | $O(n^{3 + \varepsilon})$ | $O(\log n)$ | real RAM, worst case | Chazelle, Sharir and Welzl (1992) |
| [kd-tree](/kd-tree-range-search/) | $O(n)$ | no good worst case bound | real RAM | fast in practice |

## Bounds

- **Reporting.** $\Omega(\log n + k)$ in the comparison model, met by the lifting reduction.
- **Emptiness.** $\Omega(\log n)$ in the algebraic decision tree model, since a disk of radius $0$ decides membership in $P$; met by nearest neighbor search.
- **Counting with linear space.** The best known bound is about $\sqrt{n}$; the lifting to $\mathbb{R}^3$ alone gives only $n^{2/3}$ because it does not use the special shape of the lifted point set, which lies on a paraboloid.

## Reductions

- **To halfspaces in $\mathbb{R}^3$.** $(p_x - c_x)^2 + (p_y - c_y)^2 \le r^2$ is equivalent to $p_x^2 + p_y^2 \le 2 c_x p_x + 2 c_y p_y + (r^2 - c_x^2 - c_y^2)$, a linear inequality in the lifted point $(p_x, p_y, p_x^2 + p_y^2)$.
- **From nearest neighbors.** The $k$ nearest neighbors of $c$ are the points in the smallest disk around $c$ that holds $k$ points, so a counting or reporting structure for disks with a search on $r$ answers [k-nearest neighbor search](/k-nearest-neighbor-search/); with halfspace reporting this takes $O(\log n + k)$.
- **Emptiness and nearest neighbors.** The disk is empty exactly when the [nearest neighbor](/nearest-neighbor-search/) of $c$ is at distance greater than $r$.

## Applications

- **Location queries**: all shops, sensors or stations within distance $r$ of a point.
- **Neighbor finding in simulations**: particles within an interaction radius.
- **Clustering**: density-based clustering asks for the points within $\varepsilon$ of each point.
- **Delaunay and Voronoi structures**: the empty-circle property of the [Delaunay triangulation](/delaunay-triangulation/) is a disk emptiness condition.

## References
