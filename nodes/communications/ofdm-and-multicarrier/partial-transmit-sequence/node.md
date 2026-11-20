---
tag: JND5P6
kind: algorithm
slug: partial-transmit-sequence
name: Partial transmit sequence
aliases:
- PTS
area: communications/ofdm-and-multicarrier
level: core
summary: "Lowers the PAPR of OFDM by splitting the subcarriers into V subblocks, transforming each once, and searching phase factors for the subblocks. The best factors go to the receiver."
model: real-ram
complexity:
  vars: {V: the number of subblocks, W: the number of allowed phase factors, N: the number of subcarriers, L: the oversampling factor}
  time: {worst: O(V L N log(L N) + W^(V-1) V L N)}
  space: {extra: O(V L N)}
properties: {deterministic: true, distortionless: true, side_information: true, never_worse_than_plain_ofdm: true}
history:
  year: 1997
  people: [Stefan H. Müller, Johannes B. Huber]
  note: "Müller and Huber proposed optimum combination of partial transmit sequences in 1997, one year after selected mapping by Bäuml, Fischer and Huber."
prereqs: [peak-to-average-power-ratio, orthogonal-frequency-division-multiplexing]
see_also: [selected-mapping, iterative-clipping-and-filtering, tone-reservation, active-constellation-extension, fast-fourier-transform, quadrature-amplitude-modulation]
sources:
  - paper: doi:10.1049/el:19970266
    title: "S. H. Müller and J. B. Huber, OFDM with reduced peak-to-average power ratio by optimum combination of partial transmit sequences, Electronics Letters 33(5), 1997, pages 368 to 369"
    locator: "the partition into subblocks, the separate transforms, the rotation factors and the search for their best combination"
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the section on partial transmit sequences, with the partitions and the cost of the search"
---

