---
tag: BTM11T
kind: algorithm
slug: max-log-demapping
name: Max-log demapping
aliases:
- max-log LLR approximation
area: communications/modulation-and-detection
level: core
summary: "Approximates each bit LLR by the squared distance to the nearest point with the bit 1, minus that to the nearest point with the bit 0, over N0. It needs no exponentials."
solves: [symbol-by-symbol-map-decoding]
model: real-ram
complexity:
  vars: {M: the number of constellation points, m: the number of bits per point (log2 M)}
  time: {worst: Θ(M log M)}
  space: {extra: Θ(M)}
properties: {deterministic: true, exact: false, needs_noise_level: false, accepts_priors: true}
history:
  year: 1992
  people: [Ephraim Zehavi]
  note: Zehavi used a bit metric of this form in the decoder of bit-interleaved 8-PSK trellis codes. The same max approximation of a log-sum-exp is the basis of the max-log BCJR algorithm.
prereqs: [soft-demapping, signal-constellation, gray-labeling, minimum-distance-detector]
see_also: [soft-demapping, bit-interleaved-coded-modulation, min-sum-decoding, minimum-distance-detector, log-sum-exp-trick, ldpc-code, list-sphere-decoder, bcjr-algorithm]
sources:
  - paper: doi:10.1109/26.141453
    title: Ephraim Zehavi, 8-PSK trellis codes for a Rayleigh channel, IEEE Transactions on Communications 40(5), 873-884, 1992
    locator: the bit interleaver and the bit metrics of the decoder
  - paper: doi:10.1109/18.669123
    title: Giuseppe Caire, Giorgio Taricco and Ezio Biglieri, Bit-interleaved coded modulation, IEEE Transactions on Information Theory 44(3), 927-946, 1998
    locator: the bit metrics of BICM and their simplified form
---

Max-log demapping computes an approximate log-likelihood ratio (LLR) for each bit of a received symbol. The exact LLR of [soft demapping](/soft-demapping/) is the log of a ratio of two sums of exponentials, one over the points whose bit is $0$ and one over the points whose bit is $1$. Max-log keeps only the largest term of each sum. Without priors, the result is the squared distance from the received sample to the nearest point with the bit $1$, minus the squared distance to the nearest point with the bit $0$, divided by $N_0$. It needs no $\exp$ and no $\ln$, its signs are the bits of the [minimum distance detector](/minimum-distance-detector/), and its error is at most $\ln(M/2)$ per bit. For Gray square QAM it falls apart into simple piecewise linear functions of the in-phase and quadrature components. Most hardware receivers for [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) use it.

## In plain words

For each bit, the receiver asks two questions. Of all the points whose bit is 0, which one is nearest to what I received, and how far is it? And the same for the points whose bit is 1. If the nearest "0" point is much nearer than the nearest "1" point, the bit is very likely 0. The difference of the two squared distances is the answer: its sign gives the bit, and its size gives the confidence. The method ignores all points except the two nearest ones in each comparison. That makes it cheap, and at a good signal level it loses almost nothing.

## The problem

The receiver sees $y = h x + w$, where $x$ is one of the points $a_0, \ldots, a_{M-1}$, $a_i$ carries the bit label $i$ with bits $b_0(i), \ldots, b_{m-1}(i)$ (most significant first), $h \ne 0$ is a known gain, $j$ is the imaginary unit and $w \sim \mathcal{CN}(0, N_0)$. The optional prior LLRs are $L^a_k = \ln P(b_k = 0)/P(b_k = 1)$. With the point metric

$$d_i = -\frac{|y - h a_i|^2}{N_0} + \sum_{k} \frac{(1 - 2b_k(i))\, L^a_k}{2},$$

the exact LLR is $L_k = \ln\sum_{b_k(i) = 0} e^{d_i} - \ln\sum_{b_k(i) = 1} e^{d_i}$, and the max-log LLR is

$$\tilde L_k = \max_{i:\, b_k(i) = 0} d_i - \max_{i:\, b_k(i) = 1} d_i, \qquad k = 0, \ldots, m-1.$$

Without priors, $\tilde L_k = \big(\min_{b_k(i) = 1}|y - h a_i|^2 - \min_{b_k(i) = 0}|y - h a_i|^2\big)/N_0$. A positive value favors the bit $0$.

## The algorithm

```pseudo id=main
MAX-LOG-DEMAP(y, h, N0, a_0..a_{M-1}, La_0..La_{m-1})   ▷ a_i has the label i; La = 0 without priors
L1  for i ← 0 to M - 1
L2      d_i ← -|y - h·a_i|² / N0 + Σ_k (1 - 2·b_k(i)) · La_k / 2
L3  for k ← 0 to m - 1
L4      B_0 ← -∞ ;  B_1 ← -∞
L5      for i ← 0 to M - 1
L6          B_{b_k(i)} ← max(B_{b_k(i)}, d_i)
L7      L_k ← B_0 - B_1
L8  return L_0..L_{m-1} and the extrinsic values E_k ← L_k - La_k
```

