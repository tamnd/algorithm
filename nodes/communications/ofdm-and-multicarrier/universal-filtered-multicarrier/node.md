---
tag: 45M7YX
kind: technique
slug: universal-filtered-multicarrier
name: Universal filtered multicarrier
aliases:
- UFMC
area: communications/ofdm-and-multicarrier
level: research
summary: "OFDM with the subcarriers in subbands and a short filter on each subband. The filter tails replace the cyclic prefix and cut the out-of-band emission."
prereqs: [orthogonal-frequency-division-multiplexing, fir-filter, cyclic-prefix]
see_also: [filter-bank-multicarrier, generalized-frequency-division-multiplexing, orthogonal-time-frequency-space-modulation, chebyshev-polynomials, orthogonal-frequency-division-multiple-access, inter-carrier-interference, delay-spread, fast-fourier-transform]
sources:
  - paper: doi:10.1109/GLOCOMW.2013.6824990
    title: "Vida Vakilian, Thorsten Wild, Frank Schaich, Stephan ten Brink and Jean-François Frigon, Universal-filtered multi-carrier technique for wireless systems beyond LTE, IEEE Globecom Workshops, 2013, pages 223 to 228"
    locator: "the transmitter with one Dolph-Chebyshev filter per subband, the block without a cyclic prefix and the receiver with a 2N-point FFT"
---

Universal filtered multicarrier (UFMC) is a variant of [OFDM](/orthogonal-frequency-division-multiplexing/) proposed by Vakilian, Wild, Schaich, ten Brink and Frigon in 2013. The $N$ subcarriers are grouped into subbands of a few adjacent subcarriers. Each subband is turned into time with an $N$-point inverse DFT, as in OFDM, and then passes through its own short [FIR filter](/fir-filter/) of length $L$. The filtered subbands are added. A block has $N + L - 1$ samples and no [cyclic prefix](/cyclic-prefix/): the rising and falling tails of the filter take the place of the prefix. The filter is narrow enough to attenuate the sidelobes of the subband outside its edges, so the out-of-band emission is much lower than for OFDM, but wide enough to pass the subband. The filters are short because a subband is much wider than one subcarrier. The receiver pads the block to $2N$ samples, takes one $2N$-point FFT, keeps the even bins, and divides each by the filter and channel response. The page uses $j$ for the imaginary unit.

## In plain words

An OFDM signal spreads some power outside its own band, which disturbs neighbors. UFMC cuts the band into small groups of subcarriers and smooths each group with a short filter, so very little power leaves the group. The smoothing makes each block a little longer, and this extra length also does the job of the guard interval of OFDM. The receiver uses one transform of twice the usual size and then undoes the known effect of the filter on each subcarrier.

## When it applies

- Users or services share a band and must not disturb each other, for example uplink users that are not exactly synchronized in time or frequency, or narrow allocations next to other systems.
- The blocks are short, so a filter per subcarrier as in [filter bank multicarrier](/filter-bank-multicarrier/) would give too long a tail, but a filter per subband stays short.
- The channel [delay spread](/delay-spread/) is short compared with the filter length, or a short zero guard is added after each block.
- The receiver can afford a $2N$-point FFT and a division per subcarrier.

## The template

```pseudo id=main
UFMC(X[0..N-1], subbands, f_1..f_B, h)            ▷ f_i has length L; bins k are signed, -N/2 ≤ k < N/2
L1  x_i ← the unitary N-point inverse DFT of X on the bins of subband i, for each i
L2  x ← Σ_i f_i ∗ x_i                              ▷ linear convolution; N + L - 1 samples
L3  send x with no cyclic prefix
L4  Y ← the 2N-point DFT of the received block, padded with zeros to 2N samples
L5  X̂[k] ← Y[2k] / (√N · F_i[2k] · H[2k])  for each bin k of subband i
```

Here $F_i$ and $H$ are the $2N$-point DFTs of the filter and the channel.

**Why the even bins work.** The $2N$-point DFT of $x_i$ at bin $2k$ is its $N$-point DFT at bin $k$, which is $\sqrt N X[k]$ on the bins of subband $i$ and 0 elsewhere. The linear convolutions with $f_i$ and with the channel have at most $N + L + L_h - 2$ samples, so if this fits in $2N$ samples the $2N$-point DFT turns them into products. Bin $2k$ then holds $\sqrt N F_i[2k] H[2k] X[k]$ and nothing from the other subbands, which have zeros at bin $k$. Line L5 is exact in the noiseless case.

**The filter.** Vakilian and coauthors use a Dolph-Chebyshev window shifted to the center of each subband. This window has the narrowest main lobe for a given sidelobe level and the same height for all its sidelobes. Its coefficients come from the [Chebyshev polynomial](/chebyshev-polynomials/) $T_{L-1}$.

