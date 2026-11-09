---
title: The visibility map stage returns a triangulation of the polygon
proves: [correctness, termination]
status: full
---

**Scope.** This proof covers the code: a brute-force visibility map followed by the linear-time conversion to triangles that ends Chazelle's algorithm. The correctness of Chazelle's linear-time construction of the map is proved in his paper; it produces the same map, so the second half of this proof applies to it unchanged.

**Setting.** $P$ is a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, distinct and with no three collinear. "Above" is the $(y, x)$ order, and all geometric words refer to the picture after a tiny shear $(x, y) \mapsto (x, y + \varepsilon x)$, which keeps orientation signs and gives the vertices distinct heights. A **chord** at $v$ is the horizontal segment from $v$ to the first edge it meets, drawn when it starts into the interior. The faces of $P$ cut by all chords are the inside trapezoids.

## Lemma 1: the rays that start into the interior

Let $u$ and $w$ be the neighbors of $v$ before and after it. The interior lies to the left of the boundary direction. If $u$ is above and $w$ below, the boundary runs downward through $v$ and only the eastward ray starts inside; if $w$ is above and $u$ below, only the westward ray does. If both neighbors are on the same side, both rays start inside when $\mathrm{orient}(u, v, w) < 0$ (a reflex angle) and neither does otherwise. Line L2 encodes this. $\square$

## Lemma 2: the nearest edge

An edge $s$ meets the horizontal line through $v$ at a point other than $v$ exactly when $v$ is strictly inside its span (`spans`), and that point is east of $v$ exactly when $v$ is left of the upward line of $s$. Two such edges both meet the line through $v$ and do not cross, so one is left of the other on the whole common part of their spans. `is_left` decides this from an end point of one edge that lies strictly inside the span of the other and is not shared; such a point exists because the spans overlap and distinct edges have at most one common end point. Line L3 keeps, among the edges on each side, the one nearest to $v$, so the recorded edge is where the chord ends. $\square$

## Lemma 3: the trapezoids

The left wall of an inside trapezoid is an edge with the interior to its east, which for a counterclockwise polygon is an edge directed downward. The chords that end on a downward edge $s$ come from the east and cut $s$ into the left sides of the trapezoids along it. So the consecutive pairs in the list (upper end of $s$, owners of the chords ending on $s$ from top to bottom, lower end of $s$) are the top and bottom vertices of these trapezoids (line L4), and the same is true of right walls on upward edges. In a simple polygon a top and bottom pair belongs to one trapezoid only, so left and right walls match. Since every chord crosses the interior from boundary to boundary and splits one face into two, there is one more trapezoid than chords. $\square$

## Lemma 4: the diagonals cut $P$ into monotone mountains

Let $T$ be an inside trapezoid with top $t$ and bottom $b$. If $t$ and $b$ are adjacent on $P$, the edge $tb$ joins the top and bottom sides of the convex set $T$ and cannot enter its interior, so it is a wall. Otherwise $tb$ crosses the interior of $T$ and is a diagonal of $P$ (line L5). Diagonals in different trapezoids have disjoint relative interiors, and no chord crosses a diagonal, because a chord at a height strictly between $t$ and $b$ would cross the interior of $T$.

Let $Q$ be a face of $P$ cut by these diagonals, with $m$ vertices.

*$Q$ is monotone.* At a vertex $v$ of $Q$ with both $Q$-neighbors below and a reflex angle in $Q$, the trapezoid directly above $v$ inside $Q$ has bottom $v$ and some top $t$. The segment $tv$ is either a wall of that trapezoid going up from $v$, which would be an edge of $Q$ above $v$, or a diagonal entering the interior of $Q$. Both contradict the assumption, and the case of a reflex vertex with both neighbors above is symmetric. So $Q$ has no interior cusp, and every horizontal line meets $Q$ in one interval at most.

*$Q$ is a mountain.* Let $u_1, \ldots, u_m$ be the vertices of $Q$ from top to bottom. For $1 < j < m$, the ray at $u_j$ into $Q$ crosses $Q$ and is part of the chord at $u_j$. No other chord meets the interior of $Q$, since chords stop at edges and cross no diagonal. So the $m - 2$ chords at $u_2, \ldots, u_{m-1}$ cut $Q$ into $m - 1$ horizontal layers, and the layer between $u_j$ and $u_{j+1}$ lies in one trapezoid $T_j$ whose top is $u_j$ and whose bottom is $u_{j+1}$. If $u_j$ and $u_{j+1}$ are not adjacent on $P$, the diagonal of $T_j$ joins them, and since it runs from the top to the bottom of $T_j$ it bounds the layer, so it is an edge of $Q$. If they are adjacent, $T_j$ contains no diagonal, so $T_j$ lies inside $Q$ and its wall $u_j u_{j+1}$ is an edge of $Q$. Either way, $u_j u_{j+1}$ is an edge of $Q$ for every $j$. These are $m - 1$ distinct edges of the cycle $Q$ that form a path through all its vertices, so the last edge of $Q$ joins $u_m$ to $u_1$. Thus the bottom and the top of $Q$ are adjacent, and the rest of the boundary is a chain that descends in height. $\square$

## Lemma 5: triangulating a mountain

Let $Q$ be a monotone mountain with base edge $u_1 u_m$ and chain $u_1, \ldots, u_m$ in height order (line L6). All chain vertices other than $u_1$ and $u_m$ lie strictly on one side of the line through the base, because at each height $Q$ is the interval between the base and the chain, and the chain cannot change sides without meeting the base.

*Ears.* If a chain vertex $c$ with chain neighbors $a$ above and $d$ below has a strictly convex angle in $Q$, then $acd$ is an ear. The triangle lies on the chain side of the base line, so it does not meet the base. Every other edge of the chain has both end points at heights outside the open range between $a$ and $d$, so it does not enter the triangle, and no vertex lies in that range other than $c$. So $ad$ is a diagonal of $Q$, and removing $c$ leaves a smaller monotone mountain.

*The stack.* The loop of lines L7 and L8 keeps the invariant that the stack is the part of the current mountain's chain from $u_1$ to the last pushed vertex, and every corner strictly inside the stack is reflex. Pushing $u_j$ may make the corner at the second vertex from the top convex; then that vertex is an ear by the previous paragraph, the triangle is output with the orientation of $Q$, and the vertex is removed, after which the corner below it is tested. When all vertices are pushed, the remaining mountain is the stack plus the base, and its only possibly convex vertices are $u_1$ and $u_m$. A polygon has at least three convex vertices, so nothing is left but the base: the stack has exactly two vertices, and $m - 2$ triangles were output. $\square$

## Conclusion and termination

With $d$ diagonals there are $d + 1$ mountains whose vertex counts sum to $n + 2d$, so line L9 returns $n + 2d - 2(d + 1) = n - 2$ triangles inside $P$ with disjoint interiors, which is a triangulation of $P$.

The map is computed by two nested loops over the vertices and the edges; reading the trapezoids handles each chord end once; the face tracing visits each directed edge once; and in the mountain loop each vertex is pushed once and removed at most once. So the algorithm terminates.
