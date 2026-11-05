---
tag: 981JCR
kind: algorithm
slug: karger-min-cut
name: Karger's algorithm
aliases:
- Karger's contraction algorithm
- Karger's min-cut algorithm
- random contraction algorithm
- random edge contraction
area: graphs/flows-and-cuts
level: core
summary: Randomly contract edges until two vertices remain; repeat to find a min cut with high probability.
solves: [global-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, T: the number of runs}
  time: {worst: O(T m α(n))}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [global-min-cut-problem, graph-contraction, monte-carlo-algorithm, disjoint-set]
see_also: [karger-stein, stoer-wagner, nagamochi-ibaraki, minimum-cut-count-bound, edge-connectivity, kruskal, randomized-contractions]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 13.2, Finding the Global Minimum Cut (the contraction algorithm, its success probability, and the bound on the number of global minimum cuts)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.5, Application, A randomized min-cut algorithm
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Section 1.1, A min-cut algorithm, and Section 10.2 on the faster recursive version
  - paper: doi:10.1145/234533.234534
    title: David R. Karger and Clifford Stein, A new approach to the minimum cut problem, Journal of the ACM 43(4), 601 to 640 (1996)
    locator: Section 2 (the contraction algorithm and its analysis)
---

Karger's algorithm finds a [global minimum cut](/global-min-cut-problem/) of an undirected graph by [contracting](/graph-contraction/) uniformly random edges until only two super-vertices remain; the edges between them form a cut. One run returns a fixed minimum cut with probability at least $2 / (n(n-1))$, so about $\binom{n}{2} \ln(1/\varepsilon)$ independent runs find a minimum cut with probability at least $1 - \varepsilon$. It is a [Monte Carlo algorithm](/monte-carlo-algorithm/): the answer is always a real cut, but it may be larger than the minimum. Its analysis also proves that a graph has at most $\binom{n}{2}$ minimum cuts.

## In plain words

Take a network of cities and roads. Pick a road at random, and merge its two cities into one big city; roads inside the big city disappear, and the other roads stay. Repeat until only two big cities are left. The roads between them are a way to cut the network in two.

Why would this find the smallest cut? A smallest cut has few roads, while the network as a whole has many roads, because each city has at least as many roads as the smallest cut. So a random road is rarely one of the roads of that cut. If the process never picks one of them, the cut survives to the end. This happens with a small but known chance, so the method is run many times and the best result is kept.

## The problem

The input is an undirected [multigraph](/multigraph/) $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, $n \ge 2$, and $m$ edges. Parallel edges count separately, so an edge of integer weight $w$ can be given as $w$ parallel edges; self-loops are ignored. The graph may be disconnected. The output is a set $S$ with $\emptyset \ne S \subsetneq V$ that minimizes the number of edges with exactly one end in $S$. No source or sink is given, and edge direction plays no role; for directed graphs see the [directed global min cut](/directed-global-min-cut-problem/).

## The algorithm

Contracting edges in a uniformly random order, and skipping the edges that have become self-loops, is the same as contracting a uniform random non-loop edge at each step. So one run is a shuffle followed by [Kruskal](/kruskal/)-style merging in a [union-find](/disjoint-set/) structure, stopped at two classes.

```pseudo id=main
KARGER-MIN-CUT(n, E, T)
L1  best ← ∞
L2  repeat T times
L3      (S, k) ← CONTRACT(n, E)
L4      if k < best then best ← k, bestS ← S
L5  return best, bestS

CONTRACT(n, E)
L6  make a union-find structure with the classes {0}, ..., {n − 1}; comps ← n
L7  π ← a uniformly random permutation of E
L8  for each edge (u, v) in the order π, while comps > 2 do
L9      if FIND(u) ≠ FIND(v) then UNION(u, v), comps ← comps − 1
L10 S ← the class of vertex 0
L11 k ← the number of edges of E with exactly one end in S
L12 return S, k
```

Line L9 contracts the edge $(u, v)$: the two super-vertices become one, and every edge between them becomes a self-loop, which line L9 later skips. When the loop of line L8 stops with two classes, $S$ is one of them. If the graph is disconnected, the loop can run out of edges with more than two classes; then each class is a connected component, $S$ is the component of vertex 0, and $k = 0$, which is correct.

## Example

The graph has the vertices $a, b, c, d, e, f$. The triangles $abc$ and $def$ have each edge doubled, and the edges $c d$ and $b e$ join them, so $m = 14$. Each vertex has degree 4 or 5, and the unique minimum cut is $S = \{a, b, c\}$, with $k = 2$.

One run with the order that starts $ab, de, ef, ac, \ldots$:

| step | contracted edge | super-vertices | non-loop edges left |
|---|---|---|---|
| start | | $a, b, c, d, e, f$ | 14 |
| 1 | $a b$ | $ab, c, d, e, f$ | 12 |
| 2 | $d e$ | $ab, c, de, f$ | 10 |
| 3 | $e f$ | $ab, c, def$ | 6 |
| 4 | $a c$ | $abc, def$ | 2 |

The two edges left are $c d$ and $b e$, so the run returns the minimum cut. A run fails only when it contracts $c d$ or $b e$ before the two triangles are merged. Over all orders, one run returns $\{a, b, c\}$ with probability $13/35 \approx 0.371$, far above the guarantee $2/(6 \cdot 5) = 1/15$; the next most likely outcomes are the single vertices $\{a\}$ and $\{f\}$, each with $k = 4$.

