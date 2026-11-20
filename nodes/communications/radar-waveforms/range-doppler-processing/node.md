---
tag: YRN86W
kind: algorithm
slug: range-doppler-processing
name: Range-Doppler processing
aliases:
- pulse-Doppler processing
- range-Doppler map
area: communications/radar-waveforms
level: core
summary: "Applies the matched filter to each pulse in fast time, then a windowed FFT across the pulses at each range bin, which gives a map of target power over range and Doppler."
model: real-ram
complexity:
  vars: {P: "the number of pulses, a power of two", N: the number of samples per pulse, L: the length of the pulse}
  time: {worst: Θ(P N L + N P log P), average: Θ(P N L + N P log P), best: Θ(P N L + N P log P)}
  space: {extra: Θ(P N)}
properties: {deterministic: true, linear: true, coherent: true, processing_gain: "L P for a unit-modulus pulse and a rectangular window", doppler_aliasing: "modulo the PRF"}
prereqs: [pulse-compression, matched-filter, fast-fourier-transform, window-functions]
see_also: [moving-target-indication, cfar-detection, ambiguity-function, range-doppler-coupling, spectral-leakage, fmcw-radar, space-time-adaptive-processing, range-doppler-algorithm]
sources:
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 5, Section 5.3 (the DFT of the slow-time data, windows, straddle loss and Doppler ambiguity)"
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 3, MTI and Pulse Doppler Radar (pulse Doppler radar, range and Doppler ambiguities)"
---

Range-Doppler processing turns the returns of a train of $P$ coherent pulses into a two-dimensional map of power over range and radial speed. For each pulse it applies the [matched filter](/matched-filter/) of the transmitted pulse along fast time, which is [pulse compression](/pulse-compression/), and then, for each range bin, it takes a windowed [FFT](/fast-fourier-transform/) across the pulses along slow time. A point target gives a peak at its delay and its Doppler bin, with the coherent gain $L P$ over the noise of one sample. The [CFAR detector](/cfar-detection/) then runs on the map. The page [range-Doppler algorithm](/range-doppler-algorithm/) has a similar name but is a SAR image formation algorithm, which focuses a synthetic aperture image, not the detection map of range and speed described here.

## In plain words

A radar sends the same pulse $P$ times, at a fixed interval. Put the samples of each echo in a row of a table, so that the columns are the ranges. First, correlate each row with the pulse, so that each target becomes a sharp peak at its range. Then look down each column. A target that moves turns its phase by the same step from one pulse to the next, so down the column you see a complex sinusoid. Its frequency is the Doppler shift, and an FFT down the column finds it. Each column becomes a spectrum, and the table becomes a map: one axis is range, the other is speed. Fixed clutter goes to the zero speed row, and moving targets go to other rows.

## The problem

The input is a $P \times N$ array $x[p][n]$ of complex baseband samples, pulse $p = 0, \dots, P - 1$ (slow time, one row per pulse repetition interval) and sample $n = 0, \dots, N - 1$ (fast time), the pulse $s[0], \dots, s[L-1]$ with $1 \le L \le N$, and a window $w[0], \dots, w[P-1]$. $P$ is a power of two. The output is the map

$$D[k][r] = \sum_{p=0}^{P-1} w[p] \left( \sum_{l=0}^{L-1} \overline{s[l]}\, x[p][r + l] \right) e^{-j 2\pi k p / P}$$

for the Doppler bins $k = 0, \dots, P - 1$ and the range bins $r = 0, \dots, N - L$. Bin $k$ is the Doppler frequency $k\,\mathrm{PRF}/P$ for $k < P/2$ and $(k - P)\,\mathrm{PRF}/P$ for $k \ge P/2$, and the radial speed is $v = f_d \lambda / 2$.

## The algorithm

```pseudo id=main
RANGE-DOPPLER(x[0..P-1][0..N-1], s[0..L-1], w[0..P-1])
L1  for p <- 0 to P - 1                                            ▷ fast time: matched filter of each pulse
L2      for r <- 0 to N - L
L3          z[p][r] <- sum over l = 0, ..., L - 1 of conj(s[l]) * x[p][r + l]
L4  for r <- 0 to N - L                                            ▷ slow time: Doppler spectrum of each range bin
L5      u[p] <- w[p] * z[p][r] for p = 0, ..., P - 1
L6      D[0..P-1][r] <- FFT(u)
L7  return D
```

