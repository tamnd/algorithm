---
tag: 3R84JE
kind: algorithm
slug: common-phase-error-correction
name: Common phase error correction
aliases:
- CPE correction
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Estimates from pilot subcarriers the rotation that phase noise gives to all subcarriers of an OFDM symbol, and removes it before the one-tap equalizer."
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of subcarriers, P: the number of pilot subcarriers}
  time: {worst: O(N + P)}
  space: {extra: O(N)}
properties: {deterministic: true, data_aided: true, exact_for_constant_phase: true, removes_ici: false}
history:
  year: 1995
  people: [Patrick Robertson, Stefan Kaiser]
  note: "Robertson and Kaiser analyzed how phase noise in OFDM splits into a rotation common to all subcarriers and interference between subcarriers."
prereqs: [orthogonal-frequency-division-multiplexing, inter-carrier-interference, pilot-symbol-assisted-modulation]
see_also: [comb-pilot-channel-estimation, phase-locked-loop, decision-directed-carrier-recovery, frequency-offset-estimation, schmidl-cox-synchronization, two-dimensional-wiener-pilot-interpolation, iq-imbalance-compensation, channel-equalization]
sources:
  - paper: doi:10.1109/ICC.1995.524481
    title: "P. Robertson and S. Kaiser, Analysis of the effects of phase-noise in orthogonal frequency division multiplex (OFDM) systems, IEEE International Conference on Communications (ICC), 1995"
    locator: "pages 1652 to 1657 (the split of phase noise into a common phase error and inter-carrier interference)"
  - paper: doi:10.1109/11.948268
    title: "A. Garcia Armada, Understanding the effects of phase noise in orthogonal frequency division multiplexing (OFDM), IEEE Transactions on Broadcasting 47(2), 2001"
    locator: "pages 153 to 159 (the common phase error and the inter-carrier interference from phase noise)"
  - paper: doi:10.1109/26.380034
    title: "T. Pollet, M. Van Bladel and M. Moeneclaey, BER sensitivity of OFDM systems to carrier frequency offset and Wiener phase noise, IEEE Transactions on Communications 43(2/3/4), 1995"
    locator: "pages 191 to 193 (the SNR degradation caused by Wiener phase noise)"
---

Common phase error correction removes the part of oscillator phase noise that an [OFDM](/orthogonal-frequency-division-multiplexing/) receiver can remove cheaply. Phase noise $\varphi[n]$ multiplies time sample $n$ by $e^{j\varphi[n]}$. After the DFT, every subcarrier is scaled by the same complex factor $I_0$, the mean of $e^{j\varphi[n]}$ over the symbol, and receives some [inter-carrier interference](/inter-carrier-interference/) from the others. The angle of $I_0$ is the common phase error (CPE). It changes from symbol to symbol, so the channel estimate of an earlier symbol does not include it. The receiver knows the pilot values $X_p$ and the channel $H[p]$, so it adds up $Y[p] (H[p] X_p)^*$ over the pilots, takes the angle of the sum, and rotates every subcarrier back by it before the one-tap equalizer. A constant phase is removed exactly; for slowly varying phase noise most of the error is removed, and the interference part, of power $1 - |I_0|^2$, stays. The page uses $j$ for the imaginary unit and the unitary DFT pair of the OFDM page.

## In plain words

The local oscillator of a receiver does not hold a perfectly steady phase; it wanders a little all the time. Over one OFDM symbol, most of that wander acts as one twist of the whole symbol: every subcarrier is turned by the same angle. The rest smears a little energy between subcarriers. The twist alone would make many decisions wrong, but it is easy to fix. A few subcarriers carry known pilots, so the receiver checks how far they have turned, averages that over the pilots, and turns the whole symbol back. The smear cannot be fixed this way, but it is small when the oscillator is good.

## The problem

The input is one received OFDM symbol after the DFT, $Y[0], \ldots, Y[N-1]$, the channel $H[k]$ on every subcarrier (known from an earlier estimate), and the pilot subcarriers $p \in \mathcal P$ with their known values $X_p$. The model is $Y[k] = I_0 H[k] X[k] + \sum_{m \ne k} I_{k - m} H[m] X[m] + W[k]$ with $I_q = \frac1N \sum_n e^{j\varphi[n]} e^{-j 2\pi q n / N}$, an unknown phase noise $\varphi[n]$ and white noise $W[k] \sim \mathcal{CN}(0, N_0)$. Output the equalized values $Z[k] = Y[k] e^{-j\hat\varphi} / H[k]$, with $\hat\varphi$ an estimate of $\angle I_0$.