Partial transmit sequences (PTS) lower the [peak-to-average power ratio](/peak-to-average-power-ratio/) (PAPR) of an [OFDM](/orthogonal-frequency-division-multiplexing/) symbol without distorting it. The transmitter splits the $N$ subcarriers into $V$ disjoint subblocks, takes one inverse FFT of each subblock alone, and then searches for phase factors $b_1 = 1, b_2, \ldots, b_V$ from a small set such as $\{\pm 1, \pm j\}$ so that the sum $\sum_v b_v x_v$ has the lowest peak. Because the transform is linear, this sum is the OFDM symbol of the data with every subcarrier of subblock $v$ rotated by $b_v$, so each candidate costs additions only. The receiver gets the factors as side information and undoes them. Müller and Huber proposed it in 1997. It is a structured form of [selected mapping](/selected-mapping/): SLM needs one inverse FFT per candidate, while PTS needs $V$ inverse FFTs for $W^{V-1}$ candidates, but its search grows exponentially in $V$. The page uses the unitary DFT pair $F[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, and $j$ is the imaginary unit.

## In plain words

A tall peak in an OFDM signal happens when many tones line up at one instant. If you turn a whole group of tones by some angle, they line up at different instants, and the peak can disappear. PTS cuts the tones into a few groups and builds the signal of each group separately. Then it tries all the ways to turn each group by a quarter turn, a half turn or not at all. Adding the turned group signals is cheap, so many combinations can be tried. The sender keeps the combination with the lowest peak and tells the receiver which one it used. The receiver turns each group back. The data are not changed at all, but the number of combinations grows very fast with the number of groups.

## The problem

The input is a block of $N$ data symbols $X[0], \ldots, X[N-1]$ with $E|X[k]|^2 = 1$, a partition of the subcarriers into subblocks $S_1, \ldots, S_V$, a set $W$ of allowed phase factors of magnitude 1, and an oversampling factor $L$, usually 4. The output is a vector of factors $b \in \{1\} \times W^{V-1}$ and the oversampled OFDM symbol of the rotated data $X_b[k] = b_v X[k]$ for $k \in S_v$, such that its PAPR is the smallest over all such vectors. The first factor is fixed to 1, because multiplying all factors by a common phase does not change the PAPR.

## The algorithm

```pseudo id=main
PTS(X[0..N-1], S_1..S_V, W, L)
L1  for v ← 1 to V
L2      x_v ← √L · F_LNᴴ (X on S_v, 0 elsewhere, with (L-1)N zeros in the middle)
L3  best ← ∞
L4  for each (b_2, .., b_V) in W^(V-1), with b_1 = 1
L5      x ← Σ_v b_v · x_v                       ▷ the symbol of the rotated data, by linearity
L6      r ← max_m |x[m]|² / mean_m |x[m]|²
L7      if r < best then best ← r; b* ← b
L8  return b*, Σ_v b*_v · x_v                   ▷ send the symbol and the V - 1 factors
```

Lines L1 and L2 compute the $V$ partial transmit sequences, each with one inverse FFT of size $LN$. The zeros go in the middle of each spectrum, because the indices $k \ge N/2$ are the negative frequencies. Lines L4 to L7 search every combination of the free factors; line L5 forms the candidate with $O(VLN)$ multiplications and additions, which are only sign changes and swaps for $W = \{\pm 1, \pm j\}$. Line L8 sends the best candidate. The side information is $(V - 1) \log_2 W$ bits. The receiver equalizes and computes $X[k] = Y[k]\, \overline{b^\ast_v}$ for $k \in S_v$.

## Example

Take $N = 64$ QPSK subcarriers, $L = 4$, $V = 4$ adjacent subblocks of 16 subcarriers and $W = \{1, -1, j, -j\}$, so $4^3 = 64$ candidates and 6 bits of side information. For one block (Python `random.Random(1)`), plain OFDM has a PAPR of 6.94 dB. The search returns $b^\ast = (1, -j, j, -j)$ and a PAPR of 5.59 dB, 1.35 dB lower.

Over 300 random blocks (`random.Random(2)`):

| setting | candidates | side bits | mean PAPR | 99 percent below | $\Pr(> 7\ \mathrm{dB})$ |
|---|---|---|---|---|---|
| plain OFDM | 1 | 0 | 7.36 dB | 9.48 dB | 0.613 |
| $V = 2$, $W = 4$, adjacent | 4 | 2 | 6.75 dB | 8.20 dB | 0.300 |
| $V = 4$, $W = 2$, adjacent | 8 | 3 | 6.32 dB | 7.38 dB | 0.083 |
| $V = 4$, $W = 4$, adjacent | 64 | 6 | 5.78 dB | 6.81 dB | none in 300 |
| $V = 4$, $W = 4$, interleaved | 64 | 6 | 6.13 dB | 7.38 dB | 0.030 |
| $V = 8$, $W = 2$, adjacent | 128 | 7 | 5.53 dB | 6.22 dB | none in 300 |

Adjacent subblocks do better than interleaved ones (subcarrier $k$ in subblock $k \bmod V$) with the same number of candidates. The reason is that an interleaved subblock has a time signal that repeats $V$ times within the symbol, so the rotations cannot move a peak in one part of the symbol without moving its copies. More subblocks help more than more phase values: $V = 8$ with 2 phases beats $V = 4$ with 4 phases.

## Correctness

The claim is that line L8 returns the factors that minimize the PAPR over all of $\{1\} \times W^{V-1}$, together with the exact OFDM symbol of the rotated data, and that the receiver recovers $X$ exactly. The key fact is linearity: the map from subcarrier values to the oversampled symbol is linear, and the subblocks are disjoint, so $\sum_v b_v x_v$ is exactly the symbol of the rotated data. The loop invariant is that $\mathit{best}$ is the smallest PAPR among the vectors tried so far, and $b^\ast$ is the first vector that reaches it. Fixing $b_1 = 1$ loses nothing when $W$ is a group, since a common phase leaves the PAPR unchanged. The vector of all ones is in the search, so the result is never worse than plain OFDM. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The $V$ inverse [FFTs](/fast-fourier-transform/) cost $O(V L N \log(LN))$. The search tries $W^{V-1}$ vectors, each at $O(VLN)$ for the sum and the PAPR, so one block costs $O(V L N \log(LN) + W^{V-1} V L N)$ operations in the real-RAM model, and the memory is $O(VLN)$ for the partial sequences. The search term dominates quickly: for $N = 64$, $L = 4$, $V = 8$ and $W = 4$ it is $4^7 = 16384$ candidates per symbol. The exhaustive search is what makes the result optimal; the practical versions below search only part of the space and give up that guarantee.

## Properties

- **Distortionless.** The data reach the receiver unchanged.
- **Never worse than OFDM.** The vector of all ones is one of the candidates.
- **Cheaper transforms than SLM.** $V$ inverse FFTs give $W^{V-1}$ candidates. [Selected mapping](/selected-mapping/) needs one inverse FFT for each candidate.
- **Exponential search.** The number of candidates grows as $W^{V-1}$, and the search, not the transforms, sets the cost for $V$ above about 4.
- **Side information.** $(V - 1) \log_2 W$ bits per symbol, which must reach the receiver without error.
- **Partition matters.** In the example, adjacent subblocks give a lower PAPR than interleaved ones for the same $V$ and $W$.

## Variants and improvements

- **Sub-optimal search.** An iterative search flips one factor at a time and keeps the change if the PAPR falls, with $O(V W)$ candidates instead of $W^{V-1}$. Other versions use a threshold: stop as soon as a candidate has a PAPR below a target.
- **Pseudo-random partition.** Each subcarrier goes to a random subblock, known to both ends. This avoids the periodic time signals of the interleaved partition.
- **Blind PTS.** The receiver finds the factors without side information, using the structure of the constellation, at the cost of a search at the receiver.
- **Continuous phases.** Factors from a continuous set, chosen by an optimization, reach a lower PAPR but need more side information or a blind receiver.
- **Combined methods.** PTS can be followed by [clipping and filtering](/iterative-clipping-and-filtering/) to remove the remaining rare peaks.

## When to use it

Use PTS when the data must reach the receiver without distortion, a few bits of protected side information per symbol are acceptable, and the transmitter cannot afford one inverse FFT per candidate as in SLM. Keep $V$ small, 4 to 8, or use a sub-optimal search. If the receiver cannot be changed, use [clipping and filtering](/iterative-clipping-and-filtering/) or [tone reservation](/tone-reservation/) instead.

## Pitfalls

- **Searching on Nyquist-rate samples.** Line L2 with $L = 1$ ranks the candidates by their samples only, and the selected symbol can still have a peak between samples. Use $L \ge 4$ in line L2.
- **Overlapping subblocks.** If a subcarrier belongs to two subblocks, line L5 adds it twice and the symbol is no longer that of rotated data. Line L2 must use a partition: every subcarrier in exactly one subblock.
- **Searching $b_1$ too.** Letting line L4 range over all of $W^V$ multiplies the work by $W$ and finds nothing better, because a common phase does not change the PAPR. Fix $b_1 = 1$.
- **Interleaved partition by default.** Choosing $S_v = \{k : k \bmod V = v - 1\}$ in line L2 is easy to code but gives a weaker result. Use adjacent or pseudo-random subblocks.
- **Unprotected factors.** One wrong factor at the receiver rotates a whole subblock and destroys its data. Code the side information strongly.

## Implementations

## History

Müller and Huber published PTS in 1997 as an optimum combination of partial transmit sequences, one year after Bäuml, Fischer and Huber published [selected mapping](/selected-mapping/). Later work focused on reducing the search, with iterative and threshold searches, and on removing the side information. The overview of Han and Lee (2005) compares PTS with SLM and the other PAPR methods.

## References
