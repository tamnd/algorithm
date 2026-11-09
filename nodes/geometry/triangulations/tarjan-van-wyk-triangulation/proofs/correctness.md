---
title: The visibility map pipeline returns a triangulation of the polygon
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, distinct and with no three collinear. "Above" is the $(y, x)$ order. As in every sweep with this order, all statements refer to the picture after a tiny shear $(x, y) \mapsto (x, y + \varepsilon x)$, which keeps all orientation signs and makes the heights of the vertices distinct. A **chord** at $v$ is the horizontal segment from $v$ to the first edge it meets, drawn only when it starts into the interior of $P$. The **visibility map** is the set of all chords, and its faces inside $P$ are the inside trapezoids. This proof covers the pipeline in the code; the $O(n \log \log n)$ computation of the map by Tarjan and Van Wyk is a different way to produce the same map, and the triangulation stage after it is the same.

## Lemma 1: the chord sides

Let $u$ and $w$ be the previous and next vertex of $v$. The interior lies to the left of the boundary direction. If $u$ is above $v$ and $w$ is below, the boundary runs downward through $v$, its left side is east, and only the right ray starts into the interior. If $w$ is above and $u$ is below, the boundary runs upward and only the left ray does. If both are below or both are above, the horizontal line through $v$ meets the boundary near $v$ only at $v$, and both rays start into the interior exactly when the interior angle exceeds $\pi$, that is, when $\mathrm{orient}(u, v, w) < 0$; otherwise neither does. This is `chord_sides`. $\square$

## Lemma 2: the sweep finds the nearest edges

**Invariant.** When the loop of line L2 reaches vertex $v$, the list `active` holds, from left to right, the edges that cross the horizontal line just above $v$, that is, the edges whose upper end point is above $v$ and whose lower end point is $v$ or below it.

*Base.* Before the first vertex, the list is empty and no edge crosses a line above all vertices.

*Step.* Line L3 removes the edges whose lower end point is $v$. The remaining edges cross the line through $v$ at points other than $v$, since no other edge passes through a vertex, and they keep their order, because edges do not cross between two consecutive vertex heights. Each lies entirely left or right of $v$ at that height, and `left_of(s, v)` is false for edges left of $v$ and true for edges right of $v$. This predicate is monotone along the list, so the binary search of line L4 returns the index of the first edge right of $v$. The edges just before and after that index are the nearest edges on the two sides, so the chords recorded on line L5 are correct by Lemma 1. Line L6 inserts the edges whose upper end point is $v$ at that index. When there are two, the edge whose lower end point lies left of the other edge's line is the left one just below $v$. So the list is sorted for the line just below $v$, which is the line just above the next vertex. $\square$

## Lemma 3: reading the trapezoids

Every inside trapezoid $T$ has a left wall and a right wall, which are polygon edges, and a top vertex and a bottom vertex, at which its top and bottom sides lie. The interior of $P$ is to the east of the left wall, so the left wall is directed downward. Along a downward edge $s$, the inside trapezoids to its east are separated by the chords that end on $s$ from the east, and these are left chords. So, listing the upper end point of $s$, the owners of the chords that end on $s$ from top to bottom, and the lower end point of $s$ (line L7), each consecutive pair is the top vertex and the bottom vertex of one trapezoid whose left wall is $s$. The owner of a chord is the top or bottom vertex of the trapezoids it bounds, and an end point of $s$ is the top or bottom vertex of the trapezoid at that end of $s$. Every inside trapezoid appears exactly once in this way. The same holds for right walls on upward edges, with right chords. A top and bottom pair determines at most one trapezoid of a simple polygon: two trapezoids with the same top and bottom vertex would enclose, between them, a region of the exterior that no chord bounds, which would be a hole. So line L8 matches each left wall to its right wall. The number of trapezoids is the number of chords plus one, since each chord joins two boundary points through the interior and splits one face into two. $\square$

## Lemma 4: the diagonals and the monotone pieces

In an inside trapezoid $T$ with top $t$ and bottom $b$, the segment $tb$ joins a point of the top side to a point of the bottom side of the convex set $T$. If $t$ and $b$ are adjacent on the polygon, the edge $tb$ cannot pass through the interior of $T$, so it is a wall, and no diagonal is needed. If they are not adjacent, $tb$ is not a wall, its relative interior lies in the interior of $T$, and it is a diagonal of $P$ (line L9). Diagonals in distinct trapezoids have disjoint relative interiors, so they do not cross.

Each face $Q$ of the cut polygon is monotone. Suppose $v$ were an interior cusp of $Q$ with both neighbors in $Q$ below it and an angle more than $\pi$. The trapezoid $T$ with bottom vertex $v$ that lies directly above $v$ in $Q$ has a top vertex $t$. If $t$ were adjacent to $v$, the edge $tv$ would be a wall of $T$ at $v$ going upward, and $v$ would have a neighbor in $Q$ above it. So $tv$ is a diagonal that leaves $v$ into the interior of $Q$, which is impossible for an edge of the subdivision. The case of a cusp pointing down is symmetric. $\square$

## Lemma 5: the stack triangulation

For a monotone face listed from top to bottom (line L10), the stack holds a reflex chain on one side, ending at the last processed vertex. A vertex on the other chain sees every stack vertex and fans to them (line L11). A vertex on the same chain cuts off triangles while the corner at the top of the stack is strictly convex (line L12), and the final vertex fans to what is left (line L13). Each emitted triangle is cut off along a diagonal of the remaining polygon, so a face with $m$ vertices gives $m - 2$ triangles. $\square$

## Conclusion and termination

With $d$ diagonals there are $d + 1$ faces, whose vertex counts sum to $n + 2d$, so the total number of triangles is $n + 2d - 2(d + 1) = n - 2$. The triangles lie inside $P$ with disjoint interiors, so they form a triangulation (line L14).

The sweep handles each vertex once; the binary search halves an interval of the list at each step; the list of chord owners on each edge is finite; the face tracing visits each directed edge once; and in the stack algorithm every pop emits a triangle or ends an inner loop, and every vertex is pushed at most twice. So the algorithm terminates.
