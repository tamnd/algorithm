---
tag: HGVMCQ
kind: algorithm
slug: schmidl-cox-synchronization
name: Schmidl-Cox synchronization
aliases:
- Schmidl-Cox algorithm
area: communications/ofdm-and-multicarrier
level: core
summary: "Finds the start of an OFDM frame and its carrier frequency offset from a training symbol with two equal halves, and the even integer part of the offset from a second training symbol."
solves: [frequency-offset-estimation, frame-synchronization]
model: real-ram
complexity:
  vars: {N: the number of subcarriers, D: the number of candidate start positions, G: the number of integer offsets tried}
  time: {worst: O(D + N log N + G N)}
  space: {extra: O(N)}
properties: {deterministic: true, data_aided: true, timing_and_frequency: true}
history:
  year: 1997
  people: [Timothy M. Schmidl, Donald C. Cox]
  note: "Schmidl and Cox published the method in 1997 for wireless LAN bursts: one training symbol with two equal halves for the timing and the fractional offset, and a second one for the integer offset."
prereqs: [orthogonal-frequency-division-multiplexing, frequency-offset-estimation, data-aided-synchronization]
see_also: [moose-frequency-offset-estimator, van-de-beek-estimator, inter-carrier-interference, preamble-correlation-detection, frame-synchronization, kay-frequency-estimator, cramer-rao-bound, autocorrelation]
sources:
  - paper: doi:10.1109/26.650240
    title: "T. M. Schmidl and D. C. Cox, Robust frequency and timing synchronization for OFDM, IEEE Transactions on Communications 45(12), 1997"
    locator: "pages 1613 to 1621 (the training symbol with two identical halves, the timing metric and its plateau, the fractional offset from the angle of P, and the second training symbol for the integer offset)"
  - paper: doi:10.1109/26.328961
    title: "P. H. Moose, A technique for orthogonal frequency division multiplexing frequency offset correction, IEEE Transactions on Communications 42(10), 1994"
    locator: "pages 2908 to 2914 (the maximum likelihood offset estimate from a repeated symbol, the basis of the fractional estimate)"
  - paper: doi:10.1109/78.599949
    title: "J.-J. van de Beek, M. Sandell and P. O. Börjesson, ML estimation of time and frequency offset in OFDM systems, IEEE Transactions on Signal Processing 45(7), 1997"
    locator: "pages 1800 to 1805 (the blind alternative that uses the cyclic prefix instead of a training symbol)"
---

Schmidl-Cox synchronization finds where an OFDM burst starts and how far the receiver's carrier frequency is from the transmitter's, before the receiver can take any DFT. It needs a training symbol whose time samples are two equal halves, made by putting data only on the even subcarriers. The receiver correlates each half-length window of the input with the next one, $P(d) = \sum_m r[d+m]^* r[d+m+N/2]$, and normalizes it to $M(d) = |P(d)|^2 / R(d)^2$ with $R(d)$ the energy of the second half. $M$ rises to a plateau when the window lies on the training symbol, which gives the timing. On the plateau the angle of $P$ is $\pi\varepsilon$, which gives the offset $\varepsilon$ modulo 2, in units of the subcarrier spacing. A second training symbol, with a known pattern relative to the first, removes the remaining ambiguity $2g$. It is a data-aided method for the problems of [frame synchronization](/frame-synchronization/) and [frequency offset estimation](/frequency-offset-estimation/) in [OFDM](/orthogonal-frequency-division-multiplexing/). The [Moose estimator](/moose-frequency-offset-estimator/) uses two whole repeated symbols and assumes the timing is known; the [van de Beek estimator](/van-de-beek-estimator/) uses the cyclic prefix and needs no training symbol. The page uses $j$ for the imaginary unit, the unitary DFT pair of the OFDM page, and $\varepsilon = \Delta f\, N / f_s$.

## In plain words

