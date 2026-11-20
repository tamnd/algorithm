---
tag: NZHGJE
kind: algorithm
slug: parallel-code-phase-search
name: Parallel code phase search
aliases:
- FFT-based code acquisition
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Correlates a received block with a spreading code at all code phases at once: an FFT, a product with the conjugate code FFT and an inverse FFT per carrier offset. Standard in software GNSS receivers."
solves: [signal-detection]
model: real-ram
complexity:
  vars: {F: the number of carrier offsets, N: "the block length in samples, with bounded prime factors"}
  time: {worst: "Θ(F N log N)"}
  space: {extra: Θ(N)}
properties: {deterministic: true, exhaustive: true, circular_correlation: true, needs_full_code_period: true}
history:
  year: 1991
  people: [R. D. J. van Nee, A. J. R. M. Coenen]
  note: Van Nee and Coenen proposed in 1991 to acquire the GPS C/A code with FFTs, computing the correlations for all code phases at once.
prereqs: [fast-fourier-transform, circular-convolution, cross-correlation, serial-search-code-acquisition]
see_also: [discrete-fourier-transform, delay-locked-loop, frequency-offset-estimation, preamble-correlation-detection, direct-sequence-spread-spectrum, maximal-length-sequence, autocorrelation, zadoff-chu-sequence]
sources:
  - paper: doi:10.1049/el:19910102
    title: R. D. J. van Nee and A. J. R. M. Coenen, New fast GPS code-acquisition technique using FFT, Electronics Letters 27(2), 1991
    locator: pp. 158 to 160
  - book: isbn:9780817643904
    title: Kai Borre, Dennis M. Akos, Nicolaj Bertelsen, Peter Rinder and Søren Holdt Jensen, A Software-Defined GPS and Galileo Receiver, Birkhäuser, 2007
    locator: Section 6.4, p. 81 (parallel code phase search acquisition); Section 6.3, p. 78 (the parallel search over frequency)
---

Parallel code phase search finds the code phase and the carrier offset of a spread-spectrum signal by computing the correlation of a received block with the local code at **all** code phases at once. For each candidate carrier offset, it removes the carrier, takes the FFT of the block, multiplies it by the conjugate FFT of the code, and takes the inverse FFT. The result is the circular [cross-correlation](/cross-correlation/) at every code phase. The cell with the largest magnitude gives the code phase and the offset. A [serial search](/serial-search-code-acquisition/) needs one dwell per code phase. The parallel search needs one block and $O(N \log N)$ work per carrier offset. It is the usual acquisition in software receivers for GPS and Galileo, before a [delay-locked loop](/delay-locked-loop/) takes over.

## In plain words

You have a copy of a long beep pattern, and you have recorded a short piece of the signal. You want to know where the pattern starts in your recording.

The slow way is to slide your copy one step at a time and score each position. The fast way uses a trick: break the recording and your copy into pure tones, combine them tone by tone, and turn the result back. This gives the scores for every position at the same time, for much less work.

The transmitter may also be a little off in frequency, because it moves. So you repeat the trick for a few guesses of the frequency error. The best score over all guesses tells you both the start and the frequency error.

## The problem

The received block has $N$ samples, one per chip here:
$$x[n] = A\, e^{j 2\pi \nu n / N}\, c[(n - \tau) \bmod N] + w[n], \qquad n = 0, \ldots, N - 1,$$
with a known periodic code $c$ of unit energy, an unknown code phase $\tau$, an unknown carrier offset $\nu$ in cycles per block, and noise $w[n] \sim \mathcal{CN}(0, N_0)$. The task is to compute, for each candidate offset $\nu_i$ and each phase $t$,
$$S_i[t] = \sum_{n} x[n]\, e^{-j 2\pi \nu_i n / N}\, \overline{c[(n - t) \bmod N]},$$
and to find the cell with the largest $|S_i[t]|^2$. The receiver then compares that peak with a threshold, as in any [signal detection](/signal-detection/) problem.

## The algorithm

```pseudo id=main
PCPS(x, c, ν_1, …, ν_F)
L1  C ← conj(FFT(c))                          ▷ once per code
L2  for i ← 1 to F do
L3      y[n] ← x[n] · e^{-j2π ν_i n / N} for all n    ▷ carrier wipe-off
L4      R_i ← IFFT(FFT(y) · C)                ▷ R_i[t] = Σ_n y[n] conj(c[(n - t) mod N])
L5      t_i ← argmax_t |R_i[t]|
L6  return the (i, t_i) with the largest |R_i[t_i]|², and the rows R_i
```

L4 uses the correlation theorem: the DFT of the circular cross-correlation $\rho[t] = \sum_n y[n]\, \overline{c[n - t]}$ is $Y[k]\, \overline{C[k]}$. The FFT of the code does not depend on the received data, so it is computed once and stored. A frequency error $\delta = \nu - \nu_i$ lowers the peak by the factor $D_N(\delta) = |\sin(\pi\delta) / (N \sin(\pi\delta/N))|$, close to $|\operatorname{sinc}(\delta)|$. This loss sets the spacing of the carrier offsets.

## Example

**A small search.** Take the m-sequence of length $N = 63$ with unit energy, $A = 1$, no noise, $\tau = 40$ and a carrier offset of $\nu = 0.3$ cycles per block. Search the offsets $-0.5$, $0$ and $0.5$.

