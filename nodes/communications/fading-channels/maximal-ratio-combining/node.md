---
tag: 5E6BSS
kind: algorithm
slug: maximal-ratio-combining
name: Maximal ratio combining
aliases:
- maximum ratio combining
area: communications/fading-channels
level: intro
summary: "Weights each diversity branch by the conjugate of its gain over its noise power and adds the branches. The output SNR is the sum of the branch SNRs, the largest of any linear combiner."
solves: [symbol-detection]
model: real-ram
complexity:
  vars: {L: the number of diversity branches}
  time: {worst: O(L)}
  space: {extra: O(1)}
properties: {optimal_linear_combiner: true, needs_branch_phases: true, needs_branch_noise_powers: true, diversity_order: L}
history:
  year: 1954
  people: [Leonard R. Kahn, D. G. Brennan]
  note: "Kahn described a ratio-squared combiner for diversity radio in 1954. Brennan (1959) named maximal ratio combining and compared it with equal gain and selection combining."
prereqs: [rayleigh-fading-channel, diversity-order, matched-filter]
see_also: [diversity-order, equal-gain-combining, selection-combining, maximum-ratio-transmission, rake-receiver, beamforming, outage-probability, alamouti-code]
sources:
  - paper: doi:10.1109/JRPROC.1959.287136
    title: "D. G. Brennan, Linear diversity combining techniques, Proceedings of the IRE 47(6), 1959, pages 1075 to 1102"
    locator: "the analysis of maximal ratio, equal gain and selection combining"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Section 7.2.4 (maximal-ratio combining)"
  - book: isbn:9780471649533
    title: "Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, 2nd edition, Wiley, 2005"
    locator: "Chapter 9, Section 9.2 (maximal-ratio combining)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 5.4.2 (receive diversity)"
---

Maximal ratio combining (MRC) is a linear receiver for $L$ diversity branches that see the same symbol through different fading gains: it multiplies each branch by the conjugate of its gain, divided by its noise power, and adds the results. Among the combiners of the [diversity order](/diversity-order/) family, MRC has the highest output SNR; [equal gain combining](/equal-gain-combining/) only aligns the phases, and [selection combining](/selection-combining/) keeps one branch. [Maximum ratio transmission](/maximum-ratio-transmission/) is the same weighting used at a transmitter with several antennas, and the [rake receiver](/rake-receiver/) applies MRC to the delayed copies of one signal.

## In plain words

Suppose the same message arrives over several antennas, and each copy is faded and noisy in its own way. Some copies are strong, some are weak, and each one arrives with its own phase. MRC turns each copy so that all of them point the same way, then gives each copy a weight that grows with its strength and shrinks with its noise. A strong, clean copy counts a lot and a weak, noisy copy counts little. After the copies are added, the signal parts add up in step, while the noise parts, which are independent, add up only in power. The result is as good as one copy whose quality is the total of the qualities of all the copies.

## The problem

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$, where $x$ is the transmitted symbol with energy $E_s$, $h_l$ is the complex fading gain of the branch, and $w_l \sim CN(0, N_{0,l})$ is noise, independent across branches. The branch SNR is $\gamma_l = |h_l|^2 E_s / N_{0,l}$, and $\bar\gamma = E[\gamma_l]$ is its mean. The receiver has CSIR: it knows $h_l$ and $N_{0,l}$. The task is to form one statistic $z = \sum_l c_l^* y_l$ with the largest SNR, and to pass $z$ to a [symbol detector](/symbol-detection/). The gains may follow block fading, with one value per codeword, or fast fading, with a new value per symbol; the combiner acts symbol by symbol either way. There is no CSIT.

## The algorithm

```pseudo id=main
MRC(h[1..L], y[1..L], N0[1..L])
L1  c_l ← h_l / N0_l  for l = 1 .. L               ▷ the combining weights
L2  z ← Σ_l conj(c_l) · y_l
L3  g ← Σ_l |h_l|² / N0_l                          ▷ the output SNR per unit symbol energy
L4  return z / g, g                                 ▷ z / g = x + noise of variance 1 / g
```

