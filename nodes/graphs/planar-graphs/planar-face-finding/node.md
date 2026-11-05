---
tag: X3Q68V
kind: algorithm
slug: planar-face-finding
name: Finding faces of a planar graph
aliases:
- face tracing
- face traversal
area: graphs/planar-graphs
level: core
summary: Algorithm that finds all faces of a planar graph embedded in the plane by sorting edges by angle and walking around each face.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [rotation-system, planar-face]
see_also: [planar-dual-graph, euler-formula, doubly-connected-edge-list, planar-embedding, lipton-tarjan-separator, maximal-planar-graph, graph-genus, planar-subdivision]
sources:
  - book: isbn:9780486417417
    title: Jonathan L. Gross and Thomas W. Tucker, Topological Graph Theory, Dover edition, 2001
    locator: Chapter 3, Surfaces and graph imbeddings (the face tracing algorithm for a rotation system)
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapters 3 and 4 (the facial walks of an embedding given by a rotation system)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Line segment intersection (Section 2.2 on the doubly connected edge list, and Section 2.3 on computing the overlay, where the boundary cycles are found by following next pointers)
---

Face finding lists the [faces](/planar-face/) of an embedded [planar graph](/planar-graph/). The embedding is given as a [rotation system](/rotation-system/), the counterclockwise order of the neighbours around each vertex; if it is given by coordinates, the algorithm first sorts the edges at each vertex by angle. Then it walks around each face: from a half-edge $(u, v)$ it turns to the neighbour of $v$ that comes just before $u$ in the order at $v$. Each half-edge is walked once, so the time is $\Theta(n + m)$ after the sort.

## In plain words

Think of each edge as a two-lane road, one lane in each direction. Drive along a lane. When you reach a crossing, take the sharpest right turn that leaves the crossing, which is the road just clockwise from the one you came on. If you keep doing this, you go around one region of the map, with the region always on your left, and you come back to the lane where you started.

Mark every lane you drive on. Start a new drive from each lane that is not yet marked. Each drive gives one region, and when no lane is left, you have every region. An edge that sticks into a region, with nothing at its end, is driven twice, once in each lane.

## The problem

**Input.** A simple undirected graph $G = (V, E)$ and a rotation system $\rho$: for each vertex $v$, the list $\rho_v$ of its neighbours in counterclockwise order around $v$, read cyclically. If the input is a straight-line drawing with a point $p_v \in \mathbb{Z}^2$ for each vertex, $\rho_v$ is the order of the neighbours $w$ by the angle of $p_w - p_v$.

**Output.** The cycles of the face permutation on the set $D$ of $2m$ darts,

$$\varphi(u, v) = (v, w), \qquad w = \text{the neighbour just before } u \text{ in } \rho_v,$$

each written as the closed walk $u_0, u_1, \ldots, u_{k-1}$ of the tails of its darts. When $\rho$ comes from a planar drawing, these walks are the boundaries of the faces, each with its face on the left, and the number of walks $f$ satisfies $n - m + f = 2c$ for $c$ components, counting an isolated vertex as one face of length 0. When $\rho$ is not planar, the walks are the faces of the embedding in a surface of higher genus that $\rho$ describes, and $n - m + f < 2c$.

## The algorithm

```pseudo id=main
FACES(ρ)                                   ▷ ρ_v: neighbours of v, counterclockwise
L1  for each v and each index i: pos[(v, ρ_v[i])] ← i
L2  visited ← ∅, F ← empty list
L3  for each dart (u, v), u in vertex order, v in the order ρ_u
L4      if (u, v) ∈ visited then continue
L5      W ← empty walk, d ← (u, v)
L6      while d ∉ visited
L7          visited ← visited ∪ {d}, append the tail of d to W
L8          (a, b) ← d, i ← pos[(b, a)]         ▷ where a sits in ρ_b
L9          d ← (b, ρ_b[(i − 1) mod deg b])      ▷ the neighbour just before a
L10     append W to F
L11 return F
```

Line L1 stores, for each dart $(v, w)$, the index of $w$ in $\rho_v$, so that line L8 finds in $O(1)$ time where the walk entered $b$. Line L9 is the face rule: it leaves $b$ along the edge just clockwise of the edge it came in on. An isolated vertex has no dart; the implementation reports it as a face of length 0, so that Euler's formula counts it.

**From coordinates.** Sort each $\rho_v$ by angle. To avoid rounding, compare two directions $a, b$ exactly: first by half-plane ($a_y > 0$, or $a_y = 0$ and $a_x > 0$, is the upper half), then by the sign of the cross product $a_x b_y - a_y b_x$. Integer coordinates then give an exact order.

## Example

The drawing has the square $0 = (0, 0)$, $1 = (4, 0)$, $2 = (4, 4)$, $3 = (0, 4)$, the diagonal $02$, a roof vertex $4 = (2, 6)$ joined to 2 and 3, and a pendant vertex $5 = (3, 1)$ joined to 1, inside the triangle $0, 1, 2$. So $n = 6$ and $m = 8$. Sorting by angle gives

$$\rho_0 = (1, 2, 3), \; \rho_1 = (2, 5, 0), \; \rho_2 = (4, 3, 0, 1), \; \rho_3 = (2, 4, 0), \; \rho_4 = (3, 2), \; \rho_5 = (1).$$

The first walk starts at the dart $(0, 1)$:

| step | dart $d$ | $\rho_b$ | index of $a$ in $\rho_b$ | next dart |
|---|---|---|---|---|
| 1 | $(0, 1)$ | $\rho_1 = (2, 5, 0)$ | 2 | $(1, 5)$ |
| 2 | $(1, 5)$ | $\rho_5 = (1)$ | 0 | $(5, 1)$ |
| 3 | $(5, 1)$ | $\rho_1 = (2, 5, 0)$ | 1 | $(1, 2)$ |
| 4 | $(1, 2)$ | $\rho_2 = (4, 3, 0, 1)$ | 3 | $(2, 0)$ |
| 5 | $(2, 0)$ | $\rho_0 = (1, 2, 3)$ | 1 | $(0, 1)$, visited |