Lines L1 to L3 compress each pulse: the correlation with the conjugated pulse is the matched filter, and only the $N - L + 1$ lags where the whole pulse fits in the samples are kept. Line L5 applies the window along slow time, and line L6 takes the FFT of length $P$ of each column. The implementation uses an iterative radix-2 FFT with a bit reversal permutation. For long pulses, lines L1 to L3 are also done with FFTs: a fast convolution of each row.

## Example

Take $P = 4$ pulses of $N = 5$ samples, the pulse $s = (1, 1)$ of length $L = 2$, a rectangular window, and one target with amplitude 1, delay 1 and Doppler $f_d = \mathrm{PRF}/4$. The target turns a quarter cycle per pulse, so $x[p][n] = j^p s[n - 1]$, and row $p$ is $(0, j^p, j^p, 0, 0)$.

| step | $r = 0$ | $r = 1$ | $r = 2$ | $r = 3$ |
|---|---|---|---|---|
| $z[p][r]$ after line L3 | $j^p$ | $2 j^p$ | $j^p$ | $0$ |
| $D[0][r]$ | 0 | 0 | 0 | 0 |
| $D[1][r]$ | 4 | 8 | 4 | 0 |
| $D[2][r]$ | 0 | 0 | 0 | 0 |
| $D[3][r]$ | 0 | 0 | 0 | 0 |

The FFT of $(1, j, -1, -j)$ is $(0, 4, 0, 0)$, so all the energy goes to Doppler bin 1. The peak is $D[1][1] = 8 = E_s P$, with the pulse energy $E_s = 2$, at the true delay. The values 4 at $r = 0$ and $r = 2$ are the range sidelobes of the pulse, the autocorrelation $(1, 2, 1)$ of $s$.

A larger case: at 10 GHz with a PRF of 10 kHz and $P = 16$, the Doppler bins are $10\,000/16 = 625$ Hz apart, which is 9.37 m/s. Bin 3 is 1875 Hz, or 28.11 m/s, and bin 13 is bin $-3$, a target moving away at 28.11 m/s. The unambiguous speeds are $\pm 74.95$ m/s and the unambiguous range is $c/(2\,\mathrm{PRF}) = 14.99$ km. With the 13-chip Barker code, the gain is $L P = 208$, or 23.18 dB.

## Correctness

Lines L1 to L3 compute the inner sum of the definition for every pair $(p, r)$, and every index $r + l$ is at most $N - 1$. The radix-2 FFT returns the DFT of its input, which is proved by induction on the block size after the bit reversal. Line L6 applies it to $w[p] z[p][r]$, which gives the outer sum. For a point target $a\, e^{j 2\pi \phi p} s[n - r_0]$, the Cauchy-Schwarz inequality bounds $|z[p][r]|$ by $|a| E_s$, with equality at $r = r_0$. When $\phi = k_0/P$, the column at $r_0$ is a sampled sinusoid on a DFT bin, so the map has the value $a E_s P$ at $(k_0, r_0)$ for a rectangular window and 0 in the other bins of that column. White noise of power $N_0$ gives $E|D|^2 = N_0 E_s \sum_p |w[p]|^2$. The [correctness proof](proofs/correctness.md) gives the full arguments.

## Complexity

**Time.** Lines L1 to L3 do $L$ multiplications for each of the $P (N - L + 1)$ outputs, which is $\Theta(P N L)$ for $L \le N/2$. The FFT of line L6 costs $\Theta(P \log P)$, and it runs $N - L + 1$ times, which is $\Theta(N P \log P)$. The total is $\Theta(P N L + N P \log P)$ in every case. With fast convolution, the matched filter costs $O(P N \log N)$ instead. A direct DFT in place of line L6 would cost $\Theta(N P^2)$; the tests use that form as the reference.

**Space.** $\Theta(P N)$ for the compressed data $z$, beyond the input and the map.

## Properties

