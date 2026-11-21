---
tag: 83T1AZ
kind: algorithm
slug: mlem-reconstruction
name: Maximum likelihood expectation maximization reconstruction
aliases:
- MLEM
- Shepp-Vardi algorithm
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Maximize the Poisson likelihood of emission data by multiplying the image by the back-projected ratio of measured to predicted counts, keeping it nonnegative.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of iterations"}
  time: {per_iteration: "O(a d n)", total: "O(K a d n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, iterative: true, in_place: false, recursive: false, monotone_likelihood: true, keeps_nonnegativity: true, linear_in_data: false}
history:
  year: 1982
  people: [Lawrence A. Shepp, Yehuda Vardi]
  note: Shepp and Vardi applied the EM algorithm to the Poisson model of positron emission tomography.
prereqs: [emission-tomography-model, expectation-maximization, back-projection-operator]
see_also: [osem, one-step-late-algorithm, separable-paraboloidal-surrogates, richardson-lucy-deconvolution, sirt, semi-convergence, kullback-leibler-divergence, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1109/TMI.1982.4307558
    title: L. A. Shepp and Y. Vardi, Maximum likelihood reconstruction for emission tomography, IEEE Transactions on Medical Imaging 1(2), 1982
    locator: pp. 113 to 122 (the EM algorithm for the Poisson model of PET)
  - paper: "K. Lange and R. Carson, EM reconstruction algorithms for emission and transmission tomography, Journal of Computer Assisted Tomography 8(2), 1984"
    locator: the EM update for emission data and its monotone likelihood (general locator)
  - paper: doi:10.1080/01621459.1985.10477119
    title: Y. Vardi, L. A. Shepp and L. Kaufman, A statistical model for positron emission tomography, Journal of the American Statistical Association 80(389), 1985
    locator: pp. 8 to 20 (the convergence of the EM iterates to a maximum likelihood estimate)
  - paper: "I. Csiszar and G. Tusnady, Information geometry and alternating minimization procedures, Statistics and Decisions, Supplement Issue 1, 1984"
    locator: pp. 205 to 237 (the convergence of alternating minimization of the Kullback-Leibler divergence)
---

MLEM computes the maximum likelihood image of the [emission tomography model](/emission-tomography-model/). The counts are $y_i \sim \operatorname{Poisson}(\bar y_i)$ with $\bar y = A x + b$, where $A$ is a nonnegative $m \times N$ system matrix, $b \ge 0$ a known background and $x \ge 0$ the activity image. Each iteration projects the current image, divides the measured counts by the predicted counts, back-projects the ratios, and multiplies the image by the result, pixel by pixel: $x_j \leftarrow (x_j / s_j) \sum_i a_{ij} y_i / \bar y_i$ with $s_j = \sum_i a_{ij}$. It is the [EM algorithm](/expectation-maximization/) for this model. The update keeps the image nonnegative, never decreases the likelihood, and with $b = 0$ converges to a maximizer. With noisy data the maximizer is noisy, so in practice the iteration is stopped early. The same update for a convolution is [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/).

## In plain words

A scanner counts photons from a tracer in the body. Each detector bin sees the photons from the pixels along its line. MLEM starts with a flat image that has no negative values. It computes how many counts the image would give in each bin. Then it compares these numbers with the measured counts, bin by bin, as a ratio.

A ratio above 1 says that the image is too dark along that line. A ratio below 1 says that it is too bright. Each pixel collects the ratios of all bins that see it and takes their weighted average. Then it multiplies its value by this average. A pixel never becomes negative, because it only gets multiplied by a positive number. Each step makes the measured counts more probable for the image. Too many steps make the image fit the random noise of the counts.

## The problem

Given the counts $y \in \{0, 1, 2, \ldots\}^m$, a matrix $A$ with $a_{ij} \ge 0$ and positive column sums $s_j = \sum_i a_{ij}$, and a background $b \ge 0$, maximize the Poisson log-likelihood
$$L(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i\big], \qquad \bar y = A x + b,$$
over $x \ge 0$. The constant $-\sum_i \log y_i!$ is left out. Maximizing $L$ is the same as minimizing the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $\operatorname{KL}(y, A x + b)$. $L$ is concave, and $\hat x$ is a maximizer if and only if the [KKT conditions](/kkt-conditions/) hold: $\sum_i a_{ij} y_i / \bar y_i \le s_j$ for each $j$, with equality where $\hat x_j > 0$.

## The algorithm

```pseudo id=main
MLEM(A, y, b, x0, K)                      ▷ x0 > 0 in every pixel; b ≥ 0 is known
L1  s_j ← Σ_i a_ij for each pixel j       ▷ the sensitivity image, A^T 1
L2  x ← x0
L3  for k ← 1 to K do
L4      ȳ ← A x + b                       ▷ the forward projection
L5      r_i ← y_i / ȳ_i for each bin i    ▷ r_i ← 0 if y_i = 0
L6      g ← A^T r                         ▷ the back projection of the ratios
L7      x_j ← x_j g_j / s_j for each pixel j
L8  return x
```

Line L1 runs once. Each iteration does one forward projection (line L4) and one back projection (line L6). Line L6 must use the transpose of the matrix of line L4, and $s$ must be the column sums of the same matrix, or the theory below does not hold. A common start is the constant image whose projections have the measured total count; the code uses it by default. In the EM view, the complete data are the unobserved counts $z_{ij} \sim \operatorname{Poisson}(a_{ij} x_j)$ from pixel $j$ in bin $i$. The E-step estimates them by $\mathbb{E}[z_{ij} \mid y] = y_i a_{ij} x_j / \bar y_i$, and the M-step sets $x_j$ to $\sum_i \mathbb{E}[z_{ij} \mid y] / s_j$. This is line L7.

## Example

Take a $2 \times 2$ image $x = (x_0, x_1, x_2, x_3)$ in row-major order, no background, and five rays with weights 0 or 1: the two rows, the two columns and the diagonal through $x_0$ and $x_3$. The counts are the exact projections of $(1, 2, 3, 4)$: $y = (3, 7, 4, 6, 5)$. The sensitivities are $s = (3, 2, 2, 3)$. Start from $x = (1, 1, 1, 1)$, so $\bar y = (2, 2, 2, 2, 2)$. Line L5 gives $r = (3/2, 7/2, 2, 3, 5/2)$. Line L6 gives $g_0 = 3/2 + 2 + 5/2 = 6$, $g_1 = 3/2 + 3 = 9/2$, $g_2 = 7/2 + 2 = 11/2$ and $g_3 = 7/2 + 3 + 5/2 = 9$. Line L7 multiplies by $x_j / s_j$:

| iteration | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $L(x)$ |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 7.3287 |
| 1 | 2 | 9/4 | 11/4 | 3 | 15.8143 |
| 2 | 1646/969 = 1.6987 | 495/238 = 2.0798 | 2475/874 = 2.8318 | 541/161 = 3.3602 | 16.0627 |
| 3 | 1.5091 | 1.9726 | 2.8508 | 3.6086 | 16.1712 |

The likelihood rises at each step toward its maximum $L(1, 2, 3, 4) = 16.2601$. After iteration 1 the weighted sum $\sum_j s_j x_j$ equals the total count 25, and it stays there. The error $\max_j |x_j - x^\dagger_j|$ is $0.13$ after 10 iterations, $1.7 \cdot 10^{-3}$ after 50 and $8.2 \cdot 10^{-6}$ after 100. The iterates are rational, but their denominators grow fast: iteration 3 already has 16 digits in each denominator.

A larger case. The image is $16 \times 16$ on $[-1, 1]^2$, with pixel $(i, j)$ centered at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$. The object is a disk of radius 0.6 with value 1, scanned at 12 angles in $[0, \pi)$ with 23 bins and the pixel-driven matrix of the shared helper. With exact mean data (5 times the projections), the relative error $\|x_k - x\| / \|x\|$ is $0.63$ after 1 iteration, $0.19$ after 10, $0.13$ after 50, $0.11$ after 100 and $0.066$ after 300. With Poisson counts of mean 50 times the projections (seed 7, 5676 counts in total), the error of $x_k / 50$ is smallest, $0.235$, at $k = 10$. Then it rises to $0.41$ at $k = 50$, $0.47$ at $k = 100$ and $0.56$ at $k = 300$, while the likelihood still rises. This is [semi-convergence](/semi-convergence/). These numbers are measurements of this setup, not properties of the method.

## Correctness

Fix a positive $x$ with $\bar y_i > 0$ wherever $y_i > 0$. The weights $a_{ij} x_j / \bar y_i$ and $b_i / \bar y_i$ are nonnegative and sum to 1 over $j$. Jensen's inequality for the concave logarithm then gives, for every $x' \ge 0$,
$$L(x') \ge Q(x'; x) = \text{const} + \sum_j \Big[x_j g_j \log x'_j - s_j x'_j\Big], \qquad g_j = \sum_i a_{ij} \frac{y_i}{\bar y_i},$$
with equality at $x' = x$. The surrogate $Q$ splits into one concave function per pixel, and the maximizer of $x_j g_j \log t - s_j t$ is $t = x_j g_j / s_j$, the update of line L7. So $L(x^{k+1}) \ge Q(x^{k+1}; x^k) \ge Q(x^k; x^k) = L(x^k)$: the likelihood never decreases. It increases strictly unless $x^{k+1} = x^k$. This is a minorize-maximize argument, and it is the EM monotonicity for this model.

Three more facts follow from the update.

- **Positivity.** A positive pixel stays positive if some bin that sees it has counts. A zero pixel stays zero.
- **The total count.** With $b = 0$, $\sum_j s_j x^{k+1}_j = \sum_i y_i$ after every iteration.
- **Fixed points.** A positive $x$ is a fixed point if and only if $\partial L / \partial x_j = g_j - s_j = 0$ for all $j$. A maximizer is a fixed point. A fixed point with zero pixels need not be a maximizer, which is why the start must be positive.

With $b = 0$ and a positive start, the iterates converge to a maximizer of $L$. Vardi, Shepp and Kaufman (1985) proved this for PET, and Csiszar and Tusnady (1984) proved it for alternating minimization of the KL divergence, of which MLEM is a case. The proofs of monotonicity, positivity, the count and the fixed points are in [proofs/correctness.md](proofs/correctness.md); the convergence is cited there.

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins each ($m = a d$ bins) and an $n \times n$ image ($N = n^2$ pixels):

- Line L1 takes one pass over the nonzero entries of $A$. A ray-driven projector has $O(n)$ entries per bin, so $\operatorname{nnz}(A) = O(a d n)$.
- Lines L4 and L6 take $O(a d n)$ each. Lines L5 and L7 take $O(a d)$ and $O(n^2)$.

So one iteration costs $O(a d n)$ time and $O(a d + n^2)$ extra space, and $K$ iterations cost $O(K a d n)$. The number of iterations is the regularization parameter. No bound on the right $K$ follows from the model: without a known noise level, every stopping rule for MLEM is a heuristic. The error of the slow components falls slowly, and in the small example above the error shrinks by a factor of about 3 every 10 iterations.

## Properties

- **Nonnegative.** The update multiplies by nonnegative numbers, so no projection onto $x \ge 0$ is necessary.
- **Monotone likelihood.** $L(x^k)$ never decreases. This is a theorem (see Correctness). The error against the true image is not monotone with noise.
- **A scaled gradient step.** Line L7 equals $x_j + (x_j / s_j)\, \partial L / \partial x_j$. So MLEM is gradient ascent with the step $x_j / s_j$ for pixel $j$. The step is small where the pixel is small, which keeps the pixel positive.
- **Count preserving.** With $b = 0$ the predicted total count equals the measured one after each iteration.
- **Not linear in the data.** The iterate depends on $y$ in a nonlinear way, unlike [SIRT](/sirt/) without the positivity step. So its noise cannot be written in closed form.
- **Slow at fine detail.** In practice the coarse structure of the image appears in a few iterations and fine detail needs many. This is an observation, and it is why [OSEM](/osem/) is used.

## Variants and improvements

- **OSEM.** Apply the update with one subset of the bins at a time. One pass over the subsets costs about as much as one MLEM iteration and does about as much work as several. See [OSEM](/osem/).
- **Penalized likelihood.** Add a penalty $-\beta R(x)$ to $L$. The [one-step-late algorithm](/one-step-late-algorithm/) of Green (1990) puts the gradient of $R$ at the old image into the denominator of line L7. [Separable paraboloidal surrogates](/separable-paraboloidal-surrogates/) minimize a separable quadratic majorizer and keep the monotone property with a penalty.
- **Transmission data.** Lange and Carson (1984) gave an EM algorithm for the transmission model too. Its M-step has no closed form.
- **Richardson-Lucy.** For a convolution matrix $A$ with $\sum_i a_{ij} = 1$, the update is [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/).
- **List mode and time of flight.** The same update works on a list of single events instead of binned counts. Time of flight adds a position along each line to the model, which only changes $A$.
- **Post-filtering.** Run many iterations and smooth the result. It is a common practice, but its choice of the filter is a heuristic.

## When to use it

Use MLEM for emission data with low counts, where the Poisson model matters and [filtered back-projection](/filtered-back-projection/) gives streaks. It needs only a forward and a back projector, it handles any geometry and any known background, and it keeps the image nonnegative. Use it as the reference method when you test a faster variant: OSEM, for example, should give a similar image in fewer passes. For a reproducible result, fix the number of iterations or add a penalty, because the image depends on where you stop. For high counts, a weighted least squares method is also good.

## Pitfalls

- **A zero start.** A pixel that starts at 0 stays at 0. Start with a positive image.
- **Division by zero.** A bin with $y_i > 0$ and $\bar y_i = 0$ makes line L5 fail. This happens if the bin sees no pixel and $b_i = 0$. Remove such bins, or give them a small background.
- **Precorrected data.** If the data have random coincidences subtracted, some counts can be negative and the model is wrong. Put the estimate in $b$ and keep the raw counts.
- **A mismatched back projector.** If line L6 does not use $A^T$, or $s$ is not $A^T \mathbf{1}$ for the same $A$, the likelihood can decrease and the limit is not the maximum likelihood image.
- **Too many iterations.** With noise, the image becomes noisy as $k$ grows, while the likelihood still increases. The rise of $L$ is not a sign of a better image.
- **Expecting a unique answer.** If $A$ does not have full column rank, the maximizer is not unique, and the limit depends on the start.

## Implementations

The Python code takes the system matrix as sparse rows of (column, weight) pairs, as built by the shared helper `imgkit.parallel_beam_matrix` or by any projector page, and works with float or `fractions.Fraction` data. The tests check the worked example exactly, the total count, the convergence on a consistent system, the monotone likelihood and the positivity on random problems with background, the KKT conditions at the limit, the adjoint test of the projector pair, and the disk phantom with exact and with noisy counts.

## History

Richardson (1972) and Lucy (1974) used the same multiplicative update to deblur images in optics and astronomy. Dempster, Laird and Rubin named and analyzed the general EM algorithm in 1977. Shepp and Vardi (1982) introduced the Poisson model of positron emission tomography and derived MLEM as its EM algorithm. Lange and Carson (1984) gave EM algorithms for emission and for transmission tomography. Vardi, Shepp and Kaufman (1985) proved the convergence for emission data, and Csiszar and Tusnady (1984) proved the convergence of alternating minimization of the KL divergence in general. The slow convergence led to OSEM in 1994, which made the method practical in the clinic.

## References
