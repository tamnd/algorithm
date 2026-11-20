---
tag: REAJPJ
kind: algorithm
slug: ungerboeck-mlse-receiver
name: Ungerboeck MLSE receiver
aliases:
- Ungerboeck metric
area: communications/channel-estimation-and-equalization
level: advanced
summary: Runs maximum likelihood sequence estimation directly on matched filter samples with a modified metric, without a whitening filter.
solves: [maximum-likelihood-sequence-estimation, channel-equalization]
model: word-ram
complexity:
  vars: {N: the number of symbols, M: the alphabet size, L: the number of channel taps}
  time: {worst: O(N M^(L-1) (M + L))}
  space: {extra: O(N M^(L-1))}
properties: {deterministic: true, exact_ml: true, needs_channel: true, needs_whitening: false, states: "M^(L-1)"}
history:
  year: 1974
  people: [Gottfried Ungerboeck]
  note: "Ungerboeck showed that the Viterbi algorithm can run on the matched filter outputs with a metric built from the channel autocorrelation, so the whitening filter of Forney's receiver is not needed."
prereqs: [viterbi-equalizer, matched-filter]
see_also: [whitened-matched-filter, maximum-likelihood-sequence-estimation, viterbi-algorithm, reduced-state-sequence-estimation, per-survivor-processing, faster-than-nyquist-signaling, bcjr-algorithm, intersymbol-interference]
sources:
  - paper: "Gottfried Ungerboeck, Adaptive maximum-likelihood receiver for carrier-modulated data-transmission systems, IEEE Transactions on Communications 22(5), 1974, pages 624 to 636"
    locator: "the metric on the matched filter outputs and its Viterbi search"
  - paper: "G. David Forney, Jr., Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972, pages 363 to 378"
    locator: "the receiver with the whitened matched filter, for comparison"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.3 (the optimum maximum likelihood receiver for channels with ISI and its metric on the matched filter outputs)"
---

The Ungerboeck receiver is a maximum likelihood sequence detector for channels with [intersymbol interference](/intersymbol-interference/) that works on the [matched filter](/matched-filter/) outputs $z_k$ directly. The matched filter outputs are sufficient statistics, but their noise is colored, so the plain Euclidean metric of the [Viterbi equalizer](/viterbi-equalizer/) does not apply to them. Forney whitened the noise first with the [whitened matched filter](/whitened-matched-filter/). Ungerboeck instead expanded the exact log-likelihood of the received samples. It splits into one term per symbol that uses $z_k$, the channel autocorrelation $R_m$ and the $L-1$ symbols before $x_k$. So the [Viterbi algorithm](/viterbi-algorithm/) runs on the same trellis with $M^{L-1}$ states and gives the same decisions, with no spectral factorization and no anticausal filter.

## In plain words

The matched filter is the best first step of a receiver, because it keeps everything that matters about the symbols. Its outputs overlap each other, and so does their noise. Forney's receiver removes the overlap in the noise with an extra filter and then measures distances. Ungerboeck's receiver keeps the matched filter outputs as they are. It scores a guessed sequence by how well each guessed symbol correlates with its matched filter output, minus a correction for the energy of the symbol and for its overlap with the symbols just before it. The score is the same as the distance score up to a constant, so both receivers pick the same sequence.

## The problem

The input is a known channel $h = (h_0, \ldots, h_{L-1})$, an alphabet $\mathcal{A}$ of $M$ points, and the samples $y_k = \sum_l h_l x_{k-l} + w_k$ for $k = 0, \ldots, N + L - 2$, with $x_k = 0$ outside the block of $N$ symbols and $w$ white $\mathcal{CN}(0, N_0)$. The output is the sequence $\hat x \in \mathcal{A}^N$ that minimizes $\|y - h * x\|^2$, the maximum likelihood sequence. The receiver may also know some tail symbols at the end of the block.

## The algorithm

