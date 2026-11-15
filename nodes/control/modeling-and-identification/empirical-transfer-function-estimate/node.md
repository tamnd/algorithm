---
tag: H22G0R
kind: algorithm
slug: empirical-transfer-function-estimate
name: Empirical transfer function estimate
aliases:
- ETFE
area: control/modeling-and-identification
level: core
summary: Estimates the frequency response as the ratio of the DFTs of output and input, and smooths it with a window to cut the variance.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, M: the half width gamma of the smoothing window}
  time: {worst: O(N log N + N M)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 1985
  people: [Lennart Ljung]
  note: "The ratio of output and input Fourier transforms is the oldest frequency analysis of a system; Ljung's 1985 paper on the estimation of transfer functions and his textbook, which uses the name empirical transfer function estimate, made it the basic nonparametric estimate of system identification."
prereqs: [frequency-response, discrete-fourier-transform, system-identification]
see_also: [fast-fourier-transform, periodogram, welch-method, bode-plot, prbs-input, persistent-excitation, output-error-model, least-squares-arx-identification]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 6 (nonparametric frequency-domain methods: the empirical transfer function estimate, its bias and variance, and smoothing by spectral analysis)"
  - paper: doi:10.1016/0005-1098(85)90042-1
    title: "Lennart Ljung, On the estimation of transfer functions, Automatica 21(6), 677-696, 1985"
    locator: nonparametric estimation of transfer functions and the frequency-domain view of bias and variance
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: the chapter on nonparametric methods (frequency analysis, Fourier analysis and spectral analysis)
---

The empirical transfer function estimate, or ETFE, estimates the [frequency response](/frequency-response/) $G(e^{i\omega})$ of a linear system from one record of $N$ input and output samples, with no model structure. It takes the [discrete Fourier transforms](/discrete-fourier-transform/) $U_k$ and $Y_k$ of the input and the output and returns their ratio $\hat G_k = Y_k / U_k$ at the frequencies $\omega_k = 2\pi k / N$ where $U_k \ne 0$. With a [fast Fourier transform](/fast-fourier-transform/) this costs $O(N \log N)$. For a periodic input in periodic steady state the ratio is exact up to the noise term $V_k / U_k$, but that term does not shrink as $N$ grows: the raw estimate stays as noisy at $N = 4096$ as at $N = 256$. A smoothed ETFE therefore averages the raw values over $2\gamma + 1$ neighboring frequencies, weighted by a window and by $\lvert U \rvert^2$, which trades a small bias for a variance that falls with $\gamma$.

## In plain words

Any input can be split into sine waves of different frequencies, and a linear system changes each sine wave only by scaling it and shifting it in time. So if you split both the input and the output into their sine waves and divide one by the other, frequency by frequency, you get the scaling and the shift at each frequency. That table is the frequency response, read straight off the data. The catch is noise: each frequency gets its own share of the noise, and recording for longer only gives you more frequencies, each one as noisy as before. To get a clean curve, you average each value with its neighbors, at the cost of blurring sharp peaks.

## The problem

**Input.** Samples $u(0), \ldots, u(N-1)$ and $y(0), \ldots, y(N-1)$ of a system $y = G(q)\, u + v$ with an additive disturbance $v$, and a half width $\gamma$ with $0 \le \gamma < N/2$. The sampling period $h$ only rescales the frequency axis: $\omega_k$ corresponds to $\omega_k / h$ radians per unit time.

**Transforms.** $U_k = \sum_{t=0}^{N-1} u(t)\, e^{-i \omega_k t}$ and $Y_k$ likewise, with $\omega_k = 2\pi k/N$.

**Output.** For $k = 0, \ldots, \lfloor N/2 \rfloor$, an estimate $\hat G_k$ of $G(e^{i\omega_k})$, or "undefined" where the input has no energy. The values for $k > N/2$ are the complex conjugates, because the data are real.

## The algorithm

```pseudo id=main
ETFE(y, u, ⟨γ⟩)
L1  Y ← DFT(y);  U ← DFT(u)
L2  for k ← 0 to ⌊N/2⌋ do
L3      if γ = 0 and |U_k| ≤ tol · max |U| then G_k ← undefined
L4      else if γ = 0 then G_k ← Y_k / U_k
L5      else
L6          G_k ← Σ_{|j| ≤ γ} W_j Y_{k+j} conj(U_{k+j}) / Σ_{|j| ≤ γ} W_j |U_{k+j}|^2, indices mod N, W_j = (1 + cos(π j / (γ + 1))) / 2; undefined if the denominator is 0
L7  return the pairs (ω_k, G_k)
```

Line L1 is two transforms, by the radix-2 FFT when $N$ is a power of 2. Line L3 refuses to divide where the input has no energy; the relative tolerance tol treats rounding residue as zero. Line L6 is the smoothed estimate with a Hann window. Because $W_j Y_m \overline{U_m} = W_j \lvert U_m \rvert^2 \cdot (Y_m / U_m)$, it is the average of the raw ratios over the window, each weighted by $W_j \lvert U_m \rvert^2$; frequencies where the input is weak count little. With $\gamma = 0$ the formula of L6 reduces to the raw ratio of L4.

## Example

Take $G(q) = q^{-1}/(1 - 0.5\, q^{-1})$, the input $u = (1, 1, -1, -1)$ repeated, and the output in periodic steady state, $y = (-1.2, 0.4, 1.2, -0.4)$; for instance $y(0) = 0.5\, y(3) + u(3) = -0.2 - 1 = -1.2$. Here $N = 4$ and $\gamma = 0$.

| $k$ | $\omega_k$ | $U_k$ | $Y_k$ | $\hat G_k$ | $G(e^{i\omega_k})$ |
|---|---|---|---|---|---|
| 0 | $0$ | $0$ | $0$ | undefined | $2$ |
| 1 | $\pi/2$ | $2 - 2i$ | $-2.4 - 0.8i$ | $-0.4 - 0.8i$ | $-0.4 - 0.8i$ |
| 2 | $\pi$ | $0$ | $0$ | undefined | $-2/3$ |

At $k = 1$, $(-2.4 - 0.8i)/(2 - 2i) = (-2.4 - 0.8i)(2 + 2i)/8 = (-3.2 - 6.4i)/8 = -0.4 - 0.8i$, and $G(e^{i\pi/2}) = -i/(1 + 0.5 i) = -0.4 - 0.8i$, so the estimate is exact. The input has zero mean and alternates in pairs, so it has no energy at $\omega = 0$ or $\omega = \pi$, and L3 returns "undefined" there: the data say nothing about the gain at those frequencies.

## Correctness

**Claim.** Suppose $G$ is BIBO stable, $u$ is periodic with period $N$, and $y = G(q)\, u + v$ in periodic steady state. Then for every $k$ with $U_k \ne 0$, $\hat G_k = G(e^{i\omega_k}) + V_k / U_k$, where $V_k$ is the DFT of $v$; with $v = 0$ the raw ETFE is exact. If $v$ is white with variance $\sigma^2$, then $\mathbb{E} \lvert \hat G_k - G(e^{i\omega_k}) \rvert^2 = N \sigma^2 / \lvert U_k \rvert^2$, and the smoothed value of L6 is the $W_j \lvert U \rvert^2$-weighted average of the raw values.

**Key invariant.** For an $N$-periodic input and an absolutely summable impulse response $g$, a delay by $\ell$ multiplies the DFT by $e^{-i\omega_k \ell}$, so $\sum_\ell g_\ell\, u(t - \ell)$ has the DFT $\sum_\ell g_\ell e^{-i\omega_k \ell}\, U_k = G(e^{i\omega_k})\, U_k$.

The noise formula follows because the DFTs of white noise at distinct frequencies of the grid are uncorrelated, each with variance $N\sigma^2$. The full proof is below.

## Complexity

Line L1 costs $O(N \log N)$ with an FFT; the reference code uses the radix-2 FFT for powers of 2 and the direct $O(N^2)$ sum otherwise. Lines L3 and L4 cost $O(1)$ per frequency, and L6 costs $O(\gamma)$, so the loop costs $O(N)$ raw and $O(N \gamma)$ smoothed. The total is $O(N \log N + N \gamma)$ arithmetic operations and evaluations of $\cos$ and $e^{i x}$ in the [real RAM](/real-ram/), with $O(N)$ extra space for the two transforms. Smoothing by a window of fixed shape is a circular convolution and can also be done by FFT in $O(N \log N)$ for any $\gamma$.

## Properties

- **Exact in periodic steady state (theorem).** With a periodic input, a whole number of periods in the record and no noise, $\hat G_k = G(e^{i\omega_k})$ wherever $U_k \ne 0$; with a [PRBS](/prbs-input/) of period $N$ every $U_k$ with $k \ne 0$ is nonzero.
- **Variance does not go to 0 (theorem).** The error $V_k / U_k$ has mean square $N\sigma^2 / \lvert U_k \rvert^2$ for white noise. For a signal of fixed power, $\lvert U_k \rvert^2$ grows like $N$, so this stays about $\sigma^2$ divided by the input power at that frequency; a longer record gives more frequencies, not more accurate ones. For a general disturbance and a random input the limit is the ratio $\Phi_v(\omega)/\Phi_u(\omega)$ of the disturbance and input spectra (Ljung 1999, Chapter 6).
- **Measurement.** For the system above with a white $\pm 1$ input and white output noise of standard deviation $0.5$, the median squared error of the raw ETFE over the frequencies was $0.257$, $0.269$ and $0.243$ for $N = 256$, $1024$ and $4096$. With $\gamma = N/32$ it was $0.0211$, $0.0041$ and $0.00106$.
- **Variance reduction by the Hann window (computation).** For $\gamma \ge 1$, $\sum_{|j| \le \gamma} W_j = \gamma + 1$ and $\sum_{|j| \le \gamma} W_j^2 = \frac34 (\gamma + 1)$. Where $\lvert U \rvert$ is constant over the window, the smoothed error has variance $\frac{3}{4(\gamma + 1)}$ times that of the raw error, for example $\frac{3}{16}$ for $\gamma = 3$.
- **Bias of smoothing.** The smoothed value averages $G$ over a band of width about $4\pi\gamma/N$, so it flattens resonance peaks narrower than that band.
- **Transients (theorem).** For a nonperiodic input the record does not start in steady state, and $\hat G_k$ gains an extra term $T_k / U_k$. For a bounded input and a $G$ whose impulse response satisfies $\sum_\ell \ell \lvert g_\ell \rvert < \infty$, $\lvert T_k \rvert$ is bounded by a constant independent of $N$, while $\lvert U_k \rvert$ typically grows like $\sqrt N$, so this term falls like $1/\sqrt N$ (Ljung 1999, Chapter 6).

## Variants and improvements

- **Periodic excitation and averaging over periods.** Repeat a period of length $P$ several times, drop the first period, and average $Y_k$ over periods before dividing. The noise variance then falls with the number of periods, with no smoothing bias.
- **Spectral analysis.** Estimate the cross spectrum $\hat\Phi_{yu}$ and the input spectrum $\hat\Phi_u$ with a lag window or by [Welch's method](/welch-method/), and take their ratio. This is the same idea as L6 with a different window.
- **Other windows.** Bartlett, Parzen or rectangular frequency windows in place of the Hann weights in L6, with the same trade between bias and variance.
- **Local polynomial and local rational methods.** Fit a low-order polynomial in frequency to $Y$ and $U$ around each $\omega_k$, which also removes the transient term.
- **Parametric fit in frequency.** Fit an [output error](/output-error-model/) or other parametric model to the ETFE by weighted least squares in the frequency domain.

## When to use it

Use it as the first look at new data: a [Bode plot](/bode-plot/) of the smoothed ETFE shows the bandwidth, resonances and delay before any model order is chosen, and it checks a parametric model. It is most accurate with a periodic input such as a PRBS of period $N$ in steady state. Do not use the raw estimate for design without smoothing or averaging, and do not use it on closed-loop data, where the ratio estimates a mixture of the plant and the inverse of the controller.

## Pitfalls

- **Dividing by an input with no energy.** At a frequency where $U_k = 0$ or nearly so, the ratio in L4 is undefined or pure noise. Keep the test of L3, and design the input so that $\lvert U_k \rvert$ is large at the frequencies of interest.
- **Expecting a longer record to help.** Computing L4 for a larger $N$ gives a finer grid with the same scatter. Use L5 and L6 with $\gamma > 0$, or average over periods.
- **Smoothing $Y/U$ instead of $Y \overline U$.** Averaging the raw ratios of L4 with equal weights lets frequencies with tiny $\lvert U_k \rvert$ dominate. L6 must weight by $\lvert U \rvert^2$, as in the ratio of the window sums.
- **A non-integer number of periods.** With a periodic input, a record that does not hold a whole number of periods leaks energy between frequencies. In L1, transform an integer number of periods taken after the transient.
- **Too wide a window.** A large $\gamma$ in L6 smears a sharp resonance over many frequencies and lowers its peak. Choose $\gamma$ so that $4\pi\gamma/N$ is well below the width of the narrowest peak.

## Implementations

## History

Frequency analysis by sine wave tests and by Fourier transforms of input and output is the oldest way to identify a linear system. Smoothing of raw Fourier ratios follows the spectral analysis of Blackman and Tukey in 1958 and of Jenkins and Watts in 1968, where averaging over frequencies controls the variance of the periodogram. Ljung's 1985 paper on the estimation of transfer functions, and his textbook, treat the ratio as the empirical transfer function estimate, analyze its bias and variance and connect it to the frequency-domain view of parametric methods.

## References
