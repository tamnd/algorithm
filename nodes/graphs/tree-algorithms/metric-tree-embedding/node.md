---
tag: 2HCVPK
kind: problem
slug: metric-tree-embedding
name: Metric tree embedding
aliases:
- probabilistic tree embedding
area: graphs/tree-algorithms
level: research
summary: Embed a finite metric into a tree metric with bounded expected distortion.
prereqs: [metric-space, tree-metric, embedding]
see_also: [frt-tree-embedding, low-stretch-spanning-tree, ultrametric, low-diameter-decomposition, k-median-problem, oblivious-routing, k-server-problem, steiner-tree-problem]
sources:
  - paper: doi:10.1016/j.jcss.2004.04.011
    title: Jittat Fakcharoenphol, Satish Rao and Kunal Talwar, A tight bound on approximating arbitrary metrics by tree metrics, Journal of Computer and System Sciences 69(3), 485 to 497 (2004)
    locator: the O(log n) upper bound on the expected distortion, matching the known lower bound
  - paper: Yair Bartal, Probabilistic approximation of metric spaces and its algorithmic applications, Proceedings of the 37th IEEE Symposium on Foundations of Computer Science (FOCS 1996)
    locator: the definition of probabilistic approximation by dominating tree metrics, hierarchically well-separated trees, the O(log^2 n) bound and the Ω(log n) lower bound
  - paper: Noga Alon, Richard M. Karp, David Peleg and Douglas West, A graph-theoretic game and its application to the k-server problem, SIAM Journal on Computing 24(1), 78 to 100 (1995)
    locator: random spanning trees of a graph with bounded expected stretch, the cycle example, and the lower bound for grids
  - paper: Yuri Rabinovich and Ran Raz, Lower bounds on the distortion of embedding finite metric spaces in graphs, Discrete and Computational Geometry 19(1), 79 to 94 (1998)
    locator: the lower bound of order n on the distortion of the n-cycle in any tree metric
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 8 (Cuts and metrics), the section on probabilistic approximation of metrics by tree metrics and its applications
---

The metric tree embedding problem asks to replace a finite metric space by a tree, so that the distances in the tree are close to the original ones. A single tree can be bad: the points of a cycle need distortion of order $n$ in every tree. But a *random* tree, drawn from a well-chosen distribution, can keep every distance within a factor $O(\log n)$ in expectation while never making a distance shorter. Bartal defined this probabilistic form in 1996, and Fakcharoenphol, Rao and Talwar reached the tight bound $O(\log n)$ in 2003 with the [FRT embedding](/frt-tree-embedding/). The result turns many problems on general metrics, such as [$k$-median](/k-median-problem/), buy-at-bulk network design and [online Steiner tree](/online-steiner-tree-problem/), into problems on trees, at the cost of an $O(\log n)$ factor.

## In plain words

You have some cities and the road distances between all pairs. Many questions are easy if the roads form a tree, because then there is only one route between two cities. So you would like to draw a tree whose distances are close to the real ones.

You cannot always do this well with one tree. Picture cities on a ring road. Any tree must cut the ring somewhere, and two neighbours at the cut become far apart.

The way out is to choose the tree at random. Each time, the cut falls in a different place, so a given pair of neighbours is far apart only rarely. On average, every pair is close to its true distance. The best possible factor is about the logarithm of the number of cities.

## Definition

**Input.** A finite metric space $(X, d)$ with $n$ points, numbered $0, \ldots, n-1$, given by the matrix of distances, or by a connected graph with non-negative edge lengths whose shortest-path distances define $d$. The input is weighted and not rooted.

**Trees.** A *tree metric* on $X$ is given by a tree $T$ with non-negative edge lengths whose vertex set contains $X$, possibly with extra (Steiner) vertices, and $d_T$ is the length of the path in $T$. The tree $T$ *dominates* $d$ if $d_T(x, y) \ge d(x, y)$ for all $x, y \in X$.

**Deterministic version.** Find a dominating tree $T$ with the least distortion $\max_{x \ne y} d_T(x, y) / d(x, y)$.

**Probabilistic version.** Find a probability distribution $\mathcal{D}$ over dominating trees, and a way to sample from it, such that for all $x, y \in X$

$$\mathbb{E}_{T \sim \mathcal{D}}[d_T(x, y)] \le \alpha \cdot d(x, y),$$

with the least possible $\alpha$, the *expected distortion* or *expected stretch*. In the spanning-tree form, $d$ is the metric of a graph $G$ and each tree must be a spanning tree of $G$, with the edge lengths of $G$; this is the [low-stretch spanning tree](/low-stretch-spanning-tree/) problem.

## Variants

- **Deterministic distortion.** One tree for all pairs. The cycle shows that the best distortion can be of order $n$.
- **Probabilistic distortion.** A distribution over trees. Every metric on $n$ points has one with $\alpha = O(\log n)$, and this is tight.
- **Ultrametrics and HSTs.** Restrict the trees to *hierarchically well-separated trees*, rooted trees whose edge lengths drop by a factor of at least $k$ at each level. These define [ultrametrics](/ultrametric/), and the FRT trees are of this kind with $k = 2$.
- **Spanning trees of a graph.** The trees must be subgraphs. The best known bound is $O(\log n \log \log n)$ expected stretch, a little above the $O(\log n)$ for general trees.
- **Steiner points.** Allowing extra vertices does not help much: Gupta showed that Steiner vertices can be removed from a tree embedding while losing only a constant factor.
- **Exact recognition.** Whether $d$ is a tree metric, with distortion $1$, is decided by the [four-point condition](/four-point-condition/), and the tree is then found by [tree metric](/tree-metric/) reconstruction.

