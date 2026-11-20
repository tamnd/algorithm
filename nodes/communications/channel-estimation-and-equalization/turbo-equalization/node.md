---
tag: XNK681
kind: algorithm
slug: turbo-equalization
name: Turbo equalization
aliases:
- iterative equalization and decoding
area: communications/channel-estimation-and-equalization
level: advanced
summary: "Exchanges extrinsic LLRs between a soft-output equalizer and a channel decoder through an interleaver, over several iterations. It works well in practice, but no general convergence theorem holds."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of code symbols, L: the number of channel taps, I: the number of iterations}
  time: {worst: O(I N 2^L)}
  space: {extra: O(N 2^L)}
properties: {deterministic: true, iterative: true, soft_output: true, exact_map: false, convergence_guaranteed: false, needs_channel: true, needs_noise_level: true}
history:
  year: 1995
  people: [Catherine Douillard, Michel Jézéquel, Claude Berrou]
  note: "Douillard, Jézéquel, Berrou and their coauthors at ENST Bretagne applied the turbo principle of iterative decoding to a convolutional code sent over an ISI channel in 1995. Tüchler, Koetter and Singer (2002) replaced the MAP equalizer by a soft MMSE equalizer and studied the loop in detail."
prereqs: [bcjr-algorithm, turbo-decoding, channel-equalization]
see_also: [soft-interference-cancellation-equalizer, viterbi-equalizer, interleaving, convolutional-code, bit-interleaved-coded-modulation, factor-graph, belief-propagation, maximum-likelihood-sequence-estimation]
sources:
  - paper: doi:10.1002/ett.4460060506
    title: "Catherine Douillard, Michel Jézéquel, Claude Berrou and others, Iterative correction of intersymbol interference: turbo-equalization, European Transactions on Telecommunications 6(5), 1995, pages 507 to 511"
    locator: "the receiver that iterates a soft-output equalizer and a soft-output decoder of a convolutional code through an interleaver"
  - paper: doi:10.1109/TCOMM.2002.1006557
    title: "Michael Tüchler, Ralf Koetter and Andrew C. Singer, Turbo equalization: principles and new results, IEEE Transactions on Communications 50(5), 2002, pages 754 to 767"
    locator: "the exchange of extrinsic information, the MAP and the MMSE equalizers in the loop, and the convergence analysis by simulation"
  - paper: doi:10.1109/MSP.2004.1267050
    title: "Ralf Koetter, Andrew C. Singer and Michael Tüchler, Turbo equalization, IEEE Signal Processing Magazine 21(1), 2004, pages 67 to 80"
    locator: "a tutorial on the turbo equalization loop"
  - paper: doi:10.1109/TIT.1974.1055186
    title: "L. R. Bahl, J. Cocke, F. Jelinek and J. Raviv, Optimal decoding of linear codes for minimizing symbol error rate, IEEE Transactions on Information Theory 20(2), 1974, pages 284 to 287"
    locator: "the forward and backward recursions used by both the equalizer and the decoder"
---

Turbo equalization is a receiver for coded data sent over a channel with intersymbol interference. It has two soft-in soft-out blocks: an equalizer that knows the channel and a decoder that knows the code. An interleaver sits between them. The equalizer computes an LLR for each code bit from the received samples and from prior LLRs. The decoder takes these as its input and returns new LLRs for the code bits. Each block passes on only its **extrinsic** part, the information that the other block did not give it, and the loop runs a few times. Douillard and others introduced it in 1995, by analogy with [turbo decoding](/turbo-decoding/). The page is about the loop. The [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/) is one equalizer for the loop, with a cost polynomial in the channel length; this page uses the exact [BCJR](/bcjr-algorithm/) equalizer, with a cost exponential in the channel length. Turbo equalization works very well in practice, often close to a receiver for the same code without ISI. There is no general convergence theorem: the loop is not proved to converge, and when it settles, the result is not proved to be the MAP decision.

## In plain words

A coded message goes through a channel with echoes. The equalizer looks at the received signal and gives, for each bit, a guess with a level of confidence. The decoder knows that only some bit patterns are valid codewords, so it can improve those guesses. It passes back only what it learned from the code. The equalizer then uses these better guesses for the neighbours of each bit to undo the echoes better, and passes back only what it learned from the signal. A shuffler between the two spreads neighbouring bits apart, so that the errors of one block look random to the other. After a few rounds, the guesses usually stop changing and are much better than after one round. Nobody has proved that this always happens.

## The problem

The input is the received sequence of a coded block. The transmitter encodes $K$ information bits $u$ with a convolutional code into $N$ code bits $c$, permutes them with an interleaver $\pi$, maps them to BPSK, $x_i = 1 - 2 c_{\pi(i)}$, and sends them through a real channel $h$ of $L$ taps with noise $N(0, \sigma^2)$:
$$y_m = \sum_{l=0}^{L-1} h_l\, x_{m-l} + w_m, \qquad m = 0, \ldots, N + L - 2.$$
The receiver knows $h$, $\sigma^2$, the code and $\pi$. The output is an LLR $L(u_k) = \ln P(u_k = 0 \mid y) / P(u_k = 1 \mid y)$ for each information bit, or an approximation of it, and the decision $\hat u_k = [L(u_k) < 0]$. The exact posterior is a sum over all $2^K$ messages, through the code and the channel at once. Because of the interleaver, the joint trellis of code and channel is too large to search. Turbo equalization splits the problem into the two trellises it can handle.