A receiver that wakes up does not know where a burst begins, and its oscillator is slightly off, so every sample turns a little more than it should. The sender starts the burst with a block that repeats itself: the second half is a copy of the first half. The receiver slides a window along the signal and compares each half with the next half. When the window sits on the special block, the two halves match very well, apart from a fixed turn. The good match tells the receiver where the block is. The size of the turn between the halves tells it how far off its oscillator is. A turn can only be measured up to a full circle, so a second known block settles the rest.

## The problem

The input is a stream of complex baseband samples $r[i] = e^{j 2\pi \varepsilon i / N} (h * s)[i] + w[i]$, where $s$ holds a burst that starts with two training symbols, each with a cyclic prefix of $N_{cp}$ samples, $h$ is a channel with $L \le N_{cp} + 1$ taps, $\varepsilon$ is the unknown offset in subcarrier spacings and $w[i] \sim \mathcal{CN}(0, N_0)$. The SNR is the mean energy per sample divided by $N_0$. The first training symbol $X_1$ is zero on the odd subcarriers; the second, $X_2$, is known through the ratio $v[k] = X_2[k] / X_1[k]$ on the even subcarriers. Find a DFT start $\hat d$ inside the part of the first symbol that is free of interference from earlier samples, and an estimate $\hat\varepsilon$ of $\varepsilon$, with $|\varepsilon| < 1 + 2 g_{\max}$.

## The algorithm

```pseudo id=main
SCHMIDL-COX(r, N, N_cp, v, g_max)
L1  for d ← 0, 1, .. do                               ▷ P(0) and R(0) are direct sums over m = 0, .., N/2-1
L2      P(d) ← P(d-1) + conj(r[d-1+N/2]) r[d-1+N] - conj(r[d-1]) r[d-1+N/2]
L3      R(d) ← R(d-1) + |r[d-1+N]|² - |r[d-1+N/2]|²
L4      M(d) ← |P(d)|² / R(d)²
L5  d̂ ← argmax_d M(d)                                 ▷ or the middle of the starts with M ≥ 0.9 max M
L6  ε_f ← angle(P(d̂)) / π                              ▷ fractional part, in (-1, 1]
L7  z[i] ← r[i] e^(-j2π ε_f i / N) for all i           ▷ remove the fractional part
L8  Y1 ← F z[d̂ .. d̂+N-1];  Y2 ← F z[d̂+N+N_cp .. d̂+2N+N_cp-1]
L9  ĝ ← argmax over |g| ≤ g_max of |Σ_{k even} conj(Y1[k+2g] v[k]) Y2[k+2g]|² / (2 (Σ_{k even} |Y2[k]|²)²)
L10 return d̂, ε_f + 2ĝ
```

Lines L1 to L4 slide the window. Each step adds the newest product and drops the oldest one, so $P$ and $R$ cost $O(1)$ per start instead of $O(N)$. Line L4 normalizes by the energy, so the metric does not depend on the received power. Line L5 picks the timing. The paper of Schmidl and Cox averages the starts whose metric is within 90 percent of the maximum, because $M$ has a flat top over the excess prefix and its largest value is often at the edge; the implementation offers both rules. Line L6 reads the phase advance over half a symbol, $\pi\varepsilon$, so the result is $\varepsilon$ modulo 2. Line L7 removes this part. The rest of the offset is an even integer $2g$, which shifts the subcarriers by $2g$ positions without leakage. Line L8 takes the DFT of both training symbols at the same position in each symbol. Line L9 tries each shift: at the true shift, the products of line L9 all have the same phase and add up coherently, because $X_1 v = X_2$. Line L10 combines the two parts.

## Example

Take $N = 16$, $N_{cp} = 4$, a channel $h = (1, 0.5)$, six zero samples before the burst, $\varepsilon = 2.3$, random QPSK training symbols (seed 11) and no noise. The first symbol occupies samples 6 to 25, its body starts at sample 10, and the starts free of interference are $d = 7, \ldots, 10$, that is $N_{cp} - L + 2 = 4$ starts.

