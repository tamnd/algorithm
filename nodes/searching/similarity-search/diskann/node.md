---
tag: KR79N8
kind: data-structure
slug: diskann
name: DiskANN
aliases:
- Vamana
- Vamana graph
- Vamana graph
area: searching/similarity-search
level: research
summary: A graph index built with robust pruning that is stored on SSD and answers queries with few random reads.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, R: the maximum out-degree, L: the search list size, E: the time of one distance evaluation}
  time: {build_full: O(n^3 E), search: O(n R E), prune: O(n R E)}
  space: {total: O(n R + n d)}
history:
  year: 2019
  people: [Suhas Jayaram Subramanya, Devvrit, Rohan Kadekodi, Ravishankar Krishnaswamy, Harsha Vardhan Simhadri]
  note: Subramanya, Devvrit, Kadekodi, Krishnaswamy and Simhadri introduced the Vamana graph and the DiskANN system at NeurIPS 2019; Indyk and Xu proved in 2023 that the version built with full pruning gives a constant-factor approximation with greedy search.
prereqs: [approximate-nearest-neighbor-search, k-nearest-neighbor-graph, external-memory-model]
see_also: [hnsw, navigable-small-world, product-quantization, inverted-file-index, k-nearest-neighbor-graph-construction, beam-search, intrinsic-dimensionality, c-approximate-nearest-neighbor]
sources:
  - url: https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html
    title: Suhas Jayaram Subramanya, Devvrit, Rohan Kadekodi, Ravishankar Krishnaswamy and Harsha Vardhan Simhadri, DiskANN, fast accurate billion-point nearest neighbor search on a single node, Advances in Neural Information Processing Systems 32 (NeurIPS), 2019
    locator: pages 13748 to 13758 (Algorithm 1 GreedySearch, Algorithm 2 RobustPrune with the parameter α, Algorithm 3 Vamana indexing with two passes, and the SSD layout with compressed vectors in memory and beam search)
  - url: https://arxiv.org/abs/2310.19126
    title: Piotr Indyk and Haike Xu, Worst-case performance of popular approximate nearest neighbor search implementations, guarantees and limitations, NeurIPS 2023
    locator: the analysis of DiskANN with slow preprocessing, which returns an (α+1)/(α−1)-approximate nearest neighbor on data of bounded doubling dimension, and the instances on which the fast preprocessing version needs at least 0.1n steps
  - paper: doi:10.1109/TPAMI.2018.2889473
    title: Yury A. Malkov and Dmitry A. Yashunin, Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs, IEEE Transactions on Pattern Analysis and Machine Intelligence 42(4), 2020
    locator: pages 824 to 836 (the neighbor selection heuristic, the case α = 1 of robust pruning)
---

DiskANN is an [approximate nearest neighbor](/approximate-nearest-neighbor-search/) index whose core is the Vamana graph: a directed graph of bounded out-degree $R$ built with a pruning rule that keeps, for each point $p$, only out-neighbors that are not "shadowed" by a kept neighbor that is $\alpha$ times closer to them. A query is a best-first [beam search](/beam-search/) from a fixed start point. The graph and the full vectors are stored on an SSD with one node per disk block, while compressed vectors held in memory guide the search, so an index of a billion points fits on one machine with tens of gigabytes of memory. With full pruning (no degree limit), Indyk and Xu proved that greedy search returns an $\frac{\alpha + 1}{\alpha - 1}$-approximate nearest neighbor; the practical build has no such guarantee.

## In plain words

Graph indexes link each point to a few others and answer a query by walking along links toward it. The walk needs short links for its end and long links to cross the data quickly at its start.

DiskANN chooses links with one rule. A point keeps its closest candidate, then throws away all candidates that are much closer to that kept point than to itself, because the walk can reach them through the kept point. The factor $\alpha$ says what "much closer" means. With $\alpha$ above 1, fewer candidates are thrown away, and more long links remain.

The graph is too big for memory, so it lives on an SSD. Each step of the walk reads one small block from the disk. Short compressed copies of all vectors stay in memory, so the walk can choose its next step without reading the disk.

## The abstract type

A static similarity index over points $P = \{x_0, \dots, x_{n-1}\}$ in a space with a distance $\delta$ (usually Euclidean), with:

- **search**$(q, k, L)$: up to $k$ points near $q$. The answer is approximate; $L \ge k$ trades time for recall.

Insertion and deletion are variants (see Variants).

## Representation