With $z_k = \sum_l \bar h_l\, y_{k+l}$ and $R_m = \sum_i h_{i+m} \bar h_i$, the identity
$$\|y\|^2 - \|y - h * x\|^2 = \sum_{k=0}^{N-1} \Big( 2\,\mathrm{Re}(\bar x_k z_k) - R_0 |x_k|^2 - 2\,\mathrm{Re}\Big(\bar x_k \sum_{m=1}^{L-1} R_m x_{k-m}\Big) \Big)$$
holds for every $y$ and $x$. The term for $k$ depends on $x_k$ and the state $(x_{k-1}, \ldots, x_{k-L+1})$, so it is a branch metric. The receiver maximizes the sum.

```pseudo id=main
UNGERBOECK-MLSE(y, h, A)
L1  z[k] ← Σ_l conj(h[l]) y[k + l]  for k = 0 … N-1          ▷ the matched filter
L2  R[m] ← Σ_i h[i + m] conj(h[i])  for m = 0 … L-1           ▷ the autocorrelation
L3  metric[s] ← 0 for the start state (all past symbols 0), -∞ for the others
L4  for k ← 0 to N - 1
L5      for each state s and each symbol a allowed at k
L6          λ ← 2 Re(conj(a) z[k]) - R[0] |a|² - 2 Re(conj(a) Σ_{m≥1} R[m] x[k-m](s))
L7          if metric[s] + λ > new[next(s, a)] then keep it and set the pointer
L8  s ← the state with the largest metric; follow the pointers back
L9  return the symbols on the path
```

Line L1 is the matched filter, sampled at the symbol rate. Line L2 needs only the channel autocorrelation, which an adaptive receiver can estimate directly. Line L6 is the Ungerboeck branch metric: a correlation with the matched filter output, the energy of the symbol, and its correlation with the past symbols of the state. Lines L4 to L7 are the add-compare-select step of the Viterbi algorithm with a maximum in place of a minimum.

## Example

Take $h = (1, 0.5)$ and BPSK, so $R_0 = 1.25$ and $R_1 = 0.5$, and the branch metric is $2 a z_k - 1.25 - a\, x_{k-1}$. The block is $x = (+1, -1, -1, +1)$, the noiseless samples are $(1, -0.5, -1.5, 0.5, 0.5)$, and the received samples are $y = (0.9, 0.1, -1.2, 0.6, 0.4)$. The matched filter gives $z_k = y_k + 0.5\, y_{k+1}$, so $z = (0.95, -0.5, -0.9, 0.8)$. Each cell shows the best metric into the state and the state it came from:

| $k$ | $z_k$ | state $+1$ | state $-1$ |
|---|---|---|---|
| 0 | 0.95 | 0.65 from the start | -3.15 from the start |
| 1 | -0.5 | -2.6 from $+1$ | 1.4 from $+1$ |
| 2 | -0.9 | -0.65 from $-1$ | 0.95 from $-1$ |
| 3 | 0.8 | 2.3 from $-1$ | -2.5 from $+1$ |

At $k = 0$ there is no past symbol, so the metric for $a = +1$ is $1.9 - 1.25 = 0.65$. At $k = 2$, the state $+1$ compares $-2.6 + (-1.8 - 1.25 - 1) = -6.65$ from $+1$ with $1.4 + (-1.8 - 1.25 + 1) = -0.65$ from $-1$. The best final metric is 2.3 in the state $+1$, and the traceback gives $\hat x = (+1, -1, -1, +1)$. As a check, $\|y\|^2 = 2.78$ and $\|y - h * \hat x\|^2 = 0.48$, and $2.78 - 0.48 = 2.3$. The metrics are not distances: they can be negative and they can fall from one step to the next.

## Correctness

**Claim.** The returned sequence maximizes the Ungerboeck metric, and so it minimizes $\|y - h * x\|^2$. It is the maximum likelihood sequence, the same as the one the [Viterbi equalizer](/viterbi-equalizer/) finds after a whitened matched filter.

**Key step.** Expand $\|y - \mathbf{H}x\|^2 = \|y\|^2 - 2\,\mathrm{Re}(x^H \mathbf{H}^H y) + x^H \mathbf{H}^H \mathbf{H} x$. The vector $\mathbf{H}^H y$ is $z$, and $\mathbf{H}^H \mathbf{H}$ is the Toeplitz matrix of $R$. The quadratic form splits into the diagonal and the pairs $(k, k - m)$, and each pair gives $2\,\mathrm{Re}(\bar x_k R_m x_{k-m})$. So the metric is a sum of terms that each depend on a symbol and its state, and the trellis search is exact. The proofs folder has the details.

