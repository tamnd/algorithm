---
tag: J6NCZD
kind: algorithm
slug: one-step-late-algorithm
name: One-step-late algorithm
aliases:
- OSL MAP-EM
- Green's one-step-late
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Add a prior to MLEM by evaluating the gradient of the penalty at the current image in the denominator of the update.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of iterations"}
  time: {per_iteration: "O(a d n)", total: "O(K a d n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, iterative: true, in_place: false, recursive: false, monotone_objective: false, keeps_nonnegativity: "only while every denominator is positive"}
history:
  year: 1990
  people: [Peter J. Green]
  note: Green proposed to put the gradient of the log prior, evaluated at the current image, into the EM update for emission tomography.
prereqs: [mlem-reconstruction, maximum-a-posteriori-estimation, markov-random-field]
see_also: [separable-paraboloidal-surrogates, osem, emission-tomography-model, richardson-lucy-total-variation, bayesian-inverse-problem, kkt-conditions, total-variation-denoising, projected-gradient-descent]
sources:
  - paper: doi:10.1109/42.52985
    title: P. J. Green, Bayesian reconstructions from emission tomography data using a modified EM algorithm, IEEE Transactions on Medical Imaging 9(1), 1990
    locator: pp. 84 to 93 (the one-step-late update for a Gibbs prior)
  - paper: doi:10.1109/42.61759
    title: K. Lange, Convergence of EM image reconstruction algorithms with Gibbs smoothing, IEEE Transactions on Medical Imaging 9(4), 1990
    locator: pp. 439 to 446 (a modified one-step-late algorithm with a line search, and its convergence)
  - paper: doi:10.1109/TMI.1982.4307558
    title: L. A. Shepp and Y. Vardi, Maximum likelihood reconstruction for emission tomography, IEEE Transactions on Medical Imaging 1(2), 1982
    locator: pp. 113 to 122 (the MLEM update that OSL modifies)
---

The one-step-late algorithm (OSL) computes a penalized likelihood, or maximum a posteriori, image for the [emission tomography model](/emission-tomography-model/) $y_i \sim \operatorname{Poisson}((A x + b)_i)$. It maximizes $\Phi(x) = L(x) - \beta R(x)$, where $L$ is the Poisson log-likelihood, $R$ is a smooth penalty such as a sum of squared differences of neighbor pixels, and $\beta \ge 0$ sets its weight. The update is the [MLEM](/mlem-reconstruction/) update with one change: the gradient of the penalty, evaluated at the current image, is added to the denominator, $x_j \leftarrow x_j g_j / (s_j + \beta\, \partial R / \partial x_j(x))$. This is cheap and easy to add to an MLEM code. Its fixed points are the maximizers of $\Phi$. But the method is not a monotone method, and for a large $\beta$ a denominator can become zero or negative, which gives a negative or undefined image. Green proposed it in 1990.

## In plain words

MLEM makes the counts more probable at each step, but with noisy data its images get noisy. A penalty fixes this: it adds a cost when a pixel differs from its neighbors, so the method prefers smooth images. MLEM with a penalty has no simple update, because the penalty ties each pixel to its neighbors.

The one-step-late trick looks at the neighbors in the old image, not the new one. If a pixel is brighter than its neighbors, its new value is divided by a larger number, so it goes down. If it is darker, its value is divided by a smaller number, so it goes up. This keeps the simple form of MLEM. The cost is that the correction is late by one step. If the penalty is strong, the correction can overshoot, and the method can fail.

## The problem

Given counts $y$, a matrix $A$ with $a_{ij} \ge 0$ and column sums $s_j > 0$, a background $b \ge 0$, a weight $\beta \ge 0$ and a differentiable penalty $R$, maximize
$$\Phi(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i\big] - \beta R(x), \qquad \bar y = A x + b,$$
over $x \ge 0$. With a prior density proportional to $e^{-\beta R(x)}$, the maximizer is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/), and the prior is a Gibbs distribution, a [Markov random field](/markov-random-field/) on the pixel grid. The page uses the quadratic neighbor penalty
$$R(x) = \tfrac12 \sum_{\{j,k\} \in E} w_{jk} (x_j - x_k)^2, \qquad \frac{\partial R}{\partial x_j} = \sum_{k \sim j} w_{jk} (x_j - x_k),$$
with $E$ the edges between neighbor pixels and $w_{jk} \ge 0$. Then $\Phi$ is concave, and a positive point is a maximizer if and only if $\nabla \Phi = 0$ there. Green's paper uses a log-cosh penalty, which grows more slowly for large differences and keeps edges better; the algorithm is the same.

