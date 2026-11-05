---
tag: CF4M1Y
kind: algorithm
slug: frt-tree-embedding
name: FRT tree embedding
aliases:
- Fakcharoenphol-Rao-Talwar embedding
area: graphs/tree-algorithms
level: research
summary: Randomized hierarchical decomposition giving O(log n) expected distortion tree embeddings.
solves: [metric-tree-embedding]
model: word-ram
complexity:
  vars: {n: the number of points, Δ: the ratio of the largest to the smallest non-zero distance}
  time: {build: O(n^2 log Δ), query: O(log Δ)}
  space: {extra: O(n log Δ)}
properties: {deterministic: false, recursive: false}
prereqs: [metric-space, tree-metric, metric-tree-embedding, random-permutation, low-diameter-decomposition]
see_also: [metric-tree-embedding, low-stretch-spanning-tree, low-diameter-decomposition, ultrametric, k-median-problem, oblivious-routing, k-server-problem, randomized-approximation-algorithm]
sources:
  - paper: doi:10.1016/j.jcss.2004.04.011
    title: "Jittat Fakcharoenphol, Satish Rao and Kunal Talwar, A tight bound on approximating arbitrary metrics by tree metrics, Journal of Computer and System Sciences 69(3) (2004), 485-497; conference version in STOC 2003"
    locator: the random permutation and random radius decomposition, the construction of the tree from the hierarchy, and the O(log n) bound on the expected stretch
  - paper: "Yair Bartal, Probabilistic approximation of metric spaces and its algorithmic applications, Proceedings of the 37th IEEE Symposium on Foundations of Computer Science (FOCS 1996)"
    locator: the definition of probabilistic approximation by dominating tree metrics, the O(log^2 n) bound, and the Ω(log n) lower bound
  - paper: "Yair Bartal, On approximating arbitrary metrics by tree metrics, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC 1998)"
    locator: the O(log n log log n) bound that FRT improved to O(log n)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 8 (Cuts and metrics), the section on probabilistic approximation of metrics by tree metrics, and its use for buy-at-bulk network design
---

The FRT tree embedding, after Fakcharoenphol, Rao and Talwar (2003), turns any finite [metric space](/metric-space/) on $n$ points into a random weighted tree whose leaves are the points. Distances in the tree are never shorter than in the metric, and on average over the random choices they are at most $O(\log n)$ times longer, which is the best possible factor. The tree comes from a hierarchy of partitions: at each scale $2^i$, points are grouped around centers taken in one random order, within one random radius, and the groups at each scale refine those at the scale above. Many problems that are hard on general metrics are easy on trees, so the embedding turns tree algorithms into $O(\log n)$ approximation algorithms for problems such as $k$-median and buy-at-bulk network design.

## In plain words

Picture towns on a map. You want to replace the road network by a family tree of regions, so that the distance between two towns becomes the length of the tree path between them. The tree path may be longer than the road, but never shorter.

Draw large regions first, then smaller regions inside them, then smaller still, until each town is alone. To draw the regions at one size, shuffle the towns once at the start, and let each town join the region of the first town in the shuffled list that is close enough. Each step down, the meaning of close enough is cut in half. The tree has one node per region, linked to the region just above it.

The random shuffle and the random radius make it unlikely that two nearby towns are split early. So on average the tree does not stretch distances much.

## The problem

The input is a finite metric on the points $0, 1, \ldots, n - 1$, $n \ge 1$, given as an $n \times n$ matrix $d$: $d(x, x) = 0$, $d(x, y) = d(y, x) > 0$ for $x \ne y$, and $d(x, z) \le d(x, y) + d(y, z)$. A graph with positive edge weights gives such a metric through its shortest-path distances.

The output is a tree $T$, rooted and with positive edge weights, together with a map $leaf$ from the points to distinct leaves of $T$. Write $d_T(x, y)$ for the weighted length of the tree path between $leaf(x)$ and $leaf(y)$. The tree must be

- *dominating*: $d_T(x, y) \ge d(x, y)$ for every pair, on every run, and
- *of low expected stretch*: $\mathbf{E}[d_T(x, y)] \le \alpha \cdot d(x, y)$ for every pair, where the expectation is over the random choices of the algorithm.

