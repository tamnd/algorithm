---
tag: T0RAP2
kind: algorithm
slug: dial-algorithm
name: Dial's algorithm
aliases:
- Dial's bucket-based Dijkstra
area: graphs/shortest-paths
level: core
summary: Dijkstra with a bucket queue for small integer weights, running in O(m + nC) time.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, C: the largest edge weight}
  time: {worst: O(m + n C), best: Θ(n + m + C)}
  space: {extra: Θ(n + m + C)}
properties: {deterministic: true, recursive: false}
prereqs: [dijkstra, bucket-queue, edge-relaxation]
see_also: [dijkstra, bucket-queue, radix-heap, zero-one-bfs, delta-stepping, thorup-undirected-sssp, breadth-first-search, pseudo-polynomial-time]
sources:
  - paper: doi:10.1145/363269.363610
    title: Robert B. Dial, Algorithm 360, Shortest-path forest with topological ordering, Communications of the ACM 12(11), 632 to 633 (1969)
    locator: the whole algorithm (buckets indexed by distance, used in a circular way)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 4, Shortest paths, label-setting algorithms (the section Dial's implementation, with the O(m + nC) bound and the circular use of C + 1 buckets)
  - paper: doi:10.1287/opre.27.1.161
    title: Eric V. Denardo and Bennett L. Fox, Shortest-route methods, 1. Reaching, pruning, and buckets, Operations Research 27(1), 161 to 186 (1979)
    locator: the sections on buckets (one level and multi-level bucket structures)
  - paper: doi:10.1007/BF02592101
    title: Boris V. Cherkassky, Andrew V. Goldberg and Tomasz Radzik, Shortest paths algorithms, theory and experimental evaluation, Mathematical Programming 73(2), 129 to 174 (1996)
    locator: the section on bucket implementations of Dijkstra's algorithm, and the experiments
---

Dial's algorithm is [Dijkstra's algorithm](/dijkstra/) with the priority queue replaced by an array of buckets, one per possible distance, for graphs whose edge weights are nonnegative integers at most $C$. The scan moves through the buckets in increasing order, so finding the next vertex costs only the empty buckets passed, and every finite distance is at most $(n - 1)C$. That gives $O(m + nC)$ time. Since all tentative distances lie in a window of $C + 1$ values, $C + 1$ buckets used in a circle are enough.

## In plain words

Dijkstra's method keeps a waiting list of places, sorted by their best known cost, and always finishes the cheapest one next. Keeping the list sorted costs time.

When every road length is a small whole number, there is a cheaper list. Make a row of boxes labeled 0, 1, 2, and so on. A place whose cost is 7 goes in box 7. Walk along the boxes from left to right. Everything in the current box is the cheapest place left, so finish it and drop its neighbors into later boxes.

Costs waiting in the boxes are never more than the longest road beyond the current box, so a short row of boxes, reused in a circle, is enough.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, an integer weight $w(u, v) \in \{0, 1, \ldots, C\}$ on each edge, and a source $s$. The output is $\delta(s, v)$ for every $v$ and a [shortest-path tree](/shortest-path-tree/), as in the [single-source shortest-path problem](/single-source-shortest-paths/).

**Weight assumptions.** Every weight is a nonnegative integer at most $C$; zero weights are allowed. So there is no negative cycle. A vertex that $s$ does not reach gets $\delta(s, v) = +\infty$. Negative weights break the bucket order and fractional weights have no bucket; the implementation rejects both. For real weights, use Dijkstra with a heap; for negative weights, [Bellman-Ford](/bellman-ford/).

## The algorithm

Bucket $B[j]$, for $j = 0, \ldots, C$, holds vertices whose tentative distance is congruent to $j$ modulo $C + 1$. The index $i$ is the distance being scanned. A vertex can sit in several buckets after its label drops; only the entry that matches its current label counts.