## The algorithm

```pseudo id=main
OSL(A, y, b, β, R, x0, K)                 ▷ x0 > 0; β ≥ 0; R is differentiable
L1  s_j ← Σ_i a_ij for each pixel j
L2  x ← x0
L3  for k ← 1 to K do
L4      ȳ ← A x + b                       ▷ the forward projection
L5      r_i ← y_i / ȳ_i for each bin i    ▷ r_i ← 0 if y_i = 0
L6      g ← A^T r                         ▷ the back projection of the ratios
L7      u ← ∇R(x)                         ▷ the penalty gradient at the old image
L8      d_j ← s_j + β u_j; fail if some d_j ≤ 0
L9      x_j ← x_j g_j / d_j for each pixel j
L10 return x
```

Lines L4 to L6 are the same as in MLEM. Line L7 is the only new work, and for a neighbor penalty it costs $O(n^2)$. Line L8 is where the method can fail: the code raises an error, because a zero denominator has no result and a negative one gives a negative pixel. Some codes clip $d_j$ to a small positive number instead; that hides the failure but does not fix it. With $\beta = 0$, OSL is MLEM.

## Example

Take two pixels, each seen by one bin: $A = I$, $b = 0$, counts $y = (1, 3)$, and one edge between the pixels with $w_{12} = 1$. Then $x_j g_j = y_j$ and line L9 reads $x_1 \leftarrow 1 / (1 + \beta (x_1 - x_2))$ and $x_2 \leftarrow 3 / (1 + \beta (x_2 - x_1))$. The start is the flat image $(2, 2)$. There the penalty gradient is 0, so the first iterate is the MLEM image $(1, 3)$ for every $\beta$.

| iteration | $\beta = 1/10$ | $\beta = 3/10$ | $\beta = 1$ |
|---|---|---|---|
| 1 | $(1, 3)$ | $(1, 3)$ | $(1, 3)$ |
| 2 | $(5/4, 5/2)$ | $(5/2, 15/8)$ | $d_1 = -1$: fails |
| 3 | $(8/7, 8/3)$ | $(16/19, 48/13)$ | |
| 4 | $(105/89, 315/121)$ | $(1235/179, 3705/2291)$ | |
| 5 | | $d_2 < 0$: fails | |
| maximizer of $\Phi$ | $(1.1696, 2.6200)$ | $(1.3948, 2.3382)$ | $(1.7071, 2.1213)$ |

For $\beta = 1/10$ the iterates converge to the maximizer, and $\Phi$ rises at each step in this run: $-0.9042$, $-0.8561$, $-0.8496$, $\ldots$ For $\beta = 3/10$ the late correction overshoots: the bright pixel becomes the dark one and back, with a growing amplitude. $\Phi$ falls from $-1.3042$ to $-1.6315$ in the second step, and the fifth step has a negative denominator. For $\beta = 1$, the second step would give $x_1 = 1/(1 - 2) = -1$. For $\beta = 1/2$ the denominator is exactly 0. In all three cases the maximizer is a positive point; only the iteration fails.

## Correctness

A positive $x$ with positive denominators is a fixed point of line L9 if and only if $g_j(x) = s_j + \beta u_j(x)$ for every $j$, that is $\partial \Phi / \partial x_j = 0$. Since $\Phi$ is concave for a convex penalty, a positive fixed point is a maximizer. So when OSL converges to a positive point, the limit is the right answer.

