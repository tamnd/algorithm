---
tag: SDKX4V
kind: algorithm
slug: fractionally-spaced-equalizer
name: Fractionally spaced equalizer
aliases:
- "T/2-spaced equalizer"
area: communications/channel-estimation-and-equalization
level: core
summary: "A linear equalizer with taps spaced T/2 (or T/L_s) apart and one output per symbol. It is insensitive to the sampling phase, and a finite FIR filter can remove the ISI exactly."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of equalizer taps, L: the number of pulse samples, K: the number of symbols}
  time: {worst: O(N^2 (N + L) + K N)}
  space: {extra: O(N (N + L))}
properties: {deterministic: true, linear: true, samples_per_symbol: 2, needs_noise_level: true, insensitive_to_sampling_phase: true, biased: true}
history:
  year: 1976
  people: [Gottfried Ungerboeck]
  note: "Ungerboeck analyzed the equalizer with fractional tap spacing, showed that it does not depend on the sampling phase, and drew the consequences for clock recovery in data modems."
prereqs: [channel-equalization, mmse-linear-equalizer, sampling-theorem]
see_also: [zero-forcing-equalizer, decision-feedback-equalizer, adaptive-equalization, root-raised-cosine-filter, raised-cosine-filter, blind-equalization, subspace-channel-identification, gardner-timing-error-detector]
sources:
  - paper: "Gottfried Ungerboeck, Fractional tap-spacing equalizer and consequences for clock recovery in data modems, IEEE Transactions on Communications 24(8), 1976, pages 856 to 864"
    locator: "the insensitivity of the fractionally spaced equalizer to the sampling phase"
  - paper: "R. D. Gitlin and S. B. Weinstein, Fractionally-spaced equalization: an improved digital transversal equalizer, Bell System Technical Journal 60(2), 1981, pages 275 to 296"
    locator: "the performance of the T/2 equalizer against the symbol-spaced equalizer"
  - paper: doi:10.1109/79.489269
    title: "J. R. Treichler, I. Fijalkow and C. R. Johnson, Fractionally spaced equalizers: how long should they really be?, IEEE Signal Processing Magazine 13(3), 1996, pages 65 to 81"
    locator: "the length of a fractionally spaced equalizer"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.4-4 (fractionally spaced equalizers)"
---

A fractionally spaced equalizer (FSE) is a linear equalizer whose input is sampled faster than the symbol rate, usually at $L_s = 2$ samples per symbol, so its taps are $T/2$ apart. It still gives one output per symbol. A symbol-spaced equalizer works on samples taken at $kT + \tau$, after a [matched filter](/matched-filter/), and the result depends on the phase $\tau$: at a bad phase the aliased parts of the spectrum cancel and leave a null that no equalizer can fill. At $T/2$, a pulse with less than 100 percent excess bandwidth, such as a [root raised cosine](/root-raised-cosine-filter/) pulse, does not alias, so the FSE sees the whole signal and can form the matched filter and the equalizer in one filter, whatever the phase. The design here is the MMSE design of the [MMSE linear equalizer](/mmse-linear-equalizer/), applied to the polyphase model at $L_s = 2$. It has a second gift: the two sample phases act as two channels, and if they have no common zero, a finite FIR filter removes the ISI exactly, which a symbol-spaced FIR filter can never do. The same fact makes [blind identification](/subspace-channel-identification/) from second-order statistics possible.

## In plain words

A receiver that samples once per symbol must sample at the right instant. If it samples between the right instants, parts of the signal fold onto each other and can cancel, and then the equalizer has nothing to work with. A fractionally spaced equalizer takes two samples per symbol instead. Two samples per symbol are enough to describe the received pulse completely, so no information is lost at any sampling instant, and a shift in time is just a different set of weights. The equalizer combines the samples of both phases and still outputs one value per symbol. It costs about twice as many taps for the same time span. Its weights are found in the same way as for the MMSE equalizer.

