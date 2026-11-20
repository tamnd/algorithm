---
tag: 6JQ8CA
kind: algorithm
slug: moose-frequency-offset-estimator
name: Moose frequency offset estimator
aliases:
- repeated-symbol CFO estimator
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Estimates the OFDM carrier frequency offset from the phase change between two repeated symbols, in the frequency domain. It is the maximum likelihood estimate for white noise."
solves: [frequency-offset-estimation]
model: real-ram
complexity:
  vars: {N: the number of subcarriers}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, data_aided: true, maximum_likelihood: true, exact_without_noise: true}
history:
  year: 1994
  people: [Paul H. Moose]
  note: "Moose derived the maximum likelihood estimate of the frequency offset from two repeated OFDM symbols and showed that it can be computed after the DFT, where the interference between subcarriers is the same in both symbols."
prereqs: [orthogonal-frequency-division-multiplexing, frequency-offset-estimation, maximum-likelihood-estimation, data-aided-synchronization]
see_also: [schmidl-cox-synchronization, van-de-beek-estimator, inter-carrier-interference, kay-frequency-estimator, carrier-recovery, cramer-rao-bound, preamble-correlation-detection, autocorrelation]
sources:
  - paper: doi:10.1109/26.328961
    title: "P. H. Moose, A technique for orthogonal frequency division multiplexing frequency offset correction, IEEE Transactions on Communications 42(10), 1994"
    locator: "pages 2908 to 2914 (the repeated symbol, the maximum likelihood estimate of the offset from the phase of the correlation after the DFT, and its range)"
  - paper: doi:10.1109/26.650240
    title: "T. M. Schmidl and D. C. Cox, Robust frequency and timing synchronization for OFDM, IEEE Transactions on Communications 45(12), 1997"
    locator: "pages 1613 to 1621 (the repetition inside one symbol, which widens the range of the offset estimate)"
---

The Moose estimator finds the carrier frequency offset of an [OFDM](/orthogonal-frequency-division-multiplexing/) receiver from a training block that the transmitter sends twice. A carrier offset of $\varepsilon$ subcarrier spacings turns every sample by $e^{j 2\pi\varepsilon i / N}$, so the second copy, which starts $N + G$ samples later, arrives turned by the angle $\phi = 2\pi\varepsilon (N + G) / N$ relative to the first. The receiver takes the DFT of both copies, multiplies each subcarrier of the second copy by the conjugate of the same subcarrier of the first, adds up the products into $C$, and returns $\hat\varepsilon = \angle C \cdot N / (2\pi (N + G))$. The offset also causes [inter-carrier interference](/inter-carrier-interference/), but the interference is the same in both copies apart from the factor $e^{j\phi}$, so the estimate is exact without noise even though each DFT output is disturbed. Moose showed that this is the maximum likelihood estimate in white Gaussian noise. It is a data-aided method for [frequency offset estimation](/frequency-offset-estimation/), and the timing must be known. The page uses $j$ for the imaginary unit and the unitary DFT pair of the OFDM page.

## In plain words

The sender transmits the same block twice. If the receiver's oscillator is slightly off, every sample turns a little, and the turn builds up over time. So the second copy looks exactly like the first, only turned by an angle that grows with the offset and with the time between the copies. The receiver compares each part of the second copy with the same part of the first, measures the turn, and adds all the comparisons together, so strong parts count more than weak ones. The angle of the total is the turn, and the turn divided by the time between the copies is the frequency offset.

## The problem

The input is two windows of $N$ received samples, $y_1$ and $y_2$, the second starting $N + G$ samples after the first, where the transmitter sent the same block in both, each preceded by a cyclic prefix that covers the channel (with $G = 0$ the first copy serves as the prefix of the second). The model is $r[i] = e^{j 2\pi\varepsilon i / N} (h * s)[i] + w[i]$ with an unknown channel $h$, an unknown offset $\varepsilon$ and white noise $w[i] \sim \mathcal{CN}(0, N_0)$. Estimate $\varepsilon$, given $|\varepsilon| < N / (2(N + G))$.

## The algorithm