The only difference from the exact demapper is line L6, which uses $\max$ where the exact demapper uses $\max^*(u, v) = \max(u, v) + \ln(1 + e^{-|u - v|})$.

**Gray square QAM, one axis at a time.** Write $z = y/h$, scale each axis to the raw amplitudes $\pm 1, \pm 3, \ldots$ with $s = \sqrt{2(M - 1)/3}$, and put $u = s\,\mathrm{Re}\,z$ and $v = s\,\mathrm{Im}\,z$. Since $|y - h a|^2 = (|h|^2/s^2)\big((u - c_I)^2 + (v - c_Q)^2\big)$ for the point with raw levels $(c_I, c_Q)$, the in-phase bits depend only on $u$ and the quadrature bits only on $v$. For 16-QAM with the labels of the area (in-phase level $+3, +1, -1, -3$ with the labels $00, 01, 11, 10$),

$$\Lambda_0(u) = \begin{cases} 4u, & |u| \le 2, \\ 8(u - \operatorname{sign} u), & |u| > 2, \end{cases} \qquad \Lambda_1(u) = 4(|u| - 2),$$

and $\tilde L_0 = |h|^2\Lambda_0(u)/(10 N_0)$, $\tilde L_1 = |h|^2\Lambda_1(u)/(10 N_0)$, $\tilde L_2 = |h|^2\Lambda_0(v)/(10 N_0)$, $\tilde L_3 = |h|^2\Lambda_1(v)/(10 N_0)$. For example, for $0 \le u \le 2$ the nearest in-phase levels with the first bit $0$ and $1$ are $+1$ and $-1$, and $(u + 1)^2 - (u - 1)^2 = 4u$.

## Example

Take Gray 16-QAM, $h = 1$, $N_0 = 0.1$ and $y = 0.5 - 0.2j$, the example of the [soft demapping](/soft-demapping/) page. Then $u = \sqrt{10} \cdot 0.5 = 1.5811$ and $v = \sqrt{10} \cdot (-0.2) = -0.6325$, both inside $[-2, 2]$:

| bit $k$ | formula | max-log $\tilde L_k$ | exact $L_k$ |
|---|---|---|---|
| 0 | $4u/(10 N_0)$ | $6.3246$ | $6.4962$ |
| 1 | $4(\lvert u\rvert - 2)/(10 N_0)$ | $-1.6754$ | $-1.6772$ |
| 2 | $4v/(10 N_0)$ | $-2.5298$ | $-2.5340$ |
| 3 | $4(\lvert v\rvert - 2)/(10 N_0)$ | $-5.4702$ | $-5.5463$ |

The signs give the label 0111 of the nearest point $(1 - j)/\sqrt{10}$, and the values are within $0.18$ of the exact ones. The brute-force form gives the same: for bit 1, the nearest point with $b_1 = 0$ is $a_3 = (3 - j)/\sqrt{10}$ and the nearest with $b_1 = 1$ is $a_7$, and $(|y - a_7|^2 - |y - a_3|^2)/N_0 = (0.04728 - 0.21483)/0.1 = -1.6754$.

At $N_0 = 1$, the max-log values are ten times smaller, $0.6325, -0.1675, -0.2530, -0.5470$, while the exact values are $1.0313, -0.4539, -0.4103, -0.7376$. At a low SNR many points contribute to each sum, and the largest term is no longer a good stand-in for the whole sum.

## Correctness

Max-log demapping does not compute the exact LLR; what is proved is that it computes the max form and how far that is from the exact value. Lines L4 to L6 keep the invariant that $B_b$ is the largest $d_i$ seen so far among the points with $b_k(i) = b$, so line L7 returns $\tilde L_k$. Without priors, $\max_i(-|y - h a_i|^2/N_0) = -\min_i|y - h a_i|^2/N_0$, which gives the distance form. Each sum in the exact LLR has $M/2$ terms, each at most its largest, so $\max \le \ln\sum e^{d_i} \le \max + \ln(M/2)$ for each bit value, and $|L_k - \tilde L_k| \le \ln(M/2)$. The point $a_{i^*}$ with the largest $d_i$ lies in one of the two sets of each bit, so the sign of $\tilde L_k$ is the bit $b_k(i^*)$ of the MAP decision (of the ML decision without priors). The per-axis form for square QAM follows from the separation of $|y - h a|^2$ into an in-phase and a quadrature term; the term of the other axis is the same in both minima and cancels. The full proof is below.

## Complexity

