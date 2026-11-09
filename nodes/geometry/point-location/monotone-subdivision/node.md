---
tag: 707GVV
kind: definition
slug: monotone-subdivision
name: Monotone subdivision
aliases:
- y-monotone subdivision
- x-monotone subdivision
- regular planar graph
- regular PSLG
area: geometry/point-location
level: advanced
summary: A subdivision whose edges are monotone chains, which allows a simple search by a binary search on the chains.
prereqs: [planar-subdivision, monotone-polygon]
see_also: [chazelle-monotone-point-location, monotone-polygon-partition, planar-point-location, multiple-list-search, catalog-graph, slab-method-point-location, trapezoidal-map]
sources:
  - paper: doi:10.1137/0206043
    title: D. T. Lee and Franco P. Preparata, Location of a point in a planar subdivision and its applications, SIAM Journal on Computing 6(3), 1977
    locator: regular planar graphs, the regularization by plane sweep, and the complete set of separating chains (DOI to be checked)
  - paper: doi:10.1137/0215023
    title: Herbert Edelsbrunner, Leonidas J. Guibas and Jorge Stolfi, Optimal point location in a monotone subdivision, SIAM Journal on Computing 15(2), 1986
    locator: the definition of monotone subdivisions, the ordering of the faces and the separators (DOI to be checked)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2.2.2, The chain method (regular graphs, regularization and separating chains), to be checked
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.2, Partitioning a polygon into monotone pieces (split and merge vertices, and the sweep that removes them)
---

## Definition

**Notation.** $P$ is the set of vertices, $n$ the number of edges, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. The output size $h$ and the predicate $\mathrm{incircle}$ are not used on this page. Points are ordered by $p <_{\mathrm{lex}} p'$ if $x < x'$, or $x = x'$ and $y < y'$. This is the order of the $x$-coordinates after the symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$, so in it no two vertices share an $x$-coordinate and no edge is vertical.

**Monotone chains.** A polygonal chain $u_0 u_1 \cdots u_k$ is *$x$-monotone* if $u_0 <_{\mathrm{lex}} u_1 <_{\mathrm{lex}} \cdots <_{\mathrm{lex}} u_k$. In the sheared plane, every vertical line meets such a chain in at most one point. A chain is $y$-monotone when the same holds with the roles of $x$ and $y$ exchanged. Every statement on this page for $x$ holds for $y$ after a rotation of the plane by 90 degrees, which preserves $\mathrm{orient}$; Lee and Preparata state the chain method with $y$-monotone chains, and the pages on this site use $x$-monotone chains to match [vertical ray shooting](/vertical-ray-shooting/).

**Regular graph.** Let $G$ be a [planar straight-line graph](/planar-subdivision/) with vertices $v_1 <_{\mathrm{lex}} v_2 <_{\mathrm{lex}} \cdots <_{\mathrm{lex}} v_N$, $N \ge 2$. A vertex $v_j$ is *regular* if it has an edge to some $v_i$ with $i < j$ and an edge to some $v_k$ with $k > j$. The graph is *regular* if every vertex other than $v_1$ and $v_N$ is regular.

**Monotone subdivision.** A *monotone subdivision* (with respect to $x$) is the subdivision of a regular graph. Edelsbrunner, Guibas and Stolfi state the definition as: every face is a monotone polygon, where the unbounded face is split into an upper and a lower part by two vertical rays from $v_1$ and $v_N$ to infinity. On this site the regular form is the definition, because it is the one that the algorithms check and use. By Proposition 1, every bounded face of a regular graph is an $x$-monotone polygon; the U shape below shows that monotone bounded faces alone are not enough, since the outer boundary must be monotone too.

**Proposition 1 (faces of a regular graph).** If $G$ is regular, then $G$ is connected, and every bounded face of its subdivision is the interior of a simple $x$-monotone polygon (without holes).

