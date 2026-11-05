---
tag: 2PW2HK
kind: algorithm
slug: bellman-ford
name: Bellman-Ford algorithm
aliases:
- Ford-Bellman algorithm
- Bellman-Ford-Moore algorithm
area: graphs/shortest-paths
level: intro
summary: Relaxes all edges n-1 times; handles negative weights and detects negative cycles.
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [edge-relaxation, single-source-shortest-paths, negative-cycle]
see_also: [dijkstra, spfa, generic-shortest-path-algorithm, negative-cycle-detection, johnson, difference-constraints, currency-arbitrage, distance-vector-routing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.1, The Bellman-Ford algorithm (the procedure, its correctness lemma and theorem, and the exercises on early stopping and on finding a negative cycle)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, Section 8.7 (relax all the edges, Bellman-Ford, and its dynamic-programming view)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.8 (shortest paths in a graph with negative weights) and Section 6.10 (negative cycles in a graph)
  - paper: doi:10.1090/qam/102435
    title: Richard Bellman, On a routing problem, Quarterly of Applied Mathematics 16(1), 87 to 90 (1958)
    locator: the whole paper (the functional equation for the shortest route and its solution by successive approximation)
  - url: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    title: Wikipedia, Bellman-Ford algorithm
    locator: section History (Shimbel 1955, Ford 1956, Bellman 1958, Moore 1959)
---

The Bellman-Ford algorithm solves the [single-source shortest-path problem](/single-source-shortest-paths/) when edge weights may be **negative**, and it reports a [negative cycle](/negative-cycle/) that the source can reach. It [relaxes](/edge-relaxation/) every edge, in a fixed order, $n - 1$ times; then one more pass tells whether some edge can still be improved. It runs in $O(nm)$ time and $\Theta(n)$ extra space. It is slower than [Dijkstra's algorithm](/dijkstra/), but it is the base of [negative-cycle detection](/negative-cycle-detection/), [Johnson's algorithm](/johnson/), [difference constraints](/difference-constraints/) and distance-vector routing.

## In plain words

Each town keeps its best known cost from home. One round looks at every road once: if going to the start of the road and then along it is cheaper than the note at its end, the note is lowered.

After one round, every town whose best trip uses at most one road has the right cost. After two rounds, every town whose best trip uses at most two roads has it, and so on. A best trip never visits a town twice, so it uses fewer roads than there are towns. That many rounds are therefore enough, even when some roads have negative costs.

Then the algorithm does one more round. If some note still goes down, the costs never settle. That only happens when some loop of roads has a negative total, so the algorithm reports such a loop.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a real weight $w(u, v)$ on each edge, and a source $s$. If no cycle of negative weight is reachable from $s$, the output is $\delta(s, v)$ for each $v$, with a [shortest-path tree](/shortest-path-tree/). Otherwise the output is a cycle of negative weight that $s$ reaches.

**Weight assumptions.** Weights are any real numbers: negative weights are allowed. They need not be integers. Cycles of negative weight are allowed in the input; the algorithm detects the ones that $s$ can reach, and then it does not report distances, because some $\delta(s, v)$ is $-\infty$. A negative cycle that $s$ cannot reach does not change the distances and is not reported. A vertex that $s$ cannot reach gets $d[v] = \infty$. An undirected edge with a negative weight is a negative cycle of two edges, so on undirected graphs the algorithm is only useful for nonnegative weights.

## The algorithm

```pseudo id=main
BELLMAN-FORD(G, w, s)
L1  for each v in V do d[v] ← ∞, π[v] ← nil
L2  d[s] ← 0
L3  for i ← 1 to n − 1 do
L4      changed ← false
L5      for each edge (u, v) in E do
L6          if d[u] ≠ ∞ and d[u] + w(u, v) < d[v] then
L7              d[v] ← d[u] + w(u, v), π[v] ← u, changed ← true
L8      if changed = false then return d, π, nil      ▷ no edge is tense
L9  for each edge (u, v) in E do
L10     if d[u] ≠ ∞ and d[u] + w(u, v) < d[v] then
L11         relax (u, v); x ← v; repeat n times: x ← π[x]
L12         return d, π, the cycle π[x] → x, ..., back to x
L13 return d, π, nil
```

Lines L3 to L8 are the $n - 1$ passes. Each pass relaxes all edges in the same order. If a pass changes nothing, no edge is tense, so the estimates are final and no negative cycle is reachable; line L8 stops early. Lines L9 to L12 are the check pass. If an edge $(u, v)$ is still tense, line L11 relaxes it and walks $n$ steps back along the predecessors from $v$. The proof shows that this walk ends on a cycle of predecessor edges, and that each such cycle has negative weight. Line L12 collects that cycle by following $\pi$ from $x$ until it comes back to $x$.

The test $d[u] \ne \infty$ is needed when $\infty$ is stored as a large number, and it keeps an unreachable vertex from passing a false finite value along a negative edge.

## Example

The graph has the vertices $s, a, b, c, d$ and the edges, in this order of the passes: $c \to d$ (3), $b \to c$ ($-4$), $a \to b$ (2), $s \to a$ (3), $s \to b$ (6), $a \to d$ (4), $d \to b$ (1), $s \to c$ (5). The cycle $b \to c \to d \to b$ has weight $-4 + 3 + 1 = 0$, so there is no negative cycle. Here $n - 1 = 4$.

| pass | relaxations that change $d$, in order | $d$ for $s\,a\,b\,c\,d$ after the pass |
|---|---|---|
| start | | 0 ∞ ∞ ∞ ∞ |
| 1 | $a = 3$, $b = 6$, $d = 7$, $c = 5$ | 0 3 6 5 7 |
| 2 | $c = 2$, $b = 5$ | 0 3 5 2 7 |
| 3 | $d = 5$, $c = 1$ | 0 3 5 1 5 |
| 4 | $d = 4$ | 0 3 5 1 4 |
| check | no edge is tense | |

The answer is $\delta = (0, 3, 5, 1, 4)$, with the tree $s \to a \to b \to c \to d$. The shortest path to $d$ has 4 edges, and the edge order is bad for it, so all $n - 1 = 4$ passes are needed.

**With a negative cycle.** Add the edge $c \to a$ ($-2$) at the end of the order. Now the cycle $a \to b \to c \to a$ has weight $2 - 4 - 2 = -4$. The estimates after passes 1 to 4 are $(0, 3, 6, 5, 7)$, $(0, 0, 5, 2, 7)$, $(0, -1, 2, 1, 4)$ and $(0, -4, 1, -2, 3)$; they keep falling. In the check pass the first edge, $c \to d$, is tense ($-2 + 3 = 1 < 3$). The walk of line L11 from $d$ goes back to $c$, $b$, $a$, $c$, $b$ and stops at $x = b$. Line L12 returns the cycle $c \to a \to b \to c$.

## Correctness

**Theorem.** Let $\delta_k(v)$ be the least weight of a walk from $s$ to $v$ with at most $k$ edges. (1) After pass $k$ of lines L3 to L8, $d[v] \le \delta_k(v)$ for each $v$. (2) If no negative cycle is reachable from $s$, the algorithm returns nil for the cycle, with $d[v] = \delta(s, v)$ for each $v$ and a shortest-path tree in $\pi$. (3) If a negative cycle is reachable from $s$, it returns a cycle of the graph whose weight is negative.

Part (1) is the [path-relaxation property](/edge-relaxation/), proved by induction on $k$: a walk with $k$ edges is a walk with $k - 1$ edges followed by one edge, which pass $k$ relaxes. If no negative cycle is reachable, a shortest walk can be taken to be a simple path, with at most $n - 1$ edges, so $\delta_{n-1}(v) = \delta(s, v)$; with the upper-bound property, $d[v] = \delta(s, v)$, no edge is tense, and the check finds nothing. If a negative cycle is reachable, some edge is always tense, so the algorithm reaches line L11. The full proof, including why the walk of line L11 lands on a negative cycle, is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/); each relaxation is $O(1)$ steps.

