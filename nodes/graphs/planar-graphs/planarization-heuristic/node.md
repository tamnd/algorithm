---
tag: 8EHK3E
kind: algorithm
slug: planarization-heuristic
name: Planarization heuristic
aliases:
- planarization method
area: graphs/planar-graphs
level: advanced
summary: Heuristic that finds a large planar subgraph, then inserts the remaining edges as crossings.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of edges left out of the planar subgraph, C: the number of crossings produced}
  time: {worst: O(n m + k (n + m + C))}
  space: {extra: O(n + m + C)}
properties: {deterministic: true, recursive: false}
prereqs: [planarity-testing, planar-dual-graph, planar-face-finding]
see_also: [crossing-number, planar-embedding, rotation-system, graph-drawing, planar-straight-line-drawing, boyer-myrvold-planarity-test, breadth-first-search, crossing-lemma]
sources:
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the planarization approach in the chapters on flow and orthogonal drawings (planar subgraph, edge insertion by shortest paths in the dual, dummy vertices for crossings)
  - paper: "Carlo Batini, Maurizio Talamo and Roberto Tamassia, Computer aided layout of entity relationship diagrams, Journal of Systems and Software 4(2-3), 163 to 173 (1984)"
    locator: the planarization step of the layout pipeline, with crossings replaced by dummy vertices
  - paper: "Carsten Gutwenger, Petra Mutzel and René Weiskircher, Inserting an edge into a planar graph, Algorithmica 41(4), 289 to 308 (2005)"
    locator: inserting one edge with the fewest crossings over all embeddings, in linear time with SPQR-trees, versus the fixed-embedding insertion by a dual shortest path
  - paper: "G. Demoucron, Y. Malgrange and R. Pertuiset, Graphes planaires, reconnaissance et construction de représentations planaires topologiques, Revue Française de Recherche Opérationnelle 8, 33 to 47 (1964)"
    locator: the path addition planarity test with fragments and admissible faces, used by the implementation
---

The planarization heuristic draws a non-planar graph by turning it into a planar one. It first keeps a maximal planar subgraph $P$: it scans the edges and keeps each one that does not destroy planarity. Then it fixes an embedding of $P$ and inserts each left-out edge $uv$ along a shortest path in the dual graph, from a face at $u$ to a face at $v$. Each edge it crosses is split by a new *dummy vertex* of degree 4. The result is a planar graph, the *planarization*, that any planar drawing algorithm can draw; turning the dummy vertices back into crossings gives a drawing of the original graph. The method was introduced by Batini, Talamo and Tamassia in 1984. It is still the most successful practical approach to drawings with few crossings, although computing the [crossing number](/crossing-number/) exactly is NP-hard.

## In plain words

You want to draw a network on paper with as few crossing lines as possible. Start by putting in lines one by one, skipping any line that would force a crossing no matter how the drawing is arranged. Now you have a crossing-free drawing of most of the network.

For each skipped line, look at the regions of the current drawing. Find a way from a region touching one end to a region touching the other end that passes through as few walls as possible. Draw the line along that way, and put a small dot at every place where it crosses a wall. The dots turn the crossings into ordinary junctions, so the picture stays crossing-free and the next skipped line can be added the same way.

## The problem

**Input.** A simple undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, in a given edge order. No embedding is given: the algorithm finds one.

**Output.** A planar graph $H$ with vertex set $V \cup D$, where $D$ is a set of *dummy vertices*, with a planar embedding given as a [rotation system](/rotation-system/) $\rho$ ($\rho(x)$ lists the neighbours of $x$ counterclockwise), such that

1. every edge $uv$ of $G$ becomes a path $u, d_1, \ldots, d_j, v$ in $H$ whose inner vertices are dummy vertices, and every edge of $H$ lies on exactly one such path;
2. every dummy vertex has degree 4 and lies on exactly two of these paths, and in $\rho$ the neighbours of the two paths alternate, so the paths really cross.

The number of crossings is $C = |D|$. Drawing $H$ without crossings and erasing the dummy vertices gives a drawing of $G$ with exactly $C$ crossings. The goal is to make $C$ small; the minimum over all drawings is the [crossing number](/crossing-number/) $\text{cr}(G)$.

Faces are traced with the convention of [face finding](/planar-face-finding/): the dart after $(a, b)$ is $(b, c)$, where $c$ is the neighbour just before $a$ in $\rho(b)$. A *corner* of a vertex $x$ on a face is a pair of consecutive darts $(a, x), (x, c)$ of the face; putting a new neighbour $w$ of $x$ between $c$ and $a$ in $\rho(x)$ draws the new edge inside that face.

## The algorithm

