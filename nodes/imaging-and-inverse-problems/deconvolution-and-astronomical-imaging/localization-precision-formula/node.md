---
tag: H58F1N
kind: theorem
slug: localization-precision-formula
name: Localization precision formula
aliases:
- Thompson-Larson-Webb formula
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "The Thompson-Larson-Webb formula approximates the precision of a least squares fit of an emitter position; Mortensen et al. corrected it in 2010. The exact limit is the Cramer-Rao bound."
model: real-ram
prereqs: [cramer-rao-bound, fisher-information-matrix, poisson-distribution, point-spread-function]
see_also: [single-molecule-localization, maximum-likelihood-localization, cramer-rao-bound, fisher-information-matrix, abbe-diffraction-limit, rayleigh-criterion, parseval-theorem, least-squares-problem]
sources:
  - paper: doi:10.1016/S0006-3495(02)75618-X
    title: "R. E. Thompson, D. R. Larson and W. W. Webb, Precise nanometer localization analysis for individual fluorescent probes, Biophysical Journal 82(5), 2002, 2775 to 2783"
    locator: "the approximate variance of a least squares Gaussian fit, with the photon, pixel and background terms"
  - paper: doi:10.1016/S0006-3495(04)74193-4
    title: "R. J. Ober, S. Ram and E. S. Ward, Localization accuracy in single-molecule microscopy, Biophysical Journal 86(2), 2004, 1185 to 1200"
    locator: "the Fisher information of the photon detection process, the limit of the localization accuracy, and the effect of pixels and background"
  - paper: doi:10.1038/nmeth.1447
    title: "K. I. Mortensen, L. S. Churchman, J. A. Spudich and H. Flyvbjerg, Optimized localization analysis for single-molecule tracking and super-resolution microscopy, Nature Methods 7(5), 2010, 377 to 381"
    locator: "the corrected precision formulas for least squares and maximum likelihood fitting, and their comparison with the information limit"
---

## Statement

An emitter at $(x_0, y_0)$ sends $N$ photons (in expectation) to a camera. The photon density on the camera is $f(\xi, \eta) = N\,\mathrm{PSF}(\xi - x_0, \eta - y_0)$ with $\int \mathrm{PSF} = 1$. Square pixels of side $a$ count the photons, together with a background of $b$ photons per pixel, and the counts are independent Poisson values with the means $\mu_p = \int_p f + b$. For the Gaussian PSF of width $s$ in each direction, write $\sigma_a^2 = s^2 + a^2/12$.

**Theorem (information limit).** Let $\theta = (x_0, y_0, N, b)$ and $I(\theta) = \sum_p \nabla\mu_p\,\nabla\mu_p^T/\mu_p$ be the Fisher information of the pixel counts.

1. Every unbiased estimator $\hat x_0$ of $x_0$ from the counts has $\operatorname{Var}\hat x_0 \ge [I(\theta)^{-1}]_{11}$ (Ober, Ram and Ward 2004).
2. Whatever the pixels and the background, $[I(\theta)^{-1}]_{11} \ge 1/\int (\partial_{x_0} f)^2/f$.
3. For the Gaussian PSF, $\int (\partial_{x_0} f)^2/f = N/s^2$, so $\operatorname{Var}\hat x_0 \ge s^2/N$.
4. For the ideal in-focus PSF of a circular pupil in the scalar model, with the wavelength $\lambda$ and the numerical aperture $\mathrm{NA}$, $\int (\partial_{x_0} f)^2/f = N(2\pi\,\mathrm{NA}/\lambda)^2$, so $\operatorname{Var}\hat x_0 \ge \lambda^2/(4\pi^2\,\mathrm{NA}^2 N)$.

**The approximations.** These are not theorems; they come from approximate derivations.

- **Thompson, Larson and Webb (2002)**, for a least squares Gaussian fit, with $b$ the standard deviation of the background in a pixel (so $b^2$ is the background count for Poisson noise):
$$\langle(\Delta x)^2\rangle \approx \frac{s^2 + a^2/12}{N} + \frac{8\pi s^4 b^2}{a^2 N^2}.$$
- **Mortensen et al. (2010)**, with $\sigma_a^2 = s^2 + a^2/12$ and $b^2$ as above. For least squares,
$$\operatorname{Var} \approx \frac{\sigma_a^2}{N}\Bigl(\frac{16}{9} + \frac{8\pi\sigma_a^2 b^2}{N a^2}\Bigr),$$
and for maximum likelihood, with $\tau = 2\pi\sigma_a^2 b^2/(N a^2)$,
$$\operatorname{Var} \approx \frac{\sigma_a^2}{N}\Bigl(1 + \int_0^1 \frac{\ln t}{1 + t/\tau}\,dt\Bigr)^{-1}.$$

