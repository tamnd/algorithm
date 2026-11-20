---
tag: CVZ52Y
kind: algorithm
slug: iterative-clipping-and-filtering
name: Iterative clipping and filtering
aliases:
- clipping and filtering
area: communications/ofdm-and-multicarrier
level: core
summary: "Lowers the PAPR of an OFDM symbol by clipping the oversampled signal and removing the out-of-band regrowth with an FFT filter, repeated a few times. The receiver is unchanged."
model: real-ram
complexity:
  vars: {N: the number of subcarriers, L: the oversampling factor, K: the number of iterations}
  time: {worst: O(K L N log(L N))}
  space: {extra: O(L N)}
properties: {deterministic: true, band_limited_output: true, side_information: false, changes_data_symbols: true}
history:
  year: 2002
  people: [Jean Armstrong]
  note: "Li and Cimini (1998) studied one clip followed by a filter. Armstrong (2002) clipped the oversampled signal, filtered in the frequency domain with an FFT, and repeated both steps to remove the peaks that the filter brings back."
prereqs: [peak-to-average-power-ratio, orthogonal-frequency-division-multiplexing, convex-set]
see_also: [active-constellation-extension, tone-reservation, selected-mapping, partial-transmit-sequence, fast-fourier-transform, power-spectral-density, spectral-leakage, bit-error-rate]
sources:
  - paper: doi:10.1049/el:20020175
    title: "J. Armstrong, Peak-to-average power reduction for OFDM by repeated clipping and frequency domain filtering, Electronics Letters 38(5), 2002, pages 246 to 247"
    locator: "the oversampled clipping, the FFT filter that removes the out-of-band components, and the repetition of the two steps"
  - paper: doi:10.1109/4234.673657
    title: "Xiaodong Li and Leonard J. Cimini, Effects of clipping and filtering on the performance of OFDM, IEEE Communications Letters 2(5), 1998, pages 131 to 133"
    locator: "one clipping step followed by a filter, and its effect on the error rate and the spectrum"
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the section on clipping and filtering in the overview of reduction methods"
---

