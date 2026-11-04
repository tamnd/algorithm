---
tag: ZTDMY9
kind: technique
slug: rotational-sweep
name: Rotational sweep
aliases:
- angular sweep
- rotating sweep
area: techniques/sweep-line
level: advanced
summary: Sweep by a rotating line around a point, processing events in angular order.
prereqs: [sweep-line-technique, orientation-test, balanced-binary-search-tree]
see_also: [visibility-graph, visibility-polygon, angular-sort, graham-scan, euclidean-shortest-path, sweep-status-structure, degeneracy-in-sweeps, cross-product]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 15, Visibility Graphs (the algorithms VISIBILITYGRAPH, VISIBLEVERTICES and VISIBLE, O(n² log n) time)
  - paper: "D. T. Lee, Proximity and reachability in the plane, PhD thesis, University of Illinois at Urbana-Champaign, 1978"
    locator: the O(n² log n) visibility graph algorithm by rotational sweep
  - paper: "E. Welzl, Constructing the visibility graph for n-line segments in O(n²) time, Information Processing Letters 20(4) (1985), doi:10.1016/0020-0190(85)90044-4"
    locator: pages 167 to 171
  - paper: "T. Asano, T. Asano, L. Guibas, J. Hershberger and H. Imai, Visibility of disjoint polygons, Algorithmica 1 (1986), doi:10.1007/BF01840436"
    locator: pages 49 to 63
  - paper: "S. K. Ghosh and D. M. Mount, An output-sensitive algorithm for computing visibility graphs, SIAM Journal on Computing 20(5) (1991), doi:10.1137/0220055"
    locator: pages 888 to 910
  - paper: "B. M. Chazelle and D. T. Lee, On a circle placement problem, Computing 36 (1986), doi:10.1007/BF02238188"
    locator: pages 1 to 16
---

