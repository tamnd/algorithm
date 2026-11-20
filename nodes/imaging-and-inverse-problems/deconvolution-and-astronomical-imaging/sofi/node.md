---
tag: 70NF24
kind: algorithm
slug: sofi
name: Super-resolution optical fluctuation imaging
aliases:
- SOFI
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: research
summary: "Compute the n-th order cumulant of the blinking at each pixel of a movie. This raises the PSF to the n-th power, which narrows a Gaussian PSF by the square root of n."
model: real-ram
complexity:
  vars: {N: the number of pixels, T: the number of frames, n: the order of the cumulant}
  time: {worst: Θ(n N T), average: Θ(n N T), best: Θ(n N T)}
  space: {extra: Θ(N + n T)}
properties: {deterministic: true, iterative: false, linear: false, background_free: true, optical_method: true}
history:
  year: 2009
  people: [Thomas Dertinger, Ryan Colyer, Gopal Iyer, Shimon Weiss, Jörg Enderlein]
  note: "Dertinger and coworkers computed pixelwise cumulants of movies of blinking quantum dots and showed that the order n cumulant image is the sum of the n-th powers of the PSFs of the emitters, free of background."
prereqs: [point-spread-function, autocorrelation, markov-chain, moment-generating-function]
see_also: [single-molecule-localization, structured-illumination-microscopy, super-resolution, rayleigh-criterion, abbe-diffraction-limit, image-noise, method-of-moments, richardson-lucy-deconvolution]
sources:
  - paper: doi:10.1073/pnas.0907866106
    title: "T. Dertinger, R. Colyer, G. Iyer, S. Weiss and J. Enderlein, Fast, background-free, 3D super-resolution optical fluctuation imaging (SOFI), Proceedings of the National Academy of Sciences 106(52), 2009, 22287 to 22292"
    locator: "the model of independent blinking emitters, the cumulant of order n as a sum of n-th powers of the PSF, the removal of background and noise, and the narrowing by the square root of n for a Gaussian PSF"
---

Super-resolution optical fluctuation imaging (SOFI) is an optical method that makes a sharper image from a movie of fluorescent emitters that blink on and off independently. It does not need special optics or isolated emitters. At each pixel it computes a cumulant of order $n$ of the intensity over time, with small time lags. Because the emitters blink independently, the cumulants of different emitters add without cross terms, and each emitter contributes the $n$-th power of its point spread function (PSF), times the $n$-th power of its brightness. A constant background drops out exactly, and noise that is independent from frame to frame drops out when the lags differ. For a Gaussian PSF of width $\sigma$, the $n$-th power is a Gaussian of width $\sigma/\sqrt n$, so the image gets sharper by $\sqrt n$; for other PSFs the narrowing factor is different, but the support of the spectrum grows by $n$. The gain comes from the physical blinking, which the computation measures; a movie of emitters that do not fluctuate gives no gain.

## In plain words

Many small lamps sit closer together than a microscope can separate. Each lamp flickers on its own. The camera sees one blur. At one pixel, the light goes up and down as the nearby lamps flicker. If you measure how strongly the light at a pixel goes up and down, a pixel near the center of one lamp moves a lot, and a pixel between two lamps moves less, because its two lamps flicker independently and partly cancel in the statistics. Higher order statistics sharpen this effect. A steady glow from the background does not go up and down, so it disappears, and camera noise that is new in every frame disappears when you compare different frames.

## The problem

The input is a movie of $T$ frames of $N$ pixels. The model is $F(r, t) = b(r) + \sum_k \varepsilon_k U(r - r_k) s_k(t) + N(r, t)$: a background $b$, emitters at $r_k$ with brightness $\varepsilon_k$ and PSF $U$, independent stationary blinking processes $s_k(t) \in \{0, 1\}$, and noise that is independent from frame to frame. The goal is an image of the emitter positions sharper than the time mean of the movie, which is the widefield image $b + \sum_k \varepsilon_k \rho_k U(r - r_k)$ with the on fractions $\rho_k$.

