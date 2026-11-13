---
tag: F5ZCZM
kind: algorithm
slug: wiener-filter
name: Wiener filter
aliases:
- Wiener deconvolution
- minimum mean-square error filter
area: graphics-and-signals/signal-processing
level: advanced
summary: "The linear filter with the least mean-square error given second-order statistics: solve the Wiener-Hopf equations R w = p, or apply the gain S_x/(S_x + S_n) in each frequency bin."
solves: [signal-denoising]
model: real-ram
complexity:
  vars: {M: the number of taps, N: the number of samples}
  time: {worst: O(M^3 + N M + N log N)}
  space: {extra: O(M^2 + N)}
properties: {deterministic: true, online: false, recursive: false, exact: true}
history:
  year: 1949
  people: [Norbert Wiener, Andrey Kolmogorov, Norman Levinson]
  note: "Wiener derived the optimal linear filter for continuous time in a classified report of 1942, published as a book in 1949; Kolmogorov solved discrete-time prediction in 1941, and Levinson gave the discrete FIR form in 1947."
prereqs: [autocorrelation, power-spectral-density]
see_also: [image-deblurring, signal-denoising, linear-prediction, kalman-filter, lms-algorithm, adaptive-filtering, wiener-khinchin-theorem, tikhonov-regularization]
sources:
  - book: isbn:9780262730051
    title: "Norbert Wiener, Extrapolation, Interpolation, and Smoothing of Stationary Time Series, with Engineering Applications, MIT Press, 1964 paperback edition of the 1949 book"
    locator: "the whole book: the integral equation of Wiener and Hopf for the optimal linear filter, and its solution by factorization of the spectrum"
  - book: isbn:9780132671453
    title: "Simon Haykin, Adaptive Filter Theory, fifth edition, Pearson, 2014"
    locator: "Chapter 2 (Wiener filters: the principle of orthogonality, the Wiener-Hopf equations, the error-performance surface)"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I, Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 12 (linear Bayesian estimators: the linear MMSE estimator, its geometry, and the Wiener filters for smoothing, filtering and prediction)"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 12 (the Wiener filters for filtering and prediction: the FIR filter, the causal IIR filter by spectral factorization, and the noncausal IIR filter)"
  - paper: "N. Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25, 1947"
    locator: "pages 261 to 278, the discrete FIR form of the Wiener filter and the recursion that solves its Toeplitz equations"
---

The Wiener filter is the linear estimator of a desired signal $d$ from an observed signal $x$ that has the least mean-square error, given only second-order statistics: the [autocorrelation](/autocorrelation/) of $x$ and the [cross-correlation](/cross-correlation/) of $d$ with $x$, or the corresponding [power spectral densities](/power-spectral-density/). For an FIR filter with $M$ taps, the best taps solve the Wiener-Hopf equations $R w = p$, a symmetric positive definite Toeplitz system. Without a causality constraint, for a signal in uncorrelated additive noise, the filter is the gain $S_x / (S_x + S_n)$ at each frequency. When the signal and the noise are jointly Gaussian, the Wiener filter is the best of all estimators, linear or not. This page gives the FIR design and the noncausal gain on a block of samples computed with the DFT.

## In plain words

You receive a signal that is a mix of what you want and what you do not want, for example speech plus hiss. You know, on average, how strong each one is at each pitch, and how each one relates to its own past. The Wiener filter uses only that average knowledge to build the best fixed linear filter, the one whose output is closest to the wanted signal on average. At a pitch where the wanted signal is strong and the noise is weak, the filter lets the sound through. Where the noise is strong, it turns the sound down, in proportion. It never boosts. The filter cannot tell the two apart sample by sample; it only weighs them by how strong each is expected to be. So some noise stays and some of the signal is lost. On average, no other linear filter does better.

## The problem

**FIR form.** The inputs are the autocorrelation $r_x[k] = E[x[n]\, x[n-k]]$ and the cross-correlation $r_{dx}[k] = E[d[n]\, x[n-k]]$ for $k = 0, \ldots, M - 1$, the power $\sigma_d^2 = E[d[n]^2]$, and the length $M$, for jointly wide-sense stationary $x$ and $d$. The output is the tap vector $w = (w_0, \ldots, w_{M-1})$ that minimizes

$$J(w) = E\Big[\Big(d[n] - \sum_{k=0}^{M-1} w_k\, x[n-k]\Big)^2\Big],$$

and the minimum $J_{\min}$. If $x = s + v$ with noise $v$ uncorrelated with the signal $s$ and $d = s$, then $r_x = r_s + r_v$ and $r_{dx} = r_s$. With $d[n] = x[n + 1]$ it is the one-step [linear prediction](/linear-prediction/) problem.

