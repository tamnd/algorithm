---
tag: YR9BXZ
kind: problem
slug: st-numbering
name: st-numbering
aliases:
- st-ordering
- bipolar orientation
area: graphs/planar-graphs
level: advanced
summary: Ordering of the vertices of a biconnected graph with s first and t last, such that each other vertex has neighbours on both sides.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n + m)}
  space: {extra: O(n + m)}
prereqs: [biconnected-graph, depth-first-search, topological-sort]
see_also: [lempel-even-cederbaum-st-numbering, ear-decomposition, planarity-testing, pq-tree, biconnected-components, canonical-ordering, planar-dual-graph, planar-straight-line-drawing]
sources:
  - paper: "Abraham Lempel, Shimon Even and Israel Cederbaum, An algorithm for planarity testing of graphs, Theory of Graphs, International Symposium, Rome 1966, Gordon and Breach, 215 to 232 (1967)"
    locator: the definition of st-numbering, the proof that every 2-connected graph has one for every edge st, and its use in the vertex-addition planarity test
  - paper: doi:10.1016/0304-3975(76)90086-4
    title: Shimon Even and Robert Endre Tarjan, Computing an st-numbering, Theoretical Computer Science 2(3), 339 to 344 (1976)
    locator: the linear-time algorithm based on depth-first search and low points
  - paper: doi:10.1016/S0022-0000(76)80045-1
    title: Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3), 335 to 379 (1976)
    locator: the linear-time planarity test that processes the vertices in st-order
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the sections on st-numberings, st-planar graphs and visibility representations
---

An st-numbering of a graph $G$ for two vertices $s \ne t$ numbers the vertices $1, \ldots, n$ so that $s$ gets 1, $t$ gets $n$, and every other vertex has a neighbour with a smaller number and a neighbour with a larger number. Orienting every edge from the smaller to the larger number gives an acyclic orientation whose only source is $s$ and whose only sink is $t$, a *bipolar orientation*; conversely, any topological order of a bipolar orientation is an st-numbering. Lempel, Even and Cederbaum showed in 1967 that every [2-connected graph](/biconnected-graph/) has an st-numbering for every edge $st$, and Even and Tarjan computed one in $O(n + m)$ time in 1976. The order drives vertex-addition [planarity tests](/planarity-testing/) and many planar drawing algorithms.

## In plain words

Pick a start node $s$ and an end node $t$. You want to list all nodes in a row, starting with $s$ and ending with $t$, so that every node in between has at least one link to a node earlier in the row and at least one link to a node later in the row. Then from every node you can walk forward step by step to $t$, and backward step by step to $s$.

Such a row exists exactly when the network has no weak point: removing any single node leaves it connected, after you add a link between $s$ and $t$ if there is none.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n \ge 2$ vertices and $m$ edges, and two vertices $s \ne t$. Often $st \in E$ is required. No embedding is needed: the problem is about abstract graphs, even though its main uses are planar. When $G$ is planar and comes with an embedding as a [rotation system](/rotation-system/), and $s$ and $t$ lie on the outer face, the bipolar orientation is called an *st-planar* orientation.

**Output.** A bijection $\sigma : V \to \{1, \ldots, n\}$ with $\sigma(s) = 1$, $\sigma(t) = n$, and for every $v \notin \{s, t\}$ neighbours $u, w$ with $\sigma(u) < \sigma(v) < \sigma(w)$; or the answer that none exists.

**Existence.** An st-numbering exists if and only if the graph $G + st$ is 2-connected. If $\sigma$ is an st-numbering, every vertex $v$ has an increasing path to $t$ and a decreasing path to $s$. Remove any vertex $c$. A vertex $v$ with $\sigma(v) < \sigma(c)$ keeps its decreasing path to $s$, whose numbers are all below $\sigma(c)$; a vertex with $\sigma(v) > \sigma(c)$ keeps its increasing path to $t$; and the edge $st$ joins $s$ and $t$. If $c = s$ or $c = t$, the increasing or decreasing paths alone connect everything. So $G + st - c$ is connected for every $c$. Conversely, if $G + st$ is 2-connected, an [ear decomposition](/ear-decomposition/) starting with a cycle through $st$ builds the numbering ear by ear: each new open ear is a path between two numbered vertices, and its inner vertices are inserted, in path order, between the numbers of its ends.

## Variants

