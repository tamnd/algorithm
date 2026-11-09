---
tag: N67PPQ
kind: theorem
slug: two-ears-theorem
name: Two ears theorem
aliases:
- Meisters two ears theorem
- Meisters' two ears theorem
- two-ear theorem
area: geometry/triangulations
level: intro
summary: Every simple polygon with at least four vertices has two non-overlapping ears.
prereqs: [ear, simple-polygon, jordan-curve-theorem, orientation-test]
see_also: [ear-clipping, polygon-triangulation, triangulation-dual-tree, art-gallery-theorem, triangulation]
sources:
  - paper: "Gary H. Meisters, Polygons have ears, American Mathematical Monthly 82(6), 648 to 651 (1975)"
    locator: the theorem and its proof by induction
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2, Triangulation, Theory (existence of a diagonal, existence of a triangulation, and Meisters' theorem through the dual tree)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1, Guarding and Triangulations (existence of a diagonal through the leftmost vertex, and n - 2 triangles)
  - paper: "Godfried T. Toussaint, Anthropomorphic polygons, American Mathematical Monthly 98(1), 31 to 35 (1991)"
    locator: polygons with exactly two ears
---

The two ears theorem says that every [simple polygon](/simple-polygon/) with four or more vertices has at least two [ears](/ear/) whose triangles do not overlap. An ear is a vertex whose two neighbors can be joined by a diagonal, so the theorem gives a triangle that can be cut off, and it can be cut off at two different places. Gary Meisters proved it in 1975. It is the reason that [ear clipping](/ear-clipping/) never gets stuck, and it gives a short proof that every simple polygon has a [triangulation](/polygon-triangulation/).

## Statement

Let $P$ be a simple polygon with $n \ge 4$ distinct vertices; consecutive collinear vertices are allowed. A **diagonal** is a segment between two vertices whose relative interior lies in the interior of $P$. A vertex $v$ with neighbors $u$ and $w$ is an **ear** if $uw$ is a diagonal, and its **ear triangle** is the triangle $uvw$.

**Theorem (Meisters 1975).** $P$ has two ears $v \ne v'$ whose ear triangles have disjoint interiors.

## In plain words

Take any polygon whose boundary does not cross itself and that has at least four corners. You can always find two corners where a straight cut between the two neighbors of the corner stays inside the polygon. Each cut removes a triangle, and the two triangles do not overlap. So you can always shave off a triangle, and after the shave you still have a polygon of the same kind, with one corner fewer.

## Proof

The proof uses two lemmas and an induction on $n$. We take the vertices in counterclockwise order, so the interior lies to the left of each edge.

**Lemma 1 (a diagonal exists).** A simple polygon with $n \ge 4$ vertices has a diagonal.

*Proof.* Let $v$ be the lowest vertex, the leftmost one among the lowest. Its neighbors $u$ and $w$ lie above $v$, or on the horizontal line through $v$ to the right of it. They cannot both be on that line, because then $u$, $v$, $w$ are on the line with $u$ and $w$ on the same side of $v$, and the edges $vu$ and $vw$ would overlap. So $\mathrm{orient}(u, v, w) > 0$: the interior angle at $v$ is less than $\pi$. Let $\Delta$ be the closed triangle $uvw$ and let $S$ be the set of vertices of $P$ in $\Delta$ other than $u, v, w$.

If $S$ is empty, $uw$ is a diagonal; this is Lemma 1 of the [ear clipping correctness proof](/ear-clipping/), whose argument we repeat in the second case. If $S$ is not empty, let $x \in S$ be a vertex at the largest distance from the line $uw$, and let $L$ be the line through $x$ parallel to $uw$. Let $R$ be the closed part of $\Delta$ on the side of $L$ that holds $v$; it is a triangle with corner $v$ and its third side on $L$. No vertex lies in $R$ except $v$ and vertices on $L$. The point $x$ is not on the edges $vu$ or $vw$ (simplicity), so it lies strictly inside the third side of $R$, and the open segment $vx$ lies in the interior of $R$.

An edge $e$ of $P$ that meets the open segment $vx$ must enter $R$. It cannot cross $vu$ or $vw$ (simplicity), and it has no end point in $R$ other than vertices on $L$. So $e \cap R$ is a segment with both ends on $L$, and it lies on $L$. But the open segment $vx$ meets $L$ only at $x$, which is not on it. So no edge meets the open segment $vx$. Points of the open segment near $v$ lie in the interior of $P$, because the angle at $v$ is less than $\pi$ and $x$ lies inside that angle. The open segment is connected and misses the boundary, so all of it lies in the interior. Hence $vx$ is a diagonal. $\square$

**Lemma 2 (cutting along a diagonal).** Let $d = v_i v_j$ be a diagonal of $P$. The two boundary paths from $v_i$ to $v_j$, each closed by $d$, are simple polygons $P_1$ and $P_2$ with $n_1 + n_2 = n + 2$ vertices, $n_1, n_2 \ge 3$. Their interiors are disjoint, and the interior of $P$ is the union of their interiors and the relative interior of $d$.

*Proof.* Each path with $d$ added is a closed polygonal curve; it is simple because the relative interior of $d$ meets no edge. The path from $v_i$ to $v_j$ through $v_{i+1}$ has $j - i + 1$ vertices and the other $n - (j - i) + 1$, so the counts add to $n + 2$. Since $v_i$ and $v_j$ are not adjacent, each path has an inner vertex, so $n_1, n_2 \ge 3$. The arc $d$ splits the Jordan region bounded by $P$ into two regions, bounded by $P_1$ and $P_2$; this is the theta-curve case of the [Jordan curve theorem](/jordan-curve-theorem/). $\square$

**Proof of the theorem.** By strong induction on $n \ge 4$. Take a diagonal $d = v_i v_j$ by Lemma 1, and split $P$ into $P_1$ and $P_2$ by Lemma 2. We show that each $P_k$ holds an ear of $P$ whose ear triangle lies in $P_k$. Two such ears, one from $P_1$ and one from $P_2$, have triangles with disjoint interiors, because the interiors of $P_1$ and $P_2$ are disjoint, and they have different tips, since a tip lies on $d$ only if it is $v_i$ or $v_j$, which we exclude below. This proves the theorem.

1. *$P_k$ is a triangle.* Then $P_k = v_i\, x\, v_j$ for one vertex $x$, and the boundary of $P$ goes $v_i, x, v_j$. So the neighbors of $x$ in $P$ are $v_i$ and $v_j$, and $v_i v_j = d$ is a diagonal of $P$. So $x$ is an ear of $P$, and its ear triangle is $P_k$.
2. *$P_k$ has $n_k \ge 4$ vertices.* Then $n_k < n$, because $n_1 + n_2 = n + 2$ and the other part has at least 3 vertices. By the induction hypothesis, $P_k$ has two ears with disjoint ear triangles. They cannot be $v_i$ and $v_j$ both: $v_i$ and $v_j$ are adjacent in $P_k$, so their ear triangles both have the edge $d$ and lie on the same side of it, inside $P_k$, and two such triangles overlap near the midpoint of $d$. So $P_k$ has an ear $y \notin \{v_i, v_j\}$. The neighbors of $y$ in $P_k$ are its neighbors in $P$, because only $v_i$ and $v_j$ get a new neighbor. The segment between them is a diagonal of $P_k$, so its relative interior lies in the interior of $P_k$, which lies in the interior of $P$ by Lemma 2. So $y$ is an ear of $P$, with its ear triangle in $P_k$.

The base case $n = 4$ is covered: then $n_1 = n_2 = 3$ and case 1 applies to both parts. $\blacksquare$

## Consequences

- **Every simple polygon has a triangulation with $n - 2$ triangles and $n - 3$ diagonals.** Cut an ear and recurse on the polygon with $n - 1$ vertices; a triangle is the base. Each cut makes one triangle and one diagonal. See [polygon triangulation](/polygon-triangulation/).
- **Ear clipping is correct.** [Ear clipping](/ear-clipping/) always finds an ear while four or more vertices remain.
- **Leaves of the dual tree.** In a triangulation of a polygon, the [dual tree](/triangulation-dual-tree/) has $n - 2$ nodes. A leaf is a triangle with two polygon edges, so its middle vertex is an ear. A tree with at least two nodes has at least two leaves, which gives a second proof for $n \ge 4$.
- **Art gallery theorem.** Fisk's proof of the [art gallery theorem](/art-gallery-theorem/) 3-colors a triangulation by induction, removing an ear at each step.
- **A polygon is convex if every vertex is an ear.** The converse holds when no three vertices are collinear.

## Tightness

Two ears cannot be improved to three. For $k \ge 2$, let $L_i = (2i, 2i^2)$ for $0 \le i \le k$ and $U_i = (2i, 2i^2 + 1)$ for $1 \le i \le k - 1$, and let $P$ be the polygon $L_0, L_1, \ldots, L_k, U_{k-1}, \ldots, U_1$, with $n = 2k$ vertices in counterclockwise order: a curved strip that ends in two points. For $k = 3$ this is $(0,0), (2,2), (4,8), (6,18), (4,9), (2,3)$.

- A lower vertex $L_i$ with $1 \le i \le k - 1$ is not an ear. The chord from $L_{i-1}$ to $L_{i+1}$ passes over $x = 2i$ at height $2i^2 + 2$, so the vertex $U_i$ at height $2i^2 + 1$ lies inside the triangle $L_{i-1} L_i L_{i+1}$.
- An upper vertex $U_i$ with $2 \le i \le k - 2$ is reflex: three points of the parabola $y = x^2 / 2 + 1$ taken from right to left turn clockwise, with $\mathrm{orient}(U_{i+1}, U_i, U_{i-1}) = -8$. The vertex $U_{k-1}$ has neighbors $L_k$ and $U_{k-2}$ (or $L_k$ and $L_0$ when $k = 2$), and $U_1$ has neighbors $U_2$ and $L_0$; direct computation gives $\mathrm{orient}(U_2, U_1, L_0) = -6$, $\mathrm{orient}(L_k, U_{k-1}, U_{k-2}) = -6$ for $k \ge 3$, and $\mathrm{orient}(L_2, U_1, L_0) = -4$ for $k = 2$. So all upper vertices are reflex.

So only $L_0$ and $L_k$ can be ears, and by the theorem both are. Toussaint called polygons with exactly two ears anthropomorphic and studied them.

The hypothesis $n \ge 4$ is needed: a triangle has no diagonal, so it has no ear in this sense. Simplicity is needed too: a self-crossing closed curve, such as a bow tie, need not have any vertex whose neighbor segment lies inside.

## History

Gary Meisters published the theorem in 1975 under the title "Polygons have ears", with an induction proof close to the one above. The existence of a triangulation of a simple polygon by diagonals was known before; Meisters noted that ears give a constructive proof. O'Rourke's book derives the theorem from the existence of a triangulation and the leaves of its dual tree. Toussaint (1991) characterized polygons with exactly two ears.

## References