- **Worst case.** The initialization takes $\Theta(n)$. There are at most $n - 1$ passes and one check pass, each $\Theta(m)$. The walk of line L11 takes $n$ steps and line L12 at most $n$ more, once. The total is $O(n + nm)$, which is $O(nm)$ when $m \ge 1$.
- **The bound is reached.** On a path $v_1 \to v_2 \to \cdots \to v_n$ from $s = v_1$ whose edges are listed in reverse order, each pass fixes one more vertex, so all $n - 1$ passes change something. With $m = n - 1$ this is $\Theta(n^2) = \Theta(nm)$ work.
- **Best case.** If the first pass already gives the final values, the second pass changes nothing and line L8 stops. That is $\Theta(n + m)$, which is a lower bound for any run, since each edge is read.
- **Space.** The arrays $d$ and $\pi$ and the flag take $\Theta(n)$ extra space. The edge list is the input.

For graphs with negative weights, $O(nm)$ was the best strongly polynomial bound for decades. Scaling algorithms for integer weights ([Gabow](/gabow-scaling-sssp/), [Goldberg](/goldberg-scaling-sssp/)) reach $O(m \sqrt{n} \log N)$, and [near-linear algorithms](/near-linear-negative-sssp/) for integer weights are now known.

## Properties

- **Negative weights.** Allowed. This is the main reason to use it.
- **Label-correcting.** An estimate can change many times, unlike in Dijkstra's algorithm.
- **Any edge order.** Correctness holds for each order of the edges in a pass; the order changes only the number of passes needed.
- **Distributed form.** Each vertex needs only the estimates of its in-neighbors, so the passes can run as rounds of messages. This is the base of [distance-vector routing](/distance-vector-routing/).
- **Certificate.** On success, the values $d$ have no tense edge, which anyone can check in $O(m)$. On failure, the cycle is checked by adding its weights.