## Correctness

Every run returns a set $S$ that holds vertex 0 and not all vertices, with $k$ the exact number of edges that cross it, so $k \ge \lambda$, the minimum cut. The key fact is that contraction never lowers the degree of a super-vertex below $\lambda$: the degree of a super-vertex $X$ is the size of the cut $(X, V \setminus X)$ of $G$. So when $i$ super-vertices remain, there are at least $i \lambda / 2$ non-loop edges, and a fixed minimum cut $C$ loses an edge with probability at most $2 / i$. The cut survives all $n - 2$ contractions with probability at least

$$\prod_{i=3}^{n} \Bigl(1 - \frac{2}{i}\Bigr) = \prod_{i=3}^{n} \frac{i-2}{i} = \frac{2}{n(n-1)}.$$

The full proof, with the equivalence of the shuffle and random contraction, is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/) with a source of random numbers.

- **One run.** The shuffle takes $O(m)$. The loop does at most $m$ FIND pairs and $n - 2$ UNIONs, $O(m\, \alpha(n))$ with union by rank and path compression (path halving in the code). Lines L10 and L11 take $O(n + m)$. So a run takes $O(m\, \alpha(n))$, and $O(m)$ with a linear-time union-find for this offline setting.
- **Many runs.** $T$ runs take $O(T m\, \alpha(n))$. The failure probability is at most $(1 - 2/(n(n-1)))^T \le e^{-2T/(n(n-1))}$. With $T = \lceil \binom{n}{2} \ln n \rceil$ this is at most $1/n$, for a total of $O(n^2 m \log n\, \alpha(n))$.
- **Space.** The union-find arrays and the shuffled copy of $E$: $\Theta(n + m)$.

Karger's first version used an adjacency matrix and took $O(n^2)$ per run, $O(n^4 \log n)$ in total. The recursive [Karger-Stein algorithm](/karger-stein/) cuts the total to $O(n^2 \log^3 n)$ for success probability $1 - 1/n$.

## Properties

- **Monte Carlo, one-sided error.** The answer is an upper bound on $\lambda$ that is correct with high probability, never smaller than $\lambda$.
- **Counting bound.** For each minimum cut $C$, one run returns $C$ with probability at least $1/\binom{n}{2}$. The events for different cuts are disjoint, so there are at most $\binom{n}{2}$ minimum cuts. The cycle $C_n$ has exactly $\binom{n}{2}$, so the bound is tight; see the [minimum cut count bound](/minimum-cut-count-bound/).
- **Approximate cuts.** The same argument shows that a cut of size at most $\alpha \lambda$ survives with probability at least about $n^{-2\alpha}$, so there are $O(n^{2\alpha})$ such cuts.
- **No flows.** It never computes a flow, and it needs no source or sink.

## Variants and improvements

- **Weighted graphs.** Pick each edge with probability proportional to its weight. With the shuffle form, give each edge an exponential random key with rate equal to its weight and sort by key.
- **Karger-Stein.** Contract only down to about $n/\sqrt{2}$ vertices, where the cut still survives with probability about $\frac12$, and recurse twice: [Karger-Stein](/karger-stein/).
- **Stopping at $k$ vertices.** Contracting to $k$ super-vertices keeps a fixed minimum cut with probability at least $\binom{k}{2} / \binom{n}{2}$; this is the step that Karger-Stein uses.
- **Near-linear time.** Karger (2000) found a global minimum cut of a weighted undirected graph in $O(m \log^3 n)$ time with high probability, using tree packings instead of contraction.

## When to use it

Use it for a simple global minimum cut of an undirected graph, especially as a teaching example of random sampling with a clean analysis, or when the graph is small. For a deterministic answer, [Stoer-Wagner](/stoer-wagner/) takes $O(nm + n^2 \log n)$ and has no error. For large graphs, Karger-Stein or near-linear algorithms are faster. For an $s$-$t$ cut, use a [maximum flow](/max-flow-problem/); random contraction does not keep $s$ and $t$ apart.

## Pitfalls

- **Picking a random pair of super-vertices instead of a random edge.** The analysis needs probability proportional to the number of edges between them. Line L7 shuffles edges, not vertex pairs.
- **Counting self-loops as candidates.** A loop must not be contracted; it would waste a step without merging anything. Line L9 tests $\mathrm{FIND}(u) \ne \mathrm{FIND}(v)$.
- **Merging parallel edges into one.** After a contraction, parallel edges must stay separate (or keep their total weight); otherwise the probabilities change and the guarantee is lost.
- **Too few runs.** One run succeeds with probability only $\Omega(1/n^2)$. With $T$ fixed and small, the answer is often wrong; take $T = \Theta(n^2 \log n)$.
- **Disconnected input.** If the code assumes that a non-loop edge always exists, it fails on a disconnected graph. Line L8 runs out of edges, and lines L10 and L11 then return a component with $k = 0$.

## Implementations

## History

David Karger published the contraction algorithm in 1993, in a paper on minimum cuts in the class RNC. Karger and Stein gave the recursive version in 1993 and the full journal paper in 1996. The analysis also gives a short probabilistic proof that a graph has at most $\binom{n}{2}$ minimum cuts.

## References
