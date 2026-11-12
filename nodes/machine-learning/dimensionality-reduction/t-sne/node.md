---
tag: 5T99ZY
kind: algorithm
slug: t-sne
name: t-SNE
aliases:
- t-distributed stochastic neighbor embedding
- Barnes-Hut t-SNE
area: machine-learning/dimensionality-reduction
level: core
summary: "Symmetric SNE with a Student t kernel of one degree of freedom in the map, which relieves crowding; fitted by gradient descent, mainly to draw 2D maps of data."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, m: the map dimension, t: the number of gradient steps}
  time: {worst: "O(n^2 d + n^2 t m)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Laurens van der Maaten, Geoffrey Hinton]
  note: Van der Maaten and Hinton published t-SNE in JMLR in 2008. Van der Maaten added the Barnes-Hut tree method in 2014.
prereqs: [stochastic-neighbor-embedding, gradient-descent, momentum-method]
see_also: [umap, quadtree, vantage-point-tree, k-nearest-neighbor-graph, trustworthiness-and-continuity, principal-component-analysis, laplacian-eigenmaps, multidimensional-scaling]
sources:
  - paper: "Laurens van der Maaten and Geoffrey Hinton, Visualizing data using t-SNE, Journal of Machine Learning Research 9:2579-2605, 2008"
    title: van der Maaten and Hinton 2008
    locator: "Section 3.1 (symmetric SNE and p_ij = (p_j|i + p_i|j)/2n), Section 3.2 (the crowding problem), Section 3.3 (equations 4 and 5: the Student t kernel and the gradient), Section 3.4 (Algorithm 1, early exaggeration 4 for 50 steps, momentum 0.5 then 0.8 after step 250, learning rate 100 with Jacobs gains, 1000 steps) and Appendix A (the gradient)"
  - paper: "Laurens van der Maaten, Accelerating t-SNE using tree-based algorithms, Journal of Machine Learning Research 15:3221-3245, 2014"
    title: van der Maaten 2014
    locator: "the sparse input affinities on the nearest neighbors found with a vantage-point tree, and the Barnes-Hut approximation of the repulsive forces on a quadtree, O(n log n) per step"
  - paper: doi:10.23915/distill.00002
    title: "Martin Wattenberg, Fernanda Viégas and Ian Johnson, How to use t-SNE effectively, Distill, 2016"
    locator: the effect of the perplexity and of the number of steps, and the warnings that cluster sizes and the distances between clusters in a t-SNE map may mean nothing
  - paper: "Dmitry Kobak and Philipp Berens, The art of using t-SNE for single-cell transcriptomics, Nature Communications 10:5416, 2019"
    title: Kobak and Berens 2019
    locator: the start from PCA instead of a random start, for better global structure and repeatable maps
  - paper: "George C. Linderman and Stefan Steinerberger, Clustering with t-SNE, provably, SIAM Journal on Mathematics of Data Science 1(2), 2019"
    title: Linderman and Steinerberger 2019
    locator: the early exaggeration phase on well-separated clustered data contracts each cluster in the map
  - paper: "Sanjeev Arora, Wei Hu and Pravesh K. Kothari, An analysis of the t-SNE algorithm for data visualization, Proceedings of COLT 2018, PMLR 75"
    title: Arora, Hu and Kothari 2018
    locator: a proof that t-SNE with early exaggeration separates well-separated, spherical clusters in the map
---

t-SNE is a method that draws high-dimensional data as a map of points in 2 or 3 dimensions so that points that are near in the data are near in the map. It changes [stochastic neighbor embedding](/stochastic-neighbor-embedding/) in two ways: it uses one symmetric distribution over all pairs, and it measures map similarity with a Student t kernel of one degree of freedom, $(1 + \|y_i - y_j\|^2)^{-1}$, whose heavy tail fixes the *crowding problem* of SNE. The map minimizes a Kullback-Leibler divergence by [gradient descent](/gradient-descent/) with [momentum](/momentum-method/) and *early exaggeration*. The exact method costs $O(n^2 m)$ per step; the Barnes-Hut method of van der Maaten (2014) costs $O(n \log n)$. The cost is not convex, and the sizes of clusters and the gaps between them in a t-SNE map are not reliable measures of the data.

## In plain words

Give each pair of data points a weight. Close pairs get a large weight and far pairs a tiny one, and the reach around each point is tuned so that every point has about the same number of real neighbors. Then put the points at random on a sheet of paper and give each pair a weight from its distance on the paper.

Now pull pairs that are too light on the paper together and push pairs that are too heavy apart, many times. The paper weights fall off slowly with distance. So a pair that is only a bit far apart in the data can sit quite far apart on the paper at small cost. This leaves room on the paper, and groups of points come out as separate islands.

The islands show which points belong together. Their sizes and gaps mean little.

## The problem

The input is $n$ points $x_1, \ldots, x_n \in \mathbb{R}^d$, a map dimension $m$ (2 or 3) and a perplexity $u$ (typical values are 5 to 50). The output is a map $y_1, \ldots, y_n \in \mathbb{R}^m$.

First compute the SNE conditionals $p_{j|i}$, with each Gaussian width $\sigma_i$ set by bisection so that $2^{H(P_i)} = u$ (see [stochastic neighbor embedding](/stochastic-neighbor-embedding/)). Then make them symmetric:

$$p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}, \qquad p_{ii} = 0.$$

