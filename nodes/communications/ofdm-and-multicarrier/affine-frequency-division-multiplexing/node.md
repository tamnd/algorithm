---
tag: 94W5XF
kind: technique
slug: affine-frequency-division-multiplexing
name: Affine frequency-division multiplexing
aliases:
- AFDM
area: communications/ofdm-and-multicarrier
level: research
summary: "Multicarrier modulation on chirps given by the inverse discrete affine Fourier transform. A chirp rate matched to the largest Doppler puts each path of a doubly dispersive channel on its own bin."
prereqs: [orthogonal-frequency-division-multiplexing, doppler-spread, delay-spread, discrete-fourier-transform]
see_also: [orthogonal-time-frequency-space-modulation, cyclic-prefix, zadoff-chu-sequence, mmse-linear-equalizer, message-passing, coherence-time, generalized-frequency-division-multiplexing, fast-fourier-transform]
sources:
  - paper: doi:10.1109/TWC.2023.3260906
    title: "Ali Bemani, Nassar Ksairi and Marios Kountouris, Affine frequency division multiplexing for next generation wireless communications, IEEE Transactions on Wireless Communications 22(11), 2023, pages 8214 to 8229"
    locator: "the discrete affine Fourier transform, the chirp-periodic prefix, the input-output relation and the choice of c1 from the largest delay and Doppler"
---

Affine frequency-division multiplexing (AFDM), proposed by Bemani, Ksairi and Kountouris, sends $N$ symbols on $N$ chirps, signals whose frequency rises linearly in time. The chirps come from the inverse discrete affine Fourier transform (DAFT): an inverse DFT between two chirp multiplications with rates $c_1$ and $c_2$. With $c_1 = c_2 = 0$ AFDM is [OFDM](/orthogonal-frequency-division-multiplexing/). In a channel with both delay spread and Doppler spread, a doubly dispersive channel, OFDM subcarriers leak into each other. In AFDM a path with delay $l$ and Doppler $a$ only moves each symbol to another bin of the receiver's transform, by $a - 2Nc_1 l$, and multiplies it by a known phase. With $c_1$ chosen from the largest Doppler shift, different paths land on different bins, so the receiver can separate them and collect their diversity. The block uses a chirp-periodic prefix in place of the [cyclic prefix](/cyclic-prefix/). The page uses $j$ for the imaginary unit.

## In plain words

OFDM sends each symbol on a steady tone. When the receiver moves, every echo shifts the tones a little and they start to disturb each other. AFDM sends each symbol on a tone that slides up in frequency during the block. The slide is chosen so that an echo with a delay moves the symbol to a different place than an echo with a frequency shift. Each echo then puts its copy of the data in its own place, and the receiver can sort the copies out and add them up.

## When it applies

- The channel has a few paths with both delay and Doppler spread, for example high-mobility links, where OFDM suffers from interference between subcarriers.
- The largest delay and the largest Doppler shift are known well enough to choose the chirp rate $c_1$.
- The product of the delay and Doppler ranges fits the block: $(l_{\max} + 1)(2a_{\max} + 1) \le N$ for integer shifts.
- A one-dimensional block of $N$ samples is preferred to the two-dimensional frame of [OTFS](/orthogonal-time-frequency-space-modulation/), and the receiver can afford a joint detector over the block.

## The template

```pseudo id=main
AFDM(x[0..N-1], c1, c2, cp, paths)
L1  s[n] ← (1/√N) Σ_m x[m] e^{j2π(c1 n² + c2 m² + nm/N)}   for n = 0..N-1    ▷ inverse DAFT, with one inverse FFT
L2  s[n] ← s[N+n] e^{-j2π c1 (N² + 2Nn)}   for n = -cp..-1                    ▷ chirp-periodic prefix
L3  send s[-cp..N-1]
L4  y[q] ← (1/√N) Σ_n r[n] e^{-j2π(c1 n² + c2 q² + nq/N)}   for q = 0..N-1    ▷ DAFT of the block after the prefix
L5  x̂ ← the solution of y = H x by LMMSE or message passing, with H built from the paths
```

**The prefix.** Line L2 makes the formula of line L1 hold for negative $n$ as well. When $2Nc_1$ is an integer and $N$ is even, the factor is 1 and the prefix is an ordinary cyclic prefix.

**The channel on the bins.** Let path $p$ have gain $h_p$, delay $l_p$ samples and Doppler $a_p/N$ cycles per sample: $r[n] = \sum_p h_p e^{j2\pi a_p n/N} s[n - l_p]$. When $2Nc_1$ is an integer and the prefix is at least $\max_p l_p$, symbol $m$ arrives at bin