The code on this page is the rate 1/2 feedforward code with generators 7 and 5 in octal, with two tail bits, so $N = 2(K + 2)$. The interleaver is a random permutation with a fixed seed.

## The algorithm

```pseudo id=main
TURBO-EQUALIZE(y, h, σ², π, I)
L1  L_a^E ← (0, ..., 0)                        ▷ no prior on the code bits at first
L2  for i ← 1 to I do
L3      L_e^E ← BCJR-EQUALIZER(y, h, σ², L_a^E)  ▷ extrinsic: posterior minus L_a^E
L4      L_a^D ← DEINTERLEAVE(L_e^E, π)
L5      (L(u), L_e^D) ← BCJR-DECODER(L_a^D)      ▷ info bit posteriors, code bit extrinsics
L6      L_a^E ← INTERLEAVE(L_e^D, π)
L7      û_i ← [L(u) < 0]                         ▷ the decisions after iteration i
L8  return û_1, ..., û_I
```

Line L1 starts with no prior. Line L3 runs the [BCJR algorithm](/bcjr-algorithm/) on the channel trellis. Its state is the last $L - 1$ symbols, so it has $2^{L-1}$ states and $2^L$ edges per step. The edge from state $(x_{t-1}, \ldots, x_{t-L+1})$ with symbol $x_t$ has the metric
$$\gamma_t = -\frac{1}{2\sigma^2} \Big(y_t - \sum_{l=0}^{L-1} h_l\, x_{t-l}\Big)^2 + \frac{x_t\, L_a^E(x_t)}{2}.$$
The channel starts empty, and the last $L - 1$ samples are added as a metric on the final state. The output is the posterior LLR of each $x_t$ minus its prior, so it carries only the channel information. Line L4 puts the LLRs in code order. Line L5 runs the BCJR algorithm on the 4-state code trellis, with $\tfrac12 \sum_j (1 - 2 c_j) L_a^D(c_j)$ as the edge metric and the zero end state. It returns the posterior LLRs of the information bits and, for each code bit, its posterior LLR minus $L_a^D$. Line L6 sends these back in channel order. Lines L3 and L5 must subtract the prior; this is what makes the exchange extrinsic.

## Example

**What a prior does in the equalizer.** Take $h = (1, 0.5)$, $\sigma^2 = 0.5$, two symbols and $y = (0.9, 0.2, -0.6)$. The four symbol pairs have the squared distances below, and the metric is $-d/(2\sigma^2) = -d$.

| $(x_0, x_1)$ | $(+1,+1)$ | $(+1,-1)$ | $(-1,+1)$ | $(-1,-1)$ |
|---|---|---|---|---|
| $d$ | 2.91 | 0.51 | 4.91 | 6.51 |

With no priors, $L_e(x_0) = \ln(e^{-2.91} + e^{-0.51}) - \ln(e^{-4.91} + e^{-6.51}) = 4.303$, and $L_e(x_1) = -2.276$. If the decoder now says $L_a(x_1) = +4$, the pairs with $x_1 = +1$ get $+2$ and the others $-2$. Then $L_e(x_0) = \ln(e^{-0.91} + e^{-2.51}) - \ln(e^{-2.91} + e^{-8.51}) = 2.180$. With $L_a(x_1) = -4$, $L_e(x_0) = 5.915$. So the decoder's view of $x_1$ changes what the equalizer says about $x_0$, while $L_e(x_1)$ stays at $-2.276$ in all three cases, because it is extrinsic.

**The loop on the Proakis B channel.** Send $K = 3000$ bits (seed 11) with the (7, 5) code over $h = (0.407, 0.815, 0.407)$, with $\sigma^2 = 1 / (E_b/N_0)$, since $E_s = 1$ and the rate is 1/2. The table gives the bit errors among the 3000 after each iteration. This is a measurement.

| $E_b/N_0$ | iteration 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 3.0 dB | 232 | 58 | 25 | 21 |
| 3.5 dB | 179 | 29 | 4 | 6 |
| 4.0 dB | 119 | 9 | 2 | 2 |

Iteration 1 is the usual receiver that equalizes and then decodes. The second iteration cuts the errors by a factor of 4 to 13. At 3.5 dB, iteration 4 has more errors than iteration 3: the loop is not monotone, and a few errors move around.

## Correctness