```pseudo id=main
PLANARIZE(G)                                ▷ G = (V, E), edges in a fixed order
L1  P ← (V, ∅), R ← empty list
L2  for each edge e = uv of G in order
L3      if P + e is planar then add e to P else append e to R
L4  ρ ← a planar rotation system of P, H ← P
L5  for each edge uv in R
L6      F ← the faces of (H, ρ)
L7      BFS in the dual of H from all faces at u until a face at v: faces f_0, ..., f_k, crossing edges e_1, ..., e_k
L8      for i ← 1 to k: split e_i = x_i y_i by a new dummy vertex d_i
L9      add the path u, d_1, ..., d_k, v; its i-th edge goes through f_{i-1}, put into corners of that face
L10 return (H, ρ)
```

Line L3 is a [planarity test](/planarity-testing/); with a linear-time test such as [Boyer-Myrvold](/boyer-myrvold-planarity-test/) it costs $O(n)$, because $P + e$ has at most $3n - 5$ edges. Line L4 uses the same test to produce an embedding.

Line L7 is a [breadth-first search](/breadth-first-search/) in the [dual graph](/planar-dual-graph/): the faces are nodes, and crossing an edge moves from the face on one side to the face on the other. All faces at $u$ start at distance 0, and the search stops at the first face that contains $v$; so the search never crosses an edge at $u$ or $v$, and if $u$ and $v$ share a face, $k = 0$ and the edge is added with no crossing.

At line L8, the dart $(x_i, y_i)$ belongs to $f_{i-1}$ and $(y_i, x_i)$ to $f_i$. After the split, $\rho(d_i) = (x_i, y_i)$. At line L9, the edge into $d_i$ from the earlier face is put in the corner after $y_i$, and the edge to the later face in the corner after $x_i$. So $\rho(d_i) = (x_i, d_{i+1}, y_i, d_{i-1})$ (with $d_0 = u$ and $d_{k+1} = v$), and the two paths alternate at $d_i$.

## Example

**$K_5$ in lexicographic edge order.** The edges $01, 02, 03, 04, 12, 13, 14, 23, 24$ are kept at line L3: $K_5$ minus an edge is planar. The last edge $34$ would make $K_5$, so $R = (34)$. The embedding found at line L4 is

| vertex | $\rho$ |
|---|---|
| 0 | $1, 4, 2, 3$ |
| 1 | $0, 3, 2, 4$ |
| 2 | $0, 4, 1, 3$ |
| 3 | $0, 2, 1$ |
| 4 | $0, 1, 2$ |

with the six triangular faces $(0, 1, 4)$, $(0, 4, 2)$, $(0, 2, 3)$, $(0, 3, 1)$, $(1, 3, 2)$, $(1, 2, 4)$. The faces at 3 are $(0, 2, 3)$, $(0, 3, 1)$ and $(1, 3, 2)$, and none of them contains 4. The search crosses the edge $02$ from $(0, 2, 3)$ into $(0, 4, 2)$, which contains 4: $k = 1$. Line L8 splits $02$ by the dummy vertex 5, and line L9 adds $3\text{-}5$ and $5\text{-}4$, with $\rho(5) = (0, 4, 2, 3)$. The two paths $0, 5, 2$ and $3, 5, 4$ alternate at 5. The result has 1 crossing, which is $\text{cr}(K_5)$.

**$K_{3,3}$** with sides $\{0, 1, 2\}$ and $\{3, 4, 5\}$ in lexicographic order: the first eight edges are kept and $25$ is left out. The embedding of $P$ has the four faces $(0, 3, 2, 4)$, $(0, 4, 1, 5)$, $(0, 5, 1, 3)$ and $(1, 4, 2, 3)$. Vertex 2 lies on the first and the last, vertex 5 on the second and the third, so no face holds both. The search crosses $03$ from $(0, 3, 2, 4)$ into $(0, 5, 1, 3)$, and the edge $25$ becomes the path $2, 6, 5$ with the dummy vertex 6 on $03$: 1 crossing, which is $\text{cr}(K_{3,3})$.

**Small cases.** A single vertex, a tree and $K_4$ are planar: every edge is kept, $R$ is empty, and the output is a planar embedding with $C = 0$. For $K_6$ in lexicographic order, the heuristic gives 3 crossings, which equals $\text{cr}(K_6) = 3$.

**The edge order matters.** Over 100 random edge orders, $K_{4,4}$ gave 4 crossings 67 times and 5 crossings 33 times, while $\text{cr}(K_{4,4}) = 4$; the Petersen graph gave 2 crossings 98 times and 3 crossings twice, while its crossing number is 2.

## Correctness

The [proof](proofs/correctness.md) shows four facts. First, $P$ is a maximal planar subgraph: for every $e \in R$, $P + e$ is not planar, because $P$ only grows and $e$ already failed the test against a subgraph of the final $P$. Second, every step of the insertion loop keeps $\rho$ a planar rotation system: splitting an edge adds one vertex and one edge, and adding an edge into two corners of one face splits that face into two, so $V - E + F$ is unchanged in each component. Third, every removed edge gets at least one crossing; if $u$ and $v$ shared a face of $H$, the drawing of $H$ plus $uv$, with the other inserted paths erased, would be a planar drawing of $P + uv$. Fourth, each insertion uses the fewest crossings possible for the current embedding of $H$, because a curve from $u$ to $v$ passes through a sequence of faces in which consecutive faces are separated by a crossed edge, which is a walk in the dual.

