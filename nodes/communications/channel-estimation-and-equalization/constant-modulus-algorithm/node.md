---
tag: BYWJFM
kind: algorithm
slug: constant-modulus-algorithm
name: Constant modulus algorithm
aliases:
- Godard algorithm
area: communications/channel-estimation-and-equalization
level: core
summary: "A blind equalizer that adapts its taps by stochastic gradient on E(|z|^2 - R2)^2, so that the output modulus is as constant as possible. It ignores the carrier phase and can lock to a local minimum."
solves: [blind-equalization]
model: real-ram
complexity:
  vars: {N: the number of equalizer taps, K: the number of samples}
  time: {worst: O(K N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, blind: true, phase_independent: true, global_convergence: false}
history:
  year: 1980
  people: [Dominique N. Godard, John R. Treichler, Brian G. Agee]
  note: "Godard proposed a family of dispersion criteria for QAM in 1980; the case p = 2 is CMA. Treichler and Agee derived the same algorithm for constant envelope signals in 1983 and named it the constant modulus algorithm."
prereqs: [blind-equalization, lms-algorithm]
see_also: [sato-algorithm, adaptive-equalization, fractionally-spaced-equalizer, tong-xu-kailath-identification, carrier-recovery, decision-feedback-equalizer, mmse-linear-equalizer, stochastic-gradient-descent]
sources:
  - paper: "Dominique N. Godard, Self-recovering equalization and carrier tracking in two-dimensional data communication systems, IEEE Transactions on Communications 28(11), 1980, pages 1867 to 1875"
    locator: "the dispersion criteria E(|z|^p - R_p)^2 and their stochastic gradient algorithms"
  - paper: "John R. Treichler and Brian G. Agee, A new approach to multipath correction of constant modulus signals, IEEE Transactions on Acoustics, Speech, and Signal Processing 31(2), 1983, pages 459 to 472"
    locator: "the constant modulus algorithm for signals of constant envelope"
  - paper: doi:10.1109/5.720246
    title: "C. Richard Johnson, Jr., Philip Schniter, Thomas J. Endres, James D. Behm, Donald R. Brown and Raul A. Casas, Blind equalization using the constant modulus criterion: a review, Proceedings of the IEEE 86(10), 1998, starting at page 1927"
    locator: "the conditions under which the CM minima of a fractionally spaced equalizer are perfect equalizers, and the independence of the CM criterion from the carrier phase"
  - paper: doi:10.1109/26.99137
    title: "Zhi Ding, Rodney A. Kennedy, Brian D. O. Anderson and C. Richard Johnson, Jr., Ill-convergence of Godard blind equalizers in data communication systems, IEEE Transactions on Communications 39(9), 1991, pages 1313 to 1327"
    locator: "local minima of the Godard cost for FIR equalizers"
  - paper: doi:10.1002/j.1538-7305.1985.tb00040.x
    title: "G. J. Foschini, Equalizing without altering or detecting data, AT&T Technical Journal 64(8), 1985, pages 1885 to 1911"
    locator: "convergence of the Godard algorithm for an ideal equalizer of unbounded length"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 10 (adaptive equalization), the section on blind equalization"
---

The constant modulus algorithm (CMA) is the most used blind equalizer. It adapts the $N$ taps of a linear equalizer without a training sequence. It does this by a stochastic gradient step on the cost $J = E(|z|^2 - R_2)^2$, where $z$ is the equalizer output and $R_2 = E|a|^4 / E|a|^2$ is a constant of the symbol alphabet. The cost does not change if $z$ is rotated, so CMA works before the carrier phase is known, and it leaves the phase to a later [carrier recovery](/carrier-recovery/) stage. It costs $O(N)$ per sample. Among the methods for [blind equalization](/blind-equalization/), it differs from the [Sato algorithm](/sato-algorithm/), which pushes the output toward a scaled sign and so depends on the phase, and from [Tong-Xu-Kailath identification](/tong-xu-kailath-identification/) and [subspace identification](/subspace-channel-identification/), which estimate the channel in one batch from second-order statistics of an oversampled signal. CMA uses fourth-order statistics, so it can equalize a nonminimum-phase channel at one sample per symbol. Its weak points are that a finite equalizer can lock to a local minimum and that the output has an unknown phase.

## In plain words

A blind equalizer must fix a distorted signal without being told what was sent. CMA uses one fact about the symbols: for PSK all of them have the same size, and for QAM their sizes vary in a known way. Echoes from the channel make the received samples grow and shrink in size. So the equalizer changes its weights a little after each sample, in the direction that makes the size of its output steadier. When the size is as steady as it can be, the echoes are gone. The method never looks at the angle of the output. So it works before the receiver has found the carrier phase, but at the end the output can still be turned by an unknown angle, and a later stage must remove it.

## The problem

The input is the received sequence $y[k] = \sum_l h_l\, a[k-l] + w[k]$ at one sample per symbol (or several, for a fractionally spaced equalizer), the number of taps $N$ and a step size $\mu > 0$. The channel $h$ is unknown. The symbols $a[k]$ are independent and identically distributed, with mean zero, $E a^2 = 0$ (a circular alphabet such as QPSK or square QAM) and a known distribution. The equalizer output is $z[k] = \sum_{i=0}^{N-1} c_i\, y[k-i]$. The goal is taps $c$ with $z[k] \approx e^{j\theta} a[k - d]$ for some delay $d$ and phase $\theta$. Blind methods can find $d$ and $\theta$ only up to these ambiguities.

The cost is the Godard criterion with $p = 2$:
$$J(c) = E\left(|z[k]|^2 - R_2\right)^2, \qquad R_2 = \frac{E|a|^4}{E|a|^2}.$$
For unit-energy QPSK and every PSK, $R_2 = 1$. For unit-energy 16-QAM, the raw points $\pm 1, \pm 3$ on each axis give $E|a|^2 = 10$ and $E|a|^4 = 132$, so $R_2 = 132/100 = 1.32$.

## The algorithm

```pseudo id=main
CMA(y, N, μ, R2)
L1  c ← (0, ..., 0);  c[⌊N/2⌋] ← 1              ▷ the center spike
L2  for k ← N - 1 to K - 1 do
L3      u ← (y[k], y[k-1], ..., y[k-N+1])
L4      z[k] ← Σ_i c[i] u[i]                     ▷ the equalizer output
L5      e ← z[k] (|z[k]|² - R2)                  ▷ the CMA error
L6      c[i] ← c[i] - μ e conj(u[i])  for all i    ▷ the stochastic gradient step
L7  return c, z
```

Line L1 starts the taps at a single 1 in the middle. This lets the equalizer reach a delay near $N/2$, which it needs for a nonminimum-phase channel, whose inverse looks into the future. Line L4 is the filter. Line L5 is the error term. It is zero when $|z| = \sqrt{R_2}$, and it has the direction of $z$. Line L6 is the update. The derivative of $(|z|^2 - R_2)^2$ with respect to $\bar c_i$ is $2(|z|^2 - R_2)\, z\, \bar u_i$, so line L6 is one step of [stochastic gradient descent](/stochastic-gradient-descent/) on $J$, with the factor 2 in $\mu$. The update has the form of the [LMS algorithm](/lms-algorithm/), with $z - $ (desired value) replaced by the CMA error. No line uses a decision or a known symbol. After the taps converge, a decision device and a phase tracker take over, often with a switch to the decision-directed LMS update of [adaptive equalization](/adaptive-equalization/).

## Example

**The check value.** For unit-energy 16-QAM, $R_2 = 1.32$, as computed above. The tests check it with exact fractions.

**QPSK through a nonminimum-phase channel.** Take $h = (0.5, 1)$. Its zero is at $-2$, outside the unit circle, so it is nonminimum phase. Use $N = 11$ taps, $\mu = 0.01$, $R_2 = 1$ and $N_0 = 0.001$ (seed 5). The combined response $g = c * h$ should become one large tap. Its residual ISI, $(\sum |g_k|^2 - \max |g_k|^2) / \max |g_k|^2$, falls as follows:

| samples | 500 | 1000 | 2000 | 6000 |
|---|---|---|---|---|
| residual ISI | 0.00672 | 0.00065 | 0.00033 | 0.00042 |
| largest tap $\lvert g_6 \rvert$ | 0.966 | 0.999 | 0.994 | 0.992 |

The delay is $d = 6$: the center spike at tap 5 plus the main tap of $h$ at index 1. The taps approximate the anticausal inverse $z^{-5} / (1 + 0.5 z)$. The last 2000 decisions have no errors. The residual ISI stops falling near $4 \times 10^{-4}$, because the noise and the step size keep the taps moving.

**The phase is not found.** If the channel is $e^{j\pi/6} (0.5, 1)$ instead, CMA gives the same taps exactly, and the output is turned by 30 degrees. The tests check this: a rotated input gives the same taps within $10^{-9}$.

**A local minimum.** Take $h = (1, 0.5)$, QPSK, no noise and only $N = 2$ taps. The mean update, which is gradient descent on $J$, ends in one of two points. From $c = (1, 0)$ it reaches $c = (0.934, -0.376)$ with $J = 0.0838$ and delay 0. From $c = (0, 1)$ it reaches $c = (0.069, 0.751)$ with $J = 0.2375$, delay 1 and the residual ISI 0.236. Small random moves of the taps return to the same point, so this is a local minimum, not a saddle. Started there, CMA stays in the worse equalizer.

## Correctness

**Claim 1 (the cost of a combined response).** Let the symbols be independent, circular ($E a^2 = 0$), with $E|a|^2 = 1$ and $\kappa = E|a|^4$, and let the noise be zero. Then $z = \sum_k g_k\, a[n-k]$ and
$$J = 2 s^2 + (\kappa - 2) \sum_k |g_k|^4 - 2\kappa s + \kappa^2, \qquad s = \sum_k |g_k|^2 .$$
This is a closed form, and the tests check it against an exact sum over all symbol patterns.

**Claim 2 (the global minima).** If $\kappa < 2$, which holds for every PSK and QAM alphabet ($\kappa = 1$ for PSK, $1.32$ for 16-QAM), then the minimum of $J$ over all combined responses is $\kappa(\kappa - 1)$, and the minimizers are exactly $g = e^{j\theta} e_d$: one tap of modulus 1, at any delay $d$ and any phase $\theta$. This is a theorem. So if the equalizer can produce $g = e_d$, the global minima of CMA are perfect equalizers, up to delay and phase.

**Key step.** For fixed $s$, $\sum |g_k|^4 \le s^2$, with equality only if $g$ has one nonzero tap. Since $\kappa - 2 < 0$, $J \ge \kappa s^2 - 2\kappa s + \kappa^2 = \kappa(s - 1)^2 + \kappa(\kappa - 1)$, with equality only for one tap and $s = 1$. The proofs folder has the moment computation, the gradient of lines L5 and L6, and the proof that a rotated input gives the same taps.

**What is not claimed.** The update of line L6 is a stochastic gradient step, so for small $\mu$ the taps follow the gradient flow of $J$. But a finite equalizer at one sample per symbol cannot produce $g = e_d$ exactly, and then $J$ can have local minima that are poor equalizers (Ding, Kennedy, Anderson and Johnson 1991). The example shows one. Foschini (1985) proved convergence for an ideal equalizer of unbounded length. For a fractionally spaced equalizer, the review of Johnson et al. (1998) gives conditions (no noise, subchannels with no common zero, enough taps) under which the CM minima are perfect equalizers. In all other cases, convergence to the global minimum is not guaranteed.

## Complexity

Lines L3 to L6 cost $O(N)$ operations per sample: $N$ complex multiplications for the output and $N$ for the update. $K$ samples cost $O(K N)$ time in the [real RAM](/real-ram/) and $O(N)$ extra space. The number of samples needed to converge depends on $\mu$, the channel and the alphabet. In the example it is about 1000 for QPSK and about 4000 for 16-QAM with a smaller step; these are measurements.

## Properties

- **Phase independent.** $J$ and the update see only $|z|$, so a rotation of the input gives the same taps and a rotated output. CMA can run before carrier recovery.
- **No training.** The only prior knowledge is $R_2$, which depends on the alphabet and not on the data.
- **Works on nonminimum-phase channels.** $J$ depends on fourth-order moments of $g$, through $\sum |g_k|^4$, which second-order statistics do not see.
- **Not a decision-directed method.** CMA can open a closed eye, where decision-directed LMS fails. After the eye opens, decision-directed LMS gives a smaller error.
- **Excess error.** For QAM, $|a|^2$ is not constant, so the update never settles even at a perfect equalizer: $J = \kappa(\kappa - 1) > 0$ at the minimum. The taps move in a random way around the minimum, more so for a larger $\mu$.
- **Near the MMSE solution.** With noise, the CM minima are not the MMSE taps, but they are close to them when the noise is small (Johnson et al. 1998).

## Variants and improvements

- **Godard p = 1.** The cost $E(|z| - R_1)^2$ with $R_1 = E|a|^2 / E|a|$ gives the error $z(|z| - R_1)/|z|$. Godard's family has one algorithm for each $p$.
- **The multimodulus algorithm.** Separate costs on the real and imaginary parts, $E(z_R^2 - R)^2 + E(z_I^2 - R)^2$, recover the phase up to a multiple of 90 degrees for square QAM.
- **Fractionally spaced CMA.** With two samples per symbol, the equalizer can reach $g = e_d$ exactly when the subchannels have no common zero, and the local minima caused by a short equalizer go away in the noiseless case; see the [fractionally spaced equalizer](/fractionally-spaced-equalizer/).
- **Switch to decision-directed mode.** Run CMA until the eye opens, then switch to decision-directed LMS, as in [adaptive equalization](/adaptive-equalization/).
- **The Shalvi-Weinstein criterion.** Maximize the kurtosis of $z$ under a power constraint. This is a fourth-order criterion like CMA.
- **CMA with a DFE.** A [decision feedback equalizer](/decision-feedback-equalizer/) can run its feedforward part with CMA, but blind feedback is prone to error propagation.

## When to use it

Use CMA when there is no training sequence, or when the training is too short or lost, and the carrier phase is not yet known. Typical uses are broadcast and cable receivers, receivers that join a running stream, and the start-up of a point-to-multipoint link. If a training sequence is available, use it instead: LMS or RLS converge faster and to the MMSE taps. If many samples are available in a block and the signal is oversampled, a batch method from second-order statistics, such as the [subspace method](/subspace-channel-identification/), estimates the channel without the risk of a local minimum.

## Pitfalls

- **A spike at the wrong place in line L1.** A spike on the first tap allows only small delays, and the inverse of a nonminimum-phase channel needs a large one. Put the spike near the middle. The example with two taps shows how the start picks the minimum.
- **A step size that is too large in line L6.** The update is cubic in $z$, so a large $\mu$ or a large input makes the taps diverge. Normalize the input power, and pick $\mu$ much smaller than $1/(N E|y|^2)$.
- **The wrong R2 in line L5.** $R_2 = E|a|^4/E|a|^2$ must use the same scale as the received signal. If the gain of the channel is unknown, CMA still converges, but to taps scaled so that the output has the modulus $\sqrt{R_2}$.
- **Forgetting the phase.** CMA returns $e^{j\theta} a[k - d]$. A slicer fed directly with $z$ makes many errors for any $\theta$ that is not a symmetry of the constellation. A phase tracker must follow.
- **Taking a local minimum for a good one.** A low CMA cost is not proof of a good equalizer. Watch the decision error, and restart from another spike if it stays high.

## Implementations

## History

Sato published the first blind equalizer for multilevel PAM in 1975. Godard (1980) gave a family of criteria for two-dimensional signals such as QAM, $E(|z|^p - R_p)^2$, which do not depend on the carrier phase. The case $p = 2$ is CMA. Treichler and Agee (1983) derived the same algorithm for signals of constant envelope, such as FM, and named it the constant modulus algorithm. Foschini (1985) proved that the algorithm converges for an ideal equalizer of unbounded length. Ding, Kennedy, Anderson and Johnson (1991) showed that FIR equalizers can have local minima. The review of Johnson and coauthors (1998) collects the theory of the CM criterion, including the conditions for fractionally spaced equalizers.

## References