**What is exact.** Line L3 returns the exact extrinsic LLRs of the symbols for the channel model and independent priors $L_a^E$. Line L5 returns the exact posteriors of the information bits and the exact extrinsic LLRs of the code bits for the code and independent priors $L_a^D$. Both are theorems: they are the BCJR algorithm, which is the [forward-backward algorithm](/forward-backward-algorithm/) on a trellis. The tests check both against sums over all paths, to $10^{-9}$, for 8 symbols of the channel and 6 information bits of the code.

**What is a heuristic.** Each block treats its input LLRs as independent priors. They are not: after the first iteration, they come from the same received block and are correlated. The interleaver makes the correlation weak between bits that are close in one order, which is why the loop works, but it does not remove it. So after iteration 1, $L(u)$ is not the true posterior. Turbo equalization is an instance of loopy [belief propagation](/belief-propagation/) on the [factor graph](/factor-graph/) of code, interleaver and channel, and this graph has cycles.

**No convergence theorem.** No general theorem says that the loop converges, that it converges to the MAP decisions, or that each iteration lowers the error rate. The example above shows a case where an iteration raises it. In practice, the loop converges in a few iterations above a threshold signal-to-noise ratio. EXIT charts, which track the mutual information of the LLRs through each block, predict this threshold well for long blocks, but they are a model, not a proof. The test checks a measured drop: with the Wilson interval at $z = 3.29$, the error rate after iteration 2 is below the error rate after iteration 1, for 3000 bits at 3.5 dB on Proakis B.

## Complexity

Line L3 has $2^{L-1}$ states and $2^L$ edges per symbol, so it costs $O(N 2^L)$ per iteration in the [real RAM](/real-ram/), with $O(N 2^L)$ space for the forward metrics. Line L5 costs $O(N)$ for a 4-state code. $I$ iterations cost $O(I N 2^L)$ time. For an $M$-ary alphabet, the equalizer has $M^{L-1}$ states, which is why the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/), with a polynomial cost, replaces it for long channels and large alphabets.

## Properties

- **Extrinsic exchange.** Each block subtracts the prior it received. Without this, the loop feeds information back to its source and becomes overconfident.
- **Gain from the code.** With a good interleaver and enough signal, the bit error rate can come close to that of the same code without ISI. This is an observation from simulations, not a theorem.
- **No guarantee.** There is no general convergence theorem, and an iteration can make things worse.
- **The first iteration is the separate receiver.** Iteration 1 equals a MAP equalizer followed by a MAP decoder.
- **Needs the channel.** The equalizer needs $h$ and $\sigma^2$; in practice they are estimated, also inside the loop.

## Variants and improvements

- **MMSE equalizer.** Replace line L3 by the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/) of Tüchler, Koetter and Singer.
- **Max-log BCJR.** Replace the log-sum-exp in both blocks by a maximum. This is cheaper and loses a little.
- **Reduced-state equalizers.** Use [reduced-state sequence estimation](/reduced-state-sequence-estimation/) or a [Viterbi equalizer](/viterbi-equalizer/) with soft outputs when the channel is long.
- **Higher-order modulation.** With [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/), the equalizer passes symbol probabilities through a [soft demapper](/soft-demapping/).
- **Channel estimation in the loop.** Use the soft symbols from the decoder as extra pilots to improve the channel estimate at each iteration.
- **Frequency-domain turbo equalization.** With a cyclic prefix, the MMSE equalizer runs in the frequency domain, as in [frequency domain equalization](/frequency-domain-equalization/).

## When to use it

Use turbo equalization when the data is coded, the channel has strong ISI, and the receiver can afford a few passes over each block. It gives large gains on hard channels such as Proakis B. On mild channels, a linear equalizer and a separate decoder lose little. For long channels or large alphabets, use an MMSE equalizer in the loop in place of the BCJR equalizer. For low delay, limit the number of iterations.

## Pitfalls

- **Passing posteriors in line L3 or line L5.** Subtract the prior before passing the LLRs on; posteriors count the same information twice.
- **No interleaver or a short one.** Without a good interleaver in line L4 and line L6, neighbouring bits share errors in both blocks, and the loop gains little.
- **Sign conventions.** With $x = 1 - 2b$ and $L = \ln P(b = 0) / P(b = 1)$, a positive LLR favors $x = +1$. A mismatch between the equalizer and the decoder makes the loop diverge.
- **Wrong noise variance in the metric of line L3.** The LLRs scale with $1/\sigma^2$, and a wrong scale makes the decoder over or under trust them.
- **Overflow.** Work in the log domain with a stable log-sum-exp, as the code does.
- **Expecting monotone progress.** The error count can rise in some iterations; stop after a fixed number or when the decisions stop changing.

## Implementations

## History

Douillard, Jézéquel, Berrou and their coauthors published turbo equalization in 1995, two years after turbo codes, for a convolutional code over an ISI channel with a soft-output equalizer and decoder. Bahl, Cocke, Jelinek and Raviv (1974) had given the forward-backward algorithm that both blocks use. Tüchler, Koetter and Singer (2002) studied the loop with MAP and MMSE equalizers, and Koetter, Singer and Tüchler (2004) wrote a tutorial on it.

## References
