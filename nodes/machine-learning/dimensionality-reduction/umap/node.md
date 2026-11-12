---
tag: FBD238
kind: algorithm
slug: umap
name: UMAP
aliases:
- uniform manifold approximation and projection
area: machine-learning/dimensionality-reduction
level: core
summary: "Builds a weighted k nearest neighbor graph with a local bandwidth per point, then lays it out in 2 or 3 dimensions by SGD with negative sampling."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the map dimension, E: the number of epochs, s: the negative samples per edge}
  time: {worst: "O(n^2 d + n^3 + E k n s m)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Leland McInnes, John Healy, James Melville]
  note: McInnes, Healy and Melville put UMAP on arXiv in 2018 and published the umap-learn software in JOSS in the same year.
prereqs: [k-nearest-neighbor-graph, stochastic-gradient-descent, binary-search-on-real-numbers]
see_also: [t-sne, stochastic-neighbor-embedding, nn-descent, laplacian-eigenmaps, spectral-clustering, isomap, trustworthiness-and-continuity, force-directed-layout]
sources:
  - paper: "Leland McInnes, John Healy and James Melville, UMAP: Uniform manifold approximation and projection for dimension reduction, arXiv:1802.03426, 2018"
    title: McInnes, Healy and Melville 2018
    locator: "Section 2 (the fuzzy simplicial set view), Section 3 (the local bandwidths rho_i and sigma_i with the target log2(k), the fuzzy union a + b - ab, and the cross entropy layout), Section 4 (Algorithms 1 to 5: the spectral start, the curve 1/(1 + a d^(2b)) fitted from min_dist, and SGD with negative sampling) and the section on weaknesses"
  - paper: doi:10.21105/joss.00861
    title: "Leland McInnes, John Healy, Nathaniel Saul and Lukas Großberger, UMAP: Uniform Manifold Approximation and Projection, Journal of Open Source Software 3(29):861, 2018"
    locator: the umap-learn software, whose find_ab_params fits a and b on 300 points in [0, 3 spread]
  - paper: "Sebastian Damrich and Fred A. Hamprecht, On UMAP's true loss function, Advances in Neural Information Processing Systems 34 (NeurIPS 2021)"
    title: Damrich and Hamprecht 2021
    locator: the proof that SGD with negative sampling does not minimize the stated cross entropy, and the loss that it does minimize in expectation
  - paper: "Dmitry Kobak and George C. Linderman, Initialization is critical for preserving global data structure in both t-SNE and UMAP, Nature Biotechnology 39:156-157, 2021"
    title: Kobak and Linderman 2021
    locator: the global layout of UMAP comes mostly from the spectral start; t-SNE with a PCA start keeps it as well
  - paper: "Jan Niklas Böhm, Philipp Berens and Dmitry Kobak, Attraction-repulsion spectrum in neighbor embeddings, Journal of Machine Learning Research 23(95), 2022"
    title: Böhm, Berens and Kobak 2022
    locator: UMAP, t-SNE and force-directed layouts as points on one scale of attraction against repulsion
---

UMAP (uniform manifold approximation and projection) draws high-dimensional data as a map in 2 or 3 dimensions. It first builds a weighted [k nearest neighbor graph](/k-nearest-neighbor-graph/) in which each point has its own distance scale, so that every point has a neighborhood of about the same weight. It makes the graph symmetric with the *fuzzy union* $a + b - ab$, starts the map from a spectral embedding of the graph, and then moves the map points by [stochastic gradient descent](/stochastic-gradient-descent/): edges pull their two ends together, and a few points drawn at random push each other apart (negative sampling). The authors derive the graph from fuzzy simplicial sets in category theory. That theory motivates the formulas, but it gives no guarantee about the map. Many parts of the method are heuristic, and the page says which.

## In plain words

Join each point to its few nearest neighbors. Give each link a strength between 0 and 1. The nearest neighbor always gets strength 1, and the strength falls off with the extra distance beyond it, at a rate set for each point so that all points have about the same total strength. If two points link to each other with different strengths, combine them as "at least one of the two links holds".

Then draw the graph on paper. Start from a layout that follows the main shape of the graph. Pick links at random, strong links more often, and pull their ends together. Each time, also push the point away from a few random points. Stop after a fixed number of rounds, with smaller moves at the end.

## The problem

The input is $n$ points $x_1, \ldots, x_n$ with a metric $d$, the number of neighbors $k$, the map dimension $m$, a minimum map distance $\text{min\_dist} \ge 0$ and a number of epochs $E$. The output is $y_1, \ldots, y_n \in \mathbb{R}^m$.

**The graph.** Let $N_i$ be the $k$ nearest neighbors of $x_i$, without $x_i$ itself. Let $\rho_i = \min_{j \in N_i} d(x_i, x_j)$, and choose $\sigma_i > 0$ so that

$$\sum_{j \in N_i} \exp\!\Big(-\frac{\max(0,\, d(x_i, x_j) - \rho_i)}{\sigma_i}\Big) = \log_2 k.$$

The directed membership is $a_{ij} = \exp(-\max(0, d(x_i, x_j) - \rho_i)/\sigma_i)$ for $j \in N_i$ and $0$ otherwise, and the graph weight is the fuzzy union

$$w_{ij} = a_{ij} + a_{ji} - a_{ij}\, a_{ji}.$$

**The map.** The map membership of a pair at distance $\delta = \|y_i - y_j\|$ is $v(\delta) = 1/(1 + a\, \delta^{2b})$. The constants $a$ and $b$ are fitted by least squares to the curve that is 1 for $\delta \le \text{min\_dist}$ and $e^{-(\delta - \text{min\_dist})}$ for larger $\delta$. With $\text{min\_dist} = 0.1$ this gives $a \approx 1.577$ and $b \approx 0.895$. With $a = b = 1$ the curve is the Student t kernel of [t-SNE](/t-sne/).

**The cost.** UMAP aims to minimize the fuzzy set [cross entropy](/cross-entropy-loss/)

$$\mathrm{CE} = \sum_{i \ne j} \Big[ w_{ij} \ln \frac{w_{ij}}{v_{ij}} + (1 - w_{ij}) \ln \frac{1 - w_{ij}}{1 - v_{ij}} \Big].$$

The first term pulls linked pairs together; the second pushes unlinked pairs apart. Unlike t-SNE, nothing is normalized over all pairs.

## The algorithm

```pseudo id=main
UMAP(x[1..n], k, m, min_dist, E, s)
L1  for i ← 1 to n do N_i ← the k nearest neighbors of x_i;  ρ_i ← min_{j∈N_i} d(x_i, x_j)
L2      σ_i ← bisection so that Σ_{j∈N_i} exp(−max(0, d(x_i,x_j) − ρ_i)/σ_i) = log₂ k
L3      a_ij ← exp(−max(0, d(x_i,x_j) − ρ_i)/σ_i) for j ∈ N_i, else 0
L4  w_ij ← a_ij + a_ji − a_ij a_ji                       ▷ fuzzy union
L5  (a, b) ← least squares fit of 1/(1 + a δ^{2b}) to the min_dist curve
L6  y ← eigenvectors 2..m+1 of I − D^{−1/2} W D^{−1/2}, scaled to [0, 10]
L7  for e ← 0 to E − 1 do
L8      α ← 1 − e/E
L9      for each ordered pair (i, j) with w_ij > 0, with probability w_ij do
L10         g ← clip(−2ab‖y_i−y_j‖^{2(b−1)} / (1 + a‖y_i−y_j‖^{2b}) · (y_i − y_j));  y_i ← y_i + α g;  y_j ← y_j − α g
L11         repeat s times: c ← a random index; y_i ← y_i + α clip(2b / ((0.001 + ‖y_i−y_c‖²)(1 + a‖y_i−y_c‖^{2b})) · (y_i − y_c))
L12 return y
```

Line L2 is a bisection that doubles $\sigma$ until the sum passes $\log_2 k$ (the sum grows with $\sigma$), then halves the bracket. Line L6 is a [Laplacian eigenmap](/laplacian-eigenmaps/) of the graph. The clip bounds each coordinate of a step to $[-4, 4]$. The default values in umap-learn are $k = 15$, $\text{min\_dist} = 0.1$, $s = 5$, and $E = 200$ for large data or $500$ for small data.

The reference code differs from this outline in a few ways. It finds neighbors with [NN-descent](/nn-descent/) on random projection trees instead of an exact search. It counts the point itself as one of the $k$ neighbors. It visits edge $(i, j)$ every $\max w / w_{ij}$ epochs instead of with probability $w_{ij}$, and it drops edges with $w_{ij} < \max w / E$. If the graph has several connected components, it lays them out one by one.

## Example

Take the four points $x = 0, 1, 3, 7$ on a line and $k = 3$, so every point has the other three as neighbors. The target is $\log_2 3 = 1.585$.

| $i$ | $x_i$ | $\rho_i$ | $\sigma_i$ | $a_{i1}$ | $a_{i2}$ | $a_{i3}$ | $a_{i4}$ |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 2.6992 | 0 | 1 | 0.4767 | 0.1083 |
| 2 | 1 | 1 | 1.6196 | 1 | 0 | 0.5393 | 0.0456 |
| 3 | 3 | 2 | 1.1332 | 0.4138 | 1 | 0 | 0.1712 |
| 4 | 7 | 4 | 1.9828 | 0.2203 | 0.3647 | 1 | 0 |

For example, $a_{13} = \exp(-(3 - 1)/2.6992) = 0.4767$, and row 1 adds up to $1 + 0.4767 + 0.1083 = 1.585$. The outlier $x_4 = 7$ has its nearest neighbor at distance 4, but $\rho_4 = 4$ makes that link 1. Distances count only beyond the nearest neighbor, so every point is fully joined to at least one other point.

The fuzzy union gives $w_{12} = 1$, $w_{13} = 0.4767 + 0.4138 - 0.4767 \cdot 0.4138 = 0.6932$, $w_{14} = 0.3047$, $w_{23} = 1$, $w_{24} = 0.3937$ and $w_{34} = 1$. The graph is a strong path $1 - 2 - 3 - 4$ with weaker side links. The one-dimensional spectral start is $y = (0, 0.979, 7.080, 10)$, which already keeps the order of the data.

The fit at $\text{min\_dist} = 0.1$ gives $a = 1.5769$ and $b = 0.8951$. The fitted curve and its target are $0.687$ and $0.670$ at $\delta = 0.5$, $0.388$ and $0.407$ at $\delta = 1$, and $0.155$ and $0.150$ at $\delta = 2$.

## Correctness

The full proofs are below. What can be proved is local:

1. **The bandwidth.** The sum on line L2 is continuous and strictly increasing in $\sigma_i$, from the number $t$ of neighbors tied at distance $\rho_i$ up to $k$. So the equation has exactly one solution when $t < \log_2 k$, which holds for $k \ge 3$ without ties, and the bisection finds it.
2. **The fuzzy union.** $a \oplus b = 1 - (1-a)(1-b)$ is symmetric and lies between $\max(a, b)$ and $\min(1, a + b)$.
3. **The steps.** The coefficients on lines L10 and L11 are minus the gradients of $-\ln v_{ij}$ and $-\ln(1 - v_{ic})$ (the latter with $0.001$ added to the squared distance). Sampling edge $(i, j)$ with probability $w_{ij}$ makes the attractive step equal to the gradient step of $-w_{ij} \ln v_{ij}$ in expectation.

What is heuristic: the target $\log_2 k$, the shift by $\rho_i$, the fuzzy union, the curve family and $\text{min\_dist}$ are design choices. The negative samples are drawn uniformly and are not weighted by $1 - w_{ij}$, so the SGD does not follow the gradient of CE even in expectation. Damrich and Hamprecht (2021) derive the loss that it does minimize, and show that it is far from CE. The category theory in the paper (fuzzy simplicial sets and a functor to metric spaces) justifies the construction of the graph under the assumption that the data are uniform on a Riemannian manifold. It gives no bound on the error of the map, and no guarantee that the clusters or distances in the map match the data.

## Complexity

In the [real RAM](/real-ram/) model, for the version on this page:

- **The neighbors.** Exact search costs $O(n^2 d)$ time. NN-descent has no worst-case bound, but its observed cost grows only a little faster than $n$.
- **The bandwidths.** $O(k)$ per bisection round per point, so $O(n k \log(1/\epsilon))$.
- **The spectral start.** A dense eigensolver costs $O(n^3)$ and $O(n^2)$ memory. The reference code uses a sparse solver on the graph with $O(k n)$ edges.
- **The layout.** Each epoch handles $O(k n)$ edges in expectation, each with $1 + s$ moves of cost $O(m)$, so $O(E k n s m)$ in total, linear in $n$.

So with approximate neighbors and a sparse eigensolver, the total cost is close to linear in $n$, and UMAP runs faster than Barnes-Hut [t-SNE](/t-sne/) on large data.

## Properties

- **Local structure.** Near neighbors in the data stay near in the map; [trustworthiness](/trustworthiness-and-continuity/) is usually high, similar to t-SNE.
- **Global layout comes mostly from the start.** Kobak and Linderman (2021) show that the global arrangement of clusters comes mostly from the spectral start, and that t-SNE with a PCA start keeps it about as well.
- **Densities are not kept.** The local $\sigma_i$ make sparse and dense regions look alike, as in t-SNE.
- **Any metric.** Only the distances to the $k$ neighbors are used, so any metric works, and the map can have more than 3 dimensions.
- **New points.** The reference code can place new points by building their memberships to the old points and optimizing only the new map points.
- **Randomized.** The map depends on the seed and, with several threads, on the order of the updates.

## Variants and improvements

- **Supervised and semi-supervised UMAP** mix a graph built from the labels into $w$.
- **densMAP** adds a term that keeps the local density of the data in the map.
- **Parametric UMAP** trains a neural network that maps $x$ to $y$ with the same cost.
- **Other negative weights.** Böhm, Berens and Kobak (2022) place UMAP, t-SNE and [force-directed layout](/force-directed-layout/) methods on one spectrum of attraction against repulsion.
- **Exact neighbors** with a [vantage-point tree](/vantage-point-tree/) or a brute-force search for small data, or [HNSW](/hnsw/) for large data.

## When to use it

Use UMAP to look at the cluster structure of large data sets, when t-SNE is too slow, or when you need a map in more than 3 dimensions as input for a density-based clustering method. As with t-SNE, do not read cluster sizes, densities or the distances between clusters from the map. Check the result with several values of $k$ and $\text{min\_dist}$ and several seeds. To keep global distances, use [PCA](/principal-component-analysis/) or [multidimensional scaling](/multidimensional-scaling/).

## Pitfalls

- **Reading the map as a metric.** The distances in the map are not distances in the data. Small $k$ gives many small clusters, some of which come from noise.
- **Ties at the nearest distance.** If $t$ neighbors are at exactly distance $\rho_i$ and $t \ge \log_2 k$, the bandwidth equation has no solution; the bisection drives $\sigma_i$ to 0. The reference code puts a floor on $\sigma_i$ for this case.
- **$k = 2$.** Then $\log_2 k = 1$, which the sum reaches only as $\sigma_i \to 0$.
- **Duplicates.** Duplicate points give $\rho_i = 0$ and ties. Remove them first.
- **The claim of theory.** The topological construction does not make the map faithful. Treat UMAP as a heuristic with good results in practice.
- **Disconnected graphs.** The spectral start is not unique when the graph has several components, and the relative places of the components in the map mean nothing.

## Implementations

## History

McInnes, Healy and Melville put UMAP on arXiv in 2018, together with the umap-learn package described in JOSS. The method grew out of their work on topological data analysis and quickly became a standard tool for single-cell biology alongside t-SNE. Later work showed that the theory and the practice differ: the SGD does not minimize the stated cross entropy (Damrich and Hamprecht 2021), and much of the global layout comes from the spectral start (Kobak and Linderman 2021).

## References
