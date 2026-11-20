---
tag: N96EQ7
kind: algorithm
slug: soft-demapping
name: Soft demapping
aliases:
- soft-output demapper
- bit LLR computation
area: communications/modulation-and-detection
level: core
summary: Computes the exact log-likelihood ratio of each bit of a received symbol as a log-sum-exp over all constellation points, with optional prior LLRs from a decoder.
solves: [symbol-by-symbol-map-decoding]
model: real-ram
complexity:
  vars: {M: the number of constellation points, m: the number of bits per point (log2 M)}
  time: {worst: Θ(M log M)}
  space: {extra: Θ(M)}
properties: {deterministic: true, exact: true, needs_noise_level: true, accepts_priors: true}
history:
  year: 1998
  people: [Giuseppe Caire, Giorgio Taricco, Ezio Biglieri]
  note: Caire, Taricco and Biglieri defined the bit metric of bit-interleaved coded modulation as the log of a sum over the points with a given bit value, and studied its capacity. Zehavi had used bit metrics with a bit interleaver in 1992.
prereqs: [signal-constellation, gray-labeling, additive-white-gaussian-noise-channel, log-sum-exp-trick]
see_also: [max-log-demapping, bit-interleaved-coded-modulation, minimum-distance-detector, ldpc-code, turbo-decoding, bcjr-algorithm, turbo-equalization, list-sphere-decoder]
sources:
  - paper: doi:10.1109/18.669123
    title: Giuseppe Caire, Giorgio Taricco and Ezio Biglieri, Bit-interleaved coded modulation, IEEE Transactions on Information Theory 44(3), 927-946, 1998
    locator: the bit metrics of BICM as sums over the subsets of points with a given bit value, and the BICM capacity
  - paper: doi:10.1109/26.141453
    title: Ephraim Zehavi, 8-PSK trellis codes for a Rayleigh channel, IEEE Transactions on Communications 40(5), 873-884, 1992
    locator: the bit interleaver and the bit metrics of the decoder
---

Soft demapping computes, for each bit of a received symbol, the log-likelihood ratio (LLR): the log of the ratio of the probability that the bit is $0$ to the probability that it is $1$, given the received sample. Its sign is the hard decision and its size is the reliability. A soft-input decoder for an [LDPC code](/ldpc-code/), a [turbo code](/turbo-decoding/) or a convolutional code with the [BCJR algorithm](/bcjr-algorithm/) needs these values, and in [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) the demapper is the link between the channel and the binary decoder. The exact LLR is a log-sum-exp over all $M$ points of the constellation. [Max-log demapping](/max-log-demapping/) keeps only the largest term of each sum, which is simpler but not exact; this page is the exact form. With prior LLRs from a decoder, the same algorithm is the demapper of iterative receivers and of [turbo equalization](/turbo-equalization/).

## In plain words

The receiver gets a point that noise has moved. Each possible transmitted point gets a score that says how likely it is to have produced what was received: near points get high scores, far points get low ones. For the first bit, the receiver adds the scores of all points whose first bit is 0, and separately the scores of all points whose first bit is 1. The log of the ratio of the two totals says how sure it is about that bit, and in which direction. It does the same for every bit. Adding all the scores, and not only the best one, is what makes the answer exact.

## The problem

The receiver sees one complex sample after the [matched filter](/matched-filter/):

$$y = h x + w, \qquad x \in \{a_0, \ldots, a_{M-1}\}, \qquad w \sim \mathcal{CN}(0, N_0).$$

The gain $h \ne 0$ and the noise density $N_0 > 0$ are known; $h$ includes the amplitude $\sqrt{E_s}$, and $E_s/N_0 = |h|^2/N_0$ is the SNR per complex symbol. The point $a_i$ carries the bit label $i$ with $m = \log_2 M$ bits $b_0(i), \ldots, b_{m-1}(i)$, most significant bit first. A priori the bits are independent, with prior LLRs $L^a_k = \ln P(b_k = 0)/P(b_k = 1)$, all zero for equally likely points. The output is the a posteriori LLR of each bit,

$$L_k = \ln\frac{P(b_k = 0 \mid y)}{P(b_k = 1 \mid y)} = \ln\frac{\sum_{i:\, b_k(i) = 0} p(y \mid a_i)\, P(a_i)}{\sum_{i:\, b_k(i) = 1} p(y \mid a_i)\, P(a_i)}, \qquad k = 0, \ldots, m-1,$$

and the extrinsic LLR $L^e_k = L_k - L^a_k$. A positive value favors the bit $0$. This is [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/) of the bits of one symbol.

## The algorithm

