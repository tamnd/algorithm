---
title: Seidel's triangulation returns a triangulation of the polygon
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, no three collinear. "Above" means larger in the order of $(y, x)$. The shear $\sigma(x, y) = (x, y + \varepsilon x)$ with a small enough $\varepsilon > 0$ has determinant 1, so it keeps every orientation sign, and it turns the $(y, x)$ order of the vertices into the order of their new $y$ coordinates. Every statement below is about the sheared picture, where all vertices have distinct $y$ coordinates and "horizontal" means horizontal after the shear; since $\sigma$ maps segments to segments and keeps crossings and incidences, the conclusions hold for $P$ itself.

## Part 1: the trapezoidal decomposition

For a set $S$ of non-crossing segments and a set $V$ of points containing their end points, the **decomposition** $\mathcal{T}(S, V)$ cuts the plane by a horizontal segment through each point of $V$, extended left and right until it hits a segment of $S$ or goes to infinity. Its faces are trapezoids, each described by its top vertex, bottom vertex, left segment and right segment, with `None` for the unbounded sides.

**Invariant.** After each call of `add_point` and each call of `insert`, the leaves of the DAG are exactly the trapezoids of $\mathcal{T}(S, V)$ for the inserted segments $S$ and points $V$, and following the DAG from the root with a point (line L4) ends at the leaf whose trapezoid contains it.

*Initially*, $S = V = \emptyset$ and the single leaf is the whole plane.

*Adding a point $p$ (lines L3 to L5).* Line L4 finds the trapezoid $t$ containing $p$; by induction it is correct, because at a point node the region of the node is split by the cut at that point, and at a segment node the region lies within the vertical span of the segment and is split by it. The new cut at $p$ ends at the left and right segments of $t$, because the cut cannot leave $t$ without crossing them, so it splits $t$ into the part above $p$ and the part below, with the same left and right segments. Line L5 turns the leaf into a point node with these two leaves. No other trapezoid changes.

*Inserting a segment $s$ (lines L6 to L9).* Both end points are now in $V$. The trapezoids met by the open segment $s$ are found on line L6 by searching the DAG: at a point node with point $r$, the open segment lies entirely below the cut of $r$ if its top is not above $r$, entirely above if its bottom is not below $r$, and on both sides otherwise; at a segment node $t'$, the region of the node lies within the span of $t'$, and since $s$ and $t'$ do not cross, the part of $s$ in that region lies on one side of $t'$, which `new_is_left` decides from an end point of one segment that lies strictly inside the span of the other. So the search reaches exactly the leaves whose trapezoids meet $s$. These trapezoids $t_1, \ldots, t_k$ form a vertical stack along $s$: sorted from top to bottom, the bottom vertex of $t_i$ is the top vertex of $t_{i+1}$, a vertex $w_i$ whose cut crosses $s$.

Inserting $s$ cuts each $t_i$ into a part left of $s$ and a part right of $s$ (line L7). It also shortens each cut through $w_i$: the half of the cut on the far side of $s$ from $w_i$ now ends at $s$ and disappears. If $w_i$ lies left of $s$, the right parts of $t_i$ and $t_{i+1}$ are no longer separated, and they have the same right segment, the one the cut used to reach, so they merge into one trapezoid with the top of the upper and the bottom of the lower; symmetrically on the other side (line L8). Every other trapezoid of the old decomposition does not meet $s$ and is unchanged. Line L9 turns each leaf $t_i$ into a segment node whose two children are the (possibly shared) pieces, so the DAG keeps answering point queries correctly. $\square$

**Counting.** After all segments are inserted, the decomposition of the $n$ polygon edges and $n$ vertices has $2n + 1$ trapezoids: each vertex adds a cut with two halves, the $n$ edges add nothing beyond them, and each half of a cut increases the number of faces by one.

**The inside trapezoids.** A trapezoid lies inside $P$ exactly when its left segment exists and the polygon interior lies to its right. Because $P$ is counterclockwise, the interior is to the left of each directed edge $v_i v_{i+1}$; an edge directed downward has its left side on the east, which is the side of the trapezoid. So line L10 keeps a trapezoid exactly when its left segment exists and is directed downward, and the inside trapezoids cover $P$ with disjoint interiors.

## Part 2: the monotone pieces

Line L12 adds, in each inside trapezoid $T$ whose top $u$ and bottom $w$ are not both end points of the left segment or both of the right segment (line L11), the segment $uw$. The vertices $u$ and $w$ lie on the top and bottom sides of $T$, so $uw$ lies in the closed convex set $T$, and its relative interior lies in the interior of $T$, since it cannot run along a side of $T$ (that would make $u$ and $w$ end points of the same side segment). Interiors of distinct trapezoids are disjoint and lie in the interior of $P$. So the added segments are diagonals of $P$, and no two of them cross.