**DFT form.** The inputs are a block $y[0 \ldots N-1]$ of a signal $y = x + v$, and the power spectra $S_x[m]$ and $S_n[m]$ of $x$ and $v$ on the $N$-point [DFT](/discrete-fourier-transform/) grid. The output is the linear estimate $\hat x$ of $x$ from $y$ with the least mean-square error, for signal and noise that are uncorrelated, have zero mean, and are circularly stationary on the block. This is the problem of [signal denoising](/signal-denoising/) with known second-order statistics.

## The algorithm

```pseudo id=main
WIENER-FIR(r_x, r_dx, σ_d², M)
L1  R ← (r_x[|i − j|]) for i, j = 0 .. M − 1        ▷ Toeplitz, positive definite
L2  p ← (r_dx[0], .., r_dx[M − 1])
L3  w ← the solution of R w = p                      ▷ the Wiener-Hopf equations
L4  J_min ← σ_d² − pᵀ w
L5  return w, J_min
APPLY-FIR(w, x)
L6  for n ← 0, 1, 2, ... do  d̂[n] ← Σ_{k=0}^{M−1} w_k · x[n − k]      ▷ x[m] = 0 for m < 0
WIENER-DFT(y, S_x, S_n)                             ▷ block y[0..N−1]
L7  H[m] ← S_x[m] / (S_x[m] + S_n[m]) for m = 0 .. N − 1       ▷ H[m] ← 0 if both are 0
L8  X̂[m] ← H[m] · Y[m] for m = 0 .. N − 1, where Y = DFT(y)
L9  return x̂ ← the real part of IDFT(X̂)
```

Line L1 builds the matrix $R = E[u u^T]$ of the tap inputs $u[n] = (x[n], \ldots, x[n-M+1])$, which is Toeplitz because $x$ is stationary. Line L2 builds $p = E[d\, u]$. Line L3 solves the Wiener-Hopf equations; the implementation uses Gaussian elimination, and a Toeplitz solver from [Toeplitz system solving](/toeplitz-system-solving/), such as the [Levinson-Durbin recursion](/levinson-durbin-recursion/), does it in $O(M^2)$. Line L4 is the error that remains, the power of $d$ minus the power that the filter explains. Line L6 is the FIR convolution that runs the filter on data. Lines L7 to L9 are the noncausal filter on one block: line L7 sets the gain of each bin from the ratio of signal power to total power, line L8 scales each DFT coefficient of the block, and line L9 transforms back. When $S_x$ and $S_n$ are even in $m$, as power spectra of real signals are, the inverse DFT is real and line L9 only removes rounding.

## Example

Let $x[n] = \frac12 x[n-1] + e[n]$ with white $e$ of variance $1$, an AR(1) signal with $r_x[k] = \frac43 (\frac12)^{|k|}$, observed in white noise $v$ of variance $1$, and let $d = x$. The observation $y = x + v$ has $r_y[0] = \frac73$ and $r_y[k] = r_x[k]$ for $k \ne 0$, and $p = (r_x[0], \ldots, r_x[M-1])$. For $M = 2$, line L1 gives $R = \begin{bmatrix} 7/3 & 2/3 \\ 2/3 & 7/3 \end{bmatrix}$ and line L2 gives $p = (\frac43, \frac23)$. Then $\det R = 5$ and line L3 gives $w = \frac15 (\frac73 \cdot \frac43 - \frac23 \cdot \frac23,\ -\frac23 \cdot \frac43 + \frac73 \cdot \frac23) = (\frac{8}{15}, \frac{2}{15})$. Line L4 gives $J_{\min} = \frac43 - (\frac43 \cdot \frac{8}{15} + \frac23 \cdot \frac{2}{15}) = \frac43 - \frac45 = \frac{8}{15}$.

| estimate of $x[n]$ | taps | mean-square error |
|---|---|---|
| $0$ | none | $4/3 \approx 1.333$ |
| $y[n]$, no filter | $(1)$ | $1$ |
| $M = 1$ | $(4/7)$ | $4/7 \approx 0.5714$ |
| $M = 2$ | $(8/15, 2/15)$ | $8/15 \approx 0.5333$ |
| $M = 3$ | $(17/32, 1/8, 1/32)$ | $17/32 = 0.53125$ |
| causal IIR, $M \to \infty$ | | $(\sqrt{65} - 7)/2 \approx 0.53113$ |
| noncausal IIR | | $4/\sqrt{65} \approx 0.49614$ |

The error falls with each tap toward the causal limit, and the implementation reaches it to $10^{-12}$ at $M = 30$. The noncausal filter also uses future samples. Its gain is $S_x / (S_x + 1) = 1/(\frac94 - \cos\omega)$, and its error is the average of that gain over $\omega$, since $S_x S_n / (S_x + S_n) = S_x/(S_x + 1)$ here, which is $1/\sqrt{(9/4)^2 - 1} = 4/\sqrt{65}$.