In the [real RAM](/real-ram/), lines L1 and L2 cost $\Theta(M)$ without priors and $\Theta(M m)$ with them, and lines L3 to L7 do $mM$ comparisons. The total is $\Theta(M \log M)$ per symbol with $\Theta(M)$ extra space; the work is the same as for the exact demapper, but each step is a comparison, not an $\exp$ and a $\ln$. For Gray square QAM the per-axis form costs $\Theta(\sqrt{M}\log M)$ in general and $O(\log M)$ with closed forms such as the one for 16-QAM. With a decision region search, the nearest point with each bit value can be found without visiting all points.

## Properties

- **No noise level needed for the decoder.** Without priors, every $\tilde L_k$ is the same function of $y$ times $1/N_0$. A min-sum decoder, a Viterbi decoder or a max-log BCJR decoder gives the same output for any positive scale of its inputs, so the receiver can skip $N_0$ and pass the distance differences.
- **Hard decisions are ML decisions.** The signs of $\tilde L_0, \ldots, \tilde L_{m-1}$ are the label of the nearest point.
- **Error bound.** $|L_k - \tilde L_k| \le \ln(M/2)$, which is $\ln 8 = 2.079$ for 16-QAM. The bound is approached only when the terms of one sum are nearly equal and those of the other are not, as at low SNR. At high SNR the second largest term of each sum is usually much smaller than the largest, and the error is small, except near the boundary between two points with the same bit value.
- **Exact for BPSK and QPSK.** For BPSK each sum has one term. For Gray QPSK, each sum has two terms that differ by the same factor in the numerator and the denominator, and the factor cancels. In both cases $\tilde L_k = L_k$.
- **Piecewise linear.** Each $\tilde L_k$ is piecewise linear in the real and imaginary parts of $y$, with breaks where the nearest point with a bit value changes.
- **Biased at low SNR.** In the example at $N_0 = 1$, $\tilde L_1 = -0.17$ while $L_1 = -0.45$. The magnitudes can be too small or too large, so a fixed scaling does not remove the error.

## Variants and improvements

- **Exact demapping.** Replace $\max$ by $\max^*$: [soft demapping](/soft-demapping/).
- **Max-log with a correction.** Add a table value of $\ln(1 + e^{-|u - v|})$ in line L6 only when the two terms are close. This recovers most of the loss at a small cost.
- **Scaled max-log.** Multiply the LLRs by a constant factor, tuned by simulation for the decoder and the SNR range. It reduces the average error but cannot remove it.
- **Per-axis closed forms for QAM.** For Gray $M$-QAM each bit is a piecewise linear function of one axis, with closed forms like the 16-QAM one above. OFDM receivers use them per subcarrier.
- **MIMO.** For a vector channel, max-log needs the nearest vector with each bit value; a [list sphere decoder](/list-sphere-decoder/) or a tree search finds it without visiting all $M^n$ vectors.

## When to use it

Use max-log when the decoder is a [min-sum decoder](/min-sum-decoding/) or a max-log BCJR decoder, when $N_0$ is unknown or hard to estimate, and when cost or latency matters, as in hardware for Wi-Fi, LTE and DVB. Use the exact demapper at low SNR with large constellations, and in iterative receivers, where the extrinsic values must be accurate.

## Pitfalls

- **A sum-product decoder expects exact LLRs.** A sum-product LDPC decoder assumes exact LLRs. With max-log inputs it still works but loses a fraction of a dB, more at low rates and with large constellations.
- **Scale.** If the receiver drops $1/N_0$, the decoder must also be scale invariant. A sum-product decoder fed with unscaled distances is wrong.
- **Ties.** On a decision boundary $\tilde L_k = 0$, and the hard decision is arbitrary. It has probability zero but occurs with quantized inputs; break ties in a fixed way.
- **Closed forms depend on the labeling.** The 16-QAM formulas above hold for the area labels (in-phase bits first, Gray per axis). A different labeling or bit order needs different formulas.
- **The gain.** The per-axis forms need $z = y/h$ and the factor $|h|^2$. Dropping $|h|^2$ on a fading channel gives the same weight to faded and strong symbols, which hurts the decoder.

## Implementations

## History

The max approximation of a sum of exponentials is old; in decoding it appears as the Viterbi metric and as the max-log form of the BCJR algorithm. For bit metrics of a multilevel constellation, Zehavi in 1992 decoded bit-interleaved 8-PSK trellis codes on the Rayleigh channel with a metric per bit of this form, and Caire, Taricco and Biglieri in 1998 gave the theory of bit-interleaved coded modulation with both the exact and the simplified metrics. With LDPC and turbo codes in Wi-Fi, LTE and DVB, the max-log demapper with per-axis closed forms became the common choice in hardware.

## References
