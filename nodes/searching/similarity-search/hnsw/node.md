---
tag: ZFDM4P
kind: data-structure
slug: hnsw
name: Hierarchical navigable small world
aliases:
- HNSW
area: searching/similarity-search
level: advanced
summary: A multilayer navigable small world graph whose sparse upper layers guide greedy search in the dense bottom layer.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of elements, M: the number of links per element on the upper layers, M0: the largest number of links on layer 0, ef: the beam width of a search, E: the time of one distance evaluation}
  time: {insert: O(n E), search: O(n E)}
  space: {total: O(n M0)}
history:
  year: 2016
  people: [Yury A. Malkov, Dmitry A. Yashunin]
  note: Malkov and Yashunin put a navigable small world graph into layers with geometrically decreasing sizes, in the manner of a skip list, in a preprint of 2016 published in IEEE TPAMI in 2020; it became the most used graph index for vector search.
prereqs: [navigable-small-world, skip-list, approximate-nearest-neighbor-search]
see_also: [diskann, nn-descent, k-nearest-neighbor-graph, relative-neighborhood-graph, beam-search, small-world-network, inverted-file-index, product-quantization]
sources:
  - paper: doi:10.1109/TPAMI.2018.2889473
    title: Yury A. Malkov and Dmitry A. Yashunin, Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs, IEEE Transactions on Pattern Analysis and Machine Intelligence 42(4), 2020
    locator: pages 824 to 836 (Algorithms 1 to 5, insertion, SEARCH-LAYER, the two neighbor selection rules and K-NN-SEARCH; the level rule with m_L = 1/ln M; the parameters M, M_max0 = 2M, efConstruction and ef)
  - paper: doi:10.1016/j.is.2013.10.006
    title: Yury Malkov, Alexander Ponomarenko, Andrey Logvinov and Vladimir Krylov, Approximate nearest neighbor algorithm based on navigable small world graphs, Information Systems 45, 2014
    locator: pages 61 to 68 (the single-layer navigable small world graph built by inserting elements and linking them to their nearest found neighbors)
  - paper: doi:10.1145/78973.78977
    title: William Pugh, Skip lists, a probabilistic alternative to balanced trees, Communications of the ACM 33(6), 1990
    locator: pages 668 to 676 (levels drawn with a geometric law, which HNSW reuses for its layers)
  - url: https://arxiv.org/abs/2310.19126
    title: Piotr Indyk and Haike Xu, Worst-case performance of popular approximate nearest neighbor search implementations, guarantees and limitations, NeurIPS 2023
    locator: the instances on which HNSW and NSG need a number of steps linear in n to return a good answer
---

A hierarchical navigable small world graph (HNSW) is an index for [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) made of several layers of proximity graphs. Every element is on layer 0, and each element also appears on layers $1, 2, \dots, \ell$ for a random top level $\ell$ with $\Pr[\ell \ge j] = M^{-j}$, as in a [skip list](/skip-list/). A search walks greedily through the sparse top layers to find a good entry point and then runs a [beam search](/beam-search/) of width $ef$ on layer 0. Elements are inserted one at a time by the same search, and each new element is linked to up to $M$ neighbors found on each of its layers. There is no worst-case guarantee better than $O(n)$ distance evaluations per query, but in practice HNSW reaches recall above 0.95 with a few hundred to a few thousand evaluations on millions of vectors. Malkov and Yashunin introduced it in 2016.

## In plain words

Picture several maps of the same city. The bottom map shows every house, each linked to a few houses near it. Each higher map shows fewer houses, picked at random, also linked to near ones; the top map has only a handful.

To find the house closest to an address, start on the top map and keep moving to a linked house that is closer, until no link helps. Then drop to the next map at the same house and do it again. On the bottom map, keep a short list of the best houses seen and explore their links until the list stops getting better. The coarse maps make long jumps cheap, and the bottom map finds the fine answer.

## The abstract type

HNSW implements a [similarity index](/similarity-index/) for a set of elements of a space with a distance $\delta$: `insert(x)` and `search(q, k, ef)`, which returns $k$ elements, nearest first, and is expected but not guaranteed to return the true $k$ nearest. The parameter $ef \ge k$ sets the trade between speed and recall. The index uses only distance evaluations, so it works for any distance; in practice it is used with the Euclidean distance, inner product, and cosine.

## Representation

Each element $i$ has a top level $\ell_i$ and, for each layer $l = 0, \dots, \ell_i$, a list $N_l(i)$ of neighbor ids. The index keeps an entry point $e$, an element of the highest level $L = \ell_e$.

