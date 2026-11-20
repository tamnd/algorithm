---
tag: DC5KCE
kind: algorithm
slug: richardson-lucy-total-variation
name: Richardson-Lucy with total variation regularization
aliases:
- RLTV
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Richardson-Lucy for Poisson data with a total variation penalty added one step late: divide each update by 1 - lam div(grad x/|grad x|) to damp noise and keep edges."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, m: the number of nonzero PSF entries, K: the number of iterations}
  time: {worst: Θ(K n m), average: Θ(K n m), best: Θ(K n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: true, linear: false, nonnegative: true, monotone_objective: false, poisson_noise_model: true}
history:
  year: 2006
  people: [Nicolas Dey, Laure Blanc-Feraud, Christophe Zimmer, Pascal Roux, Zvi Kam, Jean-Christophe Olivo-Marin, Josiane Zerubia]
  note: Dey and coauthors added the total variation term to the Richardson-Lucy step in the one-step-late form of Green (1990) and used it for 3D confocal microscopy.
prereqs: [richardson-lucy-deconvolution, total-variation-denoising, expectation-maximization]
see_also: [one-step-late-algorithm, maximum-a-posteriori-estimation, poisson-distribution, point-spread-function, semi-convergence, chambolle-projection-algorithm, split-bregman-method, van-cittert-deconvolution]
sources:
  - paper: doi:10.1002/jemt.20294
    title: N. Dey, L. Blanc-Feraud, C. Zimmer, P. Roux, Z. Kam, J.-C. Olivo-Marin and J. Zerubia, Richardson-Lucy algorithm with total variation regularization for 3D confocal microscope deconvolution, Microscopy Research and Technique 69(4), 2006
    locator: pages 260 to 266
  - paper: doi:10.1364/JOSA.62.000055
    title: William Hadley Richardson, Bayesian-based iterative method of image restoration, Journal of the Optical Society of America 62(1), 1972
    locator: pages 55 to 59
  - paper: doi:10.1086/111605
    title: L. B. Lucy, An iterative technique for the rectification of observed distributions, The Astronomical Journal 79, 1974
    locator: the article from page 745
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60(1-4), 1992
    locator: pages 259 to 268
---

Richardson-Lucy with total variation regularization (RLTV) is a deblurring method for photon-count images. It takes the multiplicative update of [Richardson-Lucy](/richardson-lucy-deconvolution/), which is the [EM algorithm](/expectation-maximization/) for Poisson data, and divides it by a factor that comes from the [total variation](/total-variation-denoising/) of the estimate:

$$x \leftarrow \frac{x}{1 - \lambda \operatorname{div}\!\big(\nabla x / |\nabla x|\big)}\, \Big(\tilde h \ast \frac{y}{h \ast x}\Big).$$

Plain Richardson-Lucy fits the noise when it runs long, and the estimate breaks up into bright specks. The extra factor is larger than 1 at a local maximum of the estimate and smaller than 1 at a local minimum, so isolated peaks and pits are pulled toward their neighbors, while large flat regions and straight edges are left mostly alone. Dey and coauthors (2006) proposed it for 3D confocal microscopy. The step is the one-step-late form of maximum a posteriori estimation with a total variation prior: a positive fixed point minimizes the Poisson negative log-likelihood plus $\lambda$ times the total variation. Unlike plain Richardson-Lucy it has no monotonicity theorem.

## In plain words

You have a dim, blurred microscope image made of counted photons, and you know the blur. Richardson-Lucy improves a guess by blurring it, comparing it with the data, and multiplying each pixel by how much light is still missing there. If you repeat this many times, the guess starts to copy the random grain of the photon counts, and it turns into sharp specks. RLTV adds one more rule to each round. A pixel that stands above all its neighbors is made a little smaller, and a pixel that sits in a hole is made a little larger. A pixel in a smooth area or on a long straight edge is barely changed. One number sets how strong this rule is. Too weak, and the specks come back. Too strong, and the image turns into flat patches and the rounds can start to swing back and forth.

## The problem

The unknown is a nonnegative image $x$ with $n$ pixels (2D or 3D). The data are counts $y_i \sim \text{Poisson}((h \ast x)_i)$, independent across pixels, with a known PSF $h \ge 0$, $\sum h = 1$ (see [point spread function](/point-spread-function/) and [Poisson distribution](/poisson-distribution/)). The blur is periodic convolution with the PSF centered at index $0$; its adjoint is correlation, $\tilde h(r) = h(-r)$. The goal is the minimizer over $x \ge 0$ of

$$J(x) = \sum_i \big[(h \ast x)_i - y_i \log (h \ast x)_i\big] + \lambda \sum_i |\nabla x|_{\varepsilon, i},$$

the negative log-likelihood plus $\lambda$ times the total variation. Here $\nabla$ is the forward difference, $|g|_\varepsilon = \sqrt{g_1^2 + g_2^2 + \varepsilon^2}$, and the small $\varepsilon > 0$ makes the total variation differentiable. In Bayesian terms $J$ is the negative log-posterior for the prior $\exp(-\lambda\, \mathrm{TV}(x))$, so its minimizer is a [MAP estimate](/maximum-a-posteriori-estimation/).

## The algorithm

```pseudo id=main
RLTV(y, h, lambda, K, x0, eps)               ▷ x0 > 0, default the constant mean of y
L1  x ← x0
L2  repeat K times
L3      c ← h~ * (y / (h * x))                  ▷ Richardson-Lucy correction, two convolutions
L4      kappa ← div(grad x / |grad x|_eps)      ▷ curvature of the level lines, in [-4, 4]
L5      d ← 1 - lambda · kappa                  ▷ stop with an error if some d ≤ 0
L6      x ← x · c / d                           ▷ pixel by pixel
L7  return x
```

Line L3 is the Richardson-Lucy correction; a ratio $y/(h \ast x)$ with $y_i = 0$ counts as $0$. Line L4 uses forward differences for $\nabla$ and backward differences for $\operatorname{div}$, so that $\operatorname{div}$ is the negative adjoint of $\nabla$. Line L5 is the one-step-late term: the derivative of the total variation is taken at the current estimate. With $\lambda = 0$ the method is Richardson-Lucy.

## Example

The effect of L4 to L6 is easiest to see with a delta PSF, where $c = y/x$. Take a $5 \times 5$ periodic image of ones with one pixel of value 2 at the center, $y = x_0$, $\lambda = 0.1$ and $\varepsilon = 10^{-3}$. Then $c = 1$, and the step only divides by $d$. The curvature $\kappa$ is, to four places:

| pixel | $\kappa$ | $d = 1 - 0.1\,\kappa$ | $x_1$ |
|---|---|---|---|
| center (value 2) | $-2 - \sqrt 2 = -3.4142$ | 1.3414 | 1.4910 |
| above and left of it | 1.0000 | 0.9000 | 1.1111 |
| below and right of it | 0.7071 | 0.9293 | 1.0761 |
| all others | 0 | 1 | 1 |

The peak is pulled down and its neighbors go up. The asymmetry between the neighbors comes from the one-sided differences. The next step has $c = y/x_1 \ne 1$, which pulls the estimate back toward the data, and the two forces fight. In this case the iteration does not settle: a measurement over 500 steps shows a period-2 checkerboard around the center for $\lambda = 0.02$, $0.05$ and $0.1$, and it converges only for $\lambda = 0.01$ with $\varepsilon = 0.1$.

With a real blur the method works as intended. A measurement on one seed: a $16 \times 16$ image with background 20 and a $7 \times 7$ square of value 80, a $5 \times 5$ Gaussian PSF with $\sigma = 1$ pixel, Poisson counts, $x_0$ the constant mean and $\varepsilon = 10^{-2}$. The error $\lVert x_K - x^\dagger\rVert$ of the raw data is 165.7.

| $K$ | RL ($\lambda = 0$) | RLTV, $\lambda = 0.005$ | RLTV, $\lambda = 0.02$ | RLTV, $\lambda = 0.05$ |
|---|---|---|---|---|
| 10 | 143.2 | 135.0 | 121.9 | 119.2 |
| 20 | 160.8 | 138.6 | 110.2 | 111.0 |
| 40 | 196.9 | 147.7 | 103.1 | 104.5 |
| 80 | 259.5 | 159.1 | 100.7 | 102.8 |
| 200 | 391.5 | 172.0 | 101.5 | 108.1 |

Plain Richardson-Lucy is best near 10 steps and then fits the noise ([semi-convergence](/semi-convergence/)). With $\lambda = 0.02$ the error keeps falling to about 100 and stays there. In the same runs, $J$ decreased in every step for $\lambda = 0$, as the EM theorem says, but not for any of the three positive values.

## Correctness

The full proof is in `proofs/correctness.md`. With $c$ and $\kappa$ as in lines L3 and L4:

1. **Gradients.** $\nabla L = 1 - c$ for the Poisson term $L$ (because $\sum h = 1$), and the gradient of the smoothed total variation is $-\kappa$.
2. **A scaled gradient step.** $x^+ - x = -\dfrac{x}{1 - \lambda\kappa}\, \nabla J(x)$ pixel by pixel.
3. **Fixed points.** A positive $x$ with $d > 0$ is a fixed point if and only if $\nabla J(x) = 0$. $J$ is convex, so such a point is a global minimizer of $J$ over $x \ge 0$.
4. **Positivity.** $|\kappa| \le 4$ in 2D ($2 \cdot$ dimension in general). So for $\lambda < 1/4$ (in 3D, $\lambda < 1/6$) the denominator is at least $1 - 4\lambda > 0$, and a positive start stays nonnegative without clipping.
5. **Reduction.** For $\lambda = 0$ the step is the EM step of Richardson-Lucy, which never increases the likelihood term and keeps the total flux.

The proof does not show that $J$ decreases or that the iterates converge for $\lambda > 0$, and the measurements above show that neither holds in general.

## Complexity

In the real-RAM model one iteration costs two convolutions for L3 and $\Theta(n)$ for L4 to L6. A direct convolution with $m$ nonzero PSF entries costs $\Theta(nm)$; with the [FFT](/fast-fourier-transform/) and the OTF computed once, $\Theta(n \log n)$. So $K$ iterations cost $\Theta(Knm)$ or $\Theta(Kn\log n)$. The extra space is $\Theta(n)$ for the ratio, the correction and the two gradient images. The total variation term adds about the cost of a few vector operations per step, so RLTV costs about the same per iteration as Richardson-Lucy. It usually needs more iterations, since the regularized result is the limit and not an early-stopped iterate.

## Properties

- Nonnegative: for $\lambda < 1/4$ in 2D and a positive start, every iterate is nonnegative (Claim 4 of the proof).
- Nonlinear in $y$, and the noise model is Poisson, as for Richardson-Lucy.
- The total flux is not kept exactly for $\lambda > 0$; in the first example it rises from 26 to about 27.5.
- A pixel that becomes $0$ stays $0$, as in Richardson-Lucy.
- The result depends on $\lambda$ and $\varepsilon$. Total variation favors piecewise constant images: edges stay sharp, but smooth ramps turn into steps (staircasing) and small low-contrast details are lost.

## Variants and improvements

- **3D stacks.** The original use: the same step with 3D differences, often with a different spacing along the optical axis. The positivity bound becomes $\lambda < 1/6$.
- **Other priors in the one-step-late form.** Any differentiable prior $U$ gives $x \leftarrow x\,c/(1 + \lambda \nabla U(x))$; Green (1990) introduced this form for emission tomography (see the [one-step-late algorithm](/one-step-late-algorithm/)). Tikhonov and entropy priors are common choices.
- **Convergent splittings.** To minimize the same $J$ with a guarantee, use a primal-dual or splitting method, such as [split Bregman](/split-bregman-method/) or [ADMM](/admm/), with the total variation handled by a proximal step such as [Chambolle's projection](/chambolle-projection-algorithm/). These cost more per iteration but do not oscillate.
- **Damped steps.** Replace $x^+$ by $x + t(x^+ - x)$ with $t \in (0, 1]$ chosen by a line search on $J$; by Claim 2 the direction is a scaled descent direction, so a small enough $t$ lowers $J$.

## When to use it

Use RLTV for fluorescence microscopy, confocal stacks and other photon-limited images when the object is made of regions with sharp borders, the PSF is known and the noise is close to Poisson. It is a small change to an existing Richardson-Lucy code, which makes it popular in practice. Pick $\lambda$ well below $1/4$, relative to the scale of the counts, and watch the result for oscillation. When the object has smooth gradients, such as a diffuse cell body, total variation causes staircasing, and a smoother prior or plain Richardson-Lucy with early stopping may be better. When a guaranteed minimizer of $J$ is needed, use a convergent splitting method.

## Pitfalls

- The step is not EM for $\lambda > 0$. $J$ can rise from one step to the next, and the iterates can oscillate, as in the first example. A large $\lambda$ makes this worse.
- If $1 - \lambda\kappa \le 0$ at a pixel, the step gives a negative or infinite value. For $\lambda < 1/4$ in 2D this cannot happen.
- A very small $\varepsilon$ makes $\kappa$ jump between $\pm 4$ for tiny changes of the estimate in flat regions, which amplifies the oscillation. A larger $\varepsilon$ is safer (a heuristic; in the first example only $\varepsilon = 0.1$ converged).
- Total variation depends on the image scale: $\lambda$ that works for counts near 100 is far too strong for counts near 1, because the Poisson term scales with the counts and the total variation term with their differences.
- The periodic boundary links opposite borders. Pad the image, or use another boundary rule, when the object touches the border.
- The quality depends on the PSF model. A PSF that ignores the depth-dependent aberration of the [Gibson-Lanni model](/gibson-lanni-model/) gives artifacts deep in the sample, whatever $\lambda$ is.

## Implementations

## History

W. H. Richardson (1972) and L. B. Lucy (1974) introduced the multiplicative iteration, and Shepp and Vardi (1982) showed it is the EM algorithm for Poisson emission data. Rudin, Osher and Fatemi (1992) introduced total variation for noise removal. P. J. Green (1990) proposed the one-step-late modification of EM for MAP estimation with a prior in emission tomography. Dey, Blanc-Feraud, Zimmer, Roux, Kam, Olivo-Marin and Zerubia (2006) put total variation into this form for 3D confocal microscopy.

## References
