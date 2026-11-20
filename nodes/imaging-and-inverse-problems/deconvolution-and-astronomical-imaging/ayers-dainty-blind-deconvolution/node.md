---
tag: MB6VNZ
kind: algorithm
slug: ayers-dainty-blind-deconvolution
name: Ayers-Dainty blind deconvolution
aliases:
- iterative blind deconvolution
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Recover the image and the PSF together by alternate Fourier domain fits of each, with positivity and support constraints in the image domain. Simple, but with no convergence proof."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of passes}
  time: {worst: Θ(K N log N), average: Θ(K N log N), best: Θ(K N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, iterative: true, linear: false, nonnegative: true, convergence_proof: false, needs_good_start: true}
history:
  year: 1988
  people: [G. R. Ayers, J. C. Dainty, B. L. K. Davey, R. G. Lane, R. H. T. Bates]
  note: Ayers and Dainty (1988) adapted the alternating Fourier and image domain scheme of phase retrieval to blind deconvolution. Davey, Lane and Bates (1989) replaced the inverse filter by a Wiener-type filter.
prereqs: [image-deblurring, point-spread-function, optical-transfer-function, wiener-filter]
see_also: [error-reduction-algorithm, gerchberg-saxton-algorithm, richardson-lucy-deconvolution, variational-bayes-blind-deconvolution, phase-diversity, speckle-interferometry, blind-equalization, coordinate-descent]
sources:
  - paper: doi:10.1364/OL.13.000547
    title: G. R. Ayers and J. C. Dainty, Iterative blind deconvolution method and its applications, Optics Letters 13(7), 1988
    locator: pages 547 to 549
  - paper: doi:10.1016/0030-4018(89)90018-7
    title: B. L. K. Davey, R. G. Lane and R. H. T. Bates, Blind deconvolution of noisy complex-valued image, Optics Communications 69(5-6), 1989
    locator: pages 353 to 356 (the Wiener-type form of the two Fourier steps and the effect of the constraints on convergence)
  - paper: "R. G. Lane and R. H. T. Bates, Automatic multidimensional deconvolution, Journal of the Optical Society of America A 4(1), 1987"
    title: Lane and Bates 1987
    locator: the article (why a convolution of images, unlike one of signals, can in general be factored in one way only)
  - paper: "Deepa Kundur and Dimitrios Hatzinakos, Blind image deconvolution, IEEE Signal Processing Magazine 13(3), 1996"
    title: Kundur and Hatzinakos 1996
    locator: the section on iterative blind deconvolution
---

Ayers-Dainty blind deconvolution, also called iterative blind deconvolution, recovers both the sharp image $f$ and the [point spread function](/point-spread-function/) $h$ from one blurred image $y = h \ast f$. G. R. Ayers and J. C. Dainty proposed it in 1988. It borrows the idea of the [error reduction algorithm](/error-reduction-algorithm/) of phase retrieval: go to the Fourier domain to fit the data, go back to the image domain to apply what you know, and repeat. Here the data fit in the Fourier domain is a division, because convolution becomes a product, $\hat y = \hat h \hat f$. So with the current image the method estimates the PSF by dividing the data spectrum by the image spectrum, makes the PSF nonnegative, zero outside its known support and of sum 1, then estimates the image from the new PSF in the same way and makes it nonnegative. The divisions are done as [Wiener filters](/wiener-filter/), so small values do not blow up. The method is short and works on some problems, but it has no convergence proof. It can stall, it can cycle, and it has a trivial fixed point, "the image is the data and there is no blur".

## In plain words

You have one blurred photo and you do not know the blur. Guess a sharp picture, for example a flat gray one. Ask: which blur would turn this guess into the photo? That question has a direct answer in the frequency domain, where blurring is multiplication. Take the answer, and fix it with what every blur must obey: no negative values, small size, and total weight 1. Now ask the opposite question: which sharp picture, blurred by this blur, gives the photo? Fix that answer too: no negative brightness. Go back and forth. On a good day the two guesses settle on the true picture and the true blur. On a bad day they wander or get stuck, and nothing in the method tells you which day it is.

## The problem

The grid is periodic with $N = n_1 n_2$ pixels, and $(h \ast f)(r) = \sum_s h(s)\, f(r - s)$ with indices modulo the grid. The PSF is stored with its center at index $(0, 0)$. The data are $y = h \ast f + e$ with unknown $f$, unknown $h$ and noise $e$. The prior knowledge is:

- $f \ge 0$, and $f = 0$ outside a set $S_f$ (optional; $S_f$ is the whole grid when nothing is known);
- $h \ge 0$, $h = 0$ outside a known small set $S_h$ around the origin, and $\sum h = 1$.

The goal is a pair $(f, h)$ that satisfies the constraints and fits the data. Some ambiguities can never be resolved (a theorem, Claim 3 of the proof). The pairs $(f(\cdot - t), h(\cdot + t))$ and $(cf, h/c)$ give the same data as $(f, h)$. The sum constraint fixes $c$, and the support of $h$ limits $t$. In one dimension there are far more ambiguities: the $z$ transform of $y$ is a polynomial, it splits into linear factors, and each way to share the factors gives another pair. For example $(1, 4, 6, 4, 1) = (1, 2, 1) \ast (1, 2, 1) = (1, 1) \ast (1, 3, 3, 1) = \delta \ast (1, 4, 6, 4, 1)$, and every factor is positive. A polynomial in two variables has, in general, no factors, so for images the answer is unique up to the shift and the scale (Lane and Bates, 1987). This is why blind deconvolution is a problem for images more than for signals.

## The algorithm

Let $C = \hat y$ be the DFT of the data, and let $\alpha \ge 0$ be a small weight. For a spectrum $A$ define the Wiener-type division $W(C, A) = \overline A\, C/(|A|^2 + \alpha)$, frequency by frequency, with $0$ where the divisor is $0$.

```pseudo id=main
AYERS-DAINTY(y, f0, h0, S_h, S_f, alpha, K)
L1  f ← P_F(f0); h ← P_H(h0)
L2  C ← DFT(y)
L3  repeat K times
L4      H ← W(C, DFT(f))                      ▷ the PSF that best explains y for this f
L5      h ← P_H(IDFT(H))                      ▷ real part, h ≥ 0, h = 0 outside S_h, sum 1
L6      F ← W(C, DFT(h))                      ▷ the image that best explains y for this h
L7      f ← P_F(IDFT(F))                      ▷ real part, f ≥ 0, f = 0 outside S_f
L8  return f, h
```

$P_F$ sets negative values and values outside $S_f$ to $0$. $P_H$ does the same with $S_h$ and then divides by the sum; if nothing positive is left, it keeps the previous PSF. Line L4 is the minimizer of $\lVert y - f \ast h\rVert^2 + \alpha\lVert h\rVert^2$ over all $h$, and line L6 is the same for $f$ (a theorem, Claim 1 of the proof). So each half step is a regularized least squares fit for one unknown with the other held fixed, followed by the constraints. An optional relaxation $\beta \in (0, 1]$ replaces each new spectrum by $(1 - \beta)$ times the old one plus $\beta$ times the new one. The code is a version for images; a signal is an image with one row.

In the original paper the Fourier step is an inverse filter, $C/\hat f$, mixed with the previous estimate, with a separate rule for the frequencies where the divisor is small. Davey, Lane and Bates (1989) replaced it with the Wiener form above, which is the form most later descriptions use.

## Example

**The trivial fixed point.** Start with $f = y$ and $\alpha = 0$, and suppose that $C$ has no zero. Line L4 gives $H = C/C = 1$ at every frequency, so $h = \delta$, whatever the start PSF was. Line L6 gives $F = C/1$, so $f = y$. The method is stuck at "no blur" after one pass (Claim 5). So the start image must not be the data. A positive start with no structure, for example the mean of the data with small random changes, is a common choice.

**The true pair is also a fixed point.** If $y = h_0 \ast f_0$ exactly, the pair satisfies the constraints and neither spectrum has a zero, then one pass with $\alpha = 0$ returns $(f_0, h_0)$ unchanged (Claim 4). So the method has at least two fixed points, and which one it reaches, if any, depends on the start.

**A measured run.** On a $12 \times 12$ periodic grid, the object has random values in $[0, 1)$ on about half of the pixels of the square of rows and columns $2$ to $9$, and $0$ elsewhere. The PSF has random values in $[0.1, 1]$ on a $3 \times 3$ square around the origin, scaled to sum 1. The data have no noise. The run uses $\alpha = 0$, no object support, the PSF support $3 \times 3$, a flat start PSF, and a start image whose pixels are the mean of the data times random factors in $[0.5, 1.5]$. (A flat start image has a spectrum that is zero away from frequency 0, so the first division would divide by rounding errors.) The table gives the relative error of $f$, $\lVert f_K - f\rVert/\lVert f\rVert$, after $K$ passes, for the shift of up to 2 pixels that makes it smallest, and the relative error of $h$ for the same shift. These are measurements, with the generators of the tests.

| seed | $K = 50$ | $K = 100$ | $K = 400$ | PSF error at $K = 400$ |
|---|---|---|---|---|
| 1 | 0.50 | 0.18 | 0.19 | 0.11 |
| 2 | 0.28 | 5.4e-4 | 5.7e-15 | 3.6e-15 |
| 3 | 0.22 | 0.16 | 0.79 | 0.63 |
| 4 | 0.34 | 0.28 | 0.28 | 0.22 |
| 5 | 0.88 | 0.79 | 4.4e-3 | 1.6e-3 |
| 6 | 0.48 | 0.40 | 0.35 | 0.28 |
| 7 | 0.86 | 0.75 | 0.49 | 0.31 |
| 8 | 0.12 | 0.089 | 0.085 | 0.052 |

For comparison, the trivial pair $(y, \delta)$ has an image error between 0.69 and 0.81 on these eight problems. On seed 2 the method finds the exact pair to rounding error. On seed 5 it wanders for 200 passes and then comes close. On seeds 4, 6 and 8 it stops at a pair that fits the data only roughly. On seed 3 it is at 0.16 after 100 passes and then moves away, to 0.79, which is worse than the blurred data. With $\alpha = 10^{-3}$ the eight runs stagnate within about 100 passes, at image errors between 0.15 and 0.71; on seed 2 the error stays at 0.15 instead of falling to rounding level.

## Correctness

The full proof is in the proofs file. It shows that lines L4 and L6 are regularized least squares fits (Claim 1), that the output always satisfies the constraints (Claim 2), that the shift and scale ambiguities are exact (Claim 3), and that both the true pair and the trivial pair are fixed points (Claims 4 and 5). It does not show convergence, because there is no known result of that kind. The model $h \ast f$ is bilinear, so the set of pairs that fit the data is not convex, and each half step can undo part of the progress of the other. No quantity is known to fall from pass to pass. The tests check the five claims, check that the misfit rises between some passes on seed 1, and record the recovery on seed 2 as a measurement.

## Complexity

Each pass takes four DFTs of $N$ pixels and $\Theta(N)$ other work. With the [FFT](/fast-fourier-transform/) a pass costs $\Theta(N \log N)$, so $K$ passes cost $\Theta(K N \log N)$, and the extra space is $\Theta(N)$ for the spectra. The code here uses a direct DFT along rows and then along columns, which costs $\Theta(N(n_1 + n_2))$ per transform and is enough for small tests. The number of passes needed is not bounded by any theory; in the measured runs it ranges from about 100 to "never".

## Properties

- Nonlinear and not monotone. No objective is known to fall along the passes.
- The output satisfies the constraints after every pass: $f \ge 0$, $h \ge 0$, both zero outside their supports, and $\sum h = 1$.
- Both the true pair and the trivial pair $(y, \delta)$ are fixed points for $\alpha = 0$.
- The result depends on the start, on $\alpha$, on $\beta$ and on the number of passes.
- Each half step is a [Tikhonov](/tikhonov-regularization/) fit of one unknown, so the method is a form of alternating minimization in which the constraint step is not part of the objective.

## Variants and improvements

- **Inverse filter with averaging.** The original method of Ayers and Dainty used the plain division and averaged the new and the old spectra; the relaxation $\beta < 1$ of the code is in this spirit.
- **Wiener-type steps.** Davey, Lane and Bates (1989) used $\overline A C/(|A|^2 + \alpha)$, with $\alpha$ set from the noise level. This is the form in the code.
- **Blind Richardson-Lucy.** Replace each Fourier step by a few [Richardson-Lucy](/richardson-lucy-deconvolution/) steps, first for the PSF with the image fixed and then for the image with the PSF fixed. The multiplicative steps keep both nonnegative without a clip, and for Poisson data each half step does not decrease the likelihood. This variant was proposed by Fish and coworkers in 1995.
- **More images.** With several frames of the same object behind different blurs, as in speckle imaging, the object is shared and the problem is much better posed. [Phase diversity](/phase-diversity/) adds a known aberration to make the blurs different.
- **Priors instead of hard constraints.** [Variational Bayes blind deconvolution](/variational-bayes-blind-deconvolution/) puts a prior on the image and estimates the PSF while it averages over the image, which avoids the trivial solution of joint fitting.

## When to use it

Use it as a first try when the object is positive and sits on a dark background, the PSF is small and nonnegative, the noise is low and you can afford to restart from several starts and check the results. Typical cases are star fields and small objects behind atmospheric or optical blur. Do not use it when the PSF must be known reliably, for example for photometry, or when the data are noisy; there use a method with a noise model, or a calibrated PSF from a star in the field.

## Pitfalls

- Starting the image at the data sends the method to the trivial pair $(y, \delta)$ in one pass.
- A start image that is exactly flat has a spectrum that is zero away from frequency 0. With $\alpha = 0$ the first division then divides by rounding errors, and the run depends on them.
- The result is not unique up to shift and scale in one dimension, and positivity does not fix this. A Gaussian blur on a signal can be split into two narrower Gaussians in many ways.
- No convergence proof: the misfit can rise, the method can cycle, and a pass count that works on one image fails on the next one. Watch the misfit and stop at a good value, not at a fixed count.
- A PSF support that is too large lets the PSF absorb part of the image; one that is too small makes the true PSF infeasible. Both give wrong answers without a warning.
- With $\alpha = 0$ and noise, the divisions amplify the noise at frequencies where the spectrum is small. With a large $\alpha$ the method stalls early.
- The error must be measured up to a shift, because a shifted image and an opposite shift of the PSF fit the same data.

## Implementations

## History

Blind deconvolution of images was studied in the 1980s, when Bates and coworkers argued that a convolution of two images can in general be split in one way only, unlike a convolution of two signals. In 1988 G. R. Ayers and J. C. Dainty published a short method that applies the alternating scheme of Gerchberg, Saxton and Fienup to this problem, with positivity in the image domain and divisions in the Fourier domain. Davey, Lane and Bates (1989) made the divisions Wiener-type and studied how the constraints affect convergence. The method became a standard example in reviews of blind deconvolution, such as Kundur and Hatzinakos (1996), both for its simplicity and for its lack of convergence guarantees. Later methods, such as blind Richardson-Lucy and the variational Bayes methods of the 2000s, added a noise model and a prior.

## References
