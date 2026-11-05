---
tag: NYWQX3
kind: algorithm
slug: brandes-algorithm
name: Brandes' algorithm
aliases:
- fast betweenness algorithm
area: graphs/network-analysis
level: advanced
summary: Computes all betweenness scores in O(nm) time using dependency accumulation.
solves: [betweenness-centrality-computation]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time:
    worst: Θ(n(n + m))
    best: Θ(n^2)
  space: {extra: Θ(n + m)}
properties: {directed: true, weighted: true, deterministic: true, recursive: false}
prereqs: [betweenness-centrality, breadth-first-search, dijkstra]
see_also: [betweenness-centrality, betweenness-centrality-computation, girvan-newman-algorithm, closeness-centrality, breadth-first-search, dijkstra, all-pairs-shortest-paths, centrality]
sources:
  - paper: doi:10.1080/0022250X.2001.9990249
    title: Ulrik Brandes, A faster algorithm for betweenness centrality, Journal of Mathematical Sociology 25(2), 163 to 177 (2001)
    locator: Section 3 (the counting of shortest paths and the Bellman criterion), Section 4 (the dependency recursion, Theorem 6) and the algorithm figure with its O(nm) and O(nm + n^2 log n) bounds
  - paper: doi:10.1016/j.socnet.2007.11.001
    title: Ulrik Brandes, On variants of shortest-path betweenness centrality and their generic computation, Social Networks 30(2), 136 to 145 (2008)
    locator: the whole paper (the changes of the accumulation for endpoints, edge betweenness, bounded distance and stress)
  - paper: doi:10.2307/3033543
    title: Linton C. Freeman, A set of measures of centrality based on betweenness, Sociometry 40(1), 35 to 41 (1977)
    locator: the whole paper (the definition by the fraction of shortest paths)
  - paper: doi:10.1142/S0218127407018403
    title: Ulrik Brandes and Christian Pich, Centrality estimation in large networks, International Journal of Bifurcation and Chaos 17(7), 2303 to 2318 (2007)
    locator: the whole paper (running the source loop on a sample of pivots and scaling the sums)
---

Brandes' algorithm computes the [betweenness centrality](/betweenness-centrality/) of every [vertex](/vertex/) of a graph with $n$ vertices and $m$ edges in $O(nm)$ time without weights, and in $O(nm + n^2 \log n)$ time with positive weights. Before it, the usual method counted the shortest paths for all pairs and then summed over all triples, in $\Theta(n^3)$ time and $\Theta(n^2)$ space. Brandes saw that the contributions of one source can be summed backwards over its shortest-path [DAG](/directed-acyclic-graph/), with one recursion on the *dependencies*, so that one [breadth-first search](/breadth-first-search/) per source suffices. It solves [betweenness centrality computation](/betweenness-centrality-computation/) and is the inner step of the [Girvan-Newman algorithm](/girvan-newman-algorithm/).

## In plain words

Betweenness asks, for each person in a network, how often they sit on the shortest routes between two others.

The slow way lists the routes for every pair. Brandes' algorithm takes one starting person at a time. A search from that person finds how far each other person is, and how many shortest routes reach each of them.

Then the algorithm walks back from the far end. Each person passes credit to the people just before them on shortest routes, in proportion to how many routes go through each. The credit a person holds at the end is how much the starting person relies on them to reach everyone else.

Adding this credit over all starting people gives the betweenness. Each search and each walk back looks at each link once, which is far less work than looking at all pairs.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given by adjacency lists. It may be directed or undirected; an undirected edge is in both lists. In the weighted form, each edge has a length $\ell(e) > 0$. Let $\sigma_{st}$ be the number of shortest paths from $s$ to $t$ (with $\sigma_{ss} = 1$), and $\sigma_{st}(v)$ the number of them that pass through $v$ as an inner vertex. The output is