- **The graph.** For each point $i$, a list $N_{\text{out}}(i)$ of at most $R$ indices, as in an [adjacency list](/adjacency-list/). There is one start point $s$, the medoid of the data.
- **On the SSD.** Node $i$ is stored in a fixed-size record holding the full-precision vector $x_i$ and the list $N_{\text{out}}(i)$, padded to $R$ entries. Records are aligned to disk blocks (4 KB), so reading a node is one random read.
- **In memory.** A [product quantization](/product-quantization/) code of every vector, a few dozen bytes each. The search ranks candidates with these codes, and the full vectors read from the SSD with each node are used to rank the final answers.

So memory holds $O(n)$ short codes, and the SSD holds $O(n(d + R))$ numbers. In the [external memory model](/external-memory-model/), a search that expands $V$ nodes costs $V$ block reads, or about $V/W$ rounds of $W$ reads issued together.

## Operations

```pseudo id=main
GREEDY-SEARCH(s, q, k, L)                    ▷ returns the k nearest of the list and the set V of expanded nodes
L1  𝓛 ← {s}; V ← ∅
L2  while 𝓛 \ V is not empty
L3    p ← the point of 𝓛 \ V nearest to q; V ← V ∪ {p}
L4    𝓛 ← 𝓛 ∪ N_out(p); if |𝓛| > L then keep only the L points of 𝓛 nearest to q
L5  return the k points of 𝓛 nearest to q, and V

ROBUST-PRUNE(p, V, α, R)
L6  V ← (V ∪ N_out(p)) \ {p}; N_out(p) ← ∅
L7  while V is not empty
L8    p* ← the point of V nearest to p; add p* to N_out(p)
L9    if |N_out(p)| = R then stop
L10   remove from V every p′ with α · δ(p*, p′) ≤ δ(p, p′)
```

Line L4 reads node $p$ from the disk: one random read per expanded node. Line L10 is the $\alpha$-pruning rule. With $\alpha = 1$, $p'$ is removed when it is at least as close to $p^*$ as to $p$, which is the neighbor selection heuristic of [HNSW](/hnsw/). With $\alpha > 1$ fewer points are removed, so more long edges survive.

```pseudo id=build
VAMANA(P, R, L, α)
L11 start from a random directed graph with out-degree R; s ← the medoid of P
L12 for each pass with α′ = 1, then α′ = α, and for each i in a random order: (_, V) ← GREEDY-SEARCH(s, x_i, 1, L)
L13   ROBUST-PRUNE(i, V, α′, R)
L14   for each j ∈ N_out(i): add the edge j → i
L15     if this makes |N_out(j)| > R then ROBUST-PRUNE(j, N_out(j) ∪ {i}, α′, R)
```

The nodes visited while searching for $x_i$ in the current graph are good candidates for its links: near ones from the end of the search and far ones from the start. Line L14 adds back edges, so that $x_i$ can be reached. For an index larger than memory, DiskANN partitions the data into overlapping clusters, builds a Vamana graph for each in memory, and merges the graphs.

**Full pruning.** The variant analyzed by Indyk and Xu replaces lines L11 to L15 by ROBUST-PRUNE$(i, P, \alpha, n)$ for every $i$: each point is pruned against all other points, with no degree limit.

## Example

Nine points in the plane with the Euclidean distance:

$$x_0 = (0,0),\ x_1 = (2,0),\ x_2 = (4,0),\ x_3 = (6,0),\ x_4 = (0,3),\ x_5 = (3,3),\ x_6 = (6,3),\ x_7 = (1,6),\ x_8 = (5,6).$$

The medoid, the point with the least sum of distances to the others, is $x_5 = (3, 3)$. Full pruning with $\alpha = 1.5$ gives, for example,

| point | out-neighbors |
|---|---|
| $x_0 = (0,0)$ | $(2,0), (0,3), (3,3)$ |
| $x_5 = (3,3)$ | $(0,3), (6,3), (2,0), (1,6), (5,6), (6,0)$ |
| $x_8 = (5,6)$ | $(6,3), (3,3), (1,6)$ |

Take $x_5$. Its candidates in order of distance are $(0, 3)$ and $(6, 3)$ at 3, then $(2, 0)$ and $(4, 0)$ at 3.16. After keeping $(2, 0)$, the point $(4, 0)$ is removed, since $1.5 \cdot \delta((2,0), (4,0)) = 3 \le 3.16 = \delta((3,3), (4,0))$. A walk from $x_5$ reaches $(4, 0)$ through $(2, 0)$ or $(6, 0)$.

Greedy search with $L = 1$ from $x_0$ for $q = (5.5, 5)$ expands $x_0$ (distance 7.43), moves to $x_5$ (distance 3.20), then to $x_8$ (distance 1.12), whose out-neighbors are all farther. It returns $x_8$, the true nearest point, after 3 node reads.

## Correctness