For the DFT form, take $N = 4$, $S_x = (3, 1, 0, 1)$ and $S_n = (1, 1, 1, 1)$. Line L7 gives $H = (\frac34, \frac12, 0, \frac12)$. On the impulse $y = (1, 0, 0, 0)$, $Y = (1, 1, 1, 1)$, and lines L8 and L9 give $\hat x = (\frac{7}{16}, \frac{3}{16}, -\frac{1}{16}, \frac{3}{16})$. This is the impulse response of the noncausal filter, and it is symmetric about $n = 0$ in the circular sense, as a filter with zero phase must be.

## Correctness

**Claim.** If $R$ is positive definite, WIENER-FIR returns the unique tap vector with the least mean-square error among all FIR estimates of length $M$, and $J_{\min}$ is that error. If signal and noise are uncorrelated and circularly stationary and $S_x + S_n > 0$ in every bin, WIENER-DFT returns the linear MMSE estimate $C_x (C_x + C_n)^{-1} y$. For jointly Gaussian data, both are the [conditional expectation](/conditional-expectation/), the best estimate of all.

**Key invariant.** The error surface is a bowl: $J(w) = J_{\min} + (w - w^\ast)^T R\, (w - w^\ast)$, where $w^\ast$ solves line L3. Equivalently, the error of $w^\ast$ is uncorrelated with every tap input, the principle of orthogonality.

The DFT form follows from the same principle in vector form, $\hat x = C_{xy} C_y^{-1} y$, and from the fact that the DFT diagonalizes every circulant matrix, so the matrix inverse becomes a division in each bin. The full proof is below.

## Complexity

Line L1 writes $M^2$ entries, line L3 costs about $M^3/3$ multiplications by Gaussian elimination, and $O(M^2)$ by a Toeplitz solver, and line L4 costs $M$. Running the filter in line L6 costs $M$ multiplications per output sample, so $N M$ for $N$ samples, and an FFT convolution lowers this to $O(N \log M)$ for long filters. The DFT form costs two transforms and $N$ divisions and products: $O(N \log N)$ in the [real RAM](/real-ram/) with the [fast Fourier transform](/fast-fourier-transform/) for $N$ a power of two, which the implementation uses, and $O(N^2)$ with the direct sum for other $N$. The extra space is $O(M^2)$ for $R$, or $O(M)$ with a Toeplitz solver, and $O(N)$ for the spectra of one block.

## Properties

- **Optimal among linear filters.** No linear estimate of the same data has a smaller mean-square error. For jointly Gaussian signals no estimate of any kind does better; for other signals, nonlinear estimates such as wavelet thresholding can.
- **Orthogonal error.** The error of the Wiener filter is uncorrelated with the data it uses, and $J_{\min} = \sigma_d^2 - E[\hat d^2]$: the power of $d$ splits into the power of the estimate and the power of the error.
- **Quadratic error surface.** $J$ is a quadratic bowl with Hessian $2R$ and a unique minimum. Gradient methods such as the [LMS algorithm](/lms-algorithm/) descend this bowl, and their speed depends on the eigenvalues of $R$.
- **Gain between zero and one.** For a signal in uncorrelated noise, $0 \le H \le 1$ in every bin, with $H \approx 1$ where the signal-to-noise ratio is high and $H \approx S_x / S_n$ where it is low. The filter never amplifies, so it removes noise at the cost of attenuating weak parts of the signal.
- **Zero phase.** The noncausal gain is real and even, so the filter does not shift any frequency in time. Its impulse response is two-sided, and it needs the future of the signal.
- **Exactness.** In exact arithmetic lines L1 to L5 are rational functions of the inputs, and the implementation gives exact taps on fractions. The DFT form uses the complex exponential and is computed in floating point.
- **Fixed design.** The filter is designed once from the statistics, which must be known in advance or estimated; it does not track changes in them. Line L6 runs online, sample by sample, after the design.

## Variants and improvements

