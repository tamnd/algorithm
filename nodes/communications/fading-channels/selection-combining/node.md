---
tag: 611EDQ
kind: algorithm
slug: selection-combining
name: Selection combining
aliases:
- selection diversity
area: communications/fading-channels
level: intro
summary: "Uses only the diversity branch with the largest instantaneous SNR. It needs one receiver chain after a switch and still has diversity order L, but less SNR than maximal ratio combining."
solves: [symbol-detection]
model: real-ram
complexity:
  vars: {L: the number of diversity branches}
  time: {worst: O(L)}
  space: {extra: O(1)}
properties: {needs_branch_phases: false, needs_one_receiver_chain: true, optimal_linear_combiner: false, diversity_order: L}
history:
  year: 1959
  people: [D. G. Brennan]
  note: "Selection between antennas is the simplest diversity method. Brennan (1959) analyzed it with maximal ratio and equal gain combining."
prereqs: [rayleigh-fading-channel, diversity-order]
see_also: [maximal-ratio-combining, equal-gain-combining, diversity-order, outage-probability, rayleigh-fading-channel, noncoherent-detection, multiuser-diversity, link-adaptation]
sources:
  - paper: doi:10.1109/JRPROC.1959.287136
    title: "D. G. Brennan, Linear diversity combining techniques, Proceedings of the IRE 47(6), 1959, pages 1075 to 1102"
    locator: "the analysis of selection diversity and its comparison with maximal ratio and equal gain combining"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Section 7.2.2 (selection combining)"
  - book: isbn:9780471649533
    title: "Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, 2nd edition, Wiley, 2005"
    locator: "Chapter 9 (diversity combining), including the selection combining receivers"
---

Selection combining (SC) is a diversity receiver that measures the SNR of each of $L$ branches and uses only the branch with the largest one. Like [maximal ratio combining](/maximal-ratio-combining/) and [equal gain combining](/equal-gain-combining/), it has [diversity order](/diversity-order/) $L$ with independent branches, but it does not add the branches: its output SNR is the maximum of the branch SNRs, not their sum. It needs no phase alignment and only one receiver chain after an antenna switch, which makes it the simplest of the three.

## In plain words

The same message arrives over several antennas, and at any moment some copies are in a deep fade while others are strong. Selection combining looks at all copies, picks the one that is cleanest right now, and ignores the others. It does not need to line up the phases of the copies or weigh them, so the receiver can be one radio behind a switch. The chance that every copy is in a deep fade at the same time is small, so the selected copy is rarely bad. The cost is that the energy of the other copies is thrown away.

## The problem

Branch $l = 1, \ldots, L$ receives $y_l = h_l x + w_l$, where $x$ is the transmitted symbol with energy $E_s$, $h_l$ is the complex fading gain, and $w_l \sim CN(0, N_{0,l})$ is noise, independent across branches. The branch SNR is $\gamma_l = |h_l|^2 E_s/N_{0,l}$, with mean $\bar\gamma$ per branch. The receiver can measure the $\gamma_l$, which is CSIR on the branch qualities. The task is to choose one branch and pass its signal to a [symbol detector](/symbol-detection/). The gains may follow block fading, where the choice holds for a codeword, or fast fading, where it changes with every symbol. There is no CSIT.

## The algorithm

```pseudo id=main
SELECT(h[1..L], y[1..L], N0[1..L])
L1  s_l ← |h_l|² / N0_l  for l = 1 .. L            ▷ the branch SNRs per unit symbol energy
L2  k ← argmax_l s_l
L3  x̂ ← conj(h_k) · y_k / |h_k|²                  ▷ the estimate from branch k alone
L4  return x̂, k
```

Line L1 computes the quality of each branch and line L2 picks the best one. Line L3 removes the gain of the chosen branch, so that $\hat x = x + n$ with $n \sim CN(0, N_{0,k}/|h_k|^2)$, and the output SNR is $\gamma_{\mathrm{SC}} = \max_l \gamma_l$. With a [noncoherent detector](/noncoherent-detection/), line L3 is replaced by the detector of the chosen branch, and only the amplitudes are needed for line L1.

## Example

Take $L = 2$, $E_s = 1$, the gains $h_1 = 2$ and $h_2 = 1$, and the noise powers $N_{0,1} = 8$ and $N_{0,2} = 1$. Line L1 gives $s_1 = 0.5$ and $s_2 = 1$, so branch 2 is selected, although its gain is smaller. Choosing by $|h_l|$ alone would be wrong here.

For $L$ independent [Rayleigh](/rayleigh-fading-channel/) branches with mean $\bar\gamma$ each, $\gamma_{\mathrm{SC}}$ is below $x$ only if every branch is below $x$, so the outage probability is the closed form (independent Rayleigh branches)

$$\Pr[\gamma_{\mathrm{SC}} < x] = (1 - e^{-x/\bar\gamma})^L .$$

At $\bar\gamma = 10$ dB and $x = 1$ it is 0.0952 for $L = 1$, $9.056 \cdot 10^{-3}$ for $L = 2$ and $8.20 \cdot 10^{-5}$ for $L = 4$. Maximal ratio combining gives $4.679 \cdot 10^{-3}$ for $L = 2$. The mean output SNR is $\bar\gamma(1 + \frac12 + \cdots + \frac1L)$: 1.5 times $\bar\gamma$ for $L = 2$ and 2.083 times for $L = 4$.

The bit error rate of coherent BPSK is $P_b = \frac12\sum_{k=0}^{L}(-1)^k\binom{L}{k}\sqrt{\bar\gamma/(\bar\gamma + k)}$:

