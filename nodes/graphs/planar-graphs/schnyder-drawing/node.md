---
tag: EKZ3MZ
kind: algorithm
slug: schnyder-drawing
name: Schnyder drawing algorithm
aliases:
- Schnyder's drawing
area: graphs/planar-graphs
level: advanced
summary: Straight-line grid drawing of a planar graph on an (n-2) by (n-2) grid using Schnyder woods.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [schnyder-woods, maximal-planar-graph, rotation-system, planar-face-finding]
see_also: [planar-straight-line-drawing, de-fraysseix-pach-pollack, canonical-ordering, tutte-spring-theorem, graph-drawing, biconnected-components, planar-embedding, depth-first-search]
sources:
  - paper: "Walter Schnyder, Embedding planar graphs on the grid, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1990), 138 to 148"
    locator: the barycentric representation by region counts, the (n-2) by (n-2) grid drawing and its linear running time
  - paper: doi:10.1007/BF00353652
    title: Walter Schnyder, Planar graphs and poset dimension, Order 5(4), 323 to 343 (1989)
    locator: the definition of the three trees (realizers), the paths and regions of a vertex, and the lemma that a path of one colour cannot leave a region of a vertex
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the canonical ordering of a plane triangulation and the lemma that a vertex without a chord can always be removed
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the chapter on straight-line drawings of planar graphs (canonical orderings, Schnyder realizers and grid drawings)
---

Schnyder's drawing algorithm draws a [planar graph](/planar-graph/) with $n \ge 3$ vertices without crossings, with straight edges and all vertices at integer points of an $(n - 2) \times (n - 2)$ grid. It first adds edges until the graph is a [maximal planar graph](/maximal-planar-graph/), then splits the inner edges of this triangulation into three trees, a [Schnyder wood](/schnyder-woods/). Each inner vertex gets three coordinates by counting the vertices in the three regions that its three tree paths cut out of the outer triangle. The embedding is given as a [rotation system](/rotation-system/), and the whole run takes $\Theta(n)$ time.

## In plain words

Fill every region of the network with extra lines until every region is a triangle. Pin the three corners of the outside triangle. Then let every other node point at each corner along a path that always goes one step closer to that corner, in a way that the three paths from a node never meet again.

These three paths split the big triangle into three slices around the node. Count the nodes in each slice and use these counts, corrected a little, as the node's coordinates. A node further from a corner sees a bigger slice opposite that corner. The counts change in a way that keeps every edge apart from every other edge, so the straight-line drawing has no crossings.

## The problem