This is the [metric tree embedding](/metric-tree-embedding/) problem, and FRT achieves $\alpha = O(\log n)$. The tree has internal nodes that are not points, so it is a [tree metric](/tree-metric/) on a larger set; since all leaves are at depth $\delta$ and the edge weights depend only on the level, the distances between leaves form an [ultrametric](/ultrametric/). Tree nodes are numbered in order of creation, root first.

## The algorithm

Scale so that the smallest distance is 1: let $d_{\min}$ and $d_{\max}$ be the smallest and largest distances between distinct points, and let $\delta \ge 1$ be the smallest integer with $2^\delta d_{\min} \ge d_{\max}$ (and $\delta = 0$ if $n = 1$). Choose a uniformly random order $\pi$ of the points and a number $\beta$ uniform in $[1, 2)$. At level $i$ the radius is $\beta_i = \beta \cdot 2^{i-1}$, in units of $d_{\min}$.

```pseudo id=main
FRT(d)
L1  compute d_min, d_max and δ
L2  choose a random order π of the points and β uniform in [1, 2)
L3  make the root at level δ; node(x) ← root for every point x
L4  for i ← δ - 1 down to 0 do
L5      r ← β · 2^(i-1) · d_min
L6      for each point x do c(x) ← the first w in π with d(w, x) ≤ r
L7          if no child of node(x) has center c(x) then add one, at level i, with an edge of weight 2^(i+1) · d_min
L8          node(x) ← the child of node(x) with center c(x)
L9  leaf(x) ← node(x) for every point x; return the tree and leaf
```

A node at level $i$ is a *cluster*: the points that share a parent cluster and the same center $c(x)$ at level $i$. Line L6 always finds a center, since $x$ itself is within distance $0 \le r$ of $x$. Different clusters with the same center are possible when the center is in another parent cluster; they are kept apart because line L7 looks only at the children of $node(x)$.

At level 0 the radius is $\beta/2 \cdot d_{\min} < d_{\min}$, so every point is its own center and the leaves are single points. The edges from level $i + 1$ to level $i$ weigh $2^{i+1} d_{\min}$, so all leaves are at the same depth and the edge weights halve going down. Queries walk up from both leaves together, in $O(\delta)$ steps.

## Example

Take five points on a line at positions $0, 1, 3, 7, 8$, so $d(x, y)$ is the difference of positions. Then $d_{\min} = 1$, $d_{\max} = 8$ and $\delta = 3$. Take $\pi = (2, 0, 4, 1, 3)$ and $\beta = 1.5$.

| level $i$ | radius $\beta_i$ | centers $c(0), \ldots, c(4)$ | clusters | edge weight to the parent |
|---|---|---|---|---|
| 3 | | | $\{0, 1, 2, 3, 4\}$ (the root) | |
| 2 | 3 | 2, 2, 2, 4, 4 | $\{0, 1, 2\}$, $\{3, 4\}$ | 8 |
| 1 | 1.5 | 0, 0, 2, 4, 4 | $\{0, 1\}$, $\{2\}$, $\{3, 4\}$ | 4 |
| 0 | 0.75 | 0, 1, 2, 3, 4 | $\{0\}$, $\{1\}$, $\{2\}$, $\{3\}$, $\{4\}$ | 2 |

At level 2, point 2 comes first in $\pi$ and is within 3 of points 0, 1 and 2; point 0 is next in $\pi$ but every point within 3 of it has already been claimed by 2, and point 4 claims 3 and 4. At level 1, point 0 is no longer within 1.5 of point 2, so its first center in $\pi$ is itself. The tree is

```
{0,1,2,3,4}
├── 8 ── {0,1,2}
│        ├── 4 ── {0,1}
│        │        ├── 2 ── {0}
│        │        └── 2 ── {1}
│        └── 4 ── {2}
│                 └── 2 ── {2}
└── 8 ── {3,4}
         └── 4 ── {3,4}
                  ├── 2 ── {3}
                  └── 2 ── {4}
```

and the tree distances are

