---
tag: 35K4A5
kind: algorithm
slug: whitened-matched-filter
name: Whitened matched filter
aliases:
- Forney whitened matched filter
area: communications/channel-estimation-and-equalization
level: advanced
summary: "A matched filter followed by a noise-whitening filter. It turns an ISI channel into a causal minimum-phase channel f with white noise, the front end of the Viterbi equalizer and the DFE."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {L: the number of channel taps, K: the number of samples, T: the number of root-finding iterations}
  time: {worst: O(T L^2 + K L)}
  space: {extra: O(K + L)}
properties: {deterministic: true, linear: true, needs_channel: true, preserves_ml_metric: true, output_minimum_phase: true}
history:
  year: 1972
  people: [G. David Forney Jr.]
  note: "Forney introduced the whitened matched filter as the front end of the maximum likelihood sequence estimator for ISI channels and showed that its sampled outputs are sufficient statistics."
prereqs: [matched-filter, minimum-phase, intersymbol-interference]
see_also: [viterbi-equalizer, ungerboeck-mlse-receiver, decision-feedback-equalizer, reduced-state-sequence-estimation, maximum-likelihood-sequence-estimation, durand-kerner-method, linear-prediction, mmse-dfe-canonical-theorem]
sources:
  - paper: "G. David Forney, Jr., Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972, pages 363 to 378"
    locator: "the whitened matched filter and the discrete-time white-noise model"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.3 (the optimum receiver for channels with ISI), with 9.3-2 (the discrete-time model and the noise-whitening filter)"
---

The whitened matched filter (WMF) is the front end that Forney proposed for sequence detection on channels with [intersymbol interference](/intersymbol-interference/). It is a [matched filter](/matched-filter/) followed by a noise-whitening filter. The matched filter alone keeps all the information about the symbols, but its output noise is colored, with the same spectrum as the folded channel $R(z) = H(z) H^*(1/z^*)$. The whitening filter $1/F^*(1/z^*)$ removes the color, where $F$ is the [minimum-phase](/minimum-phase/) spectral factor of $R$. The output is $y' = f * x + n'$ with white noise of the same variance. So the receiver sees a new causal channel $f$ of the same length, with its energy as early as possible. The [Viterbi equalizer](/viterbi-equalizer/) runs on $f$ with a Euclidean metric. The [Ungerboeck receiver](/ungerboeck-mlse-receiver/) uses the matched filter output directly and needs no whitening. The [decision feedback equalizer](/decision-feedback-equalizer/) and [reduced-state sequence estimation](/reduced-state-sequence-estimation/) work best on the minimum-phase channel, because they decide the first taps first.

## In plain words

A matched filter collects the energy of each symbol, but it makes neighbouring noise samples correlated. Many detectors assume the noise samples are independent. The whitening filter undoes the correlation without losing any information, and the noise becomes independent again. The price is that the channel the detector sees is a new one. Among all channels with the same frequency response magnitude, it is the one whose energy comes earliest. That is good for detectors that decide one symbol at a time, because the first tap carries the most signal.

## The problem

The input is a channel $h = (h_0, \ldots, h_{L-1})$ known at the receiver and the received samples $y[k] = \sum_l h_l\, x[k-l] + w[k]$, with $w$ white $\mathcal{CN}(0, N_0)$. The output is a channel $f = (f_0, \ldots, f_{L-1})$ with $f_0 > 0$, all zeros of $F(z)$ in the closed unit disk and $|F(e^{j\omega})| = |H(e^{j\omega})|$, and filtered samples $y'[k] = \sum_l f_l\, x[k-l] + n'[k]$ with $n'$ white $\mathcal{CN}(0, N_0)$. The two models give the same maximum likelihood decisions.

## The algorithm

The folded spectrum $R(z) = \sum_k R_k z^{-k}$, with $R_k = \sum_l h_{l+k} \bar h_l$, has the zeros of $H(z)$ and their conjugate reciprocals. A spectral factor of $R$ keeps one zero of each pair. The minimum-phase factor keeps the one inside the unit circle. When $h$ is known, the zeros of $H$ give the factor directly.