*Proof.* Connected: from any vertex $v_j \ne v_1$, follow edges to smaller vertices; the index decreases, and the walk can stop only at $v_1$, so every vertex is joined to $v_1$. No holes: if a bounded face $F$ had an inner boundary component $K$, the lexicographically smallest vertex $w$ of $K$ has all its edges going to larger vertices, since every edge at $w$ lies in $K$. Then $w$ is not regular, and $w \ne v_1$ because the outer boundary of $F$ surrounds $K$ and has a smaller vertex. Monotone: a simple polygon is $x$-monotone exactly when it has no vertex whose two polygon neighbors are on the same side of it in the order $<_{\mathrm{lex}}$ while the interior angle is larger than $\pi$ (a split or merge vertex, de Berg et al., Section 3.2). At such a vertex $v$ of $F$, say with both neighbors larger, the interior of $F$ covers all directions near $v$ that point to smaller vertices, so a regular $v$ would need an edge into $F$, which is impossible. And $v$ is not $v_1$ or $v_N$, which have no larger or no smaller vertex in the plane at all. $\blacksquare$

**Separating chains.** A *complete family of separating chains* of a regular graph $G$ is a sequence of $x$-monotone chains $C_0, C_1, \ldots, C_r$ from $v_1$ to $v_N$ along edges of $G$ such that:

1. every edge of $G$ is in at least one chain;
2. $C_{i}$ is below $C_{i+1}$: no point of $C_{i+1}$ lies strictly below a point of $C_i$ with the same sheared $x$-coordinate;
3. the region strictly between $C_{i-1}$ and $C_i$ is one bounded face, for $i = 1, \ldots, r$.

**Theorem 2 (Lee and Preparata 1977).** A regular graph whose subdivision has $f$ bounded faces has a complete family of $f + 1$ separating chains, and the number of chains through each edge, which describes the family, can be computed in $O(n)$ time from the DCEL.

The construction orders the bounded faces by a topological order of the relation "$F$ is directly below $F'$" (they share an edge, with $F$ on its lower side), which is acyclic for a regular graph. Then $C_i$ is the upper boundary of the union of the first $i$ faces in that order together with the lower outer boundary. Condition 3 holds because each step adds one face, and the union stays bounded by two monotone chains by Proposition 1. An edge with the face $F$ below it and the face $F'$ above it is then in the chains $C_i$ for $\mathrm{index}(F) \le i < \mathrm{index}(F')$, where the outer face counts as $0$ below the graph and as $f + 1$ above it; this is how Edelsbrunner, Guibas and Stolfi describe the family. Lee and Preparata instead give each edge a weight, the number of chains through it, with two sweeps that balance the flow of chains at each vertex.

**The point location test.** For a point $q$ and an $x$-monotone chain $C$ from $v_1$ to $v_N$, with $v_1 <_{\mathrm{lex}} q <_{\mathrm{lex}} v_N$, find the edge $(a, b)$ of $C$ with $a \le_{\mathrm{lex}} q <_{\mathrm{lex}} b$ by binary search, then $\mathrm{orient}(a, b, q)$ tells whether $q$ is above $C$ ($> 0$), on it ($= 0$), or below it ($< 0$). By condition 2, "$q$ is above $C_i$" is monotone in $i$, so a second binary search over the chains finds the face of $q$. This is the chain method: $O(\log^2 n)$ query time in the simple form and $O(\log n)$ with [fractional cascading](/multiple-list-search/), see [point location in monotone subdivisions](/chazelle-monotone-point-location/).

**Regularization.** Every PSLG with $n$ edges can be made regular by adding $O(N)$ new edges that cross nothing, by two [plane sweeps](/sweep-line-technique/) in $O(n \log n)$ time: a sweep from left to right joins each vertex with no edge to the left to a suitable vertex of the slab to its left, and a sweep from right to left does the same for edges to the right. This is the same sweep that [partitions a polygon into monotone pieces](/monotone-polygon-partition/) by removing its split and merge vertices. A point located in the regularized subdivision is in the original face that contains its new face, which is stored with each new face.

## Examples and non-examples

**A regular graph with four faces.** Take the vertices $a = (0,2)$, $b = (2,0)$, $c = (2,4)$, $d = (4,2)$, $e = (6,0)$, $f = (6,4)$, $g = (8,2)$ and the ten edges $ab$, $ac$, $bd$, $cd$, $be$, $cf$, $de$, $df$, $eg$, $fg$. In lexicographic order the vertices are $a, b, c, d, e, f, g$. Vertex $d$ has the edges to $b$ and $c$ on the left and to $e$ and $f$ on the right; $b$ has $a$ on the left and $d, e$ on the right; $c$, $e$ and $f$ are checked the same way, so the graph is regular. It has $V = 7$, $E = 10$, and $f = 4$ bounded faces: the triangle $bed$, the quadrilateral $abdc$, the quadrilateral $defg$ and the triangle $cdf$. Euler's formula gives $7 - 10 + 5 = 2$. One topological order of the faces from bottom to top is $bed$, $abdc$, $defg$, $cdf$, and the five separating chains are:

