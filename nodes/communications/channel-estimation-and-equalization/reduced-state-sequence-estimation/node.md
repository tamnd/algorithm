---
tag: J2DFVA
kind: algorithm
slug: reduced-state-sequence-estimation
name: Reduced-state sequence estimation
aliases:
- RSSE
- delayed decision-feedback sequence estimation
- DDFSE
area: communications/channel-estimation-and-equalization
level: advanced
summary: Cuts the trellis of the Viterbi equalizer by keeping only part of the channel memory as state and feeding back decisions for the rest.
solves: [channel-equalization]
model: word-ram
complexity:
  vars: {N: the number of symbols, M: the alphabet size, L: the number of channel taps, S: "the number of states, J_1 J_2 ... J_K"}
  time: {worst: O(N S (M + L))}
  space: {extra: O(N S)}
properties: {deterministic: true, exact_ml: "only with full partitions", needs_channel: true, needs_minimum_phase: true, states: "J_1 J_2 ... J_K, between 1 and M^(L-1)"}
history:
  year: 1988
  people: [M. Vedat Eyuboglu, Shahid U. H. Qureshi]
  note: "Eyuboglu and Qureshi defined the reduced trellis by nested set partitions of the alphabet with decision feedback per survivor. Duel-Hallen and Heegard published the special case DDFSE in 1989."
prereqs: [viterbi-equalizer, decision-feedback-equalizer]
see_also: [whitened-matched-filter, per-survivor-processing, ungerboeck-mlse-receiver, trellis-coded-modulation, maximum-likelihood-sequence-estimation, beam-search, k-best-detector, turbo-equalization]
sources:
  - paper: "M. Vedat Eyuboglu and Shahid U. H. Qureshi, Reduced-state sequence estimation with set partitioning and decision feedback, IEEE Transactions on Communications 36(1), 1988, pages 13 to 20"
    locator: "the subset trellis, the nesting condition on the partitions and the decision feedback per survivor"
  - paper: "Alexandra Duel-Hallen and Chris Heegard, Delayed decision-feedback sequence estimation, IEEE Transactions on Communications 37(5), 1989, pages 428 to 436"
    locator: "the trellis on the first mu channel taps with decision feedback per survivor for the rest"
---

Reduced-state sequence estimation (RSSE) is a family of detectors between the [Viterbi equalizer](/viterbi-equalizer/) and the [decision feedback equalizer](/decision-feedback-equalizer/). The Viterbi equalizer for a channel with $L$ taps and an alphabet of $M$ points keeps $M^{L-1}$ states, which is too many for long channels or large constellations. RSSE keeps only partial information about the recent symbols in the state: for each of the last $K$ symbols, the label of the subset of the alphabet that holds it. The subsets come from nested partitions, like the set partitioning of [trellis-coded modulation](/trellis-coded-modulation/). The rest of the intersymbol interference is cancelled with the symbols stored on each survivor path, so each survivor runs its own decision feedback. With full partitions RSSE is the Viterbi equalizer. With no partition it is the DFE. Delayed decision-feedback sequence estimation (DDFSE) is the special case that keeps the first $\mu$ symbols in full, with $M^\mu$ states.

## In plain words

The full Viterbi equalizer remembers every possible combination of the last few symbols. That is safe but costly. A DFE remembers only its own best guess, so one wrong guess spoils the next ones. RSSE keeps a few guesses alive, but only where a wrong guess is likely. It keeps the most recent symbols, whose taps are large, and among them it only keeps apart the symbols that are close to each other and easy to confuse. Symbols that are far apart are decided on each path at once, because the risk of mixing them up is small.

## The problem

The input is a known channel $f = (f_0, \ldots, f_{L-1})$ with $f_0 \ne 0$, usually minimum phase after a [whitened matched filter](/whitened-matched-filter/), an alphabet $\mathcal{A}$ of $M$ points, the known symbols before the block, the samples $y_k = \sum_l f_l x_{k-l} + n_k$, and a list of $K \le L-1$ partitions $\Omega(1), \ldots, \Omega(K)$ of $\mathcal{A}$ into $J_1 \ge J_2 \ge \cdots \ge J_K$ subsets. Each partition must refine the next one: two points in the same subset of $\Omega(i)$ are in the same subset of $\Omega(i+1)$. The output is a sequence $\hat x \in \mathcal{A}^N$ with a small $\sum_k |y_k - \sum_l f_l \hat x_{k-l}|^2$, found with $S = J_1 \cdots J_K$ states.

## The algorithm

