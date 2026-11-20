---
tag: DHVCDM
kind: algorithm
slug: maximum-entropy-method-imaging
name: Maximum entropy method for image reconstruction
aliases:
- MEM imaging
- maximum entropy deconvolution
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Choose the positive image of maximum entropy relative to a default image among those that fit the data within the noise, that is with chi-squared equal to the number of data."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, m: the number of data, K: the total number of Newton steps}
  time: {worst: Θ(m n^2 + K n^3), average: Θ(m n^2 + K n^3), best: Θ(m n^2 + K n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, iterative: true, linear: false, nonnegative: true, unique_solution: true, gaussian_noise_model: true}
history:
  year: 1972
  people: [B. Roy Frieden, Stephen F. Gull, G. J. Daniell, John Skilling, R. K. Bryan]
  note: Frieden (1972) restored images by maximum entropy. Gull and Daniell (1978) used it for radio maps with a chi-squared constraint, and Skilling and Bryan (1984) gave the robust general algorithm.
prereqs: [kullback-leibler-divergence, morozov-discrepancy-principle, image-deblurring]
see_also: [richardson-lucy-deconvolution, tikhonov-regularization, maximum-a-posteriori-estimation, hogbom-clean, dirty-image, aperture-synthesis, van-cittert-deconvolution, lagrangian-duality]
sources:
  - paper: doi:10.1364/JOSA.62.000511
    title: B. Roy Frieden, Restoring with maximum likelihood and maximum entropy, Journal of the Optical Society of America 62(4), 1972
    locator: pages 511 to 518
  - paper: doi:10.1038/272686a0
    title: S. F. Gull and G. J. Daniell, Image reconstruction from incomplete and noisy data, Nature 272, 1978
    locator: pages 686 to 690
  - paper: doi:10.1093/mnras/211.1.111
    title: J. Skilling and R. K. Bryan, Maximum entropy image reconstruction, general algorithm, Monthly Notices of the Royal Astronomical Society 211(1), 1984
    locator: pages 111 to 124 (the entropy metric, the subspace search and the control of chi-squared)
  - paper: doi:10.1146/annurev.aa.24.090186.001015
    title: R. Narayan and R. Nityananda, Maximum entropy image restoration in astronomy, Annual Review of Astronomy and Astrophysics 24, 1986
    locator: pages 127 to 170 (survey)
---

The maximum entropy method (MEM) reconstructs a positive image from blurred, noisy or incomplete data. Many images fit the data within the noise. MEM picks the one that is "least committal": the image of largest entropy relative to a default image $m$, among all images whose misfit $\chi^2$ is equal to its expected value, the number of data. In the form of Skilling, the entropy is $S(x) = \sum_j [x_j - m_j - x_j \log(x_j/m_j)]$, which is minus the generalized [Kullback-Leibler divergence](/kullback-leibler-divergence/) of $x$ from $m$. The logarithm forces every pixel to be positive, and with no data the answer is $m$. The method came from radio and optical astronomy, where Frieden (1972), Gull and Daniell (1978) and Skilling and Bryan (1984) developed it, and it competed with [CLEAN](/hogbom-clean/) for the deconvolution of [dirty images](/dirty-image/). It is a regularization of the [image deblurring](/image-deblurring/) problem, like [Tikhonov](/tikhonov-regularization/) with a different penalty, and it differs from [Richardson-Lucy](/richardson-lucy-deconvolution/), which maximizes a Poisson likelihood with no penalty and needs early stopping.

## In plain words

You have a blurred and noisy picture of the sky. Many sharp pictures, once blurred, look like the data up to the noise. Which one should you report? MEM says: report the one that adds the least structure that the data do not ask for. "Structure" is measured against a default picture, often flat, that you would report if you had no data. The entropy is high when the picture is close to the default and falls as the picture moves away from it. So you start at the default, and move away only as far as you must to explain the data to the level of the noise. Bright points that the data demand appear; wiggles that the data do not demand stay out. Because of the logarithm in the entropy, no pixel can go negative.

## The problem

The data are $y = Ax + e$ with a known real $m \times n$ matrix $A$ (for deblurring, the matrix of convolution with the PSF; for radio interferometry, a partial Fourier transform) and Gaussian noise $e_i \sim N(0, \sigma_i^2)$, independent. The misfit is $\chi^2(x) = \sum_i (y_i - (Ax)_i)^2/\sigma_i^2$, with the expected value $m$ at the true image. The default image $m_j > 0$ is given (a flat image with the right total flux is the usual choice). The problem is

$$\max_{x > 0}\ S(x) = \sum_j \Big[x_j - m_j - x_j \log\frac{x_j}{m_j}\Big] \quad\text{subject to}\quad \chi^2(x) = C,$$

with the target $C = m$, the number of data. With the Lagrange multiplier written as $\lambda/2$, the solution minimizes

$$F_\lambda(x) = -S(x) + \frac{\lambda}{2}\chi^2(x)$$

for the $\lambda > 0$ that gives $\chi^2 = C$. The stationary condition is $x_j = m_j \exp\big(-\lambda\,(A^TW(Ax - y))_j\big)$ with $W = \operatorname{diag}(1/\sigma_i^2)$: the image is the default times the exponential of a back projection of the residual, so it is positive by construction.

Frieden and Gull and Daniell wrote the entropy as $-\sum_j x_j\log(x_j/m_j)$ (or $-\sum x_j \log x_j$) with the total flux fixed; the extra term $\sum_j(x_j - m_j)$ of Skilling's form removes the need for that constraint.

## The algorithm

The implementation here is small and dense: an outer bisection on $\log\lambda$ and, for each $\lambda$, Newton steps on the convex function $F_\lambda$.

```pseudo id=main
MEM(y, A, sigma, m, C)                ▷ C = target chi^2, default the number of data
L1  lo ← 0;  hi ← 1;  grow hi by factors of 10 until chi^2(x_hi) ≤ C
L2  repeat until |chi^2(x) - C| ≤ tol · C
L3      lambda ← sqrt(lo · hi)
L4      x ← minimizer of F_lambda, from the last x, by Newton steps L5 to L8:
L5          g ← log(x / m) + lambda · A^T W (A x - y)
L6          H ← diag(1 / x) + lambda · A^T W A
L7          d ← -H^(-1) g
L8          x ← x + t d, with t = 1, 1/2, 1/4, ... until x > 0 and F_lambda falls enough
L9      if chi^2(x) > C then lo ← lambda else hi ← lambda
L10 return x, lambda
```

If $\chi^2(m) \le C$, the default image already fits, and it is the answer. Line L8 is a backtracking line search: it halves $t$ until the new point is positive and $F_\lambda$ falls by at least a quarter of the predicted decrease. The [discrepancy principle](/morozov-discrepancy-principle/) with $\chi^2 = m$ is the classic choice of $\lambda$.

**The Skilling-Bryan algorithm.** For large images, $H$ cannot be formed. Skilling and Bryan (1984) instead search, in each iteration, a subspace of three to six directions built from $\nabla S$ and $\nabla\chi^2$, measured in the entropy metric $\operatorname{diag}(x)$ (the inverse of the entropy Hessian). They fit quadratic models of $S$ and $\chi^2$ in the subspace, and take a step that raises $S$ and lowers $\chi^2$ toward the target, with a limit on the step length in the entropy metric. Each iteration then costs a few applications of $A$ and $A^T$.

## Example

**Two pixels by hand.** Take $A = I$, $\sigma = (1, 1)$, $m = (1, 1)$ and $y = (4, 1)$, with the target $C = 2$. The second pixel already equals its default and its datum, so $x_2 = 1$. For the first pixel the stationary condition is $\log x_1 = -\lambda(x_1 - 4)$, and the constraint is $(x_1 - 4)^2 = 2$. Entropy pulls $x_1$ toward $m_1 = 1$, so $x_1 = 4 - \sqrt 2 = 2.58579$, and then $\lambda = \log(2.58579)/\sqrt 2 = 0.67177$ and $S = x_1 - 1 - x_1\log x_1 = -0.87079$. The code gets these values.

**A blurred spike train.** A measurement on one seed: $n = 16$ pixels, a periodic blur with weights $(0.1, 0.2, 0.4, 0.2, 0.1)$, the true image $1$ everywhere except $9$, $5$ and $7$ at pixels 5, 6 and 11, Gaussian noise with $\sigma = 0.3$, and a flat default equal to the mean of the data, $2.077$. The flat default has $\chi^2 = 219.1$. The table gives the minimizer of $F_\lambda$ for several $\lambda$:

| $\lambda$ | $\chi^2$ | $S$ | error $\lVert x - x^\dagger\rVert$ | smallest pixel | pixels 5, 6, 11 |
|---|---|---|---|---|---|
| 0.01 | 179.72 | -0.092 | 9.339 | 1.894 | 2.44, 2.36, 2.17 |
| 0.1 | 64.63 | -2.456 | 7.045 | 1.230 | 4.46, 3.56, 2.86 |
| 0.4536 | 16.00 | -7.447 | 4.487 | 0.633 | 6.90, 4.16, 3.97 |
| 1 | 6.85 | -10.439 | 3.548 | 0.375 | 8.02, 4.21, 4.52 |
| 10 | 1.15 | -17.121 | 3.061 | 0.003 | 9.80, 4.14, 5.45 |
| 100 | 0.90 | -19.405 | 3.255 | 0.000 | 10.25, 4.02, 5.72 |

The bisection stops at $\lambda = 0.4536$, where $\chi^2 = 16$. As $\lambda$ grows, $\chi^2$ and $S$ both fall, as Claim 4 of the proof says. The peaks come back, and every pixel stays positive. In this run the image with $\chi^2 = 16$ is smoother than the one with the smallest error ($\lambda = 10$): the classic target $\chi^2 = m$ tends to under-fit, a known weakness that led Gull (1989) to a Bayesian choice of $\lambda$.

## Correctness

The full proof is in `proofs/correctness.md`. The main facts, for $A$ real, $\sigma_i > 0$ and $m_j > 0$:

1. **Unique minimizer for each $\lambda$.** $F_\lambda$ is strictly convex on $x \ge 0$, its sublevel sets are bounded, and its minimizer $x_\lambda$ has all pixels positive (the entropy has slope $+\infty$ at $0$). It satisfies $x_j = m_j\exp(-\lambda(A^TW(Ax - y))_j)$.
2. **Newton steps are safe.** $H$ is positive definite, so $d$ is a descent direction, the line search ends, and $F_\lambda$ never increases.
3. **Maximum entropy.** If $\chi^2(x_\lambda) = C$, then $S(x_\lambda) \ge S(x)$ for every $x > 0$ with $\chi^2(x) \le C$.
4. **Monotone trade-off.** $\chi^2(x_\lambda)$ and $S(x_\lambda)$ are nonincreasing in $\lambda$.
5. **Existence of $\lambda$.** If $\inf_{x \ge 0}\chi^2(x) < C < \chi^2(m)$, a $\lambda > 0$ with $\chi^2(x_\lambda) = C$ exists, and the bisection finds it.

## Complexity

In the real-RAM model, with $n$ pixels and $m$ data, forming $A^TWA$ once costs $\Theta(mn^2)$, and each Newton step costs $\Theta(n^3)$ for the dense solve plus $\Theta(mn)$ for the gradient. So $K$ Newton steps in total cost $\Theta(mn^2 + Kn^3)$, with $\Theta(n^2)$ extra space for $H$. This dense form is for small problems; in the table above each $\lambda$ needed 3 to 9 Newton steps, and 52 steps at $\lambda = 100$, where pixels come close to $0$ and the line search cuts the steps (a measurement). The Skilling-Bryan form costs a few applications of $A$ and $A^T$ per iteration, $O(n\log n)$ each for a convolution done with the [FFT](/fast-fourier-transform/), and needs $O(n)$ extra space; no bound on the number of its iterations is known in general.

## Properties

- Positive: every output pixel is positive, without clipping.
- Nonlinear in the data, and unique: for each $\lambda$ there is one image, and the image with $\chi^2 = C$ is unique when it exists.
- With no information in the data about a pixel, the pixel goes to its default.
- The total flux is not a constraint of Skilling's form. In the example the output has the flux 33.83, the data 33.24 and the true image 34 (a measurement).
- The image depends on the default $m$ and on the target $C$.
- MEM smooths flat, low-level regions strongly and keeps bright points sharp, so its resolution depends on the brightness (Narayan and Nityananda 1986 discuss this).

## Variants and improvements

- **Bayesian MEM.** Treat $\exp(\alpha S(x))$ as a prior and choose $\alpha = 1/\lambda$ by its evidence ("classic MaxEnt", Gull 1989; Skilling 1989) instead of $\chi^2 = m$. This is the [MAP estimate](/maximum-a-posteriori-estimation/) with an entropy prior, with a rule for the weight.
- **Poisson data.** Replace $\chi^2$ by the Poisson negative log-likelihood. Iterations of Richardson-Lucy type with an entropy term then apply.
- **Multichannel and intrinsic correlation function.** Put the entropy on a hidden image and blur it to get the visible one, so that the result is smooth on a chosen scale (Gull 1989).
- **Radio interferometry.** $A$ is the sampled Fourier transform, the data are visibilities, and MEM fills in the unsampled spatial frequencies with values that keep the image positive and smooth (see [aperture synthesis](/aperture-synthesis/)). Cornwell and Evans (1985) gave a widely used form.
- **Dual methods.** The problem has a smooth unconstrained dual over the data space, since $x$ is an exponential of $A^T\mu$; this is useful when $m \ll n$ (see [Lagrangian duality](/lagrangian-duality/)).

## When to use it

Use MEM for positive images with a large dynamic range and a few bright features on a faint background, such as radio maps, spectra and some astronomical images, when the noise is close to Gaussian with a known level and you want a single best image with no negative values. For photon counts, Richardson-Lucy or a Poisson MAP method fits the noise better. For extended objects with sharp borders, total variation methods often keep edges better. When the noise level is unknown, the target $\chi^2 = m$ cannot be set, and a Bayesian choice of $\lambda$ is needed.

## Pitfalls

- The target $\chi^2 = m$ is a heuristic. The expected value of $\chi^2$ at the true image is $m$, but the fitted image has fewer degrees of freedom left, so the target tends to under-fit, as in the example.
- The result depends on the default image. A flat default with the wrong total flux biases the whole image.
- The entropy is not invariant to a change of pixel size or of the zero level. A background that is not subtracted becomes part of the "positive image", and a negative true signal cannot be represented at all.
- Resolution varies across the image: bright points are sharp and faint regions are smooth. Do not compare widths of features of different brightness.
- Plain gradient ascent on $S - \lambda\chi^2/2$ is slow and unstable because the curvature of the entropy, $1/x_j$, varies over many orders of magnitude. Use the entropy metric or Newton steps.
- If the target is below the smallest misfit any positive image can reach, no solution exists. The code then raises an error.

## Implementations

## History

E. T. Jaynes (1957) proposed maximum entropy as a rule of inference. B. R. Frieden (1972) applied it to image restoration. S. F. Gull and G. J. Daniell (1978) used it for radio astronomy maps from incomplete and noisy data, with the chi-squared constraint, and showed its good behavior on positive images. J. Skilling and R. K. Bryan (1984) gave the general algorithm with the entropy metric and the subspace search that made the method robust for large images, and the MEMSYS programs spread it. R. Narayan and R. Nityananda (1986) reviewed the method for astronomy. Later work by Gull and Skilling turned it into a Bayesian method with a rule for the regularization weight.

## References
