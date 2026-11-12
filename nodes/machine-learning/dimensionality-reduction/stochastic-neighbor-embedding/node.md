---
tag: WVHAJS
kind: algorithm
slug: stochastic-neighbor-embedding
name: Stochastic neighbor embedding
aliases:
- SNE
- asymmetric SNE
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Place points in a low-dimensional map so that Gaussian neighbor probabilities there match those of the data, by gradient descent on a sum of KL divergences."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, m: the map dimension, t: the number of gradient steps}
  time: {worst: "O(n^2 d + n^2 t m)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [Geoffrey Hinton, Sam Roweis]
  note: Hinton and Roweis presented SNE at NIPS 2002. It is the direct ancestor of t-SNE (2008).
prereqs: [shannon-entropy, gradient-descent, binary-search-on-real-numbers]
see_also: [t-sne, umap, multidimensional-scaling, locally-linear-embedding, isomap, self-organizing-map, cross-entropy-loss, trustworthiness-and-continuity]
sources:
  - paper: doi:10.5555/2968618.2968725
    title: "Geoffrey Hinton and Sam Roweis, Stochastic neighbor embedding, Advances in Neural Information Processing Systems 15 (NIPS 2002), MIT Press, 2003"
    locator: "pp. 857 to 864; Section 2 (equations 1 to 5: the conditional probabilities, the perplexity set by binary search, the cost and its gradient, jitter), Section 3 (perplexity 15 and 25 in the experiments) and Section 4 (the mixture version)"
  - paper: "Laurens van der Maaten and Geoffrey Hinton, Visualizing data using t-SNE, Journal of Machine Learning Research 9:2579-2605, 2008"
    title: van der Maaten and Hinton 2008
    locator: "Section 2 (SNE restated, perplexity as 2 to the power H in bits, momentum and annealed noise) and Section 3.2 (the crowding problem)"
  - paper: "Laurens van der Maaten, Accelerating t-SNE using tree-based algorithms, Journal of Machine Learning Research 15:3221-3245, 2014"
    title: van der Maaten 2014
    locator: "Sections 2 and 3 (the exact O(n^2) cost per step, sparse input affinities from nearest neighbors, and the tree approximation of the gradient)"
---

Stochastic neighbor embedding (SNE) turns the distances around each data point into a probability distribution over the other points, and then places the points in a map of low dimension $m$ (usually 2) so that the same construction in the map gives similar distributions. The mismatch is a sum of [Kullback-Leibler divergences](/cross-entropy-loss/), one for each point, and SNE lowers it by [gradient descent](/gradient-descent/). The width of the Gaussian around each point is set by a [bisection search](/binary-search-on-real-numbers/) so that every point has the same *perplexity*, a smooth count of its effective neighbors. The exact method costs $O(n^2 m)$ time per step; its cost function is not convex, and its maps suffer from the *crowding problem* that [t-SNE](/t-sne/) was designed to fix.

## In plain words

Each data point picks a neighbor at random. Near points are much more likely picks than far points. This gives each point a list of chances, one for each other point.

Now put the points on a sheet of paper and make the same lists from the positions on the paper. If a point's chances on paper are close to its chances in the data, its near neighbors stay near. SNE moves the points on the paper, a little at a time, to make the two sets of lists agree.

Some points sit in crowded regions and some in empty ones. So each point gets its own "reach", tuned until it has about the same number of likely neighbors as every other point. The user sets that number.

## The problem

The input is $n$ points $x_1, \ldots, x_n \in \mathbb{R}^d$ (or a matrix of dissimilarities), a map dimension $m$ and a target perplexity $u$ with $1 < u < n - 1$. The output is a map $y_1, \ldots, y_n \in \mathbb{R}^m$.

In the input space, point $i$ picks $j$ with the conditional probability

$$p_{j|i} = \frac{\exp\big(-\|x_i - x_j\|^2 / 2\sigma_i^2\big)}{\sum_{k \ne i} \exp\big(-\|x_i - x_k\|^2 / 2\sigma_i^2\big)}, \qquad p_{i|i} = 0.$$

The perplexity of row $i$ is $\mathrm{Perp}(P_i) = 2^{H(P_i)}$, where $H(P_i) = -\sum_j p_{j|i} \log_2 p_{j|i}$ is the [Shannon entropy](/shannon-entropy/) in bits. Each $\sigma_i$ is chosen so that $\mathrm{Perp}(P_i) = u$. In the map, the Gaussian has the fixed variance $\tfrac12$:

$$q_{j|i} = \frac{\exp(-\|y_i - y_j\|^2)}{\sum_{k \ne i} \exp(-\|y_i - y_k\|^2)}.$$

SNE minimizes

$$C(y) = \sum_{i=1}^{n} \mathrm{KL}(P_i \,\|\, Q_i) = \sum_{i} \sum_{j \ne i} p_{j|i} \ln \frac{p_{j|i}}{q_{j|i}}.$$

$C$ is asymmetric in its effect. A small $q_{j|i}$ for a large $p_{j|i}$ (near points placed far apart) costs a lot. A large $q_{j|i}$ for a small $p_{j|i}$ (far points placed near) costs little. So SNE keeps local structure first. Its gradient is

$$\frac{\partial C}{\partial y_i} = 2 \sum_{j \ne i} \big(p_{j|i} - q_{j|i} + p_{i|j} - q_{i|j}\big)(y_i - y_j).$$

Each term is a spring between $y_i$ and $y_j$: it pulls when $j$ is picked less often in the map than in the data, and pushes when it is picked more often.

## The algorithm

```pseudo id=main
SNE(x[1..n], m, u, T, η, α, s)
L1  for i ← 1 to n do                                  ▷ bandwidths
L2      β_i ← BANDWIDTH(i, u)                           ▷ β_i = 1/(2σ_i²)
L3      p_{j|i} ← exp(−β_i‖x_i − x_j‖²) / Σ_{k≠i} exp(−β_i‖x_i − x_k‖²) for j ≠ i
L4  y_i ← a draw from N(0, 10⁻⁴ I_m) for each i;  v_i ← 0
L5  for t ← 1 to T do
L6      q_{j|i} ← exp(−‖y_i − y_j‖²) / Σ_{k≠i} exp(−‖y_i − y_k‖²) for all i ≠ j
L7      g_i ← 2 Σ_j (p_{j|i} − q_{j|i} + p_{i|j} − q_{i|j})(y_i − y_j) for each i
L8      v_i ← α v_i − η g_i;  y_i ← y_i + v_i
L9      y_i ← y_i + a draw from N(0, (s(1 − t/T))² I_m)   ▷ jitter that shrinks to 0
L10 return y

BANDWIDTH(i, u)                                       ▷ bisection on the precision β
L11 β ← 1, lo ← 0, hi ← ∞
L12 repeat
L13     compute the row p_{·|i} at β and its entropy H in bits
L14     if H > log₂ u then lo ← β; β ← 2β if hi = ∞ else (β + hi)/2
L15     else hi ← β; β ← (lo + β)/2
L16 until |H − log₂ u| ≤ τ
L17 return β
```

The search runs on the precision $\beta_i = 1/(2\sigma_i^2)$ rather than on $\sigma_i$, because the entropy is a smooth decreasing function of $\beta_i$ (see Correctness). Line L13 subtracts the smallest distance before the exponentials, which does not change the row and avoids underflow. Hinton and Roweis used plain gradient steps with jitter that falls to zero over time, from a start with all points very close to the origin. Momentum (line L8) is the form of van der Maaten and Hinton (2008, Section 2).

## Example

Take $n = 4$ points on a line, $x = 0, 1, 3, 7$, a map of dimension $m = 1$ and perplexity $u = 2$. The search gives these rows:

| $i$ | $\beta_i$ | $\sigma_i$ | $p_{\cdot \mid i}$ for $j = 1, 2, 3, 4$ |
|---|---|---|---|
| 1 | 0.08477 | 2.4287 | 0, 0.6559, 0.3329, 0.0112 |
| 2 | 0.14417 | 1.8623 | 0.6041, 0, 0.3920, 0.0039 |
| 3 | 0.23896 | 1.4465 | 0.2227, 0.7355, 0, 0.0418 |
| 4 | 0.07379 | 2.6032 | 0.0666, 0.1737, 0.7598, 0 |

For row 1 the squared distances are $1, 9, 49$. With $\beta_1 = 0.08477$ the weights are $e^{-0.08477} = 0.9187$, $e^{-0.7629} = 0.4663$ and $e^{-4.154} = 0.0157$, with the sum $1.4007$, which gives the row in the table and the entropy 1 bit. The outlier $x_4 = 7$ gets the widest Gaussian, because it must reach far to find two effective neighbors. The rows are not symmetric: $p_{2|1} = 0.6559$ but $p_{1|2} = 0.6041$.

Start the map at $y = (0, 0.5, 1.5, 3.5)$, which is $x/2$. Then $C = 0.9879$ nats and the gradient is $(-0.9086, -1.4413, 1.6977, 0.6522)$. In the map, $q_{2|1} = 0.8808$ is larger than $p_{2|1}$, while $q_{3|4} = 0.9930$ is much larger than $p_{3|4} = 0.7598$: the half-size map puts the outlier too close to its neighbors. Gradient descent with $\eta = 0.2$ and momentum $0.8$ from a seeded small start ends at $y \approx (0.890, 0.525, 0.071, -1.466)$ with $C \approx 0.0996$. The map is the line flipped, the order is kept, and the gap to the outlier stays the largest. $C$ does not reach 0, because no one-dimensional map can match all four rows at once.

## Correctness

Two facts make the method well defined, and both are proved in full below.

1. **The bandwidth search.** With $\beta = 1/(2\sigma^2)$, the entropy of row $i$ in nats is $H(\beta) = \ln Z(\beta) + \beta\,\mathbb{E}_\beta[D]$, and $H'(\beta) = -\beta \operatorname{Var}_\beta(D)$, where $D$ is the squared distance to a neighbor drawn from the row. So $H$ falls strictly from $\ln(n-1)$ at $\beta = 0$ to $\ln |M|$ as $\beta \to \infty$, where $|M|$ is the number of nearest neighbors at the smallest distance. Each perplexity $u$ with $|M| < u < n - 1$ is reached at exactly one $\beta_i$, and bisection finds it to any tolerance.
2. **The gradient.** Write $\ln q_{j|i} = -\|y_i - y_j\|^2 - \ln Z_i$ and use $\sum_j p_{j|i} = 1$. Then $C$ is a constant plus $\sum_{i,j} p_{j|i} \|y_i - y_j\|^2 + \sum_i \ln Z_i$, and the derivative of each part gives the formula above.

Nothing more holds in general. $C$ is not convex in $y$; for example it does not change when the whole map is moved, turned or mirrored, so its minima are never isolated points. Gradient descent can stop in a poor local minimum, which is why Hinton and Roweis added the jitter.

## Complexity

In the [real RAM](/real-ram/) model:

- **Affinities.** The squared distances cost $O(n^2 d)$. Each bisection step for row $i$ costs $O(n)$, and a fixed tolerance needs $O(\log(1/\tau))$ steps for bounded data, so all rows cost $O(n^2 \log(1/\tau))$.
- **One gradient step.** Lines L6 and L7 cost $O(n^2 m)$ time.
- **Total.** $O(n^2 d + n^2 t m)$ time for $t$ steps and $O(n^2)$ memory for $P$ and $Q$.

This is the cost of the exact method on every input. Hinton and Roweis report that the method was slow; the tree methods of [t-SNE](/t-sne/) bring the step to $O(n \log n)$.

## Properties

- **Local first.** The asymmetric cost punishes torn neighborhoods much more than false neighbors, so SNE keeps small distances and may distort large ones.
- **Adaptive bandwidth.** Points in dense regions get a small $\sigma_i$ and points in sparse regions a large one.
- **Not parametric.** SNE returns positions, not a function. A new point needs a new run, or a separate model.
- **Invariant to rigid motions of the map.** $C$ depends only on the distances between the $y_i$.
- **Randomized.** The result depends on the start and the jitter, so fix the seed to repeat a run.

## Variants and improvements

- **Symmetric SNE.** Use one joint distribution $p_{ij} = (p_{j|i} + p_{i|j})/2n$ and one $q_{ij}$ over all pairs. The gradient becomes simpler, $4 \sum_j (p_{ij} - q_{ij})(y_i - y_j)$ (van der Maaten and Hinton 2008, Section 3.1).
- **t-SNE.** Symmetric SNE with a Student t kernel of one degree of freedom in the map. Its heavy tail fixes the crowding problem. See [t-SNE](/t-sne/).
- **Mixture SNE.** Hinton and Roweis (Section 4) let each object have several images in the map with mixing weights, so that an ambiguous word such as "bank" can sit near both "river" and "finance".
- **Dissimilarity input.** The $\|x_i - x_j\|^2 / 2\sigma_i^2$ can be replaced by given dissimilarities $d_{ij}^2$, which need not be symmetric.
- **Large data.** Use only the $k$ nearest neighbors of each point, from a [k-nearest neighbor graph](/k-nearest-neighbor-graph/), and approximate the far forces with a tree.

## When to use it

Use SNE for small sets when you want a map that keeps neighbors and you want the original, simplest cost. For visualization in practice, [t-SNE](/t-sne/) or [UMAP](/umap/) gives clearer maps at the same or lower cost. For a map that keeps global distances, use [multidimensional scaling](/multidimensional-scaling/) or [PCA](/principal-component-analysis/).

## Pitfalls

- **The crowding problem.** In 10 dimensions there can be 11 points at equal distance from each other, but in 2 dimensions at most 3. There is too little area in the map for the points at moderate distance, so SNE squeezes clusters together in the middle of the map (van der Maaten and Hinton 2008, Section 3.2).
- **A perplexity that cannot be reached.** If $u \ge n - 1$, or $u$ is at most the number of tied nearest neighbors, no finite $\sigma_i$ meets it. For $x = 0, 1, 2$ seen from the middle point, both neighbors are at distance 1 and the perplexity is 2 for every $\sigma$; a smaller target is never reached. Bound the number of bisection steps.
- **Base of the logarithm.** The target is $\log_2 u$ if $H$ is in bits and $\ln u$ if it is in nats. A mix of the two gives the wrong bandwidths.
- **Underflow.** For a small $\sigma_i$ all the weights of a row can round to 0. Subtract the smallest distance in the row before the exponentials.
- **Reading the map.** Distances between clusters in the map have no fixed scale, and a cluster can be split by a poor local minimum. Check the result with several seeds and with [trustworthiness and continuity](/trustworthiness-and-continuity/).

## Implementations

## History

Hinton and Roweis presented SNE at NIPS 2002. The paper defines the conditional probabilities, sets each $\sigma_i$ by a binary search for a perplexity chosen by hand, derives the gradient, and fits maps of handwritten digits and of NIPS authors with gradient descent and annealed jitter. Van der Maaten and Hinton (2008) made the probabilities symmetric and gave the map a heavy-tailed kernel, which is [t-SNE](/t-sne/). Van der Maaten (2014) later made the gradient step fast with trees.

## References
