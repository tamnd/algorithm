---
tag: GWPD9C
kind: algorithm
slug: selected-mapping
name: Selected mapping
aliases:
- SLM
area: communications/ofdm-and-multicarrier
level: core
summary: "Lowers the PAPR of OFDM by forming U phase-rotated copies of a symbol and sending the one with the lowest peak, plus its index. No distortion; costs U inverse FFTs."
model: real-ram
complexity:
  vars: {U: the number of phase sequences, N: the number of subcarriers, L: the oversampling factor}
  time: {worst: O(U L N log(L N))}
  space: {extra: O(L N)}
properties: {deterministic: true, distortionless: true, side_information: true, never_worse_than_plain_ofdm: true}
history:
  year: 1996
  people: [R. W. Bäuml, Robert F. H. Fischer, Johannes B. Huber]
  note: "Bäuml, Fischer and Huber proposed selected mapping in 1996: generate several statistically equivalent versions of the multicarrier symbol and transmit the one with the lowest peak."
prereqs: [peak-to-average-power-ratio, orthogonal-frequency-division-multiplexing]
see_also: [partial-transmit-sequence, iterative-clipping-and-filtering, tone-reservation, active-constellation-extension, walsh-hadamard-transform, fast-fourier-transform, quadrature-amplitude-modulation, sc-fdma]
sources:
  - paper: doi:10.1049/el:19961384
    title: "R. W. Bäuml, R. F. H. Fischer and J. B. Huber, Reducing the peak-to-average power ratio of multicarrier modulation by selected mapping, Electronics Letters 32(22), 1996, pages 2056 to 2057"
    locator: "the set of phase sequences, the choice of the candidate with the lowest PAPR and the side information"
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the section on selected mapping, and the comparison of the methods by distortion, side information and cost"
---