```pseudo id=main
DIAL(G, w, s)
L1  for each v do d[v] ← ∞, π[v] ← nil; B[0..C] ← empty lists
L2  d[s] ← 0; add s to B[0]
L3  i ← 0; left ← 1                              ▷ left = number of entries in all buckets
L4  while left > 0 do
L5      while B[i mod (C + 1)] is empty do i ← i + 1
L6      remove some u from B[i mod (C + 1)]; left ← left − 1
L7      if d[u] < i then continue                ▷ a stale entry: u was scanned at d[u]
L8      for each edge (u, v) do
L9          if i + w(u, v) < d[v] then
L10             d[v] ← i + w(u, v); π[v] ← u; add v to B[d[v] mod (C + 1)]; left ← left + 1
L11 return d, π
```

Lines L8 to L10 are the [relaxation](/edge-relaxation/) of Dijkstra's algorithm with $d[u] = i$. A zero-weight edge adds a vertex to the bucket being scanned, and line L5 does not move on until that bucket is empty. A version without lazy entries keeps each bucket as a doubly linked list and moves a vertex between buckets when its label drops; the bound is the same.

## Example

The vertices are $s, a, b, c, t, z$ and the edges $s \to a$ (2), $s \to b$ (3), $a \to b$ (0), $a \to c$ (3), $b \to c$ (3), $b \to t$ (3), $c \to t$ (1), $z \to s$ (1). So $C = 3$, and there are four buckets.

| $i$ | bucket $i \bmod 4$ | action | labels $s\,a\,b\,c\,t\,z$ |
|---|---|---|---|
| 0 | $\{s\}$ | scan $s$: $a = 2$ into $B[2]$, $b = 3$ into $B[3]$ | 0 2 3 ∞ ∞ ∞ |
| 1 | empty | move on | |
| 2 | $\{a\}$ | scan $a$: $b = 2$ into $B[2]$ (the zero edge), $c = 5$ into $B[1]$ | 0 2 2 5 ∞ ∞ |
| 2 | $\{b\}$ | scan $b$: $c$ stays 5, $t = 5$ into $B[1]$ | 0 2 2 5 5 ∞ |
| 3 | $\{b\}$ | stale entry for $b$ (label 2 < 3), skip | |
| 4 | empty | move on | |
| 5 | $\{c, t\}$ | scan $t$ (no edges), then $c$: $t$ stays 5 | 0 2 2 5 5 ∞ |

Bucket $B[1]$ is used for distance 5, since $5 \bmod 4 = 1$: the window of live keys at $i = 2$ is $\{2, 3, 4, 5\}$, and each of its values has its own bucket. The result is $\delta = (0, 2, 2, 5, 5, \infty)$; $z$ has an edge to $s$ but none from it, so it is not reachable.

**A negative weight.** With $a \to b$ of weight $-1$, the label $b = 1$ would belong to a bucket the scan has already passed, and $b$ would never be scanned at the right time. A negative cycle has no bucket order at all. The algorithm does not apply; the implementation raises an error.

## Correctness

**Theorem.** If all weights are integers in $\{0, \ldots, C\}$, the algorithm ends with $d[v] = \delta(s, v)$ for every $v$ and $d[v] = d[\pi[v]] + w(\pi[v], v)$ for every reachable $v \ne s$.

**Window invariant.** Every entry in the buckets has a key (the label it was added with) in $\{i, \ldots, i + C\}$. A key added in line L10 is $i + w$ with $0 \le w \le C$. The index $i$ grows only in line L5, past a bucket that is empty; since the $C + 1$ keys of the window fall into distinct buckets, that bucket held all entries with key $i$, so no key $i$ remains and the window can move up by one. So the bucket $B[i \bmod (C + 1)]$ holds exactly the entries with key $i$, and each entry removed in line L6 has the smallest key of all entries. That is what extract-min of a lazy-deletion heap returns, and an entry with $d[u] < i$ is exactly a stale one. So the run is a run of [Dijkstra's algorithm](/dijkstra/) with lazy deletion, and its correctness proof applies; see [the correctness of Dijkstra's algorithm](/dijkstra-correctness/). The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/) with integer weights in words.

