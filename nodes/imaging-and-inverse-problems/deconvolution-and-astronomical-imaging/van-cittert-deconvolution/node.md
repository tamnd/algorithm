---
tag: 3D8AWP
kind: algorithm
slug: van-cittert-deconvolution
name: Van Cittert deconvolution
aliases:
- Van Cittert iteration
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: intro
summary: "Deblur by x <- x + beta (y - h * x), adding back the residual. It converges where |1 - beta H| < 1, so it is Landweber for a positive OTF and fails where the OTF is negative."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, m: the number of nonzero PSF entries, K: the number of iterations}
  time: {worst: Θ(K n m), average: Θ(K n m), best: Θ(K n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: true, linear: true, nonnegative: false, monotone_error_for_positive_otf: true, needs_early_stopping: true}
history:
  year: 1931
  people: [Pieter Hendrik van Cittert, Peter A. Jansson]
  note: Van Cittert (1931) corrected spectral line profiles for the width of the spectrometer slit by adding back the residual again and again. Jansson, Hunt and Plyler (1970) added a bound constraint to keep the result physical.
prereqs: [point-spread-function, optical-transfer-function, richardson-iteration]
see_also: [landweber-iteration, richardson-lucy-deconvolution, image-deblurring, spectral-filter-factors, semi-convergence, wiener-filter, morozov-discrepancy-principle, tikhonov-regularization]
sources:
  - paper: doi:10.1007/BF01391351
    title: P. H. van Cittert, Zum Einfluss der Spaltbreite auf die Intensitatsverteilung in Spektrallinien. II, Zeitschrift fur Physik 69(5-6), 1931
    locator: pages 298 to 308
  - paper: doi:10.1364/JOSA.60.000596
    title: Peter A. Jansson, Robert H. Hunt and Earle K. Plyler, Resolution enhancement of spectra, Journal of the Optical Society of America 60(5), 1970
    locator: the article from page 596 (the Van Cittert step with a relaxation factor that keeps the estimate within physical bounds)
  - book: isbn:9780898716184
    title: Per Christian Hansen, James G. Nagy and Dianne P. O'Leary, Deblurring Images, Matrices, Spectra, and Filtering, SIAM, 2006
    locator: the chapters on structured blurring matrices and on spectral filtering (periodic blur diagonalized by the DFT, filter factors)
  - paper: doi:10.1086/342606
    title: J. L. Starck, E. Pantin and F. Murtagh, Deconvolution in astronomy, a review, Publications of the Astronomical Society of the Pacific 114(800), 2002
    locator: pages 1051 to 1069 (the Van Cittert, Landweber and Richardson-Lucy iterations side by side)
---

Van Cittert deconvolution is the oldest iterative deblurring method. It undoes a known blur $h$ by adding back the part of the data that the current estimate does not explain: $x \leftarrow x + \beta\,(y - h \ast x)$. P. H. van Cittert used it in 1931 to remove the effect of the slit width from measured spectral lines. In the language of linear algebra it is the [Richardson iteration](/richardson-iteration/) for the system $h \ast x = y$. In the Fourier domain each frequency is treated on its own: the error at frequency $k$ is multiplied by $1 - \beta H_k$ in every step, where $H$ is the [optical transfer function](/optical-transfer-function/). So the method converges exactly at the frequencies where $|1 - \beta H_k| < 1$. For a PSF with a positive OTF it is the [Landweber iteration](/landweber-iteration/) in another form, with the same filter factors $1 - (1 - \beta H_k)^K$. For a PSF whose OTF is negative somewhere, such as a box or a defocus blur, it diverges, and the fix is to apply the mirrored PSF to the residual, which is Landweber. Unlike [Richardson-Lucy](/richardson-lucy-deconvolution/) it is linear, does not keep the estimate nonnegative and has no noise model; with noise it must be stopped early.

## In plain words

You have a blurred picture and you know the blur. Start with a blank guess, or with the blurred picture itself. Blur your guess the same way the camera did, and compare it with the real picture. The difference shows what your guess still misses. Add that difference, or a fixed fraction of it, to your guess, and repeat. Coarse features are fixed in a few rounds, because the blur keeps them almost intact. Fine detail is weakened a lot by the blur, so it comes back slowly, a little in each round. If the blur turns some patterns upside down, as an out-of-focus lens does, adding the difference pushes those patterns the wrong way, and the guess gets worse. Noise in the picture also comes back with the detail, so you stop after a moderate number of rounds.

## The problem

The unknown is a signal or an image $x$ with $n$ pixels, and the data are $y = h \ast x + e$ with a known PSF $h$ and noise $e$. The blur is periodic convolution, $(h \ast x)_i = \sum_j h_j\, x_{(i - j) \bmod n}$, with the PSF stored with its center at index $0$, so that a delta PSF gives the identity. This boundary condition makes the blur matrix circulant, and the DFT diagonalizes it: $\widehat{h \ast x}_k = H_k \hat x_k$ with $H_k = \sum_j h_j e^{-2\pi i jk/n}$ (see [discrete Fourier transform](/discrete-fourier-transform/)). Usually $h \ge 0$ and $\sum h = 1$, so $H_0 = 1$ and $|H_k| \le 1$. The goal is an estimate of $x$; without noise, the minimum norm solution of $h \ast x = y$.

## The algorithm

```pseudo id=main
VAN-CITTERT(y, h, beta, K, x0)               ▷ beta > 0, default beta = 1, x0 = 0
L1  x ← x0
L2  repeat K times
L3      r ← y - h * x                           ▷ residual, one periodic convolution
L4      x ← x + beta · r
L5  return x
```

Line L3 blurs the estimate and subtracts it from the data. Line L4 adds a fraction $\beta$ of the residual. The classic form has $\beta = 1$ and $x_0 = y$, which is the same as $x_0 = 0$ with one more step.

## Example

Take $n = 6$, the PSF $h_0 = 2/3$, $h_{\pm 1} = 1/6$, and the true signal $x^\dagger = (0, 0, 6, 0, 0, 0)$. The data are $y = h \ast x^\dagger = (0, 1, 4, 1, 0, 0)$. The OTF is $H_k = 2/3 + (1/3)\cos(2\pi k/6)$, which is $1$, $5/6$, $1/2$ and $1/3$ for $k = 0, 1, 2, 3$. All values are positive, so with $\beta = 1$ every error component shrinks by the factor $1 - H_k$, at worst $2/3$. With $x_0 = 0$ the iterates are, in exact arithmetic:

| $K$ | $x_K$ | $\lVert x_K - x^\dagger \rVert$ |
|---|---|---|
| 1 | $(0, 1, 4, 1, 0, 0)$ | 2.4495 |
| 2 | $(-1/6, 2/3, 5, 2/3, -1/6, 0)$ | 1.3944 |
| 3 | $(-1/6, 5/12, 49/9, 5/12, -1/6, 1/18)$ | 0.8453 |
| 4 | $(-0.1343, 0.2593, 5.6759, 0.2593, -0.1343, 0.0741)$ | 0.5301 |
| 6 | $(-0.0721, 0.1034, 5.8809, 0.1034, -0.0721, 0.0566)$ | 0.2218 |

The peak grows back toward 6 and the error falls in every step, as Claim 3 of the proof says. The estimate has negative values, although the true signal and the data are nonnegative: this is the ringing of a linear method, and the reason for the bounded variant below.

For a PSF with a negative OTF the picture changes. The box of width 5 on 16 points has $H_4 = -1/5$. With $\beta = 1$ the error at frequency 4 is multiplied by $1.2$ in every step, so after 10 more steps it is $1.2^{10} = 6.19$ times larger. No positive $\beta$ helps, because $|1 - \beta H_4| = 1 + \beta/5 > 1$.

## Correctness

The full proof is in `proofs/correctness.md`. The main facts, for periodic convolution and real $\beta > 0$:

1. **Closed form.** From $x_0 = 0$, $x_K = \beta\sum_{j<K}(I - \beta A)^j y$, and in the Fourier domain $\hat x_{K,k} = f_k\, \hat y_k / H_k$ with the filter factors $f_k = 1 - (1 - \beta H_k)^K$ (for $H_k \ne 0$). This is the [spectral filter](/spectral-filter-factors/) form of Landweber, with $\beta H_k$ in place of $\omega\sigma^2$.
2. **Convergence with exact data.** If $y = h \ast x^\dagger$, the error at frequency $k$ is $-(1 - \beta H_k)^K \hat x^\dagger_k$. So $x_K$ converges to the minimum norm solution for every $x^\dagger$ if and only if $|1 - \beta H_k| < 1$ at every frequency with $H_k \ne 0$; that is, every nonzero $H_k$ lies in the open disk of center $1/\beta$ and radius $1/\beta$. For a symmetric PSF the OTF is real, and the condition is $0 < \beta H_k < 2$.
3. **Monotone error.** Under that condition the error norm never grows (Parseval).
4. **Divergence.** If $|1 - \beta H_k| > 1$ for some $k$, the error at that frequency grows geometrically for any $x^\dagger$ that has it.
5. **Noise.** With $y = h\ast x^\dagger + e$, the limit is $x^\dagger$ plus the noise term $\hat e_k / H_k$, which is large where $|H_k|$ is small, and a frequency with $H_k = 0$ and $\hat e_k \ne 0$ grows like $K\beta\hat e_k$. The iterates show [semi-convergence](/semi-convergence/): the error first falls and then rises.

## Complexity

In the real-RAM model, one iteration is one convolution and two vector operations. A direct periodic convolution with a PSF of $m$ nonzero entries costs $\Theta(nm)$; with the [FFT](/fast-fourier-transform/) and the OTF computed once, it costs $\Theta(n \log n)$ for $n$ a power of two. So $K$ iterations cost $\Theta(Knm)$ or $\Theta(K n \log n)$, and the extra space is $\Theta(n)$ for the residual. The number of iterations is the regularization parameter. With exact data the error at frequency $k$ falls like $|1 - \beta H_k|^K$, so reaching a relative error $\varepsilon$ at that frequency takes about $\log(1/\varepsilon)/|\log|1 - \beta H_k||$ steps, which is about $\log(1/\varepsilon)/(\beta H_k)$ for small positive $H_k$. With a periodic boundary and no other constraint the whole run equals one filtered division in the Fourier domain, which costs $\Theta(n \log n)$ in total; the iteration is worth its cost only when a constraint is applied in each step or when the blur is not a convolution.

## Properties

- Linear in $y$: $x_K$ is a fixed filter applied to the data.
- No noise model. It is not the maximum likelihood method of any noise law, and it does not keep the estimate nonnegative.
- The total flux is kept in the limit: $\hat x_{K,0} = (1 - (1 - \beta)^K)\, \hat y_0$ for $H_0 = 1$, and with $\beta = 1$ the sum of $x_K$ equals the sum of $y$ from the first step on.
- The step $\beta$ trades speed against safety. For a real positive OTF with $H_k \le 1$, any $0 < \beta < 2$ converges, and $\beta = 1$ removes the zero frequency error in one step.

## Variants and improvements

- **Landweber form.** Apply the adjoint of the blur, correlation with $h$, to the residual: $x \leftarrow x + \beta\, \tilde h \ast (y - h \ast x)$ with $\tilde h(r) = h(-r)$. The factor becomes $1 - \beta |H_k|^2$, so it converges for $0 < \beta < 2/\max|H_k|^2$ for every PSF, at the price of a second convolution and slower progress where $|H_k|$ is small. This is the [Landweber iteration](/landweber-iteration/) for the blur.
- **Bounded or constrained Van Cittert.** Jansson, Hunt and Plyler (1970) scaled the correction by a relaxation function that falls to zero at the physical bounds of the signal, so the estimate stays between them. A simpler version clips $x$ to $x \ge 0$ after each step, which is projected Landweber when the Landweber form is used. Constraints make the method nonlinear and can bring back some frequencies with small $|H_k|$.
- **Damped form.** Add the term $-\beta\alpha x$ to the Landweber step. The fixed point is then $(A^\ast A + \alpha I)^{-1} A^\ast y$, the solution of [Tikhonov regularization](/tikhonov-regularization/), so the iteration no longer needs early stopping.
- **Multiplicative instead of additive.** [Richardson-Lucy](/richardson-lucy-deconvolution/) multiplies by a ratio instead of adding a difference, which keeps the estimate nonnegative and is maximum likelihood for Poisson counts.

## When to use it

Use it as a simple first deblurring step, or as a teaching example of a spectral filter, when the PSF is symmetric and has a positive OTF, for example a Gaussian blur, and the noise is low. Stop it early, with the [discrepancy principle](/morozov-discrepancy-principle/) when the noise level is known. Use the Landweber form for any PSF whose OTF may be negative or complex, such as defocus, motion blur or a box. For photon counts use Richardson-Lucy, and for a fixed linear answer use the [Wiener filter](/wiener-filter/), which gets the same kind of result in one FFT pass.

## Pitfalls

- A negative OTF value makes the plain iteration diverge at that frequency, whatever $\beta$ is. Defocus and box blurs have negative lobes. Check the sign of $H$ before you use the plain form.
- An OTF zero with noise in the data makes that frequency grow linearly in $K$.
- The method shows semi-convergence: run long enough, it fits the noise. The number of iterations must be chosen; without a known noise level any stopping rule is a heuristic.
- With a zero or reflexive boundary the blur matrix is not circulant, the Fourier analysis is only an approximation, and ringing appears at the image border.
- The estimate can go negative near sharp edges, as in the example. Clip it, or use a constrained variant, if negative values break later steps.
- A PSF that does not sum to 1 changes the scale of $H$; with $\sum h = s$ the condition for $\beta = 1$ fails when $s \ge 2$.

## Implementations

## History

P. H. van Cittert (1931) studied how the width of the entrance slit of a spectrometer changes the measured intensity profile of a spectral line, and corrected the profile by repeated addition of the residual. The method was later used for spectra and images, and Jansson, Hunt and Plyler (1970) made it practical for infrared spectra by bounding the estimate. The link with the Landweber iteration (1951) and with spectral filtering came with the theory of ill-posed problems, and Starck, Pantin and Murtagh (2002) review it next to the other iterative methods of astronomical deconvolution.

## References