| $d$ | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| $M(d)$ (line L4) | 0.645 | 0.972 | 0.980 | 1 | 1 | 1 | 1 | 0.975 | 0.829 |
| $\angle P(d) / \pi$ | 0.328 | 0.323 | 0.323 | 0.3 | 0.3 | 0.3 | 0.3 | 0.296 | 0.306 |

Line L5 with the largest value finds $d = 7$, the first start of the plateau; the 90 percent rule takes the starts 5 to 11 and returns their middle, $\hat d = 8$. Line L6 gives $\varepsilon_f = 0.3$, which is $2.3$ modulo 2. After line L7 the remaining offset is $2$, so $g = 1$. Line L9 gives these values of the normalized metric for $g = -3, \ldots, 3$: $0.041$, $0.031$, $0.131$, $0.063$, $0.5$, $0.059$, $0.237$. The maximum $0.5$ is at $g = 1$, and line L10 returns $\hat\varepsilon = 0.3 + 2 = 2.3$.

At $E_s / N_0 = 10$ dB per sample with $N = 64$, $N_{cp} = 8$ and $\varepsilon = 2.12$ in white noise, the tests measure the following over 100 frames: the 90 percent rule puts the start inside the 9 starts free of interference in at least 90 frames, near the middle on average, and all 100 offset estimates are within $0.05$ of $\varepsilon$.

## Correctness

**Claim.** Without noise and with $N_{cp} \ge L - 1$: (a) $M(d) = 1$ and $\angle P(d) = \pi\varepsilon$ modulo $2\pi$ for each of the $N_{cp} - L + 2$ starts $d$ whose two half windows lie in the part of the first symbol that is free of interference; (b) for such a $\hat d$, line L9 attains its largest possible value $1/2$ at the true $g$. So the algorithm returns $\varepsilon$ exactly when $\hat d$ is on the plateau, $|g| \le g_{\max}$ and line L9 has no tie. This is a theorem in the model above.

**Key invariant.** On the plateau, the received samples are periodic with period $N/2$ apart from the offset factor: $r[i + N/2] = e^{j\pi\varepsilon} r[i]$. This holds because the training symbol has period $N/2$ and the cyclic prefix keeps the channel output circular.

Part (b) follows from the Cauchy-Schwarz inequality: at the true shift, all products have the same phase. With noise, the fractional estimate has the variance $\frac{1}{\pi^2 (N/2)\, \text{SNR}} (1 + \frac{1}{2\,\text{SNR}})$ at a high SNR, a closed form for a linearized phase error; the tests check it within 15 percent. The full proof is below.

## Complexity

Lines L1 to L4 cost $O(1)$ per start after an $O(N)$ start-up, so $D$ candidate starts cost $O(N + D)$. Line L5 is a scan, $O(D)$. Line L7 rotates $O(N)$ samples, line L8 is two FFTs, $O(N \log N)$, and line L9 costs $O(N)$ per candidate $g$, so $O(G N)$ for $G = 2 g_{\max} + 1$ candidates. The total is $O(D + N \log N + G N)$ time in the [real RAM](/real-ram/). A receiver that runs lines L1 to L4 on a stream keeps $N$ samples in a delay line, so the extra space is $O(N)$.

## Properties

- **Range.** The fractional estimate covers $|\varepsilon| < 1$, twice the range of an estimator that compares two full symbols, because the halves are only $N/2$ samples apart. The integer search extends the range to $|\varepsilon| < 1 + 2 g_{\max}$.
- **Robust to the channel.** The halves pass through the same channel, so $M$ and the angle of $P$ do not depend on $h$ on the plateau. Only the plateau gets shorter, by $L - 1$ starts.
- **Variance.** Near $\frac{1}{\pi^2 (N/2)\,\text{SNR}}$ at a high SNR: $3.32 \times 10^{-4}$ for $N = 64$ at 10 dB, a standard deviation of $0.018$ subcarrier spacings. This is 8 times the variance $\frac{1}{4\pi^2 N\,\text{SNR}}$ of the [Moose estimator](/moose-frequency-offset-estimator/) with two full symbols of $N$ samples, which correlates twice as many samples (a factor 2) spaced twice as far apart (a factor 4). The price of the Moose estimator is its range, $|\varepsilon| < 1/2$.
- **Timing is coarse.** The plateau makes the timing estimate uncertain by a few samples, which is acceptable because any start on the plateau works and the residual delay becomes a phase ramp that the channel estimate absorbs.
- **Blind to the data.** The training symbol is known only through its structure for lines L1 to L6; the known values are used only in line L9.