```pseudo id=main
WHITENED-MATCHED-FILTER(h, y)
L1  f ← MIN-PHASE-FACTOR(h)
L2      ρ_1, …, ρ_{L-1} ← the roots of h0 z^(L-1) + h1 z^(L-2) + … + h_{L-1}
L3      ρ'_i ← ρ_i if |ρ_i| ≤ 1, else 1/conj(ρ_i)          ▷ reflect into the unit disk
L4      f ← γ Π_i (1 - ρ'_i z⁻¹),  γ = |h0| Π_{|ρ_i|>1} |ρ_i|
L5  z[k] ← Σ_l conj(h[l]) y[k + l]  for every k            ▷ the matched filter
L6  for k ← K - 1 down to 0                                 ▷ the whitening filter 1/F*(1/z*)
L7      y'[k] ← (z[k] - Σ_{l≥1} conj(f[l]) y'[k + l]) / conj(f[0])
L8  return f, y'
```

Line L2 finds the zeros with the [Durand-Kerner method](/durand-kerner-method/). Line L3 keeps the magnitude response: a zero $\rho$ outside the circle and the zero $1/\bar\rho$ give the same $|1 - \rho z^{-1}|$ up to the factor $|\rho|$, which line L4 puts into $\gamma$. Line L5 is the matched filter, which correlates $y$ with $h$. Lines L6 and L7 apply $1/F^*(1/z^*)$, an anticausal filter, by back substitution from the end of the block. If only $R$ is known, factor $z^{L-1} R(z)$ instead and keep the $L-1$ roots inside the circle.

## Example

Take $h = (0.5, 1)$, a channel whose second tap is larger than its first. Its zero is at $-2$, outside the unit circle. Line L3 reflects it to $-0.5$, and line L4 gives $\gamma = 0.5 \times 2 = 1$, so $f = (1, 0.5)$. Both channels have $R_0 = 1.25$ and $R_1 = 0.5$. Send $x = (1, -1, -1, 1, 1)$ with no noise:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $y[k] = 0.5\, x[k] + x[k-1]$ | 0.5 | 0.5 | -1.5 | -0.5 | 1.5 | 1 |
| $z[k] = 0.5\, y[k] + y[k+1]$ | 0.75 | -1.25 | -1.25 | 1.25 | 1.75 | 0.5 |
| $y'[k] = z[k] - 0.5\, y'[k+1]$ | 1 | -0.5 | -1.5 | 0.5 | 1.5 | 0.5 |
| $(f * x)[k] = x[k] + 0.5\, x[k-1]$ | 1 | -0.5 | -1.5 | 0.5 | 1.5 | 0.5 |

The back substitution starts at $k = 5$ with $y'[5] = z[5] = 0.5$. The output is $f * x$ exactly. On the original channel, a zero-forcing DFE with one feedforward tap has the noise gain $1/|h_0|^2 = 4$. On the whitened channel it has $1/f_0^2 = 1$, which is 6 dB better.

On the channel B of Proakis, $h = (0.407, 0.815, 0.407)$, the zeros are at $-0.9516$ and $-1.0508$. The second one is reflected to $-0.9516$, and $f = (0.42768, 0.81400, 0.38732)$. The change is small, because the channel is almost linear phase with both zeros near the circle.

## Correctness

**Claim.** $|F| = |H|$ on the unit circle and $f$ is minimum phase. Without noise, $y' = f * x$ exactly. For any noise and any candidate sequence $x$, $\|y - h * x\|^2 - \|y' - f * x\|^2 = \|y\|^2 - \|y'\|^2$, so maximum likelihood on $y'$ with the channel $f$ gives the same decisions as on $y$ with $h$. On an infinite sequence, the noise after the filter is white with variance $N_0$.

**Key step.** Equal magnitudes give equal autocorrelations, so $\mathbf{H}^H \mathbf{H} = \mathbf{F}^H \mathbf{F}$ for the full convolution matrices. The back substitution solves $\mathbf{F}_s^H y' = \mathbf{H}_s^H y$, so the cross terms of the two metrics agree too. The noise passes through $H^*(1/z^*)/F^*(1/z^*)$, which is allpass. The proofs folder has the details, and also the proof that $f$ has the largest partial energies among all factors.

## Complexity