```pseudo id=main
MOOSE(y1, y2, G)
L1  Y1 ← F y1;  Y2 ← F y2                       ▷ DFT of both copies
L2  C ← Σ_k conj(Y1[k]) Y2[k]
L3  return angle(C) N / (2π (N + G))
```

Line L1 takes the DFT of the two windows. Line L2 forms the correlation. Each product $Y_1[k]^* Y_2[k]$ is $e^{j\phi} |Y_1[k]|^2$ without noise, so all products have the same angle, and the sum weights each subcarrier by its power. Line L3 turns the angle into an offset: the second copy is $N + G$ samples later, and an offset of one spacing turns one sample by $2\pi / N$. By the Plancherel identity, $C$ also equals $\sum_n y_1[n]^* y_2[n]$, so a receiver can skip line L1 and correlate in the time domain; the implementation offers both.

## Example

Take $N = 8$ and $G = 2$, with a prefix of 2 samples before each copy, random 4-QAM values on the subcarriers (seed 7), the channel $h = (1, 0.5)$, $\varepsilon = 0.17$ and noise with $N_0 = 0.1$ per sample. The true angle is $\phi = 2\pi \cdot 0.17 \cdot 10 / 8 = 1.335$ rad.

| $k$ | $Y_1[k]$ | $Y_2[k]$ | $Y_1[k]^* Y_2[k]$ | angle (rad) | offset from this $k$ alone |
|---|---|---|---|---|---|
| 0 | $-1.453 + 0.008j$ | $-0.493 - 1.159j$ | $0.707 + 1.687j$ | 1.174 | 0.149 |
| 1 | $-0.457 + 0.359j$ | $-1.057 - 0.848j$ | $0.179 + 0.767j$ | 1.342 | 0.171 |
| 2 | $0.822 + 1.074j$ | $-1.054 + 1.156j$ | $0.374 + 2.082j$ | 1.393 | 0.177 |
| 3 | $-0.438 + 0.173j$ | $-0.573 + 0.044j$ | $0.258 + 0.080j$ | 0.301 | 0.038 |
| 4 | $0.322 + 0.610j$ | $-0.548 + 0.471j$ | $0.111 + 0.486j$ | 1.347 | 0.171 |
| 5 | $0.555 + 0.332j$ | $-0.419 + 0.907j$ | $0.069 + 0.642j$ | 1.463 | 0.186 |
| 6 | $-1.221 - 0.113j$ | $-0.125 - 1.068j$ | $0.274 + 1.290j$ | 1.362 | 0.173 |
| 7 | $-0.229 + 1.748j$ | $-1.537 + 0.149j$ | $0.614 + 2.652j$ | 1.343 | 0.171 |

Line L2 gives $C = 2.585 + 9.687j$ with the angle $1.310$ rad, and line L3 returns $\hat\varepsilon = 1.310 \cdot 8 / (2\pi \cdot 10) = 0.1668$, an error of $0.003$. Subcarrier 3 is weak, its product is small, and its bad angle has little weight in the sum; the plain mean of the eight offsets in the last column is $0.155$, a larger error.

## Correctness

**Claim.** Without noise, if the prefixes cover the channel and $|\varepsilon| < N / (2(N + G))$, the algorithm returns $\varepsilon$ exactly. With white Gaussian noise and the transmitted block unknown, it is the joint maximum likelihood estimate of the offset. Both are theorems in the model above.

**Key invariant.** Without noise, $y_2 = e^{j\phi} y_1$ sample by sample, because the channel output of each copy depends only on that copy and its prefix. The DFT is linear, so $Y_2 = e^{j\phi} Y_1$ on every subcarrier, including the inter-carrier interference.

Then $C = e^{j\phi} \sum_k |Y_1[k]|^2$, whose angle is $\phi$. For the likelihood, the best block for a fixed $\phi$ is the midpoint of $Y_1$ and $e^{-j\phi} Y_2$, and what remains to maximize is $\operatorname{Re}(e^{-j\phi} C)$. At a high SNR, the variance is $\left( \frac{N}{2\pi (N + G)} \right)^2 \frac{N_0}{E} (1 + \frac{N N_0}{2E})$ for a block of energy $E$, a closed form for a linearized phase error. The full proof is below.

