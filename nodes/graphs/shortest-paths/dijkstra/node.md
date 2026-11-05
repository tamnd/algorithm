---
tag: 27XR9T
kind: algorithm
slug: dijkstra
name: Dijkstra's algorithm
aliases:
- Dijkstra's shortest path algorithm
area: graphs/shortest-paths
level: intro
summary: Greedily finalizes the closest unfinalized vertex using a priority queue; requires nonnegative weights.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [edge-relaxation, priority-queue, single-source-shortest-paths]
see_also: [dijkstra-correctness, bellman-ford, binary-heap, fibonacci-heap, dial-algorithm, bidirectional-dijkstra, a-star-search, breadth-first-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.3, Dijkstra's algorithm (the procedure, the correctness theorem and its analysis with a binary heap and a Fibonacci heap)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, Section 8.6 (best-first search, Dijkstra's algorithm, and its behavior with negative edges)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (Dijkstra's algorithm with an indexed priority queue)
  - paper: doi:10.1007/BF01386390
    title: Edsger W. Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1, 269 to 271 (1959)
    locator: Problem 2 (the shortest path between two nodes)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the application of Fibonacci heaps to the single-source shortest-path problem, time O(m + n log n)
  - paper: doi:10.1145/321992.321993
    title: Donald B. Johnson, Efficient algorithms for shortest paths in sparse networks, Journal of the ACM 24(1), 1 to 13 (1977)
    locator: the implementation of Dijkstra's algorithm with a heap for sparse graphs
---

Dijkstra's algorithm solves the [single-source shortest-path problem](/single-source-shortest-paths/) on a directed or undirected graph whose edge weights are all **nonnegative**. It keeps a set of *done* vertices whose distance is final, and at each step it makes the closest vertex that is not done into a done vertex, then [relaxes](/edge-relaxation/) the edges out of it. With a [binary heap](/binary-heap/) it runs in $O((n + m) \log n)$ time, and with a [Fibonacci heap](/fibonacci-heap/) in $O(m + n \log n)$. It is the standard algorithm for road maps, network routing and every other shortest-path task where no weight is negative.

## In plain words

Think of water that flows out from the start along the roads, at the same speed everywhere. The water reaches the towns one at a time, in the order of their distance. The first time it reaches a town, it came by a shortest way.

The algorithm copies this. For each town it keeps the best distance found so far. At each step it takes the town with the smallest known distance among the towns not yet reached. No other route can beat that distance: every other route must first pass a town that is at least as far away, and the roads still to come cannot make the trip shorter. It marks the town as reached and checks the roads that leave it. A road with a negative length breaks this reason, and then the answers can be wrong.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(u, v)$ for each edge, and a source $s$. The graph is directed; an undirected edge is two directed edges. The output is the distance $\delta(s, v)$ for each vertex $v$, and a predecessor $\pi[v]$ for each $v$ such that the edges $(\pi[v], v)$ form a [shortest-path tree](/shortest-path-tree/).

**Weight assumptions.** Each weight is a nonnegative real number: $w(u, v) \ge 0$. So there is no negative cycle, and each distance is a finite number or $+\infty$. The weights need not be integers; with integer weights all values stay integers. A vertex that $s$ cannot reach gets $\delta(s, v) = +\infty$ and no predecessor. With a negative weight the answer can be wrong, even with no negative cycle; for that case use the [Bellman-Ford algorithm](/bellman-ford/) or [Johnson's reweighting](/johnson/).

## The algorithm

The [priority queue](/priority-queue/) $Q$ holds pairs $(k, v)$ with key $k$. This version uses a plain binary heap and *lazy deletion*: when $d[v]$ goes down, it inserts a new pair and leaves the old pair in the heap. A pair whose vertex is already done is stale and is skipped when it comes out.

```pseudo id=main
DIJKSTRA(G, w, s)
L1  for each v in V do d[v] ← ∞, π[v] ← nil, done[v] ← false
L2  d[s] ← 0
L3  Q ← a min-heap that holds the pair (0, s)
L4  while Q is not empty do
L5      (k, u) ← EXTRACT-MIN(Q)
L6      if done[u] = false then                ▷ else the pair is stale
L7          done[u] ← true                     ▷ now d[u] = δ(s, u)
L8          for each edge (u, v) out of u do
L9              if d[u] + w(u, v) < d[v] then  ▷ RELAX(u, v, w)
L10                 d[v] ← d[u] + w(u, v), π[v] ← u
L11                 INSERT(Q, (d[v], v))
L12 return d, π
```

Lines L1 and L2 are the usual initialization: only the source has a finite estimate. Each pass of the loop takes the pair with the least key. If its vertex $u$ is not yet done, the key equals $d[u]$, and $d[u]$ is the least estimate of all vertices that are not done. Line L7 fixes $u$, and lines L8 to L11 relax each edge out of $u$. A vertex is done exactly once, so each edge is relaxed exactly once, at the moment its tail becomes done. The loop ends when the heap is empty; then each vertex that is not done is unreachable and keeps $d[v] = \infty$.

CLRS writes the same algorithm with a queue that supports DECREASE-KEY: all vertices start in $Q$, line L11 becomes DECREASE-KEY$(Q, v, d[v])$, and line L6 is not needed. The order in which vertices become done is the same, up to ties.

## Example

The graph has the vertices $s, a, b, c, d, t$ and the edges $s \to a$ (7), $s \to b$ (2), $b \to a$ (3), $b \to c$ (8), $a \to c$ (1), $a \to d$ (6), $c \to d$ (2), $c \to t$ (9), $d \to t$ (3). The table shows each pass of the loop that finds a vertex that is not done, the estimates after its relaxations (in the order $s, a, b, c, d, t$), and the heap after the pass.

| pass | done vertex, key | relaxations that change $d$ | $d$ after | heap after |
|---|---|---|---|---|
| 1 | $s$, 0 | $a = 7$, $b = 2$ | 0 7 2 ∞ ∞ ∞ | (2 b) (7 a) |
| 2 | $b$, 2 | $a = 5$, $c = 10$ | 0 5 2 10 ∞ ∞ | (5 a) (7 a) (10 c) |
| 3 | $a$, 5 | $c = 6$, $d = 11$ | 0 5 2 6 11 ∞ | (6 c) (7 a) (10 c) (11 d) |
| 4 | $c$, 6 | $d = 8$, $t = 15$ | 0 5 2 6 8 15 | (7 a) (8 d) (10 c) (11 d) (15 t) |
| | stale (7 a) | | | |
| 5 | $d$, 8 | $t = 11$ | 0 5 2 6 8 11 | (10 c) (11 d) (11 t) (15 t) |
| | stale (10 c), (11 d) | | | |
| 6 | $t$, 11 | none | 0 5 2 6 8 11 | (15 t) |
| | stale (15 t) | | | |

The distances are $\delta = (0, 5, 2, 6, 8, 11)$. The predecessors are $\pi[a] = b$, $\pi[b] = s$, $\pi[c] = a$, $\pi[d] = c$, $\pi[t] = d$, so the shortest path to $t$ is $s \to b \to a \to c \to d \to t$ with weight $2 + 3 + 1 + 2 + 3 = 11$. The vertices become done in the order of their distance: 0, 2, 5, 6, 8, 11.

**A negative edge.** Take $s \to a$ (2), $a \to c$ (1), $s \to b$ (4), $b \to a$ ($-3$). The algorithm makes $s$, then $a$ with $d[a] = 2$, then $c$ with $d[c] = 3$, then $b$ with $d[b] = 4$ done. The edge $b \to a$ then lowers $d[a]$ to 1, but $a$ is already done, so its edge to $c$ is not relaxed again. The output is $d[c] = 3$, but $\delta(s, c) = 4 - 3 + 1 = 2$. The graph has no cycle at all, so the failure comes from the negative edge alone.

## Correctness

**Theorem.** If $w(u, v) \ge 0$ for each edge, then DIJKSTRA ends, and at the end $d[v] = \delta(s, v)$ for each $v$, and the edges $(\pi[v], v)$ with $d[v] < \infty$ and $v \ne s$ form a shortest-path tree of the vertices reachable from $s$.

The proof is a [loop invariant](/loop-invariant/) of line L4, with $S$ the set of done vertices:

1. $d[v] = \delta(s, v)$ for each $v \in S$;
2. for each $v \notin S$, $d[v]$ is the least of the values $d[x] + w(x, v)$ over the edges $(x, v)$ with $x \in S$, and also $0$ when $v = s$; it is $\infty$ when there is no such value;
3. for each $v \notin S$ with $d[v] < \infty$, the heap holds the pair $(d[v], v)$, and each pair $(k, v)$ in the heap has $k \ge d[v]$.

Part 3 shows that a pair taken by line L5 for a vertex $u \notin S$ has key $d[u] = \min_{v \notin S} d[v]$. The main step shows that this $d[u]$ is $\delta(s, u)$. Take a shortest path from $s$ to $u$ and its first vertex $y \notin S$. By part 2, $d[y] \le \delta(s, y)$, and $\delta(s, y) \le \delta(s, u)$ **because the rest of the path has weight at least 0**. So $d[u] \le d[y] \le \delta(s, u)$, and the [upper-bound property](/upper-bound-property/) gives equality. This is the only place where the proof uses nonnegative weights. The full proof, with termination and the tree, is in the proof file below. The page [correctness of Dijkstra's algorithm](/dijkstra-correctness/) states the main step as a theorem on its own.

## Complexity

The model is the [word RAM](/word-ram/), where an addition or a comparison of two weights costs one step.

- **Relaxations.** Line L7 runs once for each vertex that $s$ reaches, so lines L8 to L11 run once for each edge out of such a vertex: at most $m$ relaxations in total.
- **Heap operations.** Line L3 inserts one pair and line L11 at most $m$ pairs. So the heap never holds more than $m + 1$ pairs, and line L5 runs at most $m + 1$ times. With a binary heap each operation costs $O(\log(m + 1))$.
- **Total.** The time is $O(n + m \log m)$. Without parallel edges $m \le n^2$, so $\log m \le 2 \log n$, and the time is $O(n + m \log n)$, which is within the bound $O((n + m) \log n)$ of the front matter. With parallel edges, keep only the lightest edge of each pair first.
- **Space.** The arrays take $O(n)$ and the heap up to $m + 1$ pairs, so the extra space is $O(n + m)$. The DECREASE-KEY version keeps at most $n$ items in the queue, so its extra space is $\Theta(n)$.

Other queues change the bound. The array of Dijkstra's paper gives $O(n^2)$, which is best for dense graphs. A $d$-ary heap with $d = \max(2, \lceil m/n \rceil)$ gives $O(m \log_{2 + m/n} n)$. A [Fibonacci heap](/fibonacci-heap/), with $O(1)$ amortized DECREASE-KEY, gives $O(m + n \log n)$ (Fredman and Tarjan, 1987). With integer weights at most $C$, [Dial's algorithm](/dial-algorithm/) gives $O(m + nC)$, and a [radix heap](/radix-heap/) gives $O(m + n \log C)$.

**Lower bound for this method.** The algorithm makes the vertices done in increasing order of distance. On a star with $n - 1$ edges out of $s$, this order sorts the $n - 1$ weights. So in the [comparison model](/comparison-model/), any implementation that outputs this order needs $\Omega(n \log n)$ comparisons in the worst case, and $O(m + n \log n)$ is optimal for it. Algorithms that do not produce the sorted order can beat this bound; see the [sorting barrier](/sorting-barrier/).

## Properties

- **Label-setting.** Each vertex becomes done once and its estimate never changes after that. [Bellman-Ford](/bellman-ford/) is label-correcting: an estimate can change many times.
- **Greedy.** Each step makes a locally best choice that is never undone; it is a [greedy algorithm](/greedy-algorithm/).
- **Monotone keys.** With nonnegative weights the keys taken by line L5 never decrease. This is why a [bucket queue](/bucket-queue/) or a [radix heap](/radix-heap/), which need monotone keys, can replace the heap.
- **Early stop.** If only the distance to one target $t$ is needed, stop when $t$ becomes done. The [single-pair problem](/single-pair-shortest-path/) is solved this way, and [bidirectional Dijkstra](/bidirectional-dijkstra/) and [A* search](/a-star-search/) go further.
- **Unweighted case.** With all weights equal to 1, the order of done vertices is the order of [breadth-first search](/breadth-first-search/), and a FIFO queue can replace the heap.

## Variants and improvements

- **Decrease-key version.** The CLRS form with an [indexed priority queue](/indexed-priority-queue/) and [decrease-key](/decrease-key/); $\Theta(n)$ extra space.
- **Fibonacci or pairing heaps.** $O(m + n \log n)$ in theory with a [Fibonacci heap](/fibonacci-heap/); a [pairing heap](/pairing-heap/) is often faster in practice.
- **[Dial's algorithm](/dial-algorithm/).** A bucket queue for small integer weights.
- **[Bidirectional Dijkstra](/bidirectional-dijkstra/).** Search from $s$ and from $t$ at the same time for one pair.
- **[A* search](/a-star-search/).** Add a lower bound on the rest of the distance to the key; with a [consistent heuristic](/consistent-heuristic/) it is Dijkstra's algorithm on reduced weights.
- **[Johnson's algorithm](/johnson/).** Reweight with a potential from Bellman-Ford so that all weights become nonnegative, then run Dijkstra from each source.
- **Undirected integer weights.** [Thorup's algorithm](/thorup-undirected-sssp/) runs in $O(m)$ time on the word RAM by not visiting vertices in sorted order.

## When to use it

Use Dijkstra's algorithm when all weights are nonnegative. It is the fastest simple method for one source on general graphs. For unweighted graphs, [breadth-first search](/breadth-first-search/) is simpler and takes $O(n + m)$. For weights in $\{0, 1\}$, use [0-1 BFS](/zero-one-bfs/). For a DAG, [DAG shortest paths](/dag-shortest-paths/) takes $O(n + m)$ and allows negative weights. With negative weights on a general graph, use [Bellman-Ford](/bellman-ford/). For many queries on a fixed road network, preprocess with [contraction hierarchies](/contraction-hierarchies/).

## Pitfalls

- **Negative weights.** Line L6 never makes a done vertex active again, so a later negative edge into it is lost, as the example shows. Check the weights first and use Bellman-Ford when one is negative. A version that drops line L6 and reprocesses a vertex each time its estimate falls is correct with negative edges and no negative cycle, but it can take exponential time.
- **Not skipping stale pairs.** Without the test of line L6, the lazy heap scans the edges out of a vertex once for each of its pairs, and a vertex can have one pair for each edge into it. The answer stays right, but the time can grow to $\Theta(nm)$ on dense inputs. Keep the test, or compare $k$ with $d[u]$.
- **Marking done at insertion.** Setting done$[v]$ when $v$ enters the heap, as in BFS, is wrong: a later, shorter path to $v$ is then ignored. Set it in line L7, when the pair comes out.
- **Overflow with infinity.** If $\infty$ is stored as the largest integer, $d[u] + w$ overflows. Line L9 only runs for done vertices, whose $d[u]$ is finite, so the code is safe as written; it is not safe if you relax from a vertex with $d[u] = \infty$.
- **Stopping at the first sight of the target.** For one pair, stop when $t$ is taken from the heap, not when $d[t]$ first becomes finite.

## Implementations

The Python version follows the lazy-deletion pseudocode with `heapq`, which has no decrease-key. It raises an error on a negative weight, because the result would be wrong.

## History

Edsger W. Dijkstra published the algorithm in 1959, in a three-page note that also gave a method for the minimum spanning tree. His version keeps the estimates in an array and takes $O(n^2)$ time. Donald B. Johnson used a heap for sparse graphs in 1977. Michael Fredman and Robert Tarjan invented the Fibonacci heap and gave the $O(m + n \log n)$ bound in 1987.

## References