- **The peak and the gain (theorem).** A target on a Doppler bin gives $|D| = |a| E_s \sum_p w[p]$ at its delay. With a unit-modulus pulse and a rectangular window, the signal to noise ratio at the peak is $L P$ times the ratio of one input sample.
- **Doppler resolution and ambiguity.** The bins are $\mathrm{PRF}/P$ apart, and the Doppler is known only modulo the PRF: $f_d$ and $f_d + \mathrm{PRF}$ give the same map. The range is known only modulo $c/(2\,\mathrm{PRF})$. A low PRF gives a long unambiguous range and a small unambiguous speed, and a high PRF gives the reverse.
- **Straddle loss.** A target between two bins loses gain. Half way between, the rectangular window loses $20 \log_{10}(\pi/2) = 3.92$ dB.
- **Windows trade resolution for sidelobes.** A Hamming window lowers the Doppler sidelobes to about $-43$ dB from $-13$ dB, at the cost of a wider peak and a loss in signal to noise ratio by the factor $(\sum w)^2 / (P \sum w^2)$, 1.44 dB for a Hamming window of 32 pulses. In the tests, with $P = 32$ and a target half way between bins 5 and 6, the Hamming map is more than 40 dB down at 8 or more bins from the target, and the rectangular map is not. See [spectral leakage](/spectral-leakage/).
- **Linear.** The map of a sum of targets is the sum of their maps, so weak targets can hide in the sidelobes of strong ones.

## Variants and improvements

- **Zero padding.** Pad each column to a length larger than $P$ before the FFT. This samples the spectrum more finely and lowers the straddle loss, but it does not improve the resolution.
- **MTI first.** Apply a two- or three-pulse [MTI canceller](/moving-target-indication/) along slow time before the FFT, to lower the zero Doppler clutter before it can leak into other bins through the sidelobes.
- **Multiple PRFs.** Process several dwells at different PRFs and solve for the true range and Doppler with the Chinese remainder theorem or a search.
- **FMCW radar.** In an [FMCW radar](/fmcw-radar/) the range FFT of the beat signal of each chirp replaces lines L1 to L3, and the Doppler FFT across chirps is the same as line L6.
- **Range migration.** If the target moves more than one range bin during the dwell, its energy spreads over several columns. Keystone processing or a search over speed corrects this.
- **Adaptive processing.** With several antennas, [space-time adaptive processing](/space-time-adaptive-processing/) replaces the fixed window and FFT with adaptive weights over angle and Doppler.

## When to use it

Use range-Doppler processing when a radar has a coherent train of many pulses on the same target, for example 16 to 256 pulses, and needs both the range and the radial speed: airborne and ground surveillance, weather radar, automotive radar and the tracking modes of military radars. With only two or three pulses per dwell, use [MTI](/moving-target-indication/). For an image of a fixed scene from a moving platform, use SAR processing instead.

## Pitfalls

- **No conjugate in line L3.** The matched filter correlates with $\overline{s}$. For a real code such as Barker the conjugate does nothing, so a test with Barker codes alone will not find this bug. For a complex pulse, such as an LFM chirp or a Frank code, a missing conjugate gives a smeared peak at the wrong place.
- **The FFT along the wrong axis in line L6.** The Doppler FFT is down each column (over $p$ at a fixed $r$). An FFT along each row (over range) gives a meaningless spectrum.
- **Reading the bins as positive speeds.** Bins $k \ge P/2$ are negative Doppler frequencies, targets moving away. Shift the map by $P/2$ for display, and do not compute the speed as $k\,\mathrm{PRF}/P$ for every $k$.
- **No window in line L5.** With $w = 1$, the first Doppler sidelobe is only 13 dB down. Strong clutter at zero Doppler then leaks into every bin and masks weak moving targets.
- **Range bins near the end of the row.** Line L2 stops at $N - L$. Lags beyond that would read past the end of the row, or, with circular convolution by FFT, wrap the end of the row onto its start.
- **A noise floor that changes with the window.** The noise in the map is $N_0 E_s \sum_p |w[p]|^2$, not $N_0 E_s P$. A CFAR threshold set for one window is wrong for another unless it is set from the data.

## Implementations

## History

Radars that measure range and Doppler together with a coherent pulse train came into use in airborne radars, to see targets against ground clutter. The Doppler filters were first analog filter banks, and the FFT, published by Cooley and Tukey in 1965, later made digital Doppler filter banks practical. Skolnik and Richards describe this processing in their textbooks.

## References