$$C_B(v) = \sum_{s \ne v \ne t} \frac{\sigma_{st}(v)}{\sigma_{st}},$$

summed over ordered pairs with $\sigma_{st} > 0$. For an undirected graph each unordered pair appears twice in this sum, so the algorithm halves it at the end, which gives the usual value of [betweenness centrality](/betweenness-centrality/).

**Disconnected graphs.** Pairs with no path have $\sigma_{st} = 0$ and add nothing, so the formula needs no change: the search from $s$ never reaches $t$. **Ties.** Equal shortest paths are the point of the definition: $\sigma$ counts all of them, and each gets the same share.

The key quantities are the *pair dependency* $\delta_{st}(v) = \sigma_{st}(v) / \sigma_{st}$ and the *dependency* of $s$ on $v$,

$$\delta_{s\bullet}(v) = \sum_{t \in V} \delta_{st}(v), \qquad \text{so that} \qquad C_B(v) = \sum_{s \ne v} \delta_{s\bullet}(v).$$

Brandes proved that, with $P_s(w)$ the set of predecessors of $w$ on shortest paths from $s$,

$$\delta_{s\bullet}(v) = \sum_{w \,:\, v \in P_s(w)} \frac{\sigma_{sv}}{\sigma_{sw}} \bigl(1 + \delta_{s\bullet}(w)\bigr).$$

## The algorithm

```pseudo id=main
BRANDES(G)
L1  for each v ∈ V do CB[v] ← 0
L2  for each s ∈ V do
L3      S ← empty stack; for each w ∈ V do P[w] ← empty list, σ[w] ← 0, d[w] ← ∞
L4      σ[s] ← 1; d[s] ← 0; Q ← a queue that holds s
L5      while Q is not empty do
L6          v ← DEQUEUE(Q); PUSH(S, v)
L7          for each w ∈ Adj[v] do
L8              if d[w] = ∞ then d[w] ← d[v] + 1; ENQUEUE(Q, w)
L9              if d[w] = d[v] + 1 then σ[w] ← σ[w] + σ[v]; append v to P[w]
L10     for each v ∈ V do δ[v] ← 0
L11     while S is not empty do
L12         w ← POP(S)
L13         for each v ∈ P[w] do δ[v] ← δ[v] + (σ[v] / σ[w]) · (1 + δ[w])
L14         if w ≠ s then CB[w] ← CB[w] + δ[w]
L15 if G is undirected then for each v ∈ V do CB[v] ← CB[v] / 2
L16 return CB
```

Lines L4 to L9 are a breadth-first search that also counts shortest paths: when $w$ is one step further than $v$, every shortest path to $v$ extends to one to $w$, so $\sigma[w]$ gains $\sigma[v]$, and $v$ is a predecessor of $w$. The stack $S$ receives the vertices in the order of non-decreasing distance. Lines L11 to L14 pop them in the order of non-increasing distance, so when $w$ is popped, every vertex that has $w$ as a predecessor has already passed its share to $w$, and $\delta[w]$ is final.