In the map, use the Student t kernel with one degree of freedom (the Cauchy kernel):

$$q_{ij} = \frac{(1 + \|y_i - y_j\|^2)^{-1}}{\sum_{k \ne l} (1 + \|y_k - y_l\|^2)^{-1}}, \qquad q_{ii} = 0.$$

t-SNE minimizes the single [Kullback-Leibler divergence](/cross-entropy-loss/)

$$C(y) = \mathrm{KL}(P \,\|\, Q) = \sum_{i \ne j} p_{ij} \ln \frac{p_{ij}}{q_{ij}},$$

whose gradient is

$$\frac{\partial C}{\partial y_i} = 4 \sum_{j \ne i} (p_{ij} - q_{ij})(y_i - y_j)(1 + \|y_i - y_j\|^2)^{-1}.$$

The factor $(1 + \|y_i - y_j\|^2)^{-1}$ makes the forces fall off with distance, so far clusters act on each other like single points.

## The algorithm

```pseudo id=main
T-SNE(x[1..n], m, u, T, η, e, T_e)
L1  compute p_{j|i} for all i, j with perplexity u        ▷ bisection per row, as in SNE
L2  p_ij ← (p_{j|i} + p_{i|j}) / 2n
L3  y_i ← a draw from N(0, 10⁻⁴ I_m);  v_i ← 0;  g_i ← (1, …, 1) for each i
L4  for t ← 1 to T do
L5      c ← e if t ≤ T_e else 1                         ▷ early exaggeration
L6      w_ij ← (1 + ‖y_i − y_j‖²)⁻¹;  q_ij ← w_ij / Σ_{k≠l} w_kl
L7      ∇_i ← 4 Σ_j (c·p_ij − q_ij) w_ij (y_i − y_j) for each i
L8      α ← 0.5 if t < 250 else 0.8                     ▷ momentum
L9      for each coordinate: gain ← gain + 0.2 if sign(∇) ≠ sign(v) else max(0.8·gain, 0.01)
L10     v_i ← α v_i − η (gain ⊙ ∇_i);  y_i ← y_i + v_i
L11 return y
```

These are the settings of the paper (Section 3.4): $e = 4$ for the first $T_e = 50$ steps, momentum $0.5$ before step 250 and $0.8$ after, the step size $\eta = 100$ at the start with the adaptive gains of Jacobs (1988) in line L9, and $T = 1000$ steps. In the experiments of the paper the data were first reduced to 30 dimensions with [PCA](/principal-component-analysis/), and the perplexity was 40.

**Early exaggeration.** Lines L5 and L7 multiply all $p_{ij}$ by $e$ for the first steps. Since the $q_{ij}$ still add up to 1, they cannot match the large $p_{ij}$, so the method forms tight clusters with a lot of empty space between them, and the clusters can move past each other to find a good global layout.

### Barnes-Hut t-SNE