## Complexity

Line L1 is two FFTs, $O(N \log N)$ time, and line L2 is $O(N)$. The correlation in the time domain needs only $O(N)$ time. Either way the extra space is $O(N)$ for the two windows in the [real RAM](/real-ram/).

## Properties

- **Range.** $|\varepsilon| < N / (2(N + G))$: $1/2$ for two copies back to back and $0.4$ for $G = N/4$. A larger offset wraps, so $0.6$ is read as $-0.4$ for $G = 0$, as the tests check.
- **Variance.** For $G = 0$, close to $\frac{1}{4\pi^2 N\,\text{SNR}} (1 + \frac{1}{2\,\text{SNR}})$ at a high SNR, which is $1.66 \times 10^{-4}$ for $N = 16$ at 10 dB. A larger $G$ lowers the variance by the factor $(N / (N + G))^2$ but shrinks the range by $N / (N + G)$.
- **Robust to the channel.** The channel only changes the weights $|Y_1[k]|^2$, not the angle, so no channel estimate is needed.
- **Weighting.** Strong subcarriers count more than weak ones, as the maximum likelihood estimate requires; averaging the angles of single subcarriers is worse, as in the example.
- **Needs the timing.** The windows must lie on the copies, inside the part free of interference from earlier symbols.

## Variants and improvements

- **Repetition inside one symbol.** [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) uses a symbol with two equal halves, $N/2$ samples apart, which doubles the range to $|\varepsilon| < 1$ and also gives the timing, at a larger variance.
- **More copies.** With $K$ short repetitions, the correlations at lags $1, 2, \ldots$ copies can be combined, trading range and variance; the short training field of IEEE 802.11a repeats a block of 16 samples ten times.
- **Integer part.** For offsets beyond the range, a second step searches the integer shift of the subcarriers against a known pattern, as Schmidl and Cox do with their second training symbol.
- **Blind estimation.** Without training, the [van de Beek estimator](/van-de-beek-estimator/) uses the cyclic prefix as a short repetition, with a larger variance.

## When to use it

Use the Moose estimator when the transmitter can send a repeated training block and the timing is known, for example as the fine step after a coarse search, or when the offset is known to be below half a spacing. For the same SNR, it has a smaller variance than Schmidl-Cox with half symbols or van de Beek with the prefix, because it correlates more samples over a longer lag. For a large initial offset, start with [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) or a short repeated preamble, and for a stream without training use the [van de Beek estimator](/van-de-beek-estimator/).

## Pitfalls

- **The wrong scale in line L3.** The angle covers the full distance between the copies, so line L3 must multiply by $N / (2\pi (N + G))$. Dividing by $2\pi$ alone is correct only for $G = 0$.
- **Conjugating the wrong copy.** Line L2 must use $\operatorname{conj}(Y_1[k]) Y_2[k]$. With $Y_1[k] \operatorname{conj}(Y_2[k])$ the sign of the estimate flips.
- **Windows not one copy apart.** Line L1 must take $y_2$ exactly $N + G$ samples after $y_1$, and both inside the copies. A window that starts in the wrong place sees different data in the two copies, and the products no longer share one angle.
- **Averaging angles.** Line L2 must add the complex products before line L3 takes the angle. Taking the angle of each product first and averaging gives weak subcarriers too much weight, and it breaks when the angles are near $\pm\pi$.
- **Ignoring the range.** An offset outside $|\varepsilon| < N / (2(N + G))$ wraps in line L3 with no warning. A coarse estimate with a wider range must come first.

## Implementations

## History

Paul H. Moose, at the Naval Postgraduate School, published the estimator in IEEE Transactions on Communications in 1994. He showed that the offset can be estimated after the DFT from a repeated symbol, derived the maximum likelihood estimate, and studied its accuracy. With whole symbols, the range is limited to half a subcarrier spacing. Schmidl and Cox later moved the repetition inside one symbol to widen the range and to get the timing from the same correlation, and the repeated preamble became the usual training for OFDM packet systems.

## References