## The algorithm

Choose the order $n$ and $n$ distinct lags $\tau_1, \ldots, \tau_n$, for example $0, 1, \ldots, n - 1$ frames.

```pseudo id=main
SOFI(movie, n, lags)
L1  for each pixel r
L2      s ← the series F(r, 0), ..., F(r, T - 1)
L3      X_q(t) ← s(t + τ_q) for q = 1, ..., n and t = 0, ..., T - 1 - max τ
L4      center each X_q by its mean over the window
L5      C(r) ← κ_n(X_1, ..., X_n) by the moment formula
L6  return C
```

The moment formulas on the centered series $a, b, c, d$ are $\kappa_2 = \mathbb E[ab]$, $\kappa_3 = \mathbb E[abc]$ and $\kappa_4 = \mathbb E[abcd] - \mathbb E[ab]\mathbb E[cd] - \mathbb E[ac]\mathbb E[bd] - \mathbb E[ad]\mathbb E[bc]$, where $\mathbb E$ is the mean over the window. In expectation the result is

$$C_n(r) = \sum_k \varepsilon_k^n\, U(r - r_k)^n\, \kappa_n[s_k](\tau).$$

## Example

Two emitters of equal brightness sit $2\sigma$ apart under a Gaussian PSF of width $\sigma$. In units of the peak of one PSF:

| image | at an emitter | midway | dip? |
|---|---|---|---|
| widefield, $U(r - r_1) + U(r - r_2)$ | $1 + e^{-2} = 1.1353$ | $2e^{-1/2} = 1.2131$ | no |
| SOFI order 2, $U^2(r - r_1) + U^2(r - r_2)$ | $1 + e^{-4} = 1.0183$ | $2e^{-1} = 0.7358$ | yes, ratio $0.7225$ |

The widefield image has its maximum midway, so it shows one blob. The second order image has a dip of about $28$ percent between the emitters. The test simulates this case with $4000$ frames, a background of $2$, Gaussian noise and Markov blinking with $a = b = 0.3$; the measured ratio is $0.746$, close to the expected $0.7225$ (a measurement, with the error of a finite movie).

For $\sigma = 100$ nm, the width of $U^n$ is $\sigma/\sqrt n = 70.7$, $57.7$ and $50$ nm for $n = 2, 3, 4$, and the full width at half maximum, $2.3548\,\sigma/\sqrt n$, falls from $235.5$ nm for the widefield PSF to $166.5$, $136.0$ and $117.7$ nm.

## Correctness

The proof is in `proofs/correctness.md`. The facts:

1. **Algebra (theorems).** The moment formulas equal the partition formula for the joint cumulant. Cumulants of order $n \ge 2$ ignore added constants, scale with the product of the factors, add over independent sums, and vanish when the variables split into two independent groups.
2. **SOFI formula (theorem, under the model).** With independent stationary emitters, a constant background, noise independent between frames and distinct lags, $C_n(r) = \sum_k \varepsilon_k^n U(r - r_k)^n \kappa_n[s_k](\tau)$. With equal lags, white noise adds its own cumulant, for example its variance at $n = 2$.
3. **One emitter (theorem, exact).** For a single emitter and a constant background the computed image is exactly $\varepsilon^n U^n$ times the sample cumulant of the blinking.
4. **Narrowing (theorem).** For a Gaussian PSF, $U^n$ is a Gaussian of width $\sigma/\sqrt n$. For a PSF whose OTF has the cutoff $k_c$, the spectrum of $U^n$ has the cutoff $n k_c$.
5. **Blinking cumulants (theorem).** For a two-state Markov chain with on fraction $\rho$, the zero-lag cumulants are those of a Bernoulli law, $\kappa_4 = \rho(1 - \rho)(1 - 6\rho(1 - \rho))$ is negative for $0.211 < \rho < 0.789$, and the lag-1 covariance is $\rho(1 - \rho)(1 - a - b)$.

