---
tag: WPM8SW
kind: algorithm
slug: savitzky-golay-filter
name: Savitzky-Golay filter
aliases:
- least-squares smoothing filter
area: graphics-and-signals/signal-processing
level: core
summary: "Fit a polynomial of degree p by least squares to each window of 2m + 1 samples and read the fit at the center. The result is a symmetric FIR filter that keeps peaks better than an average."
solves: [signal-denoising]
model: real-ram
complexity:
  vars: {N: the number of samples, m: the window radius (width 2m + 1), p: the degree of the fit}
  time: {worst: O(N m), average: O(N m), best: O(N m), per_sample: O(m), setup: O(m^2 p^3)}
  space: {extra: O(m p)}
properties: {linear: true, causal: false, stable: true, linear_phase: "true, zero phase when centered", deterministic: true, online: true, in_place: false}
history:
  year: 1964
  people: [Abraham Savitzky, Marcel J. E. Golay]
  note: Savitzky and Golay showed in 1964 that a local least squares polynomial fit at equally spaced points is a convolution with fixed integer weights, and they gave tables of the weights for smoothing and for derivatives.
prereqs: [least-squares-approximation, fir-filter]
see_also: [moving-average, median-filter, curve-fitting, smoothing-spline, orthogonal-polynomials, normal-equations, gram-schmidt-process, signal-denoising]
sources:
  - paper: doi:10.1021/ac60214a047
    title: Abraham Savitzky and Marcel J. E. Golay, Smoothing and Differentiation of Data by Simplified Least Squares Procedures, Analytical Chemistry 36(8), 1964
    locator: pp. 1627 to 1639 (the fit as a convolution with fixed integers, and the tables of weights for smoothing and for derivatives)
  - paper: doi:10.1021/ac60319a045
    title: Jean Steinier, Yves Termonia and Jules Deltour, Smoothing and Differentiation of Data by Simplified Least Square Procedure, Analytical Chemistry 44(11), 1972
    locator: pp. 1906 to 1909 (corrections to the tables of 1964)
  - paper: doi:10.1021/ac00205a007
    title: Peter A. Gorry, General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method, Analytical Chemistry 62(6), 1990
    locator: pp. 570 to 573 (weights from Gram polynomials for every position in the window, which treats the ends of the data)
  - paper: doi:10.1109/MSP.2011.941097
    title: Ronald W. Schafer, What Is a Savitzky-Golay Filter?, IEEE Signal Processing Magazine 28(4), 2011
    locator: pp. 111 to 117 (the filter as a linear phase FIR filter, its frequency response and its cutoff)
---

A Savitzky-Golay filter smooths a signal, or estimates its derivative, by a local fit. For each output sample $y[n]$ it takes the $2m + 1$ samples $x[n-m], \ldots, x[n+m]$, fits a polynomial of degree $p$ to them by least squares, and reads the fitted polynomial (or its derivative) at the center. Abraham Savitzky and Marcel Golay showed in 1964 that this value is a fixed weighted sum $\sum_i c_i\, x[n+i]$, with weights that depend only on $m$, $p$ and the derivative order, not on the data. So the filter is an [FIR filter](/fir-filter/) with $2m + 1$ symmetric taps, and it costs $2m + 1$ multiplies per output sample. It keeps every polynomial of degree $p$ exactly, so it keeps the height and width of peaks much better than a [moving average](/moving-average/) of the same width. Frequencies on this page are $\omega$ in radians per sample, $\omega \in [-\pi, \pi]$.

## In plain words

Look at a short stretch of the signal around the current sample. Draw the smooth curve of a chosen shape, such as a parabola, that passes as close as possible to all the samples in the stretch. Take the height of that curve at the middle. That is the new sample. Then move one step and do it again.