Line L1 is the weight of the branch: the conjugate in line L2 removes the phase of $h_l$, and the factor $|h_l|/N_{0,l}$ gives each branch a share that grows with its gain and falls with its noise. Line L3 is the normalization that turns $z$ into an unbiased estimate of $x$, $z/g = x + n$ with $n \sim CN(0, 1/g)$, so a detector for Gaussian noise, such as the [minimum distance detector](/minimum-distance-detector/), can follow. When all branches have the same noise power, the weights reduce to $c_l = h_l$, up to a common factor.

## Example

Take $L = 2$ branches with $N_0 = 1$, gains $h_1 = 1 + j$ and $h_2 = 0.5j$, and BPSK with $x = 1$. With no noise, $y_1 = 1 + j$ and $y_2 = 0.5j$. Line L2 gives $z = (1 - j)(1 + j) + (-0.5j)(0.5j) = 2 + 0.25 = 2.25$, and line L3 gives $g = 2 + 0.25 = 2.25$, so $z/g = 1 = x$. The output SNR is $E_s g = \gamma_1 + \gamma_2$, with $\gamma_1 = 2$ and $\gamma_2 = 0.25$ for $E_s = 1$. Selection combining would get only 2 from this channel.

For $L$ independent [Rayleigh](/rayleigh-fading-channel/) branches with mean $\bar\gamma$ each, the output SNR $\gamma = \sum_l \gamma_l$ has the gamma distribution with shape $L$ and mean $L\bar\gamma$. With $\mu = \sqrt{\bar\gamma/(1 + \bar\gamma)}$, the bit error rate of coherent BPSK is the closed form (independent Rayleigh branches, perfect CSIR)

$$P_b = \Big(\frac{1 - \mu}{2}\Big)^L \sum_{k=0}^{L-1} \binom{L - 1 + k}{k} \Big(\frac{1 + \mu}{2}\Big)^k.$$

| $\bar\gamma$ per branch | $L = 1$ | $L = 2$ | $L = 4$ |
|---|---|---|---|
| 5 dB | 0.06418 | 0.011829 | $5.073 \cdot 10^{-4}$ |
| 10 dB | 0.023269 | $1.5991 \cdot 10^{-3}$ | $9.698 \cdot 10^{-6}$ |
| 20 dB | $2.4814 \cdot 10^{-3}$ | $1.8442 \cdot 10^{-5}$ | $1.319 \cdot 10^{-9}$ |

The high-SNR form $\binom{2L - 1}{L}/(4\bar\gamma)^L$ gives $1.875 \cdot 10^{-3}$ for $L = 2$ at 10 dB. The outage probability is $\Pr[\gamma < x] = 1 - e^{-x/\bar\gamma}\sum_{k=0}^{L-1}(x/\bar\gamma)^k/k!$, which is $4.6788 \cdot 10^{-3}$ for $L = 2$, $x = 1$ and $\bar\gamma = 10$ dB. A simulation of 20000 BPSK bits with $L = 2$ at 5 dB (seed 5003) gives a Wilson interval with $z = 3.29$ that contains 0.011829.

## Correctness

**Claim.** For any weights $c_l$, not all zero, the SNR of $z = \sum_l c_l^* y_l$ is $E_s|\sum_l c_l^* h_l|^2 / \sum_l |c_l|^2 N_{0,l}$, and it is at most $\sum_l \gamma_l$, with equality if and only if $c_l = a\, h_l / N_{0,l}$ for one complex $a \ne 0$. So MRC maximizes the output SNR over all linear combiners, and its output SNR is $\gamma_1 + \cdots + \gamma_L$. This is a theorem.

**Key step.** Write $c_l^* h_l = (c_l^* \sqrt{N_{0,l}})(h_l/\sqrt{N_{0,l}})$ and apply the Cauchy-Schwarz inequality to the two vectors. The equality case of Cauchy-Schwarz gives the weights. For Gaussian noise and a known channel, $z/g$ is a sufficient statistic for $x$, so MRC followed by the AWGN detector is the maximum likelihood detector. The full proof is in the proofs folder.

## Complexity

Lines L1 to L3 take $O(L)$ complex multiplications and additions per symbol, in the [real RAM](/real-ram/), with $O(1)$ extra space besides the inputs. The cost of MRC is not in the arithmetic but in the inputs: each branch needs its own receiver chain and an estimate of $h_l$, and of $N_{0,l}$ when the noise powers differ.