**Lemma 1.** Every face $Q$ of the subdivision of $P$ by these diagonals is monotone.

*Proof.* A polygon is monotone with respect to the $y$ direction if it has no **interior cusp**: a vertex whose two neighbors on the polygon both lie below it, or both above it, and whose interior angle exceeds $\pi$ (de Berg, Cheong, van Kreveld and Overmars, Lemma 3.4). Suppose $v$ is a vertex of $Q$ whose neighbors in $Q$ both lie below $v$ and whose angle in $Q$ exceeds $\pi$. Then the directions just above $v$ point into $Q$, so the trapezoid $T$ directly above $v$, the one with bottom vertex $v$, has its interior near $v$ inside $Q$. If $v$ were an end point of the left or right segment of $T$, that segment would be a polygon edge leaving $v$ upward on the boundary of $T$, hence on the boundary of $Q$ at $v$, and $v$ would have a neighbor in $Q$ above it. So $v$ is an end point of neither, line L11 does not skip $T$, and the diagonal from $v$ to the top of $T$ was added. That diagonal leaves $v$ upward into the interior of $T$, which near $v$ is the interior of $Q$; but diagonals are edges of the subdivision and cannot enter the interior of a face. This contradiction rules out the cusp; the case with both neighbors above is symmetric, with the trapezoid directly below $v$. $\square$

The faces are traced by turning, at each vertex, to the next edge clockwise from the one we arrived on, which follows each face with the face on the left; the faces with positive signed area are the inner ones, the pieces of $P$.

## Part 3: triangulating a monotone piece

Let $Q$ be a monotone piece with $m$ vertices, listed counterclockwise. The vertices after the top and before the bottom form the left chain, the others the right chain. Line L13 sorts them from top to bottom as $u_1, \ldots, u_m$.

**Invariant.** Before $u_j$ is processed ($3 \le j \le m - 1$), the stack holds vertices $s_1, \ldots, s_k$ from bottom to top, $k \ge 2$, such that: they are a contiguous part of one chain, plus possibly the top vertex at the bottom of the stack; $s_k = u_{j-1}$; every interior angle of $Q$ at $s_2, \ldots, s_{k-1}$ is at least $\pi$ in the part of $Q$ not yet cut off (the stack is a reflex chain); and the part of $Q$ above the cut through $u_{j-1}$ not yet cut off is the region bounded by the stack chain, the edge from $s_1$ down the other chain, and the cut.

*Opposite chain (line L14).* If $u_j$ lies on the other chain, it sees every stack vertex: the region between the reflex stack chain and the edge from $s_1$ to $u_j$ contains no other vertex, so each segment $u_j s_i$ is a diagonal, and the triangles $u_j s_i s_{i-1}$ cut off this region. Afterwards the stack is $u_{j-1}, u_j$, which satisfies the invariant.

*Same chain (line L15).* If $u_j$ lies on the same chain as $s_k$, the segment from $u_j$ to $s_{k-1}$ is a diagonal exactly when the angle at $s_k$ between them is convex on the inside, which is the orientation test of line L15 (positive for the left chain, negative for the right one, strict because no three vertices are collinear). Each such triangle is cut off and the test is repeated with the new top. When it fails, the remaining stack with $u_j$ pushed is again reflex.

*The last vertex (line L16).* The bottom vertex $u_m$ is adjacent to the last vertices of both chains and sees every stack vertex, by the same argument as the opposite chain case, so the final fan completes the triangulation.

Each step cuts off a triangle with positive area whose sides are edges or diagonals of $Q$, so the output is a triangulation of $Q$ with $m - 2$ triangles.

## Conclusion and termination

The pieces partition $P$, and line L17 joins their triangulations. A piece with $m_i$ vertices gives $m_i - 2$ triangles; with $d$ diagonals there are $d + 1$ pieces and $\sum_i m_i = n + 2d$, so the total is $n + 2d - 2(d + 1) = n - 2$, the number of triangles of every triangulation of $P$, and every triangle is inside $P$ with disjoint interiors.

Every loop terminates: the insertion loop runs over the $n$ edges once; each DAG search visits each node at most once, since visited nodes are recorded and the DAG is finite and acyclic (every new node is a child of a former leaf); the face tracing visits each directed edge once; and in the stack algorithm every vertex is pushed at most twice per piece and every pop emits a triangle or ends a loop.
