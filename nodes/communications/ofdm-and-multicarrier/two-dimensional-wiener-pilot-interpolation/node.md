---
tag: G9C3T4
kind: algorithm
slug: two-dimensional-wiener-pilot-interpolation
name: Two-dimensional Wiener pilot interpolation
aliases:
- "2D Wiener channel interpolation"
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Interpolates OFDM pilot estimates over time and frequency with the Wiener filter of the channel correlation. It gives the least mean squared error of all linear estimates from the chosen pilots."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {T: the number of target positions, M: the number of pilots, K: the number of pilots used per target}
  time: {worst: O(T (M log M + K^3))}
  space: {extra: O(K^2 + M)}
properties: {deterministic: true, linear_mmse: true, needs_channel_statistics: true, weights_independent_of_data: true}
history:
  year: 1997
  people: [Peter Hoeher, Stefan Kaiser, Patrick Robertson]
  note: "Hoeher, Kaiser and Robertson applied two-dimensional Wiener filtering to OFDM channel estimation from pilots spread over time and frequency, at ICASSP 1997."
prereqs: [orthogonal-frequency-division-multiplexing, comb-pilot-channel-estimation, lmmse-channel-estimation, wiener-filter]
see_also: [dft-based-channel-estimation, pilot-symbol-assisted-modulation, kriging, coherence-time, coherence-bandwidth, doppler-spread, clarke-model, cholesky-decomposition]
sources:
  - paper: doi:10.1109/ICASSP.1997.598897
    title: "P. Hoeher, S. Kaiser and P. Robertson, Two-dimensional pilot-symbol-aided channel estimation by Wiener filtering, IEEE ICASSP, 1997"
    locator: "volume 3, pages 1845 to 1848 (the pilot grid in time and frequency, the two-dimensional Wiener filter and its mean squared error)"
  - paper: doi:10.1109/26.701321
    title: "O. Edfors, M. Sandell, J.-J. van de Beek, S. K. Wilson and P. O. Börjesson, OFDM channel estimation by singular value decomposition, IEEE Transactions on Communications 46(7), 1998"
    locator: "pages 931 to 939 (the LMMSE channel estimator in frequency and its low-rank approximations)"
  - paper: doi:10.1109/TBC.2002.804034
    title: "S. Coleri, M. Ergen, A. Puri and A. Bahai, Channel estimation techniques based on pilot arrangement in OFDM systems, IEEE Transactions on Broadcasting 48(3), 2002"
    locator: "pages 223 to 229 (pilot arrangements and simpler interpolators, for comparison)"
---

Two-dimensional Wiener pilot interpolation estimates the channel $H(n, k)$ of an [OFDM](/orthogonal-frequency-division-multiplexing/) system on every OFDM symbol $n$ and subcarrier $k$ from noisy estimates at a sparse grid of pilot positions, using the statistics of the channel. The channel changes slowly along frequency, because the delays are short, and slowly along time, because the Doppler shifts are small, so neighboring positions are strongly correlated. The receiver models this by the correlation $r(\Delta n, \Delta k)$, and for each target position it computes the weights of the [Wiener filter](/wiener-filter/), $w = (R + \sigma^2 I)^{-1} c$, from the correlations between the pilots, $R$, and between the pilots and the target, $c$. The estimate is $\hat H(t) = \sum_i w_i^* y_i$, the linear estimate with the least mean squared error, $r(0,0) - c^H (R + \sigma^2 I)^{-1} c$. It extends [LMMSE channel estimation](/lmmse-channel-estimation/) from one OFDM symbol to the time-frequency grid, and it is the optimal counterpart of the simple [comb pilot interpolation](/comb-pilot-channel-estimation/). Each target uses only its $K$ nearest pilots, so the matrices stay small, and the weights depend on the pilot layout and the statistics, not on the data. The page uses $j$ for the imaginary unit.

## In plain words

The receiver knows the channel roughly at a few spots of a grid of time and frequency, the pilots. It wants the channel everywhere else. It also knows, from the physics of the channel, how much the channel at one spot tells about the channel at another: spots close in frequency and close in time are almost the same, spots far apart are nearly unrelated. For each spot it wants, it mixes the nearby pilot values with weights. The Wiener weights are the mix that is wrong by the least on average. They give more weight to the pilots that are most related to the spot, they account for the pilots repeating each other's information, and they shrink toward zero when the pilots are noisy.

## The problem