The density is $p(y \mid a_i) = \frac{1}{\pi N_0}e^{-|y - h a_i|^2/N_0}$, and a bit with prior LLR $L^a$ has $P(b) \propto e^{(1 - 2b)L^a/2}$. So each point gets the log metric $d_i$ of line L2, and each sum in $L_k$ is a log-sum-exp of these metrics. The algorithm folds each sum with the Jacobian logarithm

$$\max{}^*(u, v) = \ln(e^u + e^v) = \max(u, v) + \ln\big(1 + e^{-|u - v|}\big),$$

which never overflows (see the [log-sum-exp trick](/log-sum-exp-trick/)).

```pseudo id=main
SOFT-DEMAP(y, h, N0, a_0..a_{M-1}, La_0..La_{m-1})   ▷ a_i has the label i; La = 0 without priors
L1  for i ← 0 to M - 1
L2      d_i ← -|y - h·a_i|² / N0 + Σ_k (1 - 2·b_k(i)) · La_k / 2
L3  for k ← 0 to m - 1
L4      A_0 ← -∞ ;  A_1 ← -∞
L5      for i ← 0 to M - 1
L6          A_{b_k(i)} ← max*(A_{b_k(i)}, d_i)
L7      L_k ← A_0 - A_1
L8  return L_0..L_{m-1} and the extrinsic values E_k ← L_k - La_k
```

The constant $-\ln(\pi N_0)$ and the normalizers of the priors are the same for every point, so line L2 leaves them out; they cancel in line L7.

## Example

**16-QAM at a high SNR.** Take the Gray-labeled 16-QAM of the area, $h = 1$, $N_0 = 0.1$ (an SNR of $10$ dB), no priors, and $y = 0.5 - 0.2j$. The nearest point is $a_7 = (1 - j)/\sqrt{10}$, label 0111, with $d_7 = -0.4728$. The folds of lines L4 to L7 give:

| bit $k$ | $A_0$ | $A_1$ | $L_k$ | best point with $b_k = 0$ | best point with $b_k = 1$ |
|---|---|---|---|---|---|
| 0 | $-0.2206$ | $-6.7168$ | $6.4962$ | $a_7$, $d = -0.4728$ | $a_{15}$, $d = -6.7974$ |
| 1 | $-2.0677$ | $-0.3905$ | $-1.6772$ | $a_3$, $d = -2.1483$ | $a_7$ |
| 2 | $-2.8295$ | $-0.2955$ | $-2.5340$ | $a_5$, $d = -3.0026$ | $a_7$ |
| 3 | $-5.7694$ | $-0.2230$ | $-5.5463$ | $a_6$, $d = -5.9430$ | $a_7$ |

The signs give the bits 0111, the decision of the [minimum distance detector](/minimum-distance-detector/). Bit 0, the sign of the in-phase component, is the most reliable; bit 1, which separates the inner from the outer in-phase levels, is the least reliable, because $\sqrt{10}\,\mathrm{Re}\,y = 1.58$ is close to the boundary at $2$. Max-log demapping gives $6.3246, -1.6754, -2.5298, -5.4702$, close to these values.

**16-QAM at a low SNR.** With $N_0 = 1$ and the same $y$, the exact LLRs are $1.0313, -0.4539, -0.4103, -0.7376$ and the max-log values $0.6325, -0.1675, -0.2530, -0.5470$. At low SNR many points contribute to each sum, and the maximum alone is far from the total.

**A prior.** With $N_0 = 0.1$ and a prior $L^a_2 = -3$ on bit 2 only, the output is $6.4962, -1.6772, -5.5340, -5.4741$. The prior moves $L_2$ by $-3$, and it also changes $L_3$ a little, because it reweights the points that both sums share. The extrinsic value of bit 2 is $-5.5340 + 3 = -2.5340$, the value without the prior.

## Correctness

