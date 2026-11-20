---
tag: JGTN3A
kind: algorithm
slug: least-squares-channel-estimation
name: Least squares channel estimation
aliases:
- LS channel estimator
area: communications/channel-estimation-and-equalization
level: intro
summary: "Estimates the taps of an FIR channel from known pilots as h = (X^H X)^(-1) X^H y. It needs no channel statistics, is unbiased, and its error is N0 tr((X^H X)^(-1))."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {m: the number of pilot observations, L: the number of channel taps}
  time: {worst: O(m L^2)}
  space: {extra: O(L^2)}
properties: {deterministic: true, unbiased: true, needs_channel_statistics: false, efficient_in_gaussian_noise: true}
history:
  year: 1805
  people: [Adrien-Marie Legendre, Carl Friedrich Gauss]
  note: "Legendre published the method of least squares in 1805 and Gauss gave it a probabilistic basis in 1809. Training-based channel estimation applies it to the matrix of known pilot symbols."
prereqs: [channel-estimation, least-squares-problem]
see_also: [lmmse-channel-estimation, pilot-symbol-assisted-modulation, sparse-channel-estimation, comb-pilot-channel-estimation, pseudoinverse, cramer-rao-bound, cholesky-decomposition, zero-forcing-equalizer]
sources:
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 4 (the linear model and its efficient estimator), Chapter 8 (least squares) and Chapter 15 (complex data and parameters)"
  - paper: doi:10.1109/TSP.2005.863008
    title: "M. Biguesh and A. B. Gershman, Training-based MIMO channel estimation: a study of estimator tradeoffs and optimal training signals, IEEE Transactions on Signal Processing 54(3), 2006, pages 884 to 893"
    locator: "the LS estimator, its mean squared error, and the result that orthogonal training minimizes that error for a fixed training energy"
---

Least squares (LS) channel estimation finds the taps of a channel from pilots, symbols that the receiver knows in advance. The channel is an FIR filter $h = (h_0, \ldots, h_{L-1})$, and the received samples are $y = X h + w$, where the matrix $X$ holds the pilots and $w \sim \mathcal{CN}(0, N_0 I)$ is the noise. The LS estimate $\hat h = (X^H X)^{-1} X^H y$ is the tap vector that makes $\|y - X h\|^2$ smallest; it is the [least squares problem](/least-squares-problem/) solved with the [pseudoinverse](/pseudoinverse/) of $X$. It uses no knowledge of the channel statistics. It is unbiased, its mean squared error is $N_0 \operatorname{tr}((X^H X)^{-1})$, and in Gaussian noise this error is equal to the [Cramer-Rao bound](/cramer-rao-bound/). [LMMSE channel estimation](/lmmse-channel-estimation/) adds the channel covariance and the noise level and gets a smaller error, mostly at low SNR. [Pilot symbol assisted modulation](/pilot-symbol-assisted-modulation/) decides where the pilots go in time, [sparse channel estimation](/sparse-channel-estimation/) uses fewer pilots when only a few taps are not zero, and [comb-pilot channel estimation](/comb-pilot-channel-estimation/) is the OFDM form, where LS becomes one division per pilot subcarrier.

## In plain words

The transmitter sends a short block of symbols that the receiver already knows. The channel smears each symbol over the next few samples, as an echo does. So each received sample is a sum of a few known symbols, each multiplied by an unknown channel tap, plus noise. There are more samples than taps. The receiver then picks the taps that explain the samples best: the taps for which the sum of the squared differences between the samples and the samples they predict is smallest. This is the same fit as a straight line through noisy points. The receiver needs nothing more than the pilots. The estimate is correct on average, and it is better when the pilots have more energy and when they excite all the taps equally.

## The problem

The input is a block of $N_p$ known pilots $x[0], \ldots, x[N_p - 1]$, the $N_p$ samples $y[0], \ldots, y[N_p - 1]$ that the receiver gets while they arrive, and the number of taps $L$. The model is one sample per symbol, after the matched filter:

$$y[k] = \sum_{l=0}^{L-1} h_l\, x[k - l] + w[k],$$

with complex taps $h_l$ and noise $w[k] \sim \mathcal{CN}(0, N_0)$, independent from sample to sample, so that $E|w[k]|^2 = N_0$. The first $L - 1$ samples also hold symbols sent before the pilots, which the receiver does not know. So the algorithm uses only the $m = N_p - L + 1$ samples $y[L-1], \ldots, y[N_p - 1]$. In matrix form they are $v = X h + w$, where $X$ is the $m \times L$ matrix with $X_{il} = x[i + L - 1 - l]$, constant along each diagonal. The output is an estimate $\hat h$ of the $L$ taps. LS asks for the $\hat h$ that minimizes $\|v - X \hat h\|^2$. This needs $X$ to have full column rank, and so $m \ge L$, that is $N_p \ge 2L - 1$.

