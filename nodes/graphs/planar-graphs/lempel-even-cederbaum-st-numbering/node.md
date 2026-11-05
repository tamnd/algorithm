---
tag: SJ9RE7
kind: algorithm
slug: lempel-even-cederbaum-st-numbering
name: Lempel-Even-Cederbaum st-numbering algorithm
aliases:
- Even-Tarjan st-numbering
area: graphs/planar-graphs
level: advanced
summary: Computes an st-numbering of a 2-connected graph in linear time with one depth-first search; it is the vertex order behind the Lempel-Even-Cederbaum planarity test.
solves: [st-numbering]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, needs_embedding: false, recursive: false}
history:
  year: 1976
  people: [Abraham Lempel, Shimon Even, Israel Cederbaum, Robert E. Tarjan]
  note: Lempel, Even and Cederbaum introduced st-numberings for their 1967 planarity test; Even and Tarjan computed them in linear time in 1976, and Tarjan streamlined the method in 1986.
prereqs: [biconnected-graph, depth-first-search, low-link, doubly-linked-list]
see_also: [st-numbering, canonical-ordering, planarity-testing, hopcroft-tarjan-planarity-test, boyer-myrvold-planarity-test, ear-decomposition, hopcroft-tarjan-biconnectivity, articulation-point-finding]
sources:
  - paper: doi:10.1016/0304-3975(76)90086-4
    title: Shimon Even and Robert Endre Tarjan, Computing an st-numbering, Theoretical Computer Science 2(3), 339 to 344 (1976)
    locator: the linear-time algorithm by depth-first search and path finding
  - paper: "Robert Endre Tarjan, Two streamlined depth-first search algorithms, Fundamenta Informaticae 9, 85 to 94 (1986)"
    locator: the st-numbering algorithm with the list and the signs used on this page
  - paper: "Abraham Lempel, Shimon Even and Israel Cederbaum, An algorithm for planarity testing of graphs, in Theory of Graphs, International Symposium, Rome 1966, Gordon and Breach, 215 to 232 (1967)"
    locator: the definition of st-numberings and their use in vertex-addition planarity testing
  - paper: "Ulrik Brandes, Eliminating depth-first search from the computation of st-numberings, in Algorithms, ESA 2002, Lecture Notes in Computer Science 2461, Springer, 247 to 258 (2002)"
    locator: the analysis of Tarjan's sign algorithm and a variant without depth-first search
  - paper: "Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3), 335 to 379 (1976)"
    locator: the linear-time implementation of the Lempel-Even-Cederbaum test with PQ-trees and an st-numbering
---

An [st-numbering](/st-numbering/) of a graph $G$ for an edge $st$ numbers the vertices $1, \ldots, n$ so that $s$ gets 1, $t$ gets $n$, and every other vertex has a neighbour with a smaller number and a neighbour with a larger number. It exists exactly when $G$ plus the edge $st$ is [2-connected](/biconnected-graph/). Lempel, Even and Cederbaum introduced it in 1967 as the order in which their planarity test adds vertices. Even and Tarjan computed it in linear time in 1976. This page gives Tarjan's 1986 form: one [depth-first search](/depth-first-search/) computes [low points](/low-link/), and then each vertex is put into a list right before or right after its DFS parent, as decided by one sign bit per vertex.

## In plain words

Pick two vertices, a start and a target. We want to line up all vertices in a row from the start to the target so that every vertex in between has a neighbour on its left and a neighbour on its right. Walking along the row, you can always step forward and you can always step back.

The algorithm first explores the graph by a depth-first walk that goes from the start straight to the target. Then it visits the vertices in the order the walk found them, and puts each one right next to the vertex it was found from, on the left or the right. A single mark per vertex tells which side. The mark makes sure that the side away from the parent also holds a neighbour, through a chain of descendants that leads back to an earlier vertex.

## The problem

Input: an undirected graph $G = (V, E)$ by adjacency lists, and two different vertices $s$ and $t$. The edge $st$ is treated as present. Output: numbers $\mathrm{num}(v) \in \{1, \ldots, n\}$, all different, with $\mathrm{num}(s) = 1$, $\mathrm{num}(t) = n$, and for each $v \notin \{s, t\}$ neighbours $u, w$ with $\mathrm{num}(u) < \mathrm{num}(v) < \mathrm{num}(w)$; or a report that $G + st$ is not 2-connected, in which case no st-numbering exists. No embedding is needed: the input is the abstract graph, and the output does not depend on planarity. Orienting every edge from the smaller number to the larger gives a *bipolar orientation*: acyclic, with $s$ the only source and $t$ the only sink.

