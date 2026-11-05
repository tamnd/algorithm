---
tag: H778AC
kind: concept
slug: bfs-layers
name: BFS layers
aliases:
- BFS levels
- distance layers
area: graphs/traversal
level: intro
summary: The sets of vertices at each distance from the source, produced in BFS order.
prereqs: [breadth-first-search]
see_also: [bfs-tree, multi-source-bfs, bipartiteness-check, bipartite-odd-cycle-theorem, eccentricity, parallel-bfs, direction-optimizing-bfs, edge-classification]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.2, Graph connectivity and graph traversal (the layers L0, L1, L2 of breadth-first search and the facts that layer j holds the nodes at distance j and that the ends of an edge are in the same or adjacent layers), and Section 3.4, Testing bipartiteness
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (shortest-path distances, the queue holds at most two distances at a time)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 4, Section 4.2, Breadth-first search (the layers of the search by distance)
---

The BFS layers of a graph from a source $s$ are the sets $L_0, L_1, L_2, \ldots$ where $L_i$ holds the vertices at distance exactly $i$ from $s$, counted in edges. [Breadth-first search](/breadth-first-search/) finds them in this order: it takes all of $L_i$ out of its queue before any vertex of $L_{i+1}$, and it computes $L_{i+1}$ as the vertices that are new and have an edge from $L_i$. The layers give the distances, the shape of the [BFS tree](/bfs-tree/), a test for [bipartite graphs](/bipartite-graph/), and the frontier of [parallel BFS](/parallel-bfs/).

## In plain words

Drop a stone in water and watch the rings. The first ring is the stone itself. The next ring is everything one step away. The ring after that is everything two steps away that was not in an earlier ring.

BFS layers are these rings in a network. Layer 0 is the start. Layer 1 is its neighbours. Layer 2 is every new vertex that is next to layer 1, and so on. A vertex lies in layer $i$ exactly when its shortest route from the start uses $i$ steps.

In a network where roads go both ways, a road never jumps over a ring: it stays in one ring or joins two rings that are side by side.

## The idea

Let $G = (V, E)$ be a directed or undirected graph, $s \in V$, and $\delta(s, v)$ the least number of edges on a path from $s$ to $v$, or $\infty$ if there is none. The *layers* are

$$L_i = \{ v \in V : \delta(s, v) = i \}, \qquad i = 0, 1, 2, \ldots$$

So $L_0 = \{s\}$, the layers are pairwise disjoint, and their union is the set of vertices reachable from $s$. If $L_k$ is empty, then all later layers are empty too, because a vertex at distance $j > k$ has a vertex at distance $k$ on each of its shortest paths. The largest $i$ with $L_i \ne \emptyset$ is the *eccentricity* of $s$ in its reachable part.

**Recursion.** For $i \ge 0$,

$$L_{i+1} = \{ v \notin L_0 \cup \cdots \cup L_i : (u, v) \in E \text{ for some } u \in L_i \}.$$

*Proof.* Let $v \in L_{i+1}$. Then $v$ is not in an earlier layer. Take a shortest path from $s$ to $v$, with $i + 1$ edges, and let $u$ be the vertex before $v$. The part from $s$ to $u$ has $i$ edges, so $\delta(s, u) \le i$, and if it were smaller, $v$ would have a path with fewer than $i + 1$ edges. So $u \in L_i$ and $(u, v) \in E$. Conversely, let $v$ be in the right side, with $u \in L_i$ and $(u, v) \in E$. A shortest path to $u$ followed by the edge gives $\delta(s, v) \le i + 1$, and $v$ is in no layer up to $i$, so $\delta(s, v) \ge i + 1$. So $v \in L_{i+1}$. $\square$

This is the layer-by-layer form of BFS, as in Kleinberg and Tardos: compute $L_0$, then each $L_{i+1}$ from $L_i$, and stop at the first empty layer. The queue form of BFS gives the same sets. Its correctness proof shows that the queue always holds vertices of at most two consecutive layers, $L_i$ followed by $L_{i+1}$, so BFS dequeues all of $L_i$ before any vertex of $L_{i+1}$.