A rotational sweep is a [sweep line](/sweep-line-technique/) that turns around a fixed point $p$ instead of moving across the plane: a ray from $p$ rotates through a full turn, the events are the angular positions of the vertices, and the status is the set of segments that the ray crosses, ordered by their distance from $p$. Between two events the order of the segments along the ray does not change, so a [balanced binary search tree](/balanced-binary-search-tree/) can hold it, with $O(\log n)$ work per event. The main use is to find the vertices visible from $p$ among polygonal obstacles in $O(n \log n)$ time, and from that the [visibility graph](/visibility-graph/) in $O(n^2 \log n)$ time. The same angular order, without a status tree, drives [Graham's scan](/graham-scan/) and the classic angular sweep for the largest number of points that a circle of fixed radius can cover.

## In plain words

Stand at one spot in a dark room full of furniture and hold a torch. Turn slowly on the spot, one full turn. At each moment the beam hits a list of furniture edges, near to far. Only the nearest one can be lit; the others are behind it.

The list changes only when the beam passes a corner of some piece. At a corner, an edge can start (the beam starts to hit it) or end (the beam no longer hits it). Between two corners the list keeps its order, because two edges of the furniture never cross. So you sort the corners by direction once, and at each corner you update the list and ask one question: is this corner nearer than the nearest edge in the beam? If it is, you can see it.

## When it applies

- The question is about one centre point and about directions from it: what can $p$ see, which objects does a ray from $p$ hit first, how do objects look in polar coordinates around $p$.
- The objects are segments or polygons whose interiors do not cross, so their order along a ray from $p$ changes only at their endpoints.
- A problem over all pairs, such as the visibility graph or the best circle through a point, runs one rotational sweep from each point, which gives a quadratic times logarithmic algorithm.
- Each object, seen from $p$, covers an interval of angles. Problems about intervals on a circle (the deepest point, a cover of the circle) become a sweep over the circle of directions.

## The template

The ray $\rho(\theta)$ starts at $p$ and has the direction of angle $\theta$ from the positive $x$-axis. It rotates counterclockwise from $\theta = 0$ to $2\pi$. For de Berg et al., who sweep a horizontal line downwards in their other chapters, this is the same method with an angle in place of a coordinate.

```pseudo id=main
ROTATIONAL-SWEEP(p, S)                     ▷ S: segments with disjoint interiors
L1  E ← the endpoints of S, other than p                          ▷ hole: EVENTS
L2  sort E by the angle around p, ties by the distance from p     ▷ exact comparisons
L3  T ← an empty balanced search tree, ordered by distance along the ray
L4  for each segment s that crosses the ray ρ(0) do INSERT(T, s)    ▷ hole: INITIAL-STATUS
L5  for each event w in E, in sorted order do
L6      ANSWER(w, T)                       ▷ hole: the query at w, for example "is w visible?"
L7      for each segment s with endpoint w on the clockwise side of ρ through w do DELETE(T, s)
L8      for each segment s with endpoint w on the counterclockwise side do INSERT(T, s)
L9  return the answers
```

The holes and the parts that change are:

- **EVENTS.** The angles where the status changes: the vertices of obstacles, or the endpoints of angular intervals.
- **COMPARE on the ray.** Two segments in $T$ are compared by the distance from $p$ to the points where the current ray crosses them. The tree only needs this comparison at the current angle, and the order stays valid until the next event, since the segments do not cross.
- **INITIAL-STATUS.** The segments that the starting ray $\rho(0)$ crosses must be in $T$ before the first event. A segment that crosses $\rho(0)$ has its "start" event late in the turn, near $2\pi$, and its "end" event early; without line L4 it would be missing from $T$ for the first part of the sweep.
- **ANSWER.** For visibility: $w$ is visible when the segment $pw$ does not cross the nearest segment in $T$, and does not enter the interior of the obstacle that $w$ belongs to. A rotational sweep over angular intervals answers with a counter instead of a tree.

Lines L7 and L8 use the [orientation test](/orientation-test/): for the other endpoint $u$ of a segment $wu$, the sign of $\mathrm{orient}(p, w, u)$ tells whether $u$ lies counterclockwise (positive, the segment starts) or clockwise (negative, it ends). A segment with $u$ on the ray (sign 0) lies along the ray; it is not inserted, but ANSWER must take it into account for the next vertex on the same ray.

**Cost.** For $n$ segments there are at most $2n$ events. The sort takes $O(n \log n)$ time, line L4 takes $O(n \log n)$, and each event does $O(1)$ tree operations of $O(\log n)$ each. In total $O(n \log n)$ time and $O(n)$ space for one centre.

### Exact angular comparisons

Sorting by `atan2` works, but two points at nearly the same angle can get equal or swapped keys after rounding. With integer or rational coordinates, compare exactly. For $a$ and $b$ relative to $p$, let $h(a) = 0$ when $a$ is in the upper half-plane $\{y > 0\} \cup \{y = 0, x > 0\}$ and $h(a) = 1$ otherwise. Then $a$ comes before $b$ when $h(a) < h(b)$, or $h(a) = h(b)$ and the [cross product](/cross-product/) $a \times b > 0$. When $h(a) = h(b)$ and $a \times b = 0$ the two points lie on the same ray, and the nearer one comes first, as line L2 requires. This is the order of an [angular sort](/angular-sort/).

## Classic examples

### Visible vertices and the visibility graph (de Berg et al., Chapter 15)

Let $S$ be a set of disjoint polygonal obstacles with $n$ edges in total. A vertex $w$ is *visible* from $p$ when the open segment $pw$ does not meet the interior of any obstacle; it may touch a boundary. The procedure VISIBLEVERTICES of de Berg et al. is the template above with ANSWER = the test VISIBLE, and it runs in $O(n \log n)$ time. VISIBLE treats the case where the previous vertex in the order lies on the segment $pw$: then $w$ is visible only when that vertex is visible and no edge in $T$ crosses the segment between the two.

**Example.** Let $p = (0, 0)$, and let the obstacles be the quadrilateral $A = (2, -1), (3, -0.5), (3, 1), (2, 1.5)$ and the triangles $B = (5, -2), (7, 1), (5, 2)$, $C = (-1, 2), (1, 3), (-2, 4)$ and $D = (-3, -2), (-1, -3), (-2, -1)$. The ray $\rho(0)$ is the positive $x$-axis. It crosses, near to far, the edge of $A$ at $x = 2$ (distance 2), the edge of $A$ at $x = 3$ (distance 3), the edge of $B$ at $x = 5$ (distance 5), and the edge $(5, -2)(7, 1)$ (distance $19/3 \approx 6.33$). These four edges are the initial status.

| angle | vertex | distance | nearest edge in $T$ before the update | visible | update of $T$ |
|---|---|---|---|---|---|
| 8.13° | $(7, 1)$ | 7.07 | $A$, $x = 2$, at 2.02 | no | delete $(7,1)(5,-2)$, insert $(7,1)(5,2)$ |
| 18.43° | $(3, 1)$ | 3.16 | $A$, $x = 2$, at 2.11 | no | delete $(3,1)(3,-0.5)$, insert $(3,1)(2,1.5)$ |
| 21.80° | $(5, 2)$ | 5.39 | $A$, $x = 2$, at 2.15 | no | delete both edges of $B$ at $(5,2)$ |
| 36.87° | $(2, 1.5)$ | 2.5 | its own edges | yes | delete both edges at $(2, 1.5)$; $T$ is empty |
| 71.57° | $(1, 3)$ | 3.16 | none | yes | insert both edges of $C$ at $(1, 3)$ |
| 116.57° | $(-1, 2)$ | 2.24 | its own edge | yes | delete $(-1,2)(1,3)$; the edge $(-1,2)(-2,4)$ lies on the ray |
| 116.57° | $(-2, 4)$ | 4.47 | its own edge | yes | delete $(-2,4)(1,3)$; $T$ is empty |
| 206.57° | $(-2, -1)$ | 2.24 | none | yes | insert both edges of $D$ at $(-2,-1)$ |
| 213.69° | $(-3, -2)$ | 3.61 | $(-2,-1)(-1,-3)$ at 2.25 | no | delete $(-3,-2)(-2,-1)$, insert $(-3,-2)(-1,-3)$ |
| 251.57° | $(-1, -3)$ | 3.16 | its own edges | yes | delete both edges at $(-1,-3)$; $T$ is empty |
| 333.43° | $(2, -1)$ | 2.24 | none | yes | insert both edges of $A$ at $(2, -1)$ |
| 338.20° | $(5, -2)$ | 5.39 | $A$, $x = 2$, at 2.15 | no | insert both edges of $B$ at $(5, -2)$ |
| 350.54° | $(3, -0.5)$ | 3.04 | $A$, $x = 2$, at 2.03 | no | delete $(3,-0.5)(2,-1)$, insert $(3,-0.5)(3,1)$ |

Seven of the fourteen vertices are visible: $(2, 1.5)$, $(1, 3)$, $(-1, 2)$, $(-2, 4)$, $(-2, -1)$, $(-1, -3)$ and $(2, -1)$. At the end of the turn, $T$ holds the same four edges as at the start. The two vertices of $C$ at 116.57° lie on one ray: the nearer one, $(-1, 2)$, is processed first, and $(-2, 4)$ is visible because the segment from $p$ runs along the edge $(-1, 2)(-2, 4)$ of $C$ and touches only its boundary.

**The visibility graph.** Run the sweep from each of the $n$ vertices and join each vertex to the vertices it sees. This gives the [visibility graph](/visibility-graph/) in $O(n^2 \log n)$ time; de Berg et al. present this algorithm, and Lee gave it in his thesis of 1978. With the start and the goal added as vertices, a shortest path in this graph is a [Euclidean shortest path](/euclidean-shortest-path/) among the obstacles. The graph can have $\Theta(n^2)$ edges, so $\Omega(n^2)$ is a lower bound for any algorithm that lists them. Welzl (1985) and Asano, Asano, Guibas, Hershberger and Imai (1986) gave $O(n^2)$ algorithms, and Ghosh and Mount (1991) an output-sensitive algorithm in $O(n \log n + k)$ time for a graph with $k$ edges.

### The visibility polygon

The [visibility polygon](/visibility-polygon/) of $p$ is the region that $p$ sees. The same sweep builds it: between two events the nearest segment in $T$ is the boundary of the region, and at each event where the nearest segment changes, the boundary jumps along the ray from the old nearest segment to the new one. This is $O(n \log n)$ for $n$ segments in total.

### Angular sorting in Graham's scan

[Graham's scan](/graham-scan/) sorts the points by angle around the lowest point and then walks through them in that order with a stack. The sort is lines L1 and L2 of the template, with the exact comparison above. There is no tree: the stack plays the part of the status. [Jarvis's march](/jarvis-march/) is a rotation of another kind, with the centre moving to each new hull vertex.

### The most points in a circle of fixed radius

Given $n$ points and a radius $r$, place a circle of radius $r$ to contain as many points as possible. Some optimal circle has a point $c$ of the set on its boundary (move any optimal circle until it touches one, without losing a point). Fix $c$. The centres of the circles of radius $r$ through $c$ lie on the circle of radius $r$ around $c$, at angle $\varphi$. A point $q$ with $|cq| = d \le 2r$ is inside the circle for exactly the angles $\varphi \in [\theta_q - \alpha_q, \theta_q + \alpha_q]$, where $\theta_q$ is the direction of $q$ from $c$ and $\alpha_q = \arccos(d/2r)$. Sweep $\varphi$ through these $2(n-1)$ interval ends, add 1 at an entry and subtract 1 at an exit, and keep the maximum. With a counter as the status, each centre costs $O(n \log n)$, and all centres $O(n^2 \log n)$. Chazelle and Lee gave an $O(n^2)$ algorithm in 1986.

*Example.* Points $(0, 0), (1, 0), (2, 0), (1, 1), (3, 3), (0.5, 1.6)$ and $r = 1$. Around $c = (1, 0)$ the intervals are $[-60°, 60°]$ for $(2, 0)$, $[30°, 150°]$ for $(1, 1)$, $[74.30°, 140.41°]$ for $(0.5, 1.6)$, and $[120°, 240°]$ for $(0, 0)$; the point $(3, 3)$ is too far. At $\varphi = 120°$ the intervals of $(1, 1)$, $(0.5, 1.6)$ and $(0, 0)$ overlap, so the circle with centre $(1, 0) + (\cos 120°, \sin 120°) \approx (0.5, 0.866)$ contains 4 points, $c$ included. No circle of radius 1 contains 5 of these points. In this example no entry and exit share an angle. In general, entries must come before exits at equal angles, because the intervals are closed.

## Variations

- **A rotating line instead of a ray.** A full line through $p$ sweeps both directions at once and needs only a half turn. It serves, for example, to count the points on each side of every line through $p$ and another point of the set.
- **Visibility inside a simple polygon.** For a single simple polygon and $p$ inside it, the visibility polygon takes $O(n)$ time by a walk along the boundary, without the sort.
- **Sweeps of the circle of directions.** When each object gives an arc of directions, the sweep needs only the arc ends and a counter. This covers the point of greatest depth of arcs on a circle and the test of whether arcs cover the circle.
- **All centres at once.** The $n$ separate angular sorts of the visibility graph can be replaced by one structure for all centres: the $O(n^2)$ algorithms of Welzl and of Asano et al. work with the arrangement of lines in the dual plane, which gives all the angular orders together.

## Pitfalls

- **atan2 and rounding.** Two vertices whose directions differ by less than the rounding error get the same key or the wrong order, and a segment is then inserted after the vertex that it should block. Use the half-plane test and the cross product of the section on exact comparisons.
- **Collinear vertices.** Several vertices can lie on one ray from $p$. Sort them by distance, nearer first, and let the test of the farther one use the result of the nearer one: if the nearer vertex is not visible, no vertex behind it on the same ray is visible. If it is visible, the farther vertex still needs a test of the part between the two, which can run along an obstacle edge as in the example.
- **The initial status.** The segments that cross the starting ray must be in $T$ before the first event (line L4). If they are left out, every vertex before their "end" event is tested against an incomplete status and can be reported visible by mistake. Find them with one pass over the segments, by an intersection test with the ray.
- **A vertex on the starting ray.** A vertex at angle 0 is both the first and the last event. Treat angle 0 as the start of the turn, and decide whether a segment with an endpoint on $\rho(0)$ is in the initial status by the side of its other endpoint, as in lines L7 and L8.
- **Angles that wrap around.** An interval of angles can pass through $2\pi$, as $[300°, 30°]$. In the circle sweep, split it into $[300°, 360°)$ and $[0°, 30°]$, or count it as active at the start and process its end before its start. Comparing raw angles in $(-\pi, \pi]$ treats it as empty.
- **Comparing segments at the wrong angle.** The order of $T$ is the order along the current ray. A comparison function that uses a fixed angle, or the distance of the nearer endpoint, gives a wrong order: a short segment close to $p$ can lie behind a long segment at the current angle.
- **Segments through $p$.** A segment that contains $p$ has no well-defined order along the ray. Visibility from a vertex of an obstacle must skip the edges incident to that vertex, and use the interior test of the obstacle instead.

## Exercises

1. Run the sweep of the example from $p = (4, 0)$, between $A$ and $B$, and list the visible vertices.
2. Show that the order of the segments along the ray cannot change between two consecutive events, when the segments have disjoint interiors.
3. Write the angular comparison of two points around $p$ using only integer arithmetic, and prove that it is a total preorder whose ties are exactly the points on the same ray.
4. Modify the sweep to output the visibility polygon of $p$, and give its cost.
5. Prove that some optimal circle of radius $r$ has a point of the set on its boundary, and that, if the optimum contains at least two points, some optimal circle has two points of the set on its boundary.
6. Give a set of disjoint segments whose visibility graph has $\Theta(n^2)$ edges.

## References
