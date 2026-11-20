---
tag: JMK6AT
kind: algorithm
slug: kalman-channel-tracking
name: Kalman channel tracking
aliases:
- Gauss-Markov channel tracking
area: communications/channel-estimation-and-equalization
level: core
summary: "Tracks the taps of a time-varying channel with a Kalman filter, using the first-order autoregressive model h_k = a h_(k-1) + v_k with a = J0(2 pi f_D T) and known or decided symbols."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {L: the number of channel taps, K: the number of symbols}
  time: {worst: O(K L^2)}
  space: {extra: O(L^2)}
properties: {deterministic: true, online: true, needs_noise_level: true, needs_doppler: true, exact_for_gauss_markov_model: true}
history:
  year: 1960
  people: [Rudolf E. Kalman]
  note: "Kalman published the recursive linear filter for state-space models in 1960. Its use for fading channels rests on a Gauss-Markov model of the taps; Baddour and Beaulieu (2005) studied autoregressive fits of the Clarke correlation, and Komninakis, Fragouli, Sayed and Wesel (2002) tracked MIMO fading channels this way."
prereqs: [kalman-filter, autoregressive-model, channel-estimation]
see_also: [adaptive-equalization, clarke-model, lmmse-channel-estimation, pilot-symbol-assisted-modulation, rls-algorithm, per-survivor-processing, rauch-tung-striebel-smoother, extended-kalman-filter]
sources:
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Transactions of the ASME, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: "the recursive filter for a linear state-space model"
  - paper: doi:10.1109/TWC.2005.850327
    title: "Kareem E. Baddour and Norman C. Beaulieu, Autoregressive modeling for fading channel simulation, IEEE Transactions on Wireless Communications 4(4), 2005, pages 1650 to 1662"
    locator: "autoregressive models of a Rayleigh fading process fitted to the Clarke autocorrelation by the Yule-Walker equations"
  - paper: "Christos Komninakis, Christina Fragouli, Ali H. Sayed and Richard D. Wesel, Multi-input multi-output fading channel tracking and equalization using Kalman estimation, IEEE Transactions on Signal Processing 50(5), 2002, pages 1065 to 1076"
    locator: "a Kalman tracker of a MIMO fading channel with an autoregressive model, driven by decisions"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 13 (Kalman filters)"
---

Kalman channel tracking estimates the taps of a channel that changes from symbol to symbol, such as a mobile radio channel with a Doppler spread. It models each tap as a first-order [autoregressive process](/autoregressive-model/), $h_k = a\, h_{k-1} + v_k$, and runs a [Kalman filter](/kalman-filter/) on that model. The observations are the received samples, and the regressors are known symbols: pilots, a training sequence, or decisions. For a Clarke channel with maximum Doppler shift $f_D$ and symbol time $T$, the lag-1 fit is $a = J_0(2\pi f_D T)$. The page differs from [adaptive equalization](/adaptive-equalization/): there, an LMS or RLS filter adapts the equalizer taps with a fixed step and no model of the channel motion. Here, the filter estimates the channel itself, and the model of the motion sets the gain at each step. The cost is $O(L^2)$ per symbol for $L$ taps.

## In plain words

A mobile radio channel changes while the data passes. The receiver must follow it to undo it. Each new received sample gives a noisy look at the current channel. If the channel changes slowly, the receiver should average many looks. If it changes fast, old looks are stale and should count less. The Kalman filter makes this choice in the best way. It keeps an estimate and a measure of how wrong the estimate can be. Before each sample, it lets the estimate fade a little toward zero and adds uncertainty, as the model says. Then it moves the estimate toward the new sample by an amount set by the two uncertainties. The speed of the channel sets how much uncertainty to add each step.

## The problem

The channel has $L$ taps $h_k = (h_k[0], \ldots, h_k[L-1])^T$ at symbol time $k$. The receiver sees
$$y[k] = \sum_{l=0}^{L-1} h_k[l]\, x[k-l] + w[k] = c_k h_k + w[k],$$
with the row $c_k = (x[k], x[k-1], \ldots, x[k-L+1])$ of symbols and $w[k] \sim \mathcal{CN}(0, N_0)$. The receiver knows the symbols, either as pilots or as decisions, and symbols before time 0 are 0. The state model is
$$h_k = a\, h_{k-1} + v_k, \qquad v_k \sim \mathcal{CN}(0, Q), \qquad Q = (1 - a^2)\, \mathrm{diag}(P_0, \ldots, P_{L-1}),$$
with $0 \le a \le 1$. This $Q$ keeps every tap stationary with $E|h_k[l]|^2 = P_l$, the power of tap $l$ in the [tapped delay line model](/tapped-delay-line-channel-model/). The output is, for each $k$, the estimate $\hat h_k$ of $h_k$ from $y[0], \ldots, y[k]$ and its error covariance $\Sigma_k$.