## The algorithm

```pseudo id=main
LS-CHANNEL-ESTIMATE(x, y, L)
L1  m ← N_p - L + 1                                  ▷ N_p pilots in x
L2  X[i][l] ← x[i + L - 1 - l]  for 0 ≤ i < m, 0 ≤ l < L
L3  v ← (y[L - 1], .., y[N_p - 1])                   ▷ the samples that see pilots only
L4  G ← Xᴴ X                                         ▷ L × L, Hermitian
L5  b ← Xᴴ v
L6  return ĥ ← G⁻¹ b                                 ▷ by Cholesky, G = C Cᴴ
```

Lines L1 and L2 build the pilot matrix. Each row is a window of $L$ pilots, newest first, so row $i$ times $h$ is the noiseless sample $y[i + L - 1]$. Line L3 drops the first $L - 1$ samples, which also depend on unknown symbols sent before the pilots. Lines L4 and L5 form the normal equations $G \hat h = b$, and line L6 solves them. $G$ is Hermitian and positive definite when $X$ has full column rank, so the [Cholesky decomposition](/cholesky-decomposition/) applies; it costs half as much as a general solver and fails exactly when the pilots do not excite every tap. For a fixed pilot block, the receiver computes $P = G^{-1} X^H$ once, and each later estimate is the product $\hat h = P v$.

## Example

Take $L = 2$ and the pilots $x = (1, 1, -1, 1, 1)$, so $N_p = 5$ and $m = 4$. Line L2 gives the rows $(x[1], x[0]) = (1, 1)$, $(-1, 1)$, $(1, -1)$ and $(1, 1)$. Then $X^T X = 4 I$: the two columns are orthogonal and have the same energy. The channel is $h = (1, 0.5)$, so the noiseless samples of line L3 are $X h = (1.5, -0.5, 0.5, 1.5)$.

Let the noise on these four samples be $(0.1, -0.2, 0.05, 0.1)$, so $v = (1.6, -0.7, 0.55, 1.6)$.

| step | value |
|---|---|
| L4: $G = X^T X$ | $4 I$ |
| L5: $b = X^T v$ | $(1.6 + 0.7 + 0.55 + 1.6,\ 1.6 - 0.7 - 0.55 + 1.6) = (4.45,\ 1.95)$ |
| L6: $\hat h = G^{-1} b$ | $(1.1125,\ 0.4875)$ |

The error is $(0.1125, -0.0125)$. Because $G = 4I$, each tap estimate is the true tap plus the average of four noise samples with signs, so its variance is $N_0/4$, and the mean squared error is $N_0 \operatorname{tr}(G^{-1}) = N_0/2$. With no noise, line L6 returns $(1, 0.5)$ exactly.

## Correctness

**Claim.** If $X$ has full column rank, line L6 returns the unique minimizer of $\|v - X g\|^2$. Under the model, $E[\hat h] = h$ and the error covariance is $N_0 (X^H X)^{-1}$. For pilots of a fixed total energy $T = \operatorname{tr}(X^H X)$, the mean squared error is at least $L^2 N_0 / T$, with equality if and only if $X^H X = (T/L) I$.

**Key step.** The residual $r = v - X \hat h$ is orthogonal to every column of $X$, since $X^H r = b - G \hat h = 0$. So for any other $g = \hat h + d$, $\|v - X g\|^2 = \|r\|^2 + \|X d\|^2$, and the second term is positive unless $d = 0$. The error is $\hat h - h = G^{-1} X^H w$, a linear function of zero-mean noise, which gives the bias and the covariance. The bound on the trace follows from the Cauchy-Schwarz inequality on the eigenvalues of $G$. The full proof is in the proofs folder.

## Complexity

Lines L2 and L3 copy $O(m L)$ numbers. Line L4 costs $m L^2$ complex multiplications, or about half of that with the Hermitian symmetry, line L5 costs $m L$, and the Cholesky solve of line L6 costs $O(L^3)$. Since $m \ge L$, the total is $O(m L^2)$ per pilot block in the [real RAM](/real-ram/), with $O(L^2)$ extra space for $G$. When the pilots are the same in every block, $P = (X^H X)^{-1} X^H$ is computed once, and each estimate costs $m L$ complex multiplications. With orthogonal pilots, $G$ is a multiple of $I$, and $\hat h$ is $X^H v$ times a constant.

## Properties