The input is the pilot positions $p_1, \ldots, p_M$ on the grid of symbols and subcarriers, their noisy values $y_i = H(p_i) + e_i$, for example least squares estimates $Y/X$ with $\sigma^2 = N_0 / |X_p|^2$, the correlation function $r(\Delta n, \Delta k) = E[H(n + \Delta n, k + \Delta k)\, H(n, k)^*]$ of the channel, the noise variance $\sigma^2$, the target positions, and the number $K$ of pilots per target. The channel is a zero-mean, wide-sense stationary field, and the errors are independent with variance $\sigma^2$. Output the linear estimate of $H(t)$ with the least mean squared error from the $K$ pilots nearest to each target $t$.

## The algorithm

```pseudo id=main
WIENER-2D(targets, p_1..p_M, y, r, σ², K)
L1  for each target t: S ← the K pilots nearest to t
L2      R[i][j] ← r(p_i - p_j)  for i, j in S
L3      R[i][i] ← R[i][i] + σ²
L4      c[i] ← r(p_i - t)  for i in S
L5      w ← the solution of R w = c
L6      Ĥ(t) ← Σ_{i in S} conj(w_i) y_i
```

Line L1 picks the nearest pilots, by Euclidean distance on the grid in the implementation. Lines L2 and L3 build the covariance of the pilot values, where the noise adds $\sigma^2$ on the diagonal. Line L4 builds the correlation of the pilot values with the unknown target. Line L5 solves the normal equations; the matrix is Hermitian positive definite, so a Cholesky solve works. Line L6 applies the weights. Lines L2 to L5 do not use the received values, so a receiver with a fixed pilot layout and fixed statistics computes the weights once and stores them.

## Example

The tests use $N = 16$ subcarriers and 9 symbols. The channel has three taps at delays 0, 1, 2 with powers $0.5$, $0.3$, $0.2$, and each tap changes in time as a first-order autoregressive process with coefficient $0.9$, so $r(\Delta n, \Delta k) = 0.9^{|\Delta n|} \sum_l P_l e^{-j 2\pi l \Delta k / N}$. Pilots are on symbols 0, 4, 8 and subcarriers $0, 3, \ldots, 15$, 18 in all, with $\sigma^2 = 0.05$. Take the target $t = (2, 1)$ and its four corner pilots $(0, 0)$, $(0, 3)$, $(4, 0)$, $(4, 3)$.

| pilot | $(0, 0)$ | $(0, 3)$ | $(4, 0)$ | $(4, 3)$ | MSE |
|---|---|---|---|---|---|
| Wiener weight $w_i$ | $0.323 + 0.119j$ | $0.142 - 0.119j$ | $0.323 + 0.119j$ | $0.142 - 0.119j$ | 0.2276 |
| bilinear weight | 0.333 | 0.167 | 0.333 | 0.167 | 0.2715 |

The Wiener weights are complex: the mean delay of the channel makes $H$ turn along frequency, and the weights follow that turn, which bilinear interpolation cannot do. The two symbols get equal weight because the target is halfway between them. With more pilots for the same target, the error falls: $0.432$ for $K = 1$, $0.301$ for $K = 2$, $0.228$ for $K = 4$, $0.2235$ for $K = 6$, $0.2233$ for $K = 9$ and $0.218$ for all 18. Averaged over all 144 positions of the grid, the closed-form error is $0.1439$ for $K = 4$, $0.1422$ for $K = 6$, $0.1386$ for $K = 9$ and $0.1330$ for $K = 18$; the tests check the prediction against a simulation of 300 channels within 10 percent.

## Correctness

**Claim.** For any weights $b$, the mean squared error of $\sum_i b_i^* y_i$ is $r_0 - 2 \operatorname{Re}(b^H c) + b^H (R + \sigma^2 I) b$. With $\sigma^2 > 0$, it has the unique minimum $r_0 - c^H (R + \sigma^2 I)^{-1} c$ at the weights of line L5. So line L6 returns the linear estimate with the least mean squared error from the pilots of line L1. More pilots never increase the error. This is a theorem for any wide-sense stationary channel with independent pilot errors; for jointly Gaussian channels and noise, the estimate is also the best of all estimates, linear or not.

**Key invariant.** With $Q = R + \sigma^2 I$ and $w = Q^{-1} c$, the error of any weights is the Wiener error plus $(b - w)^H Q (b - w)$, a nonnegative quadratic form.

The tests check this by brute force: random changes of the weights and bilinear weights never do better than the Wiener weights on the same pilots. The full proof is below.