## Variants and improvements

- **Normalize by both halves.** Using $R(d) = \frac12 \sum_m (|r[d+m]|^2 + |r[d+m+N/2]|^2)$ keeps $M(d) \le 1$ everywhere, by the Cauchy-Schwarz inequality and the inequality of the arithmetic and geometric means, so the maximum is on the plateau.
- **Sharper timing.** Training symbols with more than two parts, some of them negated, give a metric with a sharp peak instead of a plateau, at the cost of a smaller range.
- **Fine timing after the coarse step.** A cross-correlation with the known training symbol, as in [preamble correlation detection](/preamble-correlation-detection/), or the channel estimate itself, refines the start.
- **Integer offset from a pilot pattern.** Instead of a second training symbol, the receiver can correlate the DFT output with a known pilot pattern over the candidate shifts.
- **Repeated short symbols.** IEEE 802.11a starts its burst with ten repetitions of a short symbol; the same delay-and-correlate idea with a shorter lag gives detection and a coarse offset with a larger range.

## When to use it

Use Schmidl-Cox when an OFDM receiver must find bursts and correct large offsets quickly from a preamble, as in wireless LAN and other packet systems, and when one or two symbols of training are affordable. Use the [van de Beek estimator](/van-de-beek-estimator/) for a continuous OFDM stream without a preamble, as in broadcasting. Use the [Moose estimator](/moose-frequency-offset-estimator/) when the timing is already known and the offset is less than half a spacing, to get a smaller variance.

## Pitfalls

- **Taking the maximum of M as the timing.** With $R(d)$ the energy of the second half only, $M(d)$ can be larger than 1 next to the plateau (the tests see $1.02$), so line L5 with the plain maximum can land just outside the starts free of interference. Use the middle of the 90 percent region in line L5, or normalize by both halves in line L3.
- **A lag that is not N/2.** Line L2 must compare samples $N/2$ apart, matching the period of the training symbol. A training symbol with data on the odd subcarriers too has no period $N/2$, and $M$ never reaches its plateau.
- **Reading the angle as epsilon.** Line L6 must divide the angle by $\pi$, not $2\pi$: the halves are half a symbol apart, so the phase advance is $\pi\varepsilon$.
- **Forgetting the wrap.** The fractional estimate is only $\varepsilon$ modulo 2. For $\varepsilon = 2.3$ line L6 gives $0.3$, and without line L9 the receiver keeps an offset of two subcarriers, which renames every subcarrier and makes every decision wrong.
- **Shifting the wrong way.** In line L9, the indices are $k + 2g$ for both symbols; comparing $Y_1[k]$ with $Y_2[k + 2g]$ looks for a shift between the symbols, which does not exist.
- **Both DFT windows at different positions.** Line L8 must take the second window exactly $N + N_{cp}$ samples after the first, so that the timing phase ramp is the same in both and cancels in line L9.

## Implementations

## History

Timothy Schmidl and Donald Cox at Stanford published the method in 1997, aiming at fast acquisition of bursts in wireless LANs. They built on the idea of Moose, who in 1994 had derived the maximum likelihood estimate of the offset from two repeated symbols, and moved the repetition inside a single symbol to widen the range and to get the timing from the same correlation. The same year, van de Beek, Sandell and Börjesson gave a blind method from the cyclic prefix. The delay-and-correlate structure of Schmidl-Cox is still the usual first step of OFDM packet receivers.

## References
