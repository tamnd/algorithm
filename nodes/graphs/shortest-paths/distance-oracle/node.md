---
tag: 99Y3F8
kind: problem
slug: distance-oracle
name: Approximate distance oracle
aliases:
- distance oracle
- distance query data structure
area: graphs/shortest-paths
level: advanced
summary: Preprocess a graph into a compact structure that answers distance queries quickly, possibly approximately.
prereqs: [all-pairs-shortest-paths, single-pair-shortest-path, shortest-path]
see_also: [thorup-zwick-oracle, distance-labeling, hub-labeling, contraction-hierarchies, alt-algorithm, planar-graph, dynamic-all-pairs-shortest-paths, hopset]
sources:
  - paper: doi:10.1145/1044731.1044732
    title: Mikkel Thorup and Uri Zwick, Approximate distance oracles, Journal of the ACM 52(1), 1 to 24 (2005)
    locator: the whole paper (stretch 2k − 1 with O(k n^{1+1/k}) space and O(k) query time, and the lower bound from the girth conjecture)
  - paper: doi:10.1145/2591796.2591801
    title: Shiri Chechik, Approximate distance oracles with constant query time, STOC 2014, 654 to 663
    locator: the whole paper (stretch 2k − 1, O(n^{1+1/k}) space and O(1) query time)
  - paper: doi:10.1137/11084128x
    title: Mihai Pătraşcu and Liam Roditty, Distance oracles beyond the Thorup-Zwick bound, SIAM Journal on Computing 43(1), 300 to 311 (2014)
    locator: the whole paper (for unweighted graphs, estimates at most 2d + 1 with O(n^{5/3}) space; for weighted graphs with n²/α edges, stretch 2 with O(n²/α^{1/3}) space; and conditional lower bounds)
  - paper: doi:10.1145/1039488.1039493
    title: Mikkel Thorup, Compact oracles for reachability and approximate distances in planar digraphs, Journal of the ACM 51(6), 993 to 1024 (2004)
    locator: the whole paper ((1 + ε)-approximate distance oracles for planar graphs with O(n log n / ε) space and fast queries)
  - paper: doi:10.1145/3313276.3316316
    title: Panagiotis Charalampopoulos, Paweł Gawrychowski, Shay Mozes and Oren Weimann, Almost optimal distance oracles for planar graphs, STOC 2019, 138 to 151
    locator: the whole paper (exact oracles for planar graphs with n^{1+o(1)} space and n^{o(1)} query time)
---

A distance oracle is a data structure built from a graph that answers queries "how far is $u$ from $v$?" quickly, using much less space than the full table of [all-pairs distances](/all-pairs-shortest-paths/). An *approximate* oracle of stretch $\alpha$ may return any value $\hat d(u, v)$ with $\operatorname{dist}(u, v) \le \hat d(u, v) \le \alpha \cdot \operatorname{dist}(u, v)$. The two extreme oracles are the $n \times n$ table, with $\Theta(n^2)$ space and $O(1)$ query time, and the graph itself, with $O(m)$ space and a full [single-pair](/single-pair-shortest-path/) search per query. The central result is the [Thorup-Zwick oracle](/thorup-zwick-oracle/) (2005): for every integer $k \ge 1$, stretch $2k - 1$ with $O(k n^{1 + 1/k})$ space and $O(k)$ query time on undirected graphs, which is optimal in space if a conjecture of Erdős on graphs of high girth holds.

## In plain words

Answering "how far apart are these two places?" is easy if you write down every answer in advance, but for a million places that is a trillion numbers. It is also easy if you keep only the map and search every time, but then each answer is slow.

A distance oracle is something in between: a smaller set of notes, prepared once, from which any answer comes out fast. The price of small notes is usually accuracy. A stretch-3 oracle may say 30 km when the truth is 10 km, but never less than the truth and never more than three times it.

