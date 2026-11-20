---
tag: FAG3FG
kind: algorithm
slug: equal-gain-combining
name: Equal gain combining
aliases:
- EGC
area: communications/fading-channels
level: core
summary: "Removes the phase of each diversity branch and adds the branches with equal weights. It needs the branch phases but not the amplitudes, and is a little worse than maximal ratio combining."
solves: [symbol-detection]
model: real-ram
complexity:
  vars: {L: the number of diversity branches}
  time: {worst: O(L)}
  space: {extra: O(1)}
properties: {needs_branch_phases: true, needs_branch_amplitudes: false, optimal_linear_combiner: false, diversity_order: L}
history:
  year: 1959
  people: [D. G. Brennan]
  note: "Brennan analyzed equal gain combining with maximal ratio and selection combining in his 1959 survey of linear diversity combining, and found it nearly as good as maximal ratio combining."
prereqs: [maximal-ratio-combining, rayleigh-fading-channel]
see_also: [maximal-ratio-combining, selection-combining, diversity-order, rayleigh-fading-channel, nakagami-m-fading-channel, noncoherent-detection, beamforming, gaussian-q-function]
sources:
  - paper: doi:10.1109/JRPROC.1959.287136
    title: "D. G. Brennan, Linear diversity combining techniques, Proceedings of the IRE 47(6), 1959, pages 1075 to 1102"
    locator: "the analysis of equal gain combining and its comparison with maximal ratio and selection combining"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Section 7.2.5 (equal-gain combining)"
  - book: isbn:9780471649533
    title: "Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, 2nd edition, Wiley, 2005"
    locator: "Chapter 9, Section 9.3 (equal gain combining)"
---

Equal gain combining (EGC) is a linear receiver for $L$ diversity branches: it turns each branch by the negative of the phase of its gain and adds the branches with the same weight. It is one of the three classic combiners whose [diversity order](/diversity-order/) is $L$ with independent branches; [maximal ratio combining](/maximal-ratio-combining/) also weights each branch by its amplitude and gets the best SNR, and [selection combining](/selection-combining/) keeps only the best branch. EGC needs the phases of the branches but not their amplitudes, and its loss against maximal ratio combining in Rayleigh fading is about 0.5 to 0.7 dB.

## In plain words

The same message arrives over several antennas, each copy with its own strength and its own phase. If the copies were added as they are, their phases could cancel each other. EGC first turns every copy so that all of them point the same way, and then simply adds them, all with the same weight. It does not need to know how strong each copy is, only its phase. This is simpler than giving each copy its best weight, and the loss is small when the copies have similar strengths. When one copy is very weak, EGC still adds its full noise, and then it can do worse than just picking the best copy.

## The problem

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$, where $x$ is the transmitted symbol with energy $E_s$, $h_l$ is the complex fading gain, and $w_l \sim CN(0, N_0)$ is noise with the same power on every branch, independent across branches. The branch SNR is $\gamma_l = |h_l|^2 E_s/N_0$ with mean $\bar\gamma$. The receiver knows the phase $\arg h_l$ of each branch, and uses $|h_l|$ only to scale the final estimate. The task is to form one statistic from the $y_l$ and pass it to a [symbol detector](/symbol-detection/). The gains may follow block fading or fast fading; the combiner acts symbol by symbol either way, with CSIR on the phases and no CSIT.

## The algorithm

```pseudo id=main
EGC(h[1..L], y[1..L])
L1  c_l ← h_l / |h_l|  for l = 1 .. L              ▷ unit weights with the phase of each branch
L2  z ← Σ_l conj(c_l) · y_l
L3  a ← Σ_l |h_l|
L4  return z / a, a                                 ▷ z / a = x + noise of variance L N0 / a²
```

Line L1 keeps only the phase of each gain. Line L2 cophases and adds: each term becomes $|h_l| x$ plus noise of the same power $N_0$, because $|c_l| = 1$. Line L3 is the sum of the amplitudes, which line L4 uses to scale $z$ into an estimate of $x$. For BPSK and other constant-energy formats with a sign or phase decision, line L3 is not needed, because scaling by $a > 0$ does not change the decision. A branch with $h_l = 0$ gets the weight 0.

## Example

Take $L = 2$, $N_0 = 1$, $E_s = 1$ and the gains $h_1 = 1 + j$, $h_2 = 0.5j$. The weights are $c_1 = (1 + j)/\sqrt 2$ and $c_2 = j$. With $x = 1$ and no noise, line L2 gives $z = \sqrt 2 + 0.5 = 1.914$ and line L3 gives $a = 1.914$, so $z/a = 1$. The output SNR is $E_s a^2/(L N_0) = 1.914^2/2 = 1.832$, against $\gamma_1 + \gamma_2 = 2.25$ for maximal ratio combining and $\max \gamma_l = 2$ for selection combining. Here EGC is the worst of the three, because the branches are unequal.

For two independent [Rayleigh](/rayleigh-fading-channel/) branches with mean $\bar\gamma$ each, the bit error rate of coherent BPSK has the closed form (independent Rayleigh branches, equal noise powers, perfect phases)

$$P_b = \frac12\left(1 - \frac{\sqrt{\bar\gamma(\bar\gamma + 2)}}{\bar\gamma + 1}\right).$$

A direct numerical integral over the two amplitudes agrees with it within a relative error of $10^{-6}$ at 0, 5 and 10 dB.