A plain average is the same idea with a flat line, so it cuts the tops off peaks. A parabola can follow a peak, so the peak keeps its height. The surprise is that you never need to fit any curve while you filter. The middle height of the best curve is always the same weighted sum of the samples, so you compute the weights once and use them everywhere.

## The problem

The input is a signal $x[0 \ldots n-1]$ of real numbers at equally spaced points, a radius $m \ge 0$, a degree $p$ with $0 \le p \le 2m$, and a derivative order $d$ with $0 \le d \le p$. In a window, the offsets are $i = -m, \ldots, m$.

For the window around $k$, let $q_k$ be the polynomial of degree at most $p$ that minimizes $\sum_{i=-m}^{m} \big(x[k+i] - q_k(i)\big)^2$. It is unique, because $2m + 1 > p$ distinct points give a [Vandermonde matrix](/vandermonde-matrix/) of full column rank. The output is $y[k] = q_k^{(d)}(0)$, the value of the fit ($d = 0$) or of its derivative of order $d$, in units of the sample spacing. For a sample within $m$ of an end, there is no centered window. The method here uses the first (or last) full window and reads its fit at the offset of the sample, as Gorry proposed.

This is a [least squares approximation](/least-squares-approximation/) problem in each window, and the filter is one method of [signal denoising](/signal-denoising/).

## The algorithm

The weights come from the polynomials $P_0, \ldots, P_p$ that are orthogonal for the inner product $\langle f, g \rangle = \sum_{i=-m}^{m} f(i)\, g(i)$, the Gram polynomials. With an orthogonal basis the fit is a sum of independent projections, so no linear system is solved.

```pseudo id=main
SG-WEIGHTS(m, p, t, d)                       ▷ weights c[−m … m] for the derivative of order d at offset t
L1  for k ← 0 to p do P_k ← x^k
L2      for j ← 0 to k − 1 do P_k ← P_k − (⟨P_k, P_j⟩ / ⟨P_j, P_j⟩) P_j     ▷ Gram-Schmidt
L3  for k ← 0 to p do ν_k ← Σ_i P_k(i)²       ▷ c[i] = 0 at the start
L4      a_k ← P_k^(d)(t)
L5      for i ← −m to m do c[i] ← c[i] + P_k(i) a_k / ν_k

SAVITZKY-GOLAY(x[0 … n − 1], m, p, d)        ▷ inside, b = k − m and t = 0
L6  for k ← 0 to n − 1 do                     ▷ near an end, b is the first or last full window and t = k − b − m
L7      y[k] ← Σ_{i=−m}^{m} c_t[i] · x[b + m + i]
```

Lines L1 and L2 are the [Gram-Schmidt process](/gram-schmidt-process/) on $1, x, \ldots, x^p$ with the inner product of the window. The fit of a window $w$ is the orthogonal projection $q = \sum_k (\langle w, P_k \rangle / \nu_k) P_k$. Its derivative at $t$ is $\sum_i w_i \sum_k P_k(i)\, P_k^{(d)}(t) / \nu_k$, which is linear in $w$, and line L5 collects the factor of each $w_i$. The interior uses one set of weights, the center weights $c = c_0$. Only the first and last $m$ outputs need other weights. The weights are rational numbers, and an exact implementation computes them with fractions.

## Example

**The weights for $m = 2$, $p = 2$.** On the points $-2, \ldots, 2$ the Gram polynomials are $P_0 = 1$, $P_1 = x$ and $P_2 = x^2 - 2$, with $\nu_0 = 5$, $\nu_1 = 10$ and $\nu_2 = 14$. At $t = 0$, $P_0(0) = 1$, $P_1(0) = 0$ and $P_2(0) = -2$. So

$$c_i = \frac{1}{5} - \frac{2(i^2 - 2)}{14}, \qquad (c_{-2}, \ldots, c_2) = \frac{1}{35}(-3, 12, 17, 12, -3).$$

