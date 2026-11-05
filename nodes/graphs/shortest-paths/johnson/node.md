---
tag: GE9795
kind: algorithm
slug: johnson
name: Johnson's algorithm
aliases:
- Johnson's all-pairs shortest paths
area: graphs/shortest-paths
level: core
summary: Reweights with Bellman-Ford potentials, then runs Dijkstra from every vertex; handles sparse graphs with negative weights.
solves: [all-pairs-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: O(n m + n^2 log n)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false}
prereqs: [bellman-ford, dijkstra, potential-function-reduced-costs, all-pairs-shortest-paths]
see_also: [floyd-warshall, bellman-ford, dijkstra, potential-function-reduced-costs, negative-cycle-detection, all-pairs-shortest-paths, fibonacci-heap, slow-apsp-matrix-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.3, Johnson's algorithm for sparse graphs (the procedure JOHNSON, the reweighting lemma, Figure 23.6 and the analysis)
  - paper: doi:10.1145/321992.321993
    title: Donald B. Johnson, Efficient algorithms for shortest paths in sparse networks, Journal of the ACM 24(1), 1 to 13 (1977)
    locator: the all-pairs algorithm with reweighting
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths (the section on reweighting and Johnson's algorithm)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the section on shortest paths (Dijkstra in O(m + n log n), which gives the bound of Johnson's algorithm)
---

Johnson's algorithm solves the [all-pairs shortest paths](/all-pairs-shortest-paths/) problem on a directed graph whose arcs may have negative weights, or reports a [negative cycle](/negative-cycle/). It runs [Bellman-Ford](/bellman-ford/) once from an added vertex to get a [potential](/potential-function-reduced-costs/) $h$, changes each weight to the reduced cost $w(u, v) + h(u) - h(v) \ge 0$, and runs [Dijkstra's algorithm](/dijkstra/) from every vertex on the new weights. With a [Fibonacci heap](/fibonacci-heap/) the time is $O(nm + n^2 \log n)$, which beats the $\Theta(n^3)$ of [Floyd-Warshall](/floyd-warshall/) on sparse graphs.

## In plain words

Dijkstra's method is fast, but it fails when some roads have negative costs. Johnson's idea is to change the costs so that none is negative, without changing which routes are the cheapest.

To do that, it gives each place a height and adds to each road cost the height of its start minus the height of its end. Over a whole trip, the heights in the middle cancel, so every trip between the same two places changes by the same amount, and the cheapest trip stays the cheapest. Good heights come from one run of the slow method that allows negative costs, started from a new place joined to every place by a free road. Then the fast method runs from every place, and at the end the height change is undone.

## The problem

The input is a directed graph $G = (V, E)$ with $n = |V|$, $m = |E|$ and weights $w : E \to \mathbb{R}$. The output is the matrix $D$ with $D[u][v] = \delta(u, v)$ for all $u, v \in V$, with $\infty$ when $v$ is not reachable from $u$, or the report that $G$ has a negative cycle.

**Weight assumptions.** Any real weights, negative ones included. If $G$ has a negative cycle anywhere, the algorithm reports it and returns no matrix, even for pairs whose distance is finite. Integer weights are not needed; the Python code works with integers and floats.

## The algorithm

```pseudo id=main
JOHNSON(G, w)
L1  G′ ← G with a new vertex q and an arc (q, v) of weight 0 for each v in V
L2  run BELLMAN-FORD(G′, w, q)
L3  if it reports a negative cycle then return "negative cycle"
L4  for each v in V do h(v) ← δ(q, v)
L5  for each (u, v) in E do ŵ(u, v) ← w(u, v) + h(u) − h(v)
L6  for each u in V do
L7      run DIJKSTRA(G, ŵ, u), which gives δ̂(u, v) for each v in V
L8      for each v in V do D[u][v] ← δ̂(u, v) − h(u) + h(v)      ▷ ∞ stays ∞
L9  return D
```

Lines L1 to L4 compute the potential. Every vertex is reachable from $q$, so each $h(v)$ is a real number, and $h(v) \le 0$ because of the arc $q \to v$. Line L5 makes the reduced costs, which are all nonnegative. Lines L6 and L7 run Dijkstra on $G$ itself, without $q$. Line L8 undoes the shift: a walk from $u$ to $v$ has reduced weight equal to its true weight plus $h(u) - h(v)$.