## Complexity

- **Phase 1, lines L1 to L4.** There are $m$ planarity tests on graphs with $n$ vertices and $O(n)$ edges. With a linear-time test, this takes $O(n m)$ time.
- **Phase 2, lines L5 to L9.** Each insertion traces the faces and runs a breadth-first search on a planar graph with $n + C' \le n + C$ vertices and at most $m + 2C$ edges, where $C'$ is the number of crossings so far. So each insertion takes $O(n + m + C)$ time, and all $k$ insertions take $O(k (n + m + C))$ time.
- **Space.** $O(n + m + C)$ for $H$, $\rho$, the faces and the search.

The implementation below uses the simpler Demoucron-Malgrange-Pertuiset path addition test, which takes $O(n^2)$ time per test, so its phase 1 takes $O(m n^2)$ time.

## Properties

- **Deterministic.** For a fixed edge order and fixed tie-breaking in the planarity test and in the search, the output is fixed.
- **Not optimal.** The crossing count depends on the edge order, on the embedding chosen for $P$, and on the order in which edges are inserted; it can exceed $\text{cr}(G)$, as the $K_{4,4}$ and Petersen examples show.
- **Lower bounds checked for free.** Every removed edge costs at least one crossing, so $C \ge k$; and by the [edge bound](/planar-edge-bound/), $k \ge m - (3n - 6)$ for $n \ge 3$.
- **Adjacent and repeated crossings.** The inserted edges never cross edges at their own ends. An inserted edge never crosses the same piece of an edge twice, but two different edges of $G$ may cross more than once, which an optimal drawing never does.

## Variants and improvements

- **Maximum instead of maximal planar subgraph.** Finding a planar subgraph with the most edges is NP-hard; branch and cut methods solve it exactly for moderate sizes, and better subgraphs usually lead to fewer crossings.
- **Optimal insertion over all embeddings.** Gutwenger, Mutzel and Weiskircher showed how to insert one edge with the fewest crossings over all embeddings of a planar graph, in linear time, using SPQR-trees. This is better than the fixed-embedding search of line L7.
- **Postprocessing.** Removing each edge again and reinserting it optimally, until no improvement, typically reduces crossings considerably.
- **Randomized restarts.** Running the heuristic with many random edge orders and keeping the best result is simple and effective, as the example with $K_{4,4}$ suggests.
- **Topology-shape-metrics.** In orthogonal drawing, the planarization is the first of three steps, followed by bend minimization by network flow and compaction.

## When to use it

Use it to draw a sparse, nearly planar graph with few crossings, for example a diagram, a circuit or a network map: it is the standard first step of orthogonal and planar drawing pipelines. For graphs that are already planar it reduces to computing a [planar embedding](/planar-embedding/). For dense graphs, where every drawing has many crossings by the [crossing lemma](/crossing-lemma/), force-directed layouts are usually preferred, because the planarization becomes large and its structure is not visible in the drawing anyway.

## Pitfalls

- **Corners, not just faces.** A vertex can appear several times on one face, and the new edge must be put into a corner of the face that the search actually used; putting it between the wrong pair of neighbours makes the rotation system non-planar without any error.
- **Orientation at dummy vertices.** The neighbours of a dummy vertex must alternate between the two crossing paths; the order $x, d_{i+1}, y, d_{i-1}$ depends on which side of the split edge the path comes from.
- **Updating the faces.** After an insertion the faces change, so the dual must be recomputed or updated before the next edge, as line L6 does.
- **Multigraphs and loops.** The method assumes a simple graph; parallel edges should be merged or routed together.
- **Edges between components.** Edges joining two components of $P$ are always kept at line L3, so every removed edge has both ends in one component of $H$ and the dual search succeeds.

## Implementations

## History

Batini, Talamo and Tamassia introduced the planarization approach in 1984 for laying out entity relationship diagrams, as the first step of what became the topology-shape-metrics approach to orthogonal drawing. The planar subgraph step uses planarity tests going back to Demoucron, Malgrange and Pertuiset (1964) and to the linear-time tests of Hopcroft and Tarjan (1974) and of Boyer and Myrvold (2004). Computing a maximum planar subgraph was shown NP-hard in the late 1970s, and computing the crossing number by Garey and Johnson in 1983, which explains why a heuristic is used. In 2005 Gutwenger, Mutzel and Weiskircher made single-edge insertion optimal over all embeddings, and planarization with postprocessing remains the method of choice in graph drawing libraries such as OGDF.

## References