**Choosing a.** The taps of a [Clarke channel](/clarke-model/) have the autocorrelation $E[h_k \bar h_{k-m}] = P\, J_0(2\pi f_D T m)$. The Yule-Walker equation of order 1 matches lag 1 of this: $a = J_0(2\pi f_D T)$. The model is a fit, not the Clarke process. It keeps the correlation at lag 1 and replaces the rest by $a^m$.

## The algorithm

```pseudo id=main
KALMAN-CHANNEL-TRACK(y, x, a, P, N0)
L1  ĥ ← 0;  Σ ← diag(P)                      ▷ the prior of the taps
L2  for k ← 0 to K - 1 do
L3      ĥ ← a ĥ;  Σ ← a² Σ + Q                 ▷ predict, Q = (1 - a²) diag(P)
L4      c ← (x[k], x[k-1], ..., x[k-L+1])     ▷ known or decided symbols
L5      s ← c Σ cᴴ + N0                         ▷ the variance of the innovation
L6      g ← Σ cᴴ / s                            ▷ the Kalman gain, a column
L7      ĥ ← ĥ + g (y[k] - c ĥ)                  ▷ update with the innovation
L8      Σ ← Σ - g c Σ
L9      output ĥ, Σ
```

Line L1 starts from the stationary law of the taps. Line L3 is the prediction. It moves the estimate toward 0 by the factor $a$ and adds the variance $Q$ of the new random part. At $k = 0$ it gives back $\mathrm{diag}(P)$, because $a^2 P + (1 - a^2) P = P$. Line L4 builds the regressor. In training or pilot mode it holds known symbols. In decision-directed mode it holds the decisions of an equalizer. Line L5 is the predicted variance of $y[k]$, which is a real number. Line L6 is the gain: the covariance of the tap error with the innovation, divided by the variance of the innovation. Line L7 corrects the prediction with the innovation $y[k] - c\,\hat h$, and line L8 removes the part of the uncertainty that $y[k]$ explains. The filter needs $a$, $P$ and $N_0$. It does not need a step size.

## Example

Take one tap, $L = 1$, with $P_0 = 1$, pilots of modulus 1, $N_0 = 0.1$ (an SNR of 10 dB) and $f_D T = 0.01$. Then $a = J_0(0.0628) = 0.999013$ and $Q = 1 - a^2 = 0.001972$. The variances do not depend on the received samples:

| $k$ | 0 | 1 | 2 | 3 | 9 | 49 and later |
|---|---|---|---|---|---|---|
| predicted $\Sigma$ (line L3) | 1 | 0.092702 | 0.049984 | 0.035233 | 0.017330 | 0.014960 |
| gain $g$ (line L6) | 0.909091 | 0.481065 | 0.333262 | 0.260535 | 0.147702 | 0.130133 |
| error $\Sigma$ (line L8) | 0.090909 | 0.048106 | 0.033326 | 0.026054 | 0.014770 | 0.013013 |

The first pilot gives the error $N_0/(1 + N_0) = 0.0909$. After about 50 pilots, the filter is in steady state. The steady predicted variance solves $\Sigma^- = Q(1 - N_0)/2 + \sqrt{Q^2 (1 - N_0)^2/4 + Q N_0}$, which is $0.014960$, and the error is $\Sigma^- N_0 / (\Sigma^- + N_0) = 0.013013$. This is 7.7 times smaller than the error $N_0 = 0.1$ of one pilot alone. The gain $0.130$ means that the filter averages about the last 8 pilots: older pilots are stale.

The tests also measure a case with two taps of powers 0.6 and 0.4, QPSK training, $N_0 = 0.05$ and a faster channel, $f_D T = 0.02$ (seed 4, 600 symbols). The average of $\|h_k - \hat h_k\|^2$ over the symbols 300 to 599 is 0.0233 with $a = J_0(2\pi \cdot 0.02)$. A filter that assumes a static channel ($a = 1$, so $Q = 0$) has the error 0.654 on the same data. Its gain falls toward 0, and it stops following the channel.

## Correctness

**Claim.** If the initial taps, the increments $v_k$ and the noise are independent and circular Gaussian, and the symbols in $c_k$ are known and independent of them, then after line L8 at step $k$, $\hat h = E[h_k \mid y[0], \ldots, y[k]]$ and $\Sigma$ is the conditional error covariance. So $\hat h_k$ minimizes the mean squared error over all estimators. Without the Gaussian assumption, $\hat h_k$ is still the best linear estimator. This is a theorem.

**Key step.** By induction, $h_{k-1}$ given the past samples is Gaussian with mean $\hat h$ and covariance $\Sigma$. Then $h_k$ given the same samples has mean $a \hat h$ and covariance $a^2 \Sigma + Q$, because $v_k$ is independent of the past (line L3). The pair $(h_k, y[k])$ is then jointly Gaussian, with $\mathrm{Cov}(h_k, y[k]) = \Sigma c^H$ and $\mathrm{Var}(y[k]) = c \Sigma c^H + N_0$. The formula for a Gaussian conditional mean gives lines L6 to L8. The full proof, with the proper complex Gaussian case and the fit $a = J_0(2\pi f_D T)$, is in the proofs folder. The tests check the filter against the batch LMMSE estimate from the joint covariance $E[h_k \bar h_m^T] = a^{|k-m|} \mathrm{diag}(P)$ within $10^{-9}$.

