---
tag: 2260NZ
kind: algorithm
slug: zero-forcing-equalizer
name: Zero-forcing equalizer
aliases:
- ZF equalizer
area: communications/channel-estimation-and-equalization
level: intro
summary: "A linear FIR filter that inverts the channel, so that the combined response is a unit pulse and the intersymbol interference is zero. The price is noise enhancement, large near spectral nulls."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of equalizer taps, K: the number of symbols}
  time: {worst: O(N^3 + K N)}
  space: {extra: O(N^2)}
properties: {deterministic: true, linear: true, needs_noise_level: false, removes_isi_in_its_window: true, enhances_noise: true}
history:
  year: 1965
  people: [Robert W. Lucky]
  note: "Lucky defined the peak distortion criterion, showed that the zero-forcing equalizer minimizes it when the eye is open, and built the first automatic equalizer for telephone-line modems at Bell Labs."
prereqs: [channel-equalization, intersymbol-interference]
see_also: [mmse-linear-equalizer, decision-feedback-equalizer, fractionally-spaced-equalizer, frequency-domain-equalization, zero-forcing-mimo-detector, zero-forcing-precoding, decorrelating-detector, nyquist-isi-criterion]
sources:
  - paper: doi:10.1002/j.1538-7305.1965.tb01678.x
    title: "R. W. Lucky, Automatic equalization for digital communication, Bell System Technical Journal 44(4), 1965, pages 547 to 588"
    locator: "the peak distortion criterion, the zero-forcing tap settings and their optimality when the initial distortion is less than 1"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.4-1 (the peak distortion criterion and the zero-forcing equalizer)"
  - book: isbn:9780792375487
    title: "John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004"
    locator: "Chapter 8 (equalization)"
---

The zero-forcing (ZF) equalizer is a linear filter that undoes the [intersymbol interference](/intersymbol-interference/) of a channel by inverting it. A channel with taps $h$ smears each symbol over $L$ samples. The ZF equalizer is an FIR filter $c$ of $N$ taps, chosen so that the combined response $g = c * h$ is 1 at the decision delay $\Delta$ and 0 at the $N - 1$ indices around it. With an infinite filter it is $C(z) = 1/H(z)$ and removes all interference, so the equalized channel meets the [Nyquist ISI criterion](/nyquist-isi-criterion/). The price is noise enhancement: white noise of power $N_0$ leaves the filter with power $N_0 \|c\|^2$, which is very large when the channel has a deep spectral null. The [MMSE linear equalizer](/mmse-linear-equalizer/) adds $N_0$ to the same design and trades a little interference for much less noise, and the [decision feedback equalizer](/decision-feedback-equalizer/) cancels the past interference with decisions instead of inverting it. The same inverse appears in three other places: the [ZF MIMO detector](/zero-forcing-mimo-detector/) inverts a channel matrix across antennas, [ZF precoding](/zero-forcing-precoding/) inverts it at the transmitter, and the [decorrelating detector](/decorrelating-detector/) inverts the correlation of CDMA users. [Frequency-domain equalization](/frequency-domain-equalization/) computes a ZF or MMSE equalizer per DFT bin.

## In plain words

The channel adds an echo of each symbol to the next few samples, so the symbols overlap. The ZF equalizer is a second filter that cancels these echoes. Its taps are chosen so that, after the channel and the equalizer, each symbol arrives alone, with no part of its neighbors. A finite filter can do this exactly only at a few positions, so it forces the echoes to zero at the positions closest to the symbol, and a small residue remains further away. The equalizer does not look at the noise. Where the channel is weak at some frequency, the equalizer must amplify that frequency to restore the signal, and it amplifies the noise there too. On a good channel this costs little. On a channel with a deep fade in its spectrum, the noise can become much larger than the signal.

## The problem

The input is the channel $h = (h_0, \ldots, h_{L-1})$, known or estimated, the number of equalizer taps $N$, and the decision delay $\Delta$, with $0 \le \Delta \le N + L - 2$. The received samples are $y[n] = \sum_l h_l\, x[n - l] + w[n]$ at one sample per symbol, with $w[n] \sim \mathcal{CN}(0, N_0)$. The equalizer output is $z[n] = \sum_{i=0}^{N-1} c_i\, y[n - i] = \sum_k g_k\, x[n-k] + \nu[n]$, where $g = c * h$ has $N + L - 1$ terms and $\nu$ is the filtered noise. The output is the tap vector $c$ such that $g_\Delta = 1$ and $g_k = 0$ at the other $N - 1$ indices of a window of $N$ consecutive indices around $\Delta$. The receiver then decides $x[n - \Delta]$ from $z[n]$ with a slicer, as in the [minimum distance detector](/minimum-distance-detector/).

