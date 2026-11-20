---
tag: 5PBE09
kind: algorithm
slug: lmmse-channel-estimation
name: LMMSE channel estimation
aliases:
- linear MMSE channel estimation
- MMSE channel estimator
area: communications/channel-estimation-and-equalization
level: core
summary: "Estimates the channel taps from pilots by the linear filter with the least mean squared error, h = (R_h X^H X + N0 I)^(-1) R_h X^H y, using the channel covariance and the noise level."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {m: the number of pilot observations, L: the number of channel taps}
  time: {worst: O(m L^2 + L^3)}
  space: {extra: O(L^2)}
properties: {deterministic: true, unbiased: false, needs_channel_statistics: true, optimal_among_linear_estimators: true, optimal_for_gaussian_channels: true}
history:
  year: 1941
  people: [Andrey Kolmogorov, Norbert Wiener]
  note: "Kolmogorov in 1941 and Wiener in a 1942 report, published in 1949, derived the linear estimator with the least mean squared error. LMMSE channel estimation is that estimator applied to the pilot model."
prereqs: [channel-estimation, least-squares-channel-estimation, wiener-filter]
see_also: [two-dimensional-wiener-pilot-interpolation, dft-based-channel-estimation, pilot-symbol-assisted-modulation, mmse-linear-equalizer, mmse-mimo-detector, kalman-channel-tracking, ridge-regression, cramer-rao-bound]
sources:
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 12 (linear Bayesian estimators and the orthogonality principle) and Chapter 15 (complex data and parameters)"
  - paper: doi:10.1109/TSP.2005.863008
    title: "M. Biguesh and A. B. Gershman, Training-based MIMO channel estimation: a study of estimator tradeoffs and optimal training signals, IEEE Transactions on Signal Processing 54(3), 2006, pages 884 to 893"
    locator: "the LMMSE estimator from training, its mean squared error against the LS estimator, and the training that minimizes it"
---

LMMSE channel estimation finds the taps of a channel from pilots with the linear filter that has the smallest mean squared error on average over the channels. It is the [least squares channel estimator](/least-squares-channel-estimation/) with prior knowledge added: the receiver knows the covariance $R_h = E[h h^H]$ of the taps and the noise level $N_0$. For the model $y = X h + w$, with the pilot matrix $X$ and noise $w \sim \mathcal{CN}(0, N_0 I)$, the estimate is $\hat h = R_h X^H (X R_h X^H + N_0 I)^{-1} y = (R_h X^H X + N_0 I)^{-1} R_h X^H y$. It is the [Wiener filter](/wiener-filter/) of the pilot model. Its error is never larger than that of LS, and the gain is largest at low SNR and when $R_h$ has a few strong directions. For Gaussian channels it is also the best estimator of any kind. The estimate is biased toward the prior mean, zero here. [Two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/) applies the same filter across the time and frequency grid of OFDM, [DFT-based channel estimation](/dft-based-channel-estimation/) is a cheaper estimator that uses only the channel length, and the [MMSE linear equalizer](/mmse-linear-equalizer/) uses the same formula to estimate the data symbols instead of the channel.

## In plain words

Least squares fits the taps to the received pilots and trusts the data alone. But the receiver often knows more: how strong each tap is on average, and how much noise there is. LMMSE uses this. When a tap is weak on average or the noise is strong, it trusts the data less and pulls that estimate toward zero. When a tap is strong and the noise is weak, it gives almost the least squares answer. The pull is chosen so that the average squared error is as small as any linear rule can make it. The price is that the receiver must know the statistics, and that each single estimate is a little too small on average.

## The problem

The input is a block of $N_p$ known pilots $x[0], \ldots, x[N_p - 1]$, the samples $y[0], \ldots, y[N_p - 1]$, the number of taps $L$, the $L \times L$ covariance $R_h$ of the taps, and $N_0$. The model is one sample per symbol, $y[k] = \sum_{l=0}^{L-1} h_l\, x[k-l] + w[k]$, with $w[k] \sim \mathcal{CN}(0, N_0)$ independent of each other and of $h$. As for LS, the algorithm uses the $m = N_p - L + 1$ samples $v = (y[L-1], \ldots, y[N_p-1])$, which depend on the pilots only, so $v = X h + w$ with $X_{il} = x[i + L - 1 - l]$. The taps have mean zero; for a nonzero mean see the variants. The output is an estimate $\hat h = W v$, where the $L \times m$ matrix $W$ minimizes the mean squared error $E\|W v - h\|^2$, averaged over the channel and the noise. The SNR is $E_s/N_0$, where $E_s$ is the average energy of a pilot.

## The algorithm

