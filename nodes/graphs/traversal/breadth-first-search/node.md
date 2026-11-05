---
tag: HAEH1M
kind: algorithm
slug: breadth-first-search
name: Breadth-first search
aliases:
- BFS
area: graphs/traversal
level: intro
summary: Explores vertices in layers of increasing distance from the source using a FIFO queue.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [graph-traversal, queue, adjacency-list]
see_also: [depth-first-search, bfs-layers, bfs-tree, multi-source-bfs, zero-one-bfs, dijkstra, bipartiteness-check, whatever-first-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (the procedure BFS, the lemmas on the queue and the theorem on the correctness of the distances), and the chapter notes of Chapter 20
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.2, Graph connectivity and graph traversal, and Section 3.3, Implementing graph traversal using queues and stacks
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (the subsection Breadth-first search and the class BreadthFirstPaths)
  - paper: "Edward F. Moore, The shortest path through a maze, Proceedings of an International Symposium on the Theory of Switching, Part II, Harvard University Press (1959)"
    locator: the whole paper (the maze algorithms that number the cells by their distance from the start)
---

Breadth-first search (BFS) visits the vertices of a [graph](/graph/) in order of their distance from a source vertex $s$: first $s$, then the neighbours of $s$, then the vertices two edges away, and so on. It keeps the discovered vertices that it has not yet scanned in a first-in first-out [queue](/queue/). On a graph with $n$ vertices and $m$ edges, stored as an [adjacency list](/adjacency-list/), it runs in $\Theta(n + m)$ time. It solves [graph reachability](/graph-reachability/), and it computes the least number of edges from $s$ to each vertex, so it is the shortest-path algorithm for graphs without weights.

## In plain words

Drop a stone in still water. The ripple reaches the near points first and the far points later. Breadth-first search moves through a graph the same way.

You start at one vertex. You write down each neighbour of it, in a waiting line. Then you take the first vertex of the line, and you add to the end of the line each of its neighbours that you have not seen before. You repeat this until the line is empty.

Because the line is first in, first out, all vertices one step away leave the line before any vertex two steps away, and so on. So when you first see a vertex, you have found a way to it with the fewest possible steps. If you also write down from which vertex you saw it, you can walk back along these notes to get the route.

## The problem

The input is a graph $G = (V, E)$, directed or undirected, with $V = \{0, 1, \ldots, n-1\}$, given by adjacency lists $\mathrm{Adj}[u]$, and a source vertex $s \in V$. An undirected edge $\{u, v\}$ is in both lists. Let $\delta(s, v)$ be the least number of edges on a path from $s$ to $v$, or $\infty$ if there is no path.

The output is, for each vertex $v$, the value $\mathrm{dist}[v] = \delta(s, v)$, and a parent $\pi[v]$ such that the parent pointers give a shortest path from $s$ to each reachable vertex. The parent pointers form the [breadth-first tree](/bfs-tree/), and the sets of vertices with equal distance are the [BFS layers](/bfs-layers/). The set of vertices with finite $\mathrm{dist}$ is the answer to [graph reachability](/graph-reachability/).

## The algorithm

```pseudo id=main
BFS(G, s)
L1  for each vertex u ∈ V do dist[u] ← ∞, π[u] ← NIL
L2  dist[s] ← 0
L3  Q ← an empty queue; ENQUEUE(Q, s)
L4  while Q is not empty do
L5      u ← DEQUEUE(Q)
L6      for each v ∈ Adj[u] do
L7          if dist[v] = ∞ then                ▷ v is seen for the first time
L8              dist[v] ← dist[u] + 1
L9              π[v] ← u
L10             ENQUEUE(Q, v)
L11 return dist, π
```

A vertex is *discovered* when it gets a finite distance, at line L2 or line L8. It is *scanned* when it leaves the queue at line L5 and line L6 runs through its list. The test of line L7 makes sure that each vertex enters the queue at most one time. CLRS writes the same test with three colours: a white vertex is not yet discovered, a gray vertex is in the queue, and a black vertex is scanned. The value $\mathrm{dist}[v] = \infty$ carries the same information as "white", so this version needs no colours.

The queue is the only thing that makes this search breadth-first. With a [stack](/stack/) in its place, the same loop does a kind of depth-first search, as the page on [whatever-first search](/whatever-first-search/) explains.

## Example

The undirected graph has the vertices 0 to 7 and the 8 edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$. Vertex 7 has no edge. The adjacency lists are in increasing order, and $s = 0$.

| step | scanned $u$ | newly discovered | queue after the step | dist of $0, 1, \ldots, 7$ |
|---|---|---|---|---|
| start | | 0 | 0 | 0 ∞ ∞ ∞ ∞ ∞ ∞ ∞ |
| 1 | 0 | 1, 2 | 1 2 | 0 1 1 ∞ ∞ ∞ ∞ ∞ |
| 2 | 1 | 3 | 2 3 | 0 1 1 2 ∞ ∞ ∞ ∞ |
| 3 | 2 | 4 | 3 4 | 0 1 1 2 2 ∞ ∞ ∞ |
| 4 | 3 | 5 | 4 5 | 0 1 1 2 2 3 ∞ ∞ |
| 5 | 4 | none | 5 | 0 1 1 2 2 3 ∞ ∞ |
| 6 | 5 | 6 | 6 | 0 1 1 2 2 3 4 ∞ |
| 7 | 6 | none | empty | 0 1 1 2 2 3 4 ∞ |

In step 3, vertex 2 sees vertex 3 again, but $\mathrm{dist}[3] = 2$ is already finite, so line L7 skips it. The parents are $\pi[1] = \pi[2] = 0$, $\pi[3] = 1$, $\pi[4] = 2$, $\pi[5] = 3$ and $\pi[6] = 5$. The path back from 6 is $6, 5, 3, 1, 0$, with 4 edges. Vertex 7 keeps $\mathrm{dist}[7] = \infty$: it is not reachable from 0. The layers are $\{0\}$, $\{1, 2\}$, $\{3, 4\}$, $\{5\}$ and $\{6\}$.

## Correctness

**Theorem.** When BFS$(G, s)$ stops, $\mathrm{dist}[v] = \delta(s, v)$ for each vertex $v$. For each reachable $v \ne s$, $(\pi[v], v)$ is an edge and $\delta(s, \pi[v]) = \delta(s, v) - 1$, so the parent pointers from $v$ lead back to $s$ along a shortest path.

The proof has three steps. First, $\mathrm{dist}[v] \ge \delta(s, v)$ at all times, because line L8 sets $\mathrm{dist}[v]$ to the length of a real walk. Second, the distances in the queue are sorted and differ by at most 1 from the front to the back. This is the invariant that the first-in first-out rule gives. Third, take a vertex $v$ with a wrong final distance and the least $\delta(s, v)$, and let $u$ be the vertex before $v$ on a shortest path. When BFS scans $u$, it either discovers $v$ with the right distance, or $v$ was discovered earlier with a distance of at most $\mathrm{dist}[u] + 1$. Both cases contradict the choice of $v$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- **Initialization.** Line L1 takes $\Theta(n)$ time.
- **Queue operations.** A vertex enters the queue only when its distance changes from $\infty$ to a finite value, and this happens at most one time. So there are at most $n$ calls of ENQUEUE and of DEQUEUE, each $O(1)$.
- **Scanning.** Line L6 runs through $\mathrm{Adj}[u]$ only when $u$ is dequeued, so at most one time for each $u$. The total length of the lists is $m$ for a directed graph and $2m$ for an undirected graph. So lines L6 to L10 take $O(m)$ time in total.

The time is $O(n + m)$. It is $\Theta(n + m)$ in the worst case, for example when the graph is connected, because then each list is scanned. The best case is $\Theta(n)$, when $s$ has no edge: only line L1 does real work. If the arrays come already filled from an earlier run, or a hash map holds only the discovered vertices, the time is $O(n_s + m_s)$, where $n_s$ and $m_s$ count the vertices and edges reachable from $s$. The extra space is $\Theta(n)$ for $\mathrm{dist}$, $\pi$ and the queue.

With an [adjacency matrix](/adjacency-matrix/), line L6 must look at a full row of $n$ entries for each scanned vertex, and the time is $\Theta(n^2)$ when all vertices are reachable.

## Properties

- **Deterministic.** The output depends only on the graph and the order of the adjacency lists. A different order of the lists can give a different tree, but never different distances.
- **Not recursive.** The queue replaces the call stack, so the depth of a long path does not matter.
- **Layered.** The vertices leave the queue in non-decreasing order of distance. All vertices at distance $k$ leave before any vertex at distance $k + 1$.
- **Directed or undirected.** The same code works for both. In an undirected graph, each edge that is not a tree edge joins two vertices whose distances differ by at most 1.

## Variants and improvements

- **Full BFS.** Run BFS from each vertex that is still undiscovered, without the reset of line L1. This visits all vertices in $\Theta(n + m)$ time and finds the [connected components](/connected-components/) of an undirected graph.
- **Multi-source BFS.** Put several sources in the queue at the start, each with distance 0. This gives the distance to the nearest source. See [multi-source BFS](/multi-source-bfs/).
- **0-1 BFS.** If each edge has weight 0 or 1, a [deque](/deque/) gives shortest paths in $O(n + m)$ time: a vertex reached by an edge of weight 0 goes to the front. See [0-1 BFS](/zero-one-bfs/).
- **Bidirectional BFS.** Search from $s$ and from the target at the same time, and stop when the two searches meet. See [bidirectional search](/bidirectional-search/).
- **Direction-optimizing BFS.** When the frontier is large, let each undiscovered vertex look for a parent in the frontier, instead of the reverse. See [direction-optimizing BFS](/direction-optimizing-bfs/) and [parallel BFS](/parallel-bfs/).
- **Weighted graphs.** With positive weights, replace the queue by a [priority queue](/priority-queue/) keyed by distance. This is [Dijkstra's algorithm](/dijkstra/).
- **Trees.** On a rooted tree, BFS is the [level-order traversal](/level-order-traversal/).
- **Lexicographic BFS.** A BFS that breaks ties among vertices by the order of their earlier neighbours. See [lexicographic BFS](/lexicographic-bfs/).

## When to use it

Use BFS when you need the least number of edges from one vertex to the others, for example the fewest moves in a puzzle or the fewest hops in a network. Use it to test whether a graph is bipartite (see [bipartiteness checking](/bipartiteness-check/)). For plain reachability, BFS and [depth-first search](/depth-first-search/) have the same cost, and the choice depends on what else you need: DFS gives discovery and finish times, edge types and a [topological sort](/topological-sort/), and BFS gives distances. BFS keeps a whole layer in memory, which can be large in a wide graph. [Iterative deepening](/iterative-deepening-search/) finds the same shortest paths in a large implicit tree with memory linear in the depth.

## Pitfalls

- **Marking when the vertex leaves the queue.** If line L7 tests a "scanned" flag that is set at line L5, a vertex can enter the queue many times, and the queue can grow to $\Theta(m)$ items. Mark the vertex when it is discovered, at line L8, as the pseudocode does.
- **A stack by mistake.** A list used with `pop()` in Python removes the last item, not the first. The result is not a BFS and the distances are wrong. Use a real queue, such as `collections.deque` with `popleft()`.
- **A slow queue.** Removing the first item of an array list shifts all other items and costs $\Theta(n)$ time. Use a ring buffer, a linked queue or a head index.
- **Weighted edges.** BFS counts edges, not weights. On a weighted graph the first path found is not always the shortest.
- **Forgotten source.** Line L2 must set $\mathrm{dist}[s] = 0$ before the loop. Else a self-loop or a cycle back to $s$ makes the search discover $s$ again.

## Implementations

## History

Edward F. Moore described BFS in 1959 as a method to find a shortest path through a maze. C. Y. Lee found the same method on his own in 1961, to route wires on circuit boards. CLRS gives both in the chapter notes of Chapter 20. The proof of correctness through the ordered queue is the one of CLRS, Section 20.2.

## References