The claim does not cover two common uses. In decision-directed mode, a wrong decision puts a wrong row $c_k$ into line L4, and the filter does not know it. For a real Clarke channel, the AR(1) model is only a fit. In both cases the output is a good estimate in practice, but this is a heuristic, not a theorem.

## Complexity

Line L3 costs $O(L^2)$ for the covariance, and lines L5, L6 and L8 cost $O(L^2)$ each, because $\Sigma$ is a full $L \times L$ matrix after the first update. Lines L4 and L7 cost $O(L)$. So $K$ symbols cost $O(K L^2)$ time in the [real RAM](/real-ram/), with $O(L^2)$ extra space for $\Sigma$. There is no matrix inverse: the innovation is a scalar. With pilots of known values, the sequence of $\Sigma$ and $g$ does not depend on the data and can be computed in advance.

## Properties

- **Exact for its model.** Under the Gauss-Markov model with known symbols, no estimator has a smaller mean squared error.
- **The covariance does not depend on the samples.** Lines L3, L5, L6 and L8 use only $a$, $Q$, $N_0$ and the regressors. With constant-modulus pilots on one tap, $\Sigma$ converges to the steady value of the example.
- **Bounded uncertainty.** The error variance of each tap stays at most $P_l$, its prior variance.
- **Two limits.** With $a = 1$ and $Q = 0$, the filter gives the Bayesian LMMSE estimate of a fixed channel, and its memory grows without limit. With $a = 0$, each estimate uses only the current sample.
- **Smoothing is better.** The filter uses only the past. A smoother, such as the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/), also uses later samples and has a smaller error, at the cost of delay.

## Variants and improvements

- **Higher-order models.** An AR($p$) model fitted by the Yule-Walker equations matches $p$ lags of the Clarke correlation. The state then holds $p$ past values of each tap, so the cost grows to $O(K (pL)^2)$. Baddour and Beaulieu study such fits and their numerical conditioning.
- **Decision-directed tracking.** After a training block, the regressor holds the decisions of an equalizer. [Per-survivor processing](/per-survivor-processing/) runs one tracker on each survivor path of a Viterbi equalizer, so that each path uses its own decisions.
- **Joint symbol and channel estimation.** An [extended Kalman filter](/extended-kalman-filter/) puts the symbols and the taps in one state.
- **RLS and LMS.** The [RLS algorithm](/rls-algorithm/) with a forgetting factor and the [LMS algorithm](/lms-algorithm/) are cheaper trackers with a fixed memory. They do not use the Doppler spread.
- **Pilot interpolation.** [Pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/) puts pilots at fixed times and interpolates between them with an [LMMSE estimator](/lmmse-channel-estimation/). The Kalman filter is the recursive form of that estimator for the AR model.

## When to use it

Use Kalman tracking when the channel changes during a block, the Doppler spread and the noise level are known or estimated, and the receiver has known symbols or reliable decisions. It suits short channels, because the cost grows as $L^2$. If the channel is static over the block, a one-shot [least squares](/least-squares-channel-estimation/) or LMMSE estimate from a preamble is simpler. If the Doppler spread is unknown, an RLS tracker with a tuned forgetting factor is more robust.

## Pitfalls

- **A static model.** With $a = 1$ in line L3, $Q$ is 0, the gain decays, and the filter stops following the channel. The example shows an error 28 times larger. Set $a$ from the Doppler spread, and keep $a < 1$.
- **The conjugate in the gain.** The observation is $y = c\,h$ without a conjugate on $c$, so line L6 uses $c^H$. With $c^T$ in place of $c^H$, the filter is wrong for complex symbols but still right for BPSK pilots, so the bug can hide.
- **Wrong decisions in line L4.** In decision-directed mode, a decision error gives a wrong regressor, the estimate moves the wrong way, and more errors can follow. Use pilots often enough to recover.
- **Loss of symmetry in line L8.** Rounding makes $\Sigma$ drift away from Hermitian and positive definite over long runs. Symmetrize it after each step, as the implementation does, or use the Joseph form of the update.
- **The wrong correlation model.** The AR(1) model keeps only the lag-1 correlation. On a fast channel, $J_0(2\pi f_D T m)$ and $a^m$ differ already at small lags, and the filter is not optimal for the true channel.

## Implementations

## History

Kalman published the recursive filter for linear state-space models in 1960. Fading channels came into this frame through Gauss-Markov models of the taps: a first-order autoregressive model has one parameter, which can be set from the Doppler spread. Baddour and Beaulieu (2005) studied autoregressive models fitted to the Clarke autocorrelation, for simulation and for tracking. Komninakis, Fragouli, Sayed and Wesel (2002) used a Kalman filter on such a model to track a MIMO fading channel from decisions, for equalization.

## References
