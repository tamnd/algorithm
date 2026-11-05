---
tag: 6NDZ9M
kind: algorithm
slug: prim
name: Prim's algorithm
aliases:
- Jarník's algorithm
- Prim-Jarník algorithm
- DJP algorithm
area: graphs/spanning-trees
level: intro
summary: Grow a tree from one vertex by repeatedly adding the cheapest edge leaving it.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log m), best: Ω(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1930
  people: [Vojtěch Jarník, Robert C. Prim, Edsger W. Dijkstra]
  note: Jarník published the method in Czech in 1930. Prim found it again in 1957 and Dijkstra in 1959.
prereqs: [minimum-spanning-tree, cut-property, priority-queue, binary-heap, adjacency-list]
see_also: [kruskal, boruvka, dijkstra, generic-mst-method, safe-edge, fibonacci-heap, decrease-key, reverse-delete]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.2 (the algorithms of Kruskal and Prim), with the analysis for binary and Fibonacci heaps
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (the lazy and the eager versions of Prim's algorithm)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (Section 7.4, Jarník's ("Prim's") algorithm)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The minimum spanning tree problem (Prim's algorithm and its proof by the cut property)
  - paper: doi:10.1002/j.1538-7305.1957.tb01515.x
    title: Robert C. Prim, Shortest connection networks and some generalizations, Bell System Technical Journal 36(6) (1957), 1389-1401
    locator: the whole paper
  - paper: doi:10.1007/BF01386390
    title: Edsger W. Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1 (1959), 269-271
    locator: Problem 1, the tree of minimum total length
  - paper: doi:10.1109/MAHC.1985.10011
    title: Ronald L. Graham and Pavol Hell, On the history of the minimum spanning tree problem, Annals of the History of Computing 7(1) (1985), 43-57
    locator: the sections on Jarník and on the rediscoveries by Prim and Dijkstra
---

Prim's algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) of a connected, undirected, [weighted graph](/weighted-graph/) by growing one tree from a start vertex: at each step it adds the lightest edge that joins the tree to a vertex outside it. With a [binary heap](/binary-heap/) as the [priority queue](/priority-queue/) it runs in $O((n + m) \log m)$ time, which is $O(m \log n)$ for a connected simple graph, and with a [Fibonacci heap](/fibonacci-heap/) in $O(m + n \log n)$. Each added edge is a lightest edge across a cut, so the [cut property](/cut-property/) proves it correct. The method has the same shape as [Dijkstra's algorithm](/dijkstra/), with the weight of one edge as the key in place of the length of a path.

## In plain words

Start at any town. It is your network, with no roads yet. Look at every road that leads from a town in your network to a town outside it, and build the cheapest one. Now the network has one more town. Repeat until every town is in.

To find the cheapest road quickly, each town outside the network keeps one number: the price of its cheapest road into the network so far. When a town joins, look at its roads and lower the numbers of its neighbours if a road is cheaper. A priority queue then gives the outside town with the smallest number.

If the map is in several pieces, the tree stops growing when it has the whole piece. Start a new tree in a town that is still outside, and you get the cheapest set of roads for every piece.

## The problem

The input is an undirected graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges, given as [adjacency lists](/adjacency-list/), and a weight $w(e)$ on each edge, a real number or an integer. Weights may be negative and may tie. Parallel edges and [self-loops](/self-loop/) are allowed.

The output is a minimum spanning forest: a [spanning forest](/spanning-forest/) of $G$ of least total weight. If $G$ is [connected](/connected-graph/), this is a minimum spanning tree with $n - 1$ edges. The textbook version grows only one tree from a root $r$ and needs $G$ to be connected. The version below restarts from each vertex that is not yet in a tree, so it also handles a graph that is not connected. When weights tie, more than one minimum tree can exist, and the algorithm returns one of them.

## The algorithm

Each vertex $v$ has a key $key[v]$, the weight of the lightest edge known from the current tree to $v$, and the edge $\pi[v]$ that gives this weight. $Q$ is a min-priority queue of pairs $(k, v)$ ordered by $k$. This version does not use [DECREASE-KEY](/decrease-key/). When a key drops, it inserts a new pair and leaves the old pair in $Q$. An old pair is *stale*, and line L7 skips it.

```pseudo id=main
PRIM(G, w)
L1  for each v ∈ V do key[v] ← ∞, π[v] ← nil, inTree[v] ← false
L2  for each r ∈ V do                                  ▷ one tree for each component
L3      if not inTree[r] then
L4          key[r] ← 0, Q ← {(0, r)}
L5          while Q ≠ ∅ do
L6              (k, u) ← EXTRACT-MIN(Q)
L7              if inTree[u] then go to the next iteration of line L5   ▷ a stale pair
L8              inTree[u] ← true                           ▷ u joins the tree by the edge π[u]
L9              for each edge e = (u, v) of G do
L10                 if not inTree[v] and w(e) < key[v] then
L11                     key[v] ← w(e), π[v] ← e
L12                     INSERT(Q, (key[v], v))
L13 return {π[v] : v ∈ V and π[v] ≠ nil}
```

Line L4 starts a new tree at a vertex $r$ that no earlier tree reached. Lines L6 to L8 take the outside vertex $u$ with the smallest key and put it in the tree. Its key is then the weight of $\pi[u]$, a lightest edge between the tree and the rest of the graph. Lines L9 to L12 look at the edges of $u$ and lower the key of each outside neighbour when the new edge is lighter. The test of $inTree[v]$ in line L10 keeps the vertices of the tree fixed: their edge $\pi$ never changes after they join. A self-loop $(u, u)$ fails this test, because $u$ is already in the tree.

The edge $\pi[v]$ is stored as an edge, not as the other end. With parallel edges, the other end does not say which edge was used.

## Example

The graph has the vertices $a$ to $f$ and nine edges. Two pairs of weights tie. The tree grows from $a$.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

The table shows each pair taken from $Q$ in line L6, and the keys of the outside vertices after the step. A dash is a vertex in the tree.

| step | pair taken | action | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | tree weight |
|---|---|---|---|---|---|---|---|---|---|
| 0 | | start at $a$ | 0 | ∞ | ∞ | ∞ | ∞ | ∞ | 0 |
| 1 | $(0, a)$ | add $a$ | - | 4 | 3 | ∞ | ∞ | ∞ | 0 |
| 2 | $(3, c)$ | add $c$ by $ac$ | - | 1 | - | 4 | 5 | ∞ | 3 |
| 3 | $(1, b)$ | add $b$ by $bc$ | - | - | - | 2 | 5 | ∞ | 4 |
| 4 | $(2, d)$ | add $d$ by $bd$ | - | - | - | - | 5 | 6 | 6 |
| 5 | $(4, b)$ | stale, skip | - | - | - | - | 5 | 6 | 6 |
| 6 | $(4, d)$ | stale, skip | - | - | - | - | 5 | 6 | 6 |
| 7 | $(5, e)$ | add $e$ by $ce$ | - | - | - | - | - | 2 | 11 |
| 8 | $(2, f)$ | add $f$ by $ef$ | - | - | - | - | - | - | 13 |
| 9 | $(6, f)$ | stale, skip | - | - | - | - | - | - | 13 |

In step 2, the edge $bc$ of weight 1 lowers the key of $b$ from 4 to 1, and the pair $(4, b)$ stays in $Q$ as a stale pair. In step 4, the edge $de$ of weight 7 does not lower the key 5 of $e$. The tree is $\{ac, bc, bd, ce, ef\}$ with weight 13. It is the same tree that [Kruskal's algorithm](/kruskal/) finds, in a different order, and it is the only MST of this graph.

## Correctness

**Theorem.** For each finite undirected graph with real edge weights, PRIM returns a minimum spanning forest. Ties, negative weights, parallel edges, self-loops and disconnected graphs are allowed.

The key invariant holds before each run of line L6. Let $S$ be the set of vertices in the tree that is growing now. Then (a) for each vertex $v$ outside all trees, $key[v]$ is the least weight of an edge from $S$ to $v$, or $\infty$ if there is none, and $\pi[v]$ is such an edge; (b) $Q$ holds the pair $(key[v], v)$ for each such $v$ with a finite key, and each pair $(k, v)$ in $Q$ has $k \ge key[v]$; (c) the edges $\pi[x]$ of all vertices in trees are a subset of some minimum spanning forest. By (a) and (b), the pair taken in line L6 with an outside vertex $u$ has $k = key[u]$, and $\pi[u]$ is a lightest edge with exactly one end in $S$. The cut property then keeps (c) true. When $Q$ is empty, no edge leaves $S$, so $S$ is a whole component. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with a comparison of two weights in $O(1)$ time. $Q$ is a binary heap.

- **Line L1** takes $O(n)$ time, and building the adjacency lists takes $O(n + m)$.
- **Line L8** runs once for each vertex, and the loop of line L9 then scans the edges of that vertex once. So lines L9 to L11 run $O(m)$ times in total: once for each end of each edge.
- **Line L12** runs at most once for each edge. When an edge $(u, v)$ is scanned from $u$, line L12 inserts a pair only if $v$ is outside the tree. Then $v$ joins later, and when the edge is scanned from $v$, its end $u$ is in the tree. So $Q$ receives at most $n$ pairs from line L4 and at most $m$ from line L12.
- **Line L6** runs once for each pair inserted, so at most $n + m$ times. Each heap operation on at most $n + m$ pairs costs $O(\log(n + m))$, which is $O(\log m)$ when $m \ge n$ and $O(\log n)$ otherwise.

So the time is $O((n + m) \log m)$ in the worst case (read $\log m$ as $\log \max(m, 2)$). For a connected simple graph, $n - 1 \le m < n^2$, so this is $O(m \log n)$. Each edge is scanned on every input, so the time is $\Omega(n + m)$ in the best case. The extra space is $O(n)$ for the arrays and $O(n + m)$ for the heap and the adjacency lists.

| claim | bound | case |
|---|---|---|
| time | $O((n + m) \log m)$, which is $O(m \log n)$ for a connected simple graph | worst |
| time | $\Omega(n + m)$ | best |
| extra space | $O(n + m)$ | worst |

**Other queues.** With a heap that has DECREASE-KEY, $Q$ holds at most $n$ vertices. Then there are $n$ EXTRACT-MIN and at most $m$ DECREASE-KEY calls. A binary heap gives $O(m \log n)$, a [Fibonacci heap](/fibonacci-heap/) gives $O(m + n \log n)$ because DECREASE-KEY costs $O(1)$ amortized, and a [d-ary heap](/d-ary-heap/) with $d = \max(2, \lceil m/n \rceil)$ gives $O(m \log_{d} n)$. With no heap at all, an array of keys and a linear scan for the minimum take $O(n^2)$ time, which is optimal for a dense graph given as an [adjacency matrix](/adjacency-matrix/).

## Properties

- **Deterministic.** The order of the vertices and of the adjacency lists fixes the output.
- **One tree at a time.** At each moment the edges chosen in the current component form one connected tree. Kruskal's algorithm instead keeps a forest of many small trees.
- **Only the order of the weights matters.** Lines L10 and L6 compare weights and never add them. So negative weights need no special case, and a strictly increasing map of the weights gives the same tree.
- **Greedy.** Each edge is chosen once and never removed. After $k$ vertices have joined the tree of a component, the $k - 1$ chosen edges are part of a minimum spanning tree of that component.

## Variants and improvements

- **Eager Prim with DECREASE-KEY.** Keep at most one pair per vertex in an indexed heap and lower its key in place. This is the version of CLRS, Section 21.2, and of the "eager" version of Sedgewick and Wayne.
- **Array version for dense graphs.** Replace $Q$ by a scan of the keys. This is Jarník's and Dijkstra's original form, and it runs in $O(n^2)$ time.
- **Fibonacci heap.** $O(m + n \log n)$, which is linear when $m = \Omega(n \log n)$. Fredman and Tarjan used this in their faster [MST algorithm](/fredman-tarjan-mst/), which stops each tree early when its heap grows too large.
- **Maximum spanning tree.** Use a max-priority queue and the test $w(e) > key[v]$ with keys that start at $-\infty$. This gives a [maximum spanning tree](/maximum-spanning-tree/).
- **Geometric input.** For $n$ points with Euclidean distances, the array version on the complete graph takes $O(n^2)$ time and $O(n)$ space, with no list of the $\binom{n}{2}$ edges.

## When to use it

Use Prim's algorithm when the graph is dense or given as an adjacency matrix, where the array version runs in $O(n^2)$ with no heap and no sort, or when you have adjacency lists and a heap at hand. It grows one tree, so it fits problems that need the tree around one vertex, and it does not need the edges in a list. Use [Kruskal's algorithm](/kruskal/) when the graph comes as an edge list, or when the edges are already sorted. Use [Borůvka's algorithm](/boruvka/) for a parallel or distributed setting, because its steps work on all components at once.

## Pitfalls

- **Dijkstra's key.** Writing $key[v] \leftarrow key[u] + w(e)$ in line L11, and the same sum in line L10, gives a [shortest-path tree](/shortest-path-tree/) from the start vertex, not an MST. The right line is $key[v] \leftarrow w(e)$. The test with the triangle of weights 2, 2 and 3 catches it: the shortest-path tree from vertex 0 uses the edge of weight 3, and the MST does not.
- **No in-tree test in line L10.** Without `not inTree[v]`, a tree vertex can get a new edge $\pi[v]$, and the output loses a tree edge or holds an edge twice. The test with the triangle of weights 1, 1 and $-1$ catches it.
- **No stale test in line L7.** Without it, the output is still right, because a second scan of $u$ lowers no key. But each stale pair of $u$ makes the loop of line L9 scan the $\deg(u)$ edges of $u$ again. A vertex has at most $\deg(u)$ stale pairs, so the extra work is up to $\sum_u \deg(u)^2$ steps, which is $\Theta(n^3)$ on a complete graph, instead of $O(m)$.
- **Only one start vertex.** The textbook loop grows one tree from $r$. On a graph that is not connected it returns the tree of one component, which is not a spanning forest. The loop of line L2 fixes this; the disconnected test checks it.
- **Storing the parent vertex.** With parallel edges, $\pi[v] \leftarrow u$ loses the weight that was used. Store the edge, as line L11 does. The parallel-edge test checks that the lighter edge is chosen.

## Implementations

## History

Vojtěch Jarník described the method in 1930, in a Czech paper written as a reply to Borůvka's work of 1926. Robert Prim published it again in 1957 in the Bell System Technical Journal, and Edsger Dijkstra in 1959 in the same short paper as his shortest-path algorithm. Graham and Hell trace this history in their survey of 1985. The names "Prim's algorithm", "Jarník's algorithm" and "DJP algorithm" all refer to it. The Fibonacci heap bound of $O(m + n \log n)$ is from Fredman and Tarjan (1987).

## References