The update is not the maximizer of a surrogate of $\Phi$. Exact EM with a penalty leads to the coupled equations $x_j g_j(x) / x'_j - s_j - \beta u_j(x') = 0$, and OSL replaces $u_j(x')$ with $u_j(x)$. So the monotone argument of MLEM does not apply. The example above proves that $\Phi$ can decrease and that a denominator can become 0 or negative. A sufficient condition for a positive denominator at a nonnegative image is $\beta \sum_{k \sim j} w_{jk} x_k < s_j$, but it depends on the current image. Lange (1990) added a line search along the OSL step and proved that this modified method increases $\Phi$ and converges, under conditions on the penalty. The proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins and an $n \times n$ image, one iteration costs one forward and one back projection, $O(a d n)$, plus $O(n^2)$ for the gradient of a neighbor penalty. So it costs $O(a d n)$ time and $O(a d + n^2)$ extra space, and $K$ iterations cost $O(K a d n)$. The number of iterations to converge is not bounded by a theorem, and the method may not converge at all.

## Properties

- **The same cost as MLEM.** It needs only the projector pair and the penalty gradient.
- **Correct fixed points.** A positive limit is a maximizer of the penalized likelihood.
- **Not monotone.** $\Phi$ can decrease, as the example shows.
- **Not always positive.** The image stays positive only while every denominator is positive. A strong penalty or a steep edge can break this.
- **Converges for a small weight, in practice.** With a small $\beta$ the method behaves like MLEM, and it converges in the runs of the tests. This is an observation, not a theorem.
- **Not linear in the data**, like MLEM.

## Variants and improvements

- **OSL with a line search.** Lange (1990) searched along the step from $x$ to the OSL image for a point that raises $\Phi$. This gives a monotone method with a convergence proof.
- **Ordered subsets.** The OSL denominator can be used in each sub-iteration of [OSEM](/osem/). Then the penalty gradient is usually scaled by $1/T$ for $T$ subsets. The result has the same convergence problems as OSEM.
- **Other penalties.** Any differentiable penalty fits: log-cosh, Huber or a smoothed total variation. With total variation the method is used for deconvolution as [Richardson-Lucy with total variation](/richardson-lucy-total-variation/).
- **Monotone alternatives.** De Pierro's modified EM and [separable paraboloidal surrogates](/separable-paraboloidal-surrogates/) find a separable surrogate of the penalty too. They keep the monotone property for any $\beta$, at a similar cost per iteration.

## When to use it

Use OSL when you have an MLEM or OSEM code and want a quick penalized result with a small $\beta$, for example to reduce the noise without changing the code much. Check the denominators at each iteration. Use [SPS](/separable-paraboloidal-surrogates/) or another monotone method when $\beta$ is large, when you need a guarantee, or when the image must match the true maximizer, for example in a study of the penalty.

## Pitfalls

- **A large $\beta$.** The denominator can become 0 or negative. The failure can come after a few good steps, as in the $\beta = 3/10$ example.
- **Clipping the denominator.** Replacing a negative $d_j$ with a small positive number avoids the crash, but the iteration then has no relation to $\Phi$, and its limit is not the maximizer.
- **Assuming a monotone objective.** Do not test $\Phi$ for a monotone increase, and do not use its increase as a stopping rule.
- **A non-convex penalty.** With a non-convex penalty, $\Phi$ has many stationary points, and a fixed point need not be a maximizer.
- **The scale of $\beta$.** $\beta$ multiplies a penalty whose size depends on the units of $x$ and on the counts. A value that works for one scan can fail for another with more counts or a different matrix.

## Implementations

The Python code takes the system matrix as sparse rows of (column, weight) pairs, a list of edges with weights for the quadratic neighbor penalty, and works with float or `fractions.Fraction` data. It raises an error when a denominator is not positive. The tests check the iterates of the example exactly for $\beta = 1/10$, $3/10$, $1/2$ and $1$, the limit and the penalized KKT equations, the decrease of $\Phi$ and the failure for $\beta = 3/10$, the case $\beta = 0$ against MLEM, a fixed point on a random $4 \times 4$ problem, the penalty gradient against finite differences, and the adjoint test of the projector pair.

## History

Green published the one-step-late algorithm in 1990 in IEEE Transactions on Medical Imaging, for Bayesian reconstruction of emission tomography with a Gibbs prior. He noted that the exact M-step of EM with a penalty has no closed form, and he evaluated the derivative of the penalty at the current image to get one. In the same year, Lange showed that the plain method can fail and gave a convergent form with a line search. De Pierro (1995) later found a separable surrogate for the penalty, which gave monotone methods. The separable paraboloidal surrogates of Erdogan and Fessler (1999) built on that idea.

## References
