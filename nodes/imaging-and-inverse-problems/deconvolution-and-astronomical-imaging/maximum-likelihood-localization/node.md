---
tag: XKDP82
kind: algorithm
slug: maximum-likelihood-localization
name: Maximum likelihood emitter localization
aliases:
- MLE single-molecule fitting
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: Fit a pixel-integrated Gaussian PSF to the photon counts of one emitter by Newton steps on the Poisson likelihood. For large photon counts and a correct PSF it nears the Cramer-Rao bound.
solves: [single-molecule-localization]
model: real-ram
complexity:
  vars: {P: the number of pixels in the fitting window, K: the number of iterations}
  time: {worst: Θ(K P), average: Θ(K P), best: Θ(P)}
  space: {extra: Θ(P)}
properties: {deterministic: true, iterative: true, monotone_likelihood: true, returns_uncertainty: true, model_based: true}
history:
  year: 2010
  people: [Carlas S. Smith, Nikolai Joseph, Bernd Rieger, Keith A. Lidke, Kim I. Mortensen, L. Stirling Churchman, James A. Spudich, Henrik Flyvbjerg]
  note: "In 2010 Smith and coworkers fitted a pixel-integrated Gaussian by Newton-Raphson steps on the Poisson likelihood on a graphics processor, and Mortensen and coworkers compared maximum likelihood and least squares fitting with the Cramer-Rao bound."
prereqs: [maximum-likelihood-estimation, poisson-distribution, point-spread-function, newton-raphson-method]
see_also: [localization-precision-formula, cramer-rao-bound, fisher-information-matrix, fisher-scoring, backtracking-line-search, levenberg-marquardt, gauss-newton-algorithm, image-noise]
sources:
  - paper: doi:10.1038/nmeth.1449
    title: "C. S. Smith, N. Joseph, B. Rieger and K. A. Lidke, Fast, single-molecule localization that achieves theoretically minimum uncertainty, Nature Methods 7(5), 2010, 373 to 375"
    locator: "the pixel-integrated Gaussian model, the Poisson likelihood, its first and second derivatives, the Newton-Raphson iteration and the comparison of the variance with the Cramer-Rao bound"
  - paper: doi:10.1038/nmeth.1447
    title: "K. I. Mortensen, L. S. Churchman, J. A. Spudich and H. Flyvbjerg, Optimized localization analysis for single-molecule tracking and super-resolution microscopy, Nature Methods 7(5), 2010, 377 to 381"
    locator: "maximum likelihood against least squares fitting, the precision formulas for both, and the comparison with the information limit"
  - paper: doi:10.1016/S0006-3495(04)74193-4
    title: "R. J. Ober, S. Ram and E. S. Ward, Localization accuracy in single-molecule microscopy, Biophysical Journal 86(2), 2004, 1185 to 1200"
    locator: the Fisher information of the photon detection process and the resulting limit of the localization accuracy
---

Maximum likelihood localization estimates the position of one fluorescent emitter from a small camera image to a precision far below the width of the point spread function (PSF). It models the expected photon count of each pixel as a Gaussian PSF integrated over the pixel, times the photon count of the emitter, plus a constant background, and treats the counts as independent Poisson values. It then finds the center, the photon count and the background that make the observed counts most likely, by Newton steps on the negative log likelihood with a line search. It also returns the inverse Fisher information at the estimate, the Cramer-Rao bound, as an estimate of the uncertainty. For large photon counts and a correct PSF model, the variance of the estimate comes close to this bound, which no unbiased estimator can beat; for small counts or a wrong PSF it does not. It is the fitting step of [single-molecule localization](/single-molecule-localization/) microscopy.

## In plain words

A single glowing molecule shows up on a camera as a small blurred spot a few pixels wide. Each pixel counts the photons that hit it, and the counts are random. The method guesses where the spot's center is, how bright it is and how bright the background is, and predicts the count of each pixel. It then asks how likely the real counts are under that guess, and improves the guess until the likelihood cannot get higher. Because many photons together pin down the center, the center can be found to a few nanometers, even though the spot is hundreds of nanometers wide.

## The problem