- **Nesting.** If $j \in N_l(i)$, then $\ell_j \ge l$: links on layer $l$ join elements that are on layer $l$.
- **Degree bound.** $|N_l(i)| \le M$ for $l \ge 1$ and $|N_0(i)| \le M_0$, usually $M_0 = 2M$.
- **Levels.** $\ell_i = \lfloor -\ln U_i \cdot m_L \rfloor$ with $U_i$ uniform in $(0, 1]$ and $m_L = 1/\ln M$.

Links are directed lists. They are added in both directions at insertion, but a list that grows past its bound is cut, so the graph need not be symmetric.

## Operations

The core is a beam search on one layer, from a set of entry points.

```pseudo id=main
SEARCH-LAYER(q, E, ef, l)                   ▷ returns up to ef nearest elements found on layer l
L1  V ← E; C ← E as a min-heap by δ(q, ·); W ← E as a max-heap by δ(q, ·), cut to ef elements
L2  while C is not empty do
L3      c ← extract the nearest element of C
L4      if δ(q, c) > δ(q, the farthest element of W) then break
L5      for each e ∈ N_l(c) with e ∉ V do add e to V
L6          if |W| < ef or δ(q, e) < δ(q, farthest of W) then add e to C and W; if |W| > ef remove the farthest from W
L7  return W, nearest first

K-NN-SEARCH(q, k, ef)
L8  E ← {entry point}; for l ← L down to 1 do E ← {the nearest element of SEARCH-LAYER(q, E, 1, l)}
L9  W ← SEARCH-LAYER(q, E, max(ef, k), 0)
L10 return the k nearest elements of W
```

Line L4 stops the search when the nearest unexpanded candidate is farther than every element of the result, so no expansion can improve $W$ in one step. On the upper layers, $ef = 1$ makes SEARCH-LAYER a greedy walk. Line L9 is the beam search that does the real work.

**Insertion** finds the neighbors of the new element with the same search and links it on each of its layers.

```pseudo id=insert
INSERT(x)
L11 ℓ ← ⌊−ln U · m_L⌋ for U uniform in (0, 1]
L12 E ← {entry point}; for l ← L down to ℓ + 1 do E ← {the nearest element of SEARCH-LAYER(x, E, 1, l)}
L13 for l ← min(L, ℓ) down to 0 do
L14     W ← SEARCH-LAYER(x, E, efConstruction, l); N_l(x) ← SELECT(x, W, M); add x to N_l(e) for each e ∈ N_l(x)
L15     for each e ∈ N_l(x) with |N_l(e)| above its bound do N_l(e) ← SELECT(e, N_l(e), bound)
L16     E ← W
L17 if ℓ > L then the entry point ← x; L ← ℓ
```

SELECT$(x, W, m)$ can keep the $m$ elements of $W$ nearest to $x$ (the simple rule), or use the **heuristic**: scan $W$ from nearest to farthest and keep $e$ only if $\delta(x, e) < \delta(e, s)$ for every $s$ already kept, until $m$ are kept. The heuristic keeps links in several directions, in the spirit of the [relative neighborhood graph](/relative-neighborhood-graph/), and is the rule that makes clustered data searchable.

## Example

Take eight points in the plane with $M = 2$, $M_0 = 3$, efConstruction $= 4$, the simple selection rule, and these levels:

| id | point | level |
|---|---|---|
| 0 | (0, 0) | 2 |
| 1 | (4, 0) | 0 |
| 2 | (8, 1) | 1 |
| 3 | (1, 5) | 0 |
| 4 | (5, 6) | 1 |
| 5 | (9, 5) | 0 |
| 6 | (2, 9) | 0 |
| 7 | (7, 9) | 0 |

Inserting them in this order gives layer 2 = $\{0\}$ with no links, layer 1 with links $0 \to \{2, 4\}$, $2 \to \{0, 4\}$, $4 \to \{2, 0\}$, and on layer 0, for example, $N_0(4) = \{7, 3, 5\}$. Query $q = (6, 7)$ with $k = 1$ and $ef = 2$:

1. Layer 2: the entry point 0 has no links, so the walk stays at 0.
2. Layer 1, greedy from 0 at distance 9.22: its neighbors are 2 at 6.32 and 4 at 1.41. The walk moves to 4, whose neighbors are already seen, and stops. Entry for layer 0: 4.
3. Layer 0, beam of width 2 from 4 at 1.41: the neighbors are 7 at 2.24, 3 at 5.39 and 5 at 3.61. $W = \{4, 7\}$; 3 and 5 are farther than everything in a full $W$ and are not kept. Expanding 7 adds nothing new. The search ends.

The answer is element 4, $(5, 6)$, at distance $\sqrt 2$, which is the true nearest neighbor. The search computed distances to 6 of the 8 points.

## Correctness

HNSW is approximate: a search can miss the nearest neighbor if the walk gets stuck in a region of the graph from which no link leads closer. Three things can be proved.