These are the classic weights of the 1964 paper. The first derivative at the center uses only $P_1$: $c_i = i/10$, which gives $\frac{1}{10}(-2, -1, 0, 1, 2)$. The weights of the left end, $t = -2$, are $\frac{1}{35}(31, 9, -3, -5, 3)$.

**A short signal.** Take $x = [1, 3, 8, 5, 4, 6, 9]$ with $m = 2$ and $p = 2$.

| $k$ | window | weights | $y[k]$ |
|---|---|---|---|
| 0 | 1, 3, 8, 5, 4 | $t = -2$ | $21/35 = 3/5$ |
| 1 | 1, 3, 8, 5, 4 | $t = -1$ | $22/5$ |
| 2 | 1, 3, 8, 5, 4 | center | $217/35 = 31/5$ |
| 3 | 3, 8, 5, 4, 6 | center | $202/35$ |
| 4 | 8, 5, 4, 6, 9 | center | $149/35$ |
| 5 | 8, 5, 4, 6, 9 | $t = 1$ | $197/35$ |
| 6 | 8, 5, 4, 6, 9 | $t = 2$ | $64/7$ |

For $k = 3$: $(-3 \cdot 3 + 12 \cdot 8 + 17 \cdot 5 + 12 \cdot 4 - 3 \cdot 6)/35 = 202/35 \approx 5.77$.

**A peak.** Take $x = [0, 0, 0, 4, 8, 4, 0, 0, 0]$. At the top, the Savitzky-Golay filter with $m = 2$, $p = 2$ gives $(12 \cdot 4 + 17 \cdot 8 + 12 \cdot 4)/35 = 232/35 \approx 6.63$. A moving average of 5 gives $16/5 = 3.2$. The fit also gives small negative values, $-16/35$, at three samples from the peak, where the input is 0.

## Correctness

The weights are correct because the least squares fit is the orthogonal projection onto the polynomials of degree at most $p$, and the Gram polynomials are an orthogonal basis of that space. The projection is linear in the data, so the value at $t$ is a fixed weighted sum, and line L5 computes its weights. Three facts follow from the same formula. The weights reproduce polynomials of degree $p$: $\sum_i c_i\, q(i) = q(0)$. Their squares add up to the center weight, $\sum_i c_i^2 = c_0$. And for smoothing the degrees $2j$ and $2j + 1$ give the same center weights, because $P_{2j+1}$ is odd and vanishes at 0. The full proofs, with a check against the [normal equations](/normal-equations/), are in the proof file.

## Complexity

The cost model is real arithmetic operations.

- **Filtering.** $2m + 1$ multiplies and $2m$ additions per output sample. The center weights are symmetric, $c_{-i} = c_i$, so adding $x[k-i] + x[k+i]$ first needs only $m + 1$ multiplies. The total is $O(Nm)$.
- **Weights.** Gram-Schmidt on $p + 1$ polynomials over $2m + 1$ points costs $O(m p^3)$ as written, or $O(m p)$ with the three-term recurrence of the Gram polynomials. This is done once for each $(m, p, d)$, plus once for each of the $2m$ end positions, so all the weights cost $O(m^2 p^3)$, or $O(m^2 p)$.
- **Space.** The weights and the polynomials take $O(mp)$ space. A streaming version keeps the last $2m + 1$ inputs.

Direct fitting with the [normal equations](/normal-equations/) in every window would cost $O(m p^2 + p^3)$ per sample.

## Properties