The input is a window of $P$ pixels with photon counts $c$ around one emitter, and the known PSF width $s$ in pixels. The model is $\mu(u, v) = N E_x(u) E_y(v) + b$, where pixel $(v, u)$ covers a unit square, $E_x(u) = \frac12[\operatorname{erf}((u - x_0 + \frac12)/(\sqrt2 s)) - \operatorname{erf}((u - x_0 - \frac12)/(\sqrt2 s))]$ is the share of the PSF in column $u$, and $E_y$ is the same for the rows. The counts are independent Poisson with the means $\mu$. The goal is the maximum likelihood estimate of $\theta = (x_0, y_0, N, b)$, that is the minimizer of $L(\theta) = \sum(\mu - c\log\mu)$, and its uncertainty.

## The algorithm

```pseudo id=main
MLE-LOCALIZE(c, s)
L1  θ ← (centroid of c - b₀, total of c - b₀, b₀), with b₀ the mean of the border pixels
L2  repeat at most max_iter times
L3      compute L, ∇L, ∇²L and the Fisher information I(θ) = Σ ∇μ ∇μᵀ / μ
L4      if ∇²L is positive definite: δ ← -(∇²L)⁻¹ ∇L   ▷ Newton step, by Cholesky
L5      else δ ← -I(θ)⁻¹ ∇L                           ▷ Fisher scoring step
L6      halve t from min(1, 1/|δ_center|) until N > 0, the center is in the window and L(θ + tδ) ≤ L(θ) + 10⁻⁴ t ∇Lᵀδ
L7      θ ← θ + tδ; stop when the step is below the tolerance
L8  crb ← I(θ)⁻¹
L9  return θ, crb
```

In line L6, $|\delta_{\text{center}}|$ is the larger of $|\delta_{x_0}|$ and $|\delta_{y_0}|$, so a step moves the center by at most one pixel. The gradient is $\nabla L = \sum (1 - c/\mu)\nabla\mu$ and the Hessian is $\sum (c/\mu^2)\nabla\mu\nabla\mu^T + (1 - c/\mu)\nabla^2\mu$. The derivatives of $E_x$ are differences of the normal density $g$: $E_x' = g(t_2) - g(t_1)$ and $E_x'' = (t_2 g(t_2) - t_1 g(t_1))/s^2$, with $t_{1,2} = u - x_0 \pm \frac12$.

## Example

Take a $9 \times 9$ window, $s = 1.3$ pixels and the true $\theta = (4.3, 3.8, 500, 2)$. One Poisson image (seed $2$ in the test file) has $676$ counts. The start from line L1 is $(4.400, 3.783, 515.75, 2.31)$. The iterates are:

| step | $x_0$ | $y_0$ | $N$ | $b$ | $L$ |
|---|---|---|---|---|---|
| 0 | 4.4000 | 3.7832 | 515.75 | 2.3125 | $-1118.4983$ |
| 1 | 4.4468 | 3.7881 | 510.17 | 2.0370 | $-1119.4874$ |
| 2 | 4.4457 | 3.7881 | 509.57 | 2.0647 | $-1119.4954$ |
| 3 | 4.4457 | 3.7881 | 509.56 | 2.0650 | $-1119.4954$ |

The returned bound gives the standard deviations $0.070$, $0.070$, $26.0$ and $0.225$. The error in $x_0$ is $0.146$ pixels, about two standard deviations: one image is one random draw. Over $200$ images (seed $11$) the sample variances of $x_0$ and $y_0$ are $1.08$ and $1.02$ times the bound (a measurement). Without noise, that is with $c = \mu(\theta)$, the fit returns $\theta$ to $10^{-6}$ from the centroid start and from three poor starts.

With $s = 100$ nm, pixels of $100$ nm, $N = 1000$ and almost no background, the bound on the standard deviation of $x_0$ is $3.2914$ nm, against $s/\sqrt N = 3.1623$ nm for infinitely small pixels.

## Correctness

The proof is in `proofs/correctness.md`. The facts:

1. **Derivatives (theorem).** The formulas for $E_x'$, $E_x''$, $\nabla L$ and $\nabla^2 L$ are exact, and $I(\theta) = \mathbb E[\nabla^2 L]$.
2. **Descent (theorem).** The Newton step, when the Hessian is positive definite, and the scoring step otherwise are descent directions, and the line search ends with a decrease of $L$. So $L$ never increases.
3. **Noise-free data (theorem).** For $c = \mu(\theta^*)$, $\theta^*$ is a global minimizer of $L$, and a strict local minimizer when $I(\theta^*)$ is positive definite.
4. **The bound (theorem).** Every unbiased estimator has a covariance of at least $I(\theta)^{-1}$, the [Cramer-Rao bound](/cramer-rao-bound/). The maximum likelihood estimate reaches it only asymptotically, for large photon counts and a correct model (a standard theorem). For a finite count the closeness is a measurement.
5. **Convergence.** Convergence to a stationary point and the local quadratic rate of Newton steps are standard results for line search methods, not proved in the proof file.

## Complexity

One iteration evaluates two error functions and two exponentials per row and per column, then sums $4 \times 4$ outer products over the $P$ pixels: $\Theta(P)$ time. The $4 \times 4$ Cholesky factorization costs $O(1)$, and each trial of the line search costs $\Theta(P)$. With $K$ iterations and a bounded number of halvings per iteration, a fit costs $\Theta(KP)$, and $K$ is usually below $10$. The extra space is $\Theta(P)$ for the derivatives of the pixels. In a localization movie the fits of different spots are independent, so they run in parallel; Smith and coworkers ran them on a graphics processor.

## Properties

- **Uses the right noise model.** Photon counts are Poisson, so pixels with more light have more noise. Least squares weights all pixels the same and loses precision; Mortensen and coworkers found that its variance is larger than the bound.
- **Monotone.** The negative log likelihood never increases (Claim 3 of the proof).
- **Gives an uncertainty.** The bound at the estimate is a cheap estimate of the precision of each spot, useful for filtering and for rendering.
- **Model dependent.** The Gaussian PSF is an approximation of the real PSF. A wrong PSF width, a tilted dipole or defocus bias the result.
- **Local.** Like every Newton method, it needs a start in the basin of the true minimum. The centroid start is good for one isolated spot.

## Variants and improvements

- **Exact PSF models.** Replace the Gaussian by an Airy or vectorial PSF, or by a measured PSF, at a higher cost per pixel.
- **Free width.** Fit $s$ too, as a fifth parameter, to catch out-of-focus spots and overlapping emitters.
- **3D by astigmatism.** With a cylindrical lens the widths $s_x$ and $s_y$ depend on the depth $z$, and fitting both gives $z$.
- **Camera noise.** For EMCCD cameras the excess noise factor doubles the variance at high gain; for sCMOS cameras each pixel has its own read noise and gain, which can be added to the likelihood.
- **Several emitters.** Fit two or more emitters in one window when spots overlap, and choose the number by a likelihood ratio test.
- **Other optimizers.** [Levenberg-Marquardt](/levenberg-marquardt/) on the Poisson likelihood, or [Fisher scoring](/fisher-scoring/) at every step, which needs no second derivatives.

## When to use it

Use maximum likelihood fitting for each spot in [PALM, STORM](/single-molecule-localization/) and single-particle tracking, when the precision matters and the PSF is known well. Least squares fitting is simpler and close in precision at high background. A centroid is fastest but biased by the background and far from the bound. When the emitters are too dense for isolated spots, use a multi-emitter fit, a sparse recovery method, or [SOFI](/sofi/).

## Pitfalls

- **Wrong pixel units.** The counts must be photons, not camera units. Convert with the gain and the offset first, or the Poisson model and the bound are wrong.
- **Reading the bound as the error.** The bound is the precision of an ideal unbiased estimator under the model. Drift, a wrong PSF and too few photons make the real error larger.
- **Bad starts.** A start far from the spot can make the photon count go to $0$, and then the position is not defined. The code limits each move of the center to one pixel and keeps it inside the window.
- **Overlapping spots.** Two emitters in one window bias a single emitter fit toward their middle.

## Implementations

## History

Thompson, Larson and Webb (2002) gave the precision of least squares fitting, and Ober, Ram and Ward (2004) derived the limit from the Fisher information of the detection process. In 2010 Smith and coworkers fitted the pixel-integrated Gaussian by Newton-Raphson steps on the Poisson likelihood, fast enough on a graphics processor for whole localization movies, and showed variances at the bound. In the same issue of Nature Methods, Mortensen and coworkers compared maximum likelihood and least squares fitting and gave formulas for the precision of both.

## References