**SEARCH-LAYER keeps the best visited.** At each step $W$ holds the $\min(ef, |V|)$ elements of $V$ nearest to $q$ that have been offered, and every element of $C$ is in $V$. The loop ends, since each element enters $C$ at most once.

**Levels.** $\Pr[\ell \ge j] = \Pr[U \le M^{-j}] = M^{-j}$. So layer $j$ holds $n M^{-j}$ elements in expectation, and an element is on $1/(1 - 1/M)$ layers in expectation.

**An exact limit.** If no list on layer 0 is ever cut ($M_0 \ge n - 1$) and $ef \ge n$, K-NN-SEARCH returns the exact $k$ nearest neighbors. Without cuts the layer-0 links are symmetric and each new element links to at least one earlier one, so layer 0 is connected; with $ef \ge n$ nothing leaves $W$, line L4 never fires, and the search visits every element. The proofs are in `proofs/correctness.md`. This limit is useless for speed, but it shows that the recall loss comes only from cut lists and a small beam.

## Complexity

The model is the [real RAM](/real-ram/) with a distance oracle of cost $E$.

- **Space.** Layer 0 has at most $M_0$ links per element and each upper layer at most $M$. With the expected $1/(M-1)$ upper layers per element, the expected total is at most $n(M_0 + M/(M-1))$ links: $O(n M_0)$ ids besides the vectors.
- **Search, worst case.** SEARCH-LAYER evaluates each element at most once per call, so a search costs at most $n$ evaluations per layer, $O(n E)$ in total for a bounded number of layers. Indyk and Xu built inputs on which HNSW needs a number of steps linear in $n$ to return a good answer. No sublinear worst-case bound is known.
- **Search, in practice.** On real data of low or moderate intrinsic dimension, Malkov and Yashunin report a number of distance evaluations that grows about logarithmically in $n$ for a fixed recall. This is an empirical claim.
- **Insert.** One search with beam efConstruction per layer, plus the cuts of line L15, each of which costs $O(M_0^2)$ distances with the heuristic. In the worst case $O(nE)$ per insertion.

| operation | distance evaluations | case |
|---|---|---|
| search$(q, k, ef)$ | $O(n)$ | worst |
| search$(q, k, ef)$ | about $O(ef \cdot M_0 \log n)$ | empirical, real data |
| insert | $O(n)$ | worst |
| space | $O(n M_0)$ links | expected |

## Variants

- **One layer.** The [navigable small world](/navigable-small-world/) graph is HNSW with all elements on layer 0; the layers add a cheap way to find a good entry point.
- **Disk-resident graphs.** [DiskANN](/diskann/) builds one flat graph with a pruning rule that has a parameter $\alpha > 1$ and keeps compressed vectors in memory, so that a search reads few disk pages.
- **Graphs from k-NN graphs.** [NN-descent](/nn-descent/) builds an approximate [k-nearest neighbor graph](/k-nearest-neighbor-graph/) that can serve as layer 0.
- **Quantized vectors.** Store [product quantization](/product-quantization/) codes for the distance estimates in the search, and rerank with full vectors.
- **Deletion.** Mark elements deleted and skip them in results, then repair or rebuild; true deletion needs relinking of the neighbors.

## When to use it

Use HNSW for in-memory vector search at high recall, from thousands to hundreds of millions of vectors, when queries must be fast and inserts happen online. It is the default index of many vector databases. Its costs are memory, about $M_0$ ids per vector besides the vectors, a slower build than an [inverted file index](/inverted-file-index/), and no guarantee per query. For data on disk, use [DiskANN](/diskann/); for a guarantee, use [LSH](/locality-sensitive-hashing/); for small sets, an exact scan.

## Pitfalls

- **Too small an $ef$.** The beam must be at least $k$; recall rises steeply with $ef$ at first. Tune $ef$ on held-out queries.
- **The simple selection rule on clustered data.** Keeping only the nearest $M$ links can leave clusters with no links between them, and searches then fail to leave the first cluster. Use the heuristic.
- **Expecting exact results.** Recall below 1 is normal; measure it against a [brute-force scan](/brute-force-nearest-neighbor-search/) on a sample.
- **Insert order and duplicates.** Many equal vectors fill the neighbor lists with each other; deduplicate or break ties.
- **Memory for large $M$.** $M = 16$ to 48 is typical; larger values help only for hard, high-dimensional data and cost memory and build time.

## Implementations

## History

Malkov, Ponomarenko, Logvinov and Krylov built navigable small world graphs for search by inserting elements and linking them to their nearest found neighbors, in a paper of 2014. Malkov and Yashunin added the layers of a skip list and the heuristic neighbor selection in a preprint of 2016, published in IEEE TPAMI in 2020. Indyk and Xu studied its worst case in 2023.

## References
