---
tag: FM2HQC
kind: technique
slug: adaptive-equalization
name: Adaptive equalization
aliases:
- decision-directed equalization
area: communications/channel-estimation-and-equalization
level: core
summary: "Adjusts the equalizer taps with an adaptive filter such as LMS, first from a training sequence and then from the decided symbols, so the equalizer learns and tracks an unknown channel."
prereqs: [channel-equalization, lms-algorithm]
see_also: [kalman-channel-tracking, mmse-linear-equalizer, decision-feedback-equalizer, fractionally-spaced-equalizer, rls-algorithm, wiener-filter, blind-equalization, constant-modulus-algorithm]
sources:
  - paper: doi:10.1002/j.1538-7305.1965.tb01678.x
    title: "R. W. Lucky, Automatic equalization for digital communication, Bell System Technical Journal 44(4), 1965, pages 547 to 588"
    locator: "the automatic adjustment of a transversal equalizer from the received data"
  - paper: "Shahid U. H. Qureshi, Adaptive equalization, Proceedings of the IEEE 73(9), 1985, pages 1349 to 1387"
    locator: "the training and decision-directed modes, LMS and RLS adaptation, and the tracking of slow channel changes"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 10 (adaptive equalization)"
  - book: isbn:9780792375487
    title: "John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004"
    locator: "the chapter on adaptive equalization"
---

Adaptive equalization is the technique of learning the taps of an equalizer from the received signal, in place of computing them from a known channel. An adaptive filter, usually the [LMS algorithm](/lms-algorithm/), adjusts the taps at every symbol to make the equalizer output match a target symbol. During a training sequence the target is the known symbol. After it, the target is the receiver's own decision, so the equalizer keeps tracking slow changes of the channel with no extra overhead. The taps move toward the [MMSE equalizer](/mmse-linear-equalizer/) taps on average, and the same template adapts a [decision feedback equalizer](/decision-feedback-equalizer/) or a [fractionally spaced equalizer](/fractionally-spaced-equalizer/). This page differs from [Kalman channel tracking](/kalman-channel-tracking/): here the filter adapts the equalizer taps directly, with a fixed step and no model of how the channel moves; there a Kalman filter estimates the channel itself, using a model of its motion to set the gain at each step.

## In plain words

A receiver does not know the echoes of the channel in advance, and the echoes can change slowly. So the receiver starts with a filter that does nothing and improves it a little at each symbol. At the start, the sender transmits symbols that the receiver already knows. The receiver compares its filter output with the known symbol and nudges the filter in the direction that makes the difference smaller. After the known part ends, the receiver uses its own decisions as the right answers. This works as long as most decisions are correct. If too many are wrong, the filter learns the wrong thing and the receiver must start again with known symbols.

## When it applies

- The channel is unknown or changes slowly compared with the time the filter needs to adapt.
- A training sequence is available at the start, or the eye is already open, so that most decisions are correct.
- The equalizer structure is fixed: a linear filter, a decision feedback filter or a fractionally spaced filter, whose output is linear in the taps.
- The cost of a closed form design, such as a matrix solve for the MMSE taps, is too high per symbol, or the channel statistics needed for it are unknown.

It does not apply as stated when there is no training and the eye is closed; then a blind start such as the [constant modulus algorithm](/constant-modulus-algorithm/) must open the eye first, see [blind equalization](/blind-equalization/).

## The template

The input is the received samples $y$, the training symbols $a[0], \ldots, a[T-1]$, the number of taps $N$, the decision delay $d$, the step size $\mu$ and the constellation. The output $z[k] = \sum_i c_i\, y[k-i]$ estimates $a[k-d]$. The holes are the adaptive rule (here LMS) and the decision rule (here the nearest constellation point).

```pseudo id=main
ADAPTIVE-EQUALIZER(y, a[0..T-1], N, d, μ, constellation)
L1  c ← (0, ..., 0)
L2  for k ← N - 1 to K - 1 do
L3      u ← (y[k], y[k-1], ..., y[k-N+1])
L4      z[k] ← Σ_i c[i] u[i]
L5      if k - d < T then target ← a[k - d]            ▷ training mode
L6      else target ← the constellation point nearest to z[k]   ▷ decision mode
L7      e ← z[k] - target
L8      c[i] ← c[i] - μ e conj(u[i])  for all i          ▷ LMS
L9  return c, z
```

Lines L3 and L4 are the equalizer. Lines L5 and L6 choose the target: a known symbol while training lasts, the decision after. Lines L7 and L8 are one LMS step on the squared error $|z - \text{target}|^2$.

**Where it converges.** In training mode, the targets are the true symbols, and line L8 is a stochastic gradient step on $J(c) = E|z[k] - a[k-d]|^2$. The minimizer is the [Wiener](/wiener-filter/) solution $c^* = \overline{R^{-1} p}$ with $R = E[u u^H]$ and $p = E[u\, \overline{a[k-d]}]$, which is the MMSE equalizer for the delay $d$. This is a closed form. Under the usual independence assumption of LMS theory, the mean taps converge to $c^*$ if $0 < \mu < 2/\lambda_{\max}(R)$, and the slowest mode decays like $(1 - \mu \lambda_{\min})^k$. This is a theorem under that assumption, not for the real dependent regressors. The excess error above $J(c^*)$ grows with $\mu$.