## The algorithm

```pseudo id=main
ST-NUMBER(G, s, t)                      ▷ G by adjacency lists; no embedding
L1  DFS from s that takes the edge st first; record preorder, parent p(v) and low(v)
L2  if not all vertices are reached or low(v) ≥ pre(p(v)) for some v ∉ {s, t} then fail
L3  L ← the list (s, t); sign(s) ← −
L4  for each v ∉ {s, t} in preorder do
L5      if sign(low(v)) = − then
L6          insert v just before p(v) in L; sign(p(v)) ← +
L7      else
L8          insert v just after p(v) in L; sign(p(v)) ← −
L9  number the vertices 1, 2, ..., n in the order of L
L10 return the numbers
```

Here $\mathrm{low}(v)$ is the vertex with the smallest preorder number among $v$, its descendants, and the ends of back edges from $v$ and its descendants. Line L1 makes $t$ the only child of $s$, since $s$ continues only after the whole search from $t$ ends, and line L2 then fails exactly when $G + st$ has a cut vertex or is disconnected (the standard test with [low points](/low-link/); see [articulation point finding](/articulation-point-finding/)). For every other $v$, $\mathrm{low}(v)$ is a proper ancestor of $p(v)$.

**What the sign means.** When the loop inserts a child $c$ of a vertex $x$, it sets $\mathrm{sign}(x)$ to $+$ if $c$ went before $x$ and to $-$ if $c$ went after $x$. So $\mathrm{sign}(x)$ records on which side of $x$ its most recent child lies; all later vertices of that child's subtree stay on that side. A vertex $v$ whose low point is $x$ belongs to that subtree, so $\mathrm{sign}(x) = -$ means that $x$ lies before $p(v)$; line L6 then puts $v$ between $x$ and $p(v)$, with $p(v)$ on its right and the low point on its left.

## Example

Take the triangular prism: triangles $0, 1, 2$ and $3, 4, 5$, and the edges $03$, $14$, $25$, with sorted adjacency lists. Let $s = 0$ and $t = 1$. The search goes $0, 1, 2, 5, 3, 4$, with parents $p(1) = 0$, $p(2) = 1$, $p(5) = 2$, $p(3) = 5$, $p(4) = 3$. The back edges are $20$, $30$, $41$, $45$, so $\mathrm{low}(4) = 1$ and $\mathrm{low}(2) = \mathrm{low}(5) = \mathrm{low}(3) = 0$.

| $v$ | $p(v)$ | $\mathrm{low}(v)$ | sign of low | action | $L$ after |
|---|---|---|---|---|---|
| start | | | | | 0, 1 |
| 2 | 1 | 0 | $-$ | before 1; sign(1) $\leftarrow +$ | 0, 2, 1 |
| 5 | 2 | 0 | $-$ | before 2; sign(2) $\leftarrow +$ | 0, 5, 2, 1 |
| 3 | 5 | 0 | $-$ | before 5; sign(5) $\leftarrow +$ | 0, 3, 5, 2, 1 |
| 4 | 3 | 1 | $+$ | after 3; sign(3) $\leftarrow -$ | 0, 3, 4, 5, 2, 1 |

So $\mathrm{num} = (1, 6, 5, 2, 3, 4)$ for the vertices $0, \ldots, 5$. Check: vertex 3 (number 2) has neighbours 0 (1) and 4 (3); vertex 4 (3) has 3 (2) and 5 (4); vertex 5 (4) has 4 (3) and 2 (5); vertex 2 (5) has 0 (1) and 1 (6). Vertex 4 went after its parent because its low point 1 lies at the right end.