The formula that carries the name of Thompson, Larson and Webb is an approximation for least squares fitting. Mortensen and coworkers found that least squares fitting does worse than it says (the factor $16/9$ on the photon term), and that maximum likelihood fitting reaches the information limit. The exact statement is the Cramer-Rao bound of part 1, which a computer evaluates for any PSF, pixel size and background.

## In plain words

Each detected photon is a random sample from the blurred spot, so it tells you the position of the emitter only to within the width $s$ of the spot. Averaging $N$ photons shrinks this to $s/\sqrt N$. Pixels blur the photon positions further, by a uniform error of variance $a^2/12$ in each direction, and background photons add noise that carries no information about the position. The Cramer-Rao bound makes this exact: no unbiased estimator does better than the inverse of the Fisher information. The Thompson-Larson-Webb formula is a convenient estimate of how well a least squares fit does. It is close to the bound itself, which is why least squares fits in practice come out worse than the formula predicts.

## Proof

**Lemma 1 (Fisher information of Poisson counts).** For independent Poisson counts $c_p$ with the means $\mu_p(\theta)$, the Fisher information is $\sum_p \nabla\mu_p\nabla\mu_p^T/\mu_p$.

*Proof.* The log likelihood is $\sum_p (c_p\log\mu_p - \mu_p - \log c_p!)$, so the score is $\sum_p (c_p/\mu_p - 1)\nabla\mu_p$. The terms are independent with mean zero and $\operatorname{Var}(c_p/\mu_p) = 1/\mu_p$, so the covariance of the score is $\sum_p \nabla\mu_p\nabla\mu_p^T/\mu_p$. $\square$

Part 1 is the [Cramer-Rao bound](/cramer-rao-bound/) with this information. The proof of [maximum likelihood localization](/maximum-likelihood-localization/) also derives it from the Hessian.

**Lemma 2 (pixels and background lose information).** For each pixel $p$, $(\partial_{x_0}\mu_p)^2/\mu_p \le \int_p (\partial_{x_0} f)^2/f$.

*Proof.* $\partial_{x_0}\mu_p = \int_p \partial_{x_0} f$, since $b$ does not depend on $x_0$. By the Cauchy-Schwarz inequality,
$$\Bigl(\int_p \partial_{x_0} f\Bigr)^2 = \Bigl(\int_p \frac{\partial_{x_0} f}{\sqrt f}\sqrt f\Bigr)^2 \le \int_p \frac{(\partial_{x_0} f)^2}{f}\int_p f.$$
Divide by $\mu_p = \int_p f + b \ge \int_p f$. $\square$

Summing over the pixels gives $I_{11} \le \int (\partial_{x_0} f)^2/f$, where the integral is over the whole plane.

**Lemma 3 (other parameters only raise the bound).** For a positive definite matrix $I$, $[I^{-1}]_{11} \ge 1/I_{11}$.

*Proof.* Write $I = \begin{pmatrix} \alpha & c^T \\ c & D\end{pmatrix}$ with $D$ positive definite. By the [Schur complement](/schur-complement/), $[I^{-1}]_{11} = 1/(\alpha - c^TD^{-1}c)$, and $c^TD^{-1}c \ge 0$. $\square$

Part 2 follows from Lemmas 2 and 3: $[I^{-1}]_{11} \ge 1/I_{11} \ge 1/\int(\partial_{x_0} f)^2/f$.

