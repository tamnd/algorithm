---
tag: 4T3X0R
kind: algorithm
slug: mmse-linear-equalizer
name: MMSE linear equalizer
aliases:
- MMSE equalizer
- linear MMSE equalizer
area: communications/channel-estimation-and-equalization
level: core
summary: "The FIR filter that minimizes the mean squared error between its output and the delayed symbols. It solves (Es H H^H + N0 I) f = Es H e, trades residual ISI for less noise, and is biased."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of equalizer taps, L: the number of channel taps, K: the number of symbols}
  time: {worst: O(N^2 (N + L) + K N)}
  space: {extra: O(N (N + L))}
properties: {deterministic: true, linear: true, needs_noise_level: true, biased: true, minimizes_mse_over_linear_filters: true}
history:
  year: 1969
  people: [Allen Gersho]
  note: "Gersho studied the mean-square error criterion for adaptive equalizers of highly dispersive telephone channels, in place of the peak distortion of Lucky. The optimal taps are the finite-length Wiener filter."
prereqs: [channel-equalization, wiener-filter, zero-forcing-equalizer]
see_also: [fractionally-spaced-equalizer, decision-feedback-equalizer, mmse-dfe-canonical-theorem, frequency-domain-equalization, lmmse-channel-estimation, mmse-mimo-detector, mmse-multiuser-detector, regularized-zero-forcing-precoding]
sources:
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.4-2 (the mean-square error criterion) and Section 9.4-3 (the performance of the MSE equalizer)"
  - book: isbn:9780792375487
    title: "John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004"
    locator: "Chapter 8 (equalization)"
  - paper: "A. Gersho, Adaptive equalization of highly dispersive channels for data transmission, Bell System Technical Journal 48(1), 1969, pages 55 to 70"
    locator: "the mean-square error criterion for the equalizer taps"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 12 (linear Bayesian estimators and the Wiener filter)"
---

The MMSE linear equalizer is the FIR filter that makes its output as close as possible, in mean squared error, to the transmitted symbol a few samples back. A channel $h$ of $L$ taps smears each symbol into its neighbors, and white noise of power $N_0$ is added. The [zero-forcing equalizer](/zero-forcing-equalizer/) inverts the channel and ignores the noise, so it amplifies the noise wherever the channel is weak. The MMSE equalizer minimizes the sum of the residual [intersymbol interference](/intersymbol-interference/) and the noise. Its $N$ taps solve one Hermitian linear system, the finite-length [Wiener filter](/wiener-filter/): $(E_s H H^H + N_0 I) f = E_s H e_\Delta$, with $c = \bar f$. At high SNR it tends to a ZF design, and at low SNR to a matched filter. The same formula with a channel matrix in place of a convolution is the [MMSE MIMO detector](/mmse-mimo-detector/), the [MMSE multiuser detector](/mmse-multiuser-detector/) for CDMA, and, at the transmitter, [regularized ZF precoding](/regularized-zero-forcing-precoding/). The [LMMSE channel estimator](/lmmse-channel-estimation/) solves the same kind of equation for the channel instead of the symbols.

## In plain words

The channel adds echoes of each symbol to the next samples, and it adds noise. A linear equalizer is a short filter that combines a few received samples with fixed weights to recover one symbol. The zero-forcing choice of weights cancels the echoes completely, but if the channel is weak at some frequency, it boosts the noise there by a large factor. The MMSE choice asks a different question: which weights make the output closest to the symbol on average, counting echoes and noise together? The answer leaves a little echo in place and boosts the noise much less. It needs the channel and the noise level. The output is a little smaller than the symbol on average, so a QAM slicer must scale it first.

## The problem

The input is the channel $h = (h_0, \ldots, h_{L-1})$, known or estimated, the noise power $N_0$, the symbol energy $E_s$, the number of taps $N$ and the decision delay $\Delta$, with $0 \le \Delta \le N + L - 2$. The received samples are $y[n] = \sum_l h_l\, x[n-l] + w[n]$ at one sample per symbol, with independent symbols of mean zero and energy $E_s$, and $w[n] \sim \mathcal{CN}(0, N_0)$. The equalizer output is $z[n] = \sum_{i=0}^{N-1} c_i\, y[n-i]$. The output is the tap vector $c$ that minimizes $J = E|z[n] - x[n - \Delta]|^2$, and the minimum $J$.

Stack the last $N$ samples in $u = (y[n], \ldots, y[n-N+1])^T$. Then $u = H s + v$, where $s = (x[n], \ldots, x[n-N-L+2])^T$ and $H$ is the $N \times (N + L - 1)$ convolution matrix with $H_{ij} = h_{j-i}$. With $f = \bar c$, the output is $z[n] = f^H u$, a linear estimate of the entry $\Delta$ of $s$.