Input: a planar rotation system $\rho$ of a simple graph $G$ with $n \ge 3$ vertices: $\rho(v)$ lists the neighbours of $v$ in counterclockwise order, and the faces traced from $\rho$ satisfy [Euler's formula](/euler-formula/). Optionally, a face $(a_1, a_2, a_3)$ of the triangulation to be the outer face, listed counterclockwise.

Output: a point $x(v) \in \{0, \ldots, n - 2\}^2$ for each vertex, such that the straight segments between adjacent vertices form a planar drawing: distinct vertices go to distinct points, no vertex lies on an edge it does not belong to, and two edges meet only at a common end. The drawing realizes $\rho$: around each vertex, its neighbours appear in the order $\rho(v)$.

For $n \le 2$ there is nothing to do: the points $(0, 0)$ and $(1, 0)$ suffice.

## The algorithm

A *Schnyder wood* of a plane triangulation with outer face $a_1 a_2 a_3$ colours and orients each inner edge with one of the colours 1, 2, 3, so that each inner vertex $v$ has exactly one outgoing edge of each colour, and counterclockwise around $v$ come: the outgoing edge of colour 1, the incoming edges of colour 3, the outgoing edge of colour 2, the incoming edges of colour 1, the outgoing edge of colour 3, the incoming edges of colour 2. All inner edges at $a_i$ are incoming of colour $i$. The edges of colour $i$ form a tree $T_i$ on the inner vertices and $a_i$, rooted at $a_i$; $P_i(v)$ is the path from $v$ to $a_i$ in $T_i$. The paths $P_{i+1}(v)$ and $P_{i-1}(v)$ (indices mod 3) and the edge $a_{i+1} a_{i-1}$ bound a region $R_i(v)$. Write $|X|$ for the number of vertices in $X$.

```pseudo id=main
SCHNYDER-DRAWING(G, ρ)                      ▷ ρ: a planar rotation system, n ≥ 3
L1  if G is not a triangulation then add edges: join the components,
        remove cut vertices, then cut off triangles from the faces
L2  choose an outer face a_1, a_2, a_3, counterclockwise
L3  path ← a_1, a_3, a_2; repeat n − 2 times: remove a vertex z ∉ {a_1, a_2}
        of the path with no chord, and put its lower neighbours on the path
L4      with p, q the path neighbours of z and m_1, …, m_k the vertices below z:
        p_1(z) ← p, p_2(z) ← q, p_3(m_j) ← z
L5  D_i(v) ← the number of vertices in the subtree of v in T_i, for i = 1, 2, 3
L6  |P_j(v)| and Σ_j^i(v) ← Σ (D_i(w) − 1) over the inner w on P_j(v), top down in T_j
L7  for every inner v and i = 1, 2, 3:
        |R_i(v)| ← |P_(i+1)(v)| + |P_(i−1)(v)| − 1 + Σ_i^(i+1)(v) + Σ_i^(i−1)(v) − (D_i(v) − 1)
        x_i(v) ← |R_i(v)| − |P_(i−1)(v)|
L8  x(a_1) ← (n − 2, 1, 0), x(a_2) ← (0, n − 2, 1), x(a_3) ← (1, 0, n − 2)
L9  return (x_1(v), x_2(v)) for every vertex v
```

**Line L1, triangulation.** Join the components by one edge each, at any corners. Then, for each vertex $v$ and each two neighbours $a, b$ consecutive in $\rho(v)$ whose edges $va$ and $vb$ lie in different [biconnected components](/biconnected-components/), add the edge $ab$ in the corner of $v$ between them; $a \ne b$, and $a, b$ are not adjacent, since a common edge would put $va$ and $vb$ on a cycle. A union-find structure over the component labels merges them as edges are added. Now every face is a cycle $v_0, v_1, \ldots, v_{k-1}$. While $k > 3$, add $v_0 v_2$ inside the face if it is not an edge yet, and otherwise $v_1 v_3$; both cannot be edges, since they would cross outside the face. Every new edge goes into the rotation next to the corner of the face it splits, so the original edges keep their cyclic order.

**Line L3, the canonical ordering.** The path runs from $a_1$ to $a_2$ along the boundary of the part not yet removed. A *chord* is an edge between two path vertices that are not consecutive on the path. Removing $z$ uncovers its neighbours below the path; they are read from $\rho(z)$, counterclockwise from $p$ to $q$. Each vertex keeps the number of chords at it; a stack holds the path vertices whose count is 0. Read backwards, the removal order is the canonical ordering of de Fraysseix, Pach and Pollack, the same order that drives the [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) drawing.

**Lines L5 to L7, counting regions in linear time.** The vertices strictly inside $R_i(v)$ hang in $T_i$ from the inner vertices of its boundary paths $P_{i+1}(v)$ and $P_{i-1}(v)$, one subtree each, so $|R_i(v)|$ is the size of the boundary plus a sum of subtree sizes along two tree paths. Prefix sums from the root of $T_j$ down give each path sum in $O(1)$ per vertex.

## Example

Take the octahedron with outer face $0, 1, 2$ (counterclockwise) and inner vertices $3, 4, 5$, where the opposite pairs, which are not adjacent, are $0$ and $5$, $1$ and $3$, $2$ and $4$. Counterclockwise rotations: $\rho(3) = (0, 4, 5, 2)$, $\rho(4) = (0, 1, 5, 3)$, $\rho(5) = (4, 1, 2, 3)$, $\rho(2) = (0, 3, 5, 1)$. It is already a triangulation, so L1 does nothing; $n = 6$.

| step | removed $z$ | $p$ | $q$ | below $z$ | path afterwards | why $z$ |
|---|---|---|---|---|---|---|
| 1 | 2 | 0 | 1 | 3, 5 | 0, 3, 5, 1 | the first step removes $a_3$ |
| 2 | 5 | 3 | 1 | 4 | 0, 3, 4, 1 | 3 and 5 have no chord; the stack gives 5 |
| 3 | 3 | 0 | 4 | none | 0, 4, 1 | 4 has the chord $4\text{-}0$; 3 has none |
| 4 | 4 | 0 | 1 | none | 0, 1 | the chord $0\text{-}4$ is now on the path |

So the canonical ordering is $0, 1, 4, 3, 5, 2$. Line L4 gives the three trees: $T_1$ has the edges $3 \to 0$, $4 \to 0$, $5 \to 3$; $T_2$ has $3 \to 4$, $4 \to 1$, $5 \to 1$; $T_3$ has $3 \to 2$, $5 \to 2$, $4 \to 5$.

| $v$ | $P_1(v)$ | $P_2(v)$ | $P_3(v)$ | $\lvert R_1 \rvert, \lvert R_2 \rvert, \lvert R_3 \rvert$ | $x(v)$ |
|---|---|---|---|---|---|
| 3 | 3, 0 | 3, 4, 1 | 3, 2 | 5, 3, 4 | $(5 - 2, 3 - 2, 4 - 3) = (3, 1, 1)$ |
| 4 | 4, 0 | 4, 1 | 4, 5, 2 | 4, 5, 3 | $(4 - 3, 5 - 2, 3 - 2) = (1, 3, 1)$ |
| 5 | 5, 3, 0 | 5, 1 | 5, 2 | 3, 4, 5 | $(3 - 2, 4 - 3, 5 - 2) = (1, 1, 3)$ |

For example, $R_1(3)$ is bounded by $P_2(3) = 3, 4, 1$, $P_3(3) = 3, 2$ and the edge $1\text{-}2$, and contains 5 inside, so it has the 5 vertices $3, 4, 1, 2, 5$. Every coordinate triple sums to $n - 1 = 5$. With L8, the drawing is $0 \mapsto (4, 1)$, $1 \mapsto (0, 4)$, $2 \mapsto (1, 0)$, $3 \mapsto (3, 1)$, $4 \mapsto (1, 3)$, $5 \mapsto (1, 1)$, on the $4 \times 4$ grid: the inner triangle $3, 4, 5$ sits inside the outer triangle $0, 1, 2$, and no two edges cross.

For $K_4$, the inner vertex gets $(1, 1, 1)$ and the corners $(2, 1)$, $(0, 2)$, $(1, 0)$: a $2 \times 2$ grid. A single vertex and a tree are first triangulated by L1; a star with 5 leaves becomes a triangulation on 6 vertices and is drawn on the $4 \times 4$ grid. $K_5$ and $K_{3,3}$ have no planar rotation system, and the implementation rejects any rotation system of them because it fails Euler's formula.

## Correctness

The [proof](proofs/correctness.md) has four parts. Line L1 keeps the graph simple and plane and ends with a triangulation. The peeling of line L3 never gets stuck: on the boundary path, take a chord whose ends are closest on the path; the vertices between its ends have no chord. Line L4 produces a Schnyder wood: two linear orders, the canonical ordering and a left-to-right order, show that the three paths from a vertex meet only at the vertex.

The geometric part follows Schnyder. A path of colour $i + 1$ starting inside $R_i(v)$ cannot leave it, because every edge of that colour entering the boundary of $R_i(v)$ comes from outside. So $u \in R_i(v)$ implies $R_i(u) \subseteq R_i(v)$, and $u \ne v$ gives $x_i(u) < x_i(v)$, or a tie in coordinate $i$ that coordinate $i + 1$ breaks. Every edge lies in one region of every vertex not on it, so each vertex beats every edge it is not on in some coordinate. With only three coordinates, two crossing edges would need four different winning coordinates, which is impossible.

## Complexity

**Time.** Line L1 takes $O(n)$: a [depth-first search](/depth-first-search/) for the biconnected components, one pass over the corners, and one pass over the faces, each new edge inserted in $O(1)$ when the rotations are doubly linked lists. Line L3 removes $n - 2$ vertices; each vertex enters the path once and then scans its neighbours once to count chords, and the chord counts change $O(1)$ times per edge, so L3 takes $O(m) = O(n)$ time, using $m \le 3n - 6$. Lines L5 to L7 make a constant number of passes over each tree. In total $\Theta(n)$, in the best case too, since every vertex gets a coordinate.

**Space.** The rotations, the three parent maps, the subtree sizes and the path sums take $\Theta(n)$ words.

The reference implementation keeps rotations as Python lists and finds positions with `index`, which costs $O(\deg v)$ per insertion in L1; this does not change the results.

## Properties

- **Grid size.** All coordinates lie in $\{0, \ldots, n - 2\}$: inner vertices have every coordinate between 1 and $n - 3$, and the corners use 0, 1 and $n - 2$. The area is $(n - 2)^2$.
- **Integer arithmetic only.** Unlike a [Tutte drawing](/tutte-spring-theorem/), no linear system is solved, and the coordinates have $O(\log n)$ digits.
- **Realizes the embedding.** The drawing keeps the given rotation system and the chosen outer face.
- **Not convex in general.** The faces of the input graph need not be convex in the drawing; the triangles of the triangulation are, trivially.
- **Deterministic.** The result depends on the choice of the outer face and on the order in which chord-free vertices are removed.

## Variants and improvements

- **Face counts.** Counting faces instead of vertices in each region gives coordinates that sum to $2n - 5$, on a $(2n - 5) \times (2n - 5)$ grid. The proof is simpler, since every vertex strictly gains in each region, with no ties to break.
- **Shift method.** The [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) algorithm uses the same canonical ordering but places vertices one by one, shifting parts of the drawing to the right, on a $(2n - 4) \times (n - 2)$ grid.
- **Convex drawings.** For 3-connected graphs, variants of both methods give drawings with convex faces on grids of size $O(n) \times O(n)$.
- **Orthogonal and visibility drawings.** The three trees also give other drawing styles, and Schnyder's original use of the trees was a characterization of planarity by the dimension of a partial order (see [Schnyder woods](/schnyder-woods/)).

## When to use it

Use it when you need exact, small integer coordinates for a planar graph, for example to export a drawing, to test geometric predicates exactly, or to get a guaranteed polynomial grid size. If you want drawings that look balanced, prefer a [Tutte drawing](/tutte-spring-theorem/) or a force-directed layout: Schnyder drawings tend to squeeze many vertices close to one side and to make long thin triangles. If you need convex faces for a 3-connected graph, a Tutte drawing gives them directly.

## Pitfalls

- **Orientation.** The outer face must be listed counterclockwise, so that $(a_1, a_3, a_2)$ is a face walk of $\rho$. With the opposite order, the peeling of L3 scans the wrong side of each vertex. The implementation checks this and raises an error.
- **The correction term.** Using $|R_i(v)|$ without subtracting $|P_{i-1}(v)|$ breaks the sum $x_1 + x_2 + x_3 = n - 1$; the vertices then do not lie on one plane, and the projection to two coordinates can cross.
- **Multi-edges in L1.** Triangulating a face by joining one vertex to all others can create parallel edges when that vertex already has a chord outside the face. The test before adding $v_0 v_2$ avoids this.
- **Faces with repeated vertices.** Before the faces are cut into triangles, the graph must be 2-connected; a face walk of a tree passes the same vertex several times, and cutting it naively can create loops.
- **Chord counts.** When the removed vertex has no lower neighbours, the edge between its two path neighbours turns from a chord into a path edge, and both counts must drop.

## Implementations

## History

Walter Schnyder introduced the three trees, now called Schnyder woods or realizers, in 1989 to prove that a graph is planar exactly when its incidence order has dimension at most 3. In 1990, at the first SODA, he used the same trees to draw every planar graph on an $(n - 2) \times (n - 2)$ grid in linear time, the same year in which de Fraysseix, Pach and Pollack published their shift method on a $(2n - 4) \times (n - 2)$ grid. Both answered the question, raised by Rosenstiehl and Tarjan, whether planar graphs have straight-line drawings with polynomially bounded integer coordinates. The construction of the woods from a canonical ordering, used here, makes the link between the two methods explicit.

## References