## Complexity

For each of the $T$ targets, line L1 sorts the $M$ pilots by distance, $O(M \log M)$, lines L2 to L4 cost $O(K^2)$, and the solve of line L5 costs $O(K^3)$. The total is $O(T (M \log M + K^3))$ time and $O(K^2 + M)$ extra space in the [real RAM](/real-ram/). With a regular pilot grid, the targets fall into a few classes with the same relative layout, so a receiver computes $O(K^3)$ work once per class, and the cost per target is then $O(K)$ for line L6.

## Properties

- **Optimal among linear estimates.** For the chosen pilots, no other weights give a smaller mean squared error, by the claim.
- **Needs statistics.** The receiver must know or estimate $r(\Delta n, \Delta k)$, which depends on the delay profile and the Doppler spectrum, and $\sigma^2$. Wrong statistics raise the error by $(\tilde w - w)^H Q (\tilde w - w)$.
- **Shrinks with noise.** When $\sigma^2$ is large, the weights shrink toward zero and the estimate toward the mean 0, which lowers the error compared with an unbiased interpolator.
- **Diminishing returns.** The error falls fast for the first few pilots and slowly after, as in the example, so $K$ between 4 and 10 is common.
- **Sampling limit.** The pilot grid must sample the channel finely enough: the spacing in symbols must be small against the inverse of the Doppler spread, and the spacing in subcarriers small against $N$ divided by the delay spread in samples. A coarser grid cannot be repaired by any filter.

## Variants and improvements

- **Two cascaded filters.** A one-dimensional Wiener filter along time on the pilot subcarriers, followed by one along frequency, costs much less than the full two-dimensional filter and loses little, because the correlation of many channels factors into a part in time and a part in frequency.
- **Robust design.** When the statistics are unknown, the receiver can design the filter for a uniform delay profile over the prefix length and a uniform Doppler spectrum up to the largest expected Doppler shift, which covers the worst case at a small loss.
- **Low rank.** The eigenvectors of $R$ with the largest eigenvalues hold most of the channel energy; keeping only those reduces the cost, as in the low-rank LMMSE estimators of Edfors and coauthors.
- **Frequency only.** With pilots in every symbol, a one-dimensional filter along frequency is the [LMMSE estimate](/lmmse-channel-estimation/) for one symbol.
- **Kriging.** The same weights appear in geostatistics as [kriging](/kriging/), which interpolates a spatial field from scattered samples with its covariance.

## When to use it

Use it when the pilots are scattered over time and frequency, as in DVB-T and LTE, the channel statistics are known or can be estimated, and the receiver needs the best channel estimate for coherent detection at a low SNR. Use [DFT-based channel estimation](/dft-based-channel-estimation/) when only the channel length is known, and plain [comb pilot interpolation](/comb-pilot-channel-estimation/) when the cost must be minimal.

## Pitfalls

- **Conjugating the wrong side.** With $w = Q^{-1} c$ and $c[i] = r(p_i - t)$, line L6 must use $\sum_i \operatorname{conj}(w_i) y_i$. Using $\sum_i w_i y_i$ turns the phase the wrong way whenever the weights are complex, as in the example.
- **Reversing the correlation.** Line L4 must use $r(p_i - t)$, the pilot minus the target, consistent with line L2. With $r(t - p_i)$ the vector is conjugated, and the weights follow the turn of the channel in the wrong direction.
- **Leaving out the noise.** Line L3 must add $\sigma^2$ to the diagonal. Without it the filter trusts noisy pilots fully, and the solve of line L5 can be badly conditioned.
- **Statistics that are too narrow.** If the assumed delay or Doppler spread in lines L2 and L4 is smaller than the true one, the filter smooths away real changes of the channel. Designing for a slightly wider spread is safer than for a narrower one.
- **A pilot grid that aliases.** Line L1 can only use the pilots that exist. If the grid is too sparse for the Doppler or the delay spread, the error stays high for every $K$.

## Implementations

## History

Wiener filtering for pilot-symbol-assisted channel estimation was first used for single-carrier systems, where the pilots are spread in time only. Peter Hoeher, Stefan Kaiser and Patrick Robertson, at the German Aerospace Center, applied it in two dimensions to OFDM in 1997, with pilots spread over time and frequency and a filter that uses both correlations. Edfors and coauthors gave low-rank versions of the LMMSE estimator, and later standards such as DVB-T and LTE adopted scattered pilot grids that suit this kind of interpolation.

## References
