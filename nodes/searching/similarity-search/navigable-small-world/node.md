---
tag: XDDYQ2
kind: data-structure
slug: navigable-small-world
name: Navigable small world graph
aliases:
- NSW graph
area: searching/similarity-search
level: advanced
summary: A proximity graph in which greedy routing from any node reaches near neighbors of a query quickly.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, f: the number of links made per insertion, ef: the beam width of a search}
  time: {insert: O(f n + n log n), search: O(f n + n log n)}
  space: {total: Θ(f n)}
properties: {deterministic: false, online: true}
history:
  year: 2014
  people: [Yury Malkov, Alexander Ponomarenko, Andrey Logvinov, Vladimir Krylov]
  note: Malkov, Ponomarenko, Logvinov and Krylov built the graph by inserting points in random order and linking each to the nearest points found by a greedy search, and published the method in Information Systems in 2014.
prereqs: [nearest-neighbor-search, k-nearest-neighbor-graph, best-first-search]
see_also: [hnsw, nn-descent, k-nearest-neighbor-graph, small-world-network, delaunay-triangulation, diskann, approximate-nearest-neighbor, similarity-index]
sources:
  - paper: doi:10.1016/j.is.2013.10.006
    title: Yury Malkov, Alexander Ponomarenko, Andrey Logvinov and Vladimir Krylov, Approximate nearest neighbor algorithm based on navigable small world graphs, Information Systems 45, 2014
    locator: pages 61 to 68 (the insertion of points in random order with links to the f nearest found, the multi-search with random entry points, and the experiments on the scaling of the search)
  - paper: doi:10.1145/335305.335325
    title: Jon Kleinberg, The small-world phenomenon, an algorithmic perspective, Proceedings of the 32nd Annual ACM Symposium on Theory of Computing (STOC 2000)
    locator: pages 163 to 170 (the grid with long-range links of probability proportional to the distance to the power −r, the O(log² n) expected delivery time of greedy routing for r = 2, and the polynomial lower bounds for other r)
  - paper: doi:10.1109/TPAMI.2018.2889473
    title: Yury A. Malkov and Dmitry A. Yashunin, Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs, IEEE Transactions on Pattern Analysis and Machine Intelligence 42(4), 2020
    locator: pages 824 to 836 (Section 2 on the polylogarithmic search of NSW and its causes, and the layered structure that improves it)
---

A navigable small world (NSW) graph is a [similarity index](/similarity-index/) for approximate [nearest neighbor search](/nearest-neighbor-search/) in any space with a distance. It is a graph on the data points, built by inserting the points one at a time in random order: each new point runs a search on the graph built so far and links, in both directions, to the $f$ nearest points that the search finds. Early points get links that span the whole data set, and later points get short links, so the graph has both the long links that cross the space fast and the short links that refine the answer. A query runs a [best-first](/best-first-search/) beam search from an entry point and returns the nearest points it meets. The answer is exact when the beam is as large as the data, and it is approximate, with no proven guarantee, otherwise; Malkov et al. observed polylogarithmic search cost in experiments. The [HNSW](/hnsw/) graph builds on it with layers.

## In plain words

Think of a network of friends, where each person knows a few others. To pass a message to someone you have never met, give it to the friend who lives closest to that person, and repeat. In a well-made network a few steps are enough, because some friendships are long-distance and others are local.

An NSW graph is such a network on data points. Each point added later searches the network for the points nearest to it and becomes their friend. The first points have no near neighbors yet, so their friendships span long distances. To answer a query, start at some point and keep moving to the friend closest to the query. A short list of the best points seen so far keeps the search from stopping at a point that only looks best nearby.

## The abstract type

The graph is a dynamic [similarity index](/similarity-index/) for a space $(U, d)$ in which $d$ is symmetric and $d(x, x) = 0$; the triangle inequality is not used. It supports INSERT$(p)$ and SEARCH$(q, k)$, which returns $k$ points of the index, in order of distance from $q$, meant to be the $k$ nearest. Cost is counted in evaluations of $d$ and in other time, in the real RAM with an oracle for $d$.

## Representation

The points $p_0, p_1, \ldots$ in order of insertion, and for each point the set of its neighbors: an undirected graph $G$ stored as adjacency sets. Two parameters are fixed at creation: $f$, the number of links that each insertion makes, and the beam width $ef_c$ of the search that each insertion runs. The entry point of a search is $p_0$, possibly with a few random nodes added.