**Cost.** Line L1 costs one inverse FFT per subband (or a smaller inverse transform on the subband bins), and line L2 costs $L$ multiplications per sample per subband. The receiver costs one FFT of size $2N$.

## Classic examples

**Out-of-band emission.** $N = 64$, 4 subbands of 6 subcarriers on bins $-12$ to $11$, QPSK, 40 random blocks, Dolph-Chebyshev filters. The table lists the highest average spectrum at more than $d$ subcarrier spacings beyond the band edge, relative to the average in-band level, and two costs of the filter: the drop of the filter response at the subband edge, and the average noise gain of the division in line L5 relative to the subband center. OFDM uses the same bins and a cyclic prefix of 16 samples.

| scheme | $d = 1$ | $d = 2$ | $d = 4$ | $d = 8$ | edge drop | noise gain |
|---|---|---|---|---|---|---|
| OFDM | $-11.2$ dB | $-16.0$ dB | $-18.5$ dB | $-22.1$ dB | 0 | 0 |
| UFMC, $L = 9$, 40 dB sidelobes | $-12.1$ dB | $-16.8$ dB | $-24.6$ dB | $-44.6$ dB | 0.88 dB | 0.40 dB |
| UFMC, $L = 17$, 40 dB sidelobes | $-17.9$ dB | $-27.7$ dB | $-55.7$ dB | $-58.5$ dB | 3.27 dB | 1.66 dB |
| UFMC, $L = 17$, 60 dB sidelobes | $-14.9$ dB | $-22.0$ dB | $-37.8$ dB | $-78.8$ dB | 2.32 dB | 1.14 dB |
| UFMC, $L = 33$, 60 dB sidelobes | $-33.4$ dB | $-68.0$ dB | $-76.0$ dB | $-77.0$ dB | 9.33 dB | 5.85 dB |

A longer filter cuts the spectrum closer to the band, but its main lobe gets narrower than the subband and the edge subcarriers lose power. With subbands of 12 subcarriers the same filters drop the edge by 4.56 dB ($L = 9$), 20.2 dB ($L = 17$, 40 dB) and 67.1 dB ($L = 33$, 60 dB): the subband width and the filter length must be chosen together. For OFDM the leakage falls slowly, because the rectangular pulse has sidelobes that fall only as $1/f^2$ in power.

**A round trip.** With the same bins, $L = 17$ and a random 8-tap channel, the received block has $64 + 16 + 7 = 87$ samples, which fits in $2N = 128$. Lines L4 and L5 give back the QPSK symbols with an error below $10^{-14}$.

## Variations

- **Other filters.** Any short filter with a flat pass band over the subband and low sidelobes works. Windowed-sinc and other window designs trade edge flatness against sidelobe level.
- **Zero guard.** A short run of zeros after each block, or a longer filter tail, protects against a channel longer than the soft ramps of the filter.
- **Per-subband settings.** Each subband can have its own filter, subcarrier spacing or power, which suits users with different needs in one band.
- **Receiver windowing.** A window before the $2N$-point FFT cuts the noise and interference from outside the block at the cost of exact recovery.
- **Filtered OFDM.** One longer filter over a whole allocation, with a cyclic prefix kept, is a close relative for wider allocations.

## Pitfalls

- **Filter too long for the subband.** Line L2 with a long filter on a wide subband attenuates the edge subcarriers, and line L5 then amplifies the noise there. Choose the filter length so that its main lobe covers the subband.
- **Receiver window too short.** Line L4 with only $N + L - 1$ samples cuts off the channel tail, and line L5 is no longer exact. Keep all $N + L + L_h - 2$ samples, at most $2N$, or add a zero guard.
- **Odd bins.** Line L5 must use the even bins $2k$. The odd bins hold the interpolated spectrum between subcarriers and mix the data of neighbors.
- **Missing scale.** Line L5 must divide by $\sqrt N F_i[2k]$ as well as by $H[2k]$. Dividing by the channel alone leaves the filter gain and phase on each symbol.
- **Wrong filter for a bin.** In line L5 the bin $k$ must be divided by the filter of its own subband. The filter of a neighbor has a different phase and gain at that bin.

## Exercises

1. Show that the $2N$-point DFT of a signal of $N$ samples, padded with $N$ zeros, takes at the even bins the values of its $N$-point DFT.
2. Show that the block of line L2 has $N + L - 1$ samples and that its middle $N - L + 1$ samples are not affected by the filter ramps of a single subband.
3. Explain why the division of line L5 cannot recover a bin where the filter response $F_i[2k]$ is zero, and how the filter design avoids this.
4. With $N = 64$, $L = 17$ and a channel of $L_h$ taps, find the largest $L_h$ for which line L5 is still exact.
5. Compare the overhead of one UFMC block with $L = 17$ and one OFDM symbol with a cyclic prefix of 16 samples, both with $N = 64$.

## References
