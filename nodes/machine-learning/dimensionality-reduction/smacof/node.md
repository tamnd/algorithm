---
tag: 8BX53A
kind: algorithm
slug: smacof
name: SMACOF
aliases:
- stress majorization
- scaling by majorizing a complicated function
- Guttman transform iteration
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Minimize the raw stress of metric MDS by majorization: repeat the Guttman transform X = (1/n) B(X) X. The stress never increases."
model: real-ram
complexity:
  vars: {n: the number of objects, k: the output dimension, t: the number of iterations}
  time: {worst: "O(t n^2 k)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1977
  people: [Jan de Leeuw, Louis Guttman]
  note: De Leeuw (1977) derived the majorization of the stress. The update is the Guttman transform, after Louis Guttman (1968). De Leeuw (1988) proved the convergence properties.
prereqs: [multidimensional-scaling]
see_also: [classical-mds, sammon-mapping, isomap, gradient-descent, positive-definite-matrix, pseudoinverse]
sources:
  - paper: "Jan de Leeuw, Applications of convex analysis to multidimensional scaling, in J. R. Barra, F. Brodeau, G. Romier and B. van Cutsem (editors), Recent Developments in Statistics, North-Holland, 1977, pages 133 to 145"
    locator: the majorization of the stress by the Cauchy-Schwarz inequality and the resulting update
  - paper: "Louis Guttman, A general nonmetric technique for finding the smallest coordinate space for a configuration of points, Psychometrika 33(4), 1968, pages 469 to 506"
    locator: the correction step that is now called the Guttman transform
  - paper: doi:10.1007/BF01897162
    title: Jan de Leeuw, Convergence of the majorization method for multidimensional scaling, Journal of Classification 5(2), 1988, pages 163 to 180
    locator: monotone convergence of the stress and the convergence of the difference of successive configurations to zero
  - book: isbn:9780387251509
    title: Ingwer Borg and Patrick J. F. Groenen, Modern Multidimensional Scaling, second edition, Springer, 2005
    locator: Chapter 8 (A majorization algorithm for solving MDS, the SMACOF algorithm and the Guttman transform)
  - paper: doi:10.18637/jss.v031.i03
    title: Jan de Leeuw and Patrick Mair, Multidimensional scaling using majorization, SMACOF in R, Journal of Statistical Software 31(3), 2009
    locator: Section 2 (the SMACOF algorithm with weights and the update with the Moore-Penrose inverse of V)
---

SMACOF (scaling by majorizing a complicated function) is the standard algorithm of metric [multidimensional scaling](/multidimensional-scaling/): it minimizes the raw stress, the sum of the squared differences between the configuration distances and the dissimilarities. Each step replaces the stress by a quadratic upper bound that touches it at the current configuration, and moves to the minimum of that bound. With unit weights this step is the *Guttman transform* $X^+ = \frac1n B(X)X$. The stress never increases, no step size is needed, and the method converges to a stationary value, though not always to the global minimum.

## In plain words

You have points on a map and target distances between them. For each pair, compare the current distance with the target. If the pair is too close, it should push apart, and if it is too far, it should pull together. SMACOF moves every point at once to the place that these pushes and pulls suggest, in a precise way. It replaces the hard measure of misfit with a simpler bowl-shaped measure that is never below it and equals it at the current map. The bottom of the bowl is easy to find, and it is the new map. Since the bowl is never below the true misfit and touches it at the old map, the true misfit at the new map cannot be larger than before. Repeat until the map stops changing.

## The problem

The input is a symmetric $n \times n$ matrix of dissimilarities $\Delta = (\delta_{ij})$ with $\delta_{ij} \ge 0$ and $\delta_{ii} = 0$, an output dimension $k$, and a start configuration $X_0 \in \mathbb{R}^{n \times k}$. Here $n$ is the number of objects and $k$ the output dimension. The goal is a configuration $X$ with rows $x_i$ and distances $d_{ij}(X) = \|x_i - x_j\|$ that makes the raw stress

$$\sigma(X) = \sum_{i<j} w_{ij}\,\bigl(d_{ij}(X) - \delta_{ij}\bigr)^2$$

small. The implementation and the example use unit weights $w_{ij} = 1$. The stress is not convex and has local minima, so the method promises only a decrease, not the minimum.

## The algorithm

For a configuration $Z$, define the $n \times n$ matrix $B(Z)$ by

$$b_{ij} = -\frac{\delta_{ij}}{d_{ij}(Z)} \text{ for } i \ne j \text{ with } d_{ij}(Z) > 0, \qquad b_{ij} = 0 \text{ for } i \ne j \text{ with } d_{ij}(Z) = 0, \qquad b_{ii} = -\sum_{j \ne i} b_{ij}.$$

```pseudo id=main
SMACOF(Δ, X_0, ε, T)
L1  X ← X_0 minus the mean of its rows, σ ← σ(X)
L2  for t ← 1 to T do
L3      d_ij ← ‖x_i − x_j‖ for each pair
L4      b_ij ← −δ_ij / d_ij if d_ij > 0, else 0, for i ≠ j
L5      b_ii ← −Σ_{j ≠ i} b_ij
L6      X ← (1/n) B X                                  ▷ Guttman transform
L7      σ_new ← σ(X)
L8      if σ − σ_new < ε then return X
L9      σ ← σ_new
L10 return X
```

The rows and columns of $B$ sum to zero, so $X$ stays centered at each step. With weights, line L6 becomes $X \leftarrow V^+ B X$, where $V = \sum_{i<j} w_{ij}(e_i - e_j)(e_i - e_j)^\top$, $V^+$ is its [pseudoinverse](/pseudoinverse/), and $b_{ij} = -w_{ij}\delta_{ij}/d_{ij}$. For unit weights $V = nI - \mathbf{1}\mathbf{1}^\top$ and $V^+ = \frac1n J$ on centered matrices, which gives the $\frac1n$ of line L6.

## Example

Take three objects with $\delta_{12} = \delta_{13} = \delta_{23} = 2$, an equilateral triangle of side 2, and start from $(-1, 0), (1, 0), (0, 1)$. Line L1 centers it to $(-1, -\frac13), (1, -\frac13), (0, \frac23)$. The distances are $2, \sqrt2, \sqrt2$, so $\sigma = 2(2 - \sqrt2)^2 \approx 0.6863$, and

$$B = \begin{pmatrix} 1 + \sqrt2 & -1 & -\sqrt2 \\ -1 & 1 + \sqrt2 & -\sqrt2 \\ -\sqrt2 & -\sqrt2 & 2\sqrt2 \end{pmatrix}.$$

The first point moves to $\frac13\bigl((1+\sqrt2)(-1, -\frac13) - (1, -\frac13) - \sqrt2(0, \frac23)\bigr) = \bigl(-\frac{2+\sqrt2}{3}, -\frac{\sqrt2}{3}\bigr) \approx (-1.1381, -0.4714)$.

| step | point 1 | point 3 | raw stress |
|---|---|---|---|
| 0 | (−1, −0.3333) | (0, 0.6667) | 0.6863 |
| 1 | (−1.1381, −0.4714) | (0, 0.9428) | 0.1445 |
| 2 | (−1.0846, −0.5194) | (0, 1.0388) | 0.0493 |
| 3 | (−1.0475, −0.5472) | (0, 1.0943) | 0.0146 |
| 6 | (−1.0066, −0.5735) | (0, 1.1469) | 0.00027 |

Point 2 is the mirror image of point 1. The configuration tends to the centered equilateral triangle with vertices $(\pm 1, -1/\sqrt3)$ and $(0, 2/\sqrt3) \approx (0, 1.1547)$, From step 1 on, the ratio of two successive stress values is 2.9, 3.4, 3.7, 3.8 and 3.9, so the convergence is linear here.

## Correctness

The key is a quadratic upper bound of the stress. Expand $\sigma(X) = \sum_{i<j}\delta_{ij}^2 + \operatorname{tr}(X^\top V X) - 2\rho(X)$ with $\rho(X) = \sum_{i<j}\delta_{ij} d_{ij}(X)$. By the Cauchy-Schwarz inequality, $d_{ij}(X) \ge (x_i - x_j)^\top(z_i - z_j)/d_{ij}(Z)$, which gives $\rho(X) \ge \operatorname{tr}(X^\top B(Z) Z)$ with equality at $X = Z$. So

$$\sigma(X) \le \tau(X, Z) = \sum_{i<j}\delta_{ij}^2 + \operatorname{tr}(X^\top V X) - 2\operatorname{tr}(X^\top B(Z) Z), \qquad \sigma(Z) = \tau(Z, Z).$$

The function $\tau(\cdot, Z)$ is a convex quadratic, and its minimum over centered $X$ is the Guttman transform $X^+$. This gives the *sandwich inequality* $\sigma(X^+) \le \tau(X^+, Z) \le \tau(Z, Z) = \sigma(Z)$, and more precisely, for unit weights and a centered $Z$,

$$\sigma(Z) - \sigma(X^+) \ge n\,\|Z - X^+\|_F^2 .$$

So the stress never increases, it decreases strictly unless the configuration is a fixed point, and the sum of the squared step lengths is at most $\sigma(X_0)/n$. The full proof is in the proofs section below. De Leeuw (1988) shows that the stress values converge and that the steps tend to zero. The limit points are stationary points of $\sigma$ when the distances stay positive, but they can be local minima or saddle points.

## Complexity

- **One iteration.** Lines L3 to L5 cost $\Theta(n^2 k)$ for the distances and $\Theta(n^2)$ for $B$. Line L6 is a product of an $n \times n$ by an $n \times k$ matrix, $\Theta(n^2 k)$. Line L7 costs another $\Theta(n^2 k)$. So one iteration costs $\Theta(n^2 k)$ operations.
- **Memory.** $\Theta(n^2)$ for $\Delta$ and $B$. $B$ can be applied row by row without storing it, which leaves $\Theta(n^2)$ only for the input.
- **Iterations.** No bound on $t$ in terms of $n$ is known. De Leeuw (1988) shows that the convergence is linear in almost all cases, with a rate that is often close to 1, so the method can be slow near the end. The number of iterations depends on the start and the tolerance.
- **With weights.** $V^+$ costs $O(n^3)$ once, and then $O(n^2 k)$ per iteration.

## Properties

- **Monotone.** The stress never increases, with no step size and no line search.
- **Only descent.** The result depends on the start. A [classical MDS](/classical-mds/) start is common, together with random starts.
- **Invariance.** The stress, and the Guttman transform, commute with rotations and reflections of $X$. The result is fixed only up to these maps.
- **Fixed points.** A configuration whose distances equal $\Delta$ exactly is a fixed point: then $B(X) = V$ and $\frac1n V X = X$ for a centered $X$.
- **A gradient step.** For unit weights and a centered $X$, the Guttman transform equals $X - \frac{1}{2n}\nabla\sigma(X)$. So SMACOF is [gradient descent](/gradient-descent/) with the fixed step $\frac{1}{2n}$, and majorization proves that this step is safe.

## Variants and improvements

- **Nonmetric SMACOF.** Alternate the Guttman transform with an [isotonic regression](/isotonic-regression/) of the distances, normalized so that the disparities keep a fixed sum of squares. This is the nonmetric MDS of [multidimensional scaling](/multidimensional-scaling/) with a safe step.
- **Weights.** The weighted update $V^+ B X$ fits missing entries ($w_{ij} = 0$) and gives [Sammon](/sammon-mapping/)-like weights $w_{ij} = 1/\delta_{ij}$ with a monotone method.
- **Constraints.** Confirmatory MDS restricts $X$, for example to a linear model $X = ZC$. The majorization step then becomes a projection of $X^+$ onto the restricted set in the metric of $V$.
- **Acceleration.** A relaxed update $X \leftarrow 2X^+ - X$, or a [conjugate gradient](/nonlinear-conjugate-gradient/) or [quasi-Newton](/quasi-newton-method/) method on the stress, often takes fewer iterations.
- **Large data.** Landmark versions, or stochastic updates that sample pairs, reduce the $\Theta(n^2)$ cost per iteration.

## When to use it

Use SMACOF for metric MDS when you have dissimilarities, possibly with missing values or weights, and want the fit of the distances themselves, not of inner products. Start it from [classical MDS](/classical-mds/). Use classical MDS alone when the data are near Euclidean and you need a quick answer, and use a [manifold learning](/manifold-learning/) method when the data lie on a curved surface in a feature space.

## Pitfalls

- **Coincident points.** When $d_{ij}(X) = 0$, the stress is not differentiable. Line L4 sets $b_{ij} = 0$, which keeps the majorization valid, but the result can stay stuck with two points on top of each other.
- **Forgetting to center.** For unit weights the formula $\frac1n BX$ needs a centered $X$, and the weighted formula needs $V^+$, not $V^{-1}$: $V$ is singular, because $V\mathbf{1} = 0$.
- **Stopping too early.** A small decrease of the stress in one step does not mean a small gradient, because convergence can be slow. Also check the change of $X$.
- **Local minima.** A low stress from one start is not proof of a global minimum. Run several starts.
- **Comparing stress values.** Raw stress depends on the scale of $\Delta$. Report a normalized stress, for example $\sigma / \sum \delta_{ij}^2$, when you compare data sets.

## Implementations

## History

De Leeuw (1977) applied convex analysis to the stress and found the majorization by the Cauchy-Schwarz inequality. The update $\frac1n B(X)X$ had been used by Guttman (1968) as a correction step, which is why it is called the Guttman transform. De Leeuw (1988) proved that the stress converges and that the difference of successive configurations tends to zero. Borg and Groenen made SMACOF the central algorithm of their textbook. It is the MDS solver of the R package smacof and of scikit-learn.

## References