The question is how small the notes can be for a given accuracy and answer time. For road maps and other special maps one can do much better than for arbitrary networks.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges and a weight on each edge, and a stretch $\alpha \ge 1$.

**Task.** Build a data structure $\mathcal{O}$ that, for each query $(u, v)$, returns $\hat d(u, v)$ with $\operatorname{dist}(u, v) \le \hat d(u, v) \le \alpha \cdot \operatorname{dist}(u, v)$, and in particular $\hat d(u, v) = \infty$ exactly when $\operatorname{dist}(u, v) = \infty$. An *exact* oracle has $\alpha = 1$. The measures are the space in words, the query time, and the preprocessing time.

**Weight assumptions.** The approximate oracles are for undirected graphs with nonnegative real weights; zero weights are fine. With negative weights, multiplicative stretch makes no sense for negative distances, and with a negative cycle distances are $-\infty$; such inputs are outside the problem. For directed graphs, no oracle with $o(n^2)$ space and bounded stretch exists in general, since even reachability needs $\Omega(n^2)$ bits on some graphs; special directed classes such as planar digraphs have good oracles. Unreachable pairs, that is pairs in different components, are reported as $\infty$, which an oracle can do in $O(1)$ by storing a component number per vertex.

## Variants

- **Exact oracles** for special classes: [planar graphs](/planar-graph/), graphs of bounded treewidth, graphs with small separators.
- **Additive stretch.** Return $\operatorname{dist}(u, v) \le \hat d \le \operatorname{dist}(u, v) + \beta$, usually for unweighted graphs.
- **Mixed stretch.** Bounds of the form $\alpha \operatorname{dist}(u, v) + \beta$.
- **Labeling.** The oracle is split into one [label](/distance-labeling/) per vertex, and a query reads only the two labels.
- **Path reporting.** Also return a path whose weight is $\hat d$.
- **Dynamic oracles.** Support edge insertions and deletions, as in [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/).
- **Vertex-fault-tolerant oracles.** Answer distances avoiding a failed vertex or edge, related to [replacement paths](/replacement-paths/).
- **Engineering versions.** [Contraction hierarchies](/contraction-hierarchies/), [hub labels](/hub-labeling/) and [ALT](/alt-algorithm/) are exact oracles for road networks, judged by experiments rather than worst-case bounds.

## Examples

**Thorup-Zwick with $k = 2$ on a 6-cycle.** The vertices $0, \ldots, 5$ form a cycle with unit weights. The oracle samples a set $A_1$, here $\{0, 3\}$. Each vertex $v$ stores its nearest sampled vertex $p(v)$ and its *bunch* $B(v)$, the vertices closer to $v$ than $p(v)$ together with all of $A_1$, with their distances:

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $p(v)$ | 0 | 0 | 3 | 3 | 3 | 0 |
| $B(v)$ | $\{0, 3\}$ | $\{0, 1, 3\}$ | $\{0, 2, 3\}$ | $\{0, 3\}$ | $\{0, 3, 4\}$ | $\{0, 3, 5\}$ |

The query $(u, v)$ returns $\operatorname{dist}(u, v)$ if $u \in B(v)$. Otherwise it takes $w = p(v)$, which lies in $B(u)$ because every bunch contains $A_1$, and returns $\operatorname{dist}(u, w) + \operatorname{dist}(w, v)$, both read from the stored tables (for larger $k$ the query climbs more levels). For $(1, 2)$, at distance 1: $1 \notin B(2)$, so take $w = p(2) = 3$, and return $\operatorname{dist}(2, 3) + \operatorname{dist}(3, 1) = 1 + 2 = 3$. That is stretch exactly 3, the worst allowed. For $(2, 4)$, at distance 2: $w = p(4) = 3$ gives $1 + 1 = 2$, exact. The bunches have 16 entries; on large graphs with $A_1$ a random sample of about $\sqrt n$ vertices, the expected total is $O(n^{3/2})$.

