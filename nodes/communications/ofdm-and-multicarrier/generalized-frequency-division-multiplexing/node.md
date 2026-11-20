---
tag: 36P3DR
kind: technique
slug: generalized-frequency-division-multiplexing
name: Generalized frequency-division multiplexing
aliases:
- GFDM
area: communications/ofdm-and-multicarrier
level: research
summary: "A block of K subcarriers by M subsymbols on circularly shifted, filtered pulses, with one cyclic prefix per block. Not orthogonal, so the receiver inverts or matches the modulation matrix."
prereqs: [orthogonal-frequency-division-multiplexing, cyclic-prefix, pulse-shaping, mmse-linear-equalizer]
see_also: [filter-bank-multicarrier, universal-filtered-multicarrier, sc-fdma, orthogonal-time-frequency-space-modulation, raised-cosine-filter, zero-forcing-equalizer, matched-filter, frequency-domain-equalization]
sources:
  - paper: doi:10.1109/VETECS.2009.5073571
    title: "Gerhard Fettweis, Marco Krondorf and Steffen Bittner, GFDM - Generalized Frequency Division Multiplexing, IEEE 69th Vehicular Technology Conference (VTC Spring 2009), Barcelona, 2009, pages 1 to 4"
    locator: "the proposal of the block structure with circularly shifted pulses and one cyclic prefix per block"
  - paper: doi:10.1109/TCOMM.2014.2345566
    title: "Nicola Michailow, Maximilian Matthé, Ivan Simões Gaspar, Ainoa Navarro Caldevilla, Luciano Leonel Mendes, Andreas Festag and Gerhard Fettweis, Generalized frequency division multiplexing for 5th generation cellular networks, IEEE Transactions on Communications 62(9), 2014, pages 3045 to 3061"
    locator: "the matrix model x = A d, the zero-forcing, matched-filter and MMSE receivers, and the effect of the prototype and of an even number of subsymbols"
---

Generalized frequency-division multiplexing (GFDM) is a block multicarrier scheme proposed by Fettweis, Krondorf and Bittner in 2009. One block of $N = KM$ samples carries $K$ subcarriers and $M$ subsymbols on each, $KM$ data symbols in all. Each data symbol rides on a copy of a prototype filter $g$ that is circularly shifted in time by a multiple of $K$ samples and modulated to its subcarrier. The circular shift, sometimes called tail biting, keeps the block exactly $N$ samples long, so a single [cyclic prefix](/cyclic-prefix/) protects all $M$ subsymbols, and a smooth prototype gives lower sidelobes than [OFDM](/orthogonal-frequency-division-multiplexing/). The pulses are not orthogonal, so the receiver must undo the overlap: zero forcing inverts the modulation matrix, a [matched filter](/matched-filter/) leaves self-interference, and MMSE balances the two. With $M = 1$, GFDM is OFDM; with $K = 1$, it is a single-carrier block with a cyclic prefix. The page uses $j$ for the imaginary unit.

## In plain words

OFDM sends many short symbols side by side in frequency, each with sharp edges. GFDM groups several of these symbols in time into one longer block and gives each a smooth shape, which keeps their energy close to their own frequency. The shapes wrap around at the end of the block, so one guard interval at the start protects the whole block, not every symbol. The price is that the smooth shapes overlap and disturb each other. The receiver knows exactly how they overlap and can undo it with a fixed calculation, at the cost of more computation and a little more noise.

## When it applies

- The band must be well contained and the guard per symbol must be small, for example for many short bursts from loosely synchronized devices.
- The channel is constant over one block of $N$ samples, and its delay spread fits in one cyclic prefix.
- The receiver can afford the inverse or the MMSE filter of an $N \times N$ structured matrix, computed once for a given prototype.
- The design can choose an odd number of subsymbols $M$ or a prototype for which the modulation matrix is well conditioned.

## The template

```pseudo id=main
GFDM(d[0..N-1], g[0..N-1], K, M, cp)              ▷ N = K M; d[k + mK] is subsymbol m on subcarrier k
L1  A[n][k + mK] ← g[(n - mK) mod N] · e^{j2πkn/K}   for all n, k, m
L2  x ← A d
L3  send (x[N-cp..N-1], x)                         ▷ one cyclic prefix for the block
L4  y ← the received block without the prefix, equalized by one N-point DFT, division by H and an inverse DFT
L5  d̂ ← A⁻¹ y (zero forcing),  or Aᴴ y (matched filter),  or (AᴴA + σ²I)⁻¹ Aᴴ y (MMSE)
```

**The prototype.** A common choice is a raised cosine in frequency with roll-off $\alpha$, sampled at $M$ bins per subcarrier spacing over the $N$-point grid and transformed to time, so that $g$ is real, circularly symmetric and of unit energy. Each subcarrier then overlaps only its two neighbors in frequency.

