---
tag: 5BRFPF
kind: concept
slug: canonical-ordering
name: Canonical ordering
aliases:
- canonical vertex ordering
area: graphs/planar-graphs
level: advanced
summary: Vertex ordering of a maximal planar graph whose prefixes induce a sequence of nested polygons.
prereqs: [maximal-planar-graph, rotation-system, planar-face, biconnected-graph]
see_also: [de-fraysseix-pach-pollack, schnyder-woods, st-numbering, planar-straight-line-drawing, fary-theorem, book-embedding, schnyder-drawing, lempel-even-cederbaum-st-numbering]
sources:
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the definition of the canonical ordering and the lemma that every maximal planar graph has one
  - paper: doi:10.1007/BF02086606
    title: Goos Kant, Drawing planar graphs using the canonical ordering, Algorithmica 16(1), 4 to 32 (1996)
    locator: the extension of the canonical ordering to 3-connected planar graphs and its linear-time computation
  - paper: "Marek Chrobak and Thomas H. Payne, A linear-time algorithm for drawing a planar graph on a grid, Information Processing Letters 54(4), 241 to 246 (1995)"
    locator: computing the canonical ordering and the shift drawing in linear time
  - book: "Takao Nishizeki and Md. Saidur Rahman, Planar Graph Drawing, World Scientific, 2004"
    locator: Chapter 4, Straight line drawing (canonical ordering and the shift method)
---

A canonical ordering is a numbering $v_1, v_2, \ldots, v_n$ of the vertices of a [maximal planar graph](/maximal-planar-graph/) such that the graph grows one vertex at a time and keeps a simple outer boundary: each prefix $v_1, \ldots, v_k$ induces a 2-connected plane graph bounded by a cycle through the edge $v_1 v_2$, and the next vertex attaches to a contiguous stretch of that cycle. De Fraysseix, Pach and Pollack introduced it in 1990 to draw planar graphs on a small grid, and it is the starting point for most incremental drawing algorithms. Every maximal planar graph has one, and it can be found in linear time.

## In plain words

Think of building a triangulated shape by adding one point at a time from the bottom up. You start with one triangle that sits on a fixed base edge. Each new point is placed above the current shape and connected to a run of neighbouring points along its upper boundary, with no gaps in that run. The shape never gets a hole or a pinch: its outline stays one simple loop.

A canonical ordering is an order of the vertices that makes this building process possible. It exists for every triangulated planar graph. Drawing algorithms use it because, when a point arrives, all the points it connects to are on the visible upper outline, so there is always room to place it above them.

## The idea

**Input and embedding.** The graph $G$ is maximal planar with $n \ge 3$ vertices and comes with a fixed plane embedding, given as a [rotation system](/rotation-system/) (or as a plane drawing, from which the rotation system is read off). The outer [face](/planar-face/) is a triangle $u, v, w$, listed counterclockwise. Different choices of the outer face give different orderings.

**Definition (de Fraysseix, Pach and Pollack).** A *canonical ordering* of $G$ with respect to the outer face $u, v, w$ is an ordering $v_1 = u$, $v_2 = v$, $\ldots$, $v_n = w$ of the vertices such that, with $G_k$ the subgraph induced by $v_1, \ldots, v_k$ and drawn as in $G$, for every $3 \le k \le n$:

1. $G_k$ is [2-connected](/biconnected-graph/), every bounded face of $G_k$ is a triangle, and the boundary of the outer face of $G_k$ is a cycle $C_k$ that contains the edge $v_1 v_2$;
2. if $k < n$, the vertex $v_{k+1}$ lies in the outer face of $G_k$, and its neighbours in $G_k$ form a path of $C_k - v_1 v_2$ with at least 2 vertices.

Write $C_k$ as a path $c_1 = v_1, c_2, \ldots, c_t = v_2$ (the cycle without the edge $v_1 v_2$). The *contour* $C_k$ is the "upper boundary" of the shape built so far. When $v_{k+1}$ arrives with neighbours $c_p, \ldots, c_q$, the new contour is $c_1, \ldots, c_p, v_{k+1}, c_q, \ldots, c_t$: the vertices $c_{p+1}, \ldots, c_{q-1}$ go under $v_{k+1}$ and never return to the contour.

