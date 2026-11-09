---
tag: TDXP76
kind: theorem
slug: art-gallery-theorem
name: Art gallery theorem
aliases:
- Chvatal's art gallery theorem
- Chvátal's art gallery theorem
- Chvátal's theorem
- art gallery theorem
- Fisk's proof of the art gallery theorem
- watchman theorem
area: geometry/polygons
level: core
summary: Floor(n/3) guards always suffice and are sometimes necessary for a simple polygon with n vertices.
prereqs: [simple-polygon, polygon-triangulation, triangulation-dual-tree, graph-coloring]
see_also: [art-gallery-problem, chvatal-art-gallery-theorem, orthogonal-art-gallery-theorem, minimum-guard-np-hardness, visibility-polygon, two-ears-theorem, star-shaped-polygon, ear-clipping]
sources:
  - paper: doi:10.1016/0095-8956(75)90061-1
    title: Václav Chvátal, A combinatorial theorem in plane geometry, Journal of Combinatorial Theory, Series B 18(1), 1975
    locator: the theorem and the first proof, by induction on a triangulation
  - paper: doi:10.1016/0095-8956(78)90059-X
    title: Steve Fisk, A short proof of Chvátal's watchman theorem, Journal of Combinatorial Theory, Series B 24(3), 1978
    locator: the whole note (the 3-coloring of a triangulation)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.1, Art Gallery Theorems (the comb, Fisk's proof, and the 3-coloring through ears)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1, Guarding and Triangulations (the art gallery theorem and the 3-coloring by depth-first search on the dual tree)
  - book: "Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987"
    locator: Chapter 1 (Chvátal's theorem, Fisk's proof, and the comb) and the later chapters on variants
---

The art gallery theorem says that $\lfloor n/3 \rfloor$ guards always suffice to see every point of a simple polygon with $n$ vertices, and that some polygons need that many. Victor Klee asked the question in 1973, and Václav Chvátal proved the answer in 1975. The proof given here is Steve Fisk's from 1978: [triangulate](/polygon-triangulation/) the polygon, color its vertices with three colors so that every triangle gets all three, and put a guard at each vertex of the rarest color. The proof is an algorithm, which places the guards in $O(n)$ time after a triangulation. The question of the *fewest* guards for a given polygon is the [art gallery problem](/art-gallery-problem/), which is [NP-hard](/minimum-guard-np-hardness/).

## Statement

**Notation.** A polygon is a cyclic list of vertices $v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$, and a point is $p = (x, y)$. For a [simple polygon](/simple-polygon/) $P$, $R$ is its closed region: the boundary together with the bounded component of its complement. A point $x \in R$ *sees* a point $y \in R$ if the closed segment $xy$ lies in $R$; the segment may touch the boundary. A set $G \subseteq R$ of *guards* *covers* $P$ if every point of $R$ is seen by some point of $G$.

**Theorem (Chvátal, 1975).** Let $n \ge 3$.

1. *Sufficiency.* Every simple polygon with $n$ vertices is covered by some set of at most $\lfloor n/3 \rfloor$ guards, and the guards can be chosen among the vertices.
2. *Necessity.* There is a simple polygon with $n$ vertices that no set of fewer than $\lfloor n/3 \rfloor$ guards covers, even with guards anywhere in $R$.

So $g(n) = \lfloor n/3 \rfloor$, where $g(n)$ is the largest number of guards that a simple polygon with $n$ vertices can need.

## In plain words

A museum has one floor whose outline is a closed shape with $n$ straight walls. A guard stands still and can look in every direction, but not through walls. How many guards are always enough, whatever the shape?

The answer is one guard for every three corners, rounded down. To see why that is enough, cut the floor into triangles from corner to corner. Paint the corners red, green and blue so that every triangle has one corner of each color. One color is used for at most a third of the corners. Put a guard at each corner of that color: every triangle has such a corner, and from a corner of a triangle you see the whole triangle.

A floor shaped like a comb, with long thin teeth, shows that fewer guards can fail.

## Proof

**Step 1 (triangulate).** Every simple polygon with $n \ge 3$ vertices has a [triangulation](/polygon-triangulation/): a set of $n - 3$ diagonals, segments between vertices that lie in $R$ and meet the boundary only at their endpoints, that cut $R$ into $n - 2$ triangles with disjoint interiors. Its vertices are the vertices of $P$. Let $\mathcal{G}$ be the graph on $v_0, \ldots, v_{n-1}$ whose edges are the polygon edges and the diagonals.

**Step 2 (the graph $\mathcal{G}$ has a proper 3-coloring).** By induction on $n$. For $n = 3$, $\mathcal{G}$ is a triangle; give its vertices three colors. Let $n \ge 4$. The [dual tree](/triangulation-dual-tree/) of the triangulation has a node for each triangle and an arc between two triangles that share a diagonal; it is a tree with $n - 2 \ge 2$ nodes, so it has a leaf. The leaf triangle has exactly one side that is a diagonal, so its other two sides are polygon edges, and they meet at a vertex: the triangle is $v_{i-1} v_i v_{i+1}$ for some $i$, with diagonal $v_{i-1} v_{i+1}$. Each triangle with vertex $v_i$ fills a sector of the interior angle of $R$ at $v_i$, and these sectors do not overlap. The leaf triangle fills the whole angle, as its sides at $v_i$ are both edges at $v_i$, so no other triangle has $v_i$ as a vertex, and $v_i$ has exactly the two neighbors $v_{i-1}$ and $v_{i+1}$ in $\mathcal{G}$. Remove $v_i$. The polygon $v_0, \ldots, v_{i-1}, v_{i+1}, \ldots, v_{n-1}$ is simple, the other $n - 3$ triangles triangulate it, and its graph is $\mathcal{G}$ minus $v_i$. By induction it has a proper 3-coloring. As $v_{i-1}$ and $v_{i+1}$ are adjacent, they have different colors; give $v_i$ the third color. This is a proper 3-coloring of $\mathcal{G}$.

**Step 3 (every triangle has all three colors).** The three vertices of each triangle of the triangulation are pairwise adjacent in $\mathcal{G}$, since the sides of a triangle are polygon edges or diagonals. So in a proper 3-coloring they get three different colors.

**Step 4 (the rarest color guards everything).** The three color classes partition the $n$ vertices, so the smallest class $S$ has $|S| \le \lfloor n/3 \rfloor$, an integer at most $n/3$. Put a guard at each vertex of $S$. Let $x \in R$. Then $x$ is in some triangle $\Delta$ of the triangulation, and by Step 3 some vertex $s$ of $\Delta$ is in $S$. A triangle is convex, so the segment $s x$ lies in $\Delta \subseteq R$, and $s$ sees $x$. This proves sufficiency.

**Step 5 (the comb).** Let $k \ge 1$ and $H = 10$. The comb with $k$ teeth is the polygon with $3k$ vertices

$$(0, 0),\ (3k - 1, 0),\ \text{then, for } j = k - 1 \text{ down to } 0:\ (3j + 1, H) \text{ and, if } j \ge 1, (3j, 1), (3j - 1, 1).$$

Tooth $j$ is the part of $R$ strictly above the line $y = 1$ with $3j \le x \le 3j + 2$; its tip is $t_j = (3j + 1, H)$. The vertices $(3j - 1, 1)$ and $(3j, 1)$ lie on the bottoms of the gaps between teeth, and the part of $R$ strictly above $y = 1$ is the union of the $k$ teeth, which are pairwise disjoint.

Let $g \in R$ see $t_j$. If $g_y > 1$, the whole segment $g t_j$ is above $y = 1$, and it is connected, so it stays in one tooth: $g$ is in tooth $j$. If $g_y \le 1$, the part of the segment above $y = 1$ is connected and ends at $t_j$, so it lies in tooth $j$, and the segment crosses $y = 1$ at a point with $3j \le x \le 3j + 2$. From there it goes down to $g_y \ge 0$ with slope at least $H - 1$ in absolute value, so $g_x$ differs from that point by at most $1/(H - 1) = 1/9$. In both cases $3j - 1/9 \le g_x \le 3j + 2 + 1/9$. These intervals are pairwise disjoint for different $j$, so no guard sees two tips, and $k$ guards are needed.

For $n = 3k$ this gives $\lfloor n/3 \rfloor = k$. For $n = 3k + 1$ or $3k + 2$, replace the bottom edge by a path through one or two extra vertices at height $-1$ below the first tooth. This changes nothing above $y = 0$ except that $g_y \ge -1$, so $g_x$ moves by at most $2/9$ from the crossing point, and the intervals stay disjoint. For $3 \le n \le 5$ one guard is needed in any polygon, and $\lfloor n/3 \rfloor = 1$. This proves necessity. $\blacksquare$

## Consequences

- **An algorithm.** The proof places $\lfloor n/3 \rfloor$ vertex guards in $O(n)$ time after a triangulation: color the vertices of the first triangle, then walk the dual tree by depth-first search and give each new vertex the one color its triangle is missing. With [ear clipping](/ear-clipping/) the whole method takes $O(n^2)$ time, and with Chazelle's linear-time triangulation it takes $O(n)$. Avis and Toussaint gave an $O(n \log n)$ version in 1981.
- **Small polygons are star-shaped.** For $n \le 5$ one guard suffices, so every simple polygon with at most five vertices is [star-shaped](/star-shaped-polygon/): some point sees all of it.
- **The coloring is unique.** The dual tree is connected and each step of the walk forces the color of the new vertex, so the 3-coloring of a triangulated polygon is unique up to renaming the colors.
- **Vertex guards are as good as point guards for the worst case.** The bound $\lfloor n/3 \rfloor$ holds for vertex guards, and the comb needs it even for point guards.
- **An upper bound for the optimization problem.** For every polygon, the minimum number of guards in the [art gallery problem](/art-gallery-problem/) is between 1 and $\lfloor n/3 \rfloor$, and the coloring gives a feasible solution of that size.

## Tightness

**The bound is exact.** The comb of Step 5 shows that $\lfloor n/3 \rfloor$ cannot be lowered for any $n \ge 3$.

**The coloring can be far from optimal.** A convex polygon needs one guard, but the rarest color class has $\lfloor n/3 \rfloor$ vertices. The theorem bounds the worst case, not the optimum of a given polygon.

**Other classes of polygons.** For orthogonal polygons (all edges horizontal or vertical) $\lfloor n/4 \rfloor$ guards suffice and are sometimes necessary; see the [orthogonal art gallery theorem](/orthogonal-art-gallery-theorem/). For polygons with $h$ holes, $\lfloor (n + h)/3 \rfloor$ point guards suffice, and Fisk's coloring argument fails, because a triangulated polygon with holes need not be 3-colorable. For guarding the outside of a polygon (the fortress problem), $\lceil n/2 \rceil$ vertex guards are needed and suffice.

**The proof needs a triangulation by diagonals.** The 3-coloring exists because the graph of a triangulated simple polygon is outerplanar. A triangulation with interior Steiner points can have a graph that needs four colors.

## History

Victor Klee posed the question in 1973 in a conversation with Václav Chvátal, who proved the $\lfloor n/3 \rfloor$ bound by an induction on triangulations in 1975. Steve Fisk found the three-coloring proof given here in 1978; it is often cited as a proof from the book. Avis and Toussaint turned it into an $O(n \log n)$ algorithm in 1981. Kahn, Klawe and Kleitman proved the $\lfloor n/4 \rfloor$ bound for orthogonal polygons in 1983. Joseph O'Rourke's 1987 book Art Gallery Theorems and Algorithms collected the many variants, and Lee and Lin showed in 1986 that finding the minimum number of guards is NP-hard.

## References