**Special cases.** With $M = 1$ the prototype covers one bin and $A = F_K^H$, the unitary inverse DFT: GFDM is OFDM. With $K = 1$ there is one subcarrier and the block is a single-carrier block with a cyclic prefix, received with [frequency-domain equalization](/frequency-domain-equalization/).

**Even $M$.** For the raised-cosine prototype and an even $M$, $A$ is singular: zero forcing is impossible and MMSE loses performance. An odd $M$ avoids this.

**Cost.** Lines L2 and L5 are written as matrix products, $O(N^2)$ per block after $A^{-1}$ or the MMSE matrix is computed once. Implementations use the structure of $A$: the circular shifts and modulations allow FFTs of sizes $K$ and $M$ and a filter that touches only a few subcarriers, with a cost close to $O(N \log N)$.

## Classic examples

**Conditioning and self-interference.** The table lists, for the raised-cosine prototype, $|\det A|$, the signal-to-interference ratio of the matched filter (the diagonal power of $A^H A$ over its off-diagonal power) and the noise enhancement of zero forcing, $\frac1N \lVert A^{-1} \rVert_F^2$:

| $K$ | $M$ | $\alpha$ | $\lvert\det A\rvert$ | matched filter SIR | zero-forcing noise enhancement |
|---|---|---|---|---|---|
| 4 | 3 | 0.5 | 0.968 | 19.9 dB | 0.05 dB |
| 4 | 3 | 0.9 | 0.627 | 9.4 dB | 0.79 dB |
| 8 | 5 | 0.5 | 0.412 | 12.1 dB | 0.46 dB |
| 8 | 5 | 0.9 | 0.094 | 9.0 dB | 1.53 dB |
| 4 | 2 | 0.5 | below $10^{-16}$ | 6.5 dB | singular |
| 4 | 4 | 0.5 | below $10^{-16}$ | 9.9 dB | singular |
| 8 | 4 | 0.5 | below $10^{-16}$ | 9.9 dB | singular |

A larger roll-off gives a smoother spectrum but a worse matrix: more self-interference for the matched filter and more noise for zero forcing. For an even $M$ the determinant is zero to rounding error for every roll-off tried, 0.1, 0.5 and 0.9.

**A round trip.** With $K = 8$, $M = 5$, $\alpha = 0.5$, a prefix of 4 samples and a random 5-tap channel, 40 random 16-QAM symbols pass through lines L1 to L5 with zero forcing and come back to within rounding error. The matched filter on the same block misses some symbols by more than 0.05, the self-interference above.

## Variations

- **Receivers.** Successive interference cancellation after the matched filter, or iterative detection, recovers most of the matched-filter loss without the full inverse.
- **Windowing.** A smooth window over the prefix and the block lowers the sidelobes further, at a small cost in prefix length.
- **Other prototypes.** Prototypes designed so that $A$ is unitary make GFDM orthogonal again, at the cost of their spectral shape.
- **Offset QAM.** As in [filter bank multicarrier](/filter-bank-multicarrier/), real symbols with staggered timing make the pulses real-orthogonal.
- **Precoded GFDM.** A DFT across the subsymbols spreads each data symbol over the block, like [SC-FDMA](/sc-fdma/) for OFDM, which lowers the PAPR.

## Pitfalls

- **An even number of subsymbols.** With the raised-cosine prototype and $M$ even, line L5 with zero forcing fails because $A$ is singular. Choose $M$ odd in line L1, or another prototype.
- **Matched filter alone.** Line L5 with $A^H y$ leaves self-interference near 10 dB below the signal for typical roll-offs, an error floor at high SNR. Use zero forcing, MMSE or interference cancellation for dense constellations.
- **Large roll-off without care.** A roll-off near 1 in line L1 gives a better spectrum but a larger noise enhancement for zero forcing. Choose the roll-off by the noise enhancement as well as by the sidelobes.
- **Channel that changes within a block.** Line L4 assumes one channel for the whole block of $N$ samples. For fast fading, shorten the block with a smaller $M$.
- **Index order.** The symbol $d[k + mK]$ must be on column $k + mK$ in both lines L1 and L5. A different order at the receiver mixes the subsymbols.

## Exercises

1. Show that with $M = 1$ the matrix $A$ is the unitary inverse DFT of size $K$ when $g$ is constant.
2. Show that $A$ is unitary if and only if the pulses $a_{k,m}$ form an orthonormal basis of $\mathbb{C}^N$, and give the zero-forcing receiver in that case.
3. Show that the noise enhancement of zero forcing for white noise is $\frac1N \lVert A^{-1} \rVert_F^2$, and that it is at least 1 for unit-energy pulses.
4. With $K = 1$, write $A$ for a block of $M$ single-carrier symbols and explain why the receiver of line L4 alone recovers the data.
5. Count the prefix overhead of OFDM with $K$ subcarriers and $M$ symbols, each with a prefix of $c$ samples, and of one GFDM block with one prefix of $c$ samples.

## References