So the first face is $0, 1, 5, 1, 2$: the triangle $0, 1, 2$ with the pendant edge $15$ walked in both directions, length 5. The darts $(0, 2)$ and $(0, 3)$ then start the walks $0, 2, 3$ and $0, 3, 4, 2, 1$, and the dart $(2, 4)$ starts $2, 4, 3$. The result is

| face | walk | length |
|---|---|---|
| inner, with the pendant edge | $0, 1, 5, 1, 2$ | 5 |
| inner triangle | $0, 2, 3$ | 3 |
| outer face | $0, 3, 4, 2, 1$ | 5 |
| roof triangle | $2, 4, 3$ | 3 |

The lengths sum to $16 = 2m$, and $6 - 8 + 4 = 2$. The outer walk $0, 3, 4, 2, 1$ goes clockwise around the drawing, so the outer face is also on its left.

## Correctness

$\varphi$ is a permutation of the darts: its inverse is $(v, w) \mapsto (u, v)$ with $u$ the neighbour just after $w$ in $\rho_v$. So the darts split into disjoint cycles of $\varphi$. The loop of lines L6 to L9 follows $\varphi$ from a dart that is not yet visited and stops at the first visited dart; because the cycle of the start dart has no visited dart before the start is reached again, the walk is exactly one whole cycle. The loop of line L3 starts a walk from each dart not yet covered, so every cycle is output once. For a planar drawing, the cycles of $\varphi$ are the face boundaries by the rotation principle. The full proof is in the correctness proof below.

## Complexity

- **Line L1** visits each dart once: $\Theta(n + m)$ with a hash map, or with arrays when the adjacency lists store, for each entry, the index of its twin.
- **Lines L3 to L10** visit each dart once at line L3 and once at line L7, with $O(1)$ work each time. So they take $\Theta(n + m)$ time.
- **From coordinates**, sorting the neighbours of $v$ costs $O(\deg v \log \deg v)$, which is $O(m \log n)$ in total and $O(n \log n)$ for a simple planar graph. This sort is needed in the [algebraic decision tree](/algebraic-decision-tree/) model, since sorting $n - 1$ points by angle around a center is as hard as sorting.
- **Space.** $\Theta(n + m)$ for pos, the visited marks and the output.

## Properties

- **One pass, no recursion.** The algorithm is a pair of nested loops, and uses no stack.
- **It works on any surface.** The same code traces the faces of a rotation system of any genus. With the count $f$, the genus is $g = (2c - n + m - f)/2$, which gives a planarity check for a candidate embedding.
- **The order of output is fixed** by the vertex order and by $\rho$, so the output is deterministic.
- **Face to the left.** With counterclockwise rotations and the predecessor rule, each face is on the left of its walk: bounded faces are walked counterclockwise and the outer face clockwise. Using the successor in line L9 walks every face in the other direction.

## Variants and improvements

- **Half-edge pointers.** In a [doubly connected edge list](/doubly-connected-edge-list/), each half-edge already stores its twin and its next half-edge around its face, so line L9 is one pointer read and pos is not needed. Face finding then sets the face field of each half-edge.
- **The dual at the same time.** Give each walk a number, and record for each edge the numbers of the faces of its two darts. This builds the [planar dual](/planar-dual-graph/) in the same $\Theta(n + m)$ time.
- **Multigraphs.** With parallel edges, store darts by edge identifier, not by the pair of ends, and let $\rho_v$ order darts. The algorithm does not change.
- **Outer face detection.** For a straight-line drawing of a connected graph, the outer face is the one walk whose signed area is at most zero; all other walks have positive area.

## When to use it

Use it whenever an algorithm needs the faces of an embedded graph: to triangulate faces, to build the dual, to run the [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm, to insert edges in [planarization](/planarization-heuristic/), or to check that an embedding returned by a [planarity test](/planarity-testing/) is planar. For a graph that is only known as an adjacency list, compute an embedding first with a [planar embedding](/planar-embedding/) algorithm; the faces are not defined without one.

## Pitfalls

- **Turning the wrong way at one vertex.** The rule at line L9 must be the predecessor at every step. Mixing the predecessor and the successor (for example, a clockwise $\rho$ at some vertices) produces walks that are not faces, and the count $f$ is wrong.
- **Looking up $(a, b)$ instead of $(b, a)$.** Line L8 needs the index of $a$ in $\rho_b$, the position of the incoming edge at the head. Using pos$[(a, b)]$, the position at the tail, gives a different permutation.
- **Angles in floating point.** Sorting by atan2 can put two nearly equal directions in the wrong order and break planarity. Compare with integer cross products, as described above.
- **Isolated vertices and the empty graph.** A vertex with no edges has no dart, so a dart-only implementation counts no face for it and Euler's formula seems to fail. Count it as a face of length 0, or treat it apart.
- **Several components.** The walks of one component do not show in which face of another component it lies. Do not expect $n - m + f = 2$ for a disconnected graph; the right count is $n - m + f = 2c$ for the walks, and $1 + c$ for the faces of the drawing.

## Implementations

## History

Tracing the faces of a rotation system goes back to Heffter's work on maps in 1891 and to Edmonds' 1960 note, which showed that every rotation system of a connected graph defines an embedding in an orientable surface. Gross and Tucker present it as the face tracing algorithm. In computational geometry the same walk follows the next pointers of a doubly connected edge list, as in de Berg, Cheong, van Kreveld and Overmars.

## References