$$q = (m + a_p - 2Nc_1 l_p) \bmod N$$

with the factor $h_p e^{j2\pi(c_1 l_p^2 - m l_p/N + c_2(m^2 - q^2))}$. So $H$ has one entry per path in each column. With $c_1 = 0$, paths with the same Doppler and different delays fall on the same bin and only add up, as in OFDM.

**Choosing $c_1$.** With $a_{\max}$ the largest Doppler size, take $c_1 = (2a_{\max} + 1)/(2N)$. Then $2Nc_1 l_p = (2a_{\max} + 1) l_p$: each delay step moves the bin by more than the whole Doppler range, so all pairs $(l_p, a_p)$ with $0 \le l_p \le l_{\max}$ and $|a_p| \le a_{\max}$ give different bins when $(l_{\max} + 1)(2a_{\max} + 1) \le N$. The second rate $c_2$ does not move the bins; it changes the phases, and the paper discusses its choice.

**Cost.** Lines L1 and L4 cost one FFT of size $N$ and two chirp multiplications, $O(N \log N)$. Line L5 with a dense LMMSE solve costs $O(N^3)$; detectors that use the sparsity of $H$ cost much less.

## Classic examples

**A single pilot.** With $N = 32$, $a_{\max} = 1$, so $c_1 = 3/64$ and $2Nc_1 = 3$, and three paths $(l_p, a_p) = (0, 0), (1, 1), (2, -1)$, a block with one symbol 1 on bin 10 and zeros elsewhere arrives as exactly three nonzero values: on bins $10$, $10 + 1 - 3 = 8$ and $10 - 1 - 6 = 3$, with sizes $|h_p|$. All 9 pairs with $l_p \le 2$ and $|a_p| \le 1$ give different bins, since $3 \cdot 3 \le 32$. With $c_1 = 0$, two paths with the same Doppler 1 and delays 0 and 2 both put their copy of bin 10 on bin 11.

**Round trip.** With the same paths, $c_2 = \sqrt 2/(8N)$ and a prefix of 4 samples, 32 random QPSK symbols go through lines L1 to L5 with $H$ from the formula above and noise variance 0, and come back with an error below $10^{-9}$.

## Variations

- **Detectors.** Message passing, as for OTFS, and other sparse detectors use the few entries per column of $H$. Maximum likelihood is the reference for small blocks.
- **Fractional Doppler.** A Doppler shift between bins spreads each path over neighboring bins. A guard of extra bins in the choice of $c_1$ absorbs part of this spread.
- **Embedded pilots.** One pilot with zero guard bins around it, as in the first example, estimates the paths within the data block.
- **Chirp multicarrier relatives.** Orthogonal chirp-division multiplexing uses the discrete Fresnel transform, a fixed chirp choice, while AFDM tunes $c_1$ to the channel.

## Pitfalls

- **Chirp rate not matched to the channel.** Line L1 with $c_1$ too small lets paths with different delays share a bin, and line L5 loses the diversity. Choose $c_1 = (2a_{\max} + 1)/(2N)$ or larger, within the condition above.
- **Plain cyclic prefix for any $c_1$.** Line L2 with the factor left out is only correct when $2Nc_1$ is an integer and $N$ is even. Keep the factor $e^{-j2\pi c_1 (N^2 + 2Nn)}$.
- **Non-integer $2Nc_1$.** The formula for $H$ in line L5 needs $2Nc_1$ to be an integer; otherwise each path spreads over many bins. Round $c_1$ to a multiple of $1/(2N)$.
- **Conjugate chirps.** Line L4 must use $-c_1$ and $-c_2$, the conjugates of the chirps of line L1. The same sign on both sides leaves a chirp on the data.
- **Delay longer than the prefix.** Line L2 with a prefix shorter than the largest delay breaks the circular model of line L5. Make the prefix at least $l_{\max}$ samples.

## Exercises

1. Show that the chirp-periodic prefix of line L2 makes the formula of line L1 hold for $-cp \le n < 0$.
2. Derive the bin $q$ and the phase factor for one path with delay $l_p$ and Doppler $a_p$.
3. Show that with $c_1 = (2a_{\max} + 1)/(2N)$ and $(l_{\max} + 1)(2a_{\max} + 1) \le N$ no two paths share a bin.
4. Show that $c_1 = c_2 = 0$ gives OFDM with a cyclic prefix and a channel matrix that is diagonal when all Dopplers are 0.
5. For $N = 64$, find the largest $l_{\max}$ that keeps all paths apart when $a_{\max} = 2$.

## References
