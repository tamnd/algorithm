---
tag: V02V72
kind: problem
slug: adaptive-filtering
name: Adaptive filtering
aliases:
- adaptive signal processing
area: graphics-and-signals/signal-processing
level: core
summary: "Update the coefficients of a filter at each new sample so that its output follows a desired signal whose statistics are unknown or change, at a small cost per sample."
prereqs: [wiener-filter]
see_also: [lms-algorithm, rls-algorithm, kalman-filter, linear-prediction, beamforming, signal-denoising, stochastic-gradient-descent, least-squares-problem]
sources:
  - book: isbn:9780132671453
    title: "Simon Haykin, Adaptive Filter Theory, fifth edition, Pearson, 2014"
    locator: "Background and Preview (the four classes of applications), Chapter 6 (the LMS algorithm), Chapter 10 (the RLS algorithm) and Chapter 13 (adaptation in nonstationary environments)"
  - paper: doi:10.1109/PROC.1975.10036
    title: "Bernard Widrow, John R. Glover, John M. McCool, John Kaunitz, Charles S. Williams, Robert H. Hearn, James R. Zeidler, Eugene Dong and Robert C. Goodlin, Adaptive noise cancelling: Principles and applications, Proceedings of the IEEE 63(12), 1975, pages 1692 to 1716"
    locator: "the noise canceller with a primary and a reference input, and why minimizing the output power leaves the signal"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 13, Adaptive Filters (Section 13.1, applications: system identification, channel equalization, echo cancellation and noise cancelling)"
  - paper: "Bernard Widrow and Marcian E. Hoff, Adaptive switching circuits, IRE WESCON Convention Record, Part 4, 1960"
    locator: "pages 96 to 104, the adaptive linear element and the first stochastic-gradient rule"
---

Adaptive filtering is the problem of changing the coefficients of a filter while the data arrive, so that the filter output follows a desired signal. The statistics that would fix the best filter are not known in advance, or they change with time. At each time $n$ the filter has a weight vector $w[n]$ of length $M$, an input vector $u[n]$ and a desired sample $d[n]$; its output is $y[n] = w[n]^T u[n]$ and its error is $e[n] = d[n] - y[n]$. In a stationary setting the target is the [Wiener filter](/wiener-filter/) $w^\ast = R^{-1} p$, where $R = E[u u^T]$ and $p = E[u\, d]$. An adaptive filter gets close to $w^\ast$ from the data alone, follows $w^\ast$ when it moves, and spends $O(M)$ to $O(M^2)$ operations per sample.

## In plain words

A filter is a fixed recipe that mixes recent input values with fixed weights. The best weights depend on the signal and the noise, but in practice nobody knows them in advance, and they can drift, for example when a phone moves in a room. An adaptive filter learns the weights while it works. At each step it compares its output with a target, sees how wrong it is, and nudges the weights to be less wrong next time. Simple rules make a small, cheap nudge. Better rules remember more of the past and pay more work per step to reach good weights sooner. The open questions are always the same: how fast it learns, how close it gets, how well it follows change, and how much work each new sample costs.

## Definition

**Input.** A stream of pairs $(u[n], d[n])$ for $n = 1, 2, \ldots$, where $u[n] \in \mathbb{R}^M$ and $d[n] \in \mathbb{R}$. In the transversal (FIR) form, $u[n] = (x[n], x[n-1], \ldots, x[n-M+1])$ is a sliding window of one input signal $x$. In the linear-combiner form, the entries of $u[n]$ are different sensors.

**Output.** A causal sequence of weight vectors: $w[n]$ depends only on $u[1..n]$ and $d[1..n]$. The a priori error $e[n] = d[n] - w[n-1]^T u[n]$ uses the weights from before $d[n]$ was seen.

**Criteria.** Three criteria are in common use.

- *Stochastic.* For stationary jointly distributed $(u, d)$, the mean-square error of a fixed $w$ is $J(w) = \sigma_d^2 - 2 p^T w + w^T R w$, with the minimum $J_{\min}$ at $w^\ast$. An algorithm is judged by its convergence time, by the excess error $J_{\text{ex}} = \lim_n E[e[n]^2] - J_{\min}$, by the misadjustment $J_{\text{ex}}/J_{\min}$, and by its error when $w^\ast$ moves.
- *Deterministic.* At each $n$, find the exact minimizer of $\sum_{i=1}^{n} \lambda^{n-i} e_i^2 + \lambda^n \delta \|w\|^2$ with a forgetting factor $0 < \lambda \le 1$ and a regularizer $\delta > 0$. This is a [least-squares problem](/least-squares-problem/) that grows by one row per sample.
- *Worst case.* Bound the ratio of the energy of the estimation errors to the energy of the disturbances, over all disturbances. This is the $H^\infty$ criterion.

The cost model is the number of arithmetic operations per sample in the [real RAM](/real-ram/).

## Variants

The same algorithm serves four configurations, which differ only in what $u$ and $d$ are.

- **System identification.** $u$ drives an unknown system and $d$ is its noisy output. The weights converge to a model of the system. Echo cancellation is this case: the far-end speech drives the echo path and the microphone hears the echo.
- **Inverse modeling.** $u$ is the output of an unknown system and $d$ is a delayed copy of its input, known from a training sequence or from decisions. The filter becomes an equalizer for the channel.
- **Prediction.** $u[n] = (x[n-1], \ldots, x[n-M])$ and $d[n] = x[n]$. The filter is an adaptive [linear predictor](/linear-prediction/).
- **Interference cancelling.** $d$ is a primary input $s + v_0$, with a signal $s$ and an interference $v_0$, and $u$ comes from a reference input that is correlated with $v_0$ but not with $s$. The output of the canceller is the error $e$.