**Invariants.** (I1) $G$ is undirected: $j$ is a neighbor of $i$ exactly when $i$ is a neighbor of $j$. (I2) The point $p_i$, for $i \ge 1$, was linked when it was inserted to $\min(f, i)$ distinct earlier points. (I3) As a consequence, $G$ is connected: each $p_i$ with $i \ge 1$ has a link to an earlier point, so a path leads from every point to $p_0$.

## Operations

A search keeps a min-heap $C$ of candidates to expand and a max-heap $W$ of the best $ef$ points seen, and marks the evaluated points.

```pseudo id=main
SEARCH(q, k, ef, entries)
L1  W ← ∅; mark all points as not visited
L2  for each e in entries do mark e visited and compute d(e, q)
L3      insert e into C and into W
L4  while C ≠ ∅ do
L5      c ← the point of C nearest to q; remove it from C
L6      if |W| = ef and d(c, q) > the largest distance in W then stop
L7      for each neighbor e of c that is not visited do
L8          mark e visited and compute d(e, q)
L9          if |W| < ef or d(e, q) < the largest distance in W then insert e into C and W, and if |W| > ef remove the farthest point of W
L10 return the k points of W nearest to q

INSERT(p)
L11 if the graph is empty then add p as a node with no links; return
L12 N ← SEARCH(p, f, max(ef_c, f), entries)
L13 add p as a node, and for each x in N add the undirected edge {p, x}
```

With $ef = 1$, SEARCH is greedy routing: it moves to a neighbor that is closer to $q$ than all points seen, and stops at a point none of whose neighbors improves on it, a local minimum. A larger $ef$ keeps up to $ef$ points in $W$ and expands them in order of distance, which lets the search go around such local minima. Several entry points, random ones besides $p_0$, play the role of the restarts of Malkov et al. INSERT links the new point to the $f$ nearest points that the search finds, which are often but not always its true $f$ nearest neighbors among the earlier points.

## Example

Insert, with $f = 2$ and $ef_c = 2$, the twelve points $a = (9, 5)$, $b = (9, 1)$, $c = (0, 4)$, $d = (8, 9)$, $e = (5, 4)$, $f = (2, 5)$, $g = (2, 2)$, $h = (1, 6)$, $i = (5, 2)$, $j = (6, 9)$, $k = (6, 7)$, $l = (7, 3)$ in this order, with the Euclidean distance and entry point $a$.

| point | links made at insertion | evaluations | final neighbors |
|---|---|---|---|
| a | none | 0 | b, c, d, e, j |
| b | a | 1 | a, c, d, e, i |
| c | a, b | 2 | a, b, f, g, h |
| d | a, b | 3 | a, b, j, k |
| e | a, b | 4 | a, b, f, i, l |
| f | c, e | 5 | c, e, g, h |
| g | c, f | 6 | c, f |
| h | c, f | 7 | c, f |
| i | b, e | 6 | b, e, l |
| j | a, d | 5 | a, d, k |
| k | d, j | 6 | d, j |
| l | e, i | 8 | e, i |

The early points $a$ and $b$ link far across the set: $b$ to $c$ at distance 9.4868, $a$ to $c$ at 9.0554. The late points link only to near ones.

Search for $q = (2, 9)$ with $k = 1$. The distances are $h$: 3.1623, $f$ and $j$: 4, $k$: 4.4721, $c$: 5.3852, $e$: 5.8310, $d$: 6, and more for the rest. With $ef = 1$, the search evaluates $a$ (8.0623), then its neighbors $b$, $c$, $d$, $e$, $j$; it keeps $c$ (5.3852) and then $j$ (4). It expands $j$ and evaluates $k$ (4.4721), which does not improve. Next in $C$ is $c$, at 5.3852 > 4, so it stops and returns $j$ after 7 evaluations. The point $j$ is a local minimum: its neighbors $a$, $d$ and $k$ are all farther from $q$. The true nearest point is $h$, reachable only through $c$ or $f$. With $ef = 3$, $c$ stays in $W$, the search expands it, reaches $f$ and $h$, and returns $h$ after 10 evaluations of the 12.

## Correctness

Three statements hold for every input; they are proved in [the correctness proof](proofs/correctness.md).

1. **The graph.** After any sequence of insertions, invariants (I1) to (I3) hold.
2. **The answer is the best seen.** SEARCH returns the $\min(k, |V|)$ points nearest to $q$ among the set $V$ of the points it evaluates, in order of distance.
3. **Exact with a full beam.** If $ef \ge n$, SEARCH evaluates all $n$ points and so returns the exact $k$ nearest neighbors.