## The algorithm

```pseudo id=main
ZF-EQUALIZER(h, N, Δ)
L1  s ← min(max(Δ - ⌊(N - 1)/2⌋, 0), L - 1)         ▷ the first index of the window
L2  A[k][i] ← h[s + k - i]  for 0 ≤ k, i < N         ▷ h[t] = 0 outside 0 .. L - 1
L3  e ← (0, .., 0) with e[Δ - s] ← 1
L4  c ← A⁻¹ e                                        ▷ Gaussian elimination
L5  return c
```

Line L1 places the window of $N$ forced indices around $\Delta$, as close to centered as the length $N + L - 1$ of $g$ allows. Line L2 builds the $N \times N$ part of the convolution matrix that maps $c$ to $g_s, \ldots, g_{s+N-1}$; it is a Toeplitz matrix, constant along each diagonal. Line L3 is the target: a unit pulse at the delay. Line L4 solves for the taps. If $A$ is singular, the channel cannot be forced to zero on this window, and the implementation reports an error. Then the receiver filters the samples with $c$ and reads the output with the delay $\Delta$.

## Example

Take $h = (1, 0.5)$, $N = 5$ and $\Delta = 0$. Line L1 gives $s = \min(\max(0 - 2, 0), 1) = 0$. So $A$ is lower triangular, with 1 on the diagonal and 0.5 below it, and line L4 is a forward substitution: $c_0 = 1$ and $c_k = -0.5\, c_{k-1}$.

| | index 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| taps $c$ | 1 | -0.5 | 0.25 | -0.125 | 0.0625 | |
| combined $g = c * h$ | 1 | 0 | 0 | 0 | 0 | 0.03125 |

The interference is zero on the window $0, \ldots, 4$, and $g_5 = 0.5^5 = 0.03125$ remains outside it. The noise gain is $\|c\|^2 = 1.33203$, or 1.245 dB. As $N$ grows, it tends to $\frac{1}{2\pi}\int_{-\pi}^{\pi} |H(e^{j\omega})|^{-2} d\omega = 1/(1 - 0.5^2) = 4/3$, or 1.249 dB. For $h = (1, 0.9)$, whose spectrum falls to $0.1$ at half the symbol rate, the limit is $1/0.19 = 5.26$, or 7.21 dB.

The delay matters. For the channel $h = (0.5, 1)$, whose zero lies outside the unit circle, $N = 5$ gives the noise gain 1364 with $\Delta = 0$ and 1.31 with $\Delta = 3$. The causal inverse of such a channel grows, and a delay lets the filter approximate the decaying anticausal inverse instead.

The channel B of Proakis, $h = (0.407, 0.815, 0.407)$, has $H(e^{j\pi}) = 0.407 - 0.815 + 0.407 = -0.001$, an almost exact null. The best delay with $N = 31$ taps gives the noise gain 2641, or 34.2 dB, and the infinite-length value is $0.815/(0.815^2 - 0.814^2)^{3/2} = 12396$, or 40.9 dB. A ZF equalizer is useless on this channel.

## Correctness

**Claim.** If $A$ is invertible, the taps of line L4 give $g_\Delta = 1$ and $g_k = 0$ for the other $N - 1$ indices of the window, and they are the only taps that do so. The output is then $x[n - \Delta]$ plus the residual interference from the $L - 1$ indices outside the window, plus noise of variance $N_0 \|c\|^2$.

**Key step.** Row $k$ of $A c$ is $\sum_i h_{s+k-i}\, c_i = g_{s+k}$, so $A c = e$ is exactly the forcing condition on the window. For $\Delta = 0$, $A$ is lower triangular, and the taps are the first $N$ coefficients of the power series of $1/H(z)$. For a minimum-phase channel, Parseval's theorem then gives the limit of the noise gain. The full proof is in the proofs folder. Lucky's optimality result is cited there, not proved.

## Complexity

Line L2 fills $N^2$ entries and the Gaussian elimination of line L4 costs $O(N^3)$ operations, once per channel. A solver for Toeplitz systems brings this to $O(N^2)$. Filtering costs $N$ complex multiplications per symbol, so $K$ symbols cost $O(N^3 + K N)$ in the [real RAM](/real-ram/), with $O(N^2)$ extra space for $A$. For long channels, a ZF equalizer in the frequency domain with a cyclic prefix costs $O(\log N)$ per symbol with the [fast Fourier transform](/fast-fourier-transform/).

## Properties