Write $\ell_i(a)$ for the label of the subset of $\Omega(i)$ that holds $a$. The state at time $k$ is $t_k = (\ell_1(x_{k-1}), \ell_2(x_{k-2}), \ldots, \ell_K(x_{k-K}))$. Each state keeps one survivor: a metric and the last $L-1$ symbols of its path.

```pseudo id=main
RSSE(y, f, A, Ω(1..K), pre)
L1  survivors ← { state of pre: (metric 0, history pre) }
L2  for k ← 0 to N - 1
L3      for each survivor (t, metric, hist):  isi ← Σ_{l=1}^{L-1} f[l] hist[l]     ▷ its own past symbols
L4          for each symbol a in A
L5              λ ← |y[k] - f[0] a - isi|²
L6              t' ← (ℓ_1(a), ℓ_2(hist[1]), …, ℓ_K(hist[K-1]))
L7              if metric + λ is the smallest into t' so far, keep it with history (a, hist) and a pointer
L8  take the survivor with the smallest metric and follow the pointers back
L9  return its symbols
```

Line L3 is the decision feedback: the ISI comes from the survivor's own history, not from a common decision. Line L6 builds the next state. The nesting makes it depend only on $t$ and $\ell_1(a)$, so the trellis is well defined. Symbols with the same $\ell_1$ are parallel branches, and line L7 keeps the best one. The choices of partitions give the whole family:

| partitions | states | detector |
|---|---|---|
| $K = L-1$, all into single points | $M^{L-1}$ | Viterbi equalizer, exact ML |
| $K = \mu$, all into single points | $M^\mu$ | DDFSE |
| $K = 1$, $\Omega(1)$ into $J$ subsets | $J$ | RSSE with one partition |
| $K = 0$ | 1 | zero-forcing DFE on $f$ |

## Example

Take $f = (1, 0.6, 0.3)$, BPSK, the known symbols $x_{-1} = x_{-2} = +1$, and DDFSE with $\mu = 1$, so the state is $x_{k-1}$ and there are 2 states in place of 4. Each survivor stores its own $x_{k-2}$. The transmitted block is $(+1, +1, +1, +1, -1)$, and the received samples are $y = (1.4, 0.8, 1.8, 1.4, 0.0)$. Each cell shows the metric of the survivor and its path:

| $k$ | $y_k$ | state $+1$ | state $-1$ |
|---|---|---|---|
| 0 | 1.4 | 0.25: $+$ | 2.25: $-$ |
| 1 | 0.8 | 1.46: $++$ | 1.06: $+-$ |
| 2 | 1.8 | 1.47: $+++$ | 5.07: $++-$ |
| 3 | 1.4 | 1.72: $++++$ | 3.72: $+++-$ |
| 4 | 0.0 | 4.21: $+++-+$ | 1.73: $++++-$ |

At $k = 1$ the ISI of the true past is $0.6 + 0.3 = 0.9$, so the sample $0.8$ is closer to $0.9 - 1$ than to $0.9 + 1$, and the path $+-$ has the smaller metric. A DFE decides $x_1 = -1$ here and goes wrong. DDFSE keeps the path $++$ in the other state. At $k = 2$, the sample 1.8 fits $++$ followed by $+$ almost exactly ($1.8 - 1 - 0.6 - 0.3 = -0.1$), and the path $+-$ dies. The final answer $(+1, +1, +1, +1, -1)$ is correct and is the same as the 4-state ML answer. The DFE gives $(+1, -1, +1, +1, -1)$.

Measured with 200 blocks of 50 BPSK symbols on this channel at noise standard deviation 0.35 (seed 7703), the 2-state DDFSE gave the same block as 4-state ML 198 times, and the DFE 184 times. On 4-PAM with $f = (1, 0.7)$ and 2 states (seed 7704, 200 blocks of 40 symbols, deviation 0.35), the set partition $\{+3, -1\}, \{+1, -3\}$ agreed with the 4-state ML result on all 200 blocks. The partition $\{+3, +1\}, \{-1, -3\}$ agreed on 182 and the DFE on 177. The good partition keeps apart the neighbours, which are the points easy to confuse, and lets each survivor decide between points at the distance 4.

## Correctness

**Claim.** The trellis is well defined when the partitions are nested, and each survivor metric is the exact Euclidean metric of its own path. With full partitions RSSE is exact maximum likelihood. With no partition it is the zero-forcing DFE on $f$. Without noise it returns the transmitted sequence for every choice of partitions.

**Key step.** The nesting makes the label $\ell_{i+1}(x_{k-i})$ a function of $\ell_i(x_{k-i})$, so the next state depends only on the current state and the label of the new symbol. Since the ISI uses the survivor's own symbols, its metric is the true metric of its path. Without noise the true path has metric 0 and no other path does, so it always survives. RSSE is not exact in general, because two paths in one reduced state can differ in symbols that the state does not hold, and the compare step drops one of them. The proofs folder has the details.

