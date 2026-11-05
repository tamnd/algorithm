---
tag: 5HVW8R
kind: algorithm
slug: demetrescu-italiano-apsp
name: Demetrescu-Italiano dynamic APSP algorithm
aliases:
- Demetrescu-Italiano algorithm
area: graphs/dynamic-graphs
level: research
summary: Dynamic all-pairs shortest paths for directed graphs with amortized update bounds.
solves: [dynamic-all-pairs-shortest-paths]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {amortized: O(n^2 log^3 n)}
  space: {extra: O(m n log n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2003
  people: [Camil Demetrescu, Giuseppe F. Italiano]
  note: Presented at STOC 2003, with the journal version in the Journal of the ACM in 2004.
prereqs: [dynamic-all-pairs-shortest-paths, dijkstra, amortized-update-time]
see_also: [all-pairs-shortest-paths, dynamic-single-source-shortest-paths, decremental-sssp, floyd-warshall, ramalingam-reps, dynamic-transitive-closure]
sources:
  - paper: doi:10.1145/1039488.1039492
    title: Camil Demetrescu and Giuseppe F. Italiano, A new approach to dynamic all pairs shortest paths, Journal of the ACM 51(6), 968 to 992 (2004)
    locator: the definitions of locally shortest and locally historical paths, the bound of mn locally shortest paths under unique shortest paths, the cleanup and fixup procedures, the smoothing strategy, and the main theorem (O(n^2 log^3 n) amortized time per vertex update)
  - paper: doi:10.1145/780564.780567
    title: Camil Demetrescu and Giuseppe F. Italiano, A new approach to dynamic all pairs shortest paths, Proceedings of STOC 2003, 159 to 166
    locator: the conference version of the same results
  - paper: doi:10.1145/1198513.1198519
    title: Camil Demetrescu and Giuseppe F. Italiano, Experimental analysis of dynamic all pairs shortest path algorithms, ACM Transactions on Algorithms 2(4), 578 to 601 (2006)
    locator: the experiments with the algorithm based on locally shortest paths, and the observed number of such paths
  - paper: doi:10.1007/978-3-540-27810-8_33
    title: Mikkel Thorup, Fully-dynamic all-pairs shortest paths, faster and allowing negative cycles, Proceedings of SWAT 2004, Lecture Notes in Computer Science 3111, 384 to 396
    locator: the simplification and improvement of the Demetrescu-Italiano bound
---

The Demetrescu-Italiano algorithm keeps all-pairs shortest paths in a directed graph with nonnegative real weights under vertex updates, which change any set of edges at one vertex. It solves the [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/) problem in $O(n^2 \log^3 n)$ amortized time per update with $O(1)$ query time, and it is deterministic. Its idea is to keep, besides the shortest paths, the *locally shortest paths*: paths whose every proper subpath is shortest. After an update, new shortest paths are built only from these, by a [Dijkstra](/dijkstra/)-like pass over all pairs at once.

## In plain words

A path is "locally shortest" if cutting off its first step or its last step leaves a shortest path. Every shortest path is locally shortest, but a locally shortest path need not be shortest. These paths are the candidates: when a road changes, the new best route between two places is always one of them.

The algorithm keeps a store of candidates. When the roads at one place change, it first throws away every stored path through that place. Then it rebuilds, from the cheapest paths upward: each time it finds a new best route, it tries to grow it by one step at either end, using other best routes that fit. The full method also keeps some older paths and spreads its work over time, so that each change costs about $n^2$ steps on average.

## The problem

**Input.** A directed graph on vertices $0, \ldots, n - 1$ with weights $w(a, b) \ge 0$, and an online sequence of vertex updates. A vertex update at $v$ inserts, deletes or changes the weight of any set of edges that touch $v$.

**Output.** After each update, the distance $d(x, y)$ for every pair, and a shortest path for every pair with $d(x, y) < \infty$. A query for a distance takes $O(1)$ time, and a query for a path takes time proportional to its number of edges.

**Unique shortest paths.** The method needs a unique shortest path for each pair. Give each edge a distinct number $\mathrm{id}(e)$, and compare paths by the pair $\big(w(\pi), \sum_{e \in \pi} 2^{\mathrm{id}(e)}\big)$ in lexicographic order. Two different simple paths have different edge sets, so they never tie, and the first part of the pair is the usual weight. In this order, a subpath of a shortest path is again shortest.

## The algorithm

For a path $\pi$ from $x$ to $y$ with at least one edge, $l(\pi)$ is $\pi$ without its last edge and $r(\pi)$ is $\pi$ without its first edge. For an edge $(x, y)$, these are the one-vertex paths $x$ and $y$. A path is **locally shortest** if it is an edge, or if $l(\pi)$ and $r(\pi)$ are both shortest. Each stored path keeps pointers to $l(\pi)$ and $r(\pi)$, and lists $L_{ext}(\pi)$ and $R_{ext}(\pi)$ of the stored paths $P$ with $l(P) = \pi$ and with $r(P) = \pi$. For each current shortest path $\sigma$, the algorithm puts $\sigma$ in two lists: $L^*(r(\sigma))$ and $R^*(l(\sigma))$. So $L^*(\tau)$ holds the shortest paths that extend $\tau$ by one edge on the left, and $R^*(\tau)$ those that extend it on the right. $\mathrm{SP}[x, y]$ is the current shortest path from $x$ to $y$.

```pseudo id=main
UPDATE(v, changes)
L1  CLEANUP(v)
L2  apply the changes to the edges at v
L3  FIXUP(v)

CLEANUP(v)                                   ▷ remove every stored path through v
L4  Q ← the edge paths of all edges at v
L5  while Q is not empty do take a path π from Q
L6      remove π from the store
L7      if SP[x(π), y(π)] = π then remove π from the lists L*, R*, and clear SP[x(π), y(π)]
L8      add all paths of L_ext(π) and R_ext(π) to Q

FIXUP(v)
L9  store an edge path for each edge at v
L10 H ← a priority queue with the lightest stored path of each pair
L11 while H is not empty do
L12     π ← EXTRACT-MIN(H), with ends x and y
L13     if the pair (x, y) was already settled in this FIXUP then continue
L14     mark (x, y) as settled
L15     if SP[x, y] = π then continue                  ▷ an old shortest path, nothing new
L16     if SP[x, y] ≠ nil then remove SP[x, y] from the lists L*, R*
L17     SP[x, y] ← π, put π into L*(r(π)) and R*(l(π))
L18     for each σ in L*(l(π)) with x(σ) ≠ y do COMBINE(σ, π)
L19     for each σ in R*(r(π)) with y(σ) ≠ x do COMBINE(π, σ)

COMBINE(a, b)                                 ▷ r(a) = l(b); the new path is a followed by the last edge of b
L20 if the path with l = a and r = b is stored then return
L21 P ← a new path from x(a) to y(b), with l(P) = a, r(P) = b, w(P) = w(a) + w(last edge of b)
L22 store P, and add it to L_ext(a) and R_ext(b)
L23 INSERT(H, P)
```

The store holds every generated path until a cleanup removes it. So it also holds paths that were shortest, or locally shortest, at an earlier time; the paper calls the paths that were shortest at some time since their last update *historical*. This version is the core of the method. The full algorithm adds a **smoothing** step, described under Complexity, which this page and its implementation do not include.

## Example

Take vertices $0, 1, 2, 3$ and four vertex updates. The table lists the shortest paths of more than one edge and the stored paths of more than one edge after each update.

| update | shortest paths, weight | stored paths |
|---|---|---|
| at 1: add $0 \to 1$ (3), $1 \to 2$ (1), $1 \to 3$ (4) | 012 (4), 013 (7) | 012, 013 |
| at 2: add $0 \to 2$ (5), $2 \to 3$ (1) | 012 (4), 0123 (5), 123 (2) | 012, 013, 0123, 123 |
| at 1: delete $0 \to 1$, set $1 \to 3$ to 1 | 023 (6) | 023, 123 |
| at 1: add $0 \to 1$ (1) | 012 (2), 013 (2) | 012, 013, 023, 123 |

After the second update, the path 013 is still stored, although 0123 is now shorter: it was locally shortest when it was built. The third update shows both phases. CLEANUP at 1 removes the edge paths $01$, $12$, $13$ and, through the lists $L_{ext}$ and $R_{ext}$, every longer path through 1: 012, 013, 0123 and 123. This clears $\mathrm{SP}$ for the pairs $(0, 1)$, $(0, 2)$, $(0, 3)$, $(1, 2)$, $(1, 3)$. FIXUP stores the edge paths $12$ (1) and $13$ (1) again and starts with $H = \{02, 12, 13, 23\}$. It confirms $23$, which was already shortest, at line L15. It settles $12$, and line L19 combines it with $23$ into 123 (2). It settles $13$. Then 123 is skipped, because $(1, 3)$ is settled with weight 1. Then $02$ (5) is settled and combined with $23$ into 023 (6), which becomes the shortest path from 0 to 3. In the last update, 023 stays in the store as an old path.

## Correctness

The proof keeps a set of invariants between updates: every stored path is a simple path of the current graph with its correct weight; the lists $L_{ext}$ and $R_{ext}$ reach every stored path from its edges; each edge has a stored edge path; at most one stored path has a given vertex sequence; $\mathrm{SP}[x, y]$ is the unique shortest path for each connected pair; and for any two current shortest paths $a$ and $b$ with $r(a) = l(b)$, the path with $l = a$ and $r = b$ is stored. CLEANUP removes exactly the stored paths through $v$, together with the shortest paths among them, and keeps the other invariants. FIXUP then settles the pairs in increasing order of their shortest paths, like Dijkstra's algorithm. For a shortest path $P$ of two or more edges, $l(P)$ and $r(P)$ are shortest and lighter, so they are settled first, and the later of the two, or the store itself, puts $P$ into $H$ in time. The full proof is below.

## Complexity

**Of the full algorithm.** Under unique shortest paths, a locally shortest path is fixed by its first edge and its last vertex, because the rest is the unique shortest path from the second vertex. So there are at most $mn$ locally shortest paths, and for each pair the shortest one is among them. With only locally shortest paths, a fully dynamic sequence can make paths stop and start being shortest many times, and the work per update is not bounded by about $n^2$. Demetrescu and Italiano keep the *locally historical* paths, whose proper subpaths were shortest at some time since their last update, and they bound how many historical paths a pair can have. The smoothing step adds dummy updates of vertices whose last update lies far in the past, which keeps the number of historical paths per pair small. With it, the amortized time per vertex update is $O(n^2 \log^3 n)$, which includes the cost of the priority queues. A distance query reads $\mathrm{SP}[x, y]$ in $O(1)$ time, and a path query follows the pointers $l$ in time proportional to its length.

**Of the version on this page.** Line L10 takes $O(n^2 \log n)$ time with one heap per pair. The rest of an update costs $O(\log n)$ for each path that CLEANUP removes or COMBINE creates, plus the length of the lists that lines L18 and L19 read. Without smoothing, the number of stored paths is not bounded by $mn$, so this version has no bound of the form $\tilde O(n^2)$ per update.

## Properties

- **Deterministic.** No random choices.
- **Amortized.** One update can take much more time than the bound; the work is spread over the sequence. Thorup (2005) gives worst-case bounds with other methods; see [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/).
- **Fully dynamic, vertex updates.** Insertions, deletions and weight changes of any edges at one vertex in one update.
- **Real weights.** The algorithm only adds and compares weights, so it works for nonnegative real weights, with no dependence on their size.
- **Explicit output.** All distances are stored, which costs $\Theta(n^2)$ space at least, and is necessary for $O(1)$ queries.

## Variants and improvements

- **Thorup (2004).** A simpler and faster version with a smaller polylogarithmic factor, which also allows negative weights and reports negative cycles.
- **Worst-case versions.** Thorup (2005) and later work keep the idea of historical paths but give bounds for every single update.
- **Partially dynamic.** For sequences of only increases, or only decreases, simpler versions of the method suffice.
- **Practical versions.** Demetrescu and Italiano (2006) found in experiments that the number of locally shortest paths is usually close to the number of shortest paths, so the version without smoothing is often fast.

## When to use it

Use it when all distances must be available at once and updates touch one vertex at a time, for example when a node in a network changes all its links. For single-source distances, use a [dynamic single-source](/dynamic-single-source-shortest-paths/) method instead. If updates are rare, recomputing with $n$ runs of Dijkstra may be simpler. If only reachability matters, use a [transitive closure](/dynamic-transitive-closure/) structure.

## Pitfalls

- **Ties.** Without a strict tie-break, a pair can have many shortest paths, and the bound of $mn$ locally shortest paths fails. The perturbation by edge numbers must be used in all comparisons.
- **Zero weights.** A cycle of zero weight makes many walks equally short. The tie-break still gives a strict order, because each extra edge adds a positive amount to the second part of the key.
- **Cleanup must follow both lists.** A path through $v$ may contain an edge at $v$ only in its left part or only in its right part. Following only $L_{ext}$ misses paths.
- **Floating-point weights.** The weight of a combination is $w(a)$ plus one edge weight. Computing it as $w(a) + w(b) - w(r(a))$ adds rounding errors.

## Implementations

## History

Demetrescu and Italiano presented the algorithm at STOC 2003, and the journal version appeared in 2004. Before it, the known fully dynamic algorithms for general real weights were not much faster than recomputation, and the best subcubic bounds, such as King's (1999), depended on the size of integer weights. Thorup simplified the method and improved the bound in 2004, and gave a worst-case version in 2005.

## References