**Decision mode.** If every decision is correct, line L6 gives the same target as training, and the analysis holds. Wrong decisions bias the update. There is no general guarantee: the mode works when the decision error rate is low, which is a heuristic rule backed by practice.

**Cost.** Lines L3 to L8 cost $O(N)$ per symbol, plus the decision in line L6, which is $O(M)$ for $M$ points, or $O(1)$ per axis for square QAM. The memory is $O(N)$.

**Example.** One tap, $y = (0.9, 1.2)$, training symbols $(1, 1)$, $d = 0$ and $\mu = 0.1$. At $k = 0$: $z = 0$, $e = -1$, $c = 0 + 0.1 \times 1 \times 0.9 = 0.09$. At $k = 1$: $z = 0.09 \times 1.2 = 0.108$, $e = -0.892$, $c = 0.09 + 0.1 \times 0.892 \times 1.2 = 0.197$.

A larger run: QPSK through $h = (1, 0.5)$ with $N_0 = 0.01$, $N = 11$, $d = 5$, $\mu = 0.01$ and seed 1. The Wiener MSE is $0.0132$, and the Wiener taps from tap 5 on are $0.983, -0.485, 0.238, -0.116$, close to the inverse of the channel. The MSE of the LMS taps after $K$ training symbols is a measurement:

| training symbols | 100 | 200 | 500 | 1000 | 2000 | 6000 |
|---|---|---|---|---|---|---|
| MSE of the taps | 0.208 | 0.075 | 0.024 | 0.0139 | 0.0136 | 0.0138 |

With 1000 training symbols and then the decision mode on 11000 more (seed 2), there are no decision errors and the MSE stays within 10 percent of the Wiener value. On the Proakis B channel $(0.407, 0.815, 0.407)$, which has a deep spectral notch, 6000 training symbols give an MSE of $0.196$ against the Wiener $0.190$, but taps that differ from the Wiener taps by up to $0.29$: the slow modes of a large eigenvalue spread have not converged, although they hardly change the MSE. The tests in the code folder check these runs.

## Classic examples

- **Voiceband modems.** Lucky (1965) adjusted the taps of a transversal equalizer automatically from the data, and adaptive equalizers made high-speed telephone modems possible. Modems sent a short training sequence at the start of a call and then adapted from decisions.
- **Adaptive DFE.** The feedforward and feedback filters of a [decision feedback equalizer](/decision-feedback-equalizer/) are both linear in their taps, so one LMS step on the stacked tap vector adapts both. The past decisions are already available for the feedback filter.
- **Fractionally spaced adaptive equalizers.** A [fractionally spaced equalizer](/fractionally-spaced-equalizer/) adapted by LMS also learns the sampling phase, which made it the usual choice in later modems.
- **Blind start, then decisions.** In cable and broadcast receivers, a blind algorithm such as CMA or the [Sato algorithm](/sato-algorithm/) opens the eye, and the receiver then switches to the decision mode of this template.

## Variations

- **RLS in place of LMS.** The [RLS algorithm](/rls-algorithm/) converges in about $2N$ symbols by a common rule of thumb, almost independently of the eigenvalue spread, at a cost of $O(N^2)$ per symbol. It suits short training sequences and channels with deep notches.
- **Normalized LMS.** Divide the step by $\|u\|^2$, which makes the convergence less sensitive to the signal level.
- **Sign algorithms.** Use the sign of the error or of the regressor in line L8. This saves multiplications in hardware, at the cost of slower convergence.
- **Channel tracking in place of tap adaptation.** Estimate the channel with a [Kalman filter](/kalman-channel-tracking/) or with RLS, and design the equalizer from the estimate. This uses a model of how the channel moves.
- **Periodic training.** Insert training symbols at intervals, as in burst systems, so that the equalizer can recover after error bursts.

## Pitfalls

- **A step that is too large in line L8.** If $\mu \ge 2/\lambda_{\max}(R)$, the mean taps diverge. Even below that, a large $\mu$ gives a large excess error. A normalized step or a step that shrinks after training helps.
- **A step that is too small.** The slowest mode needs about $1/(\mu \lambda_{\min})$ symbols. On a channel with a deep notch, the eigenvalue spread is large and LMS converges slowly, as the Proakis B example shows.
- **Switching to line L6 too early.** If the decision error rate is high, the decisions pull the taps the wrong way, and errors feed more errors. Switch only after the training has opened the eye.
- **A delay that does not fit.** The delay $d$ must give the equalizer room to cancel both the precursors and the postcursors. A delay at the edge of the filter, such as $d = 0$ on a nonminimum-phase channel, leaves a large MSE whatever the step.
- **Fast fading.** If the channel changes faster than LMS can track, the taps lag behind. A tracker with a model of the channel motion, such as the Kalman filter, does better.

## Exercises

1. For a one-tap equalizer on the channel $y[k] = h\, a[k] + w[k]$, with $E|a|^2 = 1$ and noise power $N_0$, find the Wiener tap and the largest step for which the mean of the LMS tap converges.
2. Show that if every decision of line L6 is correct, the decision mode gives exactly the same tap sequence as training mode with the same symbols.
3. Write the LMS update for a DFE with $N_f$ feedforward and $N_b$ feedback taps. Which regressor does the feedback part use?
4. Run the code on Proakis B with 6000 training symbols and $\mu = 0.01$, then with RLS. Compare the number of symbols each needs to reach an MSE within 10 percent of the Wiener value.

## References