| $\bar\gamma$ per branch | MRC, $L = 2$ | EGC, $L = 2$ | SC, $L = 2$ |
|---|---|---|---|
| 0 dB | 0.05806 | 0.06699 | 0.08157 |
| 5 dB | 0.011829 | 0.014645 | 0.019701 |
| 10 dB | $1.5991 \cdot 10^{-3}$ | $2.0704 \cdot 10^{-3}$ | $2.9729 \cdot 10^{-3}$ |
| 20 dB | $1.8442 \cdot 10^{-5}$ | $2.4508 \cdot 10^{-5}$ | $3.6581 \cdot 10^{-5}$ |

At 20 dB the ratio of EGC to MRC is 1.33, so with the slope $\bar\gamma^{-2}$ EGC needs about 0.6 dB more per branch for the same error rate. A simulation of 20000 BPSK bits at 5 dB (seed 6003) gives a Wilson interval with $z = 3.29$ that contains 0.014645.

## Correctness

**Claim.** The output of line L4 is $z/a = x + n$ with $n \sim CN(0, L N_0/a^2)$, so the output SNR is $\gamma_{\mathrm{EGC}} = E_s(\sum_l |h_l|)^2/(L N_0)$. It satisfies $\frac1L \sum_l \gamma_l \le \gamma_{\mathrm{EGC}} \le \sum_l \gamma_l$, and for independent Rayleigh branches $E[\gamma_{\mathrm{EGC}}] = \bar\gamma(1 + (L - 1)\pi/4)$. These are theorems under the stated model.

**Key step.** Each term of line L2 is $|h_l| x + c_l^* w_l$, and $c_l^* w_l$ has the same distribution as $w_l$ because $|c_l| = 1$. The upper bound is the Cauchy-Schwarz inequality $(\sum_l |h_l|)^2 \le L\sum_l |h_l|^2$, and the lower bound follows from $(\sum_l |h_l|)^2 \ge \sum_l |h_l|^2$. The mean uses $E|h_l| = \sqrt{\pi\Omega}/2$ for a Rayleigh amplitude. The full proof is in the proofs folder.

## Complexity

Lines L1 to L3 take $O(L)$ operations per symbol, in the [real RAM](/real-ram/), with $O(1)$ extra space. In hardware, the cophasing of line L1 is a phase rotation per branch, with no multiplier for the amplitude. The receiver still needs one radio chain per branch and a phase estimate per branch.

## Properties

- **Mean output SNR.** $\bar\gamma(1 + (L - 1)\pi/4)$ for independent Rayleigh branches: 1.785 times $\bar\gamma$ for $L = 2$ (2.52 dB), against 2 (3.01 dB) for maximal ratio combining and 1.5 (1.76 dB) for selection combining.
- **Diversity order $L$.** With independent Rayleigh branches, the error rate falls as $\bar\gamma^{-L}$. The loss against maximal ratio combining is a constant shift of the curve, not a change of slope.
- **Not always better than selection.** With $h = (1, 0)$, EGC has output SNR $\frac12 E_s/N_0$, while selection combining has $E_s/N_0$. The added branch brings noise but no signal.
- **Between the bounds.** $\frac1L\sum_l\gamma_l \le \gamma_{\mathrm{EGC}} \le \sum_l\gamma_l$, with equality on the right when all $|h_l|$ are equal.
- **No closed form in general.** The output SNR is the square of a sum of Rayleigh variables, whose distribution has no simple form. For $L = 2$ in Rayleigh fading the BPSK error rate above is exact; for larger $L$ it is usually computed by numerical integration or series.

## Variants and improvements

- **Maximal ratio combining.** Adding the amplitude weights gives the best linear combiner; see [maximal ratio combining](/maximal-ratio-combining/).
- **Equal gain transmission.** With CSIT, a transmitter with $L$ antennas can send $x$ with the phases $e^{-j\arg h_l}/\sqrt L$ and constant amplitude, which gives the same output SNR as EGC at the receiver. It suits power amplifiers that need a constant envelope per antenna.
- **Noncoherent EGC.** For [noncoherent detection](/noncoherent-detection/), such as FSK with envelope detectors, or [differential PSK](/differential-phase-shift-keying/), the detector outputs of the branches are added with equal weights. No phase estimate is needed, but the result is a different receiver with its own error rate.
- **Generalized selection.** Adding the best $L_c$ of $L$ branches with MRC or EGC lies between selection combining and full combining.

## When to use it

Use EGC when the branch phases can be tracked but the amplitudes are hard to estimate, or when a simple analog combiner is wanted, for example with phase shifters. In Rayleigh fading with branches of equal mean power, it is within about 0.5 to 0.7 dB of maximal ratio combining. With branches of very different mean power, use [maximal ratio combining](/maximal-ratio-combining/) or [selection combining](/selection-combining/) instead, because EGC adds the full noise of the weak branches.

## Pitfalls

- **Unequal noise powers.** EGC assumes the same $N_0$ on every branch. With different noise powers, scale each branch to the same noise level first, or use maximal ratio combining.
- **A dead branch.** A branch in a deep fade or with a failed receiver adds noise and almost no signal. EGC can then be worse than one good branch.
- **Phase errors.** EGC depends fully on the phase estimates. A phase error per branch reduces the signal sum by the cosine of the error.
- **The scale in line L3.** For amplitude-dependent formats such as 16-QAM, the estimate must be divided by $a$; omitting line L3 gives a wrong decision region.

## Implementations

## History

Brennan (1959) surveyed linear diversity combining, analyzed equal gain combining next to maximal ratio and selection combining, and showed that it comes close to maximal ratio combining in Rayleigh fading. Equal gain combining was attractive in early analog receivers because cophasing is easier to build than accurate gain weighting. Its error rates for more branches and for other fading models need numerical methods; Simon and Alouini (2005, Section 9.3) treat EGC over generalized fading channels.

## References