Van der Maaten (2014) made each step cost $O(n \log n)$:

- **Sparse input affinities.** Compute $p_{j|i}$ only over the $\lfloor 3u \rfloor$ nearest neighbors of $x_i$, found with a [vantage-point tree](/vantage-point-tree/), and set the other entries to 0. $P$ is then a sparse [k-nearest neighbor graph](/k-nearest-neighbor-graph/).
- **Split the gradient.** Write $\partial C / \partial y_i = 4 (F_{\text{attr}} + F_{\text{rep}})$ with $F_{\text{attr}} = \sum_j p_{ij} q_{ij} Z (y_i - y_j)$ and $F_{\text{rep}} = -\sum_j q_{ij}^2 Z (y_i - y_j)$, where $Z = \sum_{k \ne l} w_{kl}$. The attractive part has only $O(u n)$ nonzero terms.
- **Approximate the repulsion.** Build a [quadtree](/quadtree/) on the map points (an octree in 3D). For point $i$, treat a whole cell as one point at its center of mass when the cell is small compared with its distance, that is when $r_{\text{cell}} / \|y_i - y_{\text{cell}}\| < \theta$. This is the Barnes-Hut method of N-body simulation. $Z$ is estimated in the same pass. $\theta = 0$ gives the exact sum, and larger $\theta$ is faster and less exact.

## Example

Take the four points $x = 0, 1, 3, 7$ of the SNE example with perplexity $u = 2$. The conditionals give the joint affinities

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 0.1575 | 0.0694 | 0.0097 |
| 2 | 0.1575 | 0 | 0.1409 | 0.0222 |
| 3 | 0.0694 | 0.1409 | 0 | 0.1002 |
| 4 | 0.0097 | 0.0222 | 0.1002 | 0 |

For example, $p_{12} = (0.6559 + 0.6041)/8 = 0.1575$. Each row adds up to more than $1/(2n) = 0.125$, so the outlier $x_4$ keeps the weight $0.1321$.

At the map $y = x/2 = (0, 0.5, 1.5, 3.5)$, the Student t affinities are $q_{12} = 0.2017$, $q_{13} = 0.0776$, $q_{14} = 0.0190$, $q_{23} = 0.1261$, $q_{24} = 0.0252$ and $q_{34} = 0.0504$, with $C = 0.0570$ nats. The gradient is $(0.0956, -0.0968, -0.0649, 0.0662)$. Here $q_{34} = 0.0504 < p_{34} = 0.1002$: under the heavy tail, the outlier is too far away, so the step pulls it in. SNE on the same map pushed it out (see the SNE example). One-dimensional t-SNE with $\eta = 10$ and the other settings above ends, from a seeded start, at $y \approx (0.077, -1.188, -2.610, -4.587)$ with $C \approx 0.0175$. The map keeps the order, and the gaps $1.265$, $1.422$ and $1.977$ grow with the data gaps $1$, $2$ and $4$, but much more slowly.

**Why the heavy tail helps.** Compare two map distances, 1 and 3. Under the SNE kernel the ratio of the weights is $e^{-1} / e^{-9} = e^8 \approx 2981$. Under the t kernel it is $(1 + 9)/(1 + 1) = 5$. So t-SNE can place a moderately far pair much farther apart in the map at a small cost, and the crowded middle of an SNE map opens up.

## Correctness

The full proofs are below.

1. **The joint affinities.** $p_{ij} = p_{ji}$, the $p_{ij}$ add up to 1, and $\sum_j p_{ij} > 1/(2n)$ for each $i$. The last fact keeps every point, outliers included, in the cost.
2. **The gradient.** Write $\ln q_{ij} = -\ln(1 + d_{ij}) - \ln Z$ with $d_{ij} = \|y_i - y_j\|^2$. Then $C$ is a constant plus $\sum_{i \ne j} p_{ij} \ln(1 + d_{ij}) + \ln Z$, and the derivative of each part gives $4 \sum_j p_{ij} w_{ij} (y_i - y_j)$ and $-4 \sum_j q_{ij} w_{ij} (y_i - y_j)$.
3. **Early exaggeration** is exact gradient descent on a different function, $e \sum p_{ij} \ln(1 + d_{ij}) + \ln Z$, not on $C$.

