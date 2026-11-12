---
tag: HP4B32
kind: algorithm
slug: sammon-mapping
name: Sammon mapping
aliases:
- Sammon's nonlinear mapping
- Sammon projection
- Sammon's stress
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Fit low-dimensional distances to input distances, each squared error divided by its input distance, by a diagonal Newton step with a magic factor of about 0.3 to 0.4."
model: real-ram
complexity:
  vars: {n: the number of points, k: the output dimension, t: the number of iterations}
  time: {worst: "O(t n^2 k)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1969
  people: [John W. Sammon Jr.]
  note: Sammon published the mapping in the IEEE Transactions on Computers in 1969 as a tool to look at the structure of data in many dimensions.
prereqs: [multidimensional-scaling, gradient-descent]
see_also: [smacof, classical-mds, isomap, t-sne, self-organizing-map, newton-raphson-method, trustworthiness-and-continuity]
sources:
  - paper: doi:10.1109/T-C.1969.222678
    title: John W. Sammon Jr., A nonlinear mapping for data structure analysis, IEEE Transactions on Computers C-18(5), 1969, pages 401 to 409
    locator: the error E with the weights 1/d_ij, its first and second partial derivatives, and the update with the magic factor MF of about 0.3 or 0.4
  - book: isbn:9780387393506
    title: John A. Lee and Michel Verleysen, Nonlinear Dimensionality Reduction, Springer, 2007
    locator: Chapter 4, the section on Sammon's nonlinear mapping
---

Sammon mapping is a method of metric [multidimensional scaling](/multidimensional-scaling/) that weights the error on each pair by the inverse of its input distance, so that the small distances, which describe the local structure, count more than the large ones. Sammon (1969) minimized this weighted stress with a step that divides each partial derivative by the absolute value of the matching second derivative and then multiplies by a "magic factor" of about 0.3 to 0.4. The method is a heuristic: the stress usually falls, but a single step can raise it, and the result is a local minimum that depends on the start.

## In plain words

You want to draw points from a space of many dimensions on a flat page, with the distances on the page close to the true distances. A plain fit cares most about the long distances, because a 10 percent error on a long distance is a big number. Sammon's idea is to measure each error relative to the true distance, so that a small distance must also be right. Neighbors then stay neighbors on the page. To fit, the method moves each coordinate of each point a little, by an amount set from how fast the error changes and how curved it is in that coordinate. It shrinks each move by a fixed factor that was found by experiment.

## The problem

The input is a symmetric $n \times n$ matrix of distances $\delta_{ij}$ with $\delta_{ij} > 0$ for $i \ne j$, usually Euclidean distances between data points in $\mathbb{R}^d$, an output dimension $k$ (often 2), and a start configuration $Y \in \mathbb{R}^{n \times k}$ with rows $y_i$ and distances $d_{ij} = \|y_i - y_j\|$. Here $n$ is the number of points. Sammon's stress is

$$E(Y) = \frac{1}{c}\sum_{i<j}\frac{(\delta_{ij} - d_{ij})^2}{\delta_{ij}}, \qquad c = \sum_{i<j}\delta_{ij}.$$

It is a raw stress with the weights $w_{ij} = 1/(c\,\delta_{ij})$. The constant $c$ makes $E$ invariant under a common scaling of the input and the output. $E \ge 0$, and $E = 0$ exactly when $d_{ij} = \delta_{ij}$ for all pairs.

## The algorithm

For each point $p$ and each coordinate $q$, Sammon's paper gives the partial derivatives

$$\frac{\partial E}{\partial y_{pq}} = -\frac{2}{c}\sum_{j \ne p}\frac{\delta_{pj} - d_{pj}}{\delta_{pj}d_{pj}}(y_{pq} - y_{jq}),$$

$$\frac{\partial^2 E}{\partial y_{pq}^2} = -\frac{2}{c}\sum_{j \ne p}\frac{1}{\delta_{pj}d_{pj}}\left[(\delta_{pj} - d_{pj}) - \frac{(y_{pq} - y_{jq})^2}{d_{pj}}\left(1 + \frac{\delta_{pj} - d_{pj}}{d_{pj}}\right)\right].$$

```pseudo id=main
SAMMON(Δ, Y, MF, T)
L1  E ← the stress of Y
L2  for t ← 1 to T do
L3      d_pj ← ‖y_p − y_j‖ for all pairs
L4      g_pq ← ∂E/∂y_pq for each point p and coordinate q
L5      h_pq ← ∂²E/∂y_pq² for each p and q
L6      y_pq ← y_pq − MF · g_pq / |h_pq| for each p and q, all at once
L7      E ← the stress of the new Y
L8  return Y
```

Line L6 is a Newton step for each coordinate alone, with the off-diagonal second derivatives ignored. The absolute value makes the step go downhill when the second derivative is negative, where a pure Newton step would go uphill. The magic factor MF shrinks the step. Sammon reports that values of about 0.3 to 0.4 work well. All coordinates move together, from the values of the previous iteration.

## Example

Map the four corners $(0,0,0), (1,0,0), (0,1,0), (0,0,1)$ of a corner of the unit cube to the plane. The distances are 1 from the first point to each other and $\sqrt2$ between the other three, and $c = 3 + 3\sqrt2 \approx 7.243$. Start from $(0,0), (1,0), (0,1), (0.3, 0.3)$, with $\mathrm{MF} = 0.35$.

| iteration | 0 | 1 | 2 | 3 | 4 | 5 | 10 | 40 |
|---|---|---|---|---|---|---|---|---|
| stress $E$ | 0.1289 | 0.7521 | 0.1266 | 0.0240 | 0.0137 | 0.0128 | 0.0108 | 0.0095 |

The first step makes the stress almost six times larger. After that the stress falls. After 40 iterations, the first point is near the center of the other three, at distance 0.875 from each, and the other three form a near-equilateral triangle with side 1.516. The true distances are 1 and 1.414. Four points of this shape cannot be placed in the plane exactly, so $E$ stays above 0. On 20 random data sets of 10 points in $\mathbb{R}^4$ (seeds 0 to 19, uniform on the unit cube, a uniform random start, 60 iterations), 29 of the 1200 steps raised the stress.

## Correctness

Sammon mapping has no convergence theorem. What holds is the following, with proofs in the proofs section below.

- **The derivatives are exact.** The formulas above are the first and second partial derivatives of $E$ where all $d_{pj} > 0$.
- **Exact fits are fixed points.** If $d_{ij} = \delta_{ij}$ for all pairs, then $E = 0$, each first derivative is 0, and line L6 does not move any point, provided each $|h_{pq}| > 0$.
- **The step is a descent direction.** If some first derivative is nonzero, the direction $-g_{pq}/|h_{pq}|$ has a negative inner product with the gradient. So a small enough magic factor lowers $E$. A fixed factor such as 0.35 is not always small enough, as the first step of the example shows.

The test suite checks the derivatives against finite differences, the fixed point, and that the stress falls over a run on seeded data. It does not claim monotone descent, because that is false.

## Complexity

- **One iteration.** Each of the $n$ points sums over $n - 1$ others, for each of $k$ coordinates. So lines L3 to L6 cost $\Theta(n^2 k)$ operations, and line L7 another $\Theta(n^2 k)$.
- **Memory.** $\Theta(n^2)$ for the input distances, or $\Theta(n d)$ if they are computed from the data on the fly.
- **Iterations.** No bound on the number of iterations is known. The number depends on the data, the start and the magic factor.

The quadratic cost per iteration limited the method to a few hundred or thousand points on the computers of its time. Neighbor graph methods such as [Isomap](/isomap/) and neighbor embeddings such as [t-SNE](/t-sne/) were later used for larger data.

## Properties

- **Local emphasis.** The weight $1/\delta_{ij}$ makes the errors on small distances count more, so local neighborhoods are kept better than by an unweighted stress. Large distances can be distorted more.
- **Invariance.** $E$ does not change under a rotation, reflection or translation of $Y$. Unlike the stress-1 of nonmetric MDS, it does change under a scaling of $Y$ alone.
- **Not monotone.** The diagonal Newton step with a fixed factor is a heuristic. The stress can rise in a step, and the method can oscillate when two points are close.
- **No out-of-sample map.** The method places the given points only. A new point needs a new run, or a separate fit with the old points fixed.

## Variants and improvements

- **Monotone methods.** Sammon's stress is a weighted raw stress, so [SMACOF](/smacof/) with the weights $w_{ij} = 1/\delta_{ij}$ minimizes it with a guaranteed decrease.
- **Line search.** A backtracking line search on the scaled step of line L6, or a full [gradient descent](/gradient-descent/) with a line search, removes the increases at the cost of more stress evaluations.
- **Curvilinear component analysis.** This method by Demartines and Hérault weights the errors by a decreasing function of the output distance and updates one point at a time. It is treated in Lee and Verleysen, Chapter 4.
- **Geodesic input.** Feeding graph shortest path distances, as in [Isomap](/isomap/), instead of Euclidean distances gives a nonlinear variant for curved manifolds.

## When to use it

Use Sammon mapping for a two-dimensional picture of a few hundred to a few thousand points when you want small distances kept and still care about the global layout. For a monotone method with the same criterion, use weighted [SMACOF](/smacof/). For tens of thousands of points or for clusters, a neighbor embedding such as [t-SNE](/t-sne/) is usually used instead, and its quality can be checked by [trustworthiness and continuity](/trustworthiness-and-continuity/).

## Pitfalls

- **Duplicate points.** If two input points are equal, $\delta_{ij} = 0$ and the weight $1/\delta_{ij}$ is infinite. Remove duplicates, or add a small constant to the zero distances.
- **Coincident output points.** If $d_{ij} = 0$ at some step, both derivatives divide by zero. Start from a configuration with distinct points, and guard the division as the implementation does.
- **A tiny second derivative.** When $|h_{pq}|$ is near 0, the step of line L6 is huge. Clip $|h_{pq}|$ from below or cap the step length.
- **A bad start.** A random start can trap the method. A start from [PCA](/principal-component-analysis/) or [classical MDS](/classical-mds/) is common.
- **Comparing errors.** Sammon's $E$ is not the stress-1 of Kruskal or the raw stress of SMACOF. Compare values only under the same definition.

## Implementations

## History

Sammon (1969) proposed the method as a nonlinear mapping for the analysis of data structure, at a time when linear projections were the usual tool for viewing data. He defined the weighted error, derived its first and second derivatives, and chose the step with the magic factor from experiments. The method became a standard visualization tool and a reference point for later nonlinear methods.

## References