- **Time.** Each vertex is scanned at most once (line L7 skips later entries), and each scan of $u$ looks at each edge out of $u$ once: $O(n + m)$ for lines L6 to L10, with at most $m + 1$ entries. Line L5 moves $i$ only forward, and $i$ never passes the largest finite distance, which is at most $(n - 1)C$ because a shortest path has at most $n - 1$ edges. Setting up $C + 1$ buckets takes $\Theta(C)$. The total is $O(m + nC)$, counting $n \le m + 1$ for the vertices that matter.
- **Best case.** The setup alone is $\Theta(n + m + C)$ when the graph is read in full.
- **Space.** The labels and predecessors take $\Theta(n)$, the buckets $\Theta(C)$ and the entries $O(m)$; with moving instead of lazy entries, $O(n + C)$.
- **Pseudo-polynomial.** The bound depends on the value $C$, not on its bit length, so it is [pseudo-polynomial](/pseudo-polynomial-time/). For $C = O(1)$ it is $O(m + n)$, linear time; for $C = 1$ it is in effect [breadth-first search](/breadth-first-search/).

## Properties

- **Label-setting.** Each vertex is scanned once, with its final distance, as in Dijkstra.
- **No comparisons between keys.** The order comes from the bucket index, so the $\Omega(n \log n)$ sorting bound of comparison-based Dijkstra does not apply.
- **Ties.** Vertices in the same bucket have the same distance and can be scanned in any order.
- **Circular buckets.** Only $C + 1$ buckets are needed, not $(n - 1)C + 1$.
- **Monotone.** It is a monotone priority queue: the minimum never decreases, which is what makes the single moving index enough.

## Variants and improvements

- **Without the circle.** Use $(n - 1)C + 1$ buckets, one per possible distance. Simpler, with the same time but much more space.
- **[0-1 BFS](/zero-one-bfs/).** With weights 0 and 1, the two live buckets become the two ends of a [deque](/deque/).
- **Multi-level buckets.** Denardo and Fox (1979) put buckets of growing width in levels, giving $O(m + n \sqrt{C})$ with two levels and less with more.
- **[Radix heap](/radix-heap/).** Buckets of widths $1, 1, 2, 4, 8, \ldots$ relative to the last minimum give $O(m + n \log C)$.
- **[Delta-stepping](/delta-stepping/).** Buckets of width $\Delta$, scanned as a group with re-scans inside a bucket; designed for parallel machines.
- **Thorup's algorithm.** For undirected graphs with integer weights, a hierarchy of buckets gives $O(m)$ time; see [Thorup's undirected SSSP](/thorup-undirected-sssp/).
- **Approximate buckets.** Real weights rounded to buckets of width $\varepsilon$ give distances within a small additive error, as used in some codes.

## When to use it

Use it when the weights are small nonnegative integers, such as travel times in whole minutes, unit costs plus a few penalties, or grid moves with costs 1 to 9. With $C$ small next to $\log n$, it beats a heap in both time and code size. If $C$ is large, the empty buckets dominate; use a [binary heap](/binary-heap/), a [radix heap](/radix-heap/), or multi-level buckets.

## Pitfalls

- **Too few buckets.** Using $C$ buckets instead of $C + 1$ makes keys $i$ and $i + C$ share a bucket, and a vertex could be scanned before its distance is final.
- **Stale entries.** With lazy entries, an entry whose vertex now has a smaller label must be skipped (line L7). Scanning it again is harmless for the result here but costs time.
- **Stopping at the first empty bucket.** An empty bucket does not mean the end; the count of entries does. Without it, the scan either stops too early or walks forever.
- **Large $C$.** A single heavy edge raises $C$ for the whole graph. Then the time is driven by $nC$ even if almost all weights are small.
- **Non-integer weights.** Rounding real weights to integers changes the problem; the distances are then only approximate.

## Implementations

The Python version keeps lazy entries in $C + 1$ list buckets, counts the entries to know when to stop, and rejects weights that are negative or not integers.

## History

Dial published the method in 1969 as Algorithm 360 of the Communications of the ACM. Denardo and Fox (1979) developed bucket structures with several levels, and the experiments of Cherkassky, Goldberg and Radzik (1996) found bucket-based codes among the fastest for shortest paths in practice.

## References
