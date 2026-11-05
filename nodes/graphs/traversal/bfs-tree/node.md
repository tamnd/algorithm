---
tag: FY6JYX
kind: concept
slug: bfs-tree
name: Breadth-first tree
aliases:
- BFS tree
- breadth-first search tree
area: graphs/traversal
level: intro
summary: The parent pointers recorded by BFS, giving a shortest-path tree from the source.
prereqs: [breadth-first-search]
see_also: [bfs-layers, dfs-forest, shortest-path-tree, multi-source-bfs, bipartiteness-check, breadth-first-search-distributed, girth, spanning-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (breadth-first trees, the predecessor subgraph, and the procedure PRINT-PATH)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.2, Graph connectivity and graph traversal (the breadth-first search tree, and the fact that the ends of a non-tree edge differ by at most one layer)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (BreadthFirstPaths and the shortest paths it finds)
---

The breadth-first tree of a run of [breadth-first search](/breadth-first-search/) from a source $s$ is the tree formed by the edges $(\pi[v], v)$, where $\pi[v]$ is the vertex from which BFS first discovered $v$. It spans the vertices reachable from $s$, and its path from $s$ to each vertex $v$ is a shortest path of the graph, with $\delta(s, v)$ edges. So it is a [shortest path tree](/shortest-path-tree/) for unit edge lengths, and one BFS stores shortest paths to all reachable vertices in $n$ parent pointers. Compared with the [depth-first forest](/dfs-forest/), a BFS tree is short and wide: its depth is the largest distance from $s$.

## In plain words

When BFS reaches a new vertex, it got there from a vertex in the previous ring. Remember that vertex as the parent. The parents form a tree with the start at the top.

To find a shortest route from the start to any vertex, go up from that vertex, parent by parent, until you reach the start, and then read the route backwards. Each step up goes one ring closer to the start, so the route has as few steps as possible.

## The idea

**Definition.** Run BFS from $s$ on $G = (V, E)$, and let $V_\pi$ be the set of vertices with a finite distance. The *breadth-first tree* is $G_\pi = (V_\pi, E_\pi)$ with

$$E_\pi = \{ (\pi[v], v) : v \in V_\pi \setminus \{s\} \}.$$

CLRS calls $G_\pi$ the *predecessor subgraph* of the search.

**It is a shortest path tree.** The correctness proof of BFS gives $\mathrm{dist}[v] = \delta(s, v)$ for each vertex, and $\mathrm{dist}[v] = \mathrm{dist}[\pi[v]] + 1$ for each $v \in V_\pi \setminus \{s\}$, with $(\pi[v], v) \in E$. So each step from $v$ to $\pi[v]$ decreases the distance by exactly one. The chain $v, \pi[v], \pi[\pi[v]], \ldots$ reaches $s$ after exactly $\delta(s, v)$ steps, never repeats a vertex, and read backwards is a path of $G$ with $\delta(s, v)$ edges, a shortest path. Each vertex of $V_\pi$ other than $s$ has one parent, so $G_\pi$ has $|V_\pi| - 1$ edges, and since every vertex is joined to $s$, it is a tree rooted at $s$. The depth of $v$ in the tree is $\delta(s, v)$, and the vertices at depth $i$ are the [BFS layer](/bfs-layers/) $L_i$.

**Reading a path.** To print a shortest path from $s$ to $v$, follow the parents from $v$ to $s$ and print them in reverse, or recurse on $\pi[v]$ first. This takes $\Theta(\delta(s, v) + 1)$ time.

**Non-tree edges.** In an undirected graph, each edge $\{u, v\}$ of the reachable part has $|\delta(s, u) - \delta(s, v)| \le 1$. So a non-tree edge joins two vertices of the same layer, or of two adjacent layers. A non-tree edge inside a layer closes an odd cycle with the two tree paths to the lowest common ancestor, which gives the BFS test for [bipartite graphs](/bipartiteness-check/). In a directed graph, an edge goes at most one layer forward, so BFS has no forward edges in the sense of [edge classification](/edge-classification/): a non-tree edge $(u, v)$ never joins $u$ to a proper descendant two or more layers below it.

**Not every shortest path tree is a BFS tree.** BFS gives a vertex the parent that was dequeued first among its neighbours in the previous layer. Take the undirected graph with the edges $\{s, a\}$, $\{s, b\}$, $\{a, x\}$, $\{b, x\}$, $\{a, y\}$, $\{b, y\}$. The tree with the edges $\{s, a\}$, $\{s, b\}$, $\{a, x\}$, $\{b, y\}$ is a shortest path tree. It is not a BFS tree for any order of the lists: if BFS dequeues $a$ before $b$, then $a$ discovers both $x$ and $y$, and if it dequeues $b$ first, $b$ discovers both.

## Examples

Take the undirected graph with vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, with sorted lists, and the source 0. BFS gives

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\mathrm{dist}[v]$ | 0 | 1 | 1 | 2 | 2 | 3 | 4 | $\infty$ |
| $\pi[v]$ | NIL | 0 | 0 | 1 | 2 | 3 | 5 | NIL |

The tree has the 6 edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,4\}$, $\{3,5\}$, $\{5,6\}$ on the 7 reachable vertices, and vertex 7 is not in it. The path to 6 read from the parents is $6, 5, 3, 1, 0$, so the shortest path is $0, 1, 3, 5, 6$, with 4 edges. The non-tree edge $\{2, 3\}$ joins the layers 1 and 2, and $\{4, 5\}$ joins the layers 2 and 3.

**Another order.** If the list of 0 is $2, 1$ instead, BFS dequeues 2 before 1. Then 2 discovers 3 and 4, and the tree has the edge $\{2, 3\}$ in place of $\{1, 3\}$. The distances, and so the layers, are the same.

**Compared with DFS.** DFS from 0 on the same graph with sorted lists gives the tree path $0, 1, 3, 2, 4, 5, 6$, of depth 6. The BFS tree has depth 4, the eccentricity of 0.

## Where it is used

- **Shortest paths with unit lengths.** The tree stores a shortest path from $s$ to each reachable vertex, as in the [single-source shortest paths](/single-source-shortest-paths/) problem with all lengths equal to one. Mazes, grids and word ladders are classic cases.
- **Bipartiteness.** An edge inside a layer gives an odd cycle from the tree. See [bipartiteness checking](/bipartiteness-check/).
- **Girth.** A BFS tree from each vertex finds a shortest cycle through it, which gives the [girth](/girth/) of an undirected graph.
- **Several sources.** With all sources at depth 0, the result is a forest in which each vertex hangs below its nearest source. See [multi-source BFS](/multi-source-bfs/).
- **Distributed computing.** A BFS tree is a standard structure for broadcast and for collecting values in a network. See [distributed BFS](/breadth-first-search-distributed/).
- **Spanning trees.** On a connected undirected graph, the BFS tree is a [spanning tree](/spanning-tree/) of small depth.

## References
