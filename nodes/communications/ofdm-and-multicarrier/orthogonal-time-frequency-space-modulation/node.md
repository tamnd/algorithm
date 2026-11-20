---
tag: 6XP9EH
kind: technique
slug: orthogonal-time-frequency-space-modulation
name: Orthogonal time frequency space modulation
aliases:
- OTFS
area: communications/ofdm-and-multicarrier
level: research
summary: "Places the symbols on a delay-Doppler grid and spreads each over the whole time-frequency frame. A channel of few paths becomes a sparse, nearly constant shift on that grid."
prereqs: [orthogonal-frequency-division-multiplexing, doppler-spread, delay-spread, discrete-fourier-transform]
see_also: [affine-frequency-division-multiplexing, generalized-frequency-division-multiplexing, universal-filtered-multicarrier, mmse-linear-equalizer, message-passing, coherence-time, wssus-channel-model, peak-to-average-power-ratio]
sources:
  - paper: doi:10.1109/WCNC.2017.7925924
    title: "R. Hadani, S. Rakib, M. Tsatsanis, A. Monk, A. J. Goldsmith, A. F. Molisch and R. Calderbank, Orthogonal time frequency space modulation, IEEE Wireless Communications and Networking Conference (WCNC), 2017, pages 1 to 6"
    locator: "the proposal of OTFS, the ISFFT and the Heisenberg transform at the transmitter, and the delay-Doppler view of the channel"
  - paper: doi:10.1109/TWC.2018.2860011
    title: "P. Raviteja, Khoa T. Phan, Yi Hong and Emanuele Viterbo, Interference cancellation and iterative detection for orthogonal time frequency space modulation, IEEE Transactions on Wireless Communications 17(10), 2018, pages 6501 to 6515"
    locator: "the delay-Doppler input-output relation for rectangular pulses and the message passing detector"
---

Orthogonal time frequency space (OTFS) modulation, proposed by Hadani and coauthors in 2017, places the data symbols on a grid of $N$ Doppler bins by $M$ delay bins, not on a grid of time and frequency as [OFDM](/orthogonal-frequency-division-multiplexing/) does. A two-dimensional transform, the inverse symplectic finite Fourier transform (ISFFT), spreads each symbol over the whole time-frequency frame of $N$ OFDM-like symbols of $M$ subcarriers. In the delay-Doppler domain a channel of $P$ paths, each with a delay and a Doppler shift, acts as a sum of $P$ two-dimensional circular shifts with phase factors. This channel is sparse and changes slowly compared with the time-frequency channel, which changes from symbol to symbol under high Doppler. Every symbol meets every path, so a good detector can collect the diversity of all the paths. The cost is a joint detection over the frame. The page uses $j$ for the imaginary unit and rectangular pulses with one [cyclic prefix](/cyclic-prefix/) per frame.

## In plain words

A fast-moving receiver sees each echo of the signal arrive with its own delay and its own small frequency shift. In OFDM these effects make each subcarrier fade and leak into its neighbors from one symbol to the next. OTFS puts the data on a grid whose two axes are delay and frequency shift. On this grid each echo only moves the data a fixed number of steps and turns it a little, the same for the whole frame. The receiver finds a few echoes, not a separate channel for each subcarrier and time, and every data symbol reaches it along every echo.

## When it applies

- The channel has a few dominant paths with large Doppler shifts, for example high-speed trains, vehicles, aircraft or satellites, where the channel changes within an OFDM frame.
- The delay spread fits in one prefix, and the paths keep their delays and Doppler shifts over the frame of $N$ symbols.
- The receiver can afford a detector that uses the whole frame, such as LMMSE with a sparse matrix or message passing.
- An existing OFDM modem can be reused: OTFS adds the ISFFT before an OFDM transmitter and the SFFT after an OFDM receiver.

## The template

```pseudo id=main
OTFS(x[0..N-1][0..M-1], paths, cp)                ▷ x[k][l]: Doppler bin k, delay bin l
L1  X[n][m] ← (1/√(NM)) Σ_k Σ_l x[k][l] e^{j2π(nk/N - ml/M)}     ▷ ISFFT
L2  s ← for n = 0..N-1, the unitary M-point inverse DFT of X[n], concatenated   ▷ Heisenberg transform
L3  send (s[MN-cp..MN-1], s)                       ▷ one prefix for the frame
L4  Y[n] ← the unitary M-point DFT of segment n of the received frame   ▷ Wigner transform
L5  y ← SFFT(Y), the inverse of line L1
L6  x̂ ← the solution of y = G x by LMMSE or message passing, with G built from the paths
```

**The frame in one step.** With rectangular pulses, lines L1 and L2 together are an inverse DFT along the Doppler axis alone: $s[nM + l] = \frac{1}{\sqrt N}\sum_k x[k][l]\, e^{j2\pi nk/N}$. The DFT along delay in line L1 and the inverse DFT in line L2 cancel.