## The problem

The input is the sampled pulse $p = (p[0], \ldots, p[L_p - 1])$ at $L_s$ samples per symbol, which includes the transmit filter, the channel and the sampling phase, normalized so that $\sum |p|^2 = 1$; the noise power $N_0$ per sample; the symbol energy $E_s$; the number of taps $N_f$; and the delay $\Delta$. The samples are $y[m] = \sum_k x[k]\, p[m - L_s k] + w[m]$, with $w[m] \sim \mathcal{CN}(0, N_0)$ independent from sample to sample. This page uses $L_s = 2$, the case of the alias. The output is the tap vector $c$ that minimizes $J = E|z[k] - x[k - \Delta]|^2$ for the output $z[k] = \sum_{i=0}^{N_f-1} c_i\, y[L_s k - i]$, computed once per symbol, and the minimum $J$.

The last $N_f$ samples $u = (y[L_s k], \ldots, y[L_s k - N_f + 1])^T$ satisfy $u = H s + v$, where $s = (x[k], \ldots, x[k - Q + 1])^T$ and $H_{ij} = p[L_s j - i]$. Each row of $H$ shifts by one sample, but each column by $L_s$ samples, so $H$ is a block Toeplitz matrix, not a Toeplitz one.

## The algorithm

```pseudo id=main
FSE-MMSE(p, L_s, N_f, Δ, N0, Es)
L1  Q ← ⌊(L_p + N_f - 2) / L_s⌋ + 1                         ▷ the symbols that reach the taps
L2  H[i][j] ← p[L_s j - i]  for 0 ≤ i < N_f, 0 ≤ j < Q        ▷ p[t] = 0 outside 0 .. L_p - 1
L3  R ← Es H Hᴴ + N0 I
L4  r ← Es H e_Δ
L5  f ← R⁻¹ r
L6  c ← conj(f)                                              ▷ z[k] = Σ c[i] y[L_s k - i]
L7  J ← Es - rᴴ f
L8  return c, J
```

Line L1 counts the symbols that touch the $N_f$ samples in the window. Line L2 is the polyphase convolution matrix: row $i$ holds the pulse samples that link sample $L_s k - i$ to each symbol. Lines L3 to L7 are the Wiener solution of the MMSE equalizer. The only change from the symbol-spaced equalizer is the stride $L_s$ in line L2 and the decimation of the output: the filter runs at the sample rate, but only every $L_s$-th output is computed. With $L_s = 1$ the algorithm is the MMSE linear equalizer. To pick the delay, the implementation computes all $Q$ values of $J$ from one inverse of $E_s H^H H + N_0 I$ and keeps the smallest.

## Example

**Exact zero forcing.** Take $L_s = 2$ and the pulse $p = (1, 0.5, 0.5, 1)/\sqrt{2.5}$. Its even samples form the subchannel $(1, 0.5)$ and its odd samples the subchannel $(0.5, 1)$, up to the factor $1/\sqrt{2.5}$; their zeros are at $-0.5$ and $-2$, so they share none. With $N_f = 4$, $\Delta = 1$ and $N_0 = 0$:

| | index 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| taps $c \cdot (1/\sqrt{2.5})$ | 0 | -2/3 | 4/3 | 0 |
| combined response $g = H^T c$ | 0 | 1 | 0 | 0 |

Check $g_1 = c_1 p[1] + c_2 p[0] = \sqrt{2.5}(-\tfrac{2}{3} \cdot \tfrac{0.5}{\sqrt{2.5}} + \tfrac{4}{3} \cdot \tfrac{1}{\sqrt{2.5}}) = 1$ and $g_2 = c_1 p[3] + c_2 p[2] = -\tfrac{2}{3} + \tfrac{2}{3} = 0$. The ISI is gone with two nonzero taps, a span of one symbol, and $J = 0$. A symbol-spaced equalizer on one phase, the channel $(1, 0.5)/\sqrt{2.5}$, with 2 taps (the same span) has at best $J = 1/21 = 0.0476$ even without noise, and no finite length brings it to 0. At $N_0 = 0.1$ the FSE gives $J = 0.244$ with 4 taps, 0.153 with 8 and 0.133 with 16.