The roots cost $O(T L^2)$ for $T$ iterations of Durand-Kerner on a polynomial of degree $L-1$, and building $f$ costs $O(L^2)$. Lines L5 to L7 cost $O(L)$ per sample, so $K$ samples cost $O(T L^2 + K L)$ in the [real RAM](/real-ram/), with $O(K + L)$ extra space for $z$ and $y'$. The filter needs the whole block before it can start, because it runs backward. A stream receiver uses a truncated FIR approximation of $1/F^*(1/z^*)$ with a delay.

## Properties

- **Information lossless.** The matched filter outputs are sufficient statistics, and the whitening filter is invertible, so no information is lost.
- **Same metric.** The Euclidean metric on $y'$ differs from the metric on $y$ by a constant for each block, so every maximum likelihood detector gives the same answer on both.
- **White noise.** The noise map $H^*(1/z^*)/F^*(1/z^*)$ is allpass, so the noise stays white with variance $N_0$. In a finite block, the samples near the end carry an edge effect.
- **Causal and minimum phase.** The output channel has $L$ taps, no precursors, and the most energy in its first taps among all channels with the same magnitude response.
- **Anticausal filter.** $1/F^*(1/z^*)$ is stable only as an anticausal filter, so a block receiver runs it backward and a stream receiver needs a delay.
- **Unit circle zeros.** If $H$ has a zero on the unit circle, the whitening filter has a pole on the circle and the inverse is unstable. The [Ungerboeck receiver](/ungerboeck-mlse-receiver/) avoids the whitening step.

## Variants and improvements

- **From the autocorrelation.** If only $R_k$ is known, factor the polynomial $z^{L-1} R(z)$ of degree $2L-2$ and keep the roots inside the circle. Other methods are Bauer's method, the Cholesky factorization of a large Toeplitz matrix, and the cepstral method.
- **Linear prediction.** The whitening filter is a prediction error filter for the matched filter noise, so a long [linear prediction](/linear-prediction/) filter from the Levinson recursion approximates it.
- **MMSE prefilter.** The feedforward filter of the MMSE-DFE also leaves a channel with its energy first, and it tends to the WMF at high SNR. At lower SNR it allows a little precursor ISI and bias for less noise. For RSSE and DFE receivers it often replaces the WMF.
- **Fractionally spaced front end.** With more than one sample per symbol, the matched filter is applied in continuous time or at the higher rate, and the output is then sampled at the symbol rate before whitening.

## When to use it

Use the WMF as the front end of a [Viterbi equalizer](/viterbi-equalizer/) with a Euclidean metric, of a [DFE](/decision-feedback-equalizer/) or of [reduced-state sequence estimation](/reduced-state-sequence-estimation/), when the channel is known and has no zeros on the unit circle. For a full Viterbi equalizer, the [Ungerboeck receiver](/ungerboeck-mlse-receiver/) avoids the whitening and works on the matched filter output. For suboptimal detectors that decide early, the minimum-phase output is the main reason to use the WMF.

## Pitfalls

- **Running the whitening filter forward.** $1/F^*(1/z^*)$ is unstable as a causal filter, because its pole $1/\bar\rho'$ lies outside the circle. Run it backward or use a truncated anticausal FIR.
- **Taking the maximum-phase factor.** Keeping the roots outside the circle gives a valid factor with the energy last, which ruins a DFE or an RSSE.
- **Forgetting the conjugates.** For complex channels, the matched filter correlates with $\bar h$, and the whitening uses $\bar f$. A real test channel hides the mistake.
- **Zeros near the circle.** The whitening filter then decays slowly, so the edge effect at the block end is long, and the root finder needs more iterations. The channel B of Proakis is such a case.
- **A gain error in $f$.** The scale $\gamma$ must give $\|f\|^2 = \|h\|^2$. A wrong scale changes the noise variance that the metric assumes.

## Implementations

## History

In 1972, Forney showed that the matched filter outputs at the symbol rate are sufficient statistics for the transmitted sequence on a linear Gaussian channel with ISI. He then whitened their noise with the minimum-phase spectral factor, obtaining a causal channel with white noise, and applied the Viterbi algorithm to it. The WMF made the maximum likelihood sequence estimator a practical receiver structure. In 1974, Ungerboeck showed that the Viterbi algorithm can work on the matched filter outputs directly, with a modified metric. The minimum-phase prefilter later became a standard part of reduced-state receivers.

## References