## Variants and improvements

- **Early exit.** Line L8. It does not change the worst case.
- **Queue-based Bellman-Ford ([SPFA](/spfa/)).** Relax only the edges out of vertices whose estimate changed in the last round. Same worst case, often much faster.
- **Yen's order.** Number the vertices, split the edges into those that go up and those that go down, and alternate the two in each pass. This cuts the number of passes about in half.
- **Finding all vertices with $\delta = -\infty$.** Every vertex that is reachable from a vertex changed in pass $n$ has distance $-\infty$; a [graph search](/graph-reachability/) from them marks all of them.
- **[Goldberg-Radzik](/goldberg-radzik/) and Tarjan's subtree disassembly.** Better orders and earlier detection of cycles, still $O(nm)$ in the worst case.
- **Virtual source.** To detect any negative cycle, not only those that $s$ reaches, add a new vertex with an edge of weight 0 to each vertex and run from it, or start with $d[v] = 0$ for all $v$.

## When to use it

Use Bellman-Ford when some weights are negative, or when you must detect a negative cycle, as in [arbitrage detection](/currency-arbitrage/). With nonnegative weights, [Dijkstra's algorithm](/dijkstra/) is much faster. On a DAG with any weights, [DAG shortest paths](/dag-shortest-paths/) takes $O(n + m)$. For all pairs with negative weights on a sparse graph, run Bellman-Ford once inside [Johnson's algorithm](/johnson/) and then Dijkstra from each vertex.

## Pitfalls

- **One pass too few.** The loop of line L3 must run $n - 1$ times, not $n - 2$; the reverse-order path needs all of them.
- **Reading the predecessor of $v$ as the cycle.** In line L11 the vertex $v$ of the tense edge need not be on a negative cycle; it can be behind one. Walk back $n$ steps first, as line L11 does, and only then collect the cycle.
- **Overflow and infinity.** Without the test $d[u] \ne \infty$, a large constant used for $\infty$ plus a negative weight looks finite and spreads. Keep the test in lines L6 and L10.
- **Negative edges in an undirected graph.** Turning an undirected edge of weight $-1$ into two directed edges makes a negative cycle of weight $-2$. Shortest simple paths in undirected graphs with negative edges need a different method, based on matching.
- **Reporting distances after a cycle.** When the check finds a tense edge, the values $d$ are not distances. Do not return them as an answer.

## Implementations

The Python version takes an edge list and returns the triple $(d, \pi, \text{cycle})$, where the cycle is a list of vertices in path order, or None.

## History

Alfonso Shimbel described the method in 1955. Lester Ford Jr. gave it in a RAND report in 1956, Richard Bellman published it in 1958 as the solution of a functional equation by successive approximation, and Edward F. Moore published it in 1959. The name Bellman-Ford is the usual one; some books add Moore.

## References