The computed values are cumulants of the sample, which tend to the cumulants of the model as the movie grows (a standard fact for ergodic processes, not proved here).

## Complexity

Each pixel needs $n$ lagged copies of its series, of length at most $T$, and the moment formulas cost $\Theta(T)$ per product, with a number of products that depends only on $n$. Over $N$ pixels this is $\Theta(n N T)$ time for the orders $2$ to $4$, and $\Theta(N + nT)$ extra space for the output and the series of one pixel. The partition formula for a general order has a number of terms that grows like the Bell number of $n$, which is why codes use explicit formulas for small $n$.

## Properties

- **Background-free.** A constant background has no fluctuations and drops out exactly.
- **Noise-free in expectation with distinct lags.** Noise independent between frames has zero cumulant across different frames.
- **Nonlinear in brightness.** Emitter $k$ enters with $\varepsilon_k^n \kappa_n[s_k]$. Bright or strongly blinking emitters dominate, and dim ones vanish as $n$ grows.
- **Sign changes.** Odd and higher cumulants can be negative. For $n = 4$ and on fractions between $0.211$ and $0.789$ the factor $\kappa_4$ is negative, so emitters with different blinking can give values of opposite sign.
- **Needs many frames.** The cumulant estimates have a variance that grows quickly with $n$, so higher orders need longer movies.

## Variants and improvements

- **Cross-cumulants.** Use different pixels for the $n$ factors. For a Gaussian PSF, the cross-cumulant of pixels $r_1, \ldots, r_n$ is $U^n$ centered at the mean of the pixel positions, times a factor that depends only on the distances between the pixels. So it adds new virtual pixels between the real ones and removes the noise even at zero lag, as the noise of different pixels is independent.
- **Deconvolution after SOFI.** Since the spectrum of $U^n$ reaches $n k_c$, a deconvolution of the cumulant image can push the resolution gain from $\sqrt n$ toward $n$.
- **Balanced SOFI.** Combine cumulants of several orders to cancel the brightness and the blinking factor, and so estimate the brightness, the on fraction and the positions.
- **Lags in time.** Longer lags reduce the effect of slow drifts but need blinking that stays correlated over the lag.

## When to use it

Use SOFI when the emitters blink independently, as quantum dots and many dyes do, but are too dense for [single-molecule localization](/single-molecule-localization/), or when the frame rate and the photon budget favor a simple pixelwise computation. It works with a plain widefield microscope, removes the background, and needs no fitting. For the highest resolution with sparse emitters, localization methods give tens of nanometers. For samples that do not blink, use [SIM](/structured-illumination-microscopy/) or deconvolution.

## Pitfalls

- **Correlated blinking or drift.** The formula needs independent emitters and a still sample. Drift, bleaching or a common flicker of the lamp add cross terms. Correct the drift and split long movies into blocks.
- **Equal lags.** With zero lag, white noise adds to the cumulant. Use distinct lags or cross-cumulants.
- **Short movies.** Finite movies leave cross terms between emitters of the order of the statistical error. Check that the image does not change much with half of the frames.
- **Reading values as densities.** The value at a pixel scales with $\varepsilon^n\kappa_n$, not with the number of emitters. Use balanced SOFI or another method for counting.
- **Expecting $\sqrt n$ for any PSF.** The factor $\sqrt n$ holds for a Gaussian PSF.

## Implementations

## History

Dertinger and coworkers introduced SOFI in 2009, using blinking quantum dots. They showed that the cumulant image of order $n$ is the sum of the $n$-th powers of the PSFs, free of background, and they also showed 3D images. Later work developed cross-cumulants for extra pixels, deconvolution of the cumulant images, balanced SOFI for the brightness and the on fraction, and SOFI with dyes and fluorescent proteins.

## References