Other variants change the filter structure: adaptive IIR filters have fewer weights but an error surface with local minima; lattice filters adapt order by order; frequency-domain filters adapt in blocks with FFTs; multichannel filters on sensor arrays do adaptive [beamforming](/beamforming/); kernel and Volterra filters are nonlinear in the input.

## Examples

**Identification of a two-tap system.** Let $x$ be white with unit variance, $d[n] = x[n] + \tfrac12 x[n-1] + v[n]$ with white noise $v$ of variance $\sigma_v^2$ independent of $x$, and $M = 2$. Then $R = I$ and $p = (1, \tfrac12)$, so $w^\ast = (1, \tfrac12)$, the true system, and $J_{\min} = \sigma_v^2$. The trace on the [LMS algorithm](/lms-algorithm/) page shows the weights moving toward this point from zero.

**Why a noise canceller does not cancel the signal.** In the interference-cancelling setup, $e = s + (v_0 - y)$, where $y$ depends only on the reference. If $s$ is uncorrelated with the reference and with $v_0$, then $E[e^2] = E[s^2] + E[(v_0 - y)^2]$. The first term does not depend on $w$, so minimizing the output power is the same as minimizing $E[(v_0 - y)^2]$: the filter learns to cancel the interference and leaves $s$ in $e$ (Widrow et al., 1975). If the reference also picks up some of $s$, part of the signal is cancelled too.

## Known algorithms

| algorithm | operations per sample | criterion | notes |
|---|---|---|---|
| [LMS algorithm](/lms-algorithm/) | $O(M)$ | stochastic gradient of $e^2$ | step size $\mu$; speed depends on the eigenvalue spread of $R$ |
| normalized LMS | $O(M)$ | LMS with step $\mu / (\varepsilon + \|u\|^2)$ | stable for $0 < \mu < 2$; insensitive to the input level |
| affine projection | $O(KM)$ for $K$ past inputs | projection on the last $K$ constraints | between NLMS and RLS |
| [RLS algorithm](/rls-algorithm/) | $O(M^2)$ | exact exponentially weighted least squares | speed nearly independent of the eigenvalue spread |
| fast RLS (fast transversal filters) | $O(M)$ | same as RLS, for shift inputs | uses the shift structure; needs care with rounding |
| QR-RLS and lattice RLS | $O(M^2)$ and $O(M)$ | same as RLS | better numerical behavior |
| [Kalman filter](/kalman-filter/) | $O(M^3)$ in general | MMSE for a state model of $w$ | RLS is the special case of a constant or scaled state |

LMS is [stochastic gradient descent](/stochastic-gradient-descent/) on $\tfrac12 e^2$, the same rule as the delta rule of the adaptive linear element.

## Bounds

- **The Wiener floor.** No filter with fixed weights has a mean-square error below $J_{\min}$, and an adaptive filter has a further excess error because its weights are estimated from noisy data. This floor is exact.
- **LMS stability in the mean.** Under the independence assumption (each $u[n]$ independent of the past weights), the mean weight error of LMS obeys $E[w[n]] - w^\ast = (I - \mu R)^n (E[w[0]] - w^\ast)$. For a positive definite $R$, it goes to zero for every start if and only if $0 < \mu < 2/\lambda_{\max}(R)$. The slowest mode decays like $(1 - \mu \lambda_{\min})^n$, so the convergence time grows with the eigenvalue spread $\lambda_{\max}/\lambda_{\min}$. This is proved on the [LMS algorithm](/lms-algorithm/) page.
- **LMS misadjustment.** For small $\mu$ and under the same assumption, the misadjustment is about $\tfrac{\mu}{2} \operatorname{tr} R$. This is an approximation from an analysis, not an exact bound, and the constant depends on the convention for $\mu$.
- **RLS.** With $\lambda = 1$ the RLS weights are the exact regularized least-squares answer at every $n$, so the excess error falls like $M J_{\min} / n$ for large $n$ under Gaussian assumptions, and RLS usually reaches the floor in a small multiple of $M$ samples. With $\lambda < 1$ it keeps an excess error that grows with $(1 - \lambda) M$, and in exchange it follows changes.
- **Cost.** Any algorithm that can change all $M$ weights at each sample needs $\Omega(M)$ operations per sample. LMS, NLMS and fast RLS meet this bound.

## Reductions

- **To the Wiener filter.** In a stationary environment the target of every algorithm in the table is the [Wiener filter](/wiener-filter/), and with $\lambda = 1$ the RLS weights converge to it with probability one when the sample averages of $u u^T$ and $u d$ converge to $R$ and $p$.
- **To least squares.** RLS solves a sequence of [least-squares problems](/least-squares-problem/), one new row at a time, with a rank-one update of the inverse.
- **To state estimation.** If the unknown weights follow a linear state model, such as $w[n+1] = w[n]$ or a random walk, and $d[n] = u[n]^T w[n] + v[n]$, then estimating $w[n]$ is a [state estimation](/state-estimation/) problem, and the [Kalman filter](/kalman-filter/) gives RLS for the constant model.
- **To online learning.** With features in place of shifted samples, adaptive filtering is online [linear regression](/linear-regression/) with the squared loss.

## Applications

- **Echo cancellation** on telephone lines and in hands-free speakerphones, usually with NLMS and filters of hundreds or thousands of taps.
- **Channel equalization** in modems and receivers, trained on a known sequence and then driven by decisions.
- **Active noise control** in headphones and ducts, where the error is measured by a microphone after a secondary path.
- **Noise and interference cancelling** in biomedical signals, for example mains hum in an electrocardiogram, as in the examples of Widrow et al.
- **Adaptive beamforming** with arrays of antennas or microphones, see [beamforming](/beamforming/).
- **Adaptive prediction** in speech coders with backward adaptation, which needs no side information.

## References