**The channel on the grid.** Let path $p$ have gain $h_p$, delay $l_p$ samples and Doppler $k_p/(MN)$ cycles per sample, so that $r[q] = \sum_p h_p e^{j2\pi k_p (q - l_p)/(MN)} s[q - l_p]$. For integer $l_p$ and $k_p$ and a prefix of at least $\max_p l_p$ samples, the symbol at $(k, l)$ arrives at $((k + k_p) \bmod N, (l + l_p) \bmod M)$ with the factor $h_p e^{j2\pi k_p l/(MN)}$, and one more factor $e^{-j2\pi k'/N}$ if $l + l_p \ge M$, where $k'$ is the new Doppler index. So $G$ has exactly $P$ nonzero entries in each column. A Doppler shift that is not a multiple of $1/(MN)$ spreads each path over neighboring Doppler bins.

**Peak power.** Each sample of the frame is a sum of $N$ symbols with unit-size weights over $\sqrt N$, so for constant-envelope symbols the [peak-to-average power ratio](/peak-to-average-power-ratio/) is at most $N$, against $MN$ for OFDM with $MN$ subcarriers. All $N$ symbols of one delay bin set to 1 reach the bound.

**Cost.** Lines L1, L2, L4 and L5 cost $O(MN \log(MN))$ with FFTs. Line L6 with a dense LMMSE solve costs $O((MN)^3)$; detectors that use the sparsity of $G$, such as message passing, have a cost per iteration that grows linearly with $MN$ and with $P$.

## Classic examples

**A single pilot.** With $N = 8$, $M = 16$ and three paths $(l_p, k_p) = (0, 0), (1, 2), (3, -1)$, a frame with one symbol 1 at $(k, l) = (2, 5)$ and zeros elsewhere arrives as exactly three nonzero values, at $(2, 5)$, $(4, 6)$ and $(1, 8)$, with sizes $|h_p|$. Pilots of this kind, with a guard of zeros around them, are a common way to estimate the paths.

**Diversity with LMMSE.** $N = 4$, $M = 8$, QPSK, 1500 frames (48000 symbols), ideal channel knowledge. The path gains are independent complex Gaussian with total mean power 1. OTFS uses delays 0, 1, 2 and Dopplers 0, 1, $-1$ and the LMMSE detector of line L6. OFDM uses the same gains and delays with no Doppler at all, its best case, and a one-tap equalizer per subcarrier. The table lists the symbol error rates.

| SNR | paths | OTFS with LMMSE | OFDM, one tap |
|---|---|---|---|
| 10 dB | 1 | 0.0839 | 0.0833 |
| 10 dB | 3 | 0.0621 | 0.0765 |
| 20 dB | 1 | 0.0115 | 0.0119 |
| 20 dB | 3 | 0.0021 | 0.0089 |

With one path both schemes see one flat fade. With three paths each OFDM subcarrier still sees one Rayleigh-faded gain, but each OTFS symbol meets all three paths, and the error rate at 20 dB falls by a factor of about 4.

## Variations

- **Detectors.** Message passing on the sparse factor graph of $G$, as in Raviteja and coauthors, and iterative interference cancellation scale to large frames. Maximum likelihood is the reference for small frames.
- **Prefix per symbol.** A prefix on each of the $N$ segments, in place of one per frame, makes each segment circular on its own and changes the phase factors at the delay wrap, at a higher overhead.
- **Pulse shapes.** Pulses other than the rectangle reduce the leakage of fractional Doppler shifts.
- **Zak-transform form.** The same frame can be written with the discrete Zak transform, which makes the delay-Doppler grid the primary domain and avoids the time-frequency step.
- **Embedded pilots.** A pilot with a guard region in the delay-Doppler grid, as in the first example, estimates the paths in the same frame as the data.

## Pitfalls

- **Wrong axis order.** In line L1 the sign of the exponent is $+$ for Doppler and $-$ for delay. Swapping them in line L1 but not in line L5 moves the data to the wrong bins.
- **Missing wrap phase.** Building $G$ for line L6 without the factor $e^{-j2\pi k'/N}$ for $l + l_p \ge M$ gives a wrong model for the paths that cross the delay edge and an error floor. Add the factor, or use one prefix per segment.
- **Prefix too short.** Line L3 with a prefix shorter than the largest delay breaks the circular model of line L6. Make the prefix at least $\max_p l_p$ samples.
- **Fractional Doppler ignored.** Line L6 with integer $k_p$ only, when the true shift lies between bins, leaves interference from the spread. Model the spread or use a larger $N$.
- **One-tap equalizer.** Dividing $y$ by one gain per bin in line L6, as in OFDM, ignores the other paths. The delay-Doppler channel is a sum of shifts, not a diagonal matrix.

## Exercises

1. Show that with rectangular pulses lines L1 and L2 give $s[nM + l] = \frac{1}{\sqrt N}\sum_k x[k][l] e^{j2\pi nk/N}$.
2. Derive the input-output relation for one path with delay $l_p$ and Doppler $k_p$, including the extra phase when $l + l_p \ge M$.
3. Show that the map $x \mapsto y$ for one path is $h_p$ times a unitary map, and conclude that $G$ for one path with $h_p \ne 0$ is invertible.
4. Prove that the peak-to-average power ratio of the frame is at most $N$ for constant-envelope symbols.
5. With $N = M = 8$ and paths of delays at most 2 and Dopplers at most 1 in size, how large must the zero guard around one pilot be so that the pilot response does not overlap the data?

## References