**Theorem.** Every maximal planar graph with $n \ge 3$ vertices and a fixed outer face $u, v, w$ has a canonical ordering with $v_1 = u$, $v_2 = v$, $v_n = w$.

*Proof.* We choose $v_n, v_{n-1}, \ldots, v_3$ in this order, removing one vertex at a time, and keep the invariant: $G_k$ (the remaining graph) satisfies condition 1. For $k = n$, $G_n = G$: it is 3-connected for $n \ge 4$ and a triangle for $n = 3$, its bounded faces are triangles, and $C_n$ is the triangle $u, v, w$. Set $v_n = w$.

Now let $k \ge 4$, let $G_k$ satisfy condition 1, and write $C_k$ as the path $c_1 = v_1, \ldots, c_t = v_2$. A *chord* of $C_k$ is an edge of $G_k$ between two vertices of $C_k$ that are not consecutive on $C_k$. Since $G_k$ is drawn inside $C_k$, every chord lies inside the disk bounded by $C_k$, and two chords do not cross.

*Claim: some $c_l$ with $1 < l < t$ is on no chord.* If there is no chord, take any $c_l$ with $1 < l < t$; one exists because $t \ge 3$. Otherwise choose a chord $c_i c_j$, $i < j$, with $j - i$ as small as possible. Then $j - i \ge 2$, so some $l$ has $i < l < j$. A chord $c_l c_m$ cannot cross $c_i c_j$, so $i \le m \le j$, and then $|l - m| < j - i$, which contradicts the choice of $c_i c_j$. So $c_l$ is on no chord.

Set $v_k = c_l$ for such an $l$. The bounded faces at $c_l$ are triangles, so its neighbours, in rotation order from $c_{l-1}$ to $c_{l+1}$ through the inside, form a path $c_{l-1} = w_1, w_2, \ldots, w_p = c_{l+1}$ in $G_k$. The inner vertices $w_2, \ldots, w_{p-1}$ are not on $C_k$, because $c_l$ is on no chord. Removing $c_l$ therefore replaces it on the outer boundary by the path $w_1, \ldots, w_p$, and the new boundary $C_{k-1}$ is again a simple cycle through $v_1 v_2$. Bounded faces of $G_{k-1}$ are bounded faces of $G_k$, so they are triangles. A plane graph whose outer boundary is a simple cycle and whose bounded faces are all bounded by cycles is 2-connected, so condition 1 holds for $G_{k-1}$. Condition 2 holds for $v_k$: it lies in the outer face of $G_{k-1}$, and its neighbours in $G_{k-1}$ are exactly the path $w_1, \ldots, w_p$ of $C_{k-1}$, with $p \ge 2$, which avoids the edge $v_1 v_2$ because $1 < l < t$. When $k = 3$, $G_3$ is the triangle $v_1, v_2, v_3$, and the ordering is complete. $\square$

**Computing it in linear time.** The proof is an algorithm. Keep, for each vertex on the current contour, the number of chords at it, and a list of the contour vertices with zero chords other than $v_1, v_2$. Removing $c_l$ puts $w_2, \ldots, w_{p-1}$ on the contour; for each of them, scan its neighbours and count those on the contour that are not its contour neighbours, updating the counts at both ends. Each vertex enters the contour once, and the scan at that moment looks at each of its edges once, so the total work is $O(n + m) = O(n)$ (Chrobak and Payne; Kant).

**A canonical ordering is an st-ordering.** For $3 \le k < n$, the vertex $v_k$ is on $C_k$ and differs from $v_1, v_2, v_n$. A vertex leaves the contour only when a later neighbour covers it, and $C_n$ is the triangle $v_1, v_2, v_n$, so $v_k$ has a neighbour $v_j$ with $j > k$. It also has at least 2 neighbours before it. So, with $s = v_1$ and $t = v_n$, every other vertex has a lower and a higher neighbour, which makes the ordering an [st-numbering](/st-numbering/) (after adding the edge $st$, already present here).