| $\nu_i$ | $\lvert R_i[40]\rvert^2$ | largest $\lvert R_i[t]\rvert^2$, $t \ne 40$ |
|---|---|---|
| $-0.5$ | 0.0547 | 0.0446 |
| $0$ | 0.7369 | 0.0308 |
| $0.5$ | 0.8752 | 0.0156 |

The search returns the offset $0.5$ and the phase $40$. The peak $0.8752$ is $D_{63}(0.2)^2$, the loss for the remaining error of $0.2$ cycles. In the row for $-0.5$, the error is $0.8$ cycles, and the peak almost disappears into the side values.

**GPS numbers.** A 1 ms block searched with carrier bins 500 Hz apart has a worst error of 250 Hz, which is $0.25$ cycles per block. The loss is $20 \log_{10} D(0.25) = -0.91$ dB. With bins 1 kHz apart it would be $-3.92$ dB.

**Work.** For $F = 41$ offsets and $N = 1024$ samples, the direct sums need $F N^2 = 42{,}991{,}616$ complex multiply-adds. With radix-2 FFTs of $(N/2) \log_2 N = 5120$ complex multiplications each, the search needs $41 \cdot (2 \cdot 5120 + 1024) + 5120 = 466{,}944$, about 92 times fewer.

## Correctness

By the correlation theorem, the inverse DFT of $Y[k]\, \overline{C[k]}$ is the circular cross-correlation of $y$ and $c$, and $y$ is the block with the carrier for $\nu_i$ removed. So L4 computes $R_i[t] = S_i[t]$ for every phase $t$ in one pass. The mixed-radix FFT computes the DFT by splitting the index $n = p s + r$ and using $W_N^{p s k} = W_m^{s k}$, which proves it correct by induction on $N$. L5 and L6 then take the largest value over all cells. The loss formula follows from summing the geometric series $\sum_n e^{j 2\pi \delta n / N}$ when all chips have the same magnitude. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/) model, one FFT of length $N$ costs $O(N \log N)$ when the prime factors of $N$ are bounded, for example when $N$ is a power of two. Each offset costs two FFTs and $O(N)$ other operations, so the search costs $\Theta(F N \log N)$, plus one FFT of the code. The direct correlations cost $\Theta(F N^2)$. The extra space is $\Theta(N)$ for one row; keeping all rows for a later threshold test takes $\Theta(F N)$.

## Properties

- **Exhaustive.** Every cell of the grid is computed, so the result does not depend on a search order, and the peak can be compared with all other cells, for example by the ratio of the highest to the second-highest peak.
- **Same statistics as a dwell.** Each $S_i[t]$ is exactly the correlator output of a serial search at that cell, on the same block. Only the cost differs.
- **Circular.** The FFT computes a circular correlation. It equals the true correlation only when the block holds whole periods of a periodic code.
- **Loss between bins.** The peak loss is $D_N(\delta)$ for a frequency error $\delta$, and the code phase is found to the nearest sample.

## Variants and improvements

- **Parallel frequency search.** Multiply the block by the code at one phase and take an FFT over the carrier; this searches all offsets at once for one phase. Borre and coauthors describe it next to the code phase search.
- **Longer integration.** Add the powers $|R_i[t]|^2$ of several blocks (noncoherent) or the complex values (coherent) to detect weak signals. Coherent addition needs finer frequency bins.
- **Shifting in frequency.** A cyclic shift of $\mathrm{FFT}(x)$ by one bin is a carrier offset of one cycle per block, so integer offsets need no new FFT of the block.
- **Finer phase.** Interpolate between samples around the peak, or use more samples per chip, before handing the phase to the tracking loop.

## When to use it

Use the parallel code phase search when the receiver has a processor that can run FFTs and the code period fits in one block, as for the 1023-chip GPS C/A code with 1 ms blocks. It is the standard first step of software receivers. For very long codes, a serial search over a window of phases, or a hardware bank of correlators, may be cheaper. For a known preamble in a burst, the same correlation is [preamble correlation detection](/preamble-correlation-detection/).

## Pitfalls

- **Zero padding breaks the circular model.** Padding the block with zeros to reach a power of two changes the circular correlation of a periodic code into something else, and the peak shrinks. Resample to a convenient length, or use an FFT that handles the actual length.
- **Data bit changes.** A data bit transition inside the block can cancel part of the peak. When a data bit lasts much longer than a block, a transition can affect at most one of two consecutive blocks, so searching both and keeping the better result avoids the loss.
- **Too coarse frequency bins.** The loss grows fast with the frequency error: $0.91$ dB at a quarter of a cycle per block, $3.92$ dB at half a cycle.
- **Code Doppler over long integrations.** Motion also stretches the code. Over long integrations the code phase drifts by more than a sample, and the peak spreads.
- **Peak at the edge.** The phase is circular, so a peak at $t = N - 1$ is next to the one at $t = 0$. Interpolation and tracking must handle the wrap.

## Implementations

## History

R. D. J. van Nee and A. J. R. M. Coenen proposed the FFT-based acquisition of the GPS C/A code in Electronics Letters in 1991. It replaced the code phase search of serial receivers with one circular correlation per frequency bin. With software receivers, which run all signal processing on a general processor, it became the standard acquisition method, as in the receiver of Borre and coauthors.

## References
