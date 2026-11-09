---
tag: 93B6PD
kind: data-structure
slug: order-k-voronoi-diagram
name: Order-k Voronoi diagram
aliases:
- k-order Voronoi diagram
- k-th order Voronoi diagram
- higher-order Voronoi diagram
area: geometry/voronoi-and-delaunay
level: advanced
summary: Partition by the set of k nearest sites, generalizing the ordinary (order-1) Voronoi diagram.
model: real-ram
complexity:
  vars: {n: the number of sites, k: the order}
  time: {build: O(k^2 n log n), query: O(log n + k)}
  space: {extra: O(k^2 n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [voronoi-diagram, farthest-point-voronoi-diagram, half-plane-intersection]
see_also: [k-nearest-neighbor-search, paraboloid-lifting-map, line-arrangement, voronoi-cell, power-diagram, k-nearest-neighbors, planar-point-location, sutherland-hodgman]
sources:
  - paper: "D. T. Lee, On k-nearest neighbor Voronoi diagrams in the plane, IEEE Transactions on Computers C-31(6), 1982, 478-487"
    locator: the O(k(n - k)) size bound and the iterative O(k^2 n log n) construction from the order-(k - 1) diagram
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the order-k diagram (the generalized Voronoi diagram for k nearest neighbours) and the farthest-point diagram
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 3 (higher-order and ordered order-k Voronoi diagrams)
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Toth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter on Voronoi diagrams and Delaunay triangulations (higher-order diagrams and their size)
---

The order-$k$ Voronoi diagram of a finite set $P$ of $n$ point sites in the plane splits the plane by the *set* of the $k$ nearest sites: the cell of a set $S$ of $k$ sites holds the points whose $k$ nearest sites are the sites of $S$, in any order. For $k = 1$ it is the ordinary [Voronoi diagram](/voronoi-diagram/), and for $k = n - 1$ it is the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/). Every cell is convex, two neighbouring cells differ in one site, and for sites in general position the diagram has $O(k(n - k))$ cells, edges and vertices. With [point location](/planar-point-location/) it reports the $k$ nearest sites of a query point in $O(\log n + k)$ time.

## In plain words

Put some shops on a map. For every place on the map, find the two shops that are nearest to it. Colour the place by this pair of shops. Places with the same pair get the same colour, and each colour fills one convex region.

Many pairs of shops get no region at all: two shops on opposite sides of the group are never the two nearest ones together.

The same works with three nearest shops, or any number. With one shop it is the usual nearest-shop map. With all shops but one, the colour tells which shop is farthest, because it is the one that is left out.

When the region of a place is known, its nearest shops are known at once, without measuring any distance.

## The abstract type

The diagram is a static structure over a set of distinct sites $p = (x, y)$, here with integer coordinates, for a fixed order $k \ge 1$. The code keeps only the part of the diagram inside a fixed axis-parallel box $B$. It supports:

- $\mathrm{insert}(p)$: add a site, before or between queries.
- $\mathrm{cells}()$: for each set $S$ of $k$ sites whose cell has positive area in $B$, that part of the cell, as a counterclockwise convex polygon with exact rational corners.
- $\mathrm{locate}(q)$: the sets $S$ whose closed cell holds the point $q$ of $B$; one set, unless $q$ is on the boundary of a cell.

Notation: $P$ is the set of sites, $n = |P|$, $k$ is the order, $h$ is the number of sites on the boundary of the convex hull, $d$ is the number of sides of a cell, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

**Definitions.** For a set $S \subseteq P$ with $|S| = k$, the order-$k$ cell is

$$V(S) = \{x : |x - s| \le |x - u| \text{ for all } s \in S \text{ and } u \in P \setminus S\}.$$

Each condition $|x - s|^2 \le |x - u|^2$ is the linear inequality $2 x \cdot (u - s) \le |u|^2 - |s|^2$, so $V(S)$ is an intersection of $k(n - k)$ closed half-planes and is convex. A point $x$ is in $V(S)$ exactly when $S$ is a set of $k$ nearest sites of $x$; with ties at the $k$-th distance, $x$ is in several cells.

**Properties.** These are proved in [the correctness proof](proofs/correctness/), except the size bound, which is due to Lee and is cited.

- **Refinement.** For $|S| = j + 1$, $V(S)$ is the union over $t \in S$ of the parts of $V(S \setminus \{t\})$ where $t$ is the nearest site of $P \setminus (S \setminus \{t\})$. So the order-$(j+1)$ diagram is found by cutting each order-$j$ cell by an ordinary Voronoi diagram.
- **Neighbours.** If two cells $V(S)$ and $V(S')$ share a side of positive length, then $S = A \cup \{p\}$ and $S' = A \cup \{q\}$ for a set $A$ of $k - 1$ sites, and the side lies on the bisector of $p$ and $q$.
- **Extremes.** For $k = 1$ the cells are the Voronoi cells. For $k = n - 1$, $V(P \setminus \{p\})$ is the farthest cell of $p$. For $k = n$ there is one cell, the plane.
- **Size (cited).** For $n$ sites in general position and $1 \le k \le n - 1$, the order-$k$ diagram has $O(k(n - k))$ cells, edges and vertices (D. T. Lee, 1982). The sum over all orders up to $k$ is $O(n k^2)$.
- **Lifting.** $|x - s|^2 = |x|^2 - (2 x \cdot s - |s|^2)$, so the order of the distances from $x$ is the reverse order of the $n$ affine functions $g_s(x) = 2 x \cdot s - |s|^2$. The cell of $S$ is where the functions of $S$ are the $k$ largest: the order-$k$ diagram is the projection of the $k$-th level of the arrangement of the $n$ planes $z = g_s(x)$ in space, which are the tangent planes of the [lifting paraboloid](/paraboloid-lifting-map/) at the lifted sites.

**General position.** The code assumes none. Cells of zero area, which come from collinear or cocircular sites, are dropped; their points are on the boundary of cells of positive area. The size bound is stated for general position: no three sites on a line and no four on a circle.

## Representation

The code stores the list of sites, the order $k$ and the box, and after a build a dictionary from each set $S$ of $k$ sites to the polygon $V(S) \cap B$, as a list of corners in counterclockwise order with fraction coordinates. Only cells of positive area are stored. Inserting a site only marks the stored diagram as stale; the next query rebuilds it.

A full structure stores the subdivision in a [doubly connected edge list](/doubly-connected-edge-list/), with a point location structure, and writes the set $S$ at each cell. Since neighbouring sets differ in one site, the sets can also be found by a walk that changes one site per step.

## Operations

```pseudo id=main
ORDER-K-BUILD(P, k, B)
L1  cells ← {∅ ↦ B}
L2  repeat min(k, n) times
L3      pieces ← empty; for each set T with polygon C in cells do
L4          for each site t not in T do
L5              piece ← the part of C where |x − t| ≤ |x − u| for every site u not in T ∪ {t}
L6              if piece has positive area then add the corners of piece to pieces[T ∪ {t}]
L7      cells ← {S ↦ the convex hull of pieces[S]} for each S in pieces
```

- **Line L1.** The order-$0$ diagram has one cell, the empty set of sites, and it fills the box.
- **Line L2.** Level $j$ holds the order-$j$ cells. If $n < k$ there is no set of $k$ sites and the result is empty.
- **Lines L4 and L5.** The pieces of $C$ for the sites $t \notin T$ are the cells of the ordinary Voronoi diagram of $P \setminus T$, cut to $C$. The code computes each piece by cutting $C$ with $n - j - 1$ half-planes, one at a time, with the [Sutherland-Hodgman](/sutherland-hodgman/) step for a convex polygon, in exact arithmetic.
- **Line L6.** A cutting step returns no polygon when fewer than three corners remain that are not on one line; such pieces have zero area.
- **Line L7.** By the refinement property, the pieces of $S$ fill $V(S) \cap B$, which is convex. So it is the convex hull of the corners of its pieces, computed by the monotone chain method, which also drops corners inside sides.

**locate(q).** Test each stored polygon with $\mathrm{orient}$ against each side; this takes time linear in the size of the diagram. With a point location structure over the cells, the query takes $O(\log n)$ time, plus $O(k)$ to report the set.

**Lee's iterative method.** Lines L4 and L5 cut each cell by the Voronoi diagram of all the other sites, which is wasteful. D. T. Lee's method cuts each cell only by the Voronoi diagram of the few sites that can be the next nearest site there, which are found from the neighbouring cells, and builds that diagram with an $O(m \log m)$ algorithm for $m$ such sites. This builds the order-$k$ diagram from the order-$1$ diagram in $O(k^2 n \log n)$ time.

## Example

Take $k = 2$ and the five sites $(0,0)$, $(6,0)$, $(3,5)$, $(8,6)$ and $(1,7)$. The site $(3,5)$ is inside the hull of the other four.

- **L1 and the first level.** The box is cut by the ordinary Voronoi diagram of the five sites into the five order-$1$ cells.
- **Second level, lines L3 to L6.** The cell of $(3,5)$ is cut by the Voronoi diagram of the other four sites, and its four pieces go to the pairs $\{(3,5), t\}$. The cell of $(6,0)$ is cut by the Voronoi diagram of $(0,0)$, $(3,5)$, $(8,6)$, $(1,7)$, and its piece of $(3,5)$ also goes to $\{(3,5), (6,0)\}$.
- **L7.** The pair $\{(3,5), (6,0)\}$ gets the convex hull of its two pieces, the bounded pentagon with corners $(3, 8/5)$, $(74/11, -7/11)$, $(83/14, 47/14)$, $(91/22, 87/22)$ and $(3, 22/7)$, in counterclockwise order.

In a box large enough to hold all vertices, the order-$2$ diagram has $8$ cells and $8$ vertices. Two cells are bounded: the pentagon above and the quadrilateral of $\{(0,0), (3,5)\}$ with corners $(-21/2, -13/2)$, $(3, 8/5)$, $(3, 22/7)$ and $(-3/8, 29/8)$. The pairs $\{(0,0), (8,6)\}$ and $\{(6,0), (1,7)\}$, the diagonals of the outer quadrilateral, have no cell. The point $(3,1)$ is at squared distance $10$ from $(0,0)$ and from $(6,0)$ and at $16$ from $(3,5)$, so $\mathrm{locate}((3,1))$ returns $\{(0,0), (6,0)\}$.

For the orders $k = 1, 2, 3, 4, 5$ the numbers of cells are $5, 8, 7, 4, 1$. The order-$4$ cells are the four farthest cells of the hull corners, and the order-$5$ cell is the whole box.

## Correctness

**Theorem.** For distinct integer sites, an order $k \ge 1$ and a box $B$, ORDER-K-BUILD returns, for each set $S$ of $k$ sites with $V(S) \cap B$ of positive area, exactly the polygon $V(S) \cap B$, and no other set. $\mathrm{locate}(q)$ returns a nonempty list of sets of $k$ nearest sites of $q$ for every $q \in B$, and exactly the set of $k$ nearest sites when this set is unique.

The proof is by induction on the level. The refinement property shows that the pieces made from the order-$j$ cells cover each order-$(j+1)$ cell and lie inside it. Pieces of zero area, and pieces made from order-$j$ cells of zero area, do not matter, because a convex polygon of positive area is the closure of what remains when finitely many segments are removed from it. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Size.** For sites in general position the diagram has $O(k(n - k))$ cells, edges and vertices (cited, not proved here). Storing the set $S$ at each cell takes $O(k)$ space per cell, so $O(k^2 (n - k))$ space in all; storing only the change between neighbouring cells takes $O(k(n - k))$ space.
- **Build.** Lee's iterative method takes $O(k^2 n \log n)$ worst-case time. Faster algorithms are known whose time is close to $O(n \log n + k(n - k))$; one is a randomized method of Agarwal, de Berg, Matoušek and Schwarzkopf with expected time $O(k(n - k) \log n + n \log^3 n)$. The whole arrangement of the lifted planes, which holds the diagrams of all orders at once, takes $O(n^3)$ time.
- **The code.** At level $j$ the code makes $O(n^2)$ cutting steps for each cell $C$, and a cutting step takes time linear in the size of the polygon, which is at most the number of sides of $C$ plus $n$. With the size bound, the $O(j(n - j))$ cells of level $j$ have $O(j(n - j))$ sides in all, so level $j$ takes $O(j n^4)$ time and the build takes $O(k^2 n^4)$ time, counting each exact operation as one step. It is a reference implementation for small inputs.
- **Query.** $O(\log n + k)$ with point location over the cells; the code scans the cells.

## Variants

- **Ordered order-k diagram.** Split each cell further by the *order* of the $k$ nearest sites. For $k = 2$ this gives the second-nearest neighbour diagram.
- **k-th nearest site diagram.** Cells by the $k$-th nearest site alone, which is the union of ordered cells with the same last site.
- **Farthest-point diagram.** The case $k = n - 1$, a tree with cells only for hull corners ([farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/)).
- **Higher-order Delaunay triangulations.** Triangulations in which every circumcircle has at most $k$ sites inside generalize the [Delaunay triangulation](/delaunay-triangulation/) in the same direction; they leave room to meet extra constraints, such as the shape of a terrain.
- **Weighted sites.** For the power distance, the order-$k$ power diagram is again the projection of a level of an arrangement of planes ([power diagram](/power-diagram/)).
- **Higher dimensions.** In $\mathbb{R}^d$, the order-$k$ diagram is the projection of the $k$-th level of an arrangement of hyperplanes in $\mathbb{R}^{d+1}$.

## When to use it

Use it when many queries ask for the $k$ nearest sites of a point, for a fixed small $k$ and a fixed set of sites in the plane: for example, the $k$ nearest facilities, or [k-nearest neighbours](/k-nearest-neighbors/) voting with fixed training points. For changing $k$, many sites, or higher dimensions, a [k-nearest neighbour search](/k-nearest-neighbor-search/) with a k-d tree, or with a Delaunay walk and a priority queue, uses far less space.

## Pitfalls

- **Pairs with no cell.** Not every set of $k$ sites has a cell; most do not. A structure indexed by all $\binom{n}{k}$ sets wastes space.
- **The union in line L7 is convex, the pieces are not one polygon.** Merging the pieces by a polygon union in floating point leaves slivers; the convex hull of their corners, in exact arithmetic, is both simpler and exact.
- **Ties at the $k$-th distance.** A point on a cell boundary has several sets of $k$ nearest sites. A query must report one of them, or all of them, by a fixed rule.
- **Degenerate pieces.** With collinear or cocircular sites, some pieces are segments or points. Keeping them gives cells of zero area and wrong neighbour relations.
- **Unbounded cells.** The code clips to a box. A cell that lies outside the box is lost, so the box must hold all vertices when the number of cells matters, as in the example.
- **Cost of the simple method.** Cutting by all other sites at each level, as the code does, is many times slower than Lee's method for large $n$.

## Implementations

## History

M. I. Shamos and D. Hoey described the order-$k$ diagram in 1975 for the $k$ nearest neighbour problem, together with the farthest-point diagram. D. T. Lee in 1982 proved the $O(k(n - k))$ bound on its size and gave the iterative $O(k^2 n \log n)$ algorithm. H. Edelsbrunner and R. Seidel in 1986 showed that the diagrams of all orders are projections of levels in an arrangement of planes. K. L. Clarkson and P. W. Shor used random sampling in 1989 to bound the total size of the diagrams of orders up to $k$, and later work gave algorithms with time near the output size.

## References