- **Linear and time invariant.** Inside the signal it is the convolution with fixed taps. It is a type 1 linear phase FIR filter with $2m + 1$ symmetric taps.
- **Zero phase, not causal.** Centered, the frequency response $H(e^{i\omega}) = c_0 + 2\sum_{i=1}^{m} c_i \cos(i\omega)$ is real. A causal version outputs $y[k - m]$ at time $k$, which is a delay of $m$ samples.
- **Stable.** It is an FIR filter, so it is stable.
- **Reproduces polynomials.** For $q$ of degree at most $p$, $\sum_i c_i\, q(k + i) = q(k)$. In the frequency domain, for even $p$, $H(e^{i\omega}) = 1 + O(\omega^{p+2})$, so the pass band is very flat at $\omega = 0$.
- **Noise gain.** For white noise of variance $\sigma^2$, the output variance is $\sigma^2 \sum_i c_i^2 = c_0 \sigma^2$. For $m = 2$: $p = 0$ gives $1/5$, $p = 2$ gives $17/35$ and $p = 4$ gives 1, because the fit then passes through all five points. For $m = 3$, $p = 2$ gives $1/3$. A higher degree keeps more shape and removes less noise.
- **Even and odd degrees.** For smoothing, $p = 2j$ and $p = 2j + 1$ give the same center weights. For the first derivative, $p = 2j - 1$ and $p = 2j$ give the same.
- **Poor stop band.** For $m = 2$, $p = 2$, $H(e^{i\pi}) = -13/35$. High frequencies are reduced, but not removed.

## Variants and improvements

- **Derivatives.** Set $d \ge 1$ to estimate derivatives of a noisy signal. Divide by $h^d$ for a sample spacing $h$.
- **Ends of the data.** Read the fit of the first or last window at an off center point (used here), shorten the window, or mirror the signal. The off center weights are not symmetric and amplify noise more.
- **Even window length.** Fit at half integer points to get a filter with an even number of taps and a half sample delay.
- **Two dimensions.** Fit a surface of total degree $p$ to a square block. The weights are again a fixed kernel, but it is usually not separable.
- **Nonuniform samples.** The weights then change from window to window, and each window needs its own fit. In a later paper Gorry extended his method to this case.
- **Other local fits.** Weighted local fits, such as LOESS, give each point in the window a weight that falls with distance. A [smoothing spline](/smoothing-spline/) fits one curve to the whole signal instead of one polynomial per window.

## When to use it

Use a Savitzky-Golay filter to smooth spectra, chromatograms and other measured curves when the height, position and width of peaks matter, and to estimate derivatives of noisy data. Choose the window so that it is narrower than the narrowest peak, and the degree as 2 or 4. For a hard cutoff in frequency, design a low-pass [FIR filter](/fir-filter/) with [digital filter design](/digital-filter-design/) methods instead. For impulse noise, use the [median filter](/median-filter/). For a fit of a global model, see [curve fitting](/curve-fitting/).

## Pitfalls

- **Degree too high.** With $p = 2m$ the fit interpolates every point and the filter does nothing. With $p$ close to $2m$ it removes little noise.
- **Window too wide.** A window wider than a peak flattens the peak and shifts its sides, even with a quadratic fit.
- **Overshoot.** Some weights are negative, so the output can dip below the input range next to a sharp feature, as in the peak example.
- **Normal equations in floating point.** Solving $V^\top V a = V^\top x$ with powers $i^j$ is badly conditioned for large $m$ and $p$. Use orthogonal polynomials, a QR factorization or exact fractions to compute the weights.
- **Old tables.** Some of the tables of 1964 have errors. Steinier, Termonia and Deltour corrected them in 1972. Compute the weights instead of copying them.
- **Spacing and derivatives.** The derivative weights assume unit spacing. Forgetting the factor $h^{-d}$ scales the result.

## Implementations

## History

Abraham Savitzky and Marcel J. E. Golay published the method in Analytical Chemistry in 1964. They showed that a local polynomial fit at equally spaced points reduces to a convolution with integers and a normalizing constant, and they printed tables of these integers for smoothing and for the first derivatives. Steinier, Termonia and Deltour corrected errors in the tables in 1972. In 1990 Peter Gorry used Gram polynomials to give the weights for every position in the window, which solved the problem of the end points. In 2011 Ronald Schafer described the filter for the signal processing community as a linear phase FIR filter and studied its frequency response.

## References