- **Interference removed, noise ignored.** The design uses only $h$, not $N_0$. It removes the interference on its window for any noise level.
- **Noise enhancement.** The output noise variance is $N_0 \|c\|^2$. For a long filter, $\|c\|^2$ approaches $\frac{1}{2\pi}\int |H(e^{j\omega})|^{-2} d\omega$, the average of the inverse power gain, which is dominated by the weakest frequencies. So the output SNR is $E_s / (N_0 \|c\|^2)$, where SNR means $E_s/N_0$ per complex symbol.
- **Spectral nulls.** If $H(e^{j\omega}) = 0$ at some frequency, the integral diverges, and the noise gain grows without limit as $N$ grows.
- **Peak distortion.** Lucky's theorem: if the initial distortion $D_0 = \sum_{l \ne p} |h_l| / |h_p|$, with $h_p$ the largest tap, is less than 1, the ZF equalizer with the cursor under its center tap minimizes the peak distortion $\sum_{k \ne \Delta} |g_k| / |g_\Delta|$ over all $N$-tap equalizers. If $D_0 \ge 1$, it may not.
- **Limit of the MMSE equalizer.** As $N_0 \to 0$, the MMSE linear equalizer tends to the ZF equalizer.
- **Exact recovery without noise.** When the residual interference is small enough that the eye is open, the slicer recovers every symbol exactly.

## Variants and improvements

- **Least squares ZF.** Instead of forcing $N$ indices, minimize $\sum_{k \ne \Delta} |g_k|^2$ over all $N + L - 1$ indices with $g_\Delta = 1$. This is the MMSE equalizer with $N_0 = 0$.
- **Adaptive ZF.** The adaptive ZF algorithm adjusts the taps from the correlation of the error $e[n] = z[n] - \hat x[n - \Delta]$ with the decided symbols, $c_i \leftarrow c_i - \mu\, e[n]\, \overline{\hat x[n - \Delta - i]}$ in one common form, without an estimate of $h$; see [adaptive equalization](/adaptive-equalization/).
- **Fractionally spaced ZF.** With two samples per symbol, an FIR ZF equalizer of finite length can remove the interference exactly, because the two phases of the channel rarely share a zero; see the [fractionally spaced equalizer](/fractionally-spaced-equalizer/).
- **ZF decision feedback.** A ZF-DFE cancels the postcursor interference with past decisions, so the linear part only has to make the channel causal and monic. Its noise gain is smaller than that of the linear ZF.
- **Frequency-domain ZF.** With a cyclic prefix, the channel is diagonal in the DFT domain, and the ZF equalizer is one division $1/H_k$ per bin; see [frequency-domain equalization](/frequency-domain-equalization/) and [OFDM](/orthogonal-frequency-division-multiplexing/).

## When to use it

Use a ZF equalizer when the channel has no deep spectral nulls and the SNR is high, so that the noise enhancement is small. It is simple, it does not need $N_0$, and it is a reference for other equalizers. Use the MMSE linear equalizer at moderate SNR or on channels with deep fades, and a DFE or a [Viterbi equalizer](/viterbi-equalizer/) when the channel has a null in its band.

## Pitfalls

- **A channel with a spectral null.** On a channel such as Proakis B, the ZF equalizer amplifies the noise by more than 30 dB. Check $\|c\|^2$, or the minimum of $|H(e^{j\omega})|$, before using it.
- **The wrong delay.** For a channel that is not minimum phase, delay 0 gives a filter whose taps grow, with a huge noise gain. Try every delay and keep the one with the smallest noise gain and residual interference, or use a delay near the middle of $N + L - 1$.
- **Too short a filter.** A short equalizer leaves interference outside its window. For $h = (1, a)$ and delay 0, the residue is $|a|^N$; for $|a|$ near 1 it decays slowly.
- **An estimated channel.** The ZF equalizer inverts the estimate, not the true channel. Errors in $\hat h$ near a weak frequency are amplified, just as the noise is.
- **Treating the output noise as white.** The noise $\nu[n]$ has variance $N_0 \|c\|^2$, but it is correlated from symbol to symbol. A sequence detector after the ZF equalizer must take this into account, or use a whitened model instead.

## Implementations

## History

Robert Lucky built the first automatic equalizers for data transmission over telephone lines at Bell Labs in the mid 1960s. His 1965 paper defined the peak distortion, the worst-case sum of the interference, and showed that when the eye is open before equalization, the equalizer that forces the interference to zero at the taps around the cursor minimizes it. The mean-square error criterion, which leads to the MMSE equalizer, followed in the late 1960s and soon replaced peak distortion in most designs, because it takes the noise into account and allows the LMS algorithm.

## References