- **Causal IIR Wiener filter.** For a filter of unbounded length that uses only the present and the past, write $S_y(z) = \sigma^2\, Q(z)\, Q(z^{-1})$ with $Q$ causal and [minimum phase](/minimum-phase/). The filter whitens $y$ with $1/Q$ and keeps the causal part of the result, $H(z) = \frac{1}{\sigma^2 Q(z)} \big[ S_{dy}(z) / Q(z^{-1}) \big]_+$. In the example it gives the error $(\sqrt{65} - 7)/2$.
- **Noncausal IIR Wiener filter.** $H(e^{i\omega}) = S_{dy}(e^{i\omega}) / S_y(e^{i\omega})$, which is $S_x / (S_x + S_n)$ for a signal in uncorrelated noise. Lines L7 to L9 are its version on the DFT grid.
- **Wiener deconvolution.** If $y = h * x + v$ with a known blur $h$, the noncausal filter is $G = \overline{H}\, S_x / (|H|^2 S_x + S_n)$. It is the inverse filter $1/H$ where the noise is weak and goes to zero where it is strong. [Image deblurring](/image-deblurring/) uses it in two dimensions, where it is [Tikhonov regularization](/tikhonov-regularization/) with a weight that depends on frequency.
- **Prediction and smoothing.** With $d[n] = x[n + 1]$, the filter is the linear predictor of [linear prediction](/linear-prediction/); with $d[n] = x[n - L]$ and a delay $L$, it is a fixed-lag smoother that is causal up to the delay.
- **Parametric Wiener filter.** The gain $S_x / (S_x + \alpha S_n)$, or a power of the gain, trades more noise for less distortion when $\alpha < 1$ and the reverse when $\alpha > 1$.
- **Short-time Wiener filter.** For speech in noise, apply the gain frame by frame on a [short-time Fourier transform](/short-time-fourier-transform/), with $S_x$ estimated as $\max(|Y|^2 - S_n, 0)$ or by a smoother rule. This is close to [spectral subtraction](/spectral-subtraction/).
- **Recursive and adaptive forms.** The [Kalman filter](/kalman-filter/) solves the same problem for a state-space model; it allows nonstationary signals, and its steady state for a time-invariant model is the causal Wiener filter. The [LMS](/lms-algorithm/) and [RLS](/rls-algorithm/) algorithms converge to the FIR Wiener taps without knowing $R$ and $p$, see [adaptive filtering](/adaptive-filtering/).

## When to use it

Use the Wiener filter when the signal and the noise are close to stationary, their second-order statistics are known or can be estimated, and a linear filter is acceptable: noise reduction with known spectra, equalization of a known channel, deconvolution, and the design of predictors. Use the FIR form when the filter must be causal and short, and the DFT form for offline processing of a block, where future samples are available. When the statistics change in time or are unknown, use an adaptive filter or the [Kalman filter](/kalman-filter/). When the signal has edges or is sparse in some basis, nonlinear denoising does better than any linear filter; see [signal denoising](/signal-denoising/) and, for images, [image denoising](/image-denoising/).

## Pitfalls

- **The wrong cross-correlation.** Using the autocorrelation of the noisy input in line L2, $p = (r_y[0], \ldots)$, gives $w = (1, 0, \ldots, 0)$, the filter that passes $y$ unchanged. Line L2 must use $E[d\, u]$, which is $r_s$ for a signal in uncorrelated noise.
- **Spectra on different scales.** Line L7 must use $S_x$ and $S_n$ in the same units. A common error is to divide by $|Y[m]|^2$ of one block, which is about $N$ times the power spectrum, while $S_n$ is the noise variance per sample. Either convert $|Y|^2 / N$ to a spectrum estimate or scale $S_n$ by $N$.
- **A negative signal spectrum.** If $S_x$ is estimated as $S_y - S_n$, it can be negative in some bins, and line L7 then gives a negative gain or a gain above one. Clip the estimate at zero before line L7.
- **Circular wrap-around.** Line L8 multiplies DFT coefficients, which is a circular convolution of the block with the impulse response of $H$. On a signal that is not periodic, the ends of the block mix. Process long signals in overlapping frames with a window, or pad each block with zeros before line L8.
- **The modulus instead of the real part.** Returning $|\text{IDFT}(\hat X)|$ in line L9 destroys the sign of every negative sample. Line L9 must take the real part.
- **Ill-conditioned equations.** If the spectrum of $x$ is close to zero at some frequency, $R$ in line L3 is nearly singular and the taps are large and sensitive to errors in the statistics. Add a small multiple of the identity to $R$, a white-noise correction, before line L3.

## Implementations

## History

During the Second World War, Norbert Wiener studied the prediction of the path of an aircraft for anti-aircraft fire control. His classified report of 1942 derived the optimal linear filter for continuous-time stationary processes, an integral equation that he solved with Eberhard Hopf's method of spectral factorization, and it was published as a book in 1949. Andrey Kolmogorov had solved the discrete-time prediction problem independently in 1941. Norman Levinson, in an appendix to Wiener's book and a paper of 1947, gave the discrete-time FIR form and the recursion that solves its Toeplitz equations in $O(M^2)$. Bode and Shannon gave a simpler derivation through whitening in 1950. Kalman's filter of 1960 extended the theory to nonstationary signals described by a state-space model.

## References