- **Unbiased, with no prior.** $E[\hat h] = h$ for every channel. The estimator needs neither $N_0$ nor the channel statistics, so it works when these are unknown or change.
- **Efficient in Gaussian noise.** In the linear Gaussian model, $N_0 (X^H X)^{-1}$ is equal to the Cramer-Rao bound. No unbiased estimator has a smaller error. A biased estimator with a prior on $h$, such as LMMSE, can do better.
- **Error and pilot energy.** The mean squared error $N_0 \operatorname{tr}((X^H X)^{-1})$ falls in proportion to $1/(\text{pilot energy})$ and grows with $L$. For orthogonal pilots it is $L^2 N_0 / T$, or $L N_0 / (m E_p)$ when each pilot has energy $E_p$.
- **Orthogonal training is best.** Among pilot blocks of the same energy, those with $X^H X$ a multiple of $I$ give the smallest error. A block of $m$ symbols with zero periodic autocorrelation at every lag other than 0, such as a Zadoff-Chu sequence, has this property when its last $L - 1$ symbols are also sent first, as a cyclic prefix. The example above is the block $(1, -1, 1, 1)$ with the prefix $1$.
- **Error grows with the number of taps.** Each extra tap adds about $N_0 / (m E_p)$ to the error. An $L$ chosen too large adds noise; an $L$ chosen too small leaves a model error. Sparse channel estimation tries to estimate only the taps that are not zero.
- **Linear and exact.** The estimate is a fixed linear function of $v$, and with no noise it is the true $h$.

## Variants and improvements

- **Weighted LS.** For colored noise with covariance $C$, use $\hat h = (X^H C^{-1} X)^{-1} X^H C^{-1} v$, the best linear unbiased estimator.
- **LMMSE estimation.** With the channel covariance $R_h$ and $N_0$ known, [LMMSE channel estimation](/lmmse-channel-estimation/) shrinks the LS estimate toward the prior mean and gets a smaller mean squared error.
- **OFDM and the cyclic prefix.** With a cyclic prefix, $X$ is circulant and the DFT makes it diagonal. LS then becomes one complex division per pilot subcarrier, $\hat H_k = Y_k / X_k$; see [comb-pilot channel estimation](/comb-pilot-channel-estimation/). [DFT-based channel estimation](/dft-based-channel-estimation/) then removes the noise outside the first $L$ taps.
- **MIMO training.** For $n_t$ transmit antennas, $X$ has $n_t L$ columns and each antenna needs its own pilots. Orthogonal pilots across the antennas are again best. In multicell systems, reused pilots cause [pilot contamination](/pilot-contamination/).
- **Recursive LS.** When pilots or decisions arrive one by one, the [RLS algorithm](/rls-algorithm/) updates the same solution in $O(L^2)$ per sample, with a forgetting factor that tracks a slowly changing channel.
- **Sparse estimation.** When most taps are zero, [sparse channel estimation](/sparse-channel-estimation/) fits only a few taps and needs fewer pilots than $2L - 1$.

## When to use it

Use LS when the receiver has a block of known pilots and does not know the channel statistics or the noise level, or when these change too fast to estimate. It is the first estimator to try and the reference for the others. At high SNR it is close to LMMSE. At low SNR, or with many taps and few pilots, use LMMSE if the channel covariance is known, and a sparse estimator if the channel has few strong paths.

## Pitfalls

- **Too few pilots.** With $N_p < 2L - 1$, or with pilots that do not excite every tap (for example all pilots equal, which makes the columns of $X$ the same), $X^H X$ is singular. Line L6 must detect this and not return a result.
- **Using the first samples.** The samples $y[0], \ldots, y[L-2]$ also depend on the unknown data before the pilots. Putting them in line L3 with zeros for the unknown symbols adds a bias.
- **Solving the normal equations in bad cases.** The condition number of $X^H X$ is the square of that of $X$. For badly conditioned pilots, a QR decomposition of $X$ is more accurate than lines L4 to L6. With good pilots, $X^H X$ is close to a multiple of $I$, and this does not matter.
- **Too many taps.** Each tap that the channel does not have still adds noise to the estimate. Choose $L$ from the delay spread, not larger.
- **Conjugates.** In complex arithmetic the normal equations need $X^H$, not $X^T$. With $X^T$, the estimate is wrong for every complex pilot.

## Implementations

## History

Adrien-Marie Legendre published the method of least squares in 1805, and Carl Friedrich Gauss published his account, with a probabilistic justification, in 1809. In digital communications, receivers used known training symbols from the start of adaptive equalization in the 1960s, and LS gave the estimate of the channel from such a block in one step instead of by slow adaptation. GSM, for example, places a training sequence of 26 bits in the middle of each normal burst. The theory of the estimator itself, with its error and its optimal pilots, belongs to the linear model of estimation theory, as in the book by Kay. Biguesh and Gershman in 2006 compared the LS and LMMSE estimators for MIMO training and showed that orthogonal training minimizes the LS error.

## References
