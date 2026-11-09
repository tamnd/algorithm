---
tag: KH2F9W
kind: data-structure
slug: visibility-graph
name: Visibility graph
aliases:
- visibility graph of polygonal obstacles
- V-graph
area: geometry/geometric-optimization
level: core
summary: Graph on the obstacle corners that joins two corners when the segment between them avoids every obstacle; Dijkstra on it gives shortest paths in the plane.
model: real-ram
complexity:
  vars: {n: the number of obstacle vertices, m: the number of edges of the graph}
  time: {build: O(n^3) worst case, sweep_build: O(n^2 log n) worst case, query: O(n^2 + m log n) worst case}
  space: {total: O(n + m) worst case}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1979
  people: [Tomás Lozano-Pérez, Michael A. Wesley]
  note: Lozano-Pérez and Wesley planned collision-free paths by shortest paths in the visibility graph of the grown obstacles; Lee (1978) built the graph in O(n^2 log n) time.
prereqs: [simple-polygon, orientation-test, dijkstra]
see_also: [euclidean-shortest-path, visibility-graph-of-polygon, euclidean-shortest-path-in-polygon, rotational-sweep, motion-planning, configuration-space, visibility-polygon, polygon-with-holes]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 15, Sections 15.1 and 15.2 (a shortest path is a polygonal path whose inner vertices are obstacle vertices; the O(n^2 log n) rotational sweep)
  - paper: doi:10.1145/359156.359164
    title: Tomás Lozano-Pérez and Michael A. Wesley, An algorithm for planning collision-free paths among polyhedral obstacles, Communications of the ACM 22(10), 1979
    locator: the visibility graph of the grown obstacles and the shortest path search on it
  - paper: "D. T. Lee, Proximity and reachability in the plane, PhD thesis, University of Illinois at Urbana-Champaign, 1978"
    locator: the O(n^2 log n) construction by an angular sweep around each vertex
  - paper: doi:10.1016/0020-0190(85)90044-4
    title: Emo Welzl, Constructing the visibility graph for n line segments in O(n^2) time, Information Processing Letters 20(4), 1985
    locator: the O(n^2) construction from the arrangement of the dual lines
  - paper: doi:10.1137/0220055
    title: Subir Kumar Ghosh and David M. Mount, An output-sensitive algorithm for computing visibility graphs, SIAM Journal on Computing 20(5), 1991
    locator: the O(n log n + m) construction for polygonal obstacles
---