## The algorithm

```pseudo id=main
CPE-CORRECT(Y, H, pilots, X_p)
L1  C ← Σ_{p in pilots} Y[p] conj(H[p] X_p)
L2  φ̂ ← angle(C)
L3  Z[k] ← Y[k] e^(-j φ̂) / H[k]  for k = 0, .., N-1
L4  return Z
```

Line L1 correlates the received pilots with what they would be without phase noise. Each term is $I_0 |H[p] X_p|^2$ plus interference and noise, so all terms point in the direction of $I_0$, weighted by the pilot power. Line L2 takes the angle. Line L3 rotates every subcarrier back and divides by the channel. The pilots in line L1 are the same kind as those used for [comb pilot channel estimation](/comb-pilot-channel-estimation/); 802.11a, for example, sends four pilot subcarriers in every symbol for this kind of phase tracking.

## Example

Take $N = 16$, pilots on subcarriers 2, 6, 10, 14, the channel taps $(0.9, 0.3j, -0.2)$, random 4-QAM values (seed 4), no noise, and Wiener phase noise that starts at $0.6$ rad with steps of variance $0.004$ per sample. Over the symbol, $\varphi[n]$ moves between $0.60$ and $0.81$ rad, and $I_0 = 0.776 + 0.628j$, with $|I_0| = 0.998$ and the angle $0.680$ rad.

| pilot $p$ | $\lvert H[p] X_p\rvert^2$ | $Y[p]\, (H[p] X_p)^*$ | angle (rad) |
|---|---|---|---|
| 2 | 1.407 | $1.021 + 0.921j$ | 0.734 |
| 6 | 1.407 | $1.079 + 0.919j$ | 0.706 |
| 10 | 0.473 | $0.362 + 0.260j$ | 0.622 |
| 14 | 0.473 | $0.352 + 0.325j$ | 0.745 |

Line L1 gives $C = 2.814 + 2.424j$, and line L2 gives $\hat\varphi = 0.711$ rad, $0.031$ rad from the angle of $I_0$; the difference is the interference on the pilots. Before the correction, the equalized data values are $0.65$ to $0.81$ away from the sent points, which is close to the decision boundary for 4-QAM at a rotation of about $39$ degrees: subcarrier 0, sent as $-0.707 - 0.707j$, gives $-0.020 - 1.021j$. After line L3 the errors are $0.014$ to $0.116$, and subcarrier 0 gives $-0.681 - 0.760j$.

At $N = 64$ with 8 pilots, a step variance of $0.002$, a random start phase and $N_0 = 0.02$, the tests count the wrong 4-QAM decisions on 5600 data subcarriers (100 symbols, seed 3): 4091 without correction, 1 with CPE correction, and 0 with the true angle of $I_0$.

## Correctness

**Claim.** (a) Each subcarrier after the DFT is $I_0 H[k] X[k]$ plus inter-carrier interference and noise, with $I_0$ the same for all $k$. (b) For a constant phase $\theta$ and no noise, line L2 returns $\theta$ and line L3 returns the sent values exactly. (c) For a fixed phase noise and independent zero-mean unit-modulus subcarrier values, $E[C] = I_0 \sum_p |H[p]|^2$, so the estimate points at the angle of $I_0$ on average. (d) For Wiener phase noise with step variance $\sigma^2$, $E|I_0|^2 = \frac{1}{N^2} \sum_{n,m} e^{-\sigma^2 |n - m| / 2} \approx 1 - \sigma^2 N / 6$, and the interference power that the correction cannot remove is $1 - |I_0|^2$ for a channel with $|H| = 1$. Parts (a) to (d) are theorems; the size of the spread of $\hat\varphi$ around the angle of $I_0$ is measured, not proved.

**Key invariant.** The factor $I_0$ multiplies every subcarrier, so after line L3 every subcarrier carries the same residual factor $I_0 e^{-j\hat\varphi}$, which is real and positive when $\hat\varphi = \angle I_0$.