**Unreachable pairs.** Add an isolated vertex 6. It is in no bunch of another vertex and no sampled vertex is near it; the oracle stores a component number per vertex and answers $\infty$ for every query $(6, v)$ with $v \ne 6$, without looking at bunches.

**The two extremes.** For a road network of $n = 10^7$ vertices, the full table needs $10^{14}$ entries, which is far too much, while a [Dijkstra](/dijkstra/) query reads millions of vertices. Contraction hierarchies take a few times the graph size and answer in under a millisecond, exactly.

## Known algorithms

| oracle | graphs | stretch | space | query |
|---|---|---|---|---|
| full table (APSP) | any | 1 | $n^2$ | $O(1)$ |
| no preprocessing ([Dijkstra](/dijkstra/)) | nonnegative weights | 1 | $O(m)$ | $O(m + n \log n)$ |
| [Thorup-Zwick](/thorup-zwick-oracle/) 2005 | undirected | $2k - 1$ | $O(k n^{1 + 1/k})$ | $O(k)$ |
| Chechik 2014 | undirected | $2k - 1$ | $O(n^{1 + 1/k})$ | $O(1)$ |
| Pătraşcu and Roditty 2010 | undirected, unweighted | $2d + 1$ for distance $d$ | $O(n^{5/3})$ | $O(1)$ |
| Thorup 2004 | planar (also directed) | $1 + \varepsilon$ | $O(n \log n / \varepsilon)$ | $O(\log\log \Delta + 1/\varepsilon)$, $O(1/\varepsilon)$ undirected |
| Charalampopoulos, Gawrychowski, Mozes and Weimann 2019 | planar, directed | 1 | $n^{1 + o(1)}$ | $n^{o(1)}$ |

Thorup-Zwick preprocessing takes $O(k m n^{1/k})$ expected time. In the planar row, $\Delta$ is the largest finite distance.

## Bounds

- **Space lower bound for stretch.** For stretch less than $2k + 1$, any oracle needs $\Omega(n^{1 + 1/k})$ bits on some graph, provided that Erdős's girth conjecture holds (there are graphs with $\Omega(n^{1 + 1/k})$ edges and girth $2k + 2$). The argument: on such a graph, every subgraph is a different graph, and an oracle of stretch below $2k + 1$ can tell whether each edge is present, so it must distinguish $2^{\Omega(n^{1 + 1/k})}$ graphs. The conjecture is proved for $k = 1, 2, 3, 5$.
- **Stretch below 3.** Any oracle of stretch less than 3 needs $\Omega(n^2)$ bits on some graphs (dense bipartite graphs, girth 4), so stretch 3 is the first point where subquadratic space is possible for general graphs. Pătraşcu and Roditty get below $n^2$ with stretch 2 when the graph has $n^2/\alpha$ edges, using $O(n^2/\alpha^{1/3})$ space, and with the mixed bound $2d + 1$ on unweighted graphs.
- **Exact oracles.** For general graphs, exact distances need $\Omega(n^2)$ bits, as in [distance labeling](/distance-labeling/).

## Reductions

- **From spanners.** A graph spanner of stretch $\alpha$ with $s$ edges is an oracle of stretch $\alpha$ with $O(s)$ space and a shortest-path query; Thorup-Zwick improves the query to $O(k)$.
- **From labeling.** A distance labeling scheme with labels of $\ell$ bits is an oracle of $n \ell$ bits.
- **Lower bounds from set intersection.** Conditional lower bounds for oracles with small query time come from set-intersection and set-disjointness conjectures (Pătraşcu and Roditty).

## Applications

- **Route planning.** Exact oracles for road networks are the core of navigation services.
- **Network routing.** Compact routing schemes keep small tables at each router and route along paths of bounded stretch, an oracle distributed over the nodes.
- **Social networks.** Fast approximate distances for search ranking and recommendations.
- **Algorithms.** Oracles speed up algorithms that need many distance queries, such as approximate shortest-path trees and metric embeddings.

## References