Selected mapping (SLM) lowers the [peak-to-average power ratio](/peak-to-average-power-ratio/) (PAPR) of an [OFDM](/orthogonal-frequency-division-multiplexing/) symbol without distorting it. The transmitter and the receiver share $U$ phase sequences $P_1, \ldots, P_U$ of length $N$ whose entries have magnitude 1. For each data block $X$ the transmitter forms the $U$ candidates $X \odot P_u$, computes the PAPR of each one with an inverse FFT, and sends the candidate with the lowest PAPR together with its index, $\log_2 U$ bits of side information. The receiver multiplies each subcarrier by $\overline{P_u[k]}$ and gets $X$ back exactly. Bäuml, Fischer and Huber proposed it in 1996. It differs from [partial transmit sequences](/partial-transmit-sequence/), which rotate whole blocks of subcarriers and need only one inverse FFT per block, and from [clipping and filtering](/iterative-clipping-and-filtering/), which needs no side information but adds distortion. The page uses the unitary DFT pair $F[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, and $j$ is the imaginary unit.

## In plain words

The same data can be sent in several ways that the receiver can undo. For example, the sender can turn some symbols by a quarter turn, if the receiver knows which ones. Each way gives a different signal in time, and their peaks differ, because the peaks come from chance alignments of the tones. So the sender tries a fixed list of patterns, looks at the highest peak of each signal, and sends the best one. It also tells the receiver which pattern it chose. The receiver turns the symbols back. Nothing is lost or distorted. The cost is the extra work at the sender, one transform per pattern, and a few bits to name the pattern. If those bits arrive wrong, the whole symbol is lost.

## The problem

The input is a block of $N$ data symbols $X[0], \ldots, X[N-1]$, for example QPSK with $E|X[k]|^2 = 1$, an oversampling factor $L$, usually 4, and a table of $U$ phase sequences known to both ends. The output is an index $u^\ast$ and the oversampled OFDM symbol of $X \odot P_{u^\ast}$, such that

1. its PAPR is the smallest among the $U$ candidates, and
2. the receiver can recover $X$ exactly from the subcarrier values and $u^\ast$.

The first sequence is all ones, so plain OFDM is one of the candidates.

## The algorithm

```pseudo id=main
SLM(X[0..N-1], P[1..U][0..N-1], L)
L1  for u ← 1 to U
L2      X_u[k] ← X[k] · P_u[k] for every k                  ▷ |P_u[k]| = 1, P_1 is all ones
L3      x_u ← √L · F_LNᴴ (X_u with (L-1)N zeros in the middle)
L4      r_u ← max_m |x_u[m]|² / mean_m |x_u[m]|²
L5      if u = 1 or r_u < r_{u*} then u* ← u
L6  return u*, x_{u*}                                        ▷ send x_{u*} and the index u* (log₂ U bits)
```

Line L2 rotates each subcarrier. A common table uses entries from $\{1, -1, j, -j\}$, so that the product is a sign change or a swap of the real and imaginary parts and needs no multiplication. Line L3 is the inverse FFT of size $LN$ that builds the candidate oversampled by $L$; the zeros go in the middle of the spectrum because the indices $k \ge N/2$ are the negative frequencies. Line L4 measures the PAPR, and line L5 keeps the first candidate with the smallest value. Line L6 sends it. The receiver demodulates as usual, equalizes, and computes $X[k] = Y[k]\, \overline{P_{u^\ast}[k]}$.

## Example

Take $N = 64$ QPSK subcarriers and $L = 4$. For one block (Python `random.Random(1)`) and a table of $U = 4$ sequences, the first all ones and three random ones from $\{\pm 1, \pm j\}$, the four candidates have the PAPRs 6.94 dB, 7.47 dB, 6.66 dB and 6.39 dB. SLM sends the fourth candidate, 0.55 dB below plain OFDM, and the index 4 in 2 bits.

Over 500 random blocks (`random.Random(3)`, a fixed table of 16 sequences, and for each $U$ the first $U$ of them):

| $U$ | mean PAPR | 99 percent of blocks below | $\Pr(\mathrm{PAPR} > 7\ \mathrm{dB})$ | $\Pr(\mathrm{PAPR} > 8\ \mathrm{dB})$ | $0.638^U$ |
|---|---|---|---|---|---|
| 1 | 7.50 dB | 9.92 dB | 0.638 | 0.250 | 0.638 |
| 2 | 6.92 dB | 8.50 dB | 0.402 | 0.048 | 0.407 |
| 4 | 6.52 dB | 7.72 dB | 0.164 | 0.004 | 0.166 |
| 8 | 6.23 dB | 7.13 dB | 0.020 | none in 500 | 0.028 |
| 16 | 5.98 dB | 6.76 dB | none in 500 | none in 500 | 0.0008 |

The last column is the rule $p^U$, with $p = 0.638$ the measured probability for one candidate at 7 dB. It fits the measured column at 7 dB well here. Going from 1 to 16 candidates moves the 99 percent point down by 3.2 dB; each doubling of $U$ gains less than the one before.

## Correctness

The claim has three parts. The loop keeps, as its invariant, the first index with the smallest PAPR seen so far, so line L6 returns the best candidate in the table. Because $P_1$ is all ones, the output PAPR is never above that of plain OFDM. Because $|P_u[k]| = 1$, the receiver's product $Y[k]\, \overline{P_{u^\ast}[k]}$ returns $X[k]$ exactly. For QPSK data and phases in $\{\pm 1, \pm j\}$, each candidate on its own has exactly the PAPR distribution of plain OFDM, since a quarter turn maps the QPSK set onto itself. The CCDF $p^U$ of the minimum would follow if the candidates were independent; they are not, so $p^U$ is a rule, not a theorem. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Each candidate costs one inverse [FFT](/fast-fourier-transform/) of size $LN$ and $O(LN)$ work for the PAPR, so one block costs $O(U L N \log(LN))$ operations in the real-RAM model, $U$ times the cost of measuring the PAPR of plain OFDM. The memory is $O(LN)$ beyond the table, if only the best candidate so far is kept. The side information is $\lceil \log_2 U \rceil$ bits per OFDM symbol: 4 bits for $U = 16$ against 128 data bits for 64 QPSK subcarriers.

## Properties

- **Distortionless.** The data reach the receiver unchanged; there is no in-band error and no spectral regrowth.
- **Never worse than OFDM.** With $P_1$ all ones, the PAPR of the output is at most that of plain OFDM for every block.
- **Monotone in $U$.** A larger table that contains a smaller one never gives a higher PAPR.
- **Side information.** The index must reach the receiver without error. An error in it corrupts every subcarrier of the symbol.
- **Statistical, not guaranteed.** SLM lowers the probability of a high peak. It does not bound the peak: in the worst case all candidates can have a high PAPR.
- **Any constellation.** The method does not depend on the constellation, as long as the receiver can undo the rotation.

## Variants and improvements

- **Structured tables.** Rows of a Hadamard matrix (entries $\pm 1$, see the [Walsh-Hadamard transform](/walsh-hadamard-transform/)) or other fixed sets are used instead of random sequences. A sequence that is a constant multiple of another, such as $j P_v$, gives the same PAPR and wastes a candidate.
- **Blind SLM.** The receiver finds the index without side information, for example by a maximum likelihood search over the $U$ candidates, using the fact that only one of them gives valid constellation points.
- **Embedded side information.** The index is carried by the phase sequences themselves, for example on pilot or reserved subcarriers.
- **Fewer transforms.** Some versions split the inverse FFT into stages and apply the phase sequences in the middle, so that the candidates share part of the work.
- **Other criteria.** The selection can minimize a quantity other than the PAPR, such as the energy above a clipping level, which tracks the distortion of the amplifier more closely.
- **Sub-block rotation.** [Partial transmit sequences](/partial-transmit-sequence/) restrict the phases to be constant on blocks of subcarriers, which reduces the number of inverse FFTs and the side information for a given number of candidates.

## When to use it

Use SLM when the link can carry a few bits of protected side information per symbol, the transmitter can afford $U$ inverse FFTs, and no in-band distortion is acceptable, for example with dense QAM. A table of 4 to 16 sequences gives most of the practical gain. For a mobile uplink with a tight power budget, a waveform with a low PAPR by design, such as [SC-FDMA](/sc-fdma/), is the usual choice instead.

## Pitfalls

- **Selecting at the Nyquist rate.** Line L3 with $L = 1$ ranks the candidates by their samples only, and the selected candidate can still have a high peak between samples. Use $L \ge 4$ in line L3.
- **Leaving out plain OFDM.** A table whose first sequence is not all ones loses the guarantee that SLM is never worse than plain OFDM. Keep $P_1 = (1, \ldots, 1)$ in the table used by line L2.
- **Phases that are not of magnitude 1.** Line L2 with $|P_u[k]| \ne 1$ changes the energy per subcarrier, and the division at the receiver amplifies the noise. Use unit-magnitude entries.
- **Pilots inside the rotation.** If line L2 also rotates the pilot subcarriers, the receiver must know $u^\ast$ before it can estimate the channel. Set $P_u[k] = 1$ on the pilots, or make the index readable before channel estimation.
- **Unprotected index.** Sending $u^\ast$ uncoded makes the symbol error rate at least the error rate of the index. Protect the index with strong coding or repetition.

## Implementations

## History

Bäuml, Fischer and Huber introduced selected mapping in 1996. In 1997 Müller and Huber published the related method of [partial transmit sequences](/partial-transmit-sequence/). The idea, choosing among several representations of the same data, does not depend on the constellation or on the number of subcarriers. The overview of Han and Lee (2005) compares it with the other PAPR methods by the reduction it gives, its side information and its cost.

## References