Iterative clipping and filtering lowers the [peak-to-average power ratio](/peak-to-average-power-ratio/) (PAPR) of an [OFDM](/orthogonal-frequency-division-multiplexing/) symbol by changing the signal itself. The transmitter oversamples the symbol, limits the magnitude of each sample to a threshold $A$ and keeps its phase, and then removes the out-of-band power that the clipping created with an FFT filter. The filter brings part of the peaks back, so the two steps are repeated $K$ times, usually 2 to 4. The receiver needs no change and no side information, but the data symbols on the subcarriers change a little: the method trades in-band distortion for a lower peak. It differs from [selected mapping](/selected-mapping/) and [partial transmit sequences](/partial-transmit-sequence/), which choose among exact versions of the symbol and add no distortion, and from [tone reservation](/tone-reservation/) and [active constellation extension](/active-constellation-extension/), which put the peak-cancelling signal only where it does not hurt detection. The page uses the unitary DFT pair of the OFDM page, $F[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, and $j$ is the imaginary unit.

## In plain words

An amplifier can only handle signals up to some size. An OFDM signal is usually small, but now and then many tones add up to a tall spike. The simple fix is to cut every spike down to a fixed height. Cutting changes the shape of the signal, and the sharp corners spread power into the frequencies of the neighbors, which is not allowed. So the transmitter removes that outside power with a filter. The filter rounds the corners again, and some spikes grow back, smaller than before. Doing the cut and the filter a few times leaves a signal with lower peaks that still stays in its own band. The price is a small error on every data symbol, which the receiver sees as extra noise.

## The problem

The input is one OFDM symbol, $N$ data symbols $X[0], \ldots, X[N-1]$ with $E|X[k]|^2 = 1$, and a clipping ratio $\mathrm{CR}$, the threshold $A$ divided by the RMS amplitude of the symbol. The output is a signal that

1. occupies only the $N$ subcarriers of the symbol, with no power in the bins outside them,
2. has a lower PAPR than the original symbol, measured with oversampling, and
3. carries values on the subcarriers that are close to $X$, so that the receiver can detect the data with a small loss.

The PAPR must be measured on the oversampled signal. Clipping only the $N$ samples at the Nyquist rate leaves the peaks between them, and they come back after the digital-to-analog converter.

## The algorithm

```pseudo id=main
ICF(X[0..N-1], L, CR, K)
L1  x ← √L · F_LNᴴ (X[0..N/2-1], 0, .., 0, X[N/2..N-1])   ▷ oversampled symbol, (L-1)N zeros in the middle
L2  A ← CR · √(mean of |x[m]|²)                           ▷ the threshold, fixed once
L3  for i ← 1 to K
L4      c[m] ← x[m] if |x[m]| ≤ A, else A · x[m] / |x[m]|  ▷ clip the magnitude, keep the phase
L5      C ← FFT of c (size LN)
L6      C[k] ← 0 for N/2 ≤ k < LN - N/2                     ▷ remove the out-of-band regrowth
L7      x ← inverse FFT of C (size LN)
L8  return x and its N in-band values                     ▷ bins 0..N/2-1 and LN-N/2..LN-1, scaled back
```

Line L1 builds the symbol $L$ times oversampled. The zeros go in the middle of the spectrum, because the indices $k \ge N/2$ of $X$ are the negative frequencies. Line L2 sets the threshold from the RMS amplitude of the original symbol and keeps it fixed; with $\mathrm{CR} = 1.4$ the clipping level $A^2$ is $1.96$ times the mean power, 2.92 dB. Line L4 is the clip. It is a soft limiter: a sample below $A$ passes, a sample above $A$ keeps its phase and gets the magnitude $A$. Lines L5 to L7 are the filter. In the frequency domain the clip has spread power into the bins between $N/2$ and $LN - N/2$, the spectral regrowth, and line L6 deletes it. Line L7 returns to time. After the loop the signal is band-limited, and its in-band bins are the new subcarrier values that the transmitter sends; a transmitter that builds its OFDM symbol with an inverse FFT of size $N$ uses these values as its input.

## Example

Take $N = 64$ QPSK subcarriers, $L = 4$ and $\mathrm{CR} = 1.4$. For one symbol (Python `random.Random(1)`), the PAPR and the clipped-off energy $\sum_m (|x[m]| - A)^2$ over the samples above $A$, at the start of each iteration, are:

| iteration $i$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| PAPR before the clip | 6.94 dB | 5.33 dB | 4.76 dB | 4.46 dB | 4.31 dB |
| clipped-off energy | 4.96 | 0.565 | 0.148 | 0.050 | |

The clipped-off energy falls at every step, as the correctness proof says it must. Over 300 random symbols (`random.Random(2)`), with the PAPR of the 4 times oversampled output and the in-band error $E|X_{\mathrm{out}}[k] - X[k]|^2$:

| $\mathrm{CR}$ | $K$ | mean PAPR | 99 percent of symbols below | in-band error | output power |
|---|---|---|---|---|---|
| | 0 | 7.28 dB | 9.48 dB | none | 1.000 |
| 1.4 | 1 | 5.42 dB | 6.52 dB | -18.2 dB | 0.858 |
| 1.4 | 2 | 4.84 dB | 5.59 dB | -16.2 dB | 0.822 |
| 1.4 | 4 | 4.45 dB | 5.16 dB | -15.0 dB | 0.796 |
| 1.4 | 8 | 4.16 dB | 4.81 dB | -14.4 dB | 0.782 |
| 1.7 | 4 | 5.42 dB | 5.97 dB | -20.3 dB | 0.914 |

Four iterations at $\mathrm{CR} = 1.4$ cut the 99 percent point by more than 4 dB. Each further iteration gains less and adds more in-band error. A higher $\mathrm{CR}$ gives a smaller gain and a smaller error. The output power falls because the clip removes energy; the transmitter scales the signal back up before the amplifier, and the PAPR does not depend on that scale.

## Correctness

The claim is that the output is exactly band-limited, and that the clipped-off energy never grows from one iteration to the next. The key fact is that line L4 is the projection onto the closed convex set $S$ of signals with $|x[m]| \le A$ for every $m$, and lines L5 to L7 are the orthogonal projection onto the subspace $B$ of band-limited signals. So the loop is a method of alternating projections between a [convex set](/convex-set/) and a subspace. The invariant is $x \in B$ after each iteration. If $d_i$ is the distance from $x$ to $S$ before clip $i$, and $e_i$ is the energy that filter $i$ removes, then $d_0 \ge e_0 \ge d_1 \ge e_1 \ge \cdots$, and both sequences tend to zero, because $S \cap B$ contains at least the zero signal. The full proof, with the convergence of $x$ to a point of $S \cap B$, is in [proofs/correctness.md](proofs/correctness.md). The theorem does not say that the PAPR falls to $\mathrm{CR}^2$: the limit can have a lower mean power than the original symbol.

## Complexity

Each iteration does one FFT and one inverse FFT of size $LN$, plus $O(LN)$ work for the clip and the filter, so $K$ iterations cost $O(K L N \log(LN))$ operations per OFDM symbol in the real-RAM model, with the [FFT](/fast-fourier-transform/). The memory is $O(LN)$. For $N = 64$, $L = 4$ and $K = 4$ this is 8 transforms of size 256 per symbol, against 1 transform of size 64 for plain OFDM.

## Properties

- **No side information.** The receiver demodulates as usual. The clipping error looks like extra noise on each subcarrier.
- **Band-limited output.** The out-of-band bins are exactly zero after each filter, so the method does not spoil the spectrum mask, unlike plain clipping.
- **In-band distortion.** The subcarrier values move away from $X$, by about $-15$ dB in the example. This raises the error rate, mostly for dense constellations such as 64-QAM, whose decision regions are small.
- **Diminishing returns.** The gain per iteration falls quickly; most of it comes in the first 2 to 4 iterations.
- **Data-independent cost.** The work per symbol is fixed by $K$, $L$ and $N$, with no search.

## Variants and improvements

- **One clip and one filter.** $K = 1$, as in Li and Cimini (1998). It is the cheapest form and leaves the highest peaks.
- **Filtering with a time-domain filter.** A low-pass FIR filter instead of the FFT mask. It does not remove the regrowth exactly and adds delay.
- **Clipping with a window.** Peak windowing multiplies the signal near each peak by a smooth window instead of a hard limit. The spectral regrowth is smaller, so less filtering is needed.
- **A different filter mask.** The filter can keep part of the regrowth in a guard band, or shape the in-band error so that it falls on subcarriers with robust modulation.
- **Receiver-side recovery.** Because the clipping is a known function of the data, an iterative receiver can estimate the clipping error from its decisions and subtract it.
- **Distortion only where it is allowed.** [Active constellation extension](/active-constellation-extension/) keeps the clip and filter structure but projects each subcarrier onto a region that does not move it toward a decision boundary. [Tone reservation](/tone-reservation/) puts the correction only on reserved subcarriers.

## When to use it

Use it when the receiver cannot change, for example in a standard that defines the receiver but leaves the transmitter free, and when the error budget of the link allows some in-band distortion. Avoid it, or use a high clipping ratio, with dense constellations and high-rate codes, where a $-15$ dB error is a large loss. If side information is acceptable and distortion is not, use [selected mapping](/selected-mapping/) or [partial transmit sequences](/partial-transmit-sequence/).

## Pitfalls

- **Clipping at the Nyquist rate.** Line L1 with $L = 1$ lets the peaks between the samples survive, and the analog signal still has a high PAPR. Use $L \ge 4$ in line L1.
- **Moving threshold.** Recomputing $A$ inside the loop from the current mean power makes the threshold fall with each iteration and removes more energy than needed. Compute it once, in line L2.
- **Wrong bins.** Writing line L6 as "$C[k] \leftarrow 0$ for $N \le k < LN$" deletes the negative frequencies of the symbol and keeps the regrowth. With the zeros placed in the middle by line L1, the out-of-band bins are $N/2 \le k < LN - N/2$.
- **Square clipping.** Writing line L4 as a clamp of the real part and of the imaginary part to $\pm A$ changes the phase and is not the nearest point of the disc. It also lets the magnitude reach $\sqrt 2\, A$. Clip the magnitude, as in line L4.
- **Expecting the PAPR to equal $\mathrm{CR}^2$.** After line L7 the peaks grow back above $A$, and the mean power has fallen. Measure the PAPR of the output; do not assume it.

## Implementations

## History

Clipping is the simplest way to limit the peaks of a multicarrier signal. Li and Cimini (1998) analyzed one clip at the transmitter followed by a filter, and showed the effect on the error rate and on the spectrum. Armstrong (2002) clipped the oversampled signal, filtered with an FFT so that the out-of-band power is removed exactly, and repeated the two steps, which brought the peak regrowth down. The overview by Han and Lee (2005) places clipping and filtering among the distortion methods, next to the methods with side information.

## References