| chain | vertices | the face just below it |
|---|---|---|
| $C_0$ | $a, b, e, g$ | the unbounded face |
| $C_1$ | $a, b, d, e, g$ | triangle $bed$ |
| $C_2$ | $a, c, d, e, g$ | quadrilateral $abdc$ |
| $C_3$ | $a, c, d, f, g$ | quadrilateral $defg$ |
| $C_4$ | $a, c, f, g$ | triangle $cdf$ |

Edge $de$ is in $C_1$ and $C_2$, and edge $ac$ is in $C_2$, $C_3$ and $C_4$. The chains hold $3 + 4 + 4 + 4 + 3 = 18$ edge entries for $10$ edges. The query $q = (3, 1)$ is above $C_0$, since $\mathrm{orient}(b, e, q) = \mathrm{orient}((2,0), (6,0), (3,1)) = 4 > 0$, and against the edge $bd$ of $C_1$ it gives $\mathrm{orient}((2,0), (4,2), (3,1)) = 0$, so $q$ is on the edge $bd$. The query $q = (3, 2)$ is above $C_1$ ($\mathrm{orient}(b, d, q) = 2 > 0$) and below $C_2$ ($\mathrm{orient}(c, d, q) = (4-2)(2-4) - (2-4)(3-2) = -2 < 0$), so it is in the face $abdc$.

**Long shared edges.** In general the chains of a complete family hold $\Theta(n^2)$ edge entries in total. Take an $x$-monotone path of $n/2$ edges from $v_1$, followed on its right by a stack of $n/2$ thin faces one above the other: every chain contains the whole path, so the $n/2 + 1$ chains hold more than $n^2/4$ entries. The chain method stores each edge only once, at the highest node of its balanced tree of chains whose chain contains the edge.

**Non-example: a hole.** A square with a triangle inside it is not regular: the leftmost vertex of the triangle has no edge to the left. Two edges that join it to the left side of the square make it regular.

**Non-example: a U shape.** The polygon $(0,0), (6,0), (6,2), (2,2), (2,4), (6,4), (6,6), (0,6)$ is a U that opens to the right. The vertical line $x = 4$ meets its interior in two intervals, $0 < y < 2$ and $4 < y < 6$, so it is not $x$-monotone. As a graph of its eight edges it is not regular: $(2,2)$ has the neighbors $(6,2)$ and $(2,4)$, both lexicographically larger, and $(6,2)$ has the neighbors $(6,0)$ and $(2,2)$, both smaller. The edge from $(0,0)$ to $(2,2)$ splits the inside into two $x$-monotone faces, but the graph is still not regular, because of $(6,2)$: monotone bounded faces are not enough, the outer boundary must be monotone too. The edge from $(6,2)$ to $(6,4)$ closes the mouth of the U with a third face, and then the graph is regular, with $V = 8$, $E = 10$ and $3$ bounded faces.

**Non-example: crossing chains.** A family of chains in which $C_1$ goes above $C_2$ somewhere and below it elsewhere does not satisfy condition 2, and the binary search over chains is then invalid even though each chain is monotone.

## Related definitions

A [monotone polygon](/monotone-polygon/) is a single face of this kind. A [planar subdivision](/planar-subdivision/) is the general case. The [trapezoidal map](/trapezoidal-map/) refines any subdivision into trapezoids, which are $x$-monotone faces. Every [triangulation of a point set](/triangulation-of-point-set/) is regular: an interior vertex is surrounded by its neighbors, and a hull vertex other than the leftmost and the rightmost has its two hull neighbors on both sides. The separating chains are a total order of the faces compatible with the "below" relation, the same relation that a sweep line reads off in the [slab method](/slab-method-point-location/). The [catalog graph](/catalog-graph/) of fractional cascading is, for the chain method, the balanced tree of chains.

## References