The visibility graph of a set of polygonal obstacles in the plane has a node for each obstacle vertex, and an edge between two nodes when the segment between them does not enter the interior of any obstacle. The length of an edge is the [Euclidean distance](/euclidean-distance/) between its ends. Add a start $s$ and a target $t$ as two more nodes, and a shortest path from $s$ to $t$ in this graph, found by [Dijkstra's algorithm](/dijkstra/), is a shortest path in the plane that avoids the obstacles. This is the classical method for the [Euclidean shortest path](/euclidean-shortest-path/) problem and for [motion planning](/motion-planning/) of a point or a translating polygon. The graph has $O(n^2)$ edges for $n$ obstacle vertices and can be built in $O(n^2 \log n)$ time by a [rotational sweep](/rotational-sweep/).

## In plain words

A robot must cross a room with some tables in it and wants the shortest way. Pull a string tight between the start and the goal around the tables. The tight string goes straight from table corner to table corner, so the robot only needs to know which corners can see which.

The visibility graph records this. It is a list of all pairs of corners that you can join with a straight line without going through a table. Going along a table side counts as allowed. With this list, the shortest way is a usual shortest route search over a road map, where the roads are the lines of sight and the length of a road is its straight length.

## The abstract type

Notation: the obstacles $P_1, \ldots, P_h$ are [simple polygons](/simple-polygon/) with $n$ vertices in total, given in either orientation. Their boundaries are pairwise disjoint, so the obstacles are disjoint closed sets. The free space $F$ is the plane minus the union of the open interiors. A path is feasible when it lies in $F$; it may run along an obstacle edge or pass through a vertex. Points $p$ and $q$ see each other when the closed segment $pq$ lies in $F$. Let $V$ be the set of obstacle vertices together with any extra points in $F$.

**Value.** The graph $G = (V, E)$ with $E = \{pq : p, q \in V, p \ne q, pq \subseteq F\}$ and edge weights $|pq|$. Let $m = |E|$.

**Operations.**

- BUILD(obstacles, extra points): construct $G$.
- VISIBLE$(p, q)$: decide whether $pq \subseteq F$.
- SHORTEST-PATH$(s, t)$: for $s, t \in F$, the length and the vertex list of a shortest feasible path from $s$ to $t$.

General position is not assumed. Three or more vertices may lie on one line, a segment may pass through vertices or run along edges, and a polygon may have vertices with a straight angle. Model: real RAM; the implementation uses integer or rational coordinates, so all predicates are exact, and only the path lengths are floats.

## Representation

An adjacency list: for each node, the list of its visible neighbors with the edge length. The obstacles are kept as vertex lists, so that a query can test the visibility of $s$ and $t$ to all nodes. The edge sides of each obstacle are always edges of $G$, so $m \ge n$, and $m \le n(n-1)/2$ without extra points. Both bounds are reached up to constants: $h$ disjoint triangles in convex position have $\Theta(n^2)$ visible pairs.

## Operations

```pseudo id=main
BUILD(V)
L1  for i ← 1 to |V| do
L2      for j ← i + 1 to |V| do
L3          if VISIBLE(v_i, v_j) then add the edge v_i v_j with length |v_i v_j|

VISIBLE(p, q)
L4  for each obstacle P, with orientation sign σ, do
L5      for each vertex a of P, with predecessor a⁻ and successor b, do
L6          if the edge ab and pq cross at a point interior to both then return false
L7          if a lies on the closed segment pq then mark P as touched
L8              if a ≠ q and the direction q − p points from a into the open interior of P then return false
L9              if a ≠ p and the direction p − q points from a into the open interior of P then return false
L10     if P is not touched and the midpoint of pq lies strictly inside P then return false
L11 return true
```

The interior test of lines L8 and L9 uses the two edges at $a$. With $\sigma = +1$ for a counterclockwise polygon and $-1$ for a clockwise one, a direction $u$ points into the interior at a convex vertex when $\sigma \cdot (a - a^-) \times u > 0$ and $\sigma \cdot (b - a) \times u > 0$; at a reflex vertex one of the two suffices. Line L10 is a [point in polygon](/point-in-polygon/) test that answers false on the boundary. Each of these is an [orientation test](/orientation-test/) or a sum of them.

SHORTEST-PATH$(s, t)$ tests the visibility of $s$ and $t$ to every node, adds the visible pairs as edges, and runs [Dijkstra's algorithm](/dijkstra/) with a binary heap from $s$.

**The rotational sweep.** Lee's faster build finds the neighbors of one vertex $v$ at a time. Sort the other vertices by the angle around $v$, and sweep a ray from $v$ through them. A balanced search tree holds the obstacle edges that the ray crosses, ordered by their distance from $v$ along the ray. A vertex $w$ is visible from $v$ when the segment $vw$ does not leave $v$ into its own obstacle and the nearest edge in the tree is not closer than $w$, with a separate check when the previous vertex lies on the same ray. At $w$, the edges of $w$ on the far side of the ray are inserted and those on the near side are deleted. Each vertex costs $O(n \log n)$, so the build takes $O(n^2 \log n)$ time.

## Example

Take the triangle $(2, 1), (5, 0), (4, 4)$ and the square $(6, 2), (8, 2), (8, 6), (6, 6)$, so $n = 7$. The graph has 12 edges:

| kind | edges |
|---|---|
| sides of the triangle | $(2,1)(5,0)$, $(5,0)(4,4)$, $(4,4)(2,1)$ |
| sides of the square | $(6,2)(8,2)$, $(8,2)(8,6)$, $(8,6)(6,6)$, $(6,6)(6,2)$ |
| between the obstacles | $(4,4)(6,2)$, $(4,4)(6,6)$, $(5,0)(6,2)$, $(5,0)(6,6)$, $(5,0)(8,2)$ |

The segment from $(5, 0)$ to $(6, 6)$ touches the square only at its corner, so it is an edge. The segment from $(4, 4)$ to $(8, 2)$ meets the left side of the square at $(6, 3)$, an interior point of that side, and is not an edge. The diagonals of the square are not edges, and every vertex of the triangle other than $(5, 0)$ is hidden from $(8, 2)$ by the triangle or by the square.

For $s = (0, 0)$ and $t = (10, 4)$, $s$ sees $(2, 1), (5, 0), (4, 4), (6, 6)$ and $t$ sees $(8, 2), (8, 6)$, which gives 18 edges. The segment $st$ crosses both obstacles. Dijkstra's algorithm gives the path $(0, 0), (5, 0), (8, 2), (10, 4)$ of length $5 + \sqrt{13} + \sqrt{8} \approx 11.43398$. The path over the top through $(4, 4), (6, 6), (8, 6)$ has length $\sqrt{32} + \sqrt{8} + 2 + \sqrt{8} \approx 13.31$.

## Correctness

Two facts make the structure work, and [the correctness proof](proofs/correctness/) gives both in full.

**VISIBLE is exact.** Fix an obstacle $P$ and cut the open segment $pq$ at the vertices of $P$ that lie on it. On each open piece $J$, either $J$ misses the boundary of $P$ or $J$ lies on one edge: a boundary point inside $J$ that is not a vertex is either a proper crossing, caught by line L6, or a point of an edge on the line of $pq$, and then that edge covers $J$. So each piece lies wholly inside, wholly outside, or on the boundary of $P$. A piece with a vertex at an end is decided by the direction test at that vertex (lines L8 and L9), and if no vertex lies on $pq$ there is one piece, decided by its midpoint (line L10).

**Shortest paths use only graph edges.** A shortest feasible path exists. At a point of the path where the free space is locally convex, which is every point except the obstacle vertices, a shortcut by a chord shows that the path is straight there. So a shortest path is polygonal, with inner vertices at obstacle vertices, and each of its segments is an edge of $G$. Conversely, every path in $G$ is feasible. So the distance in $G$ equals the shortest feasible length.

## Complexity

| operation | cost | case |
|---|---|---|
| VISIBLE | $O(n)$: each edge is tested once, and each obstacle has at most one point in polygon test | worst case |
| BUILD, direct | $O(n^3)$, with $O(n^2)$ calls of VISIBLE | worst case |
| BUILD, rotational sweep (Lee 1978) | $O(n^2 \log n)$ | worst case |
| BUILD, dual arrangement (Welzl 1985) | $O(n^2)$ | worst case |
| BUILD, output-sensitive (Ghosh and Mount 1991) | $O(n \log n + m)$ | worst case |
| SHORTEST-PATH | $O(n^2)$ for the visibility of $s$ and $t$, and $O(m \log n)$ for Dijkstra | worst case |
| space | $O(n + m)$, which is $O(n^2)$ | worst case |

Since $m$ can be $\Theta(n^2)$, any method that builds the whole graph needs $\Omega(n^2)$ time in the worst case, which Welzl's method matches. The best known shortest path methods do not build the graph: Hershberger and Suri find one in $O(n \log n)$ time, see [Euclidean shortest path](/euclidean-shortest-path/).

## Variants

- **Reduced visibility graph.** Only the edges that are tangent to the obstacles at both ends can lie on a shortest path, because a shortest path cannot turn at a vertex away from its obstacle. For $h$ disjoint convex obstacles there are 4 such bitangents per pair, so the graph has $O(h^2)$ edges besides the sides.
- **Inside a polygon.** For the vertices of one simple polygon and paths inside it, the [visibility graph of a polygon](/visibility-graph-of-polygon/) is the analogue; there the [shortest path in a polygon](/euclidean-shortest-path-in-polygon/) needs only $O(n)$ time.
- **Translating robot.** For a polygonal robot that moves without rotation, grow each obstacle by the [Minkowski sum](/minkowski-sum/) with the reflected robot; in this [configuration space](/configuration-space/) the robot is a point.
- **Visibility from one point.** The neighbors of one node form the vertex set of its [visibility polygon](/visibility-polygon/) restricted to obstacle vertices, which a single rotational sweep computes.
- **Three dimensions.** Shortest paths among polyhedra bend on the interiors of edges, not only at vertices, so no finite graph on the vertices suffices; the problem is NP-hard (Canny and Reif 1987).

## When to use it

Use the visibility graph when many shortest path queries are asked among fixed obstacles, or when the obstacles are few and simple, since the graph is built once and each query is a graph search. For a single query among many vertices, a method that does not build the graph, such as the shortest path map, is faster. For a path inside one simple polygon, use the funnel method instead.

## Pitfalls

- **Edges along obstacle sides.** A segment that runs along an obstacle side, or touches a corner, is feasible. A test that rejects every segment that meets an obstacle boundary misses the sides and the paths that graze a corner, and then the computed path is too long or does not exist.
- **Diagonals of one obstacle.** Two vertices of one obstacle can see each other through the outside, as across the mouth of a pocket of a nonconvex polygon, or can be blocked by its interior, as along a diagonal of a square. A segment-crossing test alone cannot tell these apart; the direction test at the end vertices does.
- **Segments through vertices.** A segment that enters an obstacle exactly at a vertex crosses no edge properly. Without the direction tests of lines L8 and L9, the diagonal of a square through two of its corners is accepted.
- **Floating-point predicates.** Rounded orientation tests decide grazing segments at random. Use exact arithmetic for the predicates and floats only for the lengths.
- **Start or target inside an obstacle.** No feasible path exists; reject the input.

## Implementations

## History

The visibility graph is usually traced to Nilsson's 1969 work on the mobile robot Shakey. Lozano-Pérez and Wesley (1979) made it the standard method for planning paths among polyhedral obstacles, after growing the obstacles by the shape of the robot. Lee (1978) built the graph in $O(n^2 \log n)$ time by an angular sweep around each vertex. Welzl (1985), and independently Asano, Asano, Guibas, Hershberger and Imai, reached $O(n^2)$ time with the arrangement of the dual lines, and Ghosh and Mount (1991) gave the output-sensitive bound $O(n \log n + m)$.

## References
