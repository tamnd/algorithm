---
tag: 7NTSGR
kind: concept
slug: shortest-path-tree
name: Shortest-path tree
aliases:
- single-source shortest-path tree
- SPT
area: graphs/shortest-paths
level: intro
summary: A tree rooted at the source that contains one shortest path from the source to every reachable vertex.
prereqs: [shortest-path, shortest-path-optimal-substructure, tree, parent-pointer-tree]
see_also: [single-source-shortest-paths, bfs-tree, edge-relaxation, upper-bound-property, dijkstra, bellman-ford, minimum-spanning-tree, shortest-path-optimality-conditions]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction, the subsection Representing shortest paths (the predecessor subgraph and the definition of a shortest-paths tree), and Section 22.5 (the predecessor-subgraph property)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Section 8.1, Shortest Path Trees
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 4, Shortest paths, label-setting algorithms (the shortest path tree and the property that a tree of shortest paths exists)
---

A shortest-path tree for a source $s$ is a [rooted tree](/tree/) on the vertices reachable from $s$ in which the tree path from $s$ to each vertex $v$ is a [shortest path](/shortest-path/) from $s$ to $v$ in the graph. It exists exactly when no [negative cycle](/negative-cycle/) is reachable from $s$. It stores all $n - 1$ shortest paths from $s$ in $\Theta(n)$ space, as one [parent pointer](/parent-pointer-tree/) per vertex, and it is the output of every [single-source shortest-paths](/single-source-shortest-paths/) algorithm.

## In plain words

From one starting place, you want the best route to every other place. Writing down every route in full takes a lot of space, because many routes share their first parts. A shortest-path tree saves this space. For each place, it remembers only the place just before it on a best route. To read the route to a place, start there and follow the "came from" marks back to the start, then reverse the list.

This works because the first part of a best route is itself a best route, so the marks of all places fit together into one tree with the start at the root.

## The idea

Let $G = (V, E)$ be directed with weights $w : E \to \mathbb{R}$, let $s \in V$, and let $V_s$ be the set of vertices reachable from $s$. A *shortest-path tree rooted at* $s$ is a subgraph $T = (V_s, E_T)$ with $E_T \subseteq E$ such that

1. $T$ is a tree rooted at $s$: each $v \in V_s \setminus \{s\}$ has exactly one parent $\pi(v)$ with $(\pi(v), v) \in E_T$, and following parents from $v$ reaches $s$;
2. for each $v \in V_s$, the unique path from $s$ to $v$ in $T$ is a shortest path from $s$ to $v$ in $G$.

**Existence.** If no negative cycle is reachable from $s$, a shortest-path tree exists. *Proof.* All $\delta(s, v)$ with $v \in V_s$ are finite. For such $v$, let $k(v)$ be the least number of arcs of a shortest path from $s$ to $v$; $k(s) = 0$ by the empty path. For $v \ne s$, take a shortest path with $k(v)$ arcs, and let $u$ be the vertex before $v$ on it. By [optimal substructure](/shortest-path-optimal-substructure/), its prefix is a shortest path to $u$ with $k(v) - 1$ arcs, so $k(u) \le k(v) - 1$. The prefix cannot have fewer arcs, else adding $(u, v)$ would give a shortest path to $v$ with fewer than $k(v)$ arcs; so $k(u) = k(v) - 1$. Set $\pi(v) = u$. Then $\delta(s, v) = \delta(s, \pi(v)) + w(\pi(v), v)$ and $k$ drops by exactly 1 at each parent step, so following parents from $v$ reaches $s$ after $k(v)$ steps. Sum over the vertices $x \ne s$ of the tree path from $s$ to $v$: its weight is $\sum_x w(\pi(x), x) = \sum_x \big(\delta(s, x) - \delta(s, \pi(x))\big) = \delta(s, v) - \delta(s, s) = \delta(s, v)$, because the sum telescopes and $\delta(s, s) = 0$. $\square$

If a negative cycle is reachable from $s$, some vertex $v$ has $\delta(s, v) = -\infty$, and no path in any tree has weight $-\infty$, so no shortest-path tree exists.