**Small cases.** For a triangle with $s = 0$, $t = 1$ the result is $0, 2, 1$. For $K_2$, or two vertices with no edge, the result is $s, t$, since the edge $st$ is added. A single vertex has no pair $s \ne t$ and is rejected. A tree with at least 3 vertices plus one edge $st$ is 2-connected only if it is a path from $s$ to $t$; a star, or a path with $s, t$ not its ends, is rejected. $K_4$, $K_5$ and $K_{3,3}$ are 2-connected, and the tests check every ordered pair $s \ne t$ on them. Planarity plays no role: $K_5$ and $K_{3,3}$ have st-numberings like any 2-connected graph.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It rests on three facts. A vertex inserted next to its parent stays on the same side as the parent of every other vertex, because insertion never jumps over a vertex. Hence all vertices of the subtree of the most recent child of $x$ lie on one side of $x$, the side recorded by $\mathrm{sign}(x)$. Hence $\mathrm{low}(v)$ ends up on the side of $v$ away from $p(v)$, and if $\mathrm{low}(v)$ is reached through a child $c$ of $v$ with $\mathrm{low}(c) = \mathrm{low}(v)$, then $c$ lies on that side too, because the sign of $\mathrm{low}(v)$ does not change between the insertion of $v$ and that of $c$. So each $v \notin \{s, t\}$ has $p(v)$ on one side and a neighbour (the low point itself or the child $c$) on the other. The vertex $s$ stays first because nothing is ever inserted before it, and $t$ stays last because its children have low point $s$ and $\mathrm{sign}(s)$ stays $-$.

## Complexity

The depth-first search and the low points take $O(n + m)$ time. Line L2 is one pass over the vertices. Each insertion into the doubly linked list and each sign update takes $O(1)$, and line L9 walks the list once. The total is $O(n + m)$ time and $\Theta(n)$ extra space for the preorder, parents, low points, signs and the list. The search is iterative, so deep graphs (long paths) do not overflow a call stack.

## Properties

- **Any 2-connected graph.** Planarity is not needed. The output is one of possibly many st-numberings.
- **Bipolar orientation.** Orienting edges by increasing number gives an acyclic orientation with the single source $s$ and the single sink $t$; conversely, a topological order of a bipolar orientation is an st-numbering.
- **Deterministic.** The result depends on the order of the adjacency lists, which fixes the DFS tree.

## Variants and improvements

- **Even and Tarjan (1976).** The original linear-time algorithm repeatedly finds paths through unvisited vertices, using the DFS tree and low points, and numbers vertices with a stack. Tarjan's sign version is shorter.
- **Ear decompositions, without depth-first search.** An st-numbering can also be built from an open [ear decomposition](/ear-decomposition/) whose first ear contains $st$, by adding the ears in order and orienting each new ear consistently with the orientation of its ends. Brandes gives a linear-time version of this idea, which avoids depth-first search.
- **Planar graphs.** For a [maximal planar graph](/maximal-planar-graph/), a [canonical ordering](/canonical-ordering/) is an st-numbering with extra structure, used for drawing.

## When to use it

Use it as a preprocessing step: the Lempel-Even-Cederbaum planarity test adds vertices in st-order and keeps the possible embeddings in a PQ-tree (Booth and Lueker); visibility representations, upward drawings, and some 2-connected graph decompositions also start from an st-numbering or a bipolar orientation. Use the planarity tests on the [planarity testing](/planarity-testing/) page when the goal is planarity itself.

## Pitfalls

- **The edge st.** The DFS must take $st$ first, even if $st$ is not in the graph. Starting the search at $s$ without forcing $t$ as its child breaks the argument: $s$ may get several children.
- **Recursive DFS.** A recursive search overflows the stack on long paths; use an explicit stack.
- **Low point as a number versus a vertex.** The sign is stored per vertex, so the low point must be turned back into a vertex (here by the preorder list) before reading its sign.
- **Not 2-connected.** Without the check of line L2, the list is still produced but some vertex lacks a neighbour on one side.
- **Insertion position.** Insert directly next to $p(v)$; inserting at the end of the list or next to the low point gives wrong results.

## Implementations

## History

Lempel, Even and Cederbaum described in 1967 a planarity test that adds the vertices of a 2-connected graph one at a time in an order now called an st-numbering, and showed that such an order exists for every 2-connected graph. The test became linear when Booth and Lueker introduced PQ-trees in 1976. In the same year Even and Tarjan gave the first linear-time algorithm for st-numbering. Tarjan's 1986 paper on streamlined depth-first search algorithms gave the list-and-sign version on this page, and Brandes analysed it in 2002 and removed the need for depth-first search.

## References