## Examples

| metric | best deterministic distortion | best expected distortion |
|---|---|---|
| a single point | 1 | 1 |
| the shortest-path metric of a path or of a star | 1 | 1 |
| any tree metric | 1 | 1 |
| the $n$-cycle with unit edges | of order $n$ | at most $2(n-1)/n < 2$ |
| the $n \times n$ grid, $N = n^2$ points | of order $n$ | of order $\log N$ |
| a constant-degree expander on $n$ points | at least of order $\log n$ | of order $\log n$ |

**The cycle.** Take the cycle $C_n$ on the points $0, \ldots, n-1$ with unit edges. Deleting the edge $\{i, i+1\}$ gives a path, a spanning tree that dominates $d$, in which $i$ and $i + 1$ are at distance $n - 1$, so its distortion is $n - 1$. Now delete an edge chosen uniformly at random. For two neighbours $x, y$, the tree distance is $1$ with probability $(n - 1)/n$ and $n - 1$ with probability $1/n$, so

$$\mathbb{E}[d_T(x, y)] = \frac{n - 1}{n} + \frac{n - 1}{n} = \frac{2(n - 1)}{n}.$$

A pair at distance $j \le n/2$ has its shortest path cut with probability $j/n$, and then has distance $n - j$, so $\mathbb{E}[d_T] = (1 - j/n) j + (j/n)(n - j) = 2j(n - j)/n$. Its expected stretch $2(n - j)/n$ is less than $2$. For $n = 4$, neighbours have expected distance $3/2$ and opposite points have distance $2$ in every such tree.

## Known algorithms

| algorithm | expected distortion | trees |
|---|---|---|
| random edge deletion (Karp) | less than $2$ | cycles only |
| Alon, Karp, Peleg and West (1995) | $\exp(O(\sqrt{\log n \log \log n}))$ | spanning trees |
| Bartal (1996) | $O(\log^2 n)$ | HSTs |
| Bartal (1998) | $O(\log n \log \log n)$ | HSTs |
| [FRT](/frt-tree-embedding/) (2003) | $O(\log n)$ | 2-HSTs |
| Elkin, Emek, Spielman and Teng (2005) | $O(\log^2 n \log \log n)$ | spanning trees |
| Abraham and Neiman (2012) | $O(\log n \log \log n)$ | spanning trees |

The FRT algorithm picks a random permutation of the points and a random scale, and cuts the space into clusters of geometrically shrinking diameters, a hierarchical [low-diameter decomposition](/low-diameter-decomposition/). The tree has one level per scale. It runs in $O(n^2 \log \Delta)$ time for a distance matrix, where $\Delta$ is the ratio of the largest to the smallest non-zero distance, and faster on sparse graphs.

## Bounds

- **Upper bound.** $O(\log n)$ expected distortion for every metric on $n$ points, by FRT.
- **Lower bound.** $\Omega(\log n)$: for constant-degree expanders, and for grids, every distribution over dominating trees has expected stretch of order $\log n$ on some edge. So $\Theta(\log n)$ is tight.
- **Deterministic lower bound.** Rabinovich and Raz showed that every tree metric that dominates the $n$-cycle has distortion of order $n$ on some pair, so the probabilistic form is needed.
- **Averaging.** By the minimax theorem, a distribution with expected stretch $\alpha$ for every pair exists if and only if, for every non-negative weighting $c$ of the pairs, some single dominating tree has $\sum c(x, y) d_T(x, y) \le \alpha \sum c(x, y) d(x, y)$. This is the form used in many proofs.

## Reductions

- **Optimization on metrics to optimization on trees.** Let a problem have a linear cost in the distances, such as [$k$-median](/k-median-problem/) or buy-at-bulk design. Solve it exactly or well on a random tree from the distribution, and use the solution in the original metric. Since trees dominate, the cost does not grow when going back; since the expected tree cost of the optimum is at most $\alpha$ times its true cost, the result is an $O(\alpha \cdot \beta)$ approximation in expectation, where $\beta$ is the ratio achieved on trees.
- **Online problems.** Online problems on trees are often easier, so the same reduction gives $O(\log n)$-competitive randomized algorithms for some online problems on metrics, such as metrical task systems and the [$k$-server problem](/k-server-problem/) on some metrics, against an oblivious adversary.
- **Routing.** Oblivious routing schemes for general graphs are built from distributions over trees, as in [oblivious routing](/oblivious-routing/).

## Applications

- Approximation algorithms for buy-at-bulk network design, group Steiner tree, $k$-median and minimum communication cost spanning trees.
- Online algorithms for metrical task systems, the $k$-server problem and the [online Steiner tree](/online-steiner-tree-problem/).
- Fast solvers for symmetric diagonally dominant linear systems, which use [low-stretch spanning trees](/low-stretch-spanning-tree/) as preconditioners.
- Distance labelling and approximate distance oracles, where a tree gives short labels and fast queries.

## References