| pair | 0,1 | 0,2 | 1,2 | 3,4 | 0,3 | 2,3 | 1,4 |
|---|---|---|---|---|---|---|---|
| $d$ | 1 | 3 | 2 | 1 | 7 | 4 | 7 |
| $d_T$ | 4 | 12 | 12 | 4 | 28 | 28 | 28 |

Every pair separated just below level $\ell$ has $d_T = 2(2 + 4 + \cdots + 2^{\ell}) = 2^{\ell+2} - 4$. All tree distances dominate the line distances. The worst stretch in this run is $28/4 = 7$, for points 2 and 3, which were split at the top level although they are only 4 apart; another order $\pi$ or radius $\beta$ would usually keep them together longer.

**Small cases.** A single point gives a tree with one node and no edges. Two points at distance $D$ give $\delta = 1$, a root and two leaves, and $d_T = 4D$. On a path metric $0, 1, \ldots, n - 1$ (points at unit spacing, $n \ge 3$) the tree has $\delta = \lceil \lg(n - 1) \rceil$ levels below the root. On a star metric, a center at distance 1 from $n - 1$ leaves that are 2 apart, $\delta = 1$ and the tree is a star of $n$ leaves with edges of weight 2, so center-leaf pairs are stretched by 4 and leaf-leaf pairs by 2.

## Correctness

The proof file has the details. The steps:

1. **The hierarchy is well defined.** Line L6 always finds a center, and each level partitions every cluster of the level above, so the clusters form a tree.
2. **Leaves are single points.** At level 0 the radius is below $d_{\min}$.
3. **Dominance.** If $x$ and $y$ are in one cluster at level $\ell$ and in different clusters at level $\ell - 1$, then $d_T(x, y) = (2^{\ell+2} - 4)\, d_{\min}$. A cluster at level $\ell < \delta$ lies within $\beta_\ell d_{\min}$ of its center, so $d(x, y) \le 2\beta_\ell d_{\min} < 2^{\ell+1} d_{\min}$; at the root, $d(x, y) \le d_{\max} \le 2^\delta d_{\min}$. In both cases $d(x, y) \le d_T(x, y)$, since $\ell \ge 1$.
4. **Expected stretch.** Fix $x \ne y$ and sort all points $w_1, w_2, \ldots, w_n$ by $\min(d(w, x), d(w, y))$. If $x$ and $y$ are split at level $i$, the first point $w$ in $\pi$ within $\beta_i$ of $x$ or $y$ is within $\beta_i$ of one of them but not the other. For $w = w_s$ this needs $\beta_i$ in an interval of length at most $d(x, y)$, and $w_s$ before $w_1, \ldots, w_{s-1}$ in $\pi$, which has probability $1/s$. A split at level $i$ costs at most $2^{i+3}$, and $\beta_i$ is uniform on $[2^{i-1}, 2^i)$, so the levels together contribute at most $16\, d(x, y)$ per $s$. Summing over $s$ gives $\mathbf{E}[d_T(x, y)] \le 16 H_n \cdot d(x, y)$, where $H_n = 1 + 1/2 + \cdots + 1/n \le 1 + \ln n$.

## Complexity

Line L1 reads the matrix in $O(n^2)$ time. The loop of lines L4 to L8 runs $\delta = O(\log \Delta)$ times, where $\Delta = d_{\max} / d_{\min}$ is the aspect ratio, and each run scans $\pi$ for each point, $O(n^2)$ time. So the build takes $O(n^2 \log \Delta)$ time, and the input itself is $\Theta(n^2)$ numbers. Each level adds at most $n$ nodes, so the tree has $O(n \log \Delta)$ nodes and the extra space is $O(n \log \Delta)$. A distance query walks up at most $\delta$ levels.

Contracting each chain of nodes with one child into a single edge, whose weight is the sum, keeps all leaf distances and leaves $O(n)$ nodes. The bound on the stretch does not depend on $\Delta$.

## Properties