**Weights.** With positive lengths, replace lines L4 to L9 by [Dijkstra's algorithm](/dijkstra/): push $v$ on $S$ when it is settled, and when an edge $(v, w)$ gives $d[v] + \ell(v, w) < d[w]$, set $d[w]$, set $\sigma[w] \leftarrow \sigma[v]$ and $P[w] \leftarrow [v]$; when it gives equality, add $\sigma[v]$ to $\sigma[w]$ and append $v$ to $P[w]$. Lines L10 to L16 do not change.

## Example

Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, with the lists in increasing order. The search from $s = 0$ pushes the vertices in the order $0, 1, 2, 3, 4, 5, 6$ and gives

| vertex $w$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d[w]$ | 0 | 1 | 1 | 2 | 3 | 4 | 4 |
| $\sigma[w]$ | 1 | 1 | 1 | 2 | 2 | 2 | 2 |
| $P[w]$ | | 0 | 0 | 1, 2 | 3 | 4 | 4 |

Vertex 3 has two shortest paths from 0, through 1 and through 2, and every vertex behind it inherits $\sigma = 2$. The pops then give

| popped $w$ | $\delta[w]$ | shares passed on |
|---|---|---|
| 6 | 0 | to 4: $\frac{2}{2}(1 + 0) = 1$ |
| 5 | 0 | to 4: $1$, so $\delta[4] = 2$ |
| 4 | 2 | to 3: $\frac{2}{2}(1 + 2) = 3$ |
| 3 | 3 | to 1 and to 2: $\frac{1}{2}(1 + 3) = 2$ each |
| 2 | 2 | to 0: $\frac{1}{1}(1 + 2) = 3$ |
| 1 | 2 | to 0: $3$, so $\delta[0] = 6$ |
| 0 | 6 | none, and $s$ is not added |

So the source 0 adds $2, 2, 3, 2, 0, 0$ to vertices 1 to 6. For example, $\delta[4] = 2$ because 0 needs 4 for the targets 5 and 6, and $\delta[1] = 2$ because half of the four targets 3, 4, 5, 6 go through 1. The dependencies of vertex 3 over the seven sources are $3, 3, 3, 0, 3, 3, 3$, which sum to 18. After the halving of line L15 the result is

$$C_B = (0, 2, 2, 9, 8, 0, 0).$$

Vertex 3 lies on every path between $\{0, 1, 2\}$ and $\{4, 5, 6\}$, 9 pairs. Vertex 4 lies on the paths from $\{5, 6\}$ to $\{0, 1, 2, 3\}$, 8 pairs. Vertices 1 and 2 each carry half of the 4 pairs between 0 and $\{3, 4, 5, 6\}$.

## Correctness

**Theorem.** BRANDES$(G)$ stops and returns $C_B(v)$ for every vertex $v$, for directed and undirected graphs, and, with the Dijkstra form of lines L4 to L9, for positive edge lengths.

The proof has three steps. First, the search computes $d[w] = d_G(s, w)$, the counts $\sigma[w] = \sigma_{sw}$, and the predecessor lists $P[w] = P_s(w)$, because each shortest path to $w$ ends with an edge from a predecessor and the predecessors are settled first. Second, the pair dependencies satisfy $\delta_{st}(v) = \sum_{w : v \in P_s(w)} \frac{\sigma_{sv}}{\sigma_{sw}} \delta_{st}(w)$ for $t \ne w$, plus $\frac{\sigma_{sv}}{\sigma_{st}}$ for $t = w$, and summing over $t$ gives the recursion for $\delta_{s\bullet}$. Third, the stack pops a vertex only after all vertices that are further from $s$, so each $\delta[w]$ is complete when it is used. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with arithmetic on $\sigma$ and $\delta$ counted as $O(1)$.

- **One source, no weights.** Lines L3, L4 and L10 take $O(n)$. The search pushes and pops each reachable vertex once and scans each list once, $O(n + m)$. Each predecessor entry corresponds to one edge, so the lists $P$ hold at most $m$ entries in total, and lines L11 to L14 take $O(n + m)$.
- **One source, with weights.** Dijkstra's algorithm with a [Fibonacci heap](/fibonacci-heap/) takes $O(m + n \log n)$, and with a [binary heap](/binary-heap/) $O(m \log n)$.
- **All sources.** $n$ times the above: $O(nm)$ for a connected graph without weights, $O(nm + n^2 \log n)$ with weights. Since line L3 costs $\Theta(n)$ per source, the time is never below $\Theta(n^2)$.

The extra space is $\Theta(n + m)$: the arrays and the predecessor lists of one source, reused for the next. Brandes' method needs no $n \times n$ table, which mattered as much as the time for large networks.

The counts $\sigma$ can grow exponentially in $n$, for example in a chain of squares, where each square doubles the count. In floating point they overflow or lose digits on large graphs of this kind; exact integers cost more than $O(1)$ per operation.

## Properties

- **Directed or undirected, weighted or not.** The same accumulation works for all four cases; only the search changes. For an undirected graph, the halving of line L15 turns ordered pairs into unordered ones.
- **Deterministic.** The result does not depend on the order of the lists or of the sources. The order affects only the floating-point rounding.
- **Not recursive.** The recursion on $\delta$ is carried out by the stack, in a loop.
- **One source at a time.** The sources are independent, so the loop of line L2 parallelizes well, with one array $C_B$ per thread summed at the end.
- **Free extras.** Each search gives the distances from $s$, so [closeness centrality](/closeness-centrality/) and the eccentricities come at no extra cost.

## Variants and improvements

- **Edge betweenness.** In line L13, the term $\frac{\sigma[v]}{\sigma[w]}(1 + \delta[w])$ is the share of the edge $(v, w)$. Adding it to a counter of that edge gives the edge betweenness in the same time, which is what the [Girvan-Newman algorithm](/girvan-newman-algorithm/) needs. Brandes (2008) gives this and other variants.
- **Endpoints.** To count $s$ and $t$ as on the path, add $\delta[w] + 1$ for $w \ne s$, plus the number of reachable vertices to $s$.
- **Stress centrality.** To count the shortest paths through $v$ rather than their fractions, accumulate $N[v] = \sum (1 + N[w])$ over the vertices $w$ with $v \in P[w]$, which is the number of shortest paths from $v$ to the vertices behind it, and add $\sigma[v] \cdot N[v]$ to the score of $v$.
- **Bounded distance.** Stop each search at distance $k$ to count only short paths.
- **Sampling.** Run the source loop only for a random sample of $k$ pivots and scale by $n/k$. Brandes and Pich study the choice of pivots. Sampling of shortest paths with bounds from the VC dimension gives guarantees for all vertices at once; see [betweenness centrality computation](/betweenness-centrality-computation/).
- **Dynamic graphs.** Incremental methods update the scores after an edge change by redoing only the sources whose DAG changes.

## When to use it

Use it for exact betweenness on graphs with up to some hundred thousand vertices, or more with a parallel source loop. It is the method in common network libraries. For larger graphs, run it on a sample of sources, or use path sampling, which bounds the error for all vertices. If the graph changes a little at a time, an incremental method can be faster than a new run. On a dense graph, $nm$ is $\Theta(n^3)$, the same as the old method, but the space is still linear.

## Pitfalls

- **Halving twice or not at all.** For an undirected graph stored with each edge in both lists, the sum over sources counts each unordered pair twice. Halve once, at the end.
- **Adding the source.** Line L14 must skip $w = s$: $\delta[s]$ is the number of reachable vertices minus 1, not a betweenness.
- **Zero-length edges.** With $\ell = 0$, two vertices can be at the same distance and be predecessors of each other, and the order of the stack is no longer safe. Merge such vertices first or forbid zero lengths.
- **Floating-point equality of distances.** With real weights, two equal path lengths can differ in the last digit, and the algorithm misses a tie. Use integer weights or a tolerance.
- **Overflow of $\sigma$.** Counts of shortest paths can exceed 64 bit integers on graphs with many parallel routes; use floats or big integers.
- **Multigraphs.** Parallel edges count as distinct paths in $\sigma$. Remove them first if paths are meant as vertex sequences.

## Implementations

## History

Anthonisse in 1971 and Freeman in 1977 defined betweenness by the fraction of shortest paths. For more than twenty years it was computed with all-pairs distances and a triple sum over all $(s, t, v)$, in $\Theta(n^3)$ time and $\Theta(n^2)$ space, which limited it to a few thousand vertices. Brandes published the dependency recursion in 2001, and it made betweenness practical on large sparse networks. In 2008 he showed how the same scheme covers the common variants.

## References