**Part 3.** With $f = N g(\xi - x_0) g(\eta - y_0)$ and the normal density $g$ of variance $s^2$, $\partial_{x_0} f = -N g'(\xi - x_0) g(\eta - y_0)$ and $g'(t) = -(t/s^2) g(t)$. So
$$\int\frac{(\partial_{x_0} f)^2}{f} = N\int\frac{g'(t)^2}{g(t)}\,dt\int g = N\int\frac{t^2}{s^4}g(t)\,dt = \frac{N}{s^2}. \quad\square$$

**Part 4.** In the scalar model the in-focus PSF is $A^2$, where the amplitude $A$ is the inverse Fourier transform of the pupil $P$, constant on the disk $|k| \le \rho$ with $\rho = \mathrm{NA}/\lambda$ and zero outside. The pupil is real and symmetric, so $A$ is real. Normalize $\int A^2 = 1$; by [Parseval's theorem](/parseval-theorem/), $\int |P|^2 = 1$, so $|P|^2 = 1/(\pi\rho^2)$ on the disk. Where $A \ne 0$,
$$\frac{(\partial_x A^2)^2}{A^2} = \frac{(2A\,\partial_x A)^2}{A^2} = 4(\partial_x A)^2,$$
and the zeros of $A$ form a set of measure zero. So $\int(\partial_{x_0} f)^2/f = 4N\int(\partial_x A)^2$. The Fourier transform of $\partial_x A$ is $2\pi i k_x P(k)$, so by Parseval again
$$\int(\partial_x A)^2 = \frac{4\pi^2}{\pi\rho^2}\int_{|k| \le \rho} k_x^2\,dk = \frac{4\pi^2}{\pi\rho^2}\cdot\frac{\pi\rho^4}{4} = \pi^2\rho^2.$$
So the information is $4\pi^2\rho^2 N = N(2\pi\,\mathrm{NA}/\lambda)^2$. $\blacksquare$

## Consequences

**Numbers.** For $s = 100$ nm and $N = 1000$ photons, part 3 gives $s/\sqrt N = 3.16$ nm. With pixels of $a = 100$ nm and no background, the exact bound of part 1, computed on a $15 \times 15$ window, is $3.2914$ nm, and $\sqrt{(s^2 + a^2/12)/N} = 3.2914$ nm as well. For $100$ photons the bound is $10.4$ nm. For the Airy PSF with $\lambda = 500$ nm, $\mathrm{NA} = 1.4$ and $N = 1000$, part 4 gives $1.80$ nm.

**Pixel size.** The exact bound against $\sqrt{(s^2 + a^2/12)/N}$, for $s = 100$ nm, $N = 1000$ and no background:

| $a$ (nm) | bound (nm) | $\sqrt{(s^2 + a^2/12)/N}$ (nm) |
|---|---|---|
| 10 | 3.1636 | 3.1636 |
| 50 | 3.1951 | 3.1951 |
| 100 | 3.2914 | 3.2914 |
| 200 | 3.6600 | 3.6515 |

So the term $a^2/12$ is a very good description of the pixel loss up to $a = s$, and slightly too small for larger pixels. This is a numerical observation, not an identity.

**Background.** The standard deviation in nm for $s = a = 100$ nm and $N = 1000$, against the background $b^2$ in photons per pixel:

| $b^2$ | exact bound | Mortensen, ML | Thompson et al. | Mortensen, LS |
|---|---|---|---|---|
| 0 | 3.2914 | 3.2914 | 3.2914 | 4.3885 |
| 1 | 3.4625 | 3.4615 | 3.3294 | 4.4220 |
| 10 | 4.0928 | 4.0925 | 3.6533 | 4.7126 |
| 100 | 6.8422 | 6.8348 | 5.9972 | 6.9825 |

The Mortensen formula for maximum likelihood follows the exact bound closely. The Thompson-Larson-Webb formula is below the exact bound when there is background, so it cannot describe any unbiased estimator there, and below the Mortensen formula for least squares everywhere.

**A simulation.** On an $11 \times 11$ window with $s = a$, $N = 1000$ and almost no background, $1000$ Poisson images (seed $6$) gave a least squares variance of $1.71$ times the bound and a maximum likelihood variance of $1.00$ times the bound. The value $1.71$ is near $16/9 = 1.78$, within the sampling error of about $0.08$.

**Design.** The precision improves as $1/\sqrt N$, so the photon count matters most; a high numerical aperture helps through both $N$ and the PSF width. Pixels much smaller than $s$ gain little and spread the photons over more pixels with read noise. An EMCCD camera at high gain doubles the variance through its excess noise.

## Tightness

- **Part 3 is reached.** Without pixels or background, and given the count $N$, the photon positions are independent normal values with the mean $x_0$ and the variance $s^2$. Their mean is unbiased with the variance exactly $s^2/N$.
- **Part 1 is reached asymptotically.** The maximum likelihood estimate reaches $[I^{-1}]_{11}$ as $N$ grows, when the PSF model is correct; the simulation above shows this at $N = 1000$.
- **Least squares does not reach it.** Unweighted least squares gives each pixel the same weight, while the Poisson variance grows with the count. Its variance is larger than the bound, by about $16/9$ at low background.
- **Biased estimators can do better** than the bound, for example by shrinking toward a prior position. The bound applies to unbiased estimators only.

## History

Thompson, Larson and Webb (2002) derived their formula for least squares fitting of a Gaussian to a fluorescent spot, with terms for the photon noise, the pixel size and the background, and it became the standard quick estimate of localization precision. Ober, Ram and Ward (2004) computed the Fisher information of the photon detection process and gave the information limit, including the effects of pixels, background and the Airy PSF. Mortensen, Churchman, Spudich and Flyvbjerg (2010) compared least squares and maximum likelihood fitting, found the factor of $16/9$ for least squares, and gave a formula for maximum likelihood that is close to the limit.

## References