**Edges between layers.** Let $(u, v) \in E$ with $u$ reachable. Then $\delta(s, v) \le \delta(s, u) + 1$, because a shortest path to $u$ followed by the edge reaches $v$. So:

- In a directed graph, an edge goes at most one layer forward. It can stay in its layer or go back by any number of layers.
- In an undirected graph, the edge also goes from $v$ to $u$, so $|\delta(s, u) - \delta(s, v)| \le 1$: each edge lies inside one layer or joins two adjacent layers.

**Odd cycles.** Let $G$ be undirected and connected. If no edge lies inside a layer, colour the even layers red and the odd layers blue: each edge joins adjacent layers, so it joins two colours, and $G$ is [bipartite](/bipartite-graph/). If an edge $\{u, v\}$ lies inside the layer $L_i$, follow the BFS tree up from $u$ and from $v$ to their lowest common ancestor $z$ in some layer $L_j$. The two tree paths have $i - j$ edges each, and with the edge $\{u, v\}$ they form a cycle with $2(i - j) + 1$ edges, an odd cycle, so $G$ is not bipartite. This is the BFS proof of the [bipartite odd cycle theorem](/bipartite-odd-cycle-theorem/), and the algorithm of [bipartiteness checking](/bipartiteness-check/).

## Examples

Take the undirected graph with vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, and the source 0.

| layer | vertices | computed from |
|---|---|---|
| $L_0$ | 0 | the source |
| $L_1$ | 1, 2 | the neighbours of 0 |
| $L_2$ | 3, 4 | new neighbours of 1 and 2 |
| $L_3$ | 5 | new neighbours of 3 and 4 |
| $L_4$ | 6 | new neighbours of 5 |
| $L_5$ | none | the search stops |

Vertex 7 is in no layer, so $\delta(0, 7) = \infty$. The eccentricity of 0 in its component is 4. Each of the 8 edges joins two adjacent layers, so no edge lies inside a layer, and the graph is bipartite with the sides $L_0 \cup L_2 \cup L_4 = \{0, 3, 4, 6\}$ and $L_1 \cup L_3 = \{1, 2, 5\}$, with the isolated vertex 7 on either side.

Add the edge $\{1, 2\}$. It lies inside $L_1$, and the lowest common ancestor of 1 and 2 in the BFS tree is 0. The cycle $0, 1, 2$ has $2(1 - 0) + 1 = 3$ edges, which is odd.

**Directed.** On the directed graph with the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none, from the source 0, the layers are $L_0 = \{0\}$, $L_1 = \{1, 2, 3\}$ and $L_2 = \{4\}$. The edge $1 \to 2$ lies inside $L_1$, the edge $2 \to 0$ goes one layer back, and no edge goes forward by two layers.

## Where it is used

- **Unweighted shortest paths.** The layer of $v$ is its distance. The [BFS tree](/bfs-tree/) gives a shortest path to each vertex.
- **Bipartiteness.** A connected undirected graph is bipartite exactly when no edge lies inside a layer. See [bipartiteness checking](/bipartiteness-check/).
- **Eccentricity and girth.** The number of nonempty layers from $s$, minus one, is the [eccentricity](/eccentricity/) of $s$. A BFS from each vertex, which looks for the first non-tree edge inside a layer or between two adjacent layers, gives the [girth](/girth/) of an undirected graph in $O(nm)$ time.
- **Several sources.** With all sources in $L_0$, the layers give the distance to the nearest source. See [multi-source BFS](/multi-source-bfs/).
- **Parallel BFS.** A layer is a *frontier*, and the vertices of one frontier can be scanned at the same time. [Parallel BFS](/parallel-bfs/) and [direction-optimizing BFS](/direction-optimizing-bfs/) work layer by layer, and the number of rounds is the number of layers.

## References