- **Dominance always, stretch in expectation.** Dominance holds on every run; only the stretch is a bound in expectation. A single run can stretch some pair by a lot, as the pair 2, 3 in the example.
- **Tight.** Bartal showed that some $n$-point metrics, such as the shortest-path metrics of expander graphs, need expected stretch $\Omega(\log n)$ for any distribution over dominating trees, so FRT is optimal up to the constant.
- **Hierarchically well separated.** Edge weights halve at each level and all leaves are at the same depth, so $T$ is a 2-HST in Bartal's sense, and its leaf distances form an ultrametric.
- **Not a subgraph.** The tree has new internal nodes and its edges need not be edges of any input graph. Trees made of graph edges are [low-stretch spanning trees](/low-stretch-spanning-tree/), with stretch $O(\log n \log \log n)$ on average over the edges.
- **Non-recursive.** The implementation uses loops only.

## Variants and improvements

- **The original density for $\beta$.** FRT choose $\beta$ in $[1, 2]$ with density $1/(x \ln 2)$, which makes the radius at each scale log-uniform and gives a constant smaller than 16. The uniform choice used here gives the simpler bound $16 H_n$.
- **From graphs, in near-linear time.** For a graph with $m$ edges, the same tree can be built without the distance matrix, by running a Dijkstra-like search from the points in the order $\pi$; later work brings the time near $O(m \log n)$.
- **Bartal's ball carving.** Bartal (1996) built the hierarchy by cutting balls of random radius with an exponential-like distribution, one cluster at a time, with stretch $O(\log^2 n)$, improved to $O(\log n \log \log n)$ in 1998. FRT's single permutation for all levels is what removes the extra factor.
- **[Low-diameter decompositions](/low-diameter-decomposition/).** One level of the hierarchy is a random partition into clusters of diameter at most $2^{i+1}$ that splits each pair with probability $O(\log n \cdot d(x, y) / 2^i)$; any such decomposition can be stacked into a tree in the same way.
- **Few trees.** Since the guarantee is in expectation, it can be met by a distribution over a small number of trees, which can be found deterministically; this is enough for many approximation algorithms.

## When to use it

Use it when a problem on a general metric has a simple exact or good algorithm on trees and its cost is a sum of distances with non-negative coefficients: then solving the problem on $T$ and mapping the solution back loses $O(\log n)$ in expectation. Examples include [$k$-median](/k-median-problem/), buy-at-bulk network design, group Steiner tree, [oblivious routing](/oblivious-routing/), and online problems such as metrical task systems and the [$k$-server problem](/k-server-problem/). Do not use it when an $O(1)$ factor is needed, when distances must be kept almost exactly (the stretch of a single pair in one run can be large), or when the tree must use the edges of the input graph.

## Pitfalls

- **Global centers, local clusters.** A point may be the center of clusters in several parent clusters. Keying the clusters only by center merges points from different parents and breaks the hierarchy; line L7 keys them by parent and center.
- **One permutation and one radius for all levels.** Drawing a new $\pi$ or $\beta$ at each level loses the analysis: the event "$w_s$ before $w_1, \ldots, w_{s-1}$" is shared by all levels only when $\pi$ is.
- **Including $\beta = 2$.** At level 0 the radius must stay below $d_{\min}$; with $\beta = 2$ two points at distance $d_{\min}$ can share a leaf, and dominance fails for them.
- **Too few levels.** With $n \ge 2$ there must be at least one level below the root even when all distances are equal; otherwise all points share the root as a leaf.
- **Expecting a good tree from one run.** The bound is on the expected stretch of each pair, not on the worst pair of one tree. Algorithms that use FRT either average over runs or need only expected costs.
- **Floating point.** Rounding in $\beta \cdot 2^{i-1}$ can decide a tie $d(w, x) = r$ either way. Ties have probability zero for a random $\beta$, and either outcome gives a valid hierarchy, so this affects only which tree is chosen.

## Implementations

## History

Probabilistic approximation of metrics by trees grew from the work of Alon, Karp, Peleg and West (1995) on random spanning trees for the $k$-server problem on graphs. Bartal (1996) defined the problem, proved the $\Omega(\log n)$ lower bound, and gave $O(\log^2 n)$ expected stretch, later improved to $O(\log n \log \log n)$ (1998). Fakcharoenphol, Rao and Talwar closed the gap at STOC 2003, with the journal version in 2004: one random permutation and one random scale suffice for $O(\log n)$. Their result became the standard way to reduce problems on metrics to problems on trees, and appears in textbooks on approximation algorithms such as Williamson and Shmoys.

## References