Part (a) follows by putting the expansion of the channel output in subcarriers into the DFT. Part (d) uses that $\varphi[n] - \varphi[m]$ is Gaussian with variance $\sigma^2 |n - m|$, and Parseval, $\sum_q |I_q|^2 = 1$. The full proof is below.

## Complexity

Line L1 costs $O(P)$ for $P$ pilots, line L2 is $O(1)$, and line L3 costs $O(N)$, so the time is $O(N + P)$ per symbol after the DFT, with $O(N)$ extra space for the output in the [real RAM](/real-ram/). This is negligible next to the FFT.

## Properties

- **Exact for a constant phase.** A phase offset that is the same over the symbol, such as a residual carrier phase, is removed exactly without noise.
- **Removes the common part only.** The interference power $1 - |I_0|^2$ stays. For $N = 64$ and a step variance of $0.002$, it is about $2$ percent of the power, a signal to interference ratio of about 17 dB.
- **Weighted average.** Line L1 weights each pilot by $|H[p] X_p|^2$, so pilots in deep fades count little, as they should.
- **Residual frequency offset.** A small residual frequency offset gives a phase that grows from symbol to symbol; CPE correction removes it symbol by symbol, apart from its small interference part.
- **Needs the channel.** Line L1 uses $H[p]$; if the channel estimate itself was made from pilots in the same symbol, the CPE is already inside it, and the correction does nothing more.

## Variants and improvements

- **Tracking across symbols.** The CPE of successive symbols is correlated, so a phase-locked loop or a Kalman filter over the estimates of line L2 reduces their noise.
- **Decision-directed.** After a first decision, all data subcarriers can join the sum of line L1 as if they were pilots, which reduces the noise of the estimate at a high SNR.
- **ICI suppression.** Estimating a few of the factors $I_q$ near $q = 0$ and equalizing with a short filter across subcarriers removes part of the interference, at a higher cost.
- **Pilot design.** 5G NR adds phase tracking reference signals for high carrier frequencies, where phase noise is stronger.
- **Joint with the channel.** When the channel is estimated in the same symbol, the CPE is part of the estimate, and only the symbols between pilot symbols need the correction.

## When to use it

Use CPE correction in every OFDM receiver whose channel estimate comes from earlier symbols, such as a preamble, and whose oscillator has noticeable phase noise, as in Wi-Fi, DVB-T and millimeter wave systems. It costs a few pilots and a few operations per symbol. When the phase noise bandwidth is a large fraction of the subcarrier spacing, CPE correction is not enough and interference suppression, or a larger subcarrier spacing, is needed.

## Pitfalls

- **Conjugating the received value.** Line L1 must use $Y[p] \operatorname{conj}(H[p] X_p)$. With $\operatorname{conj}(Y[p]) H[p] X_p$ the angle has the wrong sign, and line L3 doubles the error instead of removing it.
- **Averaging the angles.** Line L2 must take the angle of the complex sum from line L1. Taking the angle of each pilot term and averaging gives weak pilots too much weight and fails near $\pm\pi$.
- **Rotating the wrong way.** Line L3 must multiply by $e^{-j\hat\varphi}$, not $e^{+j\hat\varphi}$.
- **Ignoring the interference.** CPE correction cannot remove the interference part, so a design must not expect error-free symbols from a poor oscillator; the remaining $1 - |I_0|^2$ sets a floor on the SINR.
- **Few pilots in deep fades.** If all pilots of a symbol fall in fades, the sum of line L1 is small and its angle is noisy. Spreading the pilots across the band avoids this.

## Implementations

## History

Patrick Robertson and Stefan Kaiser at the German Aerospace Center analyzed phase noise in OFDM in 1995 and showed that it splits into a common phase error, shared by all subcarriers, and inter-carrier interference. The same year, Pollet, Van Bladel and Moeneclaey gave the SNR degradation caused by Wiener phase noise. Ana Garcia Armada explained both effects for broadcasting in 2001. Pilot-based phase tracking is part of IEEE 802.11a and its successors, and phase tracking reference signals were added to 5G NR for millimeter wave bands.

## References