## Example

The graph of CLRS Figure 23.6 has the vertices 1 to 5 and the arcs $1 \to 2$ (3), $1 \to 3$ (8), $1 \to 5$ ($-4$), $2 \to 4$ (1), $2 \to 5$ (7), $3 \to 2$ (4), $4 \to 1$ (2), $4 \to 3$ ($-5$) and $5 \to 4$ (6).

**Lines L1 to L4.** Bellman-Ford from $q$ gives $h = (0, -1, -5, 0, -4)$ for the vertices 1 to 5, and no negative cycle.

**Line L5.** The reduced costs are:

| arc | $1 \to 2$ | $1 \to 3$ | $1 \to 5$ | $2 \to 4$ | $2 \to 5$ | $3 \to 2$ | $4 \to 1$ | $4 \to 3$ | $5 \to 4$ |
|---|---|---|---|---|---|---|---|---|---|
| $w$ | 3 | 8 | $-4$ | 1 | 7 | 4 | 2 | $-5$ | 6 |
| $\hat w$ | 4 | 13 | 0 | 0 | 10 | 0 | 2 | 0 | 2 |

**Lines L6 to L8.** Dijkstra from each source on $\hat w$, then the shift back:

| source | $\hat\delta(u, \cdot)$ for 1 to 5 | $D[u][\cdot]$ for 1 to 5 |
|---|---|---|
| 1 | 0, 2, 2, 2, 0 | 0, 1, $-3$, 2, $-4$ |
| 2 | 2, 0, 0, 0, 2 | 3, 0, $-4$, 1, $-1$ |
| 3 | 2, 0, 0, 0, 2 | 7, 4, 0, 5, 3 |
| 4 | 2, 0, 0, 0, 2 | 2, $-1$, $-5$, 0, $-2$ |
| 5 | 4, 2, 2, 2, 0 | 8, 5, 1, 6, 0 |

For example $D[1][3] = \hat\delta(1, 3) - h(1) + h(3) = 2 - 0 - 5 = -3$, by the path $1 \to 5 \to 4 \to 3$ of weight $-4 + 6 - 5 = -3$. From source 1, Dijkstra finishes the vertices in the order 1 (0), 5 (0), 4 (2), 3 (2), 2 (2). The matrix agrees with Floyd-Warshall on the same graph.

**A negative cycle.** Add the arc $3 \to 4$ of weight 4. The cycle $3 \to 4 \to 3$ has weight $4 - 5 = -1$, and line L3 returns "negative cycle".

## Correctness

**Theorem.** If $G$ has a negative cycle, JOHNSON reports one. Otherwise it returns $D[u][v] = \delta(u, v)$ for all $u, v$, with $\infty$ exactly for the pairs where $v$ is not reachable from $u$.

The proof has four steps. The cycles of $G'$ are exactly the cycles of $G$, because $q$ has no incoming arc, so Bellman-Ford from $q$ (which reaches everything) reports a negative cycle exactly when $G$ has one. The triangle inequality for $\delta(q, \cdot)$ gives $\hat w \ge 0$. Dijkstra is correct on nonnegative weights. And for every walk $p$ from $u$ to $v$, $\hat w(p) = w(p) + h(u) - h(v)$, so the shortest walks and the reachable pairs are the same under $w$ and $\hat w$, and line L8 gives the true distance. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Lines L1 to L5.** $G'$ has $n + 1$ vertices and $m + n$ arcs, so Bellman-Ford takes $O(n(m + n)) = O(nm + n^2)$ time. Line L5 takes $O(m)$.
- **Lines L6 to L8.** $n$ runs of Dijkstra. With a Fibonacci heap each run takes $O(m + n \log n)$ in the worst case, so the total is $O(nm + n^2 \log n)$. Line L8 takes $O(n^2)$ in total.
- **Total.** $O(nm + n^2 \log n)$ in the worst case on the word RAM, where an addition or comparison of two weights takes $O(1)$ time. The Bellman-Ford term $O(nm)$ is dominated by the Dijkstra term. With a [binary heap](/binary-heap/), as in the Python code, each Dijkstra run takes $O((n + m) \log n)$ and the total is $O(nm \log n)$ when $m \ge n$.
- **Space.** $O(n^2)$ for the output and $O(n + m)$ for $h$, $\hat w$ and the heap, so $O(n^2 + m)$ extra space. If the output is consumed row by row, the space is $O(n + m)$.