```pseudo id=main
LMMSE-CHANNEL-ESTIMATE(x, y, L, R_h, N0)
L1  X ← the m × L pilot matrix, X[i][l] = x[i + L - 1 - l]
L2  v ← (y[L - 1], .., y[N_p - 1])                   ▷ the samples that see pilots only
L3  G ← Xᴴ X ;  b ← Xᴴ v
L4  A ← R_h G + N0 I
L5  c ← R_h b
L6  return ĥ ← A⁻¹ c                                 ▷ an L × L solve
```

Lines L1 and L2 are the same as in the LS estimator. Line L3 forms the matrix and the vector of the normal equations. Lines L4 to L6 compute $(R_h G + N_0 I)^{-1} R_h X^H v$. This form solves an $L \times L$ system instead of inverting the $m \times m$ matrix $X R_h X^H + N_0 I$, and it does not need $R_h^{-1}$, so a tap known to be zero, with a zero row in $R_h$, is allowed and is estimated as exactly zero. $A$ is not Hermitian, so line L6 uses Gaussian elimination. If $X$, $R_h$ and $N_0$ do not change, the receiver computes $W = A^{-1} R_h X^H$ once, and each estimate is $\hat h = W v$.

## Example

Use the pilots of the LS example, $x = (1, 1, -1, 1, 1)$ with $L = 2$, so $G = X^T X = 4I$, and the same samples $v = (1.6, -0.7, 0.55, 1.6)$, which give $b = X^T v = (4.45, 1.95)$ and the LS estimate $(1.1125, 0.4875)$. Let the taps be independent with $R_h = \operatorname{diag}(0.8, 0.2)$, and let $N_0 = 0.5$, an SNR of 2, or 3 dB.

| step | value |
|---|---|
| L4: $A = R_h G + N_0 I$ | $\operatorname{diag}(3.7,\ 1.3)$ |
| L5: $c = R_h b$ | $(3.56,\ 0.39)$ |
| L6: $\hat h = A^{-1} c$ | $(0.96216,\ 0.3)$ |

Because $R_h$ and $G$ are diagonal, each tap is the LS value times a shrink factor $\sigma_l^2 \cdot 4 / (\sigma_l^2 \cdot 4 + N_0)$, with $\sigma_l^2$ the variance of tap $l$: $3.2/3.7 = 0.86486$ for the strong tap and $0.8/1.3 = 0.61538$ for the weak one. The error covariance $N_0 A^{-1} R_h$ is $\operatorname{diag}(0.10811, 0.07692)$, so the mean squared error is $0.18503$, against $N_0/2 = 0.25$ for LS. The table gives both errors for other noise levels.

| $N_0$ | SNR in dB | LS error $N_0/2$ | LMMSE error |
|---|---|---|---|
| 1 | 0 | 0.5 | 0.30159 |
| 0.5 | 3.01 | 0.25 | 0.18503 |
| 0.1 | 10 | 0.05 | 0.04646 |
| 0.01 | 20 | 0.005 | 0.00496 |

At high SNR the two are almost equal. With no data at all, the best guess is $\hat h = 0$, with error $\operatorname{tr}(R_h) = 1$.

## Correctness

**Claim.** Among all linear estimators $W v$, the matrix $W_\ast = R_h X^H (X R_h X^H + N_0 I)^{-1}$ gives the smallest mean squared error, and it is the only one that does. Lines L4 to L6 compute $W_\ast v$. The error covariance is $C_e = N_0 (R_h X^H X + N_0 I)^{-1} R_h$, and its trace is at most the LS error $N_0 \operatorname{tr}((X^H X)^{-1})$.

**Key step.** The orthogonality principle: the error $W_\ast v - h$ is uncorrelated with every sample of $v$. Any other $W = W_\ast + D$ then has the error $J(W_\ast) + \operatorname{tr}(D K D^H)$ with $K = X R_h X^H + N_0 I$ positive definite. The identity $(R_h G + N_0 I) R_h X^H = R_h X^H K$ moves between the two forms. LS is one of the linear estimators, so LMMSE is at least as good. For Gaussian $h$ and $w$, the error is independent of $v$, which makes $W_\ast v$ the conditional mean. The full proof is in the proofs folder.

## Complexity

Line L3 costs $m L^2 + m L$ complex multiplications, line L4 costs $L^3$, line L5 $L^2$, and the solve of line L6 $O(L^3)$. The total is $O(m L^2 + L^3)$ per pilot block in the [real RAM](/real-ram/), with $O(L^2)$ extra space. The other form, with the $m \times m$ inverse, costs $O(m^3)$, which is worse when there are many pilots. When $X$, $R_h$ and $N_0$ are fixed, $W$ is computed once and each estimate costs $m L$ multiplications, the same as LS. In OFDM with $N$ subcarriers, the full LMMSE matrix is $N \times N$, and a low-rank approximation keeps only the strong eigenvectors of the channel covariance.

## Properties