The proofs are in the proof file.

**Lemma 1 ($\alpha$-shortcut).** After ROBUST-PRUNE$(p, V, \alpha, R)$ stops because $V$ is empty, every point $x$ of the original candidate set that is not an out-neighbor of $p$ has an out-neighbor $p'$ of $p$ with $\alpha \cdot \delta(p', x) \le \delta(p, x)$. With full pruning this holds for every $x \ne p$ in $P$.

**Theorem (Indyk and Xu).** Let the graph be built by full pruning with $\alpha > 1$, and let $\delta$ be a metric. Greedy search with $L = 1$ from any start point stops at a point $p$ with
$$\delta(p, q) \le \frac{\alpha + 1}{\alpha - 1} \cdot \min_{x \in P} \delta(x, q).$$

For $\alpha = 2$ the factor is 3; for $\alpha = 1.5$ it is 5; as $\alpha \to 1$ it grows without bound, which matches the fact that the $\alpha = 1$ rule gives no guarantee. Indyk and Xu also bound the number of steps by a logarithm of the aspect ratio of the data and the out-degree in terms of the doubling dimension (see [intrinsic dimensionality](/intrinsic-dimensionality/)).

**No guarantee for the practical build.** The degree limit $R$ at line L9 and the restriction of candidates to the visited set at line L12 break Lemma 1. Indyk and Xu give instances on which the search of the practical build needs at least $0.1n$ steps before it reaches any of the 5 nearest neighbors of the query.

## Complexity

Model: real RAM where a distance evaluation costs $E$, plus a count of block reads for the SSD.

| operation | cost | notes |
|---|---|---|
| ROBUST-PRUNE$(p, V, \alpha, R)$ | $O(\lvert V \rvert R)$ evaluations | each of at most $R$ rounds scans $V$ |
| GREEDY-SEARCH | at most $n$ expansions, $O(nR)$ evaluations; one read per expansion | no better worst-case bound for the practical build |
| full pruning build | $O(n^2)$ evaluations per point, $O(n^3 E)$ in all | the version with the guarantee |
| Vamana build | $n$ searches and prunes per pass, two passes | no worst-case bound; near-linear in practice |
| space | $O(nR)$ edges, $O(nd)$ vectors on SSD, $O(n)$ short codes in memory | |

In the reported experiments, a billion-point data set with 64 GB of memory and an SSD reached more than 95% recall of the true nearest neighbor with a mean latency under 3 ms. These are measurements, not bounds.

## Variants

- **Beam width.** The SSD version expands the $W$ best unexpanded nodes of $\mathcal{L}$ together, issuing $W$ reads in parallel per round. $W = 1$ is line L3.
- **Filtered, fresh and streaming versions.** Later systems from the same group add label filters, insertion with the same pruning, and deletion with repair of the in-neighbors of the deleted points.
- **HNSW and NSG.** [HNSW](/hnsw/) uses the $\alpha = 1$ rule with a hierarchy of layers instead of a medoid start; NSG uses the same rule on an approximate [k-nearest neighbor graph](/k-nearest-neighbor-graph/). Vamana's $\alpha > 1$ makes the graph's diameter smaller, which saves SSD reads.
- **In-memory Vamana.** The same graph without the SSD layout is a competitive in-memory index.

## When to use it

- Approximate search over data sets too large for memory, on a machine with a fast SSD.
- When the number of random reads per query, not the CPU time, is the bottleneck.
- Prefer [HNSW](/hnsw/) when the data fit in memory and frequent updates are needed, and an [inverted file index](/inverted-file-index/) with quantization when memory per vector must be smallest and recall can be lower.

## Pitfalls

- **$\alpha$ too close to 1.** The graph then has few long edges, and the search makes more steps and more disk reads. Values around 1.2 are common.
- **Compressed distances.** The search ranks candidates by [product quantization](/product-quantization/) distances, which are approximate. Rank the final candidates with the full vectors read from the SSD, or recall drops.
- **Deleted points.** Removing a node without repairing the lists that point to it leaves dangling or useless edges, and recall drops over time.
- **Not a metric.** The guarantee of the theorem needs the triangle inequality. Inner-product search on the raw vectors does not satisfy it.

## Implementations

## History

Subramanya, Devvrit, Kadekodi, Krishnaswamy and Simhadri introduced the Vamana graph and the DiskANN system in 2019, with robust pruning by $\alpha$, the two-pass build and the SSD layout with compressed vectors in memory. Indyk and Xu analyzed the worst case of popular graph indexes in 2023: the version of DiskANN with full pruning has a constant approximation factor, and the fast build and other graph indexes can need a linear number of steps.

## References
