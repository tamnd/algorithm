---
tag: RXEEKH
kind: algorithm
slug: principal-curves
name: Principal curves
aliases:
- principal curves and surfaces
- Hastie-Stuetzle principal curve
area: machine-learning/dimensionality-reduction
level: advanced
summary: "A smooth curve through the middle of the data: each point of the curve is the mean of the data that project onto it. A nonlinear version of the first principal component."
model: real-ram
complexity:
  vars: {n: the number of points, D: the dimension, I: the number of rounds}
  time: {worst: "O(I n^2 D)"}
  space: {extra: "O(n D)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1989
  people: [Trevor Hastie, Werner Stuetzle]
  note: Hastie and Stuetzle defined principal curves by self-consistency in JASA in 1989. Kégl, Krzyżak, Linder and Zeger gave a length-constrained definition and the polygonal line algorithm in 2000.
prereqs: [principal-component-analysis, point-to-segment-distance]
see_also: [self-organizing-map, smoothing-spline, autoencoder, kernel-pca, isomap, locally-linear-embedding, manifold-learning, k-means]
sources:
  - paper: "Trevor Hastie and Werner Stuetzle, Principal curves, Journal of the American Statistical Association 84(406):502-516, 1989"
    title: Hastie and Stuetzle 1989
    locator: the definition of the projection index and of self-consistency, the result that straight self-consistent lines are principal components, the algorithm that alternates projection and a scatterplot smoother from the first principal component line, and the bias of the curve for data around a circle
  - paper: "Balázs Kégl, Adam Krzyżak, Tamás Linder and Kenneth Zeger, Learning and design of principal curves, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(3):281-297, 2000"
    title: Kégl, Krzyżak, Linder and Zeger 2000
    locator: principal curves of length at most L as minimizers of the expected squared distance, their existence, the consistency of the empirical curve, and the polygonal line algorithm
  - book: isbn:9780387848570
    title: "Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009"
    locator: Section 14.5.2 (principal curves and surfaces)
  - paper: "Robert Tibshirani, Principal curves revisited, Statistics and Computing 2(4):183-190, 1992"
    title: Tibshirani 1992
    locator: a definition of principal curves as a mixture model fitted by EM, which removes the bias at the model level
---

A principal curve is a smooth curve that passes through the middle of a cloud of points. Hastie and Stuetzle (1989) defined it by *self-consistency*: every point $f(\lambda)$ of the curve is the mean of all data whose nearest point on the curve is $f(\lambda)$. A straight line has this property only along a principal axis, so principal curves extend the first [principal component](/principal-component-analysis/) to curved data. The page implements the **Hastie and Stuetzle algorithm**: start from the first principal component line, then alternate a projection step (find each point's nearest place on the curve) and a smoothing step (replace the curve by a local average of the points along it). The **polygonal line algorithm** of Kégl, Krzyżak, Linder and Zeger (2000), which fits a curve of bounded length, is described under the variants.

## In plain words

Draw a straight line through the long axis of the data. For each data point, find the nearest spot on the line, and write down how far along the line that spot is.

Now sort the points by that position. Walk along the line, and at each position put a new curve point at the average of the data points that are nearby in position. The new curve bends toward the data.

Then find the nearest spot on the new curve for each data point, and repeat. Stop when the total squared distance from the points to the curve no longer drops.

## The problem

The input is $n$ points $x_1, \ldots, x_n \in \mathbb{R}^D$. The output is a curve $f : [\lambda_{\min}, \lambda_{\max}] \to \mathbb{R}^D$, here a polygon, and a position $\lambda_i$ on it for each point.

For a curve $f$ parametrized by arc length, the **projection index** of $x$ is

$$\lambda_f(x) = \sup \big\{ \lambda : \|x - f(\lambda)\| = \inf_\mu \|x - f(\mu)\| \big\},$$

the position of the nearest point of the curve (the largest one on ties). For a random vector $X$, the curve is **self-consistent**, and is called a *principal curve*, if

$$f(\lambda) = E\big[X \mid \lambda_f(X) = \lambda\big] \quad \text{for almost every } \lambda.$$

For data the conditional mean is replaced by a scatterplot smoother, and the quality of the fit is measured by $D^2 = \sum_i \|x_i - f(\lambda_i)\|^2$.

## The algorithm

```pseudo id=main
PRINCIPAL-CURVE(x[1..n], span, tol)
L1  f ← the line through the mean x̄ along the first principal direction v
L2  λ_i ← vᵀ(x_i − x̄) for each i
L3  repeat
L4      sort the points by λ
L5      f(λ_i) ← local linear fit of x on λ, with tricube weights on the ⌈span·n⌉ points nearest in λ, at λ_i
L6      λ_i ← arc length position of the nearest point of the polygon f(λ_(1)), …, f(λ_(n)) to x_i
L7      D² ← Σ_i ‖x_i − f(λ_i)‖²
L8  until the relative change of D² is below tol
L9  return f, λ
```

Line L5 is the *conditional expectation step*: it estimates $E[X \mid \lambda]$ at each $\lambda_i$, separately for each coordinate, with a local linear smoother (a locally weighted regression, as in lowess). The weight of a neighbor at distance $u$ in $\lambda$ is $(1 - (u/h)^3)^3$, where $h$ is the largest such distance in the window. Hastie and Stuetzle allow any scatterplot smoother here, for example a smoothing spline. The span controls the stiffness of the curve: a large span gives a nearly straight curve, a small one follows the noise.

Line L6 is the *projection step*. For each segment $[a, b]$ of the polygon the nearest point to $x$ is $a + t(b - a)$ with $t = \operatorname{clip}(\langle x - a, b - a\rangle / \|b - a\|^2, 0, 1)$, and the nearest point of the polygon is the best of these (see [point to segment distance](/point-to-segment-distance/)). The new $\lambda_i$ is its arc length from the first vertex, so the curve is always parametrized by arc length.

## Example

**A segment.** Put 20 points evenly on the segment from $a = (1, 2, -1)$ to $b = (4, 6, 1)$, of length $\sqrt{29} \approx 5.385$, in random order. The first principal direction is $(3, 4, 2)/\sqrt{29}$, so the start line contains the segment and each $\lambda_i$ is the exact position of $x_i$. The local linear fit of points that lie on a line returns them unchanged, so the new polygon has the points themselves as vertices, from $a$ to $b$. The positions span exactly $5.385$, $D^2 = 0$, and the loop stops after one round. The curve recovers the segment.

**An arc.** Take 100 points at random angles $\theta \in [0, \pi]$ on the unit half circle, plus Gaussian noise with standard deviation $0.05$ in each coordinate, and span $0.2$. The values of $D^2$ are

| round | 0 (PCA line) | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $D^2$ | 9.371 | 0.417 | 0.258 | 0.231 | 0.226 | 0.2257 | 0.2255 |

The straight line leaves most of the variance unexplained. After six rounds the curve follows the arc: the mean distance of its vertices from the unit circle is $0.014$. The final $D^2 \approx 0.23$ is close to $n \sigma^2 = 0.25$, the part of the noise across the curve, which no curve can remove.

## Correctness

The full proofs are below. The loop as a whole has no proof of convergence. What holds exactly:

1. **The projection step** computes the projection index: the clipped projection is the unique nearest point of a segment (a strictly convex quadratic on $[0, 1]$), and the best segment gives the nearest point of the polygon. So for a fixed curve, this step can only lower $D^2$.
2. **Straight principal curves are principal components.** If $f(\lambda) = \mu + \lambda v$ is self-consistent, then $\Sigma v = E[\Lambda (X - \mu)] = E[\Lambda^2] v$, so $v$ is an eigenvector of the covariance. This is why the start is the first principal component line.
3. **The smoother keeps lines.** A weighted least squares line fitted to points on a line has zero error, so it returns the line. With the first two facts, this proves that points on a segment give back the segment after one round.

The smoothing step is only an estimate of the conditional mean, so $D^2$ can rise slightly between rounds. The implementation stops when the relative change is below a tolerance, and the tests check that the result is much better than the start line.

## Complexity

In the [real RAM](/real-ram/) model, one round costs $O(n \log n)$ for the sort, $O(n q D)$ for the smoother with $q = \lceil \text{span} \cdot n \rceil$ points per window, and $O(n^2 D)$ for the projection of $n$ points onto a polygon with $n$ vertices. So $I$ rounds cost $O(I n^2 D)$ time on every input, with $O(n D)$ memory. A polygon with fewer vertices, for example on a fixed grid of $\lambda$ values, makes the projection $O(n m D)$ for $m$ vertices.

## Properties

- **Generalizes PCA.** On data along a line, the principal curve is the first principal component line.
- **Not a regression.** The distance is measured orthogonally to the curve, and all coordinates are treated alike, unlike a regression of one coordinate on the others.
- **Biased.** For data spread around a circle, the self-consistent curve is a circle of larger radius than the one that made the data, and the smoother pulls the estimate toward the center of curvature.
- **Self-consistent curves are critical points.** Hastie and Stuetzle show that a principal curve is a critical point of the expected squared distance under small smooth changes of the curve. It need not be a minimum, and a distribution can have many principal curves.
- **Deterministic** for a fixed smoother, span and start.

## Variants and improvements

- **Polygonal line algorithm** (Kégl, Krzyżak, Linder and Zeger 2000). They define a principal curve of length $L$ as a curve of length at most $L$ that minimizes $E \min_\lambda \|X - f(\lambda)\|^2$. Such a curve always exists, which is not true under self-consistency, and the curve fitted to $n$ points converges to it. The algorithm starts with the first principal component segment. It adds one vertex at a time, at the middle of the segment that holds the most points, and after each addition moves the vertices one by one to lower the mean squared distance plus a penalty on the angles at the vertices.
- **Principal curves by a mixture model** (Tibshirani 1992). The curve is a latent variable model with a Gaussian spread around each point of the curve, fitted by [expectation maximization](/expectation-maximization/).
- **Principal surfaces.** The same alternation with a two-dimensional index $\lambda$ and a surface smoother.
- **Bias correction.** Banfield and Raftery (1992) smooth the residuals instead of the points, which reduces the bias toward the center.
- **Closed curves**, for data around a loop, with a periodic smoother.
- **Discrete versions.** A one-dimensional [self-organizing map](/self-organizing-map/) with many units is a discrete relative.

## When to use it

Use a principal curve to summarize data that lie along a single curved path, for example a trajectory, a growth path or a curved ridge in two or three dimensions, and to order the points along it (the $\lambda_i$ are a one-dimensional embedding). Use it when there is no response variable, so that a regression does not fit. For data with a curved structure of higher dimension, use [Isomap](/isomap/), [locally linear embedding](/locally-linear-embedding/) or an [autoencoder](/autoencoder/).

## Pitfalls

- **A bad start.** For a closed or strongly curved shape, such as a full circle or an S, the first principal component line projects far-apart points to the same place, and the curve can get stuck. Start from a hand-made curve or use the polygonal line algorithm.
- **The span.** Too small a span follows the noise and the curve can cross itself; too large a span gives the straight line. Choose it by cross-validation of $D^2$ on held-out points.
- **Scaling.** The fit uses Euclidean distance, so put the coordinates on comparable scales first.
- **No convergence guarantee.** $D^2$ can oscillate a little. Stop on a relative tolerance and a maximum number of rounds.
- **Ends of the curve.** Points beyond the ends project to the end vertices, and the local fit there uses a one-sided window, which bends the ends.

## Implementations

## History

Hastie wrote his PhD thesis on principal curves and surfaces at Stanford in 1984, and Hastie and Stuetzle published the definition by self-consistency and the algorithm in JASA in 1989. Banfield and Raftery (1992) used them to trace the outlines of ice floes in satellite images and corrected the bias. Tibshirani (1992) recast them as a mixture model. Kégl, Krzyżak, Linder and Zeger (2000) replaced self-consistency by a length constraint, which gave a curve that always exists and the polygonal line algorithm with a consistency result. Later work used principal curves to order cells along a developmental path in single-cell biology.

## References