For a sparse graph with $m = O(n)$, the time is $O(n^2 \log n)$, against $\Theta(n^3)$ for Floyd-Warshall. For a dense graph with $m = \Theta(n^2)$, both are $\Theta(n^3)$ up to the heap, and Floyd-Warshall is simpler and has smaller constants.

## Properties

- **Exact.** It returns the exact distances for any real weights without a negative cycle.
- **All or nothing on negative cycles.** One negative cycle anywhere makes line L3 stop, even for pairs that cannot reach it. To get $-\infty$ entries instead, run Bellman-Ford from each source, or Floyd-Warshall with the usual extra pass.
- **Parallel friendly.** The $n$ Dijkstra runs of line L7 are independent.
- **Paths.** Each Dijkstra run also gives a [shortest-path tree](/shortest-path-tree/) for $\hat w$, which is a shortest-path tree for $w$; the $n$ trees form the predecessor matrix.

## Variants and improvements

- **Other SSSP inside.** Any nonnegative-weight SSSP algorithm can replace Dijkstra in line L7: with [Thorup's algorithm](/thorup-undirected-sssp/) for undirected positive integer weights after reweighting, or a [radix heap](/radix-heap/) for integer weights. For small integer weights the reduced costs stay integers.
- **A faster potential.** Line L2 can use any algorithm that finds a potential or a negative cycle: [Goldberg's scaling algorithm](/goldberg-scaling-sssp/) in $O(\sqrt{n}\, m \log W)$, or the [near-linear negative SSSP](/near-linear-negative-sssp/) algorithm for integer weights. With these, the Dijkstra term dominates on every graph.
- **No added vertex.** Starting all Bellman-Ford labels at 0 is the same as the vertex $q$, and the Python code does this.
- **Reuse of the potential.** In min-cost flow by successive shortest paths, the distances of one Dijkstra run on reduced costs are the potential for the next run, so Bellman-Ford is needed only once.

## When to use it

Use Johnson's algorithm for all-pairs shortest paths on a sparse graph with negative arcs. On a dense graph, or when $n$ is a few hundred, [Floyd-Warshall](/floyd-warshall/) is simpler and fast enough. With nonnegative weights, skip lines L1 to L5 and run Dijkstra from each vertex. If you need only some sources, compute $h$ once and run Dijkstra only from those sources.

## Pitfalls

- **Forgetting the shift back.** Line L8 must subtract $h(u)$ and add $h(v)$. Returning $\hat\delta$ gives $D[1][3] = 2$ instead of $-3$ in the example.
- **The sign of the reduced cost.** Line L5 is $w(u, v) + h(u) - h(v)$. With $w(u, v) - h(u) + h(v)$ the arc $4 \to 3$ of the example gets $-5 - 0 - 5 = -10$, and Dijkstra fails.
- **Keeping $q$ after line L2.** The vertex $q$ and its arcs are only for the potential. If they stay in the graph of line L7, every row gets an extra entry and the output has the wrong shape. Run Dijkstra on $G$ only.
- **Infinity arithmetic.** An unreachable pair has $\hat\delta = \infty$. Computing $\infty - h(u) + h(v)$ with a large integer as infinity gives a wrong finite number. Test for unreachable before the shift, as the Python code does.
- **Ignoring the report.** If line L3 is skipped, $h$ is not a potential, some $\hat w$ are negative, and Dijkstra returns wrong numbers without an error. The test with a negative self-loop catches this.

## Implementations

## History

Donald B. Johnson published the algorithm in the Journal of the ACM in 1977, as part of a study of shortest-path algorithms for sparse networks. The reweighting idea also appears in the work of Edmonds and Karp (1972) on min-cost flow, where vertex potentials keep the residual costs nonnegative so that Dijkstra can be used in each augmentation. With the Fibonacci heaps of Fredman and Tarjan (1987), the bound became $O(nm + n^2 \log n)$.

## References