## Properties

- **Output SNR is the sum.** $\gamma_{\mathrm{MRC}} = \sum_l \gamma_l$. Its mean is $L\bar\gamma$, an array gain of $L$, against $\bar\gamma(1 + 1/2 + \cdots + 1/L)$ for selection combining and $\bar\gamma(1 + (L - 1)\pi/4)$ for equal gain combining.
- **Diversity order $L$.** With $L$ independent Rayleigh branches, $P_b$ falls as $\bar\gamma^{-L}$ at high $\bar\gamma$; see [diversity order](/diversity-order/). Selection and equal gain combining have the same diversity order and differ only by a constant.
- **Maximum likelihood.** With perfect CSIR and independent Gaussian noise, MRC loses no information about $x$.
- **Scale-free weights.** Multiplying all weights by one complex number does not change the SNR or the detection. Only the relative weights matter, so a common unknown phase is harmless, but a phase error per branch is not.
- **Comparison at $L = 2$.** For BPSK in Rayleigh fading at 10 dB per branch, the bit error rates are $1.599 \cdot 10^{-3}$ for MRC, $2.070 \cdot 10^{-3}$ for equal gain combining and $2.973 \cdot 10^{-3}$ for selection combining.

## Variants and improvements

- **Maximum ratio transmission.** With $L$ transmit antennas and CSIT, sending $x$ with weights $h_l^*/\|h\|$ gives the same output SNR $\|h\|^2 E_s/N_0$ at the receiver. See [maximum ratio transmission](/maximum-ratio-transmission/).
- **Rake receiver.** In a frequency-selective channel with resolvable paths, the [rake receiver](/rake-receiver/) uses MRC over the delayed copies, for example in [CDMA](/code-division-multiple-access/).
- **Correlated noise.** When the noise is correlated across branches with covariance $R$, the optimal weights are $c = R^{-1} h$, the optimum combiner. MRC is the case $R$ diagonal. With interference, this is [beamforming](/beamforming/) for the largest SINR.
- **Space-time codes.** The [Alamouti code](/alamouti-code/) gets the diversity of MRC from two transmit antennas without CSIT, at a 3 dB loss in array gain.
- **Packet combining.** [Chase combining](/chase-combining/) in [hybrid ARQ](/hybrid-arq/) applies MRC to retransmissions of the same packet, which are branches in time.

## When to use it

Use MRC whenever the receiver can estimate the gain of each branch, as with multiple receive antennas and coherent detection. It gives the best SNR of any linear combiner at the same cost in arithmetic as equal gain combining. Use [equal gain combining](/equal-gain-combining/) when the branch amplitudes are not reliable, and [selection combining](/selection-combining/) when only one receiver chain is available. With noncoherent or differential detection, where the phases are not known, combine the detector outputs, not the signals.

## Pitfalls

- **Unequal noise powers ignored.** Using $c_l = h_l$ when the $N_{0,l}$ differ is not MRC, and it can lose SNR. Divide by the noise power, as in line L1.
- **Channel estimation errors.** The output SNR is the sum only with perfect CSIR. With estimated gains the noise of the estimate adds a loss, and a branch with a poor estimate can harm the result. See [channel estimation](/channel-estimation/).
- **Correlated branches.** The diversity order is $L$ only for independent branches. Antennas spaced too closely have correlated fades; the mean output SNR stays $L\bar\gamma$, but the error rate falls more slowly.
- **Mean per branch against total.** Error rates for $L$ branches are often given against $\bar\gamma$ per branch. Against the total received power $L\bar\gamma$, the array gain disappears from the curve and only the diversity gain remains.

## Implementations

## History

Kahn (1954) described a ratio squarer for diversity radio reception, a combiner that weights the receiver outputs by their signal levels. Brennan (1959) gave the name maximal ratio combining, showed that it maximizes the output SNR among linear combiners, and compared it with equal gain and selection combining in Rayleigh fading. MRC became the reference against which other diversity receivers are measured, and the rake receiver applies the same weighting to the delayed copies of a multipath signal.

## References