## The algorithm

```pseudo id=main
MMSE-EQUALIZER(h, N, Δ, N0, Es)
L1  H[i][j] ← h[j - i]  for 0 ≤ i < N, 0 ≤ j < N + L - 1    ▷ h[t] = 0 outside 0 .. L - 1
L2  R ← Es H Hᴴ + N0 I                                      ▷ the covariance of u
L3  r ← Es H e_Δ                                            ▷ column Δ of H, times Es
L4  f ← R⁻¹ r                                               ▷ Gaussian elimination or Cholesky
L5  c ← conj(f)                                             ▷ the taps, z[n] = Σ c[i] y[n - i]
L6  J ← Es - rᴴ f                                           ▷ the minimum mean squared error
L7  return c, J
```

Line L1 builds the convolution matrix. Line L2 is the covariance of the received vector: $E_s H H^H$ from the symbols and $N_0 I$ from the noise. Line L3 is the cross-correlation between the received vector and the wanted symbol $x[n - \Delta]$. Line L4 solves the Wiener-Hopf equations $R f = r$. $R$ is Hermitian positive definite, so a [Cholesky factorization](/cholesky-decomposition/) works. Line L6 gives the error without a simulation. The delay is a design choice: the implementation also tries every $\Delta$ and keeps the one with the smallest $J$.

## Example

Take $h = (1, 0.5)$, $E_s = 1$, $N_0 = 0.1$ (an SNR of 10 dB), and $N = 5$ taps. The minimum error $J$ for each delay is:

| $\Delta$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $J$ | 0.11404 | 0.11197 | 0.11547 | 0.13606 | 0.24147 | 0.77851 |

The best delay is $\Delta = 1$. Its taps and the combined response $g = c * h$ are:

| | index 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| taps $c$ | 0.05090 | 0.86258 | -0.37987 | 0.16306 | -0.06039 | |
| combined $g$ | 0.05090 | 0.88803 | 0.05142 | -0.02687 | 0.02114 | -0.03020 |

The interference is not zero, and the cursor $g_1 = 0.88803$ is less than 1. This is the bias: $g_\Delta = 1 - J/E_s$. The noise gain is $\|c\|^2 = 0.921$, against 1.332 for the ZF equalizer. The error splits into $E_s \|g - e_\Delta\|^2 + N_0 \|c\|^2 = 0.01985 + 0.09212 = 0.11197$. The 5-tap ZF equalizer with delay 0 has the error $0.03125^2 + 0.1 \times 1.33203 = 0.13418$. After the scaling by $1/g_\Delta$, the SINR is $E_s/J - 1 = 7.93$, or 8.99 dB. A long equalizer reaches $J_\infty = N_0 / \sqrt{(1.25 + N_0)^2 - 1} = 0.11026$; 15 taps already give 0.110264.

On the channel B of Proakis, $h = (0.407, 0.815, 0.407)$, with $N = 31$ and $N_0 = 0.01$ (20 dB), the best delay is 16 and $J = 0.1795$, an unbiased SINR of 6.60 dB. The best ZF equalizer of the same length has the error 26.7, because of its noise gain of 2641.

## Correctness

**Claim.** The taps of line L5 are the unique minimizer of $J$ over all $N$-tap filters, and line L6 is the minimum. The minimum is also $J = N_0 E_s [(E_s H^H H + N_0 I)^{-1}]_{\Delta\Delta}$, and the output satisfies $E[z[n] \mid x[n-\Delta]] = (1 - J/E_s)\, x[n-\Delta]$.

**Key step.** For any taps, $J(f) = f^H R f - 2\,\mathrm{Re}(f^H r) + E_s$. Completing the square gives $J(f) = E_s - r^H R^{-1} r + (f - R^{-1} r)^H R (f - R^{-1} r)$, and $R$ is positive definite because $H$ has full row rank. The closed form follows from the push-through identity $H^H (E_s H H^H + N_0 I)^{-1} = (E_s H^H H + N_0 I)^{-1} H^H$. The full proof, with the bias, the unbiased SINR and the limits in $N_0$, is in the proofs folder.

## Complexity

Line L2 costs $O(N^2 (N + L))$ operations, line L4 costs $O(N^3)$, and lines L3, L5 and L6 cost $O(N)$, once per channel and delay. $R$ is a Hermitian Toeplitz matrix, so a Levinson recursion, as in the [Levinson-Durbin recursion](/levinson-durbin-recursion/), solves it in $O(N^2)$. Filtering costs $N$ complex multiplications per symbol, so $K$ symbols cost $O(N^2 (N + L) + K N)$ in the [real RAM](/real-ram/), with $O(N (N + L))$ extra space for $H$ and $R$. To try every delay, one inverse of $E_s H^H H + N_0 I$ gives all $N + L - 1$ values of $J$ on its diagonal.