## Complexity

The matched filter and the autocorrelation cost $O(N L + L^2)$. Each trellis step visits $M^{L-1}$ states; the ISI sum costs $O(L)$ per state and the branch metric $O(1)$ per symbol. So $N$ symbols cost $O(N M^{L-1}(M + L))$ time in the [word RAM](/word-ram/), with the metrics as numbers of fixed precision, and $O(N M^{L-1})$ space for the pointers. The trellis is the same size as the Forney receiver's, but no root finding and no backward filter are needed.

## Properties

- **Exact.** Same decisions as the Forney receiver on the same samples, for every noise realization, because the two metrics differ by a constant.
- **No whitening.** The noise in $z$ has the covariance $N_0 \mathbf{H}^H \mathbf{H}$, and the metric accounts for it. A channel with zeros on the unit circle is no problem.
- **Causal.** The matched filter output $z_k$ needs the samples up to $y_{k+L-1}$, a fixed delay. No anticausal filter runs over the whole block.
- **Only the autocorrelation.** The metric uses $z$ and $R$, not $h$ itself beyond the matched filter, so a receiver with a continuous-time matched filter only needs $R$.
- **Not a distance.** The branch metrics are not squared distances and can be negative. Suboptimal searches that compare metrics of paths of different length, or that prune by a threshold, need care.

## Variants and improvements

- **Adaptive.** Ungerboeck's receiver estimated the matched filter and the autocorrelation adaptively from decisions. [Per-survivor processing](/per-survivor-processing/) does the same along each survivor.
- **Reduced state.** The metric works with [reduced-state sequence estimation](/reduced-state-sequence-estimation/), but the ISI from the symbols after $x_k$ is in $z_k$ through the matched filter, so the minimum-phase prefilter of the Forney form is usually better for reduced-state receivers.
- **Soft outputs.** The [BCJR algorithm](/bcjr-algorithm/) can run on the same branch metrics, divided by $N_0$, for soft outputs.
- **Faster than Nyquist.** For [faster-than-Nyquist signaling](/faster-than-nyquist-signaling/), the matched filter output with its known autocorrelation is the natural model, and the Ungerboeck metric is common there.
- **Time-varying channels.** With a channel that changes from symbol to symbol, the metric uses $R_{k, m}$, the correlation of the pulses for $x_k$ and $x_{k-m}$.

## When to use it

Use it in place of the Forney receiver when the matched filter output is already available, when the channel has zeros near or on the unit circle, or when the receiver estimates the autocorrelation more easily than the channel itself. It costs about the same as the [Viterbi equalizer](/viterbi-equalizer/). For a [DFE](/decision-feedback-equalizer/) or a reduced-state search that decides early, use the [whitened matched filter](/whitened-matched-filter/) instead, because those receivers need the minimum-phase channel.

## Pitfalls

- **Euclidean distance on the matched filter output.** Measuring $|z_k - \text{expected}|^2$ looks natural but is not maximum likelihood, because the noise in $z$ is colored.
- **The factor 2.** The ISI term carries the factor 2 because each pair of symbols appears twice in the quadratic form. Dropping it changes the decisions.
- **Conjugates.** For complex symbols, $R_{-m} = \bar R_m$, and the metric uses $\bar x_k R_m x_{k-m}$ with $m \ge 1$. A real test channel hides a wrong conjugate.
- **Minimizing instead of maximizing.** The metric is a correlation. The Viterbi search must keep the largest one.
- **The ends of the block.** $z_k$ for the last symbols needs the samples after them, so the receiver must keep the full convolution output of length $N + L - 1$.

## Implementations

## History

Forney's receiver of 1972 needed a whitened matched filter in front of the Viterbi algorithm. In 1974, Ungerboeck showed that the Viterbi algorithm can work on the matched filter output with a modified metric, and built an adaptive receiver for carrier-modulated data transmission around it. The two forms were often compared later. They give the same maximum likelihood decisions, but behave differently in reduced-state and soft-output receivers. The Ungerboeck form is also common for faster-than-Nyquist signaling, where the matched filter output and its autocorrelation are known by design.

## References