There is no guarantee of a global minimum. $C$ is not convex, and different seeds give different maps. Partial results exist: Arora, Hu and Kothari (2018) and Linderman and Steinerberger (2019) prove that, for data made of well-separated clusters, the early exaggeration phase gathers each cluster into its own small region of the map.

## Complexity

In the [real RAM](/real-ram/) model:

- **Exact t-SNE.** The affinities cost $O(n^2 d)$ for the distances and $O(n^2)$ per bisection round. Each step costs $O(n^2 m)$. In total $O(n^2 d + n^2 t m)$ time and $O(n^2)$ memory, on every input.
- **Barnes-Hut t-SNE.** The neighbor search costs $O(u n \log n)$ expected time with a vantage-point tree (an observed bound; the tree has no worst-case guarantee in high dimension). Each step costs $O(u n)$ for the attraction and $O(n \log n)$ for the repulsion when the map points are spread out, with $O(n)$ memory for the tree and $O(u n)$ for $P$.

## Properties

- **Local structure first.** Near neighbors in the data stay near in the map; [trustworthiness](/trustworthiness-and-continuity/) is usually high.
- **Cluster sizes are not kept.** The bandwidth adapts to the local density, so a dense cluster and a sparse cluster come out at about the same size (Wattenberg, Viégas and Johnson 2016).
- **Gaps between clusters are not reliable.** The heavy tail stretches moderate distances by an amount that depends on the perplexity and on the run.
- **Not parametric.** t-SNE returns positions. It has no map for new points.
- **Randomized.** The map depends on the seed. Fix it, or start from PCA, to repeat a run.

## Variants and improvements

- **Barnes-Hut t-SNE** (above), the default in most libraries.
- **Interpolation methods.** FIt-SNE computes the repulsion on a grid with the fast Fourier transform, which is faster for large $n$.
- **PCA start.** Starting from the first two principal components, scaled down, keeps more of the global layout and gives the same map on each run (Kobak and Berens 2019).
- **Other degrees of freedom.** For a map with more than 3 dimensions, a t kernel with more degrees of freedom suits better; the paper discusses this as a weakness of the one-degree kernel.
- **Parametric t-SNE.** Train a neural network that maps $x$ to $y$ with the same cost, so that new points can be mapped.
- **UMAP.** [UMAP](/umap/) builds a weighted neighbor graph and fits it with a different cost and with negative sampling. Its maps look similar and it is often faster.

## When to use it

Use t-SNE to look at the cluster structure of data with a few thousand to a few million points, for example images, word vectors or single-cell gene data. Run it with several perplexities and seeds. Do not use the map as features for a later model, and do not read distances, densities or cluster sizes from it. To keep global distances, use [PCA](/principal-component-analysis/) or [multidimensional scaling](/multidimensional-scaling/).

## Pitfalls

- **Reading the gaps and the sizes.** Two clusters far apart in the map may be close in the data, and a large cluster may be a sparse one. Wattenberg, Viégas and Johnson (2016) show maps of this kind on simple synthetic data.
- **Shapes from noise.** With a small perplexity, uniform random data can show small clumps that are not in the data.
- **Too few steps.** A map that is stopped early can show pinched shapes. Run until the map no longer changes.
- **Perplexity close to n.** The perplexity must be less than $n - 1$, and for the tree method $\lfloor 3u \rfloor$ must be less than $n$.
- **Learning rate.** With a fixed $\eta = 100$, a map of many points can stall. Scale the learning rate with $n$.
- **The sign in the update.** Algorithm 1 of the paper writes $+\eta\,\partial C/\partial y$; the step must go down the gradient.

## Implementations

## History

Van der Maaten and Hinton published t-SNE in 2008, as symmetric SNE with a heavy-tailed kernel in the map. They named the crowding problem and showed maps of handwritten digits, faces and objects. Van der Maaten (2014) made it scale to millions of points with a vantage-point tree for the input and the Barnes-Hut method for the forces. Wattenberg, Viégas and Johnson (2016) wrote a widely read guide to the misreadings of t-SNE maps.

## References