## Properties

- **Optimal among linear filters.** No other $N$-tap linear equalizer has a smaller mean squared error. It does not minimize the symbol error rate in general.
- **Orthogonality.** The error $z[n] - x[n-\Delta]$ is uncorrelated with every sample $y[n-i]$ in the filter.
- **Biased.** The output is $(1 - J/E_s)\, x[n-\Delta]$ plus an uncorrelated term of variance $J(1 - J/E_s)$. The unbiased SINR is $E_s/J - 1$, which is 1 less than the biased ratio $E_s/J$.
- **Between ZF and the matched filter.** As $N_0 \to 0$, the taps tend to the least squares ZF design, which minimizes $\|c * h - e_\Delta\|^2$. As $N_0 \to \infty$, they tend to $E_s \overline{H e_\Delta}/N_0$, a matched filter.
- **Infinite length.** As $N$ grows, $J$ tends to $\frac{1}{2\pi}\int_{-\pi}^{\pi} E_s N_0 / (E_s |H(e^{j\omega})|^2 + N_0)\, d\omega$. This stays finite even if $H$ has a spectral null, unlike the noise gain of the ZF equalizer.
- **Needs the noise level.** A wrong $N_0$ gives a filter between the MMSE and the ZF designs (too small) or too close to the matched filter (too large).

## Variants and improvements

- **Adaptive MMSE.** The [LMS algorithm](/lms-algorithm/) and the [RLS algorithm](/rls-algorithm/) converge to the same Wiener taps from a training sequence, without an estimate of $h$ or $N_0$; see [adaptive equalization](/adaptive-equalization/).
- **Fractionally spaced.** With 2 samples per symbol, the same solution with a longer regressor is insensitive to the sampling phase; see the [fractionally spaced equalizer](/fractionally-spaced-equalizer/).
- **MMSE decision feedback.** The [decision feedback equalizer](/decision-feedback-equalizer/) adds a feedback filter on past decisions. The MMSE-DFE is the best structure of this kind, and the [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/) links its unbiased SNR to capacity.
- **Frequency-domain MMSE.** With a cyclic prefix, the equalizer is one scalar $\bar H_k E_s / (E_s |H_k|^2 + N_0)$ per DFT bin; see [frequency-domain equalization](/frequency-domain-equalization/).
- **Soft MMSE.** In [turbo equalization](/turbo-equalization/), the same formula with symbol means and variances from a decoder gives the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/).

## When to use it

Use the MMSE linear equalizer when the channel and the noise level are known or estimated, and a linear filter is cheap enough. It is better than ZF at every SNR, and much better on channels with deep spectral nulls. For a channel with a null in its band, a DFE or a [Viterbi equalizer](/viterbi-equalizer/) does better again. For long channels in a block system, the frequency-domain form is cheaper.

## Pitfalls

- **Forgetting the bias.** For QAM with 16 or more points, slice $z[n] / (1 - J/E_s)$, not $z[n]$. Otherwise the outer points fall short of their decision regions. For PSK and BPSK the bias does not change the decisions.
- **The conjugate.** The Wiener solution is for $z = f^H u$. A filter written as $z[n] = \sum c_i y[n-i]$ uses $c = \bar f$. For a real channel the two agree, so a bug can hide until the first complex channel.
- **The wrong delay.** The error depends on $\Delta$ by a large factor: for $h = (1, 0.5)$ and $N = 5$, from 0.112 to 0.779. A delay near the middle of $N + L - 1$ is a safe start, and a search over all delays is cheap.
- **Treating $J$ as the noise variance.** The residual is not Gaussian, because part of it is ISI from a finite alphabet. The Gaussian formula with the unbiased SINR is an approximation; the tests compare the BER with an exact sum over the ISI patterns.
- **An estimated channel.** The design uses $\hat h$ and $\hat N_0$. Channel errors act like extra noise, so a slightly larger $N_0$ makes the equalizer more robust.

## Implementations

## History

Lucky's zero-forcing equalizers of 1965 minimized the peak distortion. In 1969, Gersho studied the mean-square error criterion for adaptive equalizers of highly dispersive channels; with it the optimal taps are the finite-length Wiener filter, and the LMS algorithm of Widrow and Hoff can find them. The mean-square error criterion takes the noise into account, and it replaced peak distortion in most later designs. Later work on the MMSE-DFE studied the bias and linked the unbiased SNR to capacity; see the [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/).

## References