## Examples

**$K_4$.** Draw a triangle $0, 1, 3$ with vertex 2 inside. With outer face $0, 1, 3$, the ordering $0, 1, 2, 3$ is canonical: $G_3$ is the triangle $0, 1, 2$, and vertex 3 is adjacent to the whole contour $0, 2, 1$. It is the only one for this outer face, since $v_3$ must be adjacent to both $v_1$ and $v_2$ and $v_4$ must be 3.

**The octahedron.** Take the points $0 = (0,0)$, $1 = (10,0)$, $2 = (5,9)$, $3 = (5,2)$, $4 = (6.5,4)$, $5 = (3.5,4)$, and join every pair except the opposite pairs $\{0,4\}$, $\{1,5\}$, $\{2,3\}$. This is a straight-line drawing of the octahedron with outer face $0, 1, 2$ and inner triangle $3, 4, 5$. Peeling from the top, as in the proof, gives the canonical ordering $0, 1, 3, 4, 5, 2$:

| $k$ | $v_k$ | neighbours in $G_{k-1}$ | contour $C_k$ from $v_1$ to $v_2$ |
|---|---|---|---|
| 3 | 3 | 0, 1 | 0, 3, 1 |
| 4 | 4 | 3, 1 | 0, 3, 4, 1 |
| 5 | 5 | 0, 3, 4 | 0, 5, 4, 1 |
| 6 | 2 | 0, 5, 4, 1 | 0, 2, 1 |

At $k = 5$, vertex 3 goes under vertex 5 and leaves the contour. Each row's neighbour list is a contiguous part of the previous contour.

**Non-examples.** The ordering $0, 1, 4, \ldots$ fails at once: vertex 4 has only one neighbour, 1, among $\{0, 1\}$. The ordering $0, 1, 3, 5, 4, 2$ is also canonical (vertex 5 attaches to $0, 3$, then vertex 4 to $5, 3, 1$), so canonical orderings are not unique. An ordering that ends with a vertex other than $w$ is never canonical for the outer face $u, v, w$, since $C_n$ must be the outer triangle.

**Single vertex, an edge, a tree.** The definition needs $n \ge 3$ and a maximal planar graph. For a tree or any planar graph that is not maximal, one first triangulates it (adding edges inside faces), computes a canonical ordering, and later deletes the added edges; drawing algorithms do exactly this.

## Where it is used

- **Grid drawings.** The [de Fraysseix-Pach-Pollack algorithm](/de-fraysseix-pach-pollack/) adds the vertices in canonical order and places $v_{k+1}$ at the intersection of lines of slope $+1$ and $-1$ through the ends of its contour path, shifting parts of the drawing to make room. The result is a straight-line drawing on a $(2n - 4) \times (n - 2)$ grid, which proves [Fáry's theorem](/fary-theorem/) with integer coordinates; see [planar straight-line drawing](/planar-straight-line-drawing/).
- **3-connected graphs.** Kant generalized the ordering to 3-connected planar graphs, where each step adds either one vertex or a chain of degree-2 vertices. This gives convex grid drawings, orthogonal drawings and visibility representations.
- **Schnyder woods.** For each $v_k$ with $k \ge 3$, take the edges to its leftmost and rightmost neighbours on the contour, oriented away from $v_k$ into two classes, and orient each edge to a covered contour vertex toward $v_k$ in a third class. This gives a [Schnyder wood](/schnyder-woods/) of $G$. [Schnyder drawings](/schnyder-drawing/) are an alternative route to small grids.
- **st-orderings.** As shown above, a canonical ordering is an st-ordering, so it can feed algorithms that need one, such as visibility representations. For general 2-connected graphs, st-orderings come from the [Lempel-Even-Cederbaum procedure](/lempel-even-cederbaum-st-numbering/).

## References