Line L2 gives each point $d_i = \ln\big(p(y \mid a_i)P(a_i)\big) + C$, where $C$ does not depend on $i$. Lines L4 to L6 keep the invariant that after the points $a_0, \ldots, a_{i-1}$, $A_b$ is the log of the sum of $e^{d_{i'}}$ over the points seen so far with $b_k(i') = b$, because $\max^*(u, v) = \ln(e^u + e^v)$ and $\max^*(-\infty, v) = v$. At the end the two sums are complete, the constant $C$ cancels in line L7, and $L_k$ is the a posteriori LLR. For the extrinsic value, the prior term of bit $k$ is the same for all points in each sum, so it moves $A_0$ by $+L^a_k/2$ and $A_1$ by $-L^a_k/2$; the difference $L_k - L^a_k$ is the LLR without the prior of bit $k$. The full proof is below.

## Complexity

In the [real RAM](/real-ram/) with $\exp$ and $\ln$ as unit-cost operations, lines L1 and L2 cost $\Theta(M)$ without priors and $\Theta(M m)$ with them, and lines L3 to L7 do $m M$ evaluations of $\max^*$. The total is $\Theta(M \log M)$ per symbol and the extra space is $\Theta(M)$ for the metrics. For a general constellation every point can be the dominant term, so an exact demapper must read all $M$ points. For square QAM with $h \ne 0$, the in-phase bits depend only on $\mathrm{Re}(y/h)$ and the quadrature bits only on $\mathrm{Im}(y/h)$, so two one-dimensional demappers on $\sqrt{M}$ levels each give the same LLRs in $\Theta(\sqrt{M}\log M)$.

## Properties

- **Exact.** The output is the a posteriori LLR, not an approximation. Its error is only floating-point rounding.
- **Needs $N_0$.** The LLR is not a function of the distances alone: at a high SNR it is close to the max-log value, which scales with $1/N_0$, and at a low SNR it is not. A wrong $N_0$ gives wrong LLRs.
- **Extrinsic output.** With priors, line L8 gives the information that the channel adds about each bit, which is what an iterative receiver passes back.
- **The bits of one symbol are dependent.** The $m$ LLRs come from the same $y$. A BICM decoder treats them as independent, and the bit interleaver puts them far apart in the code to make this a good approximation.
- **Sign and size.** For BPSK, $L = 4\,\mathrm{Re}(h^* y)/N_0$. For Gray QPSK with the area labels, $L_0 = 2\sqrt{2}\,\mathrm{Re}(h^* y)/N_0$ and $L_1 = 2\sqrt{2}\,\mathrm{Im}(h^* y)/N_0$. In these two cases the exact and the max-log values agree.

## Variants and improvements

- **Max-log.** Replace $\max^*$ by $\max$: [max-log demapping](/max-log-demapping/). Its error per bit is at most $\ln(M/2)$ and goes to zero at high SNR.
- **Correction tables.** Hardware often computes $\ln(1 + e^{-|u - v|})$ from a small table of eight or so entries, or as a piecewise linear function. The result is between the exact and the max-log values.
- **Per-axis demapping for square QAM.** Demap $\mathrm{Re}(y/h)$ and $\mathrm{Im}(y/h)$ separately on $\sqrt{M}$-PAM with the noise density $N_0/|h|^2$.
- **MIMO and ISI.** With a vector channel $y = Hx + w$, the sums run over all $M^n$ vectors; a [list sphere decoder](/list-sphere-decoder/) keeps only the vectors near $y$. See [MIMO detection](/mimo-detection/).
- **Iterative demapping.** In BICM with iterative decoding the demapper uses the decoder's LLRs as priors in line L2 and passes the extrinsic values back. With priors, a labeling other than Gray can give a better result after a few iterations.

## When to use it

Use the exact demapper in front of any soft-input decoder when the SNR is moderate or low, when the constellation is small enough that $M$ evaluations are cheap, and always in iterative receivers, where the extrinsic values must be accurate. Use max-log when cost matters and the decoder is a min-sum decoder that ignores the scale of its inputs.

## Pitfalls

- **The sign convention.** This page uses $\ln P(0)/P(1)$, so a positive LLR favors $0$. Some decoders use the opposite sign; a mismatch makes the decoder fail completely.
- **The noise level.** $N_0$ is the density of the complex noise; each of the real and imaginary parts has variance $N_0/2$. Using $\sigma^2 = N_0/2$ in place of $N_0$ doubles every LLR.
- **Underflow.** Summing $e^{-|y - h a_i|^2/N_0}$ directly underflows at a high SNR, and the ratio becomes $0/0$. Fold in the log domain with $\max^*$.
- **The bit order.** The label is most significant bit first here. A decoder that expects the other order gets the in-phase and quadrature bits swapped.
- **Posterior or extrinsic.** In a turbo loop, passing $L_k$ instead of $L_k - L^a_k$ counts the prior twice, and the loop becomes overconfident.
- **The scale of $h$.** If the points have unit energy, $h$ must include $\sqrt{E_s}$; otherwise all distances, and so all LLRs, are wrong.

## Implementations

## History

Soft decisions are as old as the Viterbi decoder, but the bit LLR of a multilevel constellation became central with bit-interleaved coded modulation. Zehavi in 1992 put a bit interleaver between a convolutional code and an 8-PSK mapper for the Rayleigh channel and decoded with one metric per bit. Caire, Taricco and Biglieri in 1998 gave the general theory of BICM, with the exact bit metric as the log of a sum over the points with a given bit value, and its capacity. The Jacobian logarithm $\max^*$ came into use in the log-domain BCJR algorithm in the mid 1990s. Turbo codes and LDPC codes then made the exact demapper a standard block of receivers.

## References