- **Bipolar orientation.** Output the orientation instead of the numbering; the two are interchangeable in linear time through a [topological sort](/topological-sort/).
- **st-planar orientation.** For a plane graph with $s$ and $t$ on the outer face, the bipolar orientation induces a bipolar orientation of the [dual graph](/planar-dual-graph/) and gives a left-to-right order of the faces; this is the basis of visibility representations and upward drawings.
- **Canonical ordering.** For maximal planar and 3-connected planar graphs, the [canonical ordering](/canonical-ordering/) is a stronger st-order in which every prefix induces a 2-connected graph and every suffix a connected one.
- **Counting and enumeration.** The number of st-numberings can be exponential in $n$; enumeration and the choice of orientations with short longest paths are studied for drawing.
- **Dynamic and parallel versions.** st-numberings can be maintained under edge insertions and computed in parallel through ear decompositions.

## Examples

Counts by brute force over all orders.

| graph | $s, t$ | number of st-numberings | one of them |
|---|---|---|---|
| a single vertex | $s = t$ | not defined; the problem needs $s \ne t$ | |
| a path $s, \ldots, t$ | its two ends | 1 | the path order |
| a tree that is not a path | any $s, t$ | 0: a leaf other than $s, t$ has only one neighbour | |
| the star $K_{1,3}$ | two leaves | 0 | |
| the cycle $C_4$: $0, 1, 2, 3$ | $s = 0$, $t = 1$, adjacent | 1 | $0, 3, 2, 1$ |
| $C_4$ | $s = 0$, $t = 2$, opposite | 2 | $0, 1, 3, 2$ |
| $K_4$ | $s = 0$, $t = 3$ | 2 | any order of the middle |
| $K_5$ | $s = 0$, $t = 4$ | 6 | any order of the middle |
| $K_{3,3}$, sides $\{0, 1, 2\}$ and $\{3, 4, 5\}$ | $s = 0$, $t = 3$, adjacent | 8 | $0, 4, 1, 5, 2, 3$ |
| $K_{3,3}$ | $s = 0$, $t = 1$, same side | 12 | $0, 3, 2, 4, 5, 1$ |

A tree with at least 3 vertices has an st-numbering only when it is a path with $s$ and $t$ at its ends, in line with the criterion: adding $st$ to a tree makes it 2-connected only in that case. $K_5$ and $K_{3,3}$ are not planar but are 3-connected, so they have st-numberings for every pair $s, t$. The problem does not depend on planarity; only its applications do.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| Lempel, Even and Cederbaum (1967) | polynomial | existence proof by paths, used inside their planarity test |
| [Even-Tarjan](/lempel-even-cederbaum-st-numbering/) (1976) | $O(n + m)$ | a [depth-first search](/depth-first-search/) from $t$ with first edge $ts$, low points, then paths added one by one |
| Tarjan's streamlined version (1986) | $O(n + m)$ | one search computes a list order directly: each vertex is inserted before or after its parent according to a sign at its low point |
| by ear decomposition | $O(n + m)$ | number the vertices of an open ear decomposition that starts with the edge $st$, inserting each ear between its ends |

The Even-Tarjan algorithm is described in full on the page of the [Lempel-Even-Cederbaum st-numbering](/lempel-even-cederbaum-st-numbering/) algorithm.

## Bounds

- **Time.** $\Theta(n + m)$: the problem can be solved in linear time, and every algorithm must read every edge, since a single missing edge can destroy 2-connectivity.
- **Testing.** Whether a given numbering is an st-numbering can be checked in $O(n + m)$ time by looking at the smallest and largest neighbour of each vertex.
- **Space.** $O(n + m)$ for the graph and the search.

## Reductions

- **To 2-connectivity.** By the existence criterion, deciding whether an st-numbering exists is the same as testing whether $G + st$ is 2-connected, which a [biconnected components](/biconnected-components/) computation answers in linear time.
- **To topological sorting.** A bipolar orientation becomes an st-numbering by a [topological sort](/topological-sort/), and back by orienting each edge upward.
- **From planarity testing.** Vertex-addition planarity tests, the Lempel-Even-Cederbaum test and its linear-time form with [PQ-trees](/pq-tree/) by Booth and Lueker, add the vertices in st-order, so that every partial graph has its unembedded edges on the outer face.

## Applications

- **Planarity testing.** The st-order lets the Lempel-Even-Cederbaum test add one vertex at a time; Booth and Lueker made it linear with PQ-trees.
- **Planar drawing.** Visibility representations, upward drawings and some polyline grid drawings of plane graphs start from an st-planar orientation.
- **Independent paths and trees.** In a 2-connected graph, an st-numbering gives for every vertex an increasing path to $t$ and a decreasing path to $s$; such pairs underlie two independent spanning trees and fault-tolerant routing.
- **Graph partitioning.** Cutting an st-numbering at any position splits the graph into two connected parts, the vertices before the cut and those after it.

## References