## Complexity

Each step costs $O(L)$ per survivor for the ISI and $O(M)$ for the branches, so $N$ symbols cost $O(N S (M + L))$ in the [word RAM](/word-ram/), with the metrics as numbers of fixed precision, and $O(N S)$ space for the pointers. The full Viterbi equalizer has $M^{L-1}$ states, so the saving is the factor $M^{L-1}/S$. For DDFSE with memory $\mu$ it is $M^{L-1-\mu}$. For example, 16-QAM on 5 taps needs $16^4 = 65536$ states for ML, 16 states for DDFSE with $\mu = 1$, and 4 states for RSSE with one partition of 16-QAM into 4 subsets.

## Properties

- **A family.** One parameter set covers the DFE, DDFSE, RSSE and the Viterbi equalizer, and the cost and the performance move smoothly between them.
- **Survivor feedback.** Each survivor uses its own past decisions, so a wrong decision on one path does not spoil the others. Error propagation is much weaker than in a DFE.
- **Needs minimum phase.** The symbols outside the state are fed back from tentative decisions. If the channel energy comes late, these decisions are unreliable. The [whitened matched filter](/whitened-matched-filter/) or an MMSE prefilter puts the energy first.
- **Set partitioning.** The distance between the points inside a subset sets how reliable the per-survivor decisions are. A good partition makes the smallest such distance large, which is the same rule as in trellis-coded modulation.
- **Parallel branches.** With $J_1 < M$ there are $M/J_1$ branches between each pair of states, and the compare step picks the best of them at once.

## Variants and improvements

- **DDFSE.** The partitions into single points for the first $\mu$ symbols. It is the simplest member and is common in practice.
- **Ungerboeck metric.** RSSE can run on the [Ungerboeck metric](/ungerboeck-mlse-receiver/), but the matched filter output also holds the ISI from the future symbols, so the minimum-phase Forney form is the usual choice.
- **Per-survivor processing.** Running a channel or phase estimator on each survivor is the same idea as the per-survivor feedback. See [per-survivor processing](/per-survivor-processing/).
- **Breadth-first searches.** The M-algorithm and the T-algorithm keep a fixed number of the best paths, or the paths within a threshold, instead of one path per reduced state. They are a [beam search](/beam-search/) on the full trellis, and the [K-best detector](/k-best-detector/) is the same idea for MIMO.
- **Soft outputs.** A reduced-state BCJR or a reduced-state soft-output Viterbi algorithm gives soft outputs for [turbo equalization](/turbo-equalization/).

## When to use it

Use RSSE when the full Viterbi equalizer is too costly and the DFE loses too much: long channels with small alphabets, or large constellations on short channels. Start with DDFSE with $\mu = 1$ or 2. For large QAM constellations, use one or two set-partition levels for the first taps. Put a minimum-phase prefilter in front. If the channel is very long, use a [DFE](/decision-feedback-equalizer/) or [frequency-domain equalization](/frequency-domain-equalization/) instead.

## Pitfalls

- **Partitions that do not nest.** If two points share a subset in $\Omega(i)$ but not in $\Omega(i+1)$, the next state is not a function of the current state, and the search is not a trellis search.
- **A maximum-phase channel.** Without a minimum-phase prefilter, the large taps are fed back from early decisions and RSSE can be worse than a linear equalizer.
- **A common decision.** Feeding back one global decision for the taps outside the state, in place of each survivor's own history, gives a DFE in front of a smaller Viterbi search. It loses the main benefit.
- **The wrong partition.** Grouping neighbours into one subset, such as $\{+3, +1\}$ in 4-PAM, leaves the hard decisions to the feedback. In the example it agreed with ML on 182 blocks of 200, against 200 for the set partition.
- **Not ML.** RSSE does not guarantee the ML sequence, so a test that compares it with ML must allow some differences and report how many.

## Implementations

## History

The Viterbi equalizer of Forney (1972) has a number of states that grows exponentially with the channel memory. In 1988, Eyuboglu and Qureshi defined reduced-state sequence estimation with set partitions of the alphabet, as in Ungerboeck's trellis-coded modulation, and decision feedback on each survivor. In 1989, Duel-Hallen and Heegard published delayed decision-feedback sequence estimation, which keeps the first $\mu$ taps in the trellis and feeds back the rest along each survivor. Per-survivor processing in the 1990s took the same idea to channel and phase estimation.

## References
