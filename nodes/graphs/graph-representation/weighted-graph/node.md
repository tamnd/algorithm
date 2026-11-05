---
tag: TAHZEZ
kind: definition
slug: weighted-graph
name: Weighted graph
aliases:
- edge-weighted graph
area: graphs/graph-representation
level: intro
summary: Graph in which each edge carries a numeric weight or cost.
prereqs: [graph, edge]
see_also: [shortest-path, minimum-spanning-tree, dijkstra, bellman-ford, negative-cycle, adjacency-list, adjacency-matrix, laplacian-matrix]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), weighted graphs with a weight function w from E to the reals, stored in adjacency lists and in matrices; Chapter 22 (Single-source shortest paths), path weights and negative-weight edges
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3 (Minimum spanning trees), the edge-weighted graph API with Edge objects; Section 4.4 (Shortest paths), the edge-weighted digraph
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.3, weighted graphs, minimum spanning trees and shortest paths
---

A weighted graph is a [graph](/graph/) together with a number on each [edge](/edge/), its weight. The weight may stand for a length, a cost, a time, a capacity or a probability. Most optimisation problems on graphs are posed on weighted graphs: [shortest paths](/shortest-path/) minimise the total weight of a path, and a [minimum spanning tree](/minimum-spanning-tree/) minimises the total weight of a tree. The graph may be directed or undirected; the weight is extra data and does not change which edges exist.

## Definition

A **weighted graph** is a pair $(G, w)$ of a graph $G = (V, E)$, [directed](/directed-graph/) or [undirected](/undirected-graph/), and a **weight function**

$$w : E \to \mathbb{R}.$$

For an undirected edge, $w(\{u, v\})$ is one number, also written $w(u, v) = w(v, u)$. For a directed graph, $w(u, v)$ and $w(v, u)$ are the weights of two different edges and can differ. Write $n = |V|$ and $m = |E|$.

**Weights of larger objects.** The weight of a set $F \subseteq E$ is $w(F) = \sum_{e \in F} w(e)$. For a path or walk $p = (v_0, v_1, \ldots, v_k)$ it is $w(p) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$, with each edge counted as often as the walk uses it. The *shortest-path distance* is $\delta(u, v) = \min\{w(p) : p \text{ a path from } u \text{ to } v\}$, with $\delta(u, v) = \infty$ when $v$ is not reachable. If a cycle reachable from $u$ has negative total weight, the minimum over walks does not exist, and $\delta(u, v) = -\infty$ for the vertices after it; see [negative cycle](/negative-cycle/).

**Classes of weights.** Algorithms depend on the range of $w$:

| range | what it allows | example |
|---|---|---|
| all $w(e) = 1$ | the unweighted graph; distance is the number of edges | [breadth-first search](/breadth-first-search/) |
| $w(e) \ge 0$ | greedy shortest paths | [Dijkstra](/dijkstra/) |
| any real, no negative cycle | shortest paths are defined | [Bellman-Ford](/bellman-ford/), [Floyd-Warshall](/floyd-warshall/) |
| integers in $\{0, \ldots, C\}$ | bucket and radix methods | Dial's algorithm |
| $w(e) > 0$ for an undirected graph | the [Laplacian matrix](/laplacian-matrix/) and electrical flows | |

A [minimum spanning tree](/minimum-spanning-tree/) is defined for any real weights, negative ones included, since adding a constant to every weight does not change which tree is lightest.

**The model of the input.** On the [word RAM](/word-ram/), each weight is a word, and adding or comparing two weights costs $O(1)$. A bound that also depends on the size of the numbers, such as $O(m \log C)$, is said to be *weakly polynomial*; one that does not is *strongly polynomial*.

**Representations.** Weights are stored next to the structure:

| representation | where $w(u, v)$ is | space | read $w(u, v)$ |
|---|---|---|---|
| [adjacency list](/adjacency-list/) | a field in the list entry of $v$ in $\text{Adj}[u]$ | $\Theta(n + m)$ | $O(1 + d(u))$ |
| [adjacency matrix](/adjacency-matrix/) | $A[u, v]$, with a sentinel such as $\infty$, 0 or NIL for "no edge" | $\Theta(n^2)$ | $O(1)$ |
| [edge list](/edge-list/) | a triple $(u, v, w)$ | $\Theta(m)$ | $O(m)$ |
| [compressed sparse row](/compressed-sparse-row/) | a value array parallel to the column array | $\Theta(n + m)$ | $O(\log(2 + d(u)))$ if sorted |

For an undirected graph in adjacency lists, both copies of the edge carry the weight, and an update must change both.

## Examples and non-examples

**Example.** $V = \{s, a, b, t\}$, undirected, with the weights $w(s, a) = 1$, $w(s, b) = 4$, $w(a, b) = 2$, $w(a, t) = 6$, $w(b, t) = 3$.

- The path $s, a, b, t$ has weight $1 + 2 + 3 = 6$, and the path $s, a, t$ has weight 7, so $\delta(s, t) = 6$. The path with fewest edges, $s, a, t$, is not the lightest.
- The tree $\{sa, ab, bt\}$ has weight $6$, and it is the minimum spanning tree: each other spanning tree has a heavier edge in place of one of these.

**Directed, with a negative edge.** Edges $(s, a)$ of weight 2, $(a, b)$ of weight $-1$, $(b, a)$ of weight $-2$. The cycle $a, b, a$ has weight $-3 < 0$, so $\delta(s, a) = \delta(s, b) = -\infty$. Removing $(b, a)$ gives $\delta(s, a) = 2$ and $\delta(s, b) = 1$.

**Multigraph as weights.** A [multigraph](/multigraph/) with $\mu(u, v)$ parallel edges can be stored as the simple graph with $w(u, v) = \mu(u, v)$, when the edges need no names.

**Non-examples.**

- A graph with a number on each *vertex* is vertex-weighted, not weighted in the sense here. A vertex weight $c(v)$ can be moved onto edges in a directed graph by splitting $v$ into $v_{\text{in}}$ and $v_{\text{out}}$ joined by an edge of weight $c(v)$.
- An adjacency matrix that uses 0 for "no edge" cannot hold an edge of weight 0. This is a representation choice, and it is a common source of bugs.

## Related definitions

- **Shortest path.** A path of least weight. See [shortest path](/shortest-path/) and [single-source shortest paths](/single-source-shortest-paths/).
- **Minimum spanning tree.** A spanning tree of least weight. See [minimum spanning tree](/minimum-spanning-tree/).
- **Network.** A directed graph with a capacity $c(u, v) \ge 0$ on each edge, used for maximum flow; the capacity is a weight with its own rules.
- **Laplacian.** For positive weights on an undirected graph, $L = D - W$ with the weighted degrees on the diagonal. See [Laplacian matrix](/laplacian-matrix/).
- **Negative cycle.** A cycle of negative total weight in a directed graph. See [negative cycle](/negative-cycle/).

## References