Nothing better holds in the worst case: on the example, $ef = 1$ returns a point that is not the nearest. If the graph contains the [Delaunay](/delaunay-triangulation/) graph of the points, greedy search with $ef = 1$ is exact, since every point that is not the nearest neighbor of $q$ has a Delaunay neighbor closer to $q$; an NSW graph is a sparse approximation of it. Kleinberg's theorem explains why the mix of long and short links helps: on an $n \times n$ grid where each node has its four grid neighbors and one long-range link to $v$ chosen with probability proportional to $d(u, v)^{-2}$, greedy routing between any two nodes takes $O(\log^2 n)$ steps in expectation over the random links, and with exponent $r \ne 2$ instead of 2 it takes a polynomial number of steps for some pairs.

## Complexity

The model is the [real RAM](/real-ram/) with an oracle for $d$.

| operation | cost | case |
|---|---|---|
| search | at most $n$ evaluations, $O(fn + n \log n)$ time | worst; each point is evaluated once and each edge scanned at most twice |
| insert | one search plus $O(f)$ time to link | worst |
| build of $n$ points | $O(n^2)$ evaluations, $O(n^2 (f + \log n))$ time | worst |
| space | $\Theta(fn)$ | at most $f$ new edges per insertion |
| search, observed | polylogarithmic in $n$ | experiments of Malkov et al. on low-dimensional data |

A search visits each point at most once, since it marks it, and scans the neighbor set of each point it expands, at most once; the graph has at most $f(n - 1)$ edges, and the heaps hold at most $n$ entries. Malkov and Yashunin explain the polylogarithmic observed cost: the number of hops grows like $\log n$ and the degree of the visited points, mostly the old hubs, also grows like $\log n$. HNSW removes the second factor by layers.

## Variants

- **[HNSW](/hnsw/).** Each point is assigned a random level with a geometric distribution; the graph of level $\ell$ holds the points of level at least $\ell$. A search descends from the sparse top level, where links are long, to the bottom one. The degree is capped, and the links are chosen by a heuristic that prefers diverse directions. The search becomes logarithmic in practice.
- **Degree caps and pruning.** Limit the degree of each point and drop the longest links; or keep only the links that are not dominated by a shorter path, as in the [relative neighborhood graph](/relative-neighborhood-graph/). This removes hubs but can disconnect the graph unless done with care.
- **Restarts.** Malkov et al. run $m$ independent searches from random entry points and merge the results; a larger $m$ trades time for recall like a larger $ef$.
- **Graphs built in other ways.** A [k-nearest neighbor graph](/k-nearest-neighbor-graph/) built by [NN-descent](/nn-descent/), or the Vamana graph of [DiskANN](/diskann/), is searched by the same beam search; NSW differs in how its edges are chosen.
- **Deletion.** Removing a point removes its links and can disconnect the graph; implementations mark points as deleted and rebuild from time to time.

## When to use it

Use a graph index for approximate nearest neighbor search on large data sets in tens to thousands of dimensions, when a recall below 1 is acceptable and points arrive over time. In practice HNSW is preferred to plain NSW, since it has the same insertion scheme and a faster search. For exact answers in low dimension use a [k-d tree](/kd-tree/), and for exact answers in a general metric use a [metric index](/metric-space-indexing/) such as the [vantage-point tree](/vantage-point-tree/).

## Pitfalls

- **No guarantee.** A small beam can return a far point, as in the example. Measure the recall on sample queries and raise $ef$ until it is enough.
- **Order of insertion.** The long links come from the early points. Inserting the points in a sorted or clustered order, instead of a random one, gives a graph with only short links, and searches take many hops.
- **Hubs.** The first points gain links with every insertion near them, and their degree grows with $n$; each visit to them costs many evaluations.
- **Ties and duplicates.** Many points at the same distance from a query make the beam fill with equal points; break ties consistently, for example by index.
- **Clusters.** Data in well-separated clusters can leave few links between clusters, and the search from an entry point in one cluster may never reach another. Use several entry points.

## Implementations

## History

Kleinberg showed in 2000 that greedy routing finds short paths in a grid augmented with random long-range links only for a particular distribution of the link lengths, which gave the notion of a navigable small world. Malkov, Ponomarenko, Logvinov and Krylov proposed building such a graph for nearest neighbor search by inserting points in random order, in conference papers from 2012 and in Information Systems in 2014. Malkov and Yashunin's hierarchical version, HNSW, appeared as a preprint in 2016 and in IEEE Transactions on Pattern Analysis and Machine Intelligence in 2020.

## References