**The sampling phase.** Take a root raised cosine pulse with roll-off 0.35, truncated to 8 symbols on each side, and $E_s/N_0 = 20$ dB. The symbol-spaced MMSE equalizer has 15 taps after the matched filter, on the raised cosine samples $\mathrm{rc}(kT + \tau)$. The FSE has 30 taps at $T/2$, on the samples $\mathrm{rrc}(mT/2 - \tau)$, normalized. Both use their best delay. The unbiased SINR $E_s/J - 1$ is:

| phase $\tau$ | 0 | $T/4$ | $T/2$ |
|---|---|---|---|
| symbol-spaced, 15 taps | 20.00 dB | 19.41 dB | 11.16 dB |
| FSE at $T/2$, 30 taps | 20.00 dB | 20.00 dB | 20.00 dB |

At 10 dB the same rows are 10.00, 9.44 and 6.89 dB against 10.00 dB at every phase. At $\tau = T/2$ the folded spectrum of the symbol-spaced samples is zero at half the symbol rate, so the symbol-spaced equalizer loses 8.8 dB at 20 dB SNR. The FSE reaches the matched filter bound $E_s/N_0$ at every phase.

## Correctness

**Claim.** Lines L5 to L7 give the unique taps that minimize $J$ over all $N_f$-tap filters at $L_s$ samples per symbol, and the minimum $J$. At $L_s = 2$, if the even and odd subchannels have no common zero and each phase has enough taps, the FSE removes the ISI exactly, so with $N_0 = 0$ it reaches $J = 0$.

**Key step.** The samples in the window are $u = H s + v$ with $H_{ij} = p[L_s j - i]$, so the problem is the same Wiener problem as for the MMSE linear equalizer, and completing the square gives the solution. For exact zero forcing, split the taps by phase: $G(\zeta) = C_0(\zeta) A(\zeta) + C_1(\zeta) B(\zeta)$, where $A$ and $B$ are the subchannels. If $A$ and $B$ have no common root, the map $(C_0, C_1) \mapsto C_0 A + C_1 B$ on polynomials of degrees less than $\deg B$ and $\deg A$ is one to one, so it reaches $\zeta^\Delta$. This is the Bezout identity of the [extended Euclidean algorithm](/extended-euclidean-algorithm/); its matrix is the [Sylvester matrix](/sylvester-matrix/), nonsingular when the [resultant](/resultant/) is not zero. The full proof, with the folded spectrum null at $\tau = T/2$, is in the proofs folder. The phase insensitivity of a long FSE is cited from Ungerboeck and from Gitlin and Weinstein and checked numerically.

## Complexity

Line L3 costs $O(N_f^2 Q)$ operations with $Q \approx (L_p + N_f)/L_s$, line L5 costs $O(N_f^3)$, and lines L4, L6 and L7 cost $O(N_f)$, once per channel and delay. With $N = N_f$ and $L = L_p$, this is $O(N^2 (N + L))$ in the [real RAM](/real-ram/). Filtering costs $N_f$ complex multiplications per symbol, since only one output per symbol is computed, so $K$ symbols cost $O(N^2 (N + L) + K N)$ in total, with $O(N (N + L))$ extra space. For the same time span, the FSE has $L_s$ times as many taps as a symbol-spaced equalizer, so its cost per symbol is $L_s$ times higher, and its design is about $L_s^3$ times higher.

## Properties