- **Least mean squared error among linear estimators.** No other linear function of the pilots does better on average over the channel distribution.
- **Optimal for Gaussian channels.** For Rayleigh fading taps and Gaussian noise, $\hat h = E[h \mid v]$, the best estimator of any kind.
- **Biased.** For a fixed channel, $E[\hat h \mid h] = W_\ast X h \ne h$ in general: the estimate is pulled toward zero. The error is small on average over the channels, not for each channel.
- **At least as good as LS.** $\operatorname{tr}(C_e) \le N_0 \operatorname{tr}((X^H X)^{-1})$. The gain is large at low SNR and for channels whose covariance has a few strong eigenvalues, and it vanishes as $N_0 \to 0$, where the estimate tends to LS.
- **Error covariance.** $C_e = (R_h^{-1} + X^H X / N_0)^{-1}$ when $R_h$ is invertible: the information from the prior adds to the information from the pilots.
- **Sensitive to the model.** A wrong $R_h$ or $N_0$ gives a larger error than the formula. In practice, a covariance for a longer delay spread than the true one loses less than a covariance for a shorter one, which suppresses real taps.

## Variants and improvements

- **Nonzero mean.** For a channel with a known mean $\bar h$, such as Rician fading, use $\hat h = \bar h + W_\ast (v - X \bar h)$.
- **Diagonal approximation.** With independent taps and orthogonal pilots, $X^H X = m E_s I$, and the estimate is the LS estimate times one shrink factor per tap, $\sigma_l^2 m E_s / (\sigma_l^2 m E_s + N_0)$, as in the example.
- **OFDM frequency and time interpolation.** [Two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/) estimates the channel at every subcarrier and symbol from the pilots of a grid, with the correlation from the delay spread and the Doppler spread. Separable filters, one in frequency and one in time, cut the cost.
- **Low-rank LMMSE.** Keep the $r$ largest eigenvalues of $R_h$ only. The cost per estimate falls from $O(N^2)$ to $O(N r)$ with little loss. The $N \times N$ frequency correlation of a channel with $L$ taps at multiples of the sample time has rank at most $L$, so $r = L$ loses nothing.
- **Tracking.** If the channel changes over time with a known model, the [Kalman filter](/kalman-filter/), as in [Kalman channel tracking](/kalman-channel-tracking/), gives the LMMSE estimate from all pilots so far, updated recursively.
- **Regularized LS.** If only $N_0$ and the tap power $\sigma^2$ are known, $R_h = \sigma^2 I$ gives $(X^H X + (N_0/\sigma^2) I)^{-1} X^H v$, which is [ridge regression](/ridge-regression/) with the parameter $N_0/\sigma^2$.

## When to use it

Use LMMSE when the receiver knows or can estimate the channel covariance and the noise level, and when the SNR is low or the pilots are few, so that LS is noisy. Typical cases are OFDM receivers with a known power delay profile, and pilot interpolation in time with a known Doppler spread. Use LS when the statistics are unknown or change fast, or at high SNR, where both give nearly the same error.

## Pitfalls

- **A wrong noise level.** If $N_0$ is too small, the estimate is close to LS and keeps its noise. If $N_0$ is too large, the estimate shrinks the taps too much and is biased. Measure $N_0$, for example from guard subcarriers or from the residual of the LS fit.
- **A covariance from the wrong channel.** $R_h$ comes from the power delay profile. A profile that is shorter than the true one sets the late taps to almost zero and loses their energy. When in doubt, use a profile that is too long, not too short.
- **The inverse of $R_h$.** The form $(R_h^{-1} + G/N_0)^{-1} G \hat h_{LS} / N_0$ fails for a singular $R_h$, which is common in OFDM, where the $N \times N$ covariance of a channel with $L < N$ taps has rank $L$. Lines L4 to L6 do not need the inverse.
- **The cost of the large form.** $R_h X^H (X R_h X^H + N_0 I)^{-1}$ inverts an $m \times m$ matrix. For many pilots, use the $L \times L$ form of lines L4 to L6.
- **Expecting an unbiased estimate.** For one channel, the LMMSE estimate is too small on average. A detector that uses it with the error covariance $C_e$ works as designed; one that treats it as exact loses a little.

## Implementations

## History

Andrey Kolmogorov in 1941, for discrete time, and Norbert Wiener in a classified report of 1942, published in 1949, derived the linear estimator of a stationary process with the least mean squared error. The matrix form for a finite set of observations, with the orthogonality principle, became standard in estimation theory. In wireless receivers, LMMSE channel estimation became common with OFDM in the 1990s, where the correlation of the channel across subcarriers is known from the delay spread. Biguesh and Gershman in 2006 compared the LS and LMMSE estimators for training-based MIMO systems and gave the training signals that minimize the error of each.

## References