| $\bar\gamma$ per branch | $L = 1$ | $L = 2$ | $L = 4$ |
|---|---|---|---|
| 5 dB | 0.06418 | 0.019701 | $4.265 \cdot 10^{-3}$ |
| 10 dB | 0.023269 | $2.9729 \cdot 10^{-3}$ | $1.4870 \cdot 10^{-4}$ |
| 20 dB | $2.4814 \cdot 10^{-3}$ | $3.6581 \cdot 10^{-5}$ | $3.003 \cdot 10^{-8}$ |

A simulation of 20000 channels with $L = 2$ at 10 dB (seed 6102) gives a Wilson interval with $z = 3.29$ that contains the outage $9.056 \cdot 10^{-3}$, and 20000 BPSK bits at 5 dB (seed 6103) give one that contains 0.019701.

## Correctness

**Claim.** The output is $\hat x = x + n$ with $n \sim CN(0, N_{0,k}/|h_k|^2)$, so the output SNR is $\max_l \gamma_l$, the best that any receiver using one branch can get. For independent Rayleigh branches with mean $\bar\gamma$: the outage is $(1 - e^{-x/\bar\gamma})^L$, the mean output SNR is $\bar\gamma H_L$ with $H_L = 1 + \frac12 + \cdots + \frac1L$, and the BPSK error rate is the alternating sum above. These are closed forms under the stated model.

**Key step.** The maximum of independent variables is below $x$ if and only if all of them are, so its distribution function is the product of theirs. The mean follows from $E\gamma = \int_0^\infty \Pr[\gamma > x]\, dx$, and the error rate from expanding $(1 - e^{-x/\bar\gamma})^L$ by the binomial theorem and integrating each exponential against $Q(\sqrt{2x})$. The full proof is in the proofs folder.

## Complexity

Lines L1 and L2 take $O(L)$ operations per decision, in the [real RAM](/real-ram/), and line L3 takes $O(1)$, with $O(1)$ extra space. In hardware, the selection needs a measurement of each branch but only one demodulator, which is the main saving against the other combiners. If the choice is made once per block, the measurement cost is shared by the whole block.

## Properties

- **Output SNR is the maximum.** $\gamma_{\mathrm{SC}} = \max_l \gamma_l \le \sum_l \gamma_l = \gamma_{\mathrm{MRC}}$.
- **Mean gain grows slowly.** $E[\gamma_{\mathrm{SC}}] = \bar\gamma H_L$, and $H_L$ grows like $\ln L$. Most of the benefit of SC is in the lower tail, not in the mean.
- **Diversity order $L$.** For independent Rayleigh branches, $\Pr[\gamma_{\mathrm{SC}} < x] \approx (x/\bar\gamma)^L$ for large $\bar\gamma$, so the outage and the error rate fall as $\bar\gamma^{-L}$, the same slope as for maximal ratio combining.
- **No phase needed.** SC does not combine signals, so it works with coherent and with noncoherent detection.
- **Comparison at $L = 2$ and 10 dB.** The BPSK error rate is $2.973 \cdot 10^{-3}$ for SC, $2.070 \cdot 10^{-3}$ for equal gain combining and $1.599 \cdot 10^{-3}$ for maximal ratio combining.

## Variants and improvements

- **Selection by received power.** Measuring the SNR of each branch is hard; practical receivers often select the branch with the largest total power, signal plus noise. With equal noise powers this gives the same choice.
- **Switched diversity.** Switch-and-stay combining monitors only the current branch and switches when its SNR falls below a threshold. It needs one measurement at a time, at the cost of more outage than full selection.
- **Generalized selection combining.** Combining the best $L_c$ of the $L$ branches with maximal ratio weights lies between SC ($L_c = 1$) and maximal ratio combining ($L_c = L$).
- **Transmit antenna selection.** With feedback, the transmitter can use only its best antenna. This is SC moved to the transmitter, with the same output SNR $\max_l \gamma_l$.
- **Selection over users.** [Multiuser diversity](/multiuser-diversity/) schedules the user with the best channel, which is selection over users instead of antennas.

## When to use it

Use SC when only one receiver chain is affordable, when the detection is noncoherent, or when the branch phases cannot be tracked. It gives the full diversity order of the antennas at the smallest hardware cost. When each branch has its own receiver chain and channel estimates, [maximal ratio combining](/maximal-ratio-combining/) gives a higher SNR at almost no extra cost in arithmetic.

## Pitfalls

- **Selecting by gain instead of SNR.** With different noise powers, the branch with the largest $|h_l|$ is not the best one, as in the example. Select by $|h_l|^2/N_{0,l}$.
- **Stale selection.** The choice is based on a measurement. If the fading changes before the selection takes effect, which happens in fast fading or with a slow switch, the selected branch is no longer the best one and the diversity gain falls. Compare the measurement delay with the [coherence time](/coherence-time/).
- **Correlated branches.** The product formula for the outage needs independent branches. Closely spaced antennas fade together, and SC then gains much less.
- **Switching transients.** Switching an analog front end during a symbol creates phase and amplitude jumps. Switch at symbol or block boundaries.

## Implementations

## History

Choosing the best of several antennas or receivers is the simplest diversity method, because it needs no combining of signals. Brennan (1959) gave a unified analysis of linear diversity combining, in which selection diversity is compared with maximal ratio and equal gain combining for Rayleigh fading. Later work added switched diversity for simple receivers, generalized selection combining, and transmit antenna selection with feedback.

## References