- **Insensitive to the sampling phase.** At $L_s = 2$ and an excess bandwidth below 100 percent, the samples do not alias, and a long FSE gives the same MSE at every phase, as in the table above.
- **Matched filter included.** The FSE can realize the matched filter and the equalizer in one filter, so the receive filter before it only has to reject the noise outside the band.
- **Exact zero forcing with a finite filter.** If the two phases share no zero, a finite FSE removes the ISI exactly; the needed length is at least the degree of the other phase, per phase.
- **Biased.** As for every MMSE design, $E[z \mid x] = (1 - J/E_s)\, x$.
- **The noise per sample.** With $\sum |p|^2 = 1$ and noise $N_0$ per sample, the matched filter bound is $E_s/N_0$, the same as for the symbol-spaced model after a matched filter, so the two can be compared directly.
- **Not unique when too long.** If $N_f$ exceeds the number of symbols in its window, $H H^H$ is singular, and with $N_0 = 0$ many tap vectors give the same output; see the pitfalls.

## Variants and improvements

- **Other oversampling factors.** $L_s = 3/2$ or $4/3$ samples per symbol is enough when the excess bandwidth is small, and costs fewer taps; $L_s = 4$ or 8 is used when the same samples also feed the timing recovery.
- **Adaptive FSE.** The [LMS algorithm](/lms-algorithm/) adapts the taps from training or decisions, with one update per symbol; see [adaptive equalization](/adaptive-equalization/). A small tap leakage keeps the taps bounded.
- **Blind FSE.** The [constant modulus algorithm](/constant-modulus-algorithm/) is often run on a fractionally spaced equalizer, and the second-order statistics at $T/2$ identify the channel, as in the [Tong-Xu-Kailath method](/tong-xu-kailath-identification/); see [blind equalization](/blind-equalization/).
- **Fractionally spaced DFE.** A [decision feedback equalizer](/decision-feedback-equalizer/) with a fractionally spaced feedforward filter and a symbol-spaced feedback filter combines both gains.
- **Timing recovery.** Because the FSE does not care about the phase, the timing loop, such as the [Gardner detector](/gardner-timing-error-detector/), only has to track the symbol rate, not lock to a precise phase.

## When to use it

Use an FSE when the sampling phase is not known or drifts, when the pulse has a significant excess bandwidth, or when the equalizer must also act as the matched filter. It is the usual choice in modems with an adaptive equalizer. Use a symbol-spaced equalizer when a matched filter and an accurate timing loop are already in place and the cost of extra taps matters, and use [frequency-domain equalization](/frequency-domain-equalization/) for long channels in block systems.

## Pitfalls

- **Tap drift.** When $N_f$ is larger than the number of symbols in the window, the out-of-band part of the input has no signal, and an adaptive FSE without leakage can let its taps grow there until they overflow. Add a small leakage or a small $N_0$ in the design.
- **The noise model.** The noise must be white at the sample rate for the formulas here. A narrow receive filter before the FSE colors the noise; then replace $N_0 I$ by the noise covariance.
- **Mixing conventions.** The pulse is normalized to $\sum |p|^2 = 1$ at $L_s$ samples per symbol, not $\sum |p|^2 = L_s$. With the wrong normalization the SNR is off by $10 \log_{10} L_s$ dB.
- **Common zeros.** If the two phases share a zero, for example when the pulse is a symbol-spaced pulse with zeros inserted, the FSE is no better than a symbol-spaced equalizer, and with $N_0 = 0$ the system is singular.
- **The output rate.** Only one output per symbol is used. Computing all outputs and then dropping half of them doubles the cost for nothing.

## Implementations

## History

Ungerboeck's 1976 paper analyzed the equalizer with fractional tap spacing and showed that its performance does not depend on the sampling phase, which simplifies the clock recovery. Gitlin and Weinstein compared the $T/2$ equalizer with the symbol-spaced one in 1981. In the 1990s, the view of the $T/2$ samples as two channels led to blind identification from second-order statistics, and Treichler, Fijalkow and Johnson asked in 1996 how long a fractionally spaced equalizer should be.

## References