**Tight arcs and the zero-cycle trap.** Call an arc $(u, v)$ *tight* when $\delta(s, u) + w(u, v) = \delta(s, v)$. Every arc of a shortest-path tree is tight, and every path of tight arcs from $s$ is a shortest path. But a choice of one tight arc into each vertex need not give a tree: a cycle of weight 0 can be all tight. The proof above avoids this by choosing the parent with the least arc count. Algorithms avoid it differently: [Dijkstra's algorithm](/dijkstra/) sets $\pi(v)$ only to a vertex finished earlier, and [Bellman-Ford](/bellman-ford/) sets $\pi(v)$ only on a strict decrease of $d(v)$, which is why the predecessor graph of a run of [relaxations](/edge-relaxation/) ends as a shortest-path tree (CLRS, predecessor-subgraph property).

**Size.** The tree has $|V_s| - 1$ arcs. Reading the path to $v$ from the parent array takes $O(k)$ time for a path of $k$ arcs. All-pairs shortest paths are stored as $n$ such trees, which is the *predecessor matrix* of [Floyd-Warshall](/floyd-warshall/).

## Examples

**A tree with negative arcs.** In the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), the distances from $s$ are $(0, 2, 4, 7, -2)$ for $(s, t, x, y, z)$. The tight arcs are $s \to y$, $y \to x$, $x \to t$, $t \to z$ and $z \to s$. They form the cycle $s \to y \to x \to t \to z \to s$ of weight 0. Since $s$ is the root, the arc $z \to s$ is dropped, and the tree is the single path $s \to y \to x \to t \to z$: $\pi(y) = s$, $\pi(x) = y$, $\pi(t) = x$, $\pi(z) = t$.

**The zero-cycle trap.** Take $s \to a$ (1), $a \to b$ (0) and $b \to a$ (0). Then $\delta(s, a) = \delta(s, b) = 1$, and all three arcs are tight. The choice $\pi(a) = b$, $\pi(b) = a$ uses only tight arcs, but it is a cycle that does not reach $s$. The least arc count gives $k(a) = 1$, $k(b) = 2$, so $\pi(a) = s$ and $\pi(b) = a$.

**Not unique.** On the square $s \to a$, $s \to b$, $a \to c$, $b \to c$ with all weights 1, $\delta(s, c) = 2$ and both $\pi(c) = a$ and $\pi(c) = b$ give a shortest-path tree. With unit weights a shortest-path tree is a [BFS tree](/bfs-tree/).

**Not a minimum spanning tree.** In the undirected triangle with $\{s, a\}$ and $\{s, b\}$ of weight 2 and $\{a, b\}$ of weight 1, the shortest-path tree from $s$ is $\{s, a\}, \{s, b\}$ with total weight 4. A [minimum spanning tree](/minimum-spanning-tree/) has total weight 3, for example $\{s, a\}, \{a, b\}$, but in it the distance from $s$ to $b$ is 3, not 2. The two trees minimize different things: the sum of the root-to-vertex distances against the sum of the edge weights.

**An unreachable vertex.** A vertex with no path from $s$ is not in the tree. Implementations keep $\pi(v) = \mathrm{nil}$ and $d(v) = \infty$ for it.

## Where it is used

- [Dijkstra's algorithm](/dijkstra/), [Bellman-Ford](/bellman-ford/), [DAG shortest paths](/dag-shortest-paths/) and [0-1 BFS](/zero-one-bfs/) return their paths as a parent array.
- The [upper-bound property](/upper-bound-property/) and the predecessor-subgraph property show that relaxation builds a shortest-path tree.
- [Johnson's algorithm](/johnson/) and [Floyd-Warshall](/floyd-warshall/) keep one tree per source.
- Routing protocols such as OSPF compute a shortest-path tree from each router to fill its table of next hops.
- [Yen's algorithm](/yen-k-shortest-paths/) and the [replacement paths](/replacement-paths/) problem start from the shortest-path tree and ask what changes when an arc is removed.

## References
